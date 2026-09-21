#!/usr/bin/env python3
"""Report model-level decision failures in the latest cycle.
Exit 1 when any model is DATA_BLOCKED so cron alerts rather than claiming full success.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = sorted((ROOT / "data" / "picks").glob("*.json"))
if not files:
    print("🚨 Morti cycle health: no picks file")
    raise SystemExit(1)
latest = files[-1]
data = json.loads(latest.read_text())
errors = []
for mid, result in data.get("results", {}).items():
    if result.get("error"):
        errors.append((result.get("model", mid), str(result["error"])[:120]))
if errors:
    names = ", ".join(name for name, _ in errors)
    print(f"⚠️ Morti partial cycle: DATA_BLOCKED models: {names}. Last valid books were carried forward; retry next cycle.")
    raise SystemExit(1)
print(f"cycle health PASS: {len(data.get('results', {}))} model decisions valid")
