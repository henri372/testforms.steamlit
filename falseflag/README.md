# False Flag Claim Checker

A Streamlit platform that tests claims that an attack or incident was a "false flag". For each case it:

- **collects coverage** from news sites (Google News RSS, GDELT) and social media (Reddit, X API v2),
  tagging each item by source type and by stance toward the claim;
- **lays out arguments** for and against the claim, each with an evidence type, verification status and source;
- **scores the claim 0–100** by evidence quality (log-odds model, see the Methodology page);
- optionally uses **Claude** to read the coverage, search the web and propose new arguments for human review.

Popularity is never counted as evidence: thousands of posts repeating a claim add nothing to its score.
Calibration cases (Gleiwitz 1939, Lavon Affair 1954, Operation Northwoods 1962, Sandy Hook "hoax" claims)
check that the scoring separates documented false flags from debunked ones.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

On Windows you can double-click `run.bat`.

## Optional keys (environment variables)

| Variable | Enables |
|---|---|
| `ANTHROPIC_API_KEY` | AI analyst (console.anthropic.com) |
| `X_BEARER_TOKEN` | Posts from x.com via the official X API v2 (developer.x.com; recent search needs a paid tier) |

Windows: `set ANTHROPIC_API_KEY=...` in the same Command Prompt before `streamlit run app.py`.

## Data

- `data/cases.json` — cases and their arguments (edited by the app's forms and AI analyst)
- `data/source_ratings.json` — source-type labels for domains
- `core.py` — evidence weights, verification multipliers, prior and verdict bands
