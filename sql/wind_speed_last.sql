-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent valid wind speed **(mph)**
CREATE OR REPLACE wind_speed_last (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
