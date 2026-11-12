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

## Your book (ChatGPT) — marked at this snapshot
- Equity **$99,931.87** (-0.068% vs $100,000 start) | Cash $60,000.00 | Gross 40.0% | Net +40.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLD | long | 39.8915 | 376.02 | 367.25 | -349.85 | -2.33% | 14.66% | 364.00 | 413.00 |
| SPY | long | 19.9267 | 752.76 | 755.98 | +64.16 | +0.43% | 15.07% | 730.00 | 815.00 |
| XLE | long | 161.747 | 61.83 | 63.17 | +217.55 | +2.18% | 10.22% | 59.00 | 69.00 |

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
