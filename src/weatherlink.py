from pathlib import Path
from redis import Redis
from signal import SIGINT, signal
from time import sleep
from tinydb import TinyDB
from weatherlink_utils import (
    bootstrap_lmr,
    combine_packet,
    difference_in_radians,
    get_current_conditions,
    stop_service,
    wlconfig,
    KEYS_TO_RETAIN,
    SLEEP_DURATION,
    WEATHERLINK_URL_PATH,
)

from datetime import datetime

### INIT SESSION ###
# Listener for `CTRL-C` event
signal(SIGINT, stop_service)
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
redis_con.select(wlconfig["dbs"]["redis"]["n"])

# TinyDB instance for persisting `diff`s
# TEMPORARY
persistence_layer = TinyDB(
    f"{wlconfig['dbs']['tinydb']['path']}/{datetime.now()}-wl_data_stream.json"
)
###

### INIT WEATHERLINK DATA FOR SESSION ###
print(WEATHERLINK_URL_PATH)

# Sample from WeatherLink weather station
current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)

# Populate session variables to hold Last Most Recent data
LMR_VALUES, LMR_TIMESTAMPS, LMR_REFERENCE_TS = bootstrap_lmr(
    redis_con, current_conditions, KEYS_TO_RETAIN
)
sleep(SLEEP_DURATION)
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
    combined_packet = combine_packet(current_conditions, LMR_VALUES, diffs)
    persistence_layer.insert(combined_packet)

    print(combined_packet, "\n")
    ###

    ### Write updated LMR values to Redis database ###
    # WARNING: Temporary, will be deprecated
    for (k, v) in current_conditions.items():
        # Update session dictionaries
        LMR_VALUES[k] = v
        LMR_TIMESTAMPS[k] = current_conditions["ts"]

        # Update Redis
        redis_con.set(k, v)
        redis_con.set(f"{k}_ts", current_conditions["ts"])
    ###

    # Pause before making next request
    sleep(SLEEP_DURATION)
###
