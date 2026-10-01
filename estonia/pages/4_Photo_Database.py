import re

import requests
import streamlit as st

from lib import add_submission, load, page_header

page_header(
    "Photo database",
    "Two collections: openly licensed images pulled live from **Wikimedia Commons** (with author and "
    "licence for each), and a catalogue of **archive and press galleries** that hold copyrighted "
    "photographs, linked rather than copied.",
)

COMMONS_API = "https://commons.wikimedia.org/w/api.php"


@st.cache_data(ttl=24 * 3600, show_spinner="Searching Wikimedia Commons…")
def commons_search(term, limit):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": term, "gsrnamespace": 6, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 480,
    }
    headers = {"User-Agent": "MS-Estonia-fact-site/1.0 (educational Streamlit app)"}
    resp = requests.get(COMMONS_API, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    pages = resp.json().get("query", {}).get("pages", {}).values()
    results = []
    for p in sorted(pages, key=lambda p: p.get("index", 0)):
        info = (p.get("imageinfo") or [{}])[0]
        meta = info.get("extmetadata", {})
        field = lambda k: (meta.get(k, {}).get("value") or "").strip()
        if not info.get("thumburl"):
            continue
        results.append({
            "title": p["title"].removeprefix("File:"),
            "thumb": info["thumburl"],
            "page": info.get("descriptionurl"),
            "artist": re.sub(r"<[^>]+>", "", field("Artist")).strip(),
            "license": field("LicenseShortName") or "see file page",
            "date": field("DateTimeOriginal") or field("DateTime"),
        })
    return results


tab_open, tab_archive, tab_submit = st.tabs(["Open-licence images", "Archive & press galleries", "Submit a photo"])

with tab_open:
    c1, c2 = st.columns([3, 1])
    term = c1.text_input("Search Commons", value='"MS Estonia" OR "Viking Sally" OR "Estonia disaster"')
    limit = c2.slider("Results", 6, 48, 18, step=6)
    try:
        images = commons_search(term, limit)
    except requests.RequestException as exc:
        images = []
        st.error(f"Could not reach Wikimedia Commons ({exc.__class__.__name__}). Try again later.")
    if not images and term:
        st.info("No images found for that search.")
    cols = st.columns(3)
    for i, img in enumerate(images):
        with cols[i % 3]:
            st.image(img["thumb"], width="stretch")
            st.markdown(f"[{img['title']}]({img['page']})")
            st.caption(f"Licence: {img['license']}" + (f" · {img['date'][:10]}" if img["date"] else ""))
            if img["artist"]:
                st.caption("Author: " + img["artist"])
    st.caption("Images are shown under their Commons licences; click through for full attribution.")

with tab_archive:
    photos = load("photos")
    cats = sorted({p["category"] for p in photos})
    cat = st.radio("Category", ["All"] + cats, horizontal=True)
    rows = [p for p in photos if cat == "All" or p["category"] == cat]
    st.dataframe(
        rows,
        column_order=["title", "category", "date", "holder", "license", "url"],
        column_config={"url": st.column_config.LinkColumn("Link", display_text="Open"),
                       "title": "Title", "category": "Category", "date": "Date",
                       "holder": "Holder", "license": "Rights"},
        hide_index=True, width="stretch",
    )
    for p in rows:
        st.markdown(f"- **[{p['title']}]({p['url']})** — {p['description']}")

with tab_submit:
    st.markdown("Suggest a photograph or collection. Include where it is held and its licence; "
                "entries are stored as **unverified** until reviewed.")
    with st.form("photo", clear_on_submit=True):
        title = st.text_input("Title")
        url = st.text_input("Link to image or gallery")
        holder = st.text_input("Photographer / archive")
        license_ = st.text_input("Licence or rights statement")
        desc = st.text_area("Description")
        if st.form_submit_button("Submit for review"):
            if title and url and holder:
                add_submission("photo", {"title": title, "url": url, "holder": holder,
                                         "license": license_, "description": desc})
                st.success("Thank you — saved for review.")
            else:
                st.warning("Title, link and photographer/archive are required.")
