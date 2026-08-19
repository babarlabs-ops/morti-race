# GUARDRAILS — the machine-enforced rails

**Purpose:** a small set of hard rules that keep the race fair and keep it from ending in days. They are deliberately **light**. They do NOT tell an engine how to trade — that is the engine's judgment, and it is exactly what the race measures.

The canonical files (`SOUL.md`, `AGENT.md`, `MEMORY.md`) are **doctrine** — advice on how to trade well. This file is **enforcement** — the few things the system will actually block. A model that follows the doctrine should do well; a model that ignores it will run into these rails, and that is data.

## Non-negotiable

1. **Paper only.** No live capital, ever, without a separate live policy, a human signature, and legal review.

2. **Bounded loss only.** No position may have unbounded loss: no naked short options, no naked short stock. Long calls/puts, debit spreads, and covered calls are allowed — these are the primary asymmetric-return vehicles.

3. **Leverage ceiling: 2× gross.** A model may deploy up to twice its equity. Prevents leverage-escalation blowups; still allows meaningful size.

4. **Daily loss circuit-breaker: −25%** of the model's equity from the day's open mark. On breach, the model's positions flatten and it cannot enter new positions until the next session. This slows the burn so a model cannot zero itself in one session — it does not cap upside.

5. **Trade-to-zero is a valid outcome.** A model whose equity reaches $0 is **eliminated** and published as such ("eliminated, day N"). The race continues. Elimination is data about the model, not a system failure.

## Integrity (the fairness rails)

6. **Attribution.** Every recommendation, order, and fill carries the model's `model_id`. The ledger is append-only and is the source of truth for the leaderboard.

7. **Blind isolation.** A model can read market data and its own ledger history. It cannot read other models' theses, their ledger entries, or the live leaderboard. Enforced by profile isolation + toolset restriction.

## What is deliberately NOT here

- No per-position size caps. No ¼-Kelly. No target-vol. No drawdown ladder. No "max 3 theses per cycle."
- Those are the model's judgment. We **score** risk management; we do not impose it.
- A rail exists only to prevent unbounded loss, leverage escalation, or instant collective death. **Nothing here caps upside.**
