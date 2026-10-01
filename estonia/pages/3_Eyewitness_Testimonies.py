import streamlit as st

from lib import add_submission, cite, load, load_submissions, page_header

page_header(
    "Eyewitness testimonies",
    "Summaries of published accounts by survivors and crew. Accounts are paraphrased from the cited "
    "interviews and reports — follow the source links for the original words. The JAIC final report "
    "(chapter 21.3) reproduces many more survivor statements deck by deck.",
)

testimonies = load("testimonies")
themes = sorted({t for item in testimonies for t in item["themes"]})
c1, c2 = st.columns([2, 3])
theme = c1.selectbox("Theme", ["All"] + themes)
query = c2.text_input("Search", placeholder="e.g. bang, lifeboat, ramp")

for t in testimonies:
    if theme != "All" and theme not in t["themes"]:
        continue
    if query and query.lower() not in (t["name"] + t["summary"] + t["role"]).lower():
        continue
    with st.container(border=True):
        st.markdown(f"#### {t['name']}")
        st.caption(f"{t['role']} · {t['location_aboard']} · themes: {', '.join(t['themes'])}")
        st.write(t["summary"])
        cite(t["sources"])

st.divider()
st.subheader("Contribute a published account")
st.markdown(
    "Know of another published testimony (book, interview, report)? Submit it with a source. "
    "Submissions are stored as **unverified** and are not shown above until checked."
)
with st.form("testimony", clear_on_submit=True):
    name = st.text_input("Witness name")
    role = st.text_input("Role (passenger, crew, rescuer…)")
    summary = st.text_area("Summary of the account")
    source = st.text_input("Source (title and URL) — required")
    if st.form_submit_button("Submit for review"):
        if name and summary and source:
            add_submission("testimony", {"name": name, "role": role, "summary": summary, "source": source})
            st.success("Thank you — saved for review.")
        else:
            st.warning("Name, summary and source are required.")

pending = [s for s in load_submissions() if s["kind"] == "testimony"]
if pending:
    st.caption(f"{len(pending)} submission(s) awaiting review.")
