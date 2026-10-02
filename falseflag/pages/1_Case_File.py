import streamlit as st

from core import score_case
from ui import argument_card, pick_case, score_badge, setup

setup("Case file")
case = pick_case()
result = score_case(case)

top, side = st.columns([3, 1])
with top:
    st.markdown(f"**Date:** {case['date']}")
    st.markdown(f"**What happened:** {case['event']}")
    st.markdown(f"**Official account:** {case['official_account']}")
    st.markdown(f"**Claim tested:** _{case['claim']}_")
with side:
    score_badge(result)

st.divider()
left, right = st.columns(2)
rows = result["rows"]
with left:
    st.subheader(f"Arguments supporting the claim ({sum(r['side'] == 'for' for r in rows)})")
    st.caption(f"Total evidence weight: {result['weight_for']}")
    for r in rows:
        if r["side"] == "for":
            argument_card(r)
with right:
    st.subheader(f"Arguments against the claim ({sum(r['side'] == 'against' for r in rows)})")
    st.caption(f"Total evidence weight: {result['weight_against']}")
    for r in rows:
        if r["side"] == "against":
            argument_card(r)

if case.get("open_questions"):
    st.subheader("Open questions")
    st.markdown("\n".join(f"- {q}" for q in case["open_questions"]))

with st.expander("Score breakdown"):
    st.dataframe(
        [{"Side": r["side"], "Argument": r["text"], "Evidence": r["evidence_type"],
          "Status": r["status"], "Weight": r["contribution"]} for r in rows],
        hide_index=True, width="stretch",
    )
    st.caption("Positive weights push toward the claim, negative weights against it. "
               "See Methodology for the formula.")
