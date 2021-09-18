-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent valid wind direction **(°degree)**
CREATE OR REPLACE wind_dir_last (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
