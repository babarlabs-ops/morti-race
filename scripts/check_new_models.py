#!/usr/bin/env python3
"""Check OpenRouter for newly-released models across the Morti Race families.

Uses each model's `created` timestamp (recency) rather than version parsing,
and a state file so each new model is alerted exactly once. Empty stdout =
silent (cron no_agent delivers nothing). Exit 1 on fetch error.
"""
import json, os, re, sys, time, urllib.request

REPO = "/Users/minimi/Claude Working files/morti-race"
STATE = os.path.join(REPO, "data", "model_watch_seen.json")
RECENT_DAYS = 21

FAMILIES = [
    "anthropic/claude", "openai/gpt", "x-ai/grok", "google/gemini", "deepseek/",
    "qwen/", "z-ai/glm", "meta-llama/llama", "mistralai/", "moonshotai/kimi",
]

# substrings that mark a variant, not a major release (kept light so a real
# tier like "flash" or "pro" is NOT filtered)
VARIANT_KW = ("thinking", "reasoning", "reasoner", "multi-agent", "vision",
              "instruct", "turbo", "free", "beta", "preview", "nitro",
              "online", "extended", "search", "browser", "nano", "exp")


def is_variant(mid):
    if ":" in mid:
        return True
    low = mid.lower()
    if any(k in low for k in VARIANT_KW):
        return True
    # dated suffix: -0813, -2407
    if re.search(r"-\d{4,}", low):
        return True
    # size suffix: -27b, -2.4t
    if re.search(r"-\d+(?:\.\d+)?[bt]", low):
        return True
    return False


def load_seen():
    try:
        return set(json.load(open(STATE)).get("seen", []))
    except Exception:
        return set()


def save_seen(seen):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump({"seen": sorted(seen)}, f, indent=2)


def main():
    cfg = json.load(open(os.path.join(REPO, "config", "models.json")))
    current_ids = {m["model"] for m in cfg["models"]}

    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/models",
                                     headers={"User-Agent": "morti-race"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())["data"]
    except Exception as e:
        print("⚠️ check_new_models: fetch failed:", str(e)[:120])
        sys.exit(1)

    now = time.time()
    seen = load_seen()
    fresh = []
    for m in data:
        mid = m["id"]
        if not any(mid.startswith(f) for f in FAMILIES):
            continue
        if mid in current_ids:
            continue
        if is_variant(mid):
            continue
        c = m.get("created", 0)
        if not c:
            continue
        age = (now - c) / 86400
        if age <= RECENT_DAYS:
            fresh.append((mid, round(age, 1)))

    new = [(mid, age) for mid, age in fresh if mid not in seen]
    if new:
        lines = ["🔔 New model release(s) detected on OpenRouter:"]
        for mid, age in sorted(new, key=lambda x: x[1]):
            lines.append(f"   • {mid}  ({age}d old)")
        print("\n".join(lines))
        seen.update(mid for mid, _ in new)
        save_seen(seen)


if __name__ == "__main__":
    main()
