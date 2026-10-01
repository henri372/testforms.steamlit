import streamlit as st

from lib import load, page_header

page_header(
    "Sources & books",
    "Everything on this site is drawn from the material below. Official reports carry the most weight; "
    "books and documentaries presenting alternative theories are included because they shaped the public "
    "debate — their claims are flagged where official findings contradict them.",
)

sources = load("sources")
types = sorted({s["type"] for s in sources})
c1, c2 = st.columns([2, 3])
picked = c1.multiselect("Type", types, default=types)
query = c2.text_input("Search", placeholder="author, title, keyword")

for t in types:
    if t not in picked:
        continue
    group = [s for s in sources if s["type"] == t and
             (not query or query.lower() in " ".join(s.values()).lower())]
    if not group:
        continue
    st.subheader(t)
    for s in group:
        st.markdown(f"**[{s['title']}]({s['url']})**  \n{s['author']} · {s['year']}")
        st.caption(s["notes"])
