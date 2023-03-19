import asyncio
import aiohttp
import logging

from pathlib import Path
from pytomlpp import load as tomload
from sys import exit, stdout
from time import localtime, sleep, strftime

# from redis import Redis

## Initiate Logging ##
script_start_time = strftime("%Y-%m-%dT%H%M%S", localtime())

logger = logging.getLogger("wl_logger")
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler(Path.cwd() / f"weatherlink_{script_start_time}.log")
stream_handler = logging.StreamHandler(stdout)

file_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
##

"""
def extract_weatherlink_keys(data: dict, keys: list) -> dict:
    # Extracted Key-Value pairs from a WeatherLink data packet

    extracted_kv = {"ts": data["ts"]}

    for conditions in data["conditions"]:
        retained_pairs = {
            k: v for (k, v) in conditions.items() if (k in keys) and (v is not None)
        }

        for (k, v) in retained_pairs.items():
            extracted_kv[k] = v

    return extracted_kv
"""


async def fetch(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as resp:
        return await resp.json()


# async def main(config: dict, rdb: redis.Redis, logger: logging.Logger) -> None:
async def main(config: dict, logger: logging.Logger) -> None:
    # Entering asynchronous code block, log as successful start
    logger.info("SUCCESS")
    # Set session variables from TOML config
    # keys = config["weatherlink"]["keys_to_retain"]
    request_timeout = aiohttp.ClientTimeout(
        total=config["weatherlink"]["request_timeout"]
    )
    request_interval = config["weatherlink"]["request_interval"]
    url = config["weatherlink"]["url"]

    # Used for testing with 'http://httpbin.org/delay'
    from random import randint

    async with aiohttp.ClientSession(timeout=request_timeout) as session:
        while True:
            # Used for testing with 'http://httpbin.org/delay'
            delay = randint(0, 10)
            logger.info(f"fetch '{url}/{delay}'...")

            # logger.info(f"fetch '{url}'...")
            try:
                # Used for testing with 'http://httpbin.org/delay'
                json_response = await fetch(session, f"{url}/{delay}")

                # json_response = await fetch(session, url)
                # data_to_persist = extract_weatherlink_keys(json_response, keys)
                print(json_response)
                # print(data_to_persist)
                logger.info("SUCCESS")
            except Exception as e:
                logger.warning(f"EXCEPTION: {repr(e)}")

            sleep(request_interval)


## Start Application ##
# Load TOML Configuration for App
try:
    config_path = Path(__file__).parent.parent / "config" / "config.toml"
    logger.info(f"LOAD '{config_path}'...")
    wlconfig = tomload(config_path)
except Exception as e:
    logger.error(f"EXCEPTION: {repr(e)}")
    logger.critical("EXITING")
    exit()

logger.info("SUCCESS")

# Establish Redis Connection
"""
try:
    logger.info(f"CONNECT to Redis instance at {wlconfig['redis']['host']}:{wlconfig['redis']['port']} (database {wlconfig['redis']['database']})")

    redis_con = redis.ConnectionPool(
        host=wlconfig["redis"]["host"], port=wlconfig["redis"]["port"], db=wlconfig["redis"]["database"]
    )
except Exception as e:
   logger.error(f"EXCEPTION: {repr(e)}")
   logger.error("CANNOT connect to Redis instance")
   logger.critical("EXITING")
   exit()

logger.info("CONNECTED")
"""

logger.info("START asynchronous application service...")
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    asyncio.run(main(wlconfig, logger))
    # asyncio.run(main(wlconfig, redis_con))
except KeyboardInterrupt:
    logger.warning("KeyboardInterrupt, stopping service...")
    exit()
except Exception as e:
    logger.error(f"EXCEPTION: {repr(e)}")
    logger.critical("EXITING")
    exit()


## NEED TO IMPLEMENT ##
# Function to poll WeatherLink station, with backoff on request failure
#     # Convenience variable for accessing contents of `data` key
#     current_conditions_data = current_conditions_json["data"]
# Sample (approximately) current conditions round sensor array
# while True:
#     current_conditions = get_current_conditions(WEATHERLINK_URL_PATH, KEYS_TO_RETAIN)
#     print(current_conditions)
#     # Push to Redis Stream
#     redis_con.xadd(wlconfig["redis"]["stream_prefix"], current_conditions)
