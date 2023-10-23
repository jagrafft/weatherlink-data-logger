# WeatherLink Data Logger

**DEPRECATED** Repository moved to GitLab [weatherlink-live-local-logger](https://gitlab.com/jgrafft/weatherlink-live-local-logger)

Python application to poll a WeatherLink station and push data to a [Redis][redis] stream. Parses the return packet for the data points listed in [Parameters](#parameters). You may change what is captured by modifying the elements in `wlconfig.toml:keys_to_retain`&mdash;see `docs/` for an example [WeatherLink Live Local API][wllla] return packet.

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
