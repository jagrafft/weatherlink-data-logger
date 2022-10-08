# WeatherLink Data Logger
Python application to retreive then log data from a WeatherLink station. This branch experiments with writing data to Apache Arrow file streams with the longer-term objective of utilizing the Arrow Flight service.

## Parameters
| Parameter         | Data Type | SQL Data Type | Note       |
|:------------------|-----------|:-------------:|------------|
| `bar_sea_level`   | Inch      | `REAL`        |            |
| `dew_point`       | °F        | `REAL`        |            |
| `hum`idity        | \%RH      | `REAL`        |            |
| `hum_in`terior    | \%RH      | `REAL`        |            |
| `solar_rad`iation | W/m²      | `REAL`        |            |
| `temp`erature     | °F        | `REAL`        |            |
| `temp_in`terior   | °F        | `REAL`        |            |
| `timestamp`       | Integer   | `INT`         | Global key |
| `uv_index`        | Index     | `REAL`        |            |
| `wind_dir_last`   | °degree   | `REAL`        |            |
| `wind_speed_last` | mph       | `REAL`        |            |

See [WeatherLink Live local API][wllla] 

## Setup and Execution
1. Install [Poetry][poetry] for your platform
1. enter directory: `cd weatherlink-data-logger`
1. copy configuration example: `cp config/wlconfig.example.toml config/wlconfig.toml`
1. Edit `config/wlconfig.toml` as needed
1. activate virtual environment: `poetry shell`
    - install dependencies (_first run_): `poetry install`
1. run: `python3 src/weatherlink.py`

[poetry]: https://python-poetry.org/
[wllla]: https://weatherlink.github.io/weatherlink-live-local-api/
