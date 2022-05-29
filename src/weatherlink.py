from pathlib import Path
from pytomlpp import load as tomload
from redis import Redis
from signal import SIGINT, signal
from time import sleep
from tinydb import TinyDB
from weatherlink_utils import (
    difference_in_radians,
    get_or_set_lmr_in_redis,
    get_current_conditions,
    stop_service,
)

from datetime import datetime

### INIT SESSION ###
# Listener for `CTRL-C` event
signal(SIGINT, stop_service)

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

# Set session variables from TOML config
KEYS_TO_RETAIN = wlconfig["weatherlink"]["keys_to_retain"]
SLEEP_INTERVAL = wlconfig["weatherlink"]["interval"]
THETA_THRESHOLD = wlconfig["weatherlink"]["theta_threshold"]
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)
###

### INIT DATABASE CONNECTIONS ###
# RAI Cloud database connection
# from railib import api, config
# con = api.Context(**config.read(profile=wlconfig["dbs"]["rai"]["profile"]))

# Redis connection
# Used to persist Last Most Recent (LMR) values
redis_con = Redis(
    host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"]
)
redis_con.select(13)

# TinyDB instance for persisting `diff`s
# TEMPORARY
diff_db = TinyDB(f"{wlconfig['dbs']['tinydb']['path']}/lmr_diffs.json")
###

### INIT WEATHERLINK DATA FOR SESSION ###
print(WEATHERLINK_URL_PATH)

# Sample from WeatherLink weather station
current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)

# Populate session variables to hold Last Most Recent data
LMR_VALUES, LMR_TIMESTAMPS, LMR_REFERENCE_TS = get_or_set_lmr_in_redis(
    redis_con, current_conditions, KEYS_TO_RETAIN
)
sleep(SLEEP_INTERVAL)
###

### REQUEST DATA FROM WEATHERLINK SERVICE TILL `SIGINT` IS ISSUED ###
while True:
    # Sample (approximately) current conditions round sensor array
    current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)

    # `diff` current conditions with last most recent data written to DB
    diffs = difference_in_radians(current_conditions, LMR_VALUES, LMR_REFERENCE_TS)

    # Update last most recent timestamp
    LMR_REFERENCE_TS = current_conditions["ts"]

    ### Combine `current_conditions` and `diffs` for study of output (temporary) ###
    combined_packet = {
        k: {"cur": None, "last": None, "theta": None, "write": None}
        for k in current_conditions.keys()
        if k != "ts"
    }

    for k in combined_packet.keys():
        combined_packet[k]["cur"] = current_conditions[k]
        combined_packet[k]["last"] = LMR_VALUES[k]
        combined_packet[k]["theta"] = diffs[k]
        combined_packet[k]["write"] = "true" if diffs[k] > THETA_THRESHOLD else "false"

    combined_packet["wl_ts"] = current_conditions["ts"]
    combined_packet["ts"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    diff_db.insert(combined_packet)

    print(combined_packet, "\n")
    ###

    ### DATABASE UPDATE(S) ###
    for (k, theta) in diffs.items():
        # Persist values exceeding threshold
        if theta > THETA_THRESHOLD:
            # Update session dictionaries
            LMR_VALUES[k] = current_conditions[k]
            LMR_TIMESTAMPS[k] = current_conditions["ts"]

            # Update Redis
            redis_con.set(k, current_conditions[k])
            redis_con.set(f"{k}_ts", current_conditions["ts"])
    ###

    # Pause before making next request
    sleep(SLEEP_INTERVAL)
###
