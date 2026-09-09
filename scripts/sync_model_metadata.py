#!/usr/bin/env python3
"""Synchronize immutable model identity metadata into the public ledger.
Does not touch prices, positions, P&L, or theses.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "models.json"
LEDGER = ROOT / "data" / "ledger.json"

cfg = json.loads(CONFIG.read_text())
ledger = json.loads(LEDGER.read_text())
by_id = {m["id"]: m for m in cfg["models"]}
updated = 0
for mid, row in ledger.get("models", {}).items():
    meta = by_id.get(mid)
    if not meta:
        continue
    for key in ("name", "parent", "tier", "cohort", "start_date"):
        if row.get(key) != meta.get(key, ""):
            row[key] = meta.get(key, "")
            updated += 1
    if row.get("model_id") != meta["model"]:
        row["model_id"] = meta["model"]
        updated += 1

LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
print(f"metadata fields updated: {updated}; ledger models: {len(ledger.get('models', {}))}")
