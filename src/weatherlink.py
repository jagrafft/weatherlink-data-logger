from pathlib import Path
from pytomlpp import load as tomload
from redis import Redis
from signal import SIGINT, signal
from time import sleep
from tinydb import TinyDB
from weatherlink_utils import (
    difference_in_radians,
    get_or_set_lmr_in_redis,
    sample_weatherlink,
    stop_service,
)

from datetime import datetime

# Listener for `CTRL-C` event
signal(SIGINT, stop_service)

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

### DATABASE CONNECTIONS ###
# RAI Cloud database connection
# from railib import api, config
# con = api.Context(**config.read(profile=wlconfig["dbs"]["rai"]["profile"]))

# Redis connection
# Used to persist Last Most Recent (LMR) values
r = Redis(host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"])
r.select(13)

# TinyDB instance for persisting `diff`s
# TEMPORARY
diff_db = TinyDB(f"{wlconfig['dbs']['tinydb']['path']}/lmr_diffs.json")
###

### WEATHERLINK ###
# Weatherlink service URL path
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)
print(WEATHERLINK_URL_PATH)

# Sample from WeatherLink weather station
current = sample_weatherlink(
    WEATHERLINK_URL_PATH, wlconfig["weatherlink"]["keys_to_retain"]
)

# Populate `last_most_recent` dictionary
last_most_recent = get_or_set_lmr_in_redis(
    r, current, wlconfig["weatherlink"]["keys_to_retain"]
)
sleep(wlconfig["weatherlink"]["interval"])
###

# Loop for requesting data from Weatherlink service interminably
while True:
    # Sample (approximately) current conditions round sensor array
    current = sample_weatherlink(
        WEATHERLINK_URL_PATH, wlconfig["weatherlink"]["keys_to_retain"]
    )

    # `diff` current sample with last most recent data written to DB
    diffs = difference_in_radians(current, last_most_recent)

    # Update last most recent timestamp
    last_most_recent["timestamp"] = current["ts"]

    # Combine packets above for study of output
    # TEMPORARY
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
