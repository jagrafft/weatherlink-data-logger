// Well-built library for the `Future` type, used to make
// operations asynchronous
const {Future} = require("fluture")

/**
 * Check if `entity` exists in postgres `table` in `db` and return its
 * primary key or insert entity on fail
 * @param {String} db Database to check
 * @param {String} table Table to search
 * @param {String|Number} entity Value to search for
 * @returns {Fluture.<Future>} `id` || Failure
 */
export const entityExistsOrInsert = (db, table, entity) => {
    
}

/**
 * @param {} 
 * @returns {Fluture.<Future>}
 */
export const mkInsertString = () => {
    
}

/**
 * Write `cmd` to postgres `table` in `db`
 * @param {String} db Database to write to
 * @param {String} table Table to write to
 * @param {String} cmd Command string
 * @returns {Fluture.<Future>}
 */
export const pgWrite = (db, table, cmd) => {
    
}

// TODO Refactor to build table?
/**
 * Check if postgres `table` exists in `db`
 * @param {String} db Database to check
 * @param {String} table Table to check for
 * @returns {Fluture.<Future>}
 */
export const tableExists = (db, table) => {
    
}