#!/usr/bin/env python3
"""Morti Race — daily decision cycle.

Each model reviews its current book (positions + P&L), forms a fresh daily
thesis, and decides what to HOLD, SELL, or OPEN — equities, ETFs, crypto, and
defined-risk options (long calls/puts). Robust: per-model timeout, incremental
save, resumable.
"""
import json, os, sys, urllib.request, urllib.error
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = "/Users/minimi/.hermes/profiles/morti/.env"
MODEL_TIMEOUT = 90


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


def call_model(model, system, user, key):
    payload = {"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ], "temperature": 0.4, "max_tokens": 3000}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=MODEL_TIMEOUT) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
    except Exception as e:
        return "ERR", str(e)[:200]


def extract_json(text):
    t = text.strip()
    if t.startswith("```"):
        parts = t.split("```")
        if len(parts) > 1:
            t = parts[1]
        t = t.lstrip("json").strip()
    try:
        return json.loads(t)
    except Exception:
        start, end = t.find("{"), t.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(t[start:end + 1])
            except Exception:
                return None
    return None


def current_book_summary(prev, mid):
    """Render a model's current book as a compact text block."""
    if not prev or mid not in prev.get("models", {}):
        return "No open positions. This is your opening move.\n"
    m = prev["models"][mid]
    lines = [f"Equity: ${m.get('equity', 100000):,.2f}. Realized P&L: ${m.get('realized_pnl', 0):,.2f}."]
    pos = m.get("positions", [])
    if not pos:
        lines.append("(no open positions — flat)")
    else:
        lines.append("Your open positions (marked to market):")
        for p in pos:
            if p.get("kind") == "option":
                kind = "LONG CALL" if p.get("is_call") else "LONG PUT"
                lines.append(f"  - {kind} {p['ticker']}: {p['contracts']} contracts, "
                             f"strike ${p['strike']}, entry premium ${p['premium']:.2f}")
            else:
                side = p["side"].upper()
                pnl = p.get("unrealized_pnl", 0)
                lines.append(f"  - {side} {p['ticker']}: ${p.get('dollar', 0):,.0f} "
                             f"(entry ${p['entry']:.2f}, last ${p['last']:.2f}, P&L {pnl:+,.2f})")
    return "\n".join(lines) + "\n"


def main():
    env = load_env(ENV_PATH)
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print("FATAL: OPENROUTER_API_KEY not set")
        sys.exit(1)
    cfg = json.loads(read(os.path.join(ROOT, "config", "models.json")))
    doctrine_files = ["SOUL.md", "AGENT.md", "BENCHMARK.md", "HERMES.md", "MEMORY.md"]
    doctrine = "\n\n".join(
        "===== " + f + " =====" + "\n" + read(os.path.join(ROOT, "canonical", f))
        for f in doctrine_files
    )

    market = ""
    snap = os.path.join(ROOT, "data", "market_snapshot.json")
    if os.path.exists(snap):
        market = "\n\nCURRENT MARKET SNAPSHOT (live data):\n" + read(snap)

    macro = ""
    macropath = os.path.join(ROOT, "data", "macro.json")
    if os.path.exists(macropath):
        try:
            macro = "\n\n" + (json.loads(read(macropath)).get("summary") or "")
        except Exception:
            macro = ""

    prev = None
    ledger_path = os.path.join(ROOT, "data", "ledger.json")
    if os.path.exists(ledger_path):
        try:
            prev = json.loads(read(ledger_path))
        except Exception:
            prev = None

    system = (
        "You are Morti, an autonomous trader. Internalize this doctrine exactly:\n\n"
        + doctrine
    )

    def user_prompt(mid):
        book = current_book_summary(prev, mid)
        contract = (
            "DECISION CONTRACT — every position you open must state, up front:\n"
            "- edge_type: one of informational | analytical | behavioral | structural. "
            "No position without a declared edge (name who is giving you the alpha and why).\n"
            "- probability: your honest estimate (0.05–0.95) that this trade hits its target "
            "before its stop, within horizon_days. Calibration beats conviction: being right "
            "60% while claiming 60% beats being right 75% while claiming 95%.\n"
            "- invalidation: the falsifier, written BEFORE entry — \"we are wrong if X by date D\". "
            "If you cannot write it, you do not understand the trade yet.\n"
            "- horizon_days: how many days you give the thesis to resolve (options: use expiry_days).\n"
            "FLAT IS A POSITION. \"No action\" is a valid and frequently correct cycle output. "
            "Do not invent trades to look productive.\n"
        )
        return (
            "You are racing $100,000 to $1,000,000 in one year. This is today's decision cycle.\n\n"
            "YOUR CURRENT BOOK:\n" + book +
            "\nDecide today's moves: which positions to HOLD, which to SELL, and what NEW "
            "positions to OPEN (long, short, or swing).\n"
            "Rules: ALL assets are fair game — US equities, ETFs, and crypto (BTC, ETH, SOL, "
            "etc.). Defined-risk OPTIONS are allowed where the payoff justifies it (long calls "
            "or long puts only). Up to 10 positions. Allocations are percentages of equity "
            "summing to at most 100 (leave the rest cash if unsure).\n\n"
            + contract +
            "\nFor an equity/crypto position give: ticker, side (long/short), alloc_pct, one-line "
            "thesis, stop_pct (e.g. -8), target_pct (e.g. +25), edge_type, probability, invalidation, horizon_days.\n"
            "For an option give: ticker (underlying), type (long_call/long_put), strike_pct "
            "(percent OUT-OF-THE-MONEY, 1 to 40: e.g. 5 = strike 5% above spot for a call, "
            "5% below spot for a put), expiry_days (e.g. 30), alloc_pct, thesis, edge_type, probability, invalidation, horizon_days.\n"
            + market + macro +
            "\n\nRespond ONLY as JSON: {\"thesis\":\"<one-line macro thesis for today>\","
            "\"justification\":\"<2-4 sentences on your selection logic>\","
            "\"positions\":[{\"ticker\":\"AAPL\",\"side\":\"long\",\"alloc_pct\":15,\"thesis\":\"...\",\"stop_pct\":-8,\"target_pct\":25,\"edge_type\":\"analytical\",\"probability\":0.62,\"invalidation\":\"...\",\"horizon_days\":30} OR "
            "{\"ticker\":\"NVDA\",\"type\":\"long_call\",\"strike_pct\":5,\"expiry_days\":30,\"alloc_pct\":5,\"thesis\":\"...\",\"edge_type\":\"behavioral\",\"probability\":0.55,\"invalidation\":\"...\",\"horizon_days\":30}]}"
        )

    outdir = os.path.join(ROOT, "data", "picks")
    os.makedirs(outdir, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = os.path.join(outdir, day + ".json")

    results = {}
    if os.path.exists(out):
        try:
            results = json.loads(read(out)).get("results", {})
            print(f"Resuming — {len(results)} models already done")
        except Exception:
            results = {}

    def save():
        with open(out, "w") as f:
            json.dump({"generated_utc": datetime.now(timezone.utc).isoformat(), "results": results}, f, indent=2)

    for m in cfg["models"]:
        mid = m["id"]
        if mid in results:
            print(f"✓ skip {m['name']} (done)")
            continue
        print(f"→ {m['name']} ({m['model']})...", flush=True)
        status, resp = call_model(m["model"], system, user_prompt(mid), key)
        if status != 200:
            print(f"  FAIL {status}: {str(resp)[:160]}")
            results[mid] = {"model": m["name"], "tier": m["tier"], "error": str(resp)[:200]}
        else:
            try:
                msg = resp["choices"][0].get("message", {}) or {}
                content = msg.get("content") or ""
                usage = resp.get("usage", {})
                if not content.strip():
                    print(f"  EMPTY content — recording as error")
                    results[mid] = {"model": m["name"], "tier": m["tier"], "error": "empty response content"}
                    save()
                    continue
                picks = extract_json(content)
                n = len(picks.get("positions", [])) if isinstance(picks, dict) else "?"
                print(f"  OK — {n} positions, {usage.get('total_tokens')} tok")
                results[mid] = {"model": m["name"], "tier": m["tier"], "picks": picks, "raw_usage": usage}
            except Exception as e:
                print(f"  PARSE FAIL: {e}")
                results[mid] = {"model": m["name"], "tier": m["tier"], "error": str(e)}
        save()

    print(f"\nDone — {len(results)}/{len(cfg['models'])} models → {out}")


if __name__ == "__main__":
    main()
