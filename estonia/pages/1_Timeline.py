import streamlit as st

from lib import cite, load, page_header

page_header("Timeline", "Times are local (Finnish/Estonian) time and approximate unless stated; "
            "they follow the JAIC final report except where noted.")

events = load("timeline")
phases = list(dict.fromkeys(e["phase"] for e in events))
chosen = st.multiselect("Show phases", phases, default=phases)

for e in events:
    if e["phase"] not in chosen:
        continue
    when = e["date"] + (f" · {e['time']}" if e["time"] else "")
    with st.container(border=True):
        a, b = st.columns([1, 4])
        a.markdown(f"**{when}**")
        a.caption(e["phase"])
        b.markdown(e["event"])
        with b:
            cite(e["sources"])
