import os

import streamlit as st

from analyst import AnalystError, analyse
from core import EVIDENCE_TYPES, STATUS, upsert_case
from ui import pick_case, setup

setup(
    "AI analyst",
    "Claude reads the coverage collected in the Live monitor (and can search the web) and proposes new "
    "arguments for and against the claim. **Nothing is added until you review it.**",
)

if not os.environ.get("ANTHROPIC_API_KEY"):
    st.warning("Set the `ANTHROPIC_API_KEY` environment variable to use the AI analyst "
               "(get a key at console.anthropic.com). The rest of the platform works without it.")

case = pick_case()
items = []
if st.session_state.get("collected_for") == case["id"]:
    items = st.session_state["collected"][0]
st.caption(f"{len(items)} collected items will be sent for analysis"
           + ("" if items else " — run the Live monitor first for better results"))
web = st.toggle("Let Claude search the web to verify facts", value=True)

if st.button("Analyse", type="primary"):
    with st.spinner("Analysing… this can take a minute or two"):
        try:
            st.session_state["proposal"] = (case["id"], analyse(case, items, use_web_search=web))
        except AnalystError as e:
            st.error(str(e))

proposal = st.session_state.get("proposal")
if proposal and proposal[0] == case["id"]:
    result = proposal[1]
    st.subheader("Summary")
    st.write(result["summary"])
    st.subheader("Proposed arguments")
    rows = [{"add": True, **a} for a in result["arguments"]]
    edited = st.data_editor(
        rows,
        column_config={
            "add": st.column_config.CheckboxColumn("Add"),
            "side": st.column_config.SelectboxColumn("Side", options=["for", "against"]),
            "evidence_type": st.column_config.SelectboxColumn("Evidence", options=list(EVIDENCE_TYPES)),
            "status": st.column_config.SelectboxColumn("Status", options=list(STATUS)),
            "text": st.column_config.TextColumn("Argument", width="large"),
            "source_url": st.column_config.LinkColumn("Source"),
        },
        hide_index=True, width="stretch",
    )
    if result.get("open_questions"):
        st.markdown("**Open questions:**\n" + "\n".join(f"- {q}" for q in result["open_questions"]))

    if st.button("Add selected arguments to case"):
        chosen = [r for r in edited if r["add"]]
        for r in chosen:
            case["arguments"].append({
                "side": r["side"], "text": r["text"], "evidence_type": r["evidence_type"],
                "status": r["status"], "note": f"AI-proposed, human-reviewed. {r['note']}".strip(),
                "sources": [{"title": r["source_url"], "url": r["source_url"]}] if r["source_url"] else [],
            })
        upsert_case(case)
        st.session_state.pop("proposal")
        st.success(f"Added {len(chosen)} argument(s). The score has been updated in the Case file.")
