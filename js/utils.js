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
 * Insert `entity` into postgres `table` in `pool` then return its
 * primary key
 * @param {} pool PostgreSQL pool
 * @param {String} table Table 
 * @param {String} relation Column
 * @param {String|Number} entity Value to search `table.relation` for
 * @returns {Promise} `id` || Failure
 */
module.exports.dbTransact = (pool, query) => {
    return new Promise((resolve, reject) => {
	console.log(query)
        pool.query(query,
            (err, res) => {
                if (err) { reject(`ERROR: ${err}`) }
                resolve(res)
            }
        )
    })
}

/**
 * Wrap non-number entites in single quotes
 * @param {String} entity Entity to wrap
 * @reutrns {String}
 */
const fmtEntity = (entity) => typeof entity === "number" ? entity : `'${entity}'`

/**
 * Create INSERT statament from inputs
 * @param {} pool PostgreSQL pool
 * @param {String} table Table
 * @param {String} relation Column
 * @param {String|Number} entity
 * @returns {String}
 */
module.exports.insertSingleEntity = (table, relation, entity) => {
    return `INSERT INTO ${table}(${relation}) VALUES (${fmtEntity(entity)}) ON CONFLICT DO NOTHING;`
}

module.exports.insertMultipleEntities = (table, relations, entities) => {
    return `INSERT INTO ${table}(${relations.join(",")}) VALUES (${entities.map(fmtEntity).join(",")});`
}

/**
 * Create SELECT statament from inputs
 * @param {} pool PostgreSQL pool
 * @param {String} table Table
 * @param {String} relation Column
 * @param {String|Number} entity
 * @returns {String}
 */
module.exports.lookupEntity = (table, relation, entity) => {
   return `SELECT id FROM ${table} WHERE ${relation} = ${fmtEntity(entity)};`
}

// TODO Refactor to build table?
/**
 * Check if postgres `table` exists in `pool`
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to check for
 * @returns {Promise}
 */
/*
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
*/
