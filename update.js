module.exports = {
  run: [
    { method: "shell.run", params: { message: ["git pull"] } },
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "estonia",
        message: ["python -m pip install -r requirements.txt"]
      }
    }
  ]
}
