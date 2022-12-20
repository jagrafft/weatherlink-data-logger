from datetime import datetime
from json import loads as jsonloads
from pathlib import Path
from pytomlpp import load as tomload
from redis import Redis
from signal import SIGINT, signal
from sys import exit
from time import sleep
from urllib.request import Request, urlopen


# Function to halt service
def stop_service(sig, frame):
    """
    Stop execution of program. Called by `signal` on `SIGINT`.
    """
    print("Stopping service...")
    exit(0)


# Listener for `CTRL-C` event
signal(SIGINT, stop_service)

# Load TOML configuration for app from 'config' directory
config_path = Path(__file__).parent.parent / "config" / "wlconfig.toml"

try:
    wlconfig = tomload(config_path)
except:
    print(f"Error loading TOML at '{config_path}', exiting...")
    exit()

# Set session variables from TOML config
KEYS_TO_RETAIN = wlconfig["weatherlink"]["keys_to_retain"]
SLEEP_INTERVAL = wlconfig["weatherlink"]["interval"]
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)

# Redis connection
# Used to persist Last Most Recent (LMR) values
redis_con = Redis(
    host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"]
)

redis_con.select(wlconfig["dbs"]["redis"]["database"])


# Function to poll WeatherLink station
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


# Print URL
print(WEATHERLINK_URL_PATH)

# Sample (approximately) current conditions round sensor array
while True:
    current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)

    print(current_conditions)

    # Push to Redis Stream
    redis_con.xadd(wlconfig["dbs"]["redis"]["stream_name"], current_conditions)

    # Pause before making next request
    sleep(SLEEP_INTERVAL)
###
