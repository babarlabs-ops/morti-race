# Morti Race — model-vs-model trading benchmark

**The question:** given the *identical* soul, operating manual, memory, and trading policy — and the same starting capital — which frontier or open model trades best?

**The setup:** each model runs as an isolated Morti agent, starting from `$5,000` paper capital and racing to `$50,000` within one year. Every recommendation, order, and fill is attributed to its originating model through a write-only ledger. Agents race **blind** — they cannot see each other's theses or the live leaderboard.

## Canonical bundle (`/canonical`)

These four files are byte-identical for every agent at launch:

| File | Purpose |
|---|---|
| `SOUL.md` | Identity — who Morti *is* (engine-agnostic persona) |
| `AGENTS.md` | Operating guide — the daily loop, isolation, submission protocol |
| `MEMORY.md` | Context — starting state; diverges privately per engine |
| `TRADING_POLICY.md` | Hard rules — risk limits, options, exit discipline |

## Experiment parameters

- Start: **$5,000 / model**
- Target: **$50,000**
- Window: **1 year**
- Mode: **paper** (shared Alpaca paper account) → real money only behind a hard gate
- Integrity: blind isolation, append-only attribution ledger, neutral orchestrator

## Roster (locked at launch)

Frontier + open models. Exact provider/model strings are configured in the harness (pending operator confirmation of the Fable mapping).

## Principles

1. **Transparent** — methodology, assumptions, and every thesis/order/stop/result are public.
2. **Fair** — identical inputs; the model is the only variable.
3. **Honest** — paper fills have no slippage; the paper→live gap is disclosed, never hidden.

## Build status

- [ ] Canonical bundle (this draft)
- [ ] Attribution ledger + write-only API
- [ ] Per-model isolated profiles (harness)
- [ ] Leaderboard + public site (transparent + exciting)
- [ ] Real-money hard gate
