module.exports = {
  version: "3.7",
  title: "MS Estonia 1994",
  description: "Fact-based site on the sinking of MS Estonia: timeline, unanswered questions, eyewitness testimonies, photo database and sources.",
  menu: async (kernel, info) => {
    const installed = info.exists("estonia/env")
    const installing = info.running("install.js")
    const running = info.running("start.js")
    if (installing) {
      return [{ default: true, icon: "fa-solid fa-plug", text: "Installing", href: "install.js" }]
    }
    if (!installed) {
      return [{ default: true, icon: "fa-solid fa-plug", text: "Install", href: "install.js" }]
    }
    if (running) {
      const local = info.local("start.js")
      const items = []
      if (local && local.url) {
        items.push({ default: true, icon: "fa-solid fa-rocket", text: "Open Site", href: local.url })
      }
      items.push({ icon: "fa-solid fa-terminal", text: "Terminal", href: "start.js" })
      return items
    }
    return [
      { default: true, icon: "fa-solid fa-power-off", text: "Start", href: "start.js" },
      { icon: "fa-solid fa-rotate", text: "Update", href: "update.js" },
      { icon: "fa-solid fa-plug", text: "Reinstall", href: "install.js" }
    ]
  }
}
