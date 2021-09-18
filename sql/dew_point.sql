-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- dew_point **(°F)**
CREATE OR REPLACE dew_point (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
