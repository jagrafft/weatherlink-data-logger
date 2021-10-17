use dotenv::dotenv;
use hyper::Client;
use hyper::body::Buf;
use serde_json::{from_reader, Value};
use std::env;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;

#[tokio::main]
async fn main() -> Result<()> {
    dotenv().ok();

    // Request packet from WeatherLink station
    // See https://weatherlink.github.io/weatherlink-live-local-api/ for explanation of data elements
    let client = Client::new();
    let url = format!("{}{}", env::var("WEATHERLINK_URL").unwrap(), env::var("WEATHERLINK_PATH").unwrap()).parse().unwrap();
    let res = client.get(url).await?;
    let body = hyper::body::aggregate(res).await?;
    let json:Value = from_reader(body.reader())?;
    let data:&Value = &json["data"];
    //
    
    println!("device id: {}", data["did"]);
    println!("timestamp: {}", data["ts"]);

    for c in data["conditions"].as_array().unwrap() {
        let obj = c.as_object().unwrap();
       println!("lsid: {}, packet_length: {:?}, data_structure_type: {:?}", c["lsid"], obj.len(), obj.get("data_structure_type"));
    };
    Ok(())
}
