const now = new Date()
const dt = now.toISOString()

const base_path = ""

const params = new Object({
      log_path: "",
      script_path: `${base_path}/js`,
      observable_connector_path: "",
      postgres_addr: "127.0.0.1",
      postgres_port: 3211,
      postgres_user: "",
      postgres_pass: "",
      postgres_db: "",
      weatherlink_url: "http://192.168.1.161/v1/current_conditions"
})

module.exports = {
    apps: [
      {
         name: "observable-notebook-connector",
         script: "observable-connector.js",
         cwd: params.observable_connector_path,
         env: {
         },
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
         watch: false,
         error_file: `${params.log_path}-observable-notebook-connector_error.log`,
         out_file: `${params.log_path}-observable-notebook-connector_out.log`
      },
      {
         name: "weatherlink-data-capture",
         script: "app.js",
         cwd: params.script_path,
         env: {
            "POSTGRES_ADDR":  params.postgres_addr,
            "POSTGRES_PORT": params.postgres_port,
            "POSTGRES_USER": params.postgres_user,
            "POSTGRES_PASS": params.postgres_pass,
            "POSTGRES_DB:" params.postgres_db,
            "WEATHERLINK_URL": params.weatherlink_url
         },
         autorestart: true,
         exec_mode: "fork",
         instances: 1,
         watch: false,
         error_file: `${params.log_path}-weatherlink-data-capture_error.log`,
         out_file: `${params.log_path}-weatherlink-data-capture_out.log`
      }
    ]
}