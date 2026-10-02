import streamlit as st

from core import BANDS, DEFAULT_PRIOR, EVIDENCE_TYPES, STATUS
from ui import setup

setup("Methodology")

st.markdown(f"""
### What the score means
The score (0–100) estimates how well the **available evidence supports the false-flag claim**. It is not a
measure of how popular the claim is, and it is not a final verdict — it moves as evidence is added.

### How it is calculated
1. **Start from a prior** of {DEFAULT_PRIOR:.0%}: before looking at evidence, most publicly alleged false flags
   are not confirmed, but some are (see the calibration cases).
2. **Each argument adds or subtracts weight** in log-odds: `weight = evidence type × verification status`.
   Arguments supporting the claim push the score up; arguments against push it down.
3. **Convert to 0–100**: `score = 100 × 1 / (1 + e^-(prior log-odds + Σ weights))`.
""")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Evidence type weights**")
    st.table({"Evidence type": [v[0] for v in EVIDENCE_TYPES.values()],
              "Weight": [v[1] for v in EVIDENCE_TYPES.values()]})
with c2:
    st.markdown("**Verification multipliers**")
    st.table({"Status": [v[0] for v in STATUS.values()], "Multiplier": [v[1] for v in STATUS.values()]})

prev = 0
band_rows = []
for limit, label, icon in BANDS:
    band_rows.append({"Score": f"{prev}–{min(limit, 100)}", "Verdict": f"{icon} {label}"})
    prev = limit
st.markdown("**Verdict bands**")
st.table(band_rows)

st.markdown("""
### Principles
- **Popularity is not evidence.** Thousands of posts repeating a claim count for nothing; post volume is shown
  in the Live monitor only to track how the claim spreads.
- **Motive is not proof.** "Who benefits?" arguments get very little weight. Almost every attack benefits
  someone politically.
- **Real false flags exist and leave evidence.** Confirmed cases such as Gleiwitz (1939) and the Lavon Affair
  (1954) were exposed by documents, trials and perpetrators' admissions — the kinds of evidence weighted most.
- **Fabrications are tracked, not counted.** Debunked items (e.g. fake news reports) stay visible but carry
  zero weight.
- **Developing cases are flagged.** For events less than two weeks old, early reports often change.
- **Name sources.** Every argument needs a source link so anyone can check it.

### Data sources
News via Google News RSS and the GDELT global news database; social media via Reddit search and the official
X API v2 (requires a bearer token). Source domains are labelled by type (wire service, established outlet,
fact-checker, state-affiliated media, social media) in `data/source_ratings.json`.

### Limitations
Weights are judgement calls and are fully editable in `core.py`. Stance tags in the monitor are keyword-based
and approximate. AI-proposed arguments must be reviewed by a person before they are added.
""")
