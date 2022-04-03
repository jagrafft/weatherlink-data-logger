use dotenv::dotenv;
use hyper::Client;
use serde::{Deserialize, Serialize};
use serde::de::{self, Deserializer, Visitor, SeqAccess, MapAccess};
// use serde_json::{from_reader, Value};
use std::{env, fmt, str};

#[derive(Serialize, Debug)]
struct ParamVals {
    timestamp: i64,
    bar_sea_level: f64,
    dew_point: f64,
    hum: f64,
    hum_in: f64,
    solar_rad: f64,
    temp: f64,
    temp_in: f64,
    uv_index: f64,
    wind_dir_last: f64,
    wind_speed_last: f64
}

impl<'de> Deserialize<'de> for ParamVals {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        enum Field { Timestamp, BarSeaLevel, DewPoint, Hum, HumIn, SolarRad, Temp, TempIn, UvIndex, WindDirLast, WindSpeedLast }

        impl<'de> Deserialize<'de> for Field {
            fn deserialize<D>(deserializer: D) -> Result<Field, D::Error>
            where
                D: Deserializer<'de>,
            {
                struct FieldVisitor;

                impl<'de> Visitor<'de> for FieldVisitor {
                    type Value = Field;

                    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                        formatter.write_str("must be a member of `{ ts ; bar_sea_level ; dew_point ; hum ; hum_in ; solar_rad ; temp ;  temp_in ; uv_index ; wind_dir_last ; wind_speed_last }")
                    }

                    fn visit_str<E>(self, value: &str) -> Result<Field, E>
                    where
                        E: de::Error,
                    {
                        match value {
                            "ts" => Ok(Field::Timestamp),
                            "bar_sea_level" => Ok(Field::BarSeaLevel),
                            "dew_point" => Ok(Field::DewPoint),
                            "hum" => Ok(Field::Hum),
                            "hum_in" => Ok(Field::HumIn),
                            "solar_rad" => Ok(Field::SolarRad),
                            "temp" => Ok(Field::Temp),
                            "temp_in" => Ok(Field::TempIn),
                            "uv_index" => Ok(Field::UvIndex),
                            "wind_dir_last" => Ok(Field::WindDirLast),
                            "wind_speed_last" => Ok(Field::WindSpeedLast),
                            _ => Err(de::Error::unknown_field(value, FIELDS))
                        }
                    }
                }

                deserializer.deserialize_identifier(FieldVisitor)
            }
        }

        struct ParamValsVisitor;

        impl<'de> Visitor<'de> for ParamValsVisitor {
            type Value = ParamVals;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
                formatter.write_str("struct ParamVals")
            }

            fn visit_seq<V>(self, mut seq: V) -> Result<ParamVals, V::Error>
            where
                V: SeqAccess<'de>,
            {
                let timestamp = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(0, &self))?;
                let bar_sea_level = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(1, &self))?;
                let dew_point = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(2, &self))?;
                let hum = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(3, &self))?;
                let hum_in = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(4, &self))?;
                let solar_rad = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(5, &self))?;
                let temp = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(6, &self))?;
                let temp_in = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(7, &self))?;
                let uv_index = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(8, &self))?;
                let wind_dir_last = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(9, &self))?;
                let wind_speed_last = seq.next_element()?
                    .ok_or_else(|| de::Error::invalid_length(10, &self))?;
                //Ok(ParamVals::new(timestamp, bar_sea_level, dew_point, hum, hum_in, solar_rad, temp,  temp_in, uv_index, wind_dir_last, wind_speed_last))
                Ok(ParamVals { timestamp, bar_sea_level, dew_point, hum, hum_in, solar_rad, temp,  temp_in, uv_index, wind_dir_last, wind_speed_last })
            }

            fn visit_map<V>(self, mut map: V) -> Result<ParamVals, V::Error>
            where
                V: MapAccess<'de>,
            {
                let mut timestamp = None;
                let mut bar_sea_level = None;
                let mut dew_point = None;
                let mut hum = None;
                let mut hum_in = None;
                let mut solar_rad = None;
                let mut temp = None;
                let mut temp_in = None;
                let mut uv_index = None;
                let mut wind_dir_last = None;
                let mut wind_speed_last = None;

                while let Some(key) = map.next_key()? {
                    match key {
                        Field::Timestamp => {
                            if timestamp.is_some() {
                                return Err(de::Error::duplicate_field("ts"));
                            }
                            timestamp = Some(map.next_value()?);
                        }
                        Field::BarSeaLevel => {
                            if bar_sea_level.is_some() {
                                return Err(de::Error::duplicate_field("bar_sea_level"));
                            }
                            bar_sea_level = Some(map.next_value()?);
                        }
                        Field::DewPoint => {
                            if dew_point.is_some() {
                                return Err(de::Error::duplicate_field("dew_point"));
                            }
                            dew_point = Some(map.next_value()?);
                        }
                        Field::Hum => {
                            if hum.is_some() {
                                return Err(de::Error::duplicate_field("hum"));
                            }
                            hum = Some(map.next_value()?);
                        }
                        Field::HumIn => {
                            if hum_in.is_some() {
                                return Err(de::Error::duplicate_field("hum_in"));
                            }
                            hum_in = Some(map.next_value()?);
                        }
                        Field::SolarRad => {
                            if solar_rad.is_some() {
                                return Err(de::Error::duplicate_field("solar_rad"));
                            }
                            solar_rad = Some(map.next_value()?);
                        }
                        Field::Temp => {
                            if temp.is_some() {
                                return Err(de::Error::duplicate_field("temp"));
                            }
                            temp = Some(map.next_value()?);
                        }
                        Field::TempIn => {
                            if temp_in.is_some() {
                                return Err(de::Error::duplicate_field("temp_in"));
                            }
                            temp_in = Some(map.next_value()?);
                        }
                        Field::UvIndex => {
                            if uv_index.is_some() {
                                return Err(de::Error::duplicate_field("uv_index"));
                            }
                            uv_index = Some(map.next_value()?);
                        }
                        Field::WindDirLast => {
                            if wind_dir_last.is_some() {
                                return Err(de::Error::duplicate_field("wind_dir_last"));
                            }
                            wind_dir_last = Some(map.next_value()?);
                        }
                        Field::WindSpeedLast => {
                            if wind_speed_last.is_some() {
                                return Err(de::Error::duplicate_field("wind_speed_last"));
                            }
                            wind_speed_last = Some(map.next_value()?);
                        }
                    }
                }
                let timestamp = timestamp.ok_or_else(|| de::Error::missing_field("ts"))?;
                let bar_sea_level = bar_sea_level.ok_or_else(|| de::Error::missing_field("bar_sea_level"))?;
                let dew_point = dew_point.ok_or_else(|| de::Error::missing_field("dew_point"))?;
                let hum = hum.ok_or_else(|| de::Error::missing_field("hum"))?;
                let hum_in = hum_in.ok_or_else(|| de::Error::missing_field("hum_in"))?;
                let solar_rad = solar_rad.ok_or_else(|| de::Error::missing_field("solar_rad"))?;
                let temp = temp.ok_or_else(|| de::Error::missing_field("temp"))?;
                let temp_in = temp_in.ok_or_else(|| de::Error::missing_field("temp_in"))?;
                let uv_index = uv_index.ok_or_else(|| de::Error::missing_field("uv_index"))?;
                let wind_dir_last = wind_dir_last.ok_or_else(|| de::Error::missing_field("wind_dir_last"))?;
                let wind_speed_last = wind_speed_last.ok_or_else(|| de::Error::missing_field("wind_speed_last"))?;
                //Ok(ParamVals::new(timestamp, bar_sea_level, dew_point, hum, hum_in, solar_rad, temp,  temp_in, uv_index, wind_dir_last, wind_speed_last))
                Ok(ParamVals { timestamp, bar_sea_level, dew_point, hum, hum_in, solar_rad, temp,  temp_in, uv_index, wind_dir_last, wind_speed_last })
            }
        }

        const FIELDS: &'static [&'static str] = &["ts", "bar_sea_level", "dew_point", "hum", "hum_in", "solar_rad", "temp", " temp_in", "uv_index", "wind_dir_last", "wind_speed_last"];
        deserializer.deserialize_struct("ParamVals", FIELDS, ParamValsVisitor)
    }
}

type ResultT<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;

#[tokio::main]
async fn main() -> ResultT<()> {
    dotenv().ok();

    // Request packet from WeatherLink station
    // See https://weatherlink.github.io/weatherlink-live-local-api/ for explanation of data elements
    let client = Client::new();
    let url = format!("{}{}", env::var("WEATHERLINK_URL").unwrap(), env::var("WEATHERLINK_PATH").unwrap()).parse().unwrap();
    let res = client.get(url).await?;
    // let body = hyper::body::aggregate(res).await?;
    let body = hyper::body::to_bytes(res).await?;
    // let json:Value = from_reader(body.reader())?;
    // let data:&Value = &json["data"];
    
    // println!("device id: {}", data["did"]);
    // println!("timestamp: {}", data["ts"]);

    let conditions_str = match str::from_utf8(&body) {
        Ok(v) => v,
        Err(e) => panic!("Invalid UTF-8 sequence: {}", e),
    };
    println!("conditions: {:?}", conditions_str);
    // let conditions: ParamVals = serde_json::from_str(&conditions_str).unwrap();
    // println!("conditions: {:?}", conditions);

    /*
    for c in data["conditions"].as_array().unwrap() {
       let obj = c.as_object().unwrap();
       println!("lsid: {}, packet_length: {:?}, data_structure_type: {:?}", c["lsid"], obj.len(), obj.get("data_structure_type"));
    };
    */
    Ok(())
}
