const request = require("request")  // API for HTTP requests

/**
 * Request data from `url`
 * @param {String} url URL to request from
 * @returns {Promise}
 */
module.exports.data_request = (url) => {
    return new Promise((resolve, reject) => {
        request.get({
            url: url,
            json: true,
            headers: {"User-Agent": "request"}
        }, (err, res, data) => {
            if (err) {
                reject(`ERROR: ${err}`)
            } else if (res.statusCode !== 200) {
                reject(`STATUS: ${res.statusCode}`)
            } else {
                resolve(data)
            }
        })
    })
}

/**
 * Find `entity` in postgres `table` then return it's primary key
 * @param {} pool PostgreSQL pool
 * @param {String} table Table
 * @param {String} relation Column
 * @param {String|Number} entity
 * @returns {Promise} `id` || Failure
 */
module.exports.lookupEntity = (pool, table, relation, entity) => {
    return new Promise((resolve, reject) => {
	const entity_fmt = typeof entity === "number" ? entity : `'${entity}'`
        pool.query(
	    `SELECT id FROM ${table} WHERE ${relation} = ${entity_fmt}`,
	    (err, res) => {
	        if (err) { reject(`ERROR: ${err}`) }
		resolve(res)
	    }
	)
    })
}


/**
 * Insert `entity` into postgres `table` in `pool` then return its
 * primary key
 * @param {} pool PostgreSQL pool
 * @param {String} table Table 
 * @param {String} relation Column
 * @param {String|Number} entity Value to search `table.relation` for
 * @returns {Promise} `id` || Failure
 */
module.exports.insertEntity = (pool, table, relation, entity) => {
    return new Promise((resolve, reject) => {
	const entity_fmt = typeof entity === "number" ? entity : `'${entity}'`
        pool.query(`INSERT INTO ${table}(${relation}) VALUES (${entity_fmt}) ON CONFLICT DO NOTHING`,
            (err, res) => {
                if (err) { reject(`ERROR: ${err}`) }
                resolve(res)
            }
        )
    })
}

// TODO Refactor to build table?
/**
 * Check if postgres `table` exists in `pool`
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to check for
 * @returns {Promise}
 */
module.exports.tableExists = (pool, table) => {
    return new Promise((resolve, reject) => {
        pool.query(
            "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema='public' AND table_name='$1::text');",
            [table],
            (err, res) => {
                if (err) { reject(`ERROR: ${err}`) }
                resolve(res)
            }
        )
    })
}
