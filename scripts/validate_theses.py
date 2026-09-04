#!/usr/bin/env python3
"""Thesis freshness validator.
Rejects theses that mention past events as future (e.g. 'ahead of NVDA earnings' after 2026-08-26).
Run after every cycle. Exit 1 if any thesis is invalid.
"""
import json, os, re, sys
from datetime import datetime

REPO = "/Users/minimi/Claude Working files/morti-race"
LEDGER = os.path.join(REPO, "data", "ledger.json")

PAST_EVENTS = [
    (r"ahead of.*nvda.*earnings", "NVDA reported 2026-08-26"),
    (r"pre-nvda", "NVDA reported 2026-08-26"),
    (r"ahead of.*earnings.*aug", "earnings already reported"),
]

def is_stale(text):
    if not text:
        return False
    t = text.lower()
    for pat, reason in PAST_EVENTS:
        if re.search(pat, t):
            return reason
    return False

def main():
    if not os.path.exists(LEDGER):
        print("no ledger")
        sys.exit(0)
    led = json.load(open(LEDGER))
    bad = []
    for mid, m in led.get("models", {}).items():
        thesis = m.get("thesis", "")
        reason = is_stale(thesis)
        if reason:
            bad.append((mid, reason, thesis[:80]))
    if bad:
        for mid, reason, snippet in bad:
            print(f"STALE [{mid}]: {reason}")
            print(f"  thesis: {snippet}...")
        sys.exit(1)
    print("theses validated: all current")
    sys.exit(0)

if __name__ == "__main__":
    main()
