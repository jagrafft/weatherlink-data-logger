# WeatherLink Data Logger
Python application to retreive then log data from a WeatherLink station. This branch experiments with writing data to Apache Arrow file streams with the longer-term objective of utilizing the Arrow Flight service.

## Parameters
| Parameter         | Data Type | SQL Data Type |
|:------------------|-----------|:-------------:|
| `timestamp`       | Integer   | `Int64`       |
| `temp`erature     | °F        | `Float64`     |
| `hum`idity        | \%RH      | `Float64`     |
| `dew_point`       | °F        | `Float64`     |
| `wind_speed_last` | mph       | `Float64`     |
| `wind_dir_last`   | °degree   | `Float64`     |
| `temp_in`terior   | °F        | `Float64`     |
| `hum_in`terior    | \%RH      | `Float64`     |
| `bar_sea_level`   | Inch      | `Float64`     |

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

<!--
| `solar_rad`iation | W/m²      | `Float64`     |
| `uv_index`        | Index     | `Float64`     |
//-->
