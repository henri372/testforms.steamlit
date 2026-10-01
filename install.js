module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "estonia",
        message: ["python -m pip install -r requirements.txt"]
      }
    },
    {
      method: "notify",
      params: { html: "Installed. Click 'Start' to launch the MS Estonia site." }
    }
  ]
}
