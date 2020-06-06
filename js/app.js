// Ideas //
// - Refactor to use xstream.js for writing to a Kafka service

// Make values in `.env` available to program (`process.env.<VAR_NAME>`)
require("dotenv").config()

const Pool = require("pg")  // postgres connection pool
const request = require("request")  // API for HTTP requests

/**
 * "Instructions" for connecting to postgres instance
 * @const {pg.<Pool>}
 */
const pool = new Pool({
    user: process.env.POSTGRES_USER,
    host: process.env.POSTGRES_ADDR,
    database: process.env.POSTGRES_DB,
    password: process.env.POSTGRES_PASS,
    port: process.env.POSTGRES_PORT
})

/**
 * URL of WeatherLink station endpoint
 * @const {String}
 */
const weatherlink_url = process.env.WEATHERLINK_URL

/*
`setInterval` executes a function every $n$ milliseconds (see the end of 
    the function block). Here, we are using a Lambda function, which is _only_
    available to `setInterval` because it is not stored in memory outside the
    scope of that function (`Pool`, `request`, `pool`, and `weatherlink_url` 
    are).
*/
setInterval(() => {
        request.get({
                url: weatherlink_url,
                json: true,
                headers: {"User-Agent": "request"}
        }, (err, res, data) => {
                if (err) {
                    console.error(err)
                } else if (res.statusCode !== 200) {
                    console.log(`Status: ${res.statusCode}`)
                } else {
                    // Chain of futures...
                    console.log(data)
                }
        })
}, 1000) // Refresh interval, in milliseconds