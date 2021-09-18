-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent valid humidity **(%RH)**
CREATE OR REPLACE hum (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
