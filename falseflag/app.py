import streamlit as st

from core import format_score, load_cases, score_case
from ui import setup

setup(
    "False Flag Claim Checker",
    "Tests claims that an attack or incident was a **false flag** — staged by one party and blamed on "
    "another. It gathers news and social media coverage, lays out the arguments for and against each "
    "claim, and scores the claim by the **quality of its evidence**, not by how often it is repeated.",
)

cases = load_cases()
live = [c for c in cases if c["kind"] == "live"]
calibration = [c for c in cases if c["kind"] == "calibration"]


def table(group):
    rows = []
    for c in group:
        r = score_case(c)
        rows.append({
            "Case": c["title"],
            "Date": c["date"],
            "Claim": c["claim"],
            "Score": format_score(r["score"]),
            "Verdict": f"{r['icon']} {r['label']}",
            "Maturity": r["maturity"].split(" — ")[0],
            "Arguments": len(c["arguments"]),
        })
    st.dataframe(rows, hide_index=True, width="stretch")


st.subheader("Cases under review")
table(live)

st.subheader("Calibration cases")
st.caption("Historical cases with settled outcomes. They show the score separates documented false flags "
           "from debunked ones — if the model scored these wrongly, it could not be trusted on new cases.")
table(calibration)

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.page_link("pages/1_Case_File.py", label="📂 Case file", help="Arguments, sources and score breakdown")
c2.page_link("pages/2_Live_Monitor.py", label="📡 Live monitor", help="News, Reddit and X coverage")
c3.page_link("pages/3_AI_Analyst.py", label="🤖 AI analyst", help="Claude proposes new arguments")
c4.page_link("pages/5_Methodology.py", label="📐 Methodology", help="How the score works")

st.info("A low score does not mean questions are closed — it means no credible evidence currently supports "
        "the false-flag claim. Scores change as evidence is added.", icon="ℹ️")
