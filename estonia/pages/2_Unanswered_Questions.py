import streamlit as st

from lib import cite, load, page_header

page_header(
    "Unanswered questions",
    "For each question: what the official investigations concluded, what critics argue, and the "
    "evidence each side relies on. Status reflects the position after the joint final report of "
    "December 2025.",
)

STATUS_ICON = {
    "Officially resolved": "🟢",
    "Partly explained": "🟡",
    "Partly confirmed": "🟡",
    "Disputed": "🟠",
    "Disputed by some witnesses": "🟠",
    "Not supported by official findings": "⚪",
    "Policy decision": "🔵",
}

questions = load("questions")
statuses = sorted({q["status"] for q in questions})
picked = st.multiselect("Filter by status", statuses, default=statuses)

for q in questions:
    if q["status"] not in picked:
        continue
    with st.expander(f"{STATUS_ICON.get(q['status'], '•')} {q['question']}  —  *{q['status']}*"):
        a, b = st.columns(2)
        a.markdown("**Official finding**")
        a.write(q["official"])
        b.markdown("**Critics and alternative views**")
        b.write(q["critics"])
        st.markdown("**Evidence referenced**")
        st.markdown("\n".join(f"- {e}" for e in q["evidence"]))
        cite(q["sources"])
