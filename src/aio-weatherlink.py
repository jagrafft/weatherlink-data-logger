import asyncio
import aiohttp

# from datetime import datetime
# from json import loads as jsonloads
from pathlib import Path
from pytomlpp import load as tomload

# from redis import Redis
# from signal import SIGINT, signal
from sys import exit
from time import sleep


def extract_wl_kvs(data: dict, keys: list) -> dict:
    # Extracted Key-Value pairs from a WeatherLink data packet

    extracted_kv = {"ts": data["ts"]}

    for conditions in data["conditions"]:
        retained_pairs = {
            k: v for (k, v) in conditions.items() if (k in keys) and (v is not None)
        }

        for (k, v) in retained_pairs.items():
            extracted_kv[k] = v

    return extracted_kv


async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:
        return await resp.json()


async def main() -> None:
    # Load TOML configuration for app from 'config' directory
    config_path = Path(__file__).parent.parent / "config" / "wlconfig.toml"
    # print(config_path)

    try:
        wlconfig = tomload(config_path)
    except:
        print(f"Unable to load '{config_path}', exiting...")
        exit()

    # Set session variables from TOML config
    # keys_to_retain = wlconfig["weatherlink"]["keys_to_retain"]
    request_timeout = aiohttp.ClientTimeout(
        total=wlconfig["weatherlink"]["request_timeout"]
    )
    sleep_interval = wlconfig["weatherlink"]["sleep_interval"]
    url = (
        # f"{wlconfig['weatherlink']['url']}{wlconfig['weatherlink']['path']}"
        f"{wlconfig['weatherlink']['url']}"
    )

    async with aiohttp.ClientSession(timeout=request_timeout) as session:
        while True:
            try:
                print(f"Query {url}")
                json_response = await fetch(session, url)
                print(json_response)
                # kvs = extract_wl_kvs(json_response, keys_to_retain)
                # print(kvs)
            except Exception as e:
                print(f"exception: {e}")

            sleep(sleep_interval)


## Start Async Application ##
# Redis connection
# try:
#     redis_con = Redis(
#         host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"]
#     )
# except:
#    print(f"Cannot connect to Redis instance at {wlconfig["dbs"]["redis"]["host"]}:{wlconfig["dbs"]["redis"]["port"]}, exiting...")
#    exit(0)

# Select Redis Database
# redis_con.select(wlconfig["dbs"]["redis"]["database"])

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Stopping service...")
    exit(0)


# Function to poll WeatherLink station, with backoff on request failure
#     # Convenience variable for accessing contents of `data` key
#     current_conditions_data = current_conditions_json["data"]

# Sample (approximately) current conditions round sensor array
# while True:
#     current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)
#
#     print(current_conditions)
#
#     # Push to Redis Stream
#     redis_con.xadd(wlconfig["dbs"]["redis"]["stream_name"], current_conditions)
#
#     # Pause before making next request
#     sleep(SLEEP_INTERVAL)
