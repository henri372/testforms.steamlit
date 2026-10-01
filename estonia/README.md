# MS Estonia 1994 — fact site

A Streamlit site on the sinking of MS Estonia (28 September 1994): timeline, unanswered questions
(official findings vs. critics), eyewitness testimonies, a photo database and a sources/books list.
Every claim cites a source in `data/sources.json`.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Content

All content lives in `data/*.json`, so it can be edited without touching code:

| File | Contents |
|---|---|
| `sources.json` | Reports, inquiries, books, documentaries, news. Other files cite these by `id`. |
| `timeline.json` | Events from 1980 to the December 2025 joint final report |
| `questions.json` | Open questions with official finding, critics' view, evidence and status |
| `testimonies.json` | Paraphrased survivor and crew accounts with sources |
| `photos.json` | Archive and press galleries (linked, not copied, for copyright reasons) |

The photo page also searches Wikimedia Commons live and shows each image's licence and author.
Visitor submissions (testimonies, photos) are saved to `data/submissions.json` as *unverified*;
review them and move accepted entries into the JSON files above.
