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

## Your book (Gemini) — marked at this snapshot
- Equity **$99,698.16** (-0.302% vs $100,000 start) | Cash $73,399.08 | Gross 46.9% | Net +26.4% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QQQ | short | 14.7571 | 677.64 | 692.25 | -215.57 | -2.11% | 10.25% | 701.00 | 620.00 |
| GLD | long | 21.7556 | 367.25 | 365.24 | -43.73 | -0.55% | 7.97% | 358.00 | 390.00 |
| XLE | long | 126.48 | 63.17 | 63.03 | -17.07 | -0.21% | 8.00% | 61.20 | 68.50 |
| IWM | long | 72.7772 | 283.35 | 283.00 | -25.47 | -0.12% | 20.66% | 276.50 | 305.00 |

## Your book (Grok) — marked at this snapshot
- Equity **$99,616.87** (-0.383% vs $100,000 start) | Cash $71,729.61 | Gross 28.0% | Net +28.0% | Realized P&L $-332.22

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| IWM | long | 35.2522 | 283.67 | 283.00 | -23.62 | -0.24% | 10.01% | 278.00 | 300.00 |
| SPY | long | 13.1008 | 760.69 | 760.18 | -6.62 | -0.07% | 10.00% | 745.00 | 810.00 |
| QQQ | long | 11.487 | 694.05 | 692.25 | -20.68 | -0.26% | 7.98% | 670.00 | 740.00 |

Recent closes: STOP GLD @ 367.25 (-332.22)

## Your book (DeepSeek) — marked at this snapshot
- Equity **$99,987.18** (-0.013% vs $100,000 start) | Cash $94,000.00 | Gross 6.0% | Net +6.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XLE | long | 94.9818 | 63.17 | 63.03 | -12.82 | -0.21% | 5.99% | 58.00 | 75.00 |

## Your book (Qwen) — marked at this snapshot
- Equity **$99,923.32** (-0.077% vs $100,000 start) | Cash $65,020.19 | Gross 34.9% | Net +34.9% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QQQ | long | 14.7254 | 679.10 | 692.25 | +193.67 | +1.94% | 10.20% | 680.00 | 720.00 |
| GLD | long | 26.4072 | 378.69 | 365.24 | -355.04 | -3.55% | 9.65% | 360.50 | 400.00 |
| BTC-USD | long | 0.067964 | 73,424.02 | 74,351.52 | +63.04 | +1.26% | 5.06% | 70,000.00 | 85,000.00 |
| XLF | long | 85.7426 | 58.20 | 58.52 | +27.87 | +0.56% | 5.02% | 55.00 | 65.00 |
| IWM | long | 17.6438 | 283.35 | 283.00 | -6.18 | -0.12% | 5.00% | 270.00 | 300.00 |

## Your book (GLM) — marked at this snapshot
- Equity **$99,783.15** (-0.217% vs $100,000 start) | Cash $46,663.06 | Gross 53.2% | Net +53.2% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC-USD | long | 0.093409 | 74,939.58 | 74,351.52 | -54.93 | -0.78% | 6.96% | 70,000.00 | 92,000.00 |
| TLT | long | 122.003 | 81.97 | 80.89 | -131.15 | -1.31% | 9.89% | 79.20 | 88.00 |
| GLD | long | 18.4274 | 379.87 | 365.24 | -269.59 | -3.85% | 6.75% | 362.00 | 420.00 |
| QQQ | long | 20.2859 | 686.32 | 692.25 | +120.30 | +0.86% | 14.07% | 663.00 | 748.00 |
| IWM | long | 35.2825 | 281.86 | 283.00 | +40.22 | +0.40% | 10.01% | 270.00 | 305.00 |
| ETH-USD | long | 2.66631 | 2,051.37 | 2,080.74 | +78.31 | +1.43% | 5.56% | 1,950.00 | 2,560.00 |

## Your book (Mistral) — marked at this snapshot
- Equity **$99,528.30** (-0.472% vs $100,000 start) | Cash $79,572.11 | Gross 20.1% | Net +20.1% | Realized P&L $-531.55

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XLF | long | 170.908 | 58.20 | 58.52 | +55.55 | +0.56% | 10.05% | 57.00 | 63.00 |
| TLT | long | 123.054 | 80.86 | 80.89 | +4.31 | +0.04% | 10.00% | 79.30 | 84.00 |

Recent closes: STOP GLD @ 367.25 (-531.55)

## Your book (Kimi) — marked at this snapshot
- Equity **$99,580.39** (-0.420% vs $100,000 start) | Cash $80,000.00 | Gross 19.7% | Net +19.7% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLD | long | 26.4072 | 378.69 | 365.24 | -355.04 | -3.55% | 9.69% | 362.00 | 410.00 |
| NVDA | long | 28.2998 | 176.68 | 175.35 | -37.64 | -0.75% | 4.98% | 160.00 | 205.00 |
| BTC-USD | long | 0.066886 | 74,754.13 | 74,351.52 | -26.93 | -0.54% | 4.99% | 68,000.00 | 85,000.00 |

## Your book (Llama (Meta AI))
- **First cycle:** fresh $100,000.00 book. Cash $100,000.00 | Positions: none | Equity $100,000.00
- You have nothing to hold/add/trim/exit: send `"actions":[]` and up to 3 new trades (or none).

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
