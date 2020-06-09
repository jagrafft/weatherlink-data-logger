const request = require("request")  // API for HTTP requests

/**
 * Request data from `url`
 * @param {String} url URL to request from
 * @returns {Promise}
 */
data_request = (url) => {
    return new Promise((resolve, reject) => {
        request.get({
            url: weatherlink_url,
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

// TODO Insert if not exists
/**
 * Check if `entity` exists in postgres `table` in `pool` then return its
 * primary key or insert entity on fail
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to search
 * @param {String} column Column to search
 * @param {String|Number} entity Value to search `table.column` for
 * @returns {Promise} `id` || Failure
 */
export const entityExistsOrInsert = (pool, table, column, entity) => {
    return new Promise((resolve, reject) => {
        pool.query(
            "SELECT EXISTS(SELECT 1 FROM $1::text t WHERE t.$2::text = $3)",
            [table, column, entity],
            (err, res) => {
                if (err) { reject(`ERROR: ${err}`) }
                resolve(res)
            }
        )
    })
}

/**
 * @param {Object} obj 
 * @returns {Promise}
 */
export const mkInsertString = (obj) => {
    return new Promise((resolve, reject) => {
    })
}

/**
 * Write `cmd` to postgres `table` in `pool`
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to write to
 * @param {String} cmd Command string
 * @returns {Promise}
 */
export const pgWrite = (pool, table, cmd) => {
    return new Promise((resolve, reject) => {
        pool.query(
            "INSERT INTO $1::text $2::text",
            [table, cmd],
            (err, res) => {
                if (err) { reject() }
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
export const tableExists = (pool, table) => {
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
