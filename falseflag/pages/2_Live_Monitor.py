import os
from collections import Counter

import streamlit as st

from collectors import COLLECTORS, collect
from ui import pick_case, setup

setup(
    "Live monitor",
    "Collects coverage of a case from news sites, GDELT, Reddit and X. Each item is tagged by source type "
    "and by how it relates to the claim. **How widely a claim spreads is shown separately and never "
    "counts as evidence.**",
)

case = pick_case()
mode = st.radio("Search for", ["Coverage of the event", "The false-flag claim itself", "Custom query"],
                horizontal=True)
query = {"Coverage of the event": case["keywords"],
         "The false-flag claim itself": case["claim_keywords"]}.get(mode, "")
query = st.text_input("Query", value=query)

has_x = bool(os.environ.get("X_BEARER_TOKEN"))
default_platforms = [p for p in COLLECTORS if p != "X" or has_x]
platforms = st.multiselect("Sources", list(COLLECTORS), default=default_platforms)
if not has_x:
    st.caption("X is off: set the `X_BEARER_TOKEN` environment variable (from developer.x.com) to include x.com posts.")
limit = st.slider("Items per source", 10, 100, 30, step=10)


@st.cache_data(ttl=600, show_spinner="Collecting coverage…")
def run(query, platforms, limit):
    return collect(query, platforms, limit)


if st.button("Collect", type="primary") and query:
    st.session_state["collected"] = run(query, tuple(platforms), limit)
    st.session_state["collected_for"] = case["id"]

if st.session_state.get("collected_for") == case["id"]:
    items, errors = st.session_state["collected"]
    for name, err in errors.items():
        st.warning(f"{name}: {err}")
    if items:
        st.subheader(f"{len(items)} items")
        stance = Counter(i["stance"] for i in items)
        types = Counter(i["source_type"] for i in items)
        a, b, c = st.columns(3)
        a.metric("Promote the claim", stance["promotes claim"])
        b.metric("Debunk / report on the claim", stance["debunks / reports on claim"])
        c.metric("Report the event", stance["reports event"])
        st.caption("Source types: " + ", ".join(f"{k}: {v}" for k, v in types.most_common()))
        st.caption("Stance tags come from keywords and are approximate — read the items. "
                   "Use the AI analyst to turn coverage into weighted arguments.")

        f_stance = st.multiselect("Filter by stance", sorted(stance), default=sorted(stance))
        f_type = st.multiselect("Filter by source type", sorted(types), default=sorted(types))
        shown = [i for i in items if i["stance"] in f_stance and i["source_type"] in f_type]
        st.dataframe(
            shown,
            column_order=["published", "platform", "domain", "source_type", "stance", "title", "url"],
            column_config={"url": st.column_config.LinkColumn("Link", display_text="Open"),
                           "published": "Published", "platform": "Platform", "domain": "Source",
                           "source_type": "Source type", "stance": "Stance", "title": "Title"},
            hide_index=True, width="stretch",
        )
    elif not errors:
        st.info("Nothing found for that query.")
