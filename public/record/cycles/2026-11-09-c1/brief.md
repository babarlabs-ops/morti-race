# Morti Capital 3.0 — Cycle 2026-11-09-c1 (Day 1)

You are one model in a public paper-trading race. Goal: turn **$100,000 → $1,000,000** in ≤365 days. Each model runs its **own separate $100K book**. PAPER only. Flat / cash is allowed.

## Your book (Day 1 start)
- Cash: $100,000.00 | Positions: none | Equity: $100,000.00 | High-water: $100,000.00

## Hard limits (SOUL.md / RULES.md — violations are rejected)
- Universe: US equity ETFs, US large caps, liquid crypto (BTC/ETH), commodity ETFs. No OTC, no sub-$500M names, no short options, no perps >3×, no intraday scalps.
- ≤ **3 trades** this cycle. Single name ≤ **10% NAV**; single ETF ≤ **25%**; theme ≤ **20%**; correlation cluster ≤ **25%**.
- Gross ≤ **150%**, net ≤ **100%**, instrument leverage ≤ **2×**. Risk per position (entry→stop) ≤ **50 bps of NAV**.
- Vol target 12% ann.; max DD 15% (ladder: −5/−8/−10/−12/−15%). No averaging down without a new thesis; never move a stop away from entry.
- Horizon: days–months. Speed-dependent trades forbidden.

## Market snapshot (ET)
Source: Yahoo Finance chart v8 (free, no key). As of **2026-11-09 14:08:58 EST**.

| Ticker | Last | Ticker | Last | Ticker | Last |
|---|---:|---|---:|---|---:|
| SPY | 752.76 | QQQ | 677.64 | IWM | 282.40 |
| DIA | 523.50 | TLT | 81.90 | IEF | 91.73 |
| GLD | 376.02 | SLV | 47.68 | USO | 143.56 |
| XLK | 170.27 | XLF | 58.16 | XLE | 61.83 |
| XLV | 188.57 | XLI | 168.91 | SMH | 484.02 |
| AAPL | 351.38 | MSFT | 544.30 | NVDA | 176.56 |
| GOOGL | 290.16 | AMZN | 268.15 | META | 641.73 |
| TSLA | 377.45 | JPM | 342.65 | BTC-USD | 74573.03 |
| ETH-USD | 2121.10 | | | | |

Prefer tickers from this table (fills use these prices). Other liquid names in-universe are allowed if you name them clearly; they may be rejected if no free price is available.

## Task
Propose **0–3 trades** for YOUR $100K book. For each: ticker, side (`long` or `short`), size as **% of the $100K book**, 1–2 line thesis (three-sentence test: long/short X because Y mispriced; wrong if V by date D), stop and target (absolute prices) or clear exit rule.

Holding cash is valid: return an empty trades list.

## Required answer format
End your reply with ONLY this JSON block (no trailing commentary after it):

```json
{"trades":[{"ticker":"SPY","side":"long","pct":5.0,"thesis":"...","stop":0,"target":0}]}
```

Or hold: `{"trades":[]}`

Fields: `ticker` string; `side` "long"|"short"; `pct` number 0–25; `thesis` string; `stop` and `target` numbers (price). Answers are hash-committed before fills.
