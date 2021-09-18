-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent solar radiation **(W/m²)** 
CREATE OR REPLACE solar_rad (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
