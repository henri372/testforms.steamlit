"""Case storage and the evidence-weighted scoring model."""
import json
import math
from datetime import date, datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CASES_FILE = DATA_DIR / "cases.json"

# Weight = how much one item of this evidence type shifts the log-odds.
# Inference/motive arguments are deliberately weak: "who benefits" is not evidence of who did it.
EVIDENCE_TYPES = {
    "documentary": ("Documents, records or forensic/physical evidence", 3.0),
    "official_admission": ("Perpetrator admission, court ruling or official finding", 3.0),
    "multiple_independent_witnesses": ("Multiple independent eyewitnesses", 2.0),
    "named_credible_source": ("Named, accountable source or official", 1.0),
    "anonymous_report": ("Anonymous or single-source report", 0.4),
    "inference": ("Motive, timing or 'cui bono' inference", 0.15),
}

# Multiplier for how well the argument itself has been checked.
STATUS = {
    "verified": ("Independently verified", 1.0),
    "unverified": ("Not yet verified", 0.5),
    "disputed": ("Disputed by credible sources", 0.3),
    "debunked": ("Shown false / fabricated", 0.0),
}

# Prior probability that a publicly alleged false flag is genuine, before looking at evidence.
DEFAULT_PRIOR = 0.10

BANDS = [
    (10, "No credible support", "🟢"),
    (35, "Weak support", "🟡"),
    (65, "Contested / insufficient evidence", "🟠"),
    (90, "Substantial evidence", "🔴"),
    (101, "Documented false flag", "⛔"),
]


def load_cases():
    return json.loads(CASES_FILE.read_text(encoding="utf-8"))


def save_cases(cases):
    CASES_FILE.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")


def upsert_case(case):
    cases = load_cases()
    ids = [c["id"] for c in cases]
    if case["id"] in ids:
        cases[ids.index(case["id"])] = case
    else:
        cases.append(case)
    save_cases(cases)


def contribution(arg):
    weight = EVIDENCE_TYPES[arg["evidence_type"]][1]
    mult = STATUS[arg["status"]][1]
    return (1 if arg["side"] == "for" else -1) * weight * mult


def score_case(case, prior=DEFAULT_PRIOR):
    """Return a dict with the 0-100 support score for the false-flag claim and its breakdown."""
    logit = math.log(prior / (1 - prior))
    rows = []
    for arg in case["arguments"]:
        c = contribution(arg)
        logit += c
        rows.append({**arg, "contribution": round(c, 2)})
    p = 1 / (1 + math.exp(-logit))
    score = round(100 * p, 1)
    label, icon = next((lbl, ic) for limit, lbl, ic in BANDS if score < limit)
    verified = sum(1 for a in case["arguments"] if a["status"] == "verified")
    return {
        "score": score,
        "label": label,
        "icon": icon,
        "rows": rows,
        "maturity": maturity(case, verified),
        "weight_for": round(sum(r["contribution"] for r in rows if r["contribution"] > 0), 2),
        "weight_against": round(-sum(r["contribution"] for r in rows if r["contribution"] < 0), 2),
    }


def maturity(case, verified_count):
    """How settled the evidence is. Young cases are flagged because early reporting changes."""
    try:
        d = datetime.strptime(case["date"][:10], "%Y-%m-%d").date()
        age = (date.today() - d).days
    except ValueError:
        age = 10_000  # partial historical dates such as "1954-07"
    if age < 14:
        return f"Developing — event is {age} day(s) old; early reports often change"
    if verified_count < 2:
        return "Thin — fewer than two verified evidence items"
    return "Established"


def format_score(score):
    return "<1" if score < 1 else ">99" if score > 99 else f"{score:.0f}"
