require("dotenv").config()
const {exec} = require("child_process")

process.chdir(process.env.OBSERVABLE_DATABASE_PROXY_PATH)

const cmd = `./bin/observable-database-proxy start ${process.env.OBSERVABLE_DATABASE_PROXY_PROFILE}` 

exec(cmd, (error, stdout, stderr) => {
	if (error) {
		console.error(error)
	}

	console.log(cmd)
	console.log(stdout)
	console.error(stderr)
})

process.on("SIGINT", () => {
	process.exit(0)
})
