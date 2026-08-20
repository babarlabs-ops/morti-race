#!/usr/bin/env python3
"""Morti Race — fire the opening picks for all 10 models via OpenRouter.

Robust: per-model timeout, incremental save (survives interruption), resumable.
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
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
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


def main():
    env = load_env(ENV_PATH)
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        print("FATAL: OPENROUTER_API_KEY not set")
        sys.exit(1)
    cfg = json.loads(read(os.path.join(ROOT, "config", "models.json")))
    soul = read(os.path.join(ROOT, "canonical", "SOUL.md"))
    guardrails = read(os.path.join(ROOT, "canonical", "GUARDRAILS.md"))

    market = ""
    snap = os.path.join(ROOT, "data", "market_snapshot.json")
    if os.path.exists(snap):
        market = "\n\nCURRENT MARKET SNAPSHOT (live data):\n" + read(snap)

    system = (
        "You are Morti, an autonomous trader. Internalize this identity exactly:\n\n"
        + soul + "\n\nGUARDRAILS (machine-enforced limits):\n" + guardrails
    )
    user_tpl = (
        "You hold $100,000 paper capital and are racing to $1,000,000 within one year. "
        "This is your OPENING move. Allocate your portfolio now.\n"
        "Rules: US equities/ETFs only. Up to 10 positions. Allocations are percentages "
        "summing to at most 100 (leave the rest cash if unsure). Long OR short.\n"
        "For each position give: ticker, side (long/short), alloc_pct, one-line thesis, "
        "stop_pct (e.g. -8), target_pct (e.g. +25).\n"
        + market +
        "\n\nRespond ONLY as JSON: {\"positions\":[{\"ticker\":\"AAPL\",\"side\":\"long\",\"alloc_pct\":15,\"thesis\":\"...\",\"stop_pct\":-8,\"target_pct\":25}]}"
    )

    outdir = os.path.join(ROOT, "data", "picks")
    os.makedirs(outdir, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = os.path.join(outdir, day + ".json")

    # resume: load any prior partial results
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
        status, resp = call_model(m["model"], system, user_tpl, key)
        if status != 200:
            print(f"  FAIL {status}: {str(resp)[:160]}")
            results[mid] = {"model": m["name"], "tier": m["tier"], "error": str(resp)[:200]}
        else:
            try:
                content = resp["choices"][0]["message"]["content"]
                usage = resp.get("usage", {})
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
