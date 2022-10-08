import pyarrow as pa

from pathlib import Path
from signal import SIGINT, signal
from time import sleep
from weatherlink_utils import (
    get_current_conditions,
    wlconfig,
    KEYS_TO_RETAIN,
    SLEEP_DURATION,
    WEATHERLINK_URL_PATH,
)

from datetime import datetime

### INIT SESSION ###
# Schema for Arrow file
arrow_schema = pa.schema(
    [
        pa.field("timestamp", pa.int64()),
        pa.field("temp", pa.float64()),
        pa.field("hum", pa.float64()),
        pa.field("dew_point", pa.float64()),
        pa.field("wind_speed_last", pa.float64()),
        pa.field("wind_dir_last", pa.float64()),
        pa.field("temp_in", pa.float64()),
        pa.field("hum_in", pa.float64()),
        # pa.field("solar_rad", pa.float64()),
        # pa.field("uv_index", pa.float64()),
        pa.field("bar_sea_level", pa.float64()),
    ]
)

# Sink for Arrow file
arrow_sink = pa.OSFile(f"{wlconfig['arrow']['data_path']}/weatherlink_data.arrow", "wb")

# Writer for Arrow file
arrow_writer = pa.ipc.new_file(arrow_sink, arrow_schema)

# Listener for `CTRL-C` event
def stop_service(sig, frame):
    """
    Stop execution of program. Called by `signal` on `SIGINT`.
    """
    arrow_writer.close()
    arrow_sink.close()

    print("Stopping service...")
    exit(0)


signal(SIGINT, stop_service)
###

### INIT WEATHERLINK DATA FOR SESSION ###
print(WEATHERLINK_URL_PATH)

### REQUEST DATA FROM WEATHERLINK SERVICE TILL `SIGINT` IS ISSUED ###
while True:
    # Sample (approximately) current conditions round sensor array
    current_conditions_data = get_current_conditions(
        WEATHERLINK_URL_PATH, KEYS_TO_RETAIN
    )

    # Write values to Arrow sink
    arrow_writer.write(pa.record_batch(current_conditions_data, arrow_schema))

    # Pause before making next request
    sleep(SLEEP_DURATION)
###
