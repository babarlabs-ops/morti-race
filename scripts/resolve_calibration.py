#!/usr/bin/env python3
"""Morti Race — calibration resolver.

Turns every model's stated probability into a scored forecast. Each day, for
every position the models opened, we record the probability they attached to
"hits target before stop within the horizon". We then resolve those forecasts
as prices move (hit target / hit stop / exited / expired) and score the binary
outcome against the stated probability using the Brier score.

This is the fastest-converging skill signal in the whole system (BENCHMARK §2.3):
a usable calibration read emerges in weeks, where Sharpe takes years.

State lives in data/calibration.json (append-only in spirit — forecasts are only
ever added or resolved, never edited). Reads data/ledger.json for today's book.
"""
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"

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


def fetch_prices(symbols, env):
    """Fetch latest prices for a set of symbols (equities via IEX snapshots, crypto via bars)."""
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
            prices[s] = t.get("p") or db.get("c")
    if cr:
        pairs = ",".join(urllib.parse.quote(f"{s}/USD", safe="") for s in cr)
        url = f"https://data.alpaca.markets/v1beta3/crypto/us/latest/bars?symbols={pairs}"
        req = urllib.request.Request(url, headers=_headers(env))
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
        for pair, bar in data.get("bars", {}).items():
            prices[pair.split("/")[0]] = bar.get("c")
    return prices


def today_str():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def days_since(dstr):
    try:
        d = datetime.strptime(dstr, "%Y-%m-%d").date()
    except Exception:
        return None
    return (datetime.now(timezone.utc).date() - d).days


def valid_probability(p):
    try:
        p = float(p)
    except (TypeError, ValueError):
        return None
    if not (0.01 <= p <= 0.99):
        return None
    return p


def directional_side(pos):
    """Normalize to a directional side: options map to long (call) / short (put)."""
    if pos.get("kind") == "option":
        return "long" if pos.get("is_call") else "short"
    return (pos.get("side") or "long").lower()


def favorable(price, entry, side):
    """True if the move from entry to price is in the position's favor."""
    if side == "short":
        return price <= entry
    return price >= entry


def hit_stop(price, pos):
    if pos.get("stop") is None:
        return False
    stop = pos["stop"]
    return price <= stop if pos["side"] == "long" else price >= stop


def hit_target(price, pos):
    if pos.get("target") is None:
        return False
    target = pos["target"]
    return price >= target if pos["side"] == "long" else price <= target


def main():
    env = load_env(ENV_PATH)
    if not env.get("ALPACA_KEY"):
        print("FATAL: ALPACA_KEY not set")
        sys.exit(1)

    ledger_path = os.path.join(ROOT, "data", "ledger.json")
    calib_path = os.path.join(ROOT, "data", "calibration.json")

    if not os.path.exists(ledger_path):
        print("No ledger yet — nothing to calibrate.")
        sys.exit(0)

    ledger = json.loads(read(ledger_path))

    # Load prior calibration state (or start fresh).
    if os.path.exists(calib_path):
        calib = json.loads(read(calib_path))
    else:
        calib = {"as_of": None, "forecasts": [], "models": {}}
    forecasts = calib.get("forecasts", [])

    # Index OPEN forecasts by (model, ticker, side).
    open_by_key = {}
    for f in forecasts:
        if f.get("status") == "OPEN":
            open_by_key[(f["model"], f["ticker"], f["side"])] = f

    # Current book: {model: { (ticker, side): position }}.
    book = {}
    for mid, m in ledger.get("models", {}).items():
        book[mid] = {}
        for pos in m.get("positions", []):
            side = directional_side(pos)
            book[mid][(pos["ticker"].upper(), side)] = pos

    # Collect tickers we need prices for.
    tickers = set()
    for f in forecasts:
        if f.get("status") == "OPEN":
            tickers.add(f["ticker"])
    for mid, posmap in book.items():
        for (ticker, _side), _pos in posmap.items():
            tickers.add(ticker)

    try:
        prices = fetch_prices(sorted(tickers), env)
    except Exception as e:
        print(f"WARN price fetch failed: {e} — using last-known prices")
        prices = {}

    today = today_str()

    # 1. Resolve existing OPEN forecasts.
    for key, f in list(open_by_key.items()):
        mid, ticker, side = key
        price = prices.get(ticker)
        if price is None:
            price = f.get("last_price") or f.get("entry")
        f["last_price"] = price
        held = key in book.get(mid, {})
        expired = f.get("expiry_date") and f["expiry_date"] <= today

        if f.get("kind") == "option":
            # Options resolve by direction at drop or expiry; no stop/target.
            if not held:
                f.update(status="EXITED", outcome=1 if favorable(price, f["entry"], side) else 0,
                         resolved_date=today, resolved_price=price)
            elif expired:
                f.update(status="EXPIRED", outcome=1 if favorable(price, f["entry"], side) else 0,
                         resolved_date=today, resolved_price=price)
            continue

        # Equity / crypto: stop → target → dropped → expired (stop first = conservative).
        if hit_stop(price, f):
            f.update(status="STOPPED", outcome=0, resolved_date=today, resolved_price=price)
        elif hit_target(price, f):
            f.update(status="HIT_TARGET", outcome=1, resolved_date=today, resolved_price=price)
        elif not held:
            f.update(status="EXITED", outcome=1 if favorable(price, f["entry"], side) else 0,
                     resolved_date=today, resolved_price=price)
        elif expired:
            f.update(status="EXPIRED", outcome=0, resolved_date=today, resolved_price=price)
        # else: stays OPEN

    # 2. Create forecasts for current positions not yet tracked.
    created = 0
    for mid, posmap in book.items():
        name = ledger["models"][mid].get("name", mid)
        for (ticker, side), pos in posmap.items():
            key = (mid, ticker, side)
            if key in open_by_key:
                continue
            p = valid_probability(pos.get("probability"))
            if p is None:
                continue  # can't calibrate without a stated probability
            kind = pos.get("kind", "equity")
            horizon = pos.get("horizon_days") or (pos.get("expiry_days") if kind == "option" else 30)
            horizon = int(horizon)
            expiry = (datetime.now(timezone.utc) + timedelta(days=horizon)).strftime("%Y-%m-%d")
            entry = pos.get("entry")
            if kind == "option":
                entry = pos.get("underlying_spot") or pos.get("entry")
            forecasts.append({
                "id": f"{today}:{mid}:{ticker}:{side}",
                "model": mid, "name": name, "date_opened": today,
                "ticker": ticker, "side": side, "kind": kind,
                "edge_type": pos.get("edge_type") or "",
                "probability": p,
                "entry": entry,
                "stop": pos.get("stop"), "target": pos.get("target"),
                "stop_pct": pos.get("stop_pct"), "target_pct": pos.get("target_pct"),
                "horizon_days": horizon, "expiry_date": expiry,
                "thesis": (pos.get("thesis") or "")[:180],
                "invalidation": (pos.get("invalidation") or "")[:200],
                "status": "OPEN", "outcome": None,
                "resolved_date": None, "resolved_price": None, "last_price": entry,
            })
            created += 1

    # 3. Recompute per-model calibration summary.
    models = {}
    for mid in ledger.get("models", {}).keys():
        mname = ledger["models"][mid].get("name", mid)
        resolved = [f for f in forecasts if f["model"] == mid and f["outcome"] is not None]
        n = len(resolved)
        summary = {"name": mname, "n_resolved": n, "n_open": 0,
                   "brier": None, "accuracy": None, "mean_probability": None,
                   "overconfidence_gap": None, "brier_skill": None}
        if n:
            brier = sum((f["probability"] - f["outcome"]) ** 2 for f in resolved) / n
            accuracy = sum(f["outcome"] for f in resolved) / n
            mean_p = sum(f["probability"] for f in resolved) / n
            brier_base = accuracy * (1 - accuracy)  # base-rate-only forecaster
            bss = 1 - brier / brier_base if brier_base > 0 else 0.0
            summary.update(brier=round(brier, 4), accuracy=round(accuracy, 4),
                           mean_probability=round(mean_p, 4),
                           overconfidence_gap=round(mean_p - accuracy, 4),
                           brier_skill=round(bss, 4))
        models[mid] = summary

    for f in forecasts:
        if f["status"] == "OPEN":
            models.setdefault(f["model"], {})["n_open"] = models.get(f["model"], {}).get("n_open", 0) + 1

    calib["as_of"] = datetime.now(timezone.utc).isoformat()
    calib["forecasts"] = forecasts
    calib["models"] = models

    os.makedirs(os.path.dirname(calib_path), exist_ok=True)
    with open(calib_path, "w") as f:
        json.dump(calib, f, indent=2)

    resolved = [f for f in forecasts if f["outcome"] is not None]
    resolved_today = [f for f in forecasts if f.get("resolved_date") == today]
    print(f"Calibration: {len(forecasts)} total forecasts — {created} opened today, "
          f"{len(resolved_today)} resolved today, {len(resolved)} resolved overall")
    for mid, s in sorted(models.items(), key=lambda kv: -(kv[1].get("n_resolved") or 0)):
        if s["n_resolved"]:
            print(f"  {s['name']:10s} n={s['n_resolved']:>3}  Brier={s['brier']:.3f}  "
                  f"acc={s['accuracy']:.2f}  stated={s['mean_probability']:.2f}  "
                  f"gap={s['overconfidence_gap']:+.2f}  BSS={s['brier_skill']:+.2f}")
    print(f"Saved → {calib_path}")


if __name__ == "__main__":
    main()
