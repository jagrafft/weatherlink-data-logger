from json import loads as jsonloads
from pathlib import Path
from pytomlpp import load as tomload
from signal import SIGINT, signal
from sys import exit
from time import sleep

from datetime import datetime

# from railib import api, config
from urllib.request import Request, urlopen

# Load TOML configuration for app from 'config' directory
wlconfig = tomload(Path(__file__).parent.parent / "config" / "wlconfig.toml")

# Weatherlink service URL path
WEATHERLINK_URL_PATH = (
    f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
)

# RAI Cloud database connection
# con = api.Context(**config.read(profile=wlconfig["dbs"]["rai"]["profile"]))

# Stop execution of program
def stop_service(sig, frame):
    print("Stopping service...")
    exit(0)


# Listener for `CTRL-C` event
signal(SIGINT, stop_service)

# Loop for requesting data from Weatherlink service
# and writing it to RAI Cloud
while True:
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

    # `print` statements used for testing
    print(datetime.now())
    print(packet)

    # DATABASE UPDATE STRATEGY HERE...
    # wlconfig["dbs"]["rai"]["compute"]
    # wlconfig["dbs"]["rai"]["db"]

    # Wait for next request
    sleep(wlconfig["weatherlink"]["interval"])
