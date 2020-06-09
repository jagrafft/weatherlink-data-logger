require("dotenv").config()

const now = new Date()
const dt = now.toISOString()

module.exports = {
    apps: [
      {
         name: "observable-notebook-connector",
         script: `${process.env.PM2_SCRIPT_DIR}/observable-notebook-connector.js`,
         cwd: process.env.APP_PATH,
         env: {
            "OBSERVABLE_CONNECTOR_PATH": process.env.OBSERVABLE_CONNECTOR_PATH,
            "OBSERVABLE_CONNECTOR_PROFILE": process.env.OBSERVABLE_CONNECTOR_PROFILE
         },
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
         watch: false,
         error_file: `${process.env.LOG_PATH}-observable-notebook-connector_error.log`,
         out_file: `${process.env.LOG_PATH}-observable-notebook-connector_out.log`
      },
      {
         name: "weatherlink-data-capture",
         script: `${process.env.PM2_SCRIPT_DIR}/weatherlink-data-capture.js`,
         cwd: process.env.APP_PATH,
         env: {
            "APP_PATH": process.env.APP_PATH,
            "DATA_REFRESH_INTERVAL_MS": process.env.DATA_REFRESH_INTERVAL,
            "POSTGRES_ADDR": process.env.POSTGRES_ADDR,
            "POSTGRES_PORT": process.env.POSTGRES_PORT,
            "POSTGRES_USER": process.env.POSTGRES_USER,
            "POSTGRES_PASS": process.env.POSTGRES_PASS,
            "POSTGRES_DB:" process.env.POSTGRES_DB,
            "WEATHERLINK_URL": process.env.WEATHERLINK_URL
         },
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
         watch: false,
         error_file: `${process.env.LOG_PATH}-weatherlink-data-capture_error.log`,
         out_file: `${process.env.LOG_PATH}-weatherlink-data-capture_out.log`
      }
    ]
}
