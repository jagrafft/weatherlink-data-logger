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
    current_conditions = current_conditions_json["data"]

    # Seed current_conditions with timestamp from Weatherlink service
    current_conditions_data = [pa.array([current_conditions["ts"]], type=pa.int64())]

    # current_conditions_names = ["timestamp"]

    # Iterate over `conditions` key to extract desired key-value pairs
    # then assign them to `current_conditions`
    for conditions in current_conditions["conditions"]:
        retained_pairs = {
            k: v
            for (k, v) in conditions.items()
            if (k in keys_to_retain) and (v is not None)
        }

        for (k, v) in retained_pairs.items():
            current_conditions_data.append(pa.array([v], type=pa.float64()))

    return current_conditions_data
