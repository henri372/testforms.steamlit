module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "estonia",
        message: ["streamlit run app.py --server.headless true"],
        on: [{ event: "/http:\\/\\/localhost:\\d+/", done: true }]
      }
    },
    {
      method: "local.set",
      params: { url: "{{input.event[0]}}" }
    }
  ]
}
