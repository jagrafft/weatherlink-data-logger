from json import loads as jsonloads
from math import atan
from pathlib import Path
from redis import Redis
from sys import exit
from urllib.request import Request, urlopen


def difference_in_radians(S: dict, LMR: dict) -> dict:
    """
    Calculate the difference, in radians, between values in a `S`ample
    and the set of cached Last Most Recent (`LMR`) values.
    """
    diffs = {}
    shared_keys = {*S.keys()}.intersection({*LMR["values"].keys()})

    for k in shared_keys:
        if k != "ts":
            value_diff = round(abs(S[k] - LMR["values"][k]), 3)
            if value_diff > 0:
                diffs[k] = round(atan(value_diff / (S["ts"] - LMR["timestamp"])), 3)
            else:
                diffs[k] = 0.0

    return diffs


def get_or_set_lmr_in_redis(r: Redis, wlsample: dict, keys: list) -> dict:
    """
    Get Last Most Recent (LMR) values and their associated timestamps
    from the Redis instance, or sample from the WeatherLink device then
    initialize the database.
    """
    values = {}
    updates = {}

    for key in keys:
        lmr_val_at_key = r.get(key)

        if lmr_val_at_key is None:
            if key in wlsample:
                values[key] = wlsample[key]
                updates[key] = wlsample["ts"]

                # Write to Redis
                r.set(key, wlsample[key])
                r.set(f"{key}_ts", wlsample["ts"])
        else:
            lmr_val_update = int(r.get(f"{key}_ts"))
            values[key] = float(lmr_val_at_key)
            updates[key] = lmr_val_update

    return {"timestamp": wlsample["ts"], "values": values, "updates": updates}


def sample_weatherlink(url: str, keys_to_retain: list) -> dict:
    """
    Sample data from the WeatherLink device at `url` then filter to
    return a dictionary with only the keys listed in `keys_to_retain`.
    """
    # Open URL then read response
    request = Request(method="GET", url=url)

    with urlopen(request) as response:
        body = response.read()

    # Convert response from a JSON string to a Dictionary
    json = jsonloads(body)

    # Convenience variable for accessing contents of `data` key
    data = json["data"]

    # Seed packet with timestamp from Weatherlink service
    packet = {"ts": data["ts"]}

    # Iterate over `conditions` key to extract desired key-value pairs
    # then assign them to `packet`
    for condition in data["conditions"]:
        for (k, v) in condition.items():
            if k in keys_to_retain and v is not None:
                packet[k] = v

    return packet


def stop_service(sig, frame):
    """
    Stop execution of program. Called by `signal` on `SIGINT`.
    """
    print("Stopping service...")
    exit(0)
