#!/usr/bin/env python3
"""Fetch market news headlines (free RSS, no API key) -> data/news.json.

Yahoo Finance RSS (market + Dow) with a Google News RSS fallback. Deduped by
title and capped to keep the model prompt tight. Graceful: never crashes the
cycle; an empty/failed feed just leaves a shorter summary.
"""
import json, os, urllib.request, urllib.error, xml.etree.ElementTree as ET
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEEDS = [
    ("Yahoo Market", "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EGSPC&region=US&lang=en-US"),
    ("Yahoo Dow", "https://feeds.finance.yahoo.com/rss/2.0/headline?s=%5EDJI&region=US&lang=en-US"),
    ("Google News", "https://news.google.com/rss/search?q=stock%20market%20OR%20federal%20reserve%20OR%20earnings&hl=en-US&gl=US&ceid=US:en"),
]
MAX_HEADLINES = 16
UA = "MortiResearch/1.0 (morti@morti.capital)"


def fetch_feed(name, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    root = ET.fromstring(data)
    out = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        if not title:
            continue
        pub = item.findtext("pubDate") or ""
        out.append({"title": title[:140], "source": name, "date": pub[:22]})
    return out


def main():
    out = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "headlines": [], "summary": ""}
    seen = set()
    for name, url in FEEDS:
        try:
            for it in fetch_feed(name, url):
                key = it["title"].lower()[:80]
                if key in seen:
                    continue
                seen.add(key)
                out["headlines"].append(it)
        except Exception as e:
            out.setdefault("errors", {})[name] = str(e)[:120]
    out["headlines"] = out["headlines"][:MAX_HEADLINES]
    lines = [f"- {h['title']} ({h['source']})" for h in out["headlines"]]
    out["summary"] = ("NEWS HEADLINES (top %d):\n%s" % (len(lines), "\n".join(lines))) if lines else "(news unavailable)"
    path = os.path.join(ROOT, "data", "news.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])


if __name__ == "__main__":
    main()
