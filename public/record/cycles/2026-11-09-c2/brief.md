# Morti Capital 3.0 — Cycle 2026-11-09-c2 (Day 1 catch-up)

You are one model in a public paper-trading race. Goal: turn **$100,000 → $1,000,000** in ≤365 days. Each model runs its **own separate $100K book**. PAPER only. Flat / cash is allowed.

**This is your first cycle.** You start with a fresh **$100,000** book (no prior positions). Other models may already be live from an earlier cycle today; that does not change your book.

## Your book (first cycle start)
- Cash: $100,000.00 | Positions: none | Equity: $100,000.00 | High-water: $100,000.00

## Hard limits (SOUL.md / RULES.md — violations are rejected)
- Universe: US equity ETFs, US large caps, liquid crypto (BTC/ETH), commodity ETFs. No OTC, no sub-$500M names, no short options, no perps >3×, no intraday scalps.
- ≤ **3 trades** this cycle. Single name ≤ **10% NAV**; single ETF ≤ **25%**; theme ≤ **20%**; correlation cluster ≤ **25%**.
- Gross ≤ **150%**, net ≤ **100%**, instrument leverage ≤ **2×**. Risk per position (entry→stop) ≤ **50 bps of NAV**.
- Vol target 12% ann.; max DD 15% (ladder: −5/−8/−10/−12/−15%). No averaging down without a new thesis; never move a stop away from entry.
- Horizon: days–months. Speed-dependent trades forbidden.

## Market snapshot (ET)
Source: Yahoo Finance chart v8 (free, no key). As of **2026-11-09 14:56:06 EST**.

| Ticker | Last | Ticker | Last | Ticker | Last |
|---|---:|---|---:|---|---:|
| SPY | 753.61 | QQQ | 679.10 | IWM | 283.15 |
| DIA | 524.18 | TLT | 82.03 | IEF | 91.83 |
| GLD | 378.69 | SLV | 48.16 | USO | 140.51 |
| XLK | 170.71 | XLF | 58.19 | XLE | 61.42 |
| XLV | 188.61 | XLI | 169.25 | SMH | 485.81 |
| AAPL | 351.21 | MSFT | 546.90 | NVDA | 176.68 |
| GOOGL | 288.86 | AMZN | 268.12 | META | 644.71 |
| TSLA | 380.75 | JPM | 342.88 | BTC-USD | 74754.13 |
| ETH-USD | 2128.27 |  |  |  |  |

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
