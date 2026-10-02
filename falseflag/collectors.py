"""Collect news articles and social media posts about a case.

Sources:
  - Google News RSS (news sites, no key)
  - GDELT DOC 2.0 API (global news database, no key)
  - Reddit public search (no key)
  - X (Twitter) API v2 recent search (requires X_BEARER_TOKEN; scraping x.com is not used)
"""
import json
import os
import re
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse

import feedparser
import requests

UA = {"User-Agent": "FalseFlagClaimChecker/1.0 (research tool)"}
RATINGS = json.loads((Path(__file__).parent / "data" / "source_ratings.json").read_text(encoding="utf-8"))

DEBUNK_WORDS = re.compile(r"fact.?check|debunk|false claim|conspiracy theor|misinformation|disinformation|"
                          r"no evidence|fake (bbc|report|video|news)|antisemitic", re.I)
CLAIM_WORDS = re.compile(r"false.?flag|staged|inside job|hoax|crisis actor|psyop|orchestrated by", re.I)


def domain_of(url):
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def source_label(domain):
    for label, domains in RATINGS.items():
        if label.startswith("_"):
            continue
        if any(domain == d or domain.endswith("." + d) for d in domains):
            return label.replace("_", " ")
    return "unrated"


def stance(text):
    """Rough keyword tag. Not a truth judgement — just how the item relates to the claim."""
    if DEBUNK_WORDS.search(text):
        return "debunks / reports on claim"
    if CLAIM_WORDS.search(text):
        return "promotes claim"
    return "reports event"


def _item(platform, title, url, published, domain=None, text="", engagement=None):
    domain = domain or domain_of(url)
    return {
        "platform": platform,
        "title": title.strip(),
        "url": url,
        "published": published,
        "domain": domain,
        "source_type": source_label(domain),
        "stance": stance(f"{title} {text}"),
        "text": text[:500],
        "engagement": engagement,
    }


def google_news(query, limit=30):
    resp = requests.get("https://news.google.com/rss/search", headers=UA, timeout=15,
                        params={"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    out = []
    for e in feed.entries[:limit]:
        src = e.get("source", {})
        domain = domain_of(src.get("href", "")) if src.get("href") else domain_of(e.link)
        try:
            published = parsedate_to_datetime(e.published).isoformat()
        except (AttributeError, TypeError, ValueError):
            published = ""
        out.append(_item("News (Google News)", e.title, e.link, published, domain))
    return out


def gdelt(query, limit=50):
    resp = requests.get("https://api.gdeltproject.org/api/v2/doc/doc", headers=UA, timeout=20,
                        params={"query": query, "mode": "artlist", "format": "json",
                                "maxrecords": limit, "sort": "datedesc"})
    resp.raise_for_status()
    try:
        articles = resp.json().get("articles", [])
    except ValueError:  # GDELT returns plain text for malformed queries
        raise ValueError(resp.text[:200])
    return [_item("News (GDELT)", a.get("title", ""), a["url"], a.get("seendate", ""), a.get("domain"))
            for a in articles]


def reddit(query, limit=30):
    resp = requests.get("https://www.reddit.com/search.json", headers=UA, timeout=15,
                        params={"q": query, "sort": "new", "limit": limit})
    resp.raise_for_status()
    out = []
    for child in resp.json().get("data", {}).get("children", []):
        d = child["data"]
        out.append(_item("Reddit", d.get("title", ""), "https://www.reddit.com" + d.get("permalink", ""),
                         str(d.get("created_utc", "")), "reddit.com", d.get("selftext", ""),
                         {"score": d.get("score"), "comments": d.get("num_comments")}))
    return out


def x_posts(query, limit=50, token=None):
    token = token or os.environ.get("X_BEARER_TOKEN")
    if not token:
        raise RuntimeError("Set X_BEARER_TOKEN (X API v2) to include posts from x.com.")
    resp = requests.get("https://api.x.com/2/tweets/search/recent", timeout=15,
                        headers={"Authorization": f"Bearer {token}", **UA},
                        params={"query": f"({query}) -is:retweet", "max_results": max(10, min(limit, 100)),
                                "tweet.fields": "created_at,public_metrics,author_id",
                                "expansions": "author_id", "user.fields": "username"})
    resp.raise_for_status()
    body = resp.json()
    users = {u["id"]: u["username"] for u in body.get("includes", {}).get("users", [])}
    out = []
    for t in body.get("data", []):
        user = users.get(t["author_id"], "i")
        out.append(_item("X", t["text"][:140], f"https://x.com/{user}/status/{t['id']}",
                         t.get("created_at", ""), "x.com", t["text"], t.get("public_metrics")))
    return out


COLLECTORS = {
    "News (Google News)": google_news,
    "News (GDELT)": gdelt,
    "Reddit": reddit,
    "X": x_posts,
}


def collect(query, platforms, limit=30):
    """Run the chosen collectors. Returns (items, errors) — one failing source never stops the others."""
    items, errors = [], {}
    for name in platforms:
        try:
            items.extend(COLLECTORS[name](query, limit))
        except Exception as exc:  # network errors, missing token, API limits
            errors[name] = f"{exc.__class__.__name__}: {exc}"[:300]
    seen, unique = set(), []
    for it in items:
        if it["url"] not in seen:
            seen.add(it["url"])
            unique.append(it)
    return unique, errors
