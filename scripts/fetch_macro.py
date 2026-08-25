#!/usr/bin/env python3
"""Fetch macro regime (FRED rates / yields / VIX) → data/macro.json for model decisions.

Adds a concise, model-facing "macro regime" summary (fed funds, 10Y/2Y curve,
VIX vol regime) on top of the price snapshot. Cheap (FRED is free) and no LLM.
"""
import json, os, urllib.request
from datetime import datetime, timezone

ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERIES = {
    "fed_funds": "FEDFUNDS",
    "us10y": "DGS10",
    "us2y": "DGS2",
    "vix": "VIXCLS",
}


def load_env(path):
    env = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def fred_latest(series_id, key):
    url = (f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}"
           f"&api_key={key}&file_type=json&sort_order=desc&limit=3")
    req = urllib.request.Request(url, headers={"User-Agent": "morti"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode())
    for obs in data.get("observations", []):
        v = obs.get("value")
        if v not in (None, ".", ""):
            try:
                return float(v), obs.get("date")
            except (TypeError, ValueError):
                continue
    return None, None


def main():
    env = load_env(ENV_PATH)
    key = env.get("FRED_API_KEY") or env.get("FRED_KEY") or \
        next((v for k, v in env.items() if "FRED" in k.upper()), None)

    out = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "series": {}, "summary": ""}
    if key:
        for name, sid in SERIES.items():
            try:
                v, d = fred_latest(sid, key)
                if v is not None:
                    out["series"][name] = {"value": v, "date": d}
            except Exception as e:
                out["series"][name] = {"error": str(e)[:80]}

    s = out["series"]
    parts = []
    if "fed_funds" in s:
        parts.append(f"Fed funds {s['fed_funds']['value']:.2f}%")
    if "us10y" in s:
        parts.append(f"10Y {s['us10y']['value']:.2f}%")
    if "us2y" in s:
        parts.append(f"2Y {s['us2y']['value']:.2f}%")
    if "us10y" in s and "us2y" in s:
        curve = s["us10y"]["value"] - s["us2y"]["value"]
        parts.append(f"curve {'+' if curve >= 0 else ''}{curve:.2f}% ({'steep' if curve >= 0 else 'INVERTED'})")
    if "vix" in s:
        v = s["vix"]["value"]
        regime = "low vol" if v < 15 else ("normal" if v < 20 else ("elevated" if v < 25 else "HIGH vol / risk-off"))
        parts.append(f"VIX {v:.1f} ({regime})")
    out["summary"] = ("Macro: " + "; ".join(parts)) if parts else "(macro data unavailable)"

    path = os.path.join(ROOT, "data", "macro.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(out["summary"])


if __name__ == "__main__":
    main()
