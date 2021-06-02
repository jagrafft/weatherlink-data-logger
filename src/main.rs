use serde_json::{Result, Value};

fn main() -> Result<()> {
    let w00t = r#"
{
  "data": {
    "did": "001D0A712363",
    "ts": 1591842694,
    "conditions": [
      {
        "lsid": 317655,
        "data_structure_type": 1,
        "txid": 1,
        "temp": 63.7,
        "hum": 52.2,
        "dew_point": 45.8,
        "wet_bulb": 51.6,
        "heat_index": 61.9,
        "wind_chill": 63.7,
        "thw_index": 61.9,
        "thsw_index": null,
        "wind_speed_last": 1,
        "wind_dir_last": 278,
        "wind_speed_avg_last_1_min": 1.87,
        "wind_dir_scalar_avg_last_1_min": 321,
        "wind_speed_avg_last_2_min": 2.5,
        "wind_dir_scalar_avg_last_2_min": 306,
        "wind_speed_hi_last_2_min": 6,
        "wind_dir_at_hi_speed_last_2_min": 279,
        "wind_speed_avg_last_10_min": 2.37,
        "wind_dir_scalar_avg_last_10_min": 300,
        "wind_speed_hi_last_10_min": 8,
        "wind_dir_at_hi_speed_last_10_min": 246,
        "rain_size": 1,
        "rain_rate_last": 0,
        "rain_rate_hi": 0,
        "rainfall_last_15_min": 0,
        "rain_rate_hi_last_15_min": 0,
        "rainfall_last_60_min": 0,
        "rainfall_last_24_hr": null,
        "rain_storm": 90,
        "rain_storm_start_at": 1591336380,
        "solar_rad": null,
        "uv_index": null,
        "rx_state": 0,
        "trans_battery_flag": 0,
        "rainfall_daily": 48,
        "rainfall_monthly": 90,
        "rainfall_year": 90,
        "rain_storm_last": null,
        "rain_storm_last_start_at": null,
        "rain_storm_last_end_at": null
      },
      {
        "lsid": 317640,
        "data_structure_type": 4,
        "temp_in": 75.4,
        "hum_in": 36.2,
        "dew_point_in": 46.8,
        "heat_index_in": 74
      },
      {
        "lsid": 317639,
        "data_structure_type": 3,
        "bar_sea_level": 29.805,
        "bar_trend": 0.081,
        "bar_absolute": 28.807
      }
    ]
  },
  "error": null
}
"#;

    let v:Value = serde_json::from_str(w00t)?;

    for c in v["data"]["conditions"].as_array().unwrap() {
        println!("lsid: {}", c["lsid"]);
    };

    Ok(())
}
