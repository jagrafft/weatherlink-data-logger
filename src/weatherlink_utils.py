import backoff
import pyarrow as pa
import requests

from datetime import datetime
from json import loads as jsonloads
from math import atan
from pytomlpp import load as tomload
from pathlib import Path
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


@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
    on_backoff=sleep(SLEEP_DURATION),
)
def get_current_conditions_batch(
    url: str,
    keys_to_retain: list,
    schema,
    sleep_duration: float,
    batch_size: int = 1000,
) -> dict:
    """
    Sample data from the WeatherLink device at `url` then filter to
    return a dictionary with only the keys listed in `keys_to_retain`.
    """
    current_conditions_batch = {k: [] for k in keys_to_retain}

    for i in range(1, batch_size + 1, 1):
        print(f"{i}/{batch_size}: Sampling WeatherLink device...", end="")
        # Open URL then read response
        request = Request(method="GET", url=url)

        with urlopen(request) as response:
            body = response.read()

        # Convert response from a JSON string to a Dictionary
        current_conditions_json = jsonloads(body)

        # Convenience variable for accessing contents of `data` key
        current_conditions = current_conditions_json["data"]

        current_conditions_batch["timestamp"].append(current_conditions["ts"])

        # Iterate over `conditions` key to extract desired key-value pairs
        # then assign them to `current_conditions`
        for conditions in current_conditions["conditions"]:
            for (k, v) in conditions.items():
                if k in keys_to_retain:
                    current_conditions_batch[k].append(v)

        print("DONE")
        sleep(sleep_duration)

    current_conditions_data = []

    for (k, v) in current_conditions_batch.items():
        current_conditions_data.append(pa.array(v))

    return pa.record_batch(current_conditions_data, schema)
