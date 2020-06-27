// Ideas //
// version2 => Refactor to use xstream.js for writing to a Kafka service
require("dotenv").config()
const { Pool } = require("pg")  // postgres connection pool
const {	data_request, dbTransact, insertSingleEntity, insertMultipleEntities, lookupEntity } = require("./utils")

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
	    // restructure data packet
	    let data = res["data"]["conditions"]

	    // Identify `null` keys
	    const null_keys = data.reduce((a,c) => {
		Object.entries(c).forEach(X => {
	            if (X[1] === null) { a.push(X[0]) }
		})
		return a
	    }, [])

	    // Drop nulls
	    if (null_keys.length > 0) {
		data.map(obj => {
		    Object.keys(obj).forEach(key => {
		        if (null_keys.includes(key)) { delete obj[key] }
		    })
		})
	    }

	    return new Object({
		    data: data,
		    keys: [
			{
			    table: "timestamps",
			    relation: "ts",
			    entity: res["data"]["ts"]
			},
			{
			    table: "devices",
			    relation: "did", 
			    entity: res["data"]["did"]
			},
			...res["data"]["conditions"].map(x => {
				return new Object({
					table: "lsids",
					relation: "lsid",
					entity: x["lsid"]
				})
			})
	    	   ]
	    })
	})
	.then(payload => {
		return Promise.allSettled(
		    payload["keys"].map(x => dbTransact(pool, insertSingleEntity(x.table, x.relation, x.entity)))
		)
		.then(X => {
		    // Get keys 
		    return Promise.allSettled(
		        payload["keys"].map(x => {
			    return dbTransact(pool, lookupEntity(x.table, x.relation, x.entity))
					.then(res => {
					    return Promise.resolve(new Object({
						    relation: x.relation,
						    entity: x.entity,
						    foreign_key: res.rows[0]["id"]
					    	})
					    )
				})
			})
		    )
		})
		.then(key_query => {
		    return key_query.map(obj => obj.value)
		})
		.then(keys => {
			console.log(keys)
		    payload["data"].forEach(obj => {
			const lsid_obj = keys.filter(x => x.entity === obj["lsid"])[0]
			obj["did"] = keys.filter(x => x.relation === "did")[0].foreign_key
		        obj["ts"] = keys.filter(x => x.relation === "ts")[0].foreign_key
			obj["lsid"] = lsid_obj.foreign_key
		    // restructe Object into [...keys], [...values] (1:1 map, as in Object)
			const qry = insertMultipleEntities(`CONDITIONS_${lsid_obj.entity}`, Object.keys(obj), Object.values(obj))
			console.log(qry)
			dbTransact(pool, qry)
		    })
	        })
	})
}, process.env.DATA_REFRESH_INTERVAL_MS)
