#!/usr/bin/env python3
"""Scrape Reddit sentiment -> data/reddit.json.

Reddit now hard-blocks anonymous .json scraping (HTTP 403). Two paths, in order:
  1. Anonymous scrape (still works on some networks) — no credentials.
  2. Reddit OAuth "script app" (client_credentials) — FREE, not the paid API,
     just needs REDDIT_CLIENT_ID + REDDIT_CLIENT_SECRET in the profile .env.

Extracts top posts + a ticker-mention tally into a compact summary. Graceful:
any failure degrades to an empty/flagged summary, never a cycle crash.
"""
import base64, json, os, re, time, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
SUBS = ["wallstreetbets", "stocks", "investing", "CryptoCurrency"]
UA = "MortiResearch/1.0 (morti@morti.capital)"
TICKER_RE = re.compile(r"\b[A-Z]{2,5}\b")
STOPWORDS = {"I", "II", "III", "AM", "PM", "THE", "AND", "FOR", "YOU", "ARE", "NOT",
             "BUT", "ITS", "NEW", "DAY", "WEEK", "RED", "CEO", "CFO", "AI", "USD",
             "ETF", "SPY", "THIS", "THAT", "WITH", "YOUR", "HAVE", "WILL", "FROM",
             "THEY", "US", "USA", "DD", "IT", "AT", "OR", "ON", "IN", "A", "B", "C",
             "ELON", "APP", "PDF", "TV", "IPO", "CPI", "FED", "GDP", "EPS"}


def load_env(path):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _parse(data):
    posts = []
    for c in data.get("data", {}).get("children", []):
        d = c.get("data", {})
        posts.append({
            "sub": d.get("subreddit", "?"),
            "title": d.get("title", "")[:160],
            "score": d.get("score") or 0,
            "num_comments": d.get("num_comments") or 0,
            "text": (d.get("selftext") or "")[:200],
        })
    return posts


def fetch_anonymous(sub):
    url = f"https://www.reddit.com/r/{sub}/hot.json?limit=20"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return _parse(json.loads(r.read().decode()))


def fetch_oauth(sub, token):
    url = f"https://oauth.reddit.com/r/{sub}/hot?limit=20"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return _parse(json.loads(r.read().decode()))


def get_oauth_token(client_id, client_secret):
    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token",
        data=b"grant_type=client_credentials",
        headers={"Authorization": f"Basic {auth}", "User-Agent": UA,
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())["access_token"]


def main():
    out = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "posts": [], "tickers": {}, "summary": ""}
    env = load_env(ENV_PATH)
    cid = env.get("REDDIT_CLIENT_ID")
    csec = env.get("REDDIT_CLIENT_SECRET")
    token = None
    if cid and csec:
        try:
            token = get_oauth_token(cid, csec)
        except Exception as e:
            out.setdefault("errors", {})["oauth_token"] = str(e)[:120]

    for sub in SUBS:
        try:
            posts = fetch_oauth(sub, token) if token else fetch_anonymous(sub)
            out["posts"].extend(posts)
        except urllib.error.HTTPError as e:
            if e.code == 403 and not token:
                out.setdefault("errors", {})[sub] = "403 blocked (anonymous scrape) — set REDDIT_CLIENT_ID/SECRET (free script app) in .env"
            else:
                out.setdefault("errors", {})[sub] = f"HTTP {e.code}"
        except Exception as e:
            out.setdefault("errors", {})[sub] = str(e)[:120]
        time.sleep(0.5)

    for p in out["posts"]:
        blob = (p["title"] + " " + p["text"]).upper()
        for t in set(TICKER_RE.findall(blob)) - STOPWORDS:
            out["tickers"][t] = out["tickers"].get(t, 0) + 1

    top_tickers = sorted(out["tickers"].items(), key=lambda kv: -kv[1])[:15]
    top_posts = sorted(out["posts"], key=lambda p: -(p["score"] or 0))[:12]
    lines = ["REDDIT SENTIMENT (top posts by score):"]
    lines += [f"- [r/{p['sub']}] {p['title']} (↑{p['score']}, {p['num_comments']}c)" for p in top_posts]
    if top_tickers:
        lines.append("Most-mentioned tickers: " + ", ".join(f"{t}({n})" for t, n in top_tickers))
    if not out["posts"]:
        lines.append("(blocked/failed — see errors)")
    out["summary"] = "\n".join(lines)

    path = os.path.join(ROOT, "data", "reddit.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])


if __name__ == "__main__":
    main()
