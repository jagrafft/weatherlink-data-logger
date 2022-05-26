from functools import partial
from json import loads as jsonloads
from math import atan
from pathlib import Path
from pytomlpp import load as tomload

# from railib import api, config
from signal import SIGINT, signal
from sys import exit
from time import sleep
from tinydb import TinyDB, Query
from urllib.request import Request, urlopen

from datetime import datetime

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

# Weatherlink service URL path
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)

print(WEATHERLINK_URL_PATH)
# RAI Cloud database connection
# con = api.Context(**config.read(profile=wlconfig["dbs"]["rai"]["profile"]))


def diff_sample_with_lmr(LMR: dict, S: dict) -> dict:
    shared_keys = {*S.keys()}.intersection({*LMR["values"].keys()})

    return {
        k: round(
            atan(abs(S[k] - LMR["values"][k]) / (S["ts"] - LMR["timestamp"])),
            # atan(abs(S[k] - LMR["values"][k]) / wlconfig["weatherlink"]["interval"]),
            3,
        )
        for k in shared_keys
        if k != "ts"
    }


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

# Database for persisting last-most-recent values
db = TinyDB(f"{wlconfig['dbs']['tinydb']['lmr_path']}/last_most_recent.json")

if len(db.all()) == 0:
    print("No last most recent data avaialble, polling WeatherLink station...")
    wl_sample = sample_weatherlink()

    ts = wl_sample["ts"]
    del wl_sample["ts"]

    last_most_recent = {
        "values": wl_sample,
        "updates": {k: ts for k in wl_sample},
        "timestamp": ts,
    }

    db.insert(last_most_recent)
    sleep(wlconfig["weatherlink"]["interval"])
else:
    print("Last most recent data available, loading...")
    # TODO improve strategy
    last_most_recent = db.all()[0]

# Database for persisting `diff`s (for validation and testing)
diff_db = TinyDB(f"{wlconfig['dbs']['tinydb']['lmr_path']}/lmr_diffs.json")

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
        k: {"cur": current[k], "last": last_most_recent["values"][k], "theta": diffs[k]}
        for k in current.keys()
        if k != "ts"
    }
    agg["ts"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    diff_db.insert(agg)

    print(agg, "\n")

    # DATABASE UPDATE STRATEGY HERE...

    # Wait for next request
    sleep(wlconfig["weatherlink"]["interval"])
