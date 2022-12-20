# WeatherLink Data Logger: Development Branch
Python application to poll a WeatherLink station and push data to a [Redis][redis] stream.

## Parameters
| Parameter         | Data Type | SQL Data Type | Tolerance (θ) | Note       |
|:------------------|-----------|:-------------:|---------------|------------|
| `bar_sea_level`   | Inch      | `REAL`        |               |            |
| `dew_point`       | °F        | `REAL`        |               |            |
| `hum`idity        | \%RH      | `REAL`        |               |            |
| `hum_in`terior    | \%RH      | `REAL`        |               |            |
| `solar_rad`iation | W/m²      | `REAL`        |               |            |
| `temp`erature     | °F        | `REAL`        |               |            |
| `temp_in`terior   | °F        | `REAL`        |               |            |
| `timestamp`       | Integer   | `INT`         |               | Global key |
| `uv_index`        | Index     | `REAL`        |               |            |
| `wind_dir_last`   | °degree   | `REAL`        |               |            |
| `wind_speed_last` | mph       | `REAL`        |               |            |

See [WeatherLink Live local API][wllla] 


## Setup
1. Install [Poetry][poetry]
1. Install [Redis][redis]
1. `git clone https://github.com/jagrafft/weatherlink-data-logger.git`
1. `cd weatherlink-data-logger/`
1. `cp config/wlconfig.example.toml config/wlconfig.toml`
1. Edit `config/wlconfig.toml` as needed
1. `poetry install`
1. `poetry run python3 src/weatherlink.py`

[poetry]: https://python-poetry.org/
[redis]: https://redis.io/
[wllla]: https://weatherlink.github.io/weatherlink-live-local-api/
