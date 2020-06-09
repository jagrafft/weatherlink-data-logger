// Ideas //
// version2 => Refactor to use xstream.js for writing to a Kafka service

const Pool = require("pg")  // postgres connection pool

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
`setInterval` executes a function every $n$ milliseconds
*/
setInterval(() => {
    data_request(weatherlink_url).then(X => console.log(X))
}, process.env.DATA_REFRESH_INTERVAL_MS)
