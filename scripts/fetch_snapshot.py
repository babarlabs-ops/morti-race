#!/usr/bin/env python3
"""Fetch a live market snapshot (equities + crypto) for Morti Race picks.

Equities: Alpaca IEX stock snapshots. Crypto: Alpaca crypto latest bars.
Broad universe so models see ALL assets as fair game (less ETF-heavy).
"""
import json, os, urllib.request, urllib.parse
from datetime import datetime, timezone

ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
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


def fetch_stocks(symbols, env):
    key, secret = env.get("ALPACA_KEY"), env.get("ALPACA_SECRET")
    url = f"https://data.alpaca.markets/v2/stocks/snapshots?symbols={','.join(symbols)}&feed=iex"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret,
    })
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.loads(r.read().decode())
    out = {}
    for sym, d in data.items():
        trade = d.get("latestTrade") or {}
        prev = d.get("prevDailyBar") or {}
        daily = d.get("dailyBar") or {}
        price = trade.get("p") or daily.get("c")
        prev_close = prev.get("c")
        chg = round(((price / prev_close) - 1) * 100, 2) if (price and prev_close) else None
        out[sym] = {"price": price, "prev_close": prev_close, "chg_pct": chg}
    return out


def fetch_crypto(symbols, env):
    key, secret = env.get("ALPACA_KEY"), env.get("ALPACA_SECRET")
    pairs = ",".join(urllib.parse.quote(f"{s}/USD", safe="") for s in symbols)
    url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols={pairs}"
    req = urllib.request.Request(url, headers={
        "APCA-API-KEY-ID": key, "APCA-API-SECRET-KEY": secret,
    })
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.loads(r.read().decode())
    out = {}
    for pair, bar in data.get("bars", {}).items():
        sym = pair.split("/")[0]
        close, open_ = bar.get("c"), bar.get("o")
        chg = round(((close / open_) - 1) * 100, 2) if (close and open_) else None
        out[sym] = {"price": close, "prev_close": None, "chg_pct": chg}
    return out


def main():
    env = load_env(ENV_PATH)
    if not env.get("ALPACA_KEY") or not env.get("ALPACA_BASE_URL"):
        print("FATAL: Alpaca creds not found in", ENV_PATH)
        return

    indices = ["SPY", "QQQ", "DIA", "IWM", "VXX"]
    sectors = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLY", "XLP", "XLU", "XLB", "XLRE", "XLC"]
    megacaps = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AVGO"]
    singles = [
        # AI / semis
        "AMD", "INTC", "MU", "QCOM", "TSM", "ARM", "SMCI", "MRVL", "PLTR",
        # software / cloud
        "CRM", "ORCL", "ADBE", "NFLX", "SNOW", "DDOG", "PANW", "CRWD", "NET",
        # consumer / internet
        "SHOP", "UBER", "ABNB", "DIS", "NKE", "SBUX", "COST", "WMT", "TGT",
        # fintech / crypto-adjacent
        "COIN", "MSTR", "HOOD", "SQ", "PYPL",
        # industrials / cyclicals
        "BA", "CAT", "GE", "DE", "HON",
        # financials
        "JPM", "GS", "V", "MA", "BAC",
        # healthcare
        "UNH", "LLY", "PFE", "MRK", "ABBV",
        # energy
        "CVX", "XOM", "SLB",
        # autos / EV
        "F", "GM", "RIVN", "LCID", "NIO",
    ]
    crypto = ["BTC", "ETH", "SOL", "DOGE"]

    stock_symbols = sorted(set(indices + sectors + megacaps + singles))
    snap = fetch_stocks(stock_symbols, env)
    try:
        snap.update(fetch_crypto(crypto, env))
    except Exception as e:
        print(f"WARN: crypto fetch failed: {e}")

    outdir = os.path.join(ROOT, "data")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, "market_snapshot.json")
    payload = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "universe": snap}
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"Universe: {len(snap)} symbols (equities + crypto)")
    print(f"Saved → {out}")


if __name__ == "__main__":
    main()
