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

## Your book (ChatGPT) — marked at this snapshot
- Equity **$100,043.52** (+0.044% vs $100,000 start) | Cash $21,989.59 | Gross 78.0% | Net +78.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLD | long | 39.8915 | 376.02 | 365.24 | -430.03 | -2.87% | 14.56% | 364.00 | 413.00 |
| SPY | long | 19.9267 | 752.76 | 760.18 | +147.96 | +0.99% | 15.14% | 750.00 | 815.00 |
| XLE | long | 161.747 | 61.83 | 63.03 | +195.71 | +1.96% | 10.19% | 61.50 | 69.00 |
| GOOGL | long | 27.5105 | 290.60 | 294.00 | +93.54 | +1.17% | 8.08% | 286.00 | 325.00 |
| XLI | long | 41.1484 | 170.00 | 170.78 | +32.30 | +0.46% | 7.02% | 166.00 | 190.00 |
| SMH | long | 13.6057 | 514.95 | 511.19 | -51.09 | -0.73% | 6.95% | 490.00 | 580.00 |
| XLF | long | 137.215 | 58.35 | 58.52 | +23.33 | +0.29% | 8.03% | 56.00 | 65.00 |
| XLV | long | 42.6935 | 187.55 | 188.29 | +31.81 | +0.40% | 8.04% | 182.00 | 205.00 |

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
