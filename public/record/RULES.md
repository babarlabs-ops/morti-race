# RULES.md: hard limits for the 3.0 mission

Copied from SOUL.md §1 and §4 without changes; that file is the source of record. HERMES enforces these by machine before any order is built.

## Universe
- **Allowed:** US equity ETFs, US large caps, liquid crypto, commodity ETFs.
- **Excluded:** OTC, companies under $500M market cap, short option premium, perpetuals above 3×, illiquid alternatives.
- **Horizon:** days to months. No intraday trading.

## Sizing
- Fractional Kelly, capped at ¼-Kelly.
- Risk per position (entry to stop) is at most **50 bps of NAV**.
- A single name is at most **10% of NAV**, a single ETF at most **25%**, and a single theme at most **20%**.
- A correlation cluster is at most **25% of NAV**. Positions with ρ > 0.7 count as one position.
- Gross exposure is at most **150%**, net at most **100%**, and instrument leverage at most **2×**.
- A position is at most **1% of 20-day ADV** (crypto: 0.5%).
- Volatility target is **12% annualized**. Maximum drawdown tolerance is **15%**.

## Prohibited
- Naked short options, or anything with unbounded loss.
- Adding to a loser that has breached its invalidation, or averaging down without a new thesis.
- Moving a stop away from entry.
- Speed-dependent trades.
- Material non-public information.
- Content whose provenance is unverified.

## Drawdown ladder (from high-water mark)
| Drawdown | Action |
|---|---|
| −5% | Risk budget × 0.5 |
| −8% | Close the 2 lowest-conviction positions; no new themes |
| −10% | Risk budget × 0.25; written post-mortem |
| −12% | Halve all positions; cash floor of 50% |
| −15% | Flat. Full halt until a human signs off. |

## Kill switches
Any one of these freezes trading immediately:
- Prices more than 15 minutes stale.
- Sources disagreeing by more than 1%.
- Spread more than 3× its median.
- The ledger fails to reconcile.
- An unlogged trade.
- The constitution was altered without a human signature.

## Integrity
- The journal is append-only.
- Theses are hash-committed before outcomes are known.
- Losses are published with the same prominence as gains.
- Every performance number carries `n / MinTRL` (from BENCHMARK.md).
