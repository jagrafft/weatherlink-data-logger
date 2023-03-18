import asyncio
import aiohttp
import logging

from pathlib import Path
from pytomlpp import load as tomload

# from redis import Redis
from sys import exit
from time import localtime, sleep, strftime


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


# async def main(config: dict, rdb: redis.Redis) -> None:
async def main(config: dict, logger: logging.Logger) -> None:
    # Set session variables from TOML config
    # keys_to_retain = config["weatherlink"]["keys_to_retain"]
    request_timeout = aiohttp.ClientTimeout(
        total=config["weatherlink"]["request_timeout"]
    )
    sleep_interval = config["weatherlink"]["sleep_interval"]
    url = (
        # f"{config['weatherlink']['url']}{config['weatherlink']['path']}"
        f"{config['weatherlink']['url']}"
    )

    async with aiohttp.ClientSession(timeout=request_timeout) as session:
        while True:
            logger.info(f"fetch {url}")
            try:
                json_response = await fetch(session, url)
                print(json_response)
                # kvs = extract_wl_kvs(json_response, keys_to_retain)
                # print(kvs)
            except Exception:
                logger.error("EXCEPTION")

            sleep(sleep_interval)


## Start Application ##
# Initiate logger
script_start_time = strftime("%Y-%m-%dT%H%M%S", localtime())

logger = logging.getLogger("wl_logger")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(Path.cwd() / f"weatherlink_{script_start_time}.log")
file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)

# Load TOML configuration for app from 'config' directory
config_path = Path(__file__).parent.parent / "config" / "wlconfig.toml"
# print(config_path)

try:
    wlconfig = tomload(config_path)
except:
    logger.critical(f"Unable to load '{config_path}', exiting...")
    exit()

# Redis connection
# logger.info(f'Establish connection to Redis instance at {wlconfig['dbs']['redis']['host']}:{wlconfig['dbs']['redis']['port']} (database {wlconfig['dbs']['redis']['database']})')
# try:
#     redis_con = redis.ConnectionPool(
#         host=wlconfig["dbs"]["redis"]["host"], port=wlconfig["dbs"]["redis"]["port"], db=
#     )
# except:
#    print(f"Cannot connect to Redis instance at {wlconfig["dbs"]["redis"]["host"]}:{wlconfig["dbs"]["redis"]["port"]} (database {wlconfig['dbs']['redis']['database']}), exiting...")
#    logger.error(f"Cannot connect to Redis instance at {wlconfig["dbs"]["redis"]["host"]}:{wlconfig["dbs"]["redis"]["port"]} (database {wlconfig['dbs']['redis']['database']}), exiting...")
#    exit(0)

# logger.info(f"Connected to Redis instance at {wlconfig['dbs']['redis']['host']}:{wlconfig['dbs']['redis']['port']} (database {wlconfig['dbs']['redis']['database']})")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    asyncio.run(main(wlconfig, logger))
    # asyncio.run(main(wlconfig, redis_con))
except KeyboardInterrupt:
    logger.critical("KeyboardInterrupt, stopping service...")
    print("Stopping service...")
    exit()


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
