#!/usr/bin/env python3
"""X (Twitter) search via xAI Agent Tools API — Responses API + `x_search` tool.

This is the corrected wiring: xAI deprecated the old chat-completions
`live_search`/`web_search` tools (HTTP 410). Search now goes through the
OpenAI-style Responses API at POST /v1/responses with tools=[{"type":"x_search"}].

Usage (import):
    from x_search import x_search
    text, citations = x_search("What are people saying about NVDA on X?")

Usage (CLI):
    python3 scripts/x_search.py "NVDA stock" [--from 2026-08-19] [--to 2026-08-20]
"""
import json, os, sys, time, urllib.request, urllib.error

BASE = "https://api.x.ai/v1/responses"
MODEL = "grok-4.6"  # the same model the race runs
RETRIES = 4
RETRY_CODES = (403, 429, 500, 502, 503, 529)


def _load_key():
    k = os.environ.get("XAI_API_KEY")
    if k:
        return k
    # fall back to the morti profile .env
    env_path = os.path.expanduser("~/.hermes/profiles/morti/.env")
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("XAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    raise RuntimeError("XAI_API_KEY not found in env or ~/.hermes/profiles/morti/.env")


def x_search(query, max_output_tokens=900, from_date=None, to_date=None,
             allowed_x_handles=None, excluded_x_handles=None):
    """Run an X search and return (text, citations, raw_response)."""
    key = _load_key()
    tool = {"type": "x_search"}
    if from_date:
        tool["from_date"] = from_date
    if to_date:
        tool["to_date"] = to_date
    if allowed_x_handles:
        tool["allowed_x_handles"] = allowed_x_handles
    if excluded_x_handles:
        tool["excluded_x_handles"] = excluded_x_handles

    payload = {
        "model": MODEL,
        "input": [{"role": "user", "content": query}],
        "tools": [tool],
        "max_output_tokens": max_output_tokens,
    }
    req = urllib.request.Request(BASE, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})

    last_err = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode())
            break
        except urllib.error.HTTPError as e:
            last_err = e
            body = ""
            try:
                body = e.read().decode()
            except Exception:
                pass
            if e.code in RETRY_CODES and attempt < RETRIES - 1:
                wait = 5 * (2 ** attempt)  # 5, 10, 20s
                sys.stderr.write(f"x_search HTTP {e.code}, retry in {wait}s ({attempt+1}/{RETRIES}) — {body[:120]}\n")
                time.sleep(wait)
                continue
            raise RuntimeError(f"xAI x_search HTTP {e.code}: {body[:300]}") from e
        except urllib.error.URLError as e:
            last_err = e
            if attempt < RETRIES - 1:
                wait = 5 * (2 ** attempt)
                sys.stderr.write(f"x_search URLError {e}, retry in {wait}s\n")
                time.sleep(wait)
                continue
            raise
    else:
        raise RuntimeError(f"xAI x_search failed after {RETRIES} attempts: {last_err}")

    texts, citations = [], []
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for c in item.get("content", []):
            if c.get("type") == "output_text":
                texts.append(c.get("text", ""))
                for ann in c.get("annotations", []):
                    if ann.get("type") in ("url_citation", "web_search_call"):
                        u = ann.get("url")
                        if u:
                            citations.append(u)
    text = "\n".join(t for t in texts if t)
    return text, citations, data


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    q = "What are the most notable posts on X about NVDA stock today? 3 concrete items."
    if args and not args[0].startswith("--"):
        q = args.pop(0)
    frm = to = None
    for a in args:
        if a == "--from" and args.index(a) + 1 < len(args):
            frm = args[args.index(a) + 1]
        if a == "--to" and args.index(a) + 1 < len(args):
            to = args[args.index(a) + 1]
    text, cites, data = x_search(q, from_date=frm, to_date=to)
    print("=== TEXT ===")
    print(text[:2500])
    print("\n=== CITATIONS ===")
    for c in cites[:10]:
        print(" -", c)
    print("\n=== USAGE ===")
    print(json.dumps(data.get("usage", {}), indent=2))
    print("\n=== RAW KEYS ===")
    print(list(data.keys()))
