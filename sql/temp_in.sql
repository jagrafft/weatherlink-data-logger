-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent valid inside temp **(°F)** 
CREATE OR REPLACE temp_in (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
