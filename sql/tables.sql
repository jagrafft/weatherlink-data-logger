CREATE TABLE DEVICES (
        id SERIAL PRIMARY KEY,
        did VARCHAR UNIQUE
);

CREATE TABLE TIMESTAMPS (
        id SERIAL PRIMARY KEY,
        ts INTEGER UNIQUE
);

CREATE TABLE LSIDS (
        id SERIAL PRIMARY KEY,
        lsid INTEGER UNIQUE
);

CREATE TABLE CONDITIONS_317655 (
        id SERIAL PRIMARY KEY,
        did INTEGER,
        ts INTEGER,
        lsid INTEGER,
        data_structure_type INTEGER,
        txid INTEGER,
        temp DECIMAL,
        hum DECIMAL,
        dew_point DECIMAL,
        wet_bulb DECIMAL,
        heat_index DECIMAL,
        wind_chill DECIMAL,
        thw_index DECIMAL,
        thsw_index DECIMAL,
        wind_speed_last DECIMAL,
        wind_dir_last DECIMAL,
        wind_speed_avg_last_1_min DECIMAL,
        wind_dir_scalar_avg_last_1_min DECIMAL,
        wind_speed_avg_last_2_min DECIMAL,
        wind_dir_scalar_avg_last_2_min DECIMAL,
        wind_speed_hi_last_2_min DECIMAL,
        wind_dir_at_hi_speed_last_2_min DECIMAL,
        wind_speed_avg_last_10_min DECIMAL,
        wind_dir_scalar_avg_last_10_min DECIMAL,
        wind_speed_hi_last_10_min DECIMAL,
        wind_dir_at_hi_speed_last_10_min DECIMAL,
        rain_size INTEGER,
        rain_rate_last INTEGER,
        rain_rate_hi INTEGER,
        rainfall_last_15_min INTEGER,
        rain_rate_hi_last_15_min INTEGER,
        rainfall_last_60_min INTEGER,
        rainfall_last_24_hr INTEGER,
        rain_storm INTEGER,
        rain_storm_start_at INTEGER,
        solar_rad DECIMAL,
        uv_index DECIMAL,
        rx_state INTEGER,
        trans_battery_flag INTEGER,
        rainfall_daily INTEGER,
        rainfall_monthly INTEGER,
        rainfall_year INTEGER,
        rain_storm_last INTEGER,
        rain_storm_last_start_at INTEGER,
        rain_storm_last_end_at INTEGER,
        FOREIGN KEY (did) REFERENCES DEVICES(id),
        FOREIGN KEY (ts) REFERENCES TIMESTAMPS(id),
        FOREIGN KEY (lsid) REFERENCES LSIDS(id)
);

CREATE TABLE CONDITIONS_317640 (
        id SERIAL PRIMARY KEY,
        did INTEGER,
        ts INTEGER,
        lsid INTEGER,
        data_structure_type INTEGER,
        temp_in DECIMAL,
        hum_in DECIMAL,
        dew_point_in DECIMAL,
        heat_index_in DECIMAL,
        FOREIGN KEY (did) REFERENCES DEVICES(id),
        FOREIGN KEY (ts) REFERENCES TIMESTAMPS(id),
        FOREIGN KEY (lsid) REFERENCES LSIDS(id)
);

CREATE TABLE CONDITIONS_217639 (
        id SERIAL PRIMARY KEY,
        did INTEGER,
        ts INTEGER,
        lsid INTEGER,
        data_structure_type INTEGER,
        bar_sea_leve DECIMAL,
        bar_trend DECIMAL,
        bar_absolute DECIMAL,
        FOREIGN KEY (did) REFERENCES DEVICES(id),
        FOREIGN KEY (ts) REFERENCES TIMESTAMPS(id),
        FOREIGN KEY (lsid) REFERENCES LSIDS(id)
);

CREATE TABLE LOAD_ERRORS (
        id SERIAL PRIMARY KEY,
        err VARCHAR,
        packet VARCHAR,
        ts TIMESTAMP
);
