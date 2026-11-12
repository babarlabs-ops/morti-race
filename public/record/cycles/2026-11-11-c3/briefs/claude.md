# Morti Capital 3.0 — Cycle 2026-11-11-c3

You hold one seat on a shared paper-trading mission: the team is taking **$100,000 → $1,000,000** in ≤365 days. Each seat runs its **own $100K book**; the team number is the average of the seats. PAPER only. Cash is allowed.

**This cycle you manage your EXISTING book** (shown below, marked at this snapshot) and may add up to 3 new trades.
Before your answer is applied, any position whose price has crossed its stop (or reached its target) at this snapshot is closed automatically.

## Hard limits (checked on your RESULTING book — violations are rejected)
- Universe: US equity ETFs, US large caps, liquid crypto (BTC/ETH), commodity ETFs. No OTC, no sub-$500M names, no options, no intraday scalps.
- ≤ **3 new trades** this cycle. Single name ≤ **10% NAV**; single ETF ≤ **25% NAV**; theme ≤ 20%; correlation cluster ≤ 25%.
- Gross ≤ **150%**, |net| ≤ **100%**. Risk per new trade or add (price→stop) ≤ **50 bps of NAV**.
- Stops may only be tightened, never loosened. Adding to a losing position needs a new thesis.
- Horizon: days–months.

## Market snapshot (ET)
Source: Yahoo Finance chart v8 (query1.finance.yahoo.com) (free, no key). As of **2026-11-11 14:28:20 EST**. Fills use these prices.

| Ticker | Last | Ticker | Last | Ticker | Last |
|---|---:|---|---:|---|---:|
| SPY | 760.185 | QQQ | 692.25 | IWM | 283 |
| DIA | 523.8 | TLT | 80.89 | IEF | 90.929 |
| GLD | 365.24 | SLV | 46.76 | USO | 141.99 |
| XLK | 175.24 | XLF | 58.525 | XLE | 63.035 |
| XLV | 188.295 | XLI | 170.785 | SMH | 511.195 |
| AAPL | 354.96 | MSFT | 520.499 | NVDA | 175.35 |
| GOOGL | 294 | AMZN | 266.55 | META | 634.83 |
| TSLA | 392.595 | JPM | 344.305 | BTC-USD | 74351.5 |
| ETH-USD | 2080.74 |  |  |  |  |

## Your book (Claude) — marked at this snapshot
- Equity **$100,069.92** (+0.070% vs $100,000 start) | Cash $59,002.04 | Gross 41.0% | Net +41.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | long | 13.2401 | 755.28 | 760.18 | +64.94 | +0.65% | 10.06% | 738.00 | 830.00 |
| SMH | long | 16.3552 | 489.14 | 511.19 | +360.71 | +4.51% | 8.35% | 495.00 | 560.00 |
| GLD | long | 26.3248 | 379.87 | 365.24 | -385.13 | -3.85% | 9.61% | 362.00 | 420.00 |
| XLE | long | 79.0688 | 63.17 | 63.03 | -10.67 | -0.21% | 4.98% | 59.50 | 71.00 |
| BTC-USD | long | 0.054421 | 73,424.02 | 74,351.52 | +50.48 | +1.26% | 4.04% | 68,500.00 | 90,000.00 |
| QQQ | long | 5.77388 | 694.05 | 692.25 | -10.39 | -0.26% | 3.99% | 660.00 | 760.00 |

## Task
1. For **each position you hold**, choose one action: `hold` (optionally tighten stop / change target), `add` (extra % of NAV), `trim` (% of NAV to sell or cover), or `exit`.
2. Optionally propose **0–3 new trades**: ticker, side (`long`/`short`), size as **% of your current NAV**, 1–2 line thesis (long/short X because Y; wrong if V by date D), stop and target (absolute prices).
Positions you leave out are held unchanged. Doing nothing is valid.

## Required answer format
End your reply with ONLY this JSON block (no commentary after it):

```json
{"actions":[{"ticker":"GLD","action":"hold","stop":0,"target":0},{"ticker":"SPY","action":"trim","pct":5.0,"thesis":"..."}],
 "trades":[{"ticker":"XLE","side":"long","pct":5.0,"thesis":"...","stop":0,"target":0}]}
```

`action` is "hold" | "add" | "trim" | "exit". `pct` = % of current NAV (needed for add/trim). `stop`/`target` 0 = unchanged. Hold everything with no new trades: `{"actions":[],"trades":[]}`. Answers are hash-committed before fills.
