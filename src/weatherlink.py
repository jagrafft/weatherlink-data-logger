from json import loads as jsonloads
from pathlib import Path
from pytomlpp import load as tomload
from signal import SIGINT, signal
from sys import exit
from time import sleep, time_ns
from tinydb import TinyDB, Query
from urllib.request import Request, urlopen

from datetime import datetime

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

# Weatherlink service URL path
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)


def sample():
    # Open URL then read response
    request = Request(method="GET", url=WEATHERLINK_URL_PATH)

    with urlopen(request) as response:
        body = response.read()

    # Convert response from a JSON string to a Dictionary
    json = jsonloads(body)

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

db = TinyDB(wlconfig["dbs"]["tinydb"]["lmr_path"])

if len(db.all()) == 0:
    packet = {k: v for (k, v) in sample().items() if k != "ts"}
    ts = time_ns()

    # lmr_values = [{"key": k, "value": v, "ts": ts} for (k,v) in packet.items()] # use instead
    lmr_values = {"values": packet, "last_updates": {k: ts for k in packet.keys()}}
    db.insert(lmr_values)
else:
    lmv_values = db.all()

print(lmr_values)

# Loop for requesting data from Weatherlink service
# and writing it to RAI Cloud
while True:
    packet = sample()

    # `print` statements used for testing
    print(datetime.now())
    print(packet)

    # DATABASE UPDATE STRATEGY HERE...

    # Wait for next request
    sleep(wlconfig["weatherlink"]["interval"])
