# Morti Capital 3.0 — Cycle 2026-11-11-c1

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
Source: Yahoo Finance chart v8 (query1.finance.yahoo.com) (free, no key). As of **2026-11-11 10:25:43 EST**. Fills use these prices.

| Ticker | Last | Ticker | Last | Ticker | Last |
|---|---:|---|---:|---|---:|
| SPY | 755.98 | QQQ | 686.32 | IWM | 281.86 |
| DIA | 520.32 | TLT | 80.5 | IEF | 90.775 |
| GLD | 367.25 | SLV | 47.135 | USO | 144.89 |
| XLK | 173.475 | XLF | 58.2 | XLE | 63.17 |
| XLV | 187.5 | XLI | 170 | SMH | 502.5 |
| AAPL | 353.385 | MSFT | 520.67 | NVDA | 173.28 |
| GOOGL | 290.6 | AMZN | 267.23 | META | 636.905 |
| TSLA | 394.08 | JPM | 341.809 | BTC-USD | 73424 |
| ETH-USD | 2051.37 |  |  |  |  |

## Your book (Claude) — marked at this snapshot
- Equity **$99,895.56** (-0.104% vs $100,000 start) | Cash $72,000.00 | Gross 27.9% | Net +27.9% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | long | 13.2401 | 755.28 | 755.98 | +9.27 | +0.09% | 10.02% | 718.00 | 830.00 |
| SMH | long | 16.3552 | 489.14 | 502.50 | +218.51 | +2.73% | 8.23% | 460.00 | 560.00 |
| GLD | long | 26.3248 | 379.87 | 367.25 | -332.22 | -3.32% | 9.68% | 362.00 | 420.00 |

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
