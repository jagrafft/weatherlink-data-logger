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
        .then(res => {
	    res["data"]["lsids"] = res["data"]["conditions"].map(x => x["lsid"])
	    return res["data"]
	})
	.then(data => {
	    return Promise.allSettled([
	        insertEntity(pool, "timestamps", "ts", data["ts"]),
	        insertEntity(pool, "devices", "did", data["did"]),
		...data["conditions"].map(x => insertEntity(pool, "lsids", "lsid", x["lsid"]))
	    ]).then(X => {
		data["conditions"].forEach(obj => {
		    // Identify `null` keys
		    const null_keys = Object.entries(obj).reduce((a,c) => {
			      if (c[1] === null) { a.push(c[0]) }
			      return a
			  }, [])
		    // Drop nulls from Object
		    if (null_keys.length > 0) {
			    null_keys.forEach(x => delete obj[x])
		    }
		    // restructe Object into [...keys], [...values] (1:1 map, as in Object)
		    // console.log(null_keys)
		    // console.log(obj)
		    console.log(X)
		})
	    })
	})
}, process.env.DATA_REFRESH_INTERVAL_MS)
