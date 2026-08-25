#!/usr/bin/env python3
"""Intraday risk layer for Morti Race — executes stop-losses + flee-to-safety.

Reads data/ledger.json, fetches live prices (Alpaca IEX equities + crypto),
closes equity/crypto positions that breach their stop, and flattens everything
on a market-crash trigger (SPY). Silent when no action, so the cron delivers
stdout only when something actually closes.
"""
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
LEDGER = os.path.join(ROOT, "data", "ledger.json")
SNAPSHOT = os.path.join(ROOT, "data", "market_snapshot.json")

FLEE_INDEX = "SPY"
FLEE_THRESHOLD = -2.0   # % from prev close that triggers full flatten
ET = ZoneInfo("America/New_York")

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


def _headers(env):
    return {"APCA-API-KEY-ID": env["ALPACA_KEY"], "APCA-API-SECRET-KEY": env["ALPACA_SECRET"]}


def fetch_prices(symbols, env):
    eq = [s for s in symbols if s not in CRYPTO]
    cr = [s for s in symbols if s in CRYPTO]
    prices = {}
    if eq:
        url = f"https://data.alpaca.markets/v2/stocks/snapshots?symbols={','.join(eq)}&feed=iex"
        req = urllib.request.Request(url, headers=_headers(env))
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        for s, d in data.items():
            t = d.get("latestTrade") or {}
            db = d.get("dailyBar") or {}
            p = t.get("p") or db.get("c")
            if p:
                prices[s] = p
    if cr:
        pairs = ",".join(urllib.parse.quote(f"{s}/USD", safe="") for s in cr)
        url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols={pairs}"
        req = urllib.request.Request(url, headers=_headers(env))
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            for pair, bar in data.get("bars", {}).items():
                prices[pair.split("/")[0]] = bar.get("c")
        except Exception:
            pass
    return prices


def in_market_hours(now_et):
    if now_et.weekday() >= 5:   # Sat/Sun
        return False
    mins = now_et.hour * 60 + now_et.minute
    return 570 <= mins <= 960   # 09:30–16:00 ET


def main():
    if not os.path.exists(LEDGER):
        sys.exit(0)
    now_et = datetime.now(ET)
    if not in_market_hours(now_et):
        sys.exit(0)   # silent outside market hours

    env = load_env(ENV_PATH)
    if not env.get("ALPACA_KEY"):
        sys.exit(0)

    with open(LEDGER) as f:
        ledger = json.load(f)

    tickers = set()
    for m in ledger.get("models", {}).values():
        for p in m.get("positions", []):
            if p.get("kind") == "equity":
                tickers.add(p["ticker"])
    if not tickers:
        sys.exit(0)
    tickers.add(FLEE_INDEX)

    try:
        prices = fetch_prices(sorted(tickers), env)
    except Exception:
        sys.exit(0)   # price fetch failed → silent (retry next tick)

    # flee trigger: SPY down >= threshold vs prev close
    spy_prev = None
    if os.path.exists(SNAPSHOT):
        try:
            snap = json.load(open(SNAPSHOT))
            spy_prev = (snap.get("universe", {}).get(FLEE_INDEX) or {}).get("prev_close")
        except Exception:
            spy_prev = None
    spy = prices.get(FLEE_INDEX)
    flee = bool(spy and spy_prev and ((spy / spy_prev) - 1.0) * 100.0 <= FLEE_THRESHOLD)

    events = []
    for mid, m in ledger.get("models", {}).items():
        for p in list(m.get("positions", [])):
            if p.get("kind") != "equity":
                continue
            t = p["ticker"]
            last = prices.get(t)
            if not last:
                continue
            stop = p.get("stop")
            side = p.get("side", "long")
            hit = bool(stop) and ((side == "long" and last <= stop) or (side == "short" and last >= stop))
            if not (hit or flee):
                continue
            shares = p.get("shares", 0) or 0
            entry = p.get("entry", 0) or 0
            pnl = ((entry - last) if side == "short" else (last - entry)) * shares
            events.append({
                "ts": now_et.isoformat(), "model": m.get("name", mid), "ticker": t,
                "side": side, "exit": round(last, 2), "entry": entry,
                "pnl": round(pnl, 2), "reason": "FLEE" if flee else "STOP",
            })
            m["positions"].remove(p)
            m["equity"] = round(m.get("equity", 0) + pnl, 2)
            m["realized_pnl"] = round(m.get("realized_pnl", 0) + pnl, 2)

    if not events:
        sys.exit(0)   # silent

    for m in ledger.get("models", {}).values():
        invested = sum(x.get("dollar", 0) for x in m.get("positions", []))
        m["invested"] = round(invested, 2)
        m["cash"] = round(m.get("equity", 0) - invested, 2)
        m["alloc_pct"] = round(invested / m["equity"] * 100, 1) if m.get("equity") else 0
        m["n_positions"] = len(m.get("positions", []))

    ledger["as_of"] = now_et.astimezone(timezone.utc).isoformat()
    with open(LEDGER, "w") as f:
        json.dump(ledger, f, indent=2)

    ev_path = os.path.join(ROOT, "data", "intraday_events.jsonl")
    with open(ev_path, "a") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")

    print(f"🚨 Intraday risk: {len(events)} position(s) closed" + (" — FLEE TO SAFETY" if flee else ""))
    for e in events:
        print(f"  • {e['model']}: {e['side'].upper()} {e['ticker']} → {e['reason']} @ ${e['exit']:,.2f} ({e['pnl']:+,.0f})")


if __name__ == "__main__":
    main()
