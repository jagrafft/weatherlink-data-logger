-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent UV index **(Index)** 
CREATE OR REPLACE uv_index (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
