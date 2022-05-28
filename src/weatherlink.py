from functools import partial
from json import loads as jsonloads
from math import atan
from pathlib import Path
from pytomlpp import load as tomload
from signal import SIGINT, signal
from sys import exit
from time import sleep
from tinydb import TinyDB, Query
from urllib.request import Request, urlopen

from datetime import datetime
import redis

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

###
# RAI Cloud database connection
# from railib import api, config
# con = api.Context(**config.read(profile=wlconfig["dbs"]["rai"]["profile"]))

# Redis connection
# Used to persist Last Most Recent (LMR) values
r = redis.Redis(
    host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"]
)
r.select(13)
###

###
# Weatherlink service URL path
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)

print(WEATHERLINK_URL_PATH)
###


def diff_sample_with_lmr(LMR: dict, S: dict) -> dict:
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


def get_last_most_recent_vals() -> dict:
    values = {}
    updates = {}
    wlsample = sample_weatherlink()

    for key in wlconfig["weatherlink"]["keys_to_retain"]:
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


def sample_weatherlink() -> dict:
    ###
    # For testing with local file(s)
    # Make sure to change
    # - `from json import loads as jsonloads` => `from json import load as jsonload`
    # - `# from datetime import datetime` => `from datetime import datetime`
    # with open(
    #     Path(__file__).parent.parent.parent / "docs" / "example_packet.json"
    # ) as f:
    #     json = jsonload(f)
    ###
    # Open URL then read response
    request = Request(method="GET", url=WEATHERLINK_URL_PATH)

    with urlopen(request) as response:
        body = response.read()

    # Convert response from a JSON string to a Dictionary
    json = jsonloads(body)

    # Convenience variable for accessing contents of `data` key
    data = json["data"]

    # Seed packet with timestamp from Weatherlink service
    packet = {"ts": data["ts"]}

    # Iterate over `conditions` key to extract desired key-value pairs
    for condition in data["conditions"]:
        for (k, v) in condition.items():
            if k in wlconfig["weatherlink"]["keys_to_retain"] and v is not None:
                packet[k] = v

    return packet


# Stop execution of program
def stop_service(sig, frame):
    print("Stopping service...")
    exit(0)


# Listener for `CTRL-C` event
signal(SIGINT, stop_service)

# Populate `last_most_recent` data from Redis
last_most_recent = get_last_most_recent_vals()
sleep(wlconfig["weatherlink"]["interval"])

# Database for persisting `diff`s (for validation and testing)
diff_db = TinyDB(f"{wlconfig['dbs']['tinydb']['path']}/lmr_diffs.json")

# Loop for requesting data from Weatherlink service
# and writing it to RAI Cloud
while True:
    # Sample (approximately) current conditions round sensor array
    current = sample_weatherlink()

    # `diff` current sample with last most recent data written to DB
    diffs = diff_sample_with_lmr(last_most_recent, current)

    # Update last most recent timestamp
    last_most_recent["timestamp"] = current["ts"]

    # Combine packets above for study of output
    agg = {
        k: {
            "ts": current["ts"],
            "cur": current[k],
            "last": last_most_recent["values"][k],
            "theta": diffs[k],
            "write": (
                "true"
                if diffs[k] > wlconfig["weatherlink"]["theta_threshold"]
                else "false"
            ),
        }
        for k in current.keys()
        if k != "ts"
    }

    agg["write_ts"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    diff_db.insert(agg)

    print(agg, "\n")

    # DATABASE UPDATE STRATEGY HERE...
    # Write values exceeding threshold to LMR caches
    for (k, theta) in diffs.items():
        if theta > wlconfig["weatherlink"]["theta_threshold"]:
            # Update session dictionary
            last_most_recent["values"][k] = current[k]
            last_most_recent["updates"][k] = current["ts"]

            # Update Redis
            r.set(k, current[k])
            r.set(f"{k}_ts", current["ts"])

    # Wait for next request
    sleep(wlconfig["weatherlink"]["interval"])
