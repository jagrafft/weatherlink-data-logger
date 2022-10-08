import pyarrow as pa

from pathlib import Path
from signal import SIGINT, signal
from time import sleep
from weatherlink_utils import (
    get_current_conditions_batch,
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
arrow_stream_writer = pa.ipc.new_file(
    arrow_sink, arrow_schema, options=pa.ipc.IpcWriteOptions(allow_64bit=True)
)

# Listener for `CTRL-C` event
def stop_service(sig, frame):
    """
    Stop execution of program. Called by `signal` on `SIGINT`.
    """
    arrow_stream_writer.close()
    arrow_sink.close()

    print("Stopping service...")
    exit(0)


signal(SIGINT, stop_service)
###

### INIT WEATHERLINK DATA FOR SESSION ###
print(WEATHERLINK_URL_PATH)

### REQUEST DATA FROM WEATHERLINK SERVICE TILL `SIGINT` IS ISSUED ###
batch = 1
while batch > 0:
    print(f"Sampling batch {batch} from WeatherLink device...")
    # Sample (approximately) current conditions round sensor array
    current_conditions_batch = get_current_conditions_batch(
        WEATHERLINK_URL_PATH, KEYS_TO_RETAIN, arrow_schema, SLEEP_DURATION, batch_size=3
    )

    # Write values to Arrow sink
    arrow_stream_writer.write_batch(current_conditions_batch)
    print(f"Batch {batch} complete!")
    batch += 1

    # Pause before making next request
    sleep(SLEEP_DURATION)
###
