-- "Key" relation for 6NF data architecture
CREATE OR REPLACE timestamps (
    id  SERIAL  PRIMARY KEY,
    val INT     UNIQUE
);

-- For data element definitions, see
-- https://weatherlink.github.io/weatherlink-live-local-api/

-- most recent valid temperature **(°F)**
CREATE OR REPLACE temp (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- most recent valid humidity **(%RH)**
CREATE OR REPLACE hum (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- dew_point **(°F)**
CREATE OR REPLACE dew_point (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- heat_index, wind_chill, thw_index, thsw_index?

-- most recent valid wind speed **(mph)**
CREATE OR REPLACE wind_speed_last (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- most recent valid wind direction **(°degree)**
CREATE OR REPLACE wind_dir_last (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- rain_rate_*, rain_storm_start, 

-- most recent solar radiation **(W/m²)** 
CREATE OR REPLACE solar_rad (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- most recent UV index **(Index)** 
CREATE OR REPLACE uv_index (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- most recent valid inside temp **(°F)** 
CREATE OR REPLACE temp_in (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- most recent valid inside humidity **(%RH)**
CREATE OR REPLACE hum_in (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);

-- dew_point_in, heat_index_in ?

-- most recent bar sensor reading with elevation adjustment **(inches)**
CREATE OR REPLACE bar_sea_level (
    id  INT    PRIMARY KEY REFERENCES timestamps(id),
    val REAL,
    ON DELETE CASCADE
);
