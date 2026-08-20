#!/usr/bin/env python3
"""Fetch a live market snapshot from Alpaca IEX for the Morti Race opening picks."""
import json, os, urllib.request
from datetime import datetime, timezone

ENV_PATH = "/Users/minimi/.hermes/profiles/morticapital/.env"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def main():
    env = load_env(ENV_PATH)
    key, secret, base = env.get("ALPACA_KEY"), env.get("ALPACA_SECRET"), env.get("ALPACA_BASE_URL")
    if not key or not base:
        print("FATAL: Alpaca creds not found in", ENV_PATH)
        return

    indices = ["SPY", "QQQ", "DIA", "IWM", "VXX"]
    sectors = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
    megacaps = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AVGO"]
    symbols = sorted(set(indices + sectors + megacaps))

    data_base = "https://data.alpaca.markets"
    url = f"{data_base}/v2/stocks/snapshots?symbols={','.join(symbols)}&feed=iex"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret,
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())

    snap = {}
    for sym, d in data.items():
        trade = d.get("latestTrade") or {}
        prev = d.get("prevDailyBar") or {}
        daily = d.get("dailyBar") or {}
        price = trade.get("p") or daily.get("c")
        prev_close = prev.get("c")
        chg = round(((price / prev_close) - 1) * 100, 2) if (price and prev_close) else None
        snap[sym] = {"price": price, "prev_close": prev_close, "chg_pct": chg}

    outdir = os.path.join(ROOT, "data")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "market_snapshot.json")
    payload = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "universe": snap}
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(snap, indent=2))
    print(f"\nSaved → {out}")


if __name__ == "__main__":
    main()
