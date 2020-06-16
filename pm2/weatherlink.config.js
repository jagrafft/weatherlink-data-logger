const now = new Date()
const dt = now.toISOString()

const APP_PATH = `${process.env.HOME}/weatherlink-data-logger`
const LOG_PATH = `${process.env.HOME}/.pm2-logs`
const PM2_SCRIPT_DIR = "pm2"

module.exports = {
    apps: [
      {
         name: "observable-notebook-connector",
         script: `${PM2_SCRIPT_DIR}/observable-notebook-connector.js`,
         cwd: APP_PATH,
/*         env: {
            "OBSERVABLE_DATABASE_PROXY_PATH": OBSERVABLE_DATABASE_PROXY_PATH,
            "OBSERVABLE_DATABASE_PROXY_PROFILE": OBSERVABLE_DATABASE_PROXY_PROFILE
         },*/
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
	 node_args : '-r dotenv/config',
         watch: false,
         error_file: `${LOG_PATH}-observable-notebook-connector_error.log`,
         out_file: `${LOG_PATH}-observable-notebook-connector_out.log`
      },
      {
         name: "weatherlink-data-capture",
         script: `${PM2_SCRIPT_DIR}/weatherlink-data-capture.js`,
         cwd: APP_PATH,
/*         env: {
            "APP_PATH": APP_PATH,
            "DATA_REFRESH_INTERVAL_MS": DATA_REFRESH_INTERVAL_MS,
            "POSTGRES_ADDR": POSTGRES_ADDR,
            "POSTGRES_PORT": POSTGRES_PORT,
            "POSTGRES_USER": POSTGRES_USER,
            "POSTGRES_PASS": POSTGRES_PASS,
            "POSTGRES_DB:" POSTGRES_DB,
            "WEATHERLINK_URL": WEATHERLINK_URL
         },*/
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
	 node_args : '-r dotenv/config',
         watch: false,
         error_file: `${LOG_PATH}-weatherlink-data-capture_error.log`,
         out_file: `${LOG_PATH}-weatherlink-data-capture_out.log`
      }
    ]
}
