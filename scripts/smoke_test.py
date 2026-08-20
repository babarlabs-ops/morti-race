import json, urllib.request, urllib.error

ENV = "/Users/minimi/.hermes/profiles/morti/.env"

def load_env(path):
    keys = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys

env = load_env(ENV)

def post_json(url, headers, payload, timeout=40):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:250]
    except Exception as e:
        return "ERR", str(e)

def test_openai_compat(name, key, base, model):
    if not key:
        return f"{name}: NO KEY"
    status, resp = post_json(
        f"{base}/chat/completions",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        {"model": model, "messages": [{"role": "user", "content": "say ok"}], "max_tokens": 5},
    )
    if status == 200:
        return f"{name} ({model}): OK"
    return f"{name} ({model}): FAIL ({status}) {str(resp)[:160]}"

def test_anthropic(key, model):
    if not key:
        return "Anthropic: NO KEY"
    status, resp = post_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
        {"model": model, "max_tokens": 5, "messages": [{"role": "user", "content": "say ok"}]},
    )
    if status == 200:
        return f"Anthropic ({model}): OK"
    return f"Anthropic ({model}): FAIL ({status}) {str(resp)[:160]}"

print("=== MODEL KEY SMOKE TEST ===")
print(test_openai_compat("OpenAI(Sol)", env.get("OPENAI_API_KEY"), "https://api.openai.com/v1", "gpt-5.6-sol"))
print(test_anthropic(env.get("ANTHROPIC_API_KEY"), "claude-fable-5"))
print(test_openai_compat("DeepSeek", env.get("DEEPSEEK_API_KEY"), "https://api.deepseek.com/v1", "deepseek-chat"))
print(test_openai_compat("Kimi", env.get("KIMI_API_KEY"), "https://api.moonshot.ai/v1", "moonshot-v1-8k"))
print(test_openai_compat("OpenRouter(Grok)", env.get("OPENROUTER_API_KEY"), "https://openrouter.ai/api/v1", "x-ai/grok-4.3"))

# OpenRouter catalog: which open/other models are reachable?
ok = env.get("OPENROUTER_API_KEY")
if ok:
    try:
        req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {ok}"})
        with urllib.request.urlopen(req, timeout=40) as r:
            data = json.loads(r.read().decode())
        ids = [m.get("id", "") for m in data.get("data", [])]
        print(f"\n=== OpenRouter catalog: {len(ids)} models ===")
        for t in ["grok", "qwen", "glm", "z-ai", "llama", "meta-llama", "mistral", "gemini", "deepseek", "kimi", "moonshot"]:
            matches = [i for i in ids if t in i.lower()][:4]
            print(f"  {t:12s}: {matches}")
    except Exception as e:
        print("OpenRouter catalog FAIL:", str(e)[:160])
