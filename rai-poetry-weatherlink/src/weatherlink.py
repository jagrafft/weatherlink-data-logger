from datetime import datetime

from dotenv import load_dotenv
from json import load
from os import getenv
from railib import api, config
from signal import SIGINT, signal
from sys import exit
from time import sleep
from urllib.request import Request, urlopen

load_dotenv()

# Set global variables for session using `.env` file
# COMPUTE = getenv("RAI_COMPUTE")
# DATABASE = getenv("RAI_DB")
REQUEST_INTERVAL = int(getenv("REQUEST_INTERVAL"))
WEATHERLINK_URL_PATH = f"{getenv('WEATHERLINK_URL')}{getenv('WEATHERLINK_PATH')}"

# RAI Cloud database connection
# con = api.Context(**config.read(profile=getenv("RAI_PROFILE")))

# List of data keys to retain
keys_to_retain = [
    "bar_sea_level",
    "dew_point",
    "hum",
    "hum_in",
    "solar_rad",
    "temp",
    "temp_in",
    "timestamp",
    "uv_index",
    "wind_dir_last",
    "wind_speed_last",
]


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
    # request = Request(method="GET", url=WEATHERLINK_URL_PATH)

    # with urlopen(request) as response:
    #     body = response.read()

    # Convert response from a JSON string to a Dictionary
    # json = loads(body)

    ###
    # For testing with local file(s)
    # Make sure to change
    # - `from json import loads` => `from json import load`
    # - `# from datetime import datetime` => `from datetime import datetime`
    with open("docs/example_packet.json") as f:
        json = load(f)
    ###

    # Convenience variable for accessing contents of `data` key
    data = json["data"]

    # Add seed restricted packet with timestamp from Weatherlink service
    packet = {"ts": data["ts"]}

    # Iterate over `conditions` key to extract desired key-value pairs
    for condition in data["conditions"]:
        for (k, v) in condition.items():
            if k in keys_to_retain:
                packet[k] = v

    print(datetime.now())
    print(packet)

    # DATABASE UPDATE STRATEGY HERE...

    # Wait for next request
    sleep(REQUEST_INTERVAL)
