// Well-built library for the `Future` type, used to make
// operations asynchronous
const {Future} = require("fluture")
const request = require("request")  // API for HTTP requests

// TODO Wrap in Future
/**
 * Request data from `url`
 * @param {String} url URL to request from
 * @returns {Fluture.<Future>}
 */
data_request = (url) => {
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
}

/**
 * Check if `entity` exists in postgres `table` in `pool` then return its
 * primary key or insert entity on fail
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to search
 * @param {String|Number} entity Value to search for
 * @returns {Fluture.<Future>} `id` || Failure
 */
export const entityExistsOrInsert = (pool, table, entity) => {
    
}

/**
 * @param {} 
 * @returns {Fluture.<Future>}
 */
export const mkInsertString = () => {
    
}

/**
 * Write `cmd` to postgres `table` in `pool`
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to write to
 * @param {String} cmd Command string
 * @returns {Fluture.<Future>}
 */
export const pgWrite = (db, table, cmd) => {
    
}

// TODO Refactor to build table?
/**
 * Check if postgres `table` exists in `pool`
 * @param {} pool PostgreSQL pool
 * @param {String} table Table to check for
 * @returns {Fluture.<Future>}
 */
export const tableExists = (db, table) => {
    
}