import backoff
import requests

from datetime import datetime
from json import loads as jsonloads
from math import atan
from pytomlpp import load as tomload
from pathlib import Path
from redis import Redis
from sys import exit
from time import sleep
from urllib.request import Request, urlopen

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

# Set session variables from TOML config
KEYS_TO_RETAIN = wlconfig["weatherlink"]["keys_to_retain"]
SLEEP_DURATION = wlconfig["weatherlink"]["duration"]
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)

# TODO: Function likely indicates a refactor of application is necessary
def bootstrap_lmr(r: Redis, current_conditions: dict, keys: list) -> list:
    """
    Get Last Most Recent (LMR) values and their associated timestamps
    from the Redis instance, or initialize the database from `current_conditions`.
    """
    values = {}
    timestamps = {}

    for key in keys:
        lmr_val_at_key = r.get(key)

        if lmr_val_at_key is None:
            if key in current_conditions:
                values[key] = current_conditions[key]
                timestamps[key] = current_conditions["ts"]

                # Write to Redis
                r.set(key, current_conditions[key])
                r.set(f"{key}_ts", current_conditions["ts"])
        else:
            lmr_update_ts = int(r.get(f"{key}_ts"))
            values[key] = float(lmr_val_at_key)
            timestamps[key] = lmr_update_ts

    # Use `current_conditions["ts"]` as Last Most Recent timestamp
    return [values, timestamps, current_conditions["ts"]]


def combine_packet(current_conditions: dict, lmr_values: dict, diffs: dict) -> dict:
    """
    Merge `current_conditions` and `lmr_values`. Used for investigation.
    WARNING: Susceptible to deprecation.
    """
    combined_packet = {
        k: {"cur": None, "last": None, "theta": None}
        for k in current_conditions.keys()
        if k != "ts"
    }

    for k in combined_packet.keys():
        combined_packet[k]["cur"] = current_conditions[k]
        combined_packet[k]["last"] = lmr_values[k]
        combined_packet[k]["theta"] = diffs[k]

    combined_packet["wl_ts"] = current_conditions["ts"]
    combined_packet["ts"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return combined_packet


def difference_in_radians(
    current_conditions: dict, lmr_values: dict, lmr_ts: int
) -> dict:
    """
    Calculate the difference, in radians, between values in a `S`ample
    and the set of cached Last Most Recent (`LMR`) values.
    """
    shared_keys = [
        k
        for k in {*current_conditions.keys()}.intersection({*lmr_values.keys()})
        if k != "ts"
    ]

    ts_diff = current_conditions["ts"] - lmr_ts

    diffs = {}

    for k in shared_keys:
        value_diff = abs(current_conditions[k] - lmr_values[k])
        diffs[k] = round(atan(value_diff / ts_diff), 3)

    return diffs


@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    on_backoff=sleep(SLEEP_DURATION),
)
def get_current_conditions(url: str, keys_to_retain: list) -> dict:
    """
    Sample data from the WeatherLink device at `url` then filter to
    return a dictionary with only the keys listed in `keys_to_retain`.
    """
    # Open URL then read response
    request = Request(method="GET", url=url)

    with urlopen(request) as response:
        body = response.read()

    # Convert response from a JSON string to a Dictionary
    current_conditions_json = jsonloads(body)

    # Convenience variable for accessing contents of `data` key
    current_conditions_data = current_conditions_json["data"]

    # Seed current_conditions with timestamp from Weatherlink service
    current_conditions_return = {"ts": current_conditions_data["ts"]}

    # Iterate over `conditions` key to extract desired key-value pairs
    # then assign them to `current_conditions`
    for conditions in current_conditions_data["conditions"]:
        retained_pairs = {
            k: v
            for (k, v) in conditions.items()
            if (k in keys_to_retain) and (v is not None)
        }

        for (k, v) in retained_pairs.items():
            current_conditions_return[k] = v

    return current_conditions_return


def stop_service(sig, frame):
    """
    Stop execution of program. Called by `signal` on `SIGINT`.
    """
    print("Stopping service...")
    exit(0)
