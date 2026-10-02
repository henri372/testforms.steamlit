import re
from datetime import date

import streamlit as st

from core import EVIDENCE_TYPES, STATUS, load_cases, upsert_case
from ui import pick_case, setup

setup("Add or edit a case")

tab_new, tab_arg = st.tabs(["New case", "Add an argument to a case"])

with tab_new:
    with st.form("new_case", clear_on_submit=True):
        title = st.text_input("Title", placeholder="e.g. Pipeline explosion, March 2027")
        when = st.date_input("Date of event", value=date.today())
        event = st.text_area("What happened (established facts only)")
        official = st.text_area("Official account")
        claim = st.text_area("False-flag claim to test", placeholder="e.g. The explosion was staged by X and blamed on Y.")
        keywords = st.text_input("News search query for the event")
        claim_keywords = st.text_input("Search query for the claim", placeholder='e.g. pipeline "false flag"')
        if st.form_submit_button("Create case"):
            if title and event and claim:
                case_id = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] + f"-{when.year}"
                if any(c["id"] == case_id for c in load_cases()):
                    st.error("A case with this title already exists.")
                else:
                    upsert_case({
                        "id": case_id, "title": title, "date": when.isoformat(), "kind": "live",
                        "event": event, "official_account": official, "claim": claim,
                        "keywords": keywords or title, "claim_keywords": claim_keywords or f'{title} "false flag"',
                        "arguments": [], "open_questions": [],
                    })
                    st.success("Case created. Use the Live monitor and AI analyst to gather evidence.")
            else:
                st.warning("Title, what happened and the claim are required.")

with tab_arg:
    case = pick_case()
    with st.form("new_arg", clear_on_submit=True):
        side = st.radio("Side", ["for", "against"], horizontal=True,
                        format_func=lambda s: "Supports the claim" if s == "for" else "Against the claim")
        text = st.text_area("Argument")
        ev = st.selectbox("Evidence type", list(EVIDENCE_TYPES), format_func=lambda k: EVIDENCE_TYPES[k][0])
        status = st.selectbox("Status", list(STATUS), format_func=lambda k: STATUS[k][0], index=1)
        note = st.text_input("Note (optional)")
        src_title = st.text_input("Source title")
        src_url = st.text_input("Source URL — required")
        if st.form_submit_button("Add argument"):
            if text and src_url:
                case["arguments"].append({"side": side, "text": text, "evidence_type": ev, "status": status,
                                          "note": note, "sources": [{"title": src_title or src_url, "url": src_url}]})
                upsert_case(case)
                st.success("Argument added.")
            else:
                st.warning("An argument and a source URL are required.")
