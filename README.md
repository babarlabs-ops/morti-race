# Morti Race — model-vs-model trading benchmark

**The question:** given the *identical* soul, operating manual, memory, and trading policy — and the same starting capital — which frontier or open model trades best?

**The setup:** each model runs as an isolated Morti agent, starting from `$100,000` paper capital and racing to `$1,000,000` within 365 days. Every recommendation, order, and fill is attributed to its originating model through a write-only ledger. Agents race **blind** — they cannot see each other's theses or the live leaderboard.

## Canonical bundle (`/canonical`)

These five files are byte-identical for every agent at launch:

| File | Purpose |
|---|---|
| `SOUL.md` | Identity — who Morti *is* (engine-agnostic persona) |
| `AGENTS.md` | Operating guide — the daily loop, isolation, submission protocol |
| `MEMORY.md` | Context — starting state; diverges privately per engine |
| `GUARDRAILS.md` | Enforcement — the few machine-enforced rails |
| `TRADING_POLICY.md` | Risk envelope, options, exit discipline |

## Experiment parameters

- Start: **$100,000 / model**
- Target: **$1,000,000**
- Window: **365 days**
- Mode: **paper** (shared Alpaca paper account) → real money only behind a hard gate
- Integrity: blind isolation, append-only attribution ledger, neutral orchestrator
- Assets: equities, ETFs, crypto, and defined-risk options

## Roster (locked at launch)

Ten models via OpenRouter: **Fable** (`anthropic/claude-fable-5`), **Sol** (`openai/gpt-5.6-sol`), **Grok** (`x-ai/grok-4.6`), **Gemini** (`google/gemini-3.7-flash`), **DeepSeek** (`deepseek/deepseek-v4-pro`), **Qwen** (`qwen/qwen3.8-max`), **GLM** (`z-ai/glm-5.3`), **Llama** (`meta-llama/llama-4-maverick`), **Mistral** (`mistralai/mistral-medium-3-5`), **Kimi** (`moonshotai/kimi-k3`).

## Principles

1. **Transparent** — methodology, assumptions, and every thesis/order/stop/result are public.
2. **Fair** — identical inputs; the model is the only variable.
3. **Honest** — paper fills have no slippage; the paper→live gap is disclosed, never hidden.
