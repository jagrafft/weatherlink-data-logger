-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent bar sensor reading with elevation adjustment **(inches)**
CREATE OR REPLACE bar_sea_level (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
