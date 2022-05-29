# WeatherLink Data Logger
Next... concept?... for the kludge-tastic Weatherlink Data Logger: JavaScript Edition.

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
2. Install [Redis][redis]
3. ...

[poetry]: https://python-poetry.org/
[redis]: https://redis.io/
[wllla]: https://weatherlink.github.io/weatherlink-live-local-api/
