#!/usr/bin/env python3
"""Build the virtual ledger — continuous, compounding.

Each cycle: mark the previous book to market (realize P&L), then establish
today's book from each model's desired allocation. Equity compounds across days.
Supports equities, ETFs, crypto, and defined-risk options (long calls/puts).

Persistent state lives in data/ledger.json: each run reads the prior ledger
(equity + positions), realizes P&L at live prices, then writes the new ledger.
"""
import json, os, math, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
START = 100000

CRYPTO = {"BTC", "ETH", "SOL", "DOGE", "XRP", "ADA", "LTC", "AVAX", "LINK", "DOT",
          "BCH", "UNI", "SHIB", "PEPE", "TRX", "XLM", "NEAR", "APT", "SUI", "ARB",
          "OP", "TON", "INJ", "MATIC", "WIF", "BONK"}

# options pricing assumptions
VOL = 0.35   # fixed annualized volatility
RATE = 0.04  # risk-free rate
MULT = 100   # option contract multiplier


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
            print(f"WARN crypto price fetch failed: {e}")
    return prices


# ---- Black-Scholes ----
def _N(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_price(spot, strike, t_years, is_call):
    if t_years <= 0:
        return max(0.0, spot - strike) if is_call else max(0.0, strike - spot)
    d1 = (math.log(spot / strike) + (RATE + 0.5 * VOL * VOL) * t_years) / (VOL * math.sqrt(t_years))
    d2 = d1 - VOL * math.sqrt(t_years)
    if is_call:
        return spot * _N(d1) - strike * math.exp(-RATE * t_years) * _N(d2)
    return strike * math.exp(-RATE * t_years) * _N(-d2) - spot * _N(-d1)


def option_value(opt, spot, now=None):
    """Value an option position given its stored fields + current spot."""
    expiry = datetime.fromisoformat(opt["expiry"])
    now = now or datetime.now(timezone.utc)
    t_years = max(0.0, (expiry - now).total_seconds() / (365.0 * 86400.0))
    return bs_price(spot, opt["strike"], t_years, opt["is_call"])


def main():
    env = load_env(ENV_PATH)
    picks_dir = os.path.join(ROOT, "data", "picks")
    files = sorted(f for f in os.listdir(picks_dir) if f.endswith(".json"))
    picks = json.loads(read(os.path.join(picks_dir, files[-1])))
    snap = json.loads(read(os.path.join(ROOT, "data", "market_snapshot.json")))
    entry_prices = {k: v["price"] for k, v in snap["universe"].items() if v.get("price")}

    # prior state
    ledger_path = os.path.join(ROOT, "data", "ledger.json")
    prev = None
    if os.path.exists(ledger_path):
        try:
            prev = json.loads(read(ledger_path))
        except Exception:
            prev = None

    # collect all tickers needed: prior positions (underlyings) + today's picks (underlyings)
    all_tickers = set()
    for r in picks["results"].values():
        p = r.get("picks")
        if isinstance(p, dict):
            for pos in p.get("positions", []):
                t = (pos.get("ticker") or "").upper()
                if t and (pos.get("alloc_pct", 0) or 0) > 0:
                    all_tickers.add(t)
    if prev:
        for m in prev.get("models", {}).values():
            for pos in m.get("positions", []):
                all_tickers.add(pos["ticker"])
    live = fetch_prices(sorted(all_tickers), env)

    now = datetime.now(timezone.utc)
    ledger = {"as_of": now.isoformat(), "start_capital": START, "target": 1000000, "models": {}}

    for mid, r in picks["results"].items():
        name, tier = r.get("model"), r.get("tier")
        p = r.get("picks")
        p_dict = p if isinstance(p, dict) else {}

        # 1. realize P&L on the prior book
        prev_equity = START
        realized = 0.0
        if prev and mid in prev["models"]:
            pm = prev["models"][mid]
            prev_equity = pm.get("equity", START)
            for op in pm.get("positions", []):
                cur = live.get(op["ticker"], op.get("last"))
                if op.get("kind") == "option":
                    cur = option_value(op, live.get(op["ticker"], op["underlying_spot"]), now)
                    pnl = (cur - op["premium"]) * op["contracts"] * MULT
                elif op.get("side") == "short":
                    pnl = (op["entry"] - cur) * op["shares"]
                else:
                    pnl = (cur - op["entry"]) * op["shares"]
                realized += pnl
        equity = prev_equity + realized

        # 2. establish today's book from desired allocation
        positions = []
        for pos in p_dict.get("positions", []):
            ticker = (pos.get("ticker") or "").upper()
            side = (pos.get("side") or "long").lower()
            kind = pos.get("type") or pos.get("kind") or ("option" if pos.get("strike_pct") else "equity")
            alloc = pos.get("alloc_pct", 0) or 0
            if alloc <= 0:
                continue
            dollar = equity * alloc / 100.0

            if kind in ("long_call", "long_put", "option"):
                spot = live.get(ticker)
                if not spot:
                    continue
                is_call = kind in ("long_call", "option") or (pos.get("side", "long") == "long" and kind == "option")
                # default: treat "option" type + side long => call, short => put
                if kind == "option":
                    is_call = (pos.get("side", "long") == "long")
                strike_pct = max(1, min(40, pos.get("strike_pct", 5) or 5))
                strike = spot * (1 + strike_pct / 100.0) if is_call else spot * (1 - strike_pct / 100.0)
                expiry_days = pos.get("expiry_days", 30) or 30
                expiry = (now + timedelta(days=expiry_days)).isoformat()
                premium = bs_price(spot, strike, expiry_days / 365.0, is_call)
                if premium <= 0:
                    continue
                contracts = int(dollar / (premium * MULT))
                if contracts <= 0:
                    continue
                value = contracts * premium * MULT
                positions.append({
                    "ticker": ticker, "side": side, "kind": "option", "is_call": is_call,
                    "alloc_pct": alloc, "dollar": round(value, 2),
                    "contracts": contracts, "strike": round(strike, 2), "premium": premium,
                    "expiry": expiry, "underlying_spot": spot,
                    "entry": spot, "last": spot, "unrealized_pnl": 0.0, "unrealized_pnl_pct": 0.0,
                    "is_crypto": ticker in CRYPTO,
                    "thesis": (pos.get("thesis") or "")[:180],
                })
            else:
                if ticker not in entry_prices or ticker not in live:
                    continue
                entry = live[ticker]
                stop_pct = pos.get("stop_pct", 0) or 0
                target_pct = pos.get("target_pct", 0) or 0
                if side == "short":
                    stop_px = entry * (1 + abs(stop_pct) / 100.0)
                    target_px = entry * (1 - abs(target_pct) / 100.0)
                else:
                    stop_px = entry * (1 - abs(stop_pct) / 100.0)
                    target_px = entry * (1 + abs(target_pct) / 100.0)
                shares = dollar / entry
                positions.append({
                    "ticker": ticker, "side": side, "kind": "equity", "alloc_pct": alloc,
                    "dollar": round(dollar, 2), "shares": round(shares, 4),
                    "entry": entry, "last": entry, "stop": round(stop_px, 2), "target": round(target_px, 2),
                    "stop_pct": round(stop_pct, 2), "target_pct": round(target_pct, 2),
                    "unrealized_pnl": 0.0, "unrealized_pnl_pct": 0.0,
                    "is_crypto": ticker in CRYPTO,
                    "thesis": (pos.get("thesis") or "")[:180],
                })

        invested = sum(x["dollar"] for x in positions)
        cash = max(0.0, equity - invested)
        long_d = sum(x["dollar"] for x in positions if x["side"] == "long")
        short_d = sum(x["dollar"] for x in positions if x["side"] == "short")
        ledger["models"][mid] = {
            "name": name, "tier": tier,
            "thesis": (p_dict.get("thesis") or "").strip(),
            "justification": (p_dict.get("justification") or "").strip(),
            "realized_pnl": round(realized, 2),
            "cash": round(cash, 2), "invested": round(invested, 2),
            "alloc_pct": round(invested / equity * 100, 1) if equity else 0,
            "net_pct": round((long_d - short_d) / equity * 100, 1) if equity else 0,
            "unrealized_pnl": 0.0,
            "prev_equity": round(prev_equity, 2),
            "equity": round(equity, 2),
            "return_pct": round((equity / START - 1) * 100, 3),
            "n_positions": len(positions),
            "positions": positions,
        }

    os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
    with open(ledger_path, "w") as f:
        json.dump(ledger, f, indent=2)
    rows = sorted(ledger["models"].items(), key=lambda kv: -kv[1]["return_pct"])
    print("RANK  MODEL      EQUITY        RET%      POS  GROSS%   REALIZED")
    for i, (mid, m) in enumerate(rows, 1):
        print(f"{i:>4}  {m['name']:10s} ${m['equity']:>10,.2f}  {m['return_pct']:+8.3f}  {m['n_positions']:>3}  {m['alloc_pct']:>5.1f}  {m['realized_pnl']:>+10,.2f}")
    print(f"\nSaved → {ledger_path}")


if __name__ == "__main__":
    main()
