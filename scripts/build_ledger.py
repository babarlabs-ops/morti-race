#!/usr/bin/env python3
"""Build the virtual ledger: normalize picks (shorts), validate, mark to market.

Handles both equities (IEX snapshots) and crypto (crypto bars) and passes
through each model's daily thesis + justification.
"""
import json, os, urllib.request, urllib.parse
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morticapital/.env"
START = 100000

# crypto tickers are priced via Alpaca's crypto endpoint, not the stock endpoint
CRYPTO = {"BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "LTC", "AVAX", "LINK", "DOT",
          "BCH", "UNI", "SHIB", "PEPE", "TRX", "XLM", "NEAR", "APT", "SUI", "ARB",
          "OP", "TON", "INJ", "MATIC", "WIF", "BONK"}


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


def read(p):
    with open(p) as f:
        return f.read()


def _headers(env):
    return {"APCA-API-KEY-ID": env["ALPACA_KEY"], "APCA-API-SECRET-KEY": env["ALPACA_SECRET"]}


def fetch_equity_prices(symbols, env):
    url = f"https://data.alpaca.markets/v2/stocks/snapshots?symbols={','.join(symbols)}&feed=iex"
    req = urllib.request.Request(url, headers=_headers(env))
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    prices = {}
    for s, d in data.items():
        t = d.get("latestTrade") or {}
        db = d.get("dailyBar") or {}
        prices[s] = t.get("p") or db.get("c")
    return prices


def fetch_crypto_prices(symbols, env):
    pairs = ",".join(urllib.parse.quote(f"{s}/USD", safe="") for s in symbols)
    url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols={pairs}"
    req = urllib.request.Request(url, headers=_headers(env))
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    prices = {}
    for pair, bar in data.get("bars", {}).items():
        prices[pair.split("/")[0]] = bar.get("c")
    return prices


def fetch_prices(symbols, env):
    eq = [s for s in symbols if s not in CRYPTO]
    cr = [s for s in symbols if s in CRYPTO]
    prices = {}
    if eq:
        prices.update(fetch_equity_prices(eq, env))
    if cr:
        try:
            prices.update(fetch_crypto_prices(cr, env))
        except Exception as e:
            print(f"WARN: crypto live price fetch failed: {e}")
    return prices


def main():
    env = load_env(ENV_PATH)
    picks_dir = os.path.join(ROOT, "data", "picks")
    files = sorted(f for f in os.listdir(picks_dir) if f.endswith(".json"))
    picks = json.loads(read(os.path.join(picks_dir, files[-1])))
    snap = json.loads(read(os.path.join(ROOT, "data", "market_snapshot.json")))
    entry_prices = {k: v["price"] for k, v in snap["universe"].items() if v.get("price")}

    all_tickers = set()
    for r in picks["results"].values():
        p = r.get("picks")
        if isinstance(p, dict):
            for pos in p.get("positions", []):
                t = (pos.get("ticker") or "").upper()
                if t and (pos.get("alloc_pct", 0) or 0) > 0:
                    all_tickers.add(t)
    live = fetch_prices(sorted(all_tickers), env)

    ledger = {"as_of": datetime.now(timezone.utc).isoformat(),
              "start_capital": START, "target": 1000000, "models": {}}

    for mid, r in picks["results"].items():
        name, tier = r.get("model"), r.get("tier")
        p = r.get("picks")
        p_dict = p if isinstance(p, dict) else {}
        positions = []
        for pos in p_dict.get("positions", []):
            ticker = (pos.get("ticker") or "").upper()
            side = (pos.get("side") or "long").lower()
            alloc = pos.get("alloc_pct", 0) or 0
            if ticker not in entry_prices or alloc <= 0:
                continue  # drop placeholders + unknown tickers
            entry = entry_prices[ticker]
            stop_pct = pos.get("stop_pct", 0) or 0
            target_pct = pos.get("target_pct", 0) or 0
            # normalize: shorts stop ABOVE entry (positive), target BELOW (negative)
            if side == "short":
                stop_px = entry * (1 + abs(stop_pct) / 100)
                target_px = entry * (1 - abs(target_pct) / 100)
            else:
                stop_px = entry * (1 - abs(stop_pct) / 100)
                target_px = entry * (1 + abs(target_pct) / 100)
            dollar = START * alloc / 100
            shares = dollar / entry
            last = live.get(ticker, entry)
            pnl = (last - entry) * shares if side == "long" else (entry - last) * shares
            positions.append({
                "ticker": ticker, "side": side, "alloc_pct": alloc,
                "is_crypto": ticker in CRYPTO,
                "dollar": round(dollar, 2), "shares": round(shares, 4),
                "entry": entry, "last": last, "stop": round(stop_px, 2), "target": round(target_px, 2),
                "stop_pct": round(stop_pct, 2), "target_pct": round(target_pct, 2),
                "unrealized_pnl": round(pnl, 2),
                "unrealized_pnl_pct": round(pnl / dollar * 100, 2) if dollar else 0,
                "thesis": (pos.get("thesis") or "")[:180],
            })
        cash = START - sum(x["dollar"] for x in positions)
        unrealized = sum(x["unrealized_pnl"] for x in positions)
        equity = START + unrealized
        gross = sum(x["dollar"] for x in positions)
        long_d = sum(x["dollar"] for x in positions if x["side"] == "long")
        short_d = sum(x["dollar"] for x in positions if x["side"] == "short")
        ledger["models"][mid] = {
            "name": name, "tier": tier,
            "thesis": (p_dict.get("thesis") or "").strip(),
            "justification": (p_dict.get("justification") or "").strip(),
            "cash": round(cash, 2), "invested": round(gross, 2),
            "alloc_pct": round(gross / START * 100, 1),
            "net_pct": round((long_d - short_d) / START * 100, 1),
            "unrealized_pnl": round(unrealized, 2),
            "equity": round(equity, 2),
            "return_pct": round((equity / START - 1) * 100, 3),
            "n_positions": len(positions),
            "positions": positions,
        }

    out = os.path.join(ROOT, "data", "ledger.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(ledger, f, indent=2)
    rows = sorted(ledger["models"].items(), key=lambda kv: -kv[1]["return_pct"])
    print("RANK  MODEL      EQUITY        RET%      POS  GROSS%")
    for i, (mid, m) in enumerate(rows, 1):
        print(f"{i:>4}  {m['name']:10s} ${m['equity']:>10,.2f}  {m['return_pct']:+8.3f}  {m['n_positions']:>3}  {m['alloc_pct']:>5.1f}")
    print(f"\nSaved → {out}")


if __name__ == "__main__":
    main()
