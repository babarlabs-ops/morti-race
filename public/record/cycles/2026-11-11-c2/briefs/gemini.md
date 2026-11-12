# Morti Capital 3.0 — Cycle 2026-11-11-c2

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
Source: Yahoo Finance chart v8 (query1.finance.yahoo.com) (free, no key). As of **2026-11-11 12:30:28 EST**. Fills use these prices.

| Ticker | Last | Ticker | Last | Ticker | Last |
|---|---:|---|---:|---|---:|
| SPY | 760.69 | QQQ | 694.05 | IWM | 283.35 |
| DIA | 523.05 | TLT | 80.855 | IEF | 90.915 |
| GLD | 366.84 | SLV | 47.071 | USO | 142.28 |
| XLK | 176.07 | XLF | 58.355 | XLE | 62.915 |
| XLV | 187.55 | XLI | 171.109 | SMH | 514.95 |
| AAPL | 354.235 | MSFT | 521.12 | NVDA | 176.295 |
| GOOGL | 293.36 | AMZN | 266.77 | META | 642.06 |
| TSLA | 393.255 | JPM | 343.21 | BTC-USD | 74406.4 |
| ETH-USD | 2090.87 |  |  |  |  |

## Your book (Gemini) — marked at this snapshot
- Equity **$99,716.69** (-0.283% vs $100,000 start) | Cash $94,020.49 | Gross 26.3% | Net +5.7% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QQQ | short | 14.7571 | 677.64 | 694.05 | -242.13 | -2.36% | 10.27% | 701.00 | 620.00 |
| GLD | long | 21.7556 | 367.25 | 366.84 | -8.92 | -0.11% | 8.00% | 358.00 | 390.00 |
| XLE | long | 126.48 | 63.17 | 62.91 | -32.25 | -0.40% | 7.98% | 61.20 | 68.50 |

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
