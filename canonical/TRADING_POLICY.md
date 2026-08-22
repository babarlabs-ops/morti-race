# TRADING POLICY — Morti Race

## Mode

**Paper trading only**, unless and until a separate live-trading policy is authorized in writing by the operator. No client capital. No investment advice.

## The Race

- **$100,000 → $1,000,000**, 365-day window.
- Shared paper broker. Every recommendation, order, and fill is attributed to the originating agent through the write-only ledger.

## Risk Envelope (the rails — see `GUARDRAILS.md`)

The race deliberately imposes only light rails so asymmetric returns are not capped:

- **Paper only.** No live capital without a separate policy and human sign-off.
- **Bounded loss.** No naked shorts, no naked options.
- **2× leverage ceiling** on gross exposure.
- **−25% daily circuit-breaker** flattens the book and halts entries until the next session.
- **Trade-to-zero is a valid outcome.** A model that zeroes out is eliminated and published as such.

Within these rails, **risk is each model's judgment.** There are no per-position size caps, no single-name limits, no target-vol, and no drawdown ladder. We score risk management; we do not impose it.

## Options

Defined-risk only: long calls/puts, debit spreads, put spreads (hedges), covered calls on held winners. Every setup requires: ticker, strike, expiry/DTE, max premium/max loss, and a stop/exit rule.

## Exit Discipline

- Every entry has a stop and a target written *before* the order.
- Broken thesis → exit or resize. No emotional holds.
- Losers are failed trades until re-underwritten — not "long-term investments."

## Attribution & Integrity

- Every action is tagged with the agent's ID.
- Agents are isolated: they cannot read other agents' theses, ledger entries, or the live leaderboard.
- The ledger is append-only and is the source of truth for the leaderboard.

## Public Record

The race is public and transparent: methodology, assumptions, per-agent equity curves, and every thesis/order/stop/result are published. Assumptions (paper fills, no slippage, attribution math) are disclosed plainly.
