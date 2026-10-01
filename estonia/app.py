import streamlit as st

from lib import cite, page_header

page_header(
    "MS Estonia — 28 September 1994",
    "A fact-based record of the deadliest peacetime shipwreck in European waters since the Second "
    "World War, the investigations that followed, and the questions that remain. Every claim on this "
    "site links to an official report, book, archive or published interview.",
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("People aboard", "989", "803 passengers · 186 crew", delta_color="off")
c2.metric("Dead or missing", "852", "501 Swedish · 285 Estonian", delta_color="off")
c3.metric("Survivors", "137", "138 rescued, 1 died later", delta_color="off")
c4.metric("Bodies recovered", "94", "the rest remain in the wreck", delta_color="off")
cite(["jaic1997", "sr_tribute"])

st.divider()
left, right = st.columns([3, 2])
with left:
    st.subheader("What happened")
    st.markdown(
        "On the evening of **27 September 1994** the ro-ro passenger ferry *Estonia* left Tallinn for "
        "Stockholm in worsening weather. Shortly after **01:00** on 28 September, crew and passengers "
        "heard heavy bangs from the bow. Within minutes the ship took a severe starboard list. A Mayday "
        "went out at **01:22**, and by about **01:50** the ship had vanished from radar south of the "
        "Finnish island of Utö.\n\n"
        "Most people aboard never reached the open deck. Those who did faced near-freezing water and "
        "high seas; the first rescue ship arrived around 02:12 and helicopters about an hour later."
    )
    cite(["jaic1997"])

    st.subheader("The official explanation")
    st.markdown(
        "The Joint Accident Investigation Commission (1997) found that the **bow visor's locks failed** "
        "under wave loads. The visor tore away and pulled open the bow ramp, letting water flood the car "
        "deck. A re-examination opened after new wreck footage in 2020 reached the same conclusion in its "
        "**final report of 16 December 2025**, and found the newly discovered starboard damage was caused "
        "by contact with the seabed."
    )
    cite(["jaic1997", "pa2025"])

with right:
    st.subheader("The ship")
    st.table({
        "": ["Built", "Builder", "Former names", "Operator (1994)", "Type", "Route", "Wreck depth"],
        "Details": [
            "1980",
            "Meyer Werft, Papenburg",
            "Viking Sally, Silja Star, Wasa King",
            "Estline",
            "Ro-ro passenger ferry with bow visor",
            "Tallinn – Stockholm",
            "approx. 70–85 m",
        ],
    })
    cite(["jaic1997"])

st.divider()
st.subheader("Explore")
cols = st.columns(5)
pages = [
    ("pages/1_Timeline.py", "🕐 Timeline", "From 1980 to the 2025 report"),
    ("pages/2_Unanswered_Questions.py", "❓ Unanswered questions", "Official findings vs. critics"),
    ("pages/3_Eyewitness_Testimonies.py", "🗣️ Eyewitnesses", "Survivors and crew"),
    ("pages/4_Photo_Database.py", "📷 Photo database", "Archives and open-licence images"),
    ("pages/5_Sources_and_Books.py", "📚 Sources & books", "Reports, books, documentaries"),
]
for col, (path, label, help_text) in zip(cols, pages):
    with col:
        st.page_link(path, label=label)
        st.caption(help_text)

st.info(
    "This site separates **established findings** from **disputed claims**. Alternative theories are "
    "presented with their sources so readers can judge the evidence, not as endorsements.",
    icon="ℹ️",
)
