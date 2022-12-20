# WeatherLink Data Logger: Development Notes
### 2022-12-20
- Removed all calculations for and references to difference between data points
- Data now are inserted into a Redis Stream
  - Long term goal is to have several options for "dumping" the Redis stream to a SQL DB and Apache Arrow
- Updated `wlconfig.example.toml`
- Merged `weatherlink_utils.py` with `weatherlink.py`
- Updated project dependencies
- Moved `main` branch (with difference calculations to `wl-diff`)
- Promoted `python-poetry` branch to `main`
  - `python-poetry` will serve as the "pre release" branch from here out
