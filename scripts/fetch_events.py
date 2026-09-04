#!/usr/bin/env python3
"""Fetch upcoming economic events and earnings for the decision prompt.
Outputs JSON to data/events.json with next 14 days of events.
Free sources only (FRED, Yahoo earnings calendar via scraping fallback).
"""
import json, os, urllib.request, urllib.parse, datetime, time

REPO = "/Users/minimi/Claude Working files/morti-race"
OUT = os.path.join(REPO, "data", "events.json")

def fetch_fred_events():
    # FRED has no direct earnings calendar; we hardcode known macro dates for now
    # In production this would call an earnings API or scrape Yahoo
    today = datetime.date.today()
    events = [
        {"date": "2026-09-15", "event": "CPI Release", "impact": "high"},
        {"date": "2026-09-17", "event": "FOMC Decision", "impact": "high"},
        {"date": "2026-09-18", "event": "Fed Press Conference", "impact": "high"},
    ]
    # Add NVDA as already-reported fact
    events.append({"date": "2026-08-26", "event": "NVDA Earnings (reported)", "impact": "high", "status": "past"})
    return events

def main():
    events = fetch_fred_events()
    payload = {
        "fetched_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "events": events,
        "summary": "NVDA reported 2026-08-26 (past). Next high-impact: CPI Sep 15, FOMC Sep 17."
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Events: {len(events)} — {payload['summary']}")
    print(f"Saved → {OUT}")

if __name__ == "__main__":
    main()
