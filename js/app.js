// Ideas //
// version2 => Refactor to use xstream.js for writing to a Kafka service
require("dotenv").config()
const { Pool } = require("pg")  // postgres connection pool
const { data_request, lookupEntity, insertEntity } = require("./utils")

/**
 * "Instructions" for connecting to postgres instance
 * @const {pg.<Pool>}
 */
const pool = new Pool({
    database: process.env.POSTGRES_DB,
    host: process.env.POSTGRES_ADDR,
    password: process.env.POSTGRES_PASS,
    port: process.env.POSTGRES_PORT,
    user: process.env.POSTGRES_USER
})

/**
 * URL of WeatherLink station endpoint
 * @const {String}
 */
const weatherlink_url = process.env.WEATHERLINK_URL

/*
`setInterval` executes a function every $n$ milliseconds
*/
setInterval(() => {
    data_request(weatherlink_url)
        .then(res => res["data"])
	.then(data => {
	    return Promise.allSettled([
	        insertEntity(pool, "timestamps", "ts", data["ts"]),
	        insertEntity(pool, "devices", "did", data["did"])
	    ])
	})
	.then(X => console.log(X))
}, process.env.DATA_REFRESH_INTERVAL_MS)
