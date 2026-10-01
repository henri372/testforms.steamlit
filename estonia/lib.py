import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
SUBMISSIONS = DATA_DIR / "submissions.json"


@st.cache_data
def load(name):
    return json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


def sources_by_id():
    return {s["id"]: s for s in load("sources")}


def cite(ids):
    """Render a compact list of source links for the given source ids."""
    index = sources_by_id()
    links = []
    for sid in ids:
        s = index.get(sid)
        if s:
            links.append(f"[{s['author'].split('(')[0].strip()}, {s['year']}]({s['url']})")
    if links:
        st.caption("Sources: " + " · ".join(links))


def load_submissions():
    if not SUBMISSIONS.exists():
        return []
    return json.loads(SUBMISSIONS.read_text(encoding="utf-8"))


def add_submission(kind, entry):
    items = load_submissions()
    entry.update(kind=kind, status="unverified",
                 submitted=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    items.append(entry)
    SUBMISSIONS.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def page_header(title, intro=None):
    st.set_page_config(page_title=f"{title} · MS Estonia 1994", page_icon="⚓", layout="wide")
    st.title(title)
    if intro:
        st.markdown(intro)
