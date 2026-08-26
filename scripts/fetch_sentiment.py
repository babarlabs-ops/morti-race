#!/usr/bin/env python3
"""X (Twitter) sentiment via xAI x_search (paid credits) -> data/sentiment.json.

Runs a SMALL, bounded set of searches (one market-wide + the top movers from the
live snapshot) and records token usage so cost is visible in the cycle log.
Import the existing x_search module (same dir) rather than duplicating the
xAI Responses API wiring.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x_search import x_search  # noqa: E402
from datetime import datetime, timezone  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_MOVERS = 3
MAX_OUTPUT = 600


def load_snapshot():
    p = os.path.join(ROOT, "data", "market_snapshot.json")
    if not os.path.exists(p):
        return {}
    try:
        return json.load(open(p))
    except Exception:
        return {}


def top_movers(snap, n):
    uni = snap.get("universe", {})
    items = [(s, d.get("chg_pct")) for s, d in uni.items()
             if isinstance(d, dict) and isinstance(d.get("chg_pct"), (int, float))]
    items.sort(key=lambda kv: -abs(kv[1]))
    return [s for s, _ in items[:n]]


def main():
    queries = ["What is driving the US stock market today? Key movers, macro catalysts, and biggest risks."]
    for sym in top_movers(load_snapshot(), N_MOVERS):
        queries.append(f"${sym} stock — what are traders saying today? Bull and bear catalysts.")

    results = []
    usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for q in queries:
        try:
            text, cites, data = x_search(q, max_output_tokens=MAX_OUTPUT)
            u = data.get("usage", {}) or {}
            for k in ("input_tokens", "output_tokens", "total_tokens"):
                usage[k] = usage.get(k, 0) + (u.get(k) or 0)
            results.append({"query": q, "text": (text or "")[:700], "citations": (cites or [])[:5]})
        except Exception as e:
            results.append({"query": q, "error": str(e)[:160]})
        time.sleep(1)

    lines = ["X / TWITTER SENTIMENT (xAI x_search):"]
    for r in results:
        if "error" in r:
            lines.append(f"- {r['query'][:60]}... ERROR: {r['error'][:90]}")
        else:
            lines.append(f"- {r['text'][:350]}")
    out = {
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "usage": usage,
        "summary": "\n".join(lines),
    }
    path = os.path.join(ROOT, "data", "sentiment.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])
    print(f"[sentiment usage] {usage}")


if __name__ == "__main__":
    main()
