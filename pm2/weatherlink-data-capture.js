const {exec} = require("child_process")

process.chdir(process.env.APP_PATH)

const cmd = ""

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