import streamlit as st

from core import EVIDENCE_TYPES, STATUS, format_score, load_cases


def setup(title, intro=None):
    st.set_page_config(page_title=f"{title} · False Flag Claim Checker", page_icon="🔎", layout="wide")
    st.title(title)
    if intro:
        st.markdown(intro)


def pick_case(label="Case"):
    cases = sorted(load_cases(), key=lambda c: (c["kind"] != "live", c["date"]), reverse=False)
    titles = {c["title"]: c for c in cases}
    default = st.session_state.get("case_title")
    idx = list(titles).index(default) if default in titles else 0
    choice = st.selectbox(label, list(titles), index=idx)
    st.session_state["case_title"] = choice
    return titles[choice]


def score_badge(result):
    st.metric("Support for the false-flag claim", f"{format_score(result['score'])} / 100")
    st.markdown(f"**{result['icon']} {result['label']}**")
    st.progress(min(max(result["score"] / 100, 0.0), 1.0))
    st.caption(f"Evidence maturity: {result['maturity']}")


def argument_card(arg):
    ev = EVIDENCE_TYPES[arg["evidence_type"]][0]
    status = STATUS[arg["status"]][0]
    with st.container(border=True):
        text = f"~~{arg['text']}~~" if arg["status"] == "debunked" else arg["text"]
        st.markdown(text)
        st.caption(f"{ev} · {status} · weight {arg.get('contribution', 0):+}")
        if arg.get("note"):
            st.caption(f"Note: {arg['note']}")
        links = [f"[{s['title']}]({s['url']})" for s in arg.get("sources", []) if s.get("url")]
        if links:
            st.caption("Sources: " + " · ".join(links))
