#!/usr/bin/env python3
"""Check OpenRouter credit balance. Exit 0=OK, 1=LOW (<$1), 2=ERROR. Prints remaining $."""
import sys, json, urllib.request

key = None
for line in open("/Users/minimi/.hermes/profiles/morti/.env", encoding="utf-8", errors="ignore"):
    if line.startswith("OPENROUTER_API_KEY="):
        key = line.split("=", 1)[1].strip().strip('"').strip("'")
        break

if not key:
    print("NO_KEY")
    sys.exit(2)

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/credits",
    headers={"Authorization": "Bearer " + key, "User-Agent": "morti"},
)
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode()).get("data", {})
    rem = float(d.get("total_credits", 0)) - float(d.get("total_usage", 0))
    print(f"{rem:.2f}")
    sys.exit(0 if rem >= 1.0 else 1)
except Exception as e:
    print("ERR:" + str(e)[:80])
    sys.exit(2)
