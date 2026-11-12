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

## Your book (ChatGPT) — marked at this snapshot
- Equity **$100,089.68** (+0.090% vs $100,000 start) | Cash $45,010.22 | Gross 55.0% | Net +55.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLD | long | 39.8915 | 376.02 | 366.84 | -366.20 | -2.44% | 14.62% | 364.00 | 413.00 |
| SPY | long | 19.9267 | 752.76 | 760.69 | +158.02 | +1.05% | 15.14% | 742.00 | 815.00 |
| XLE | long | 161.747 | 61.83 | 62.91 | +176.30 | +1.76% | 10.17% | 61.00 | 69.00 |
| GOOGL | long | 27.5105 | 290.60 | 293.36 | +75.93 | +0.95% | 8.06% | 282.00 | 325.00 |
| XLI | long | 41.1484 | 170.00 | 171.11 | +45.63 | +0.65% | 7.03% | 164.00 | 190.00 |

## Your book (Claude) — marked at this snapshot
- Equity **$100,184.03** (+0.184% vs $100,000 start) | Cash $63,009.40 | Gross 37.1% | Net +37.1% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | long | 13.2401 | 755.28 | 760.69 | +71.63 | +0.72% | 10.05% | 718.00 | 830.00 |
| SMH | long | 16.3552 | 489.14 | 514.95 | +422.13 | +5.28% | 8.41% | 478.00 | 560.00 |
| GLD | long | 26.3248 | 379.87 | 366.84 | -343.01 | -3.43% | 9.64% | 362.00 | 420.00 |
| XLE | long | 79.0688 | 63.17 | 62.91 | -20.16 | -0.40% | 4.97% | 59.50 | 71.00 |
| BTC-USD | long | 0.054421 | 73,424.02 | 74,406.41 | +53.46 | +1.34% | 4.04% | 66,000.00 | 90,000.00 |

## Your book (Gemini) — marked at this snapshot
- Equity **$99,716.69** (-0.283% vs $100,000 start) | Cash $94,020.49 | Gross 26.3% | Net +5.7% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QQQ | short | 14.7571 | 677.64 | 694.05 | -242.13 | -2.36% | 10.27% | 701.00 | 620.00 |
| GLD | long | 21.7556 | 367.25 | 366.84 | -8.92 | -0.11% | 8.00% | 358.00 | 390.00 |
| XLE | long | 126.48 | 63.17 | 62.91 | -32.25 | -0.40% | 7.98% | 61.20 | 68.50 |

## Your book (Grok) — marked at this snapshot
- Equity **$99,656.50** (-0.344% vs $100,000 start) | Cash $89,667.78 | Gross 10.0% | Net +10.0% | Realized P&L $-332.22

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| IWM | long | 35.2522 | 283.67 | 283.35 | -11.28 | -0.11% | 10.02% | 275.00 | 300.00 |

Recent closes: STOP GLD @ 367.25 (-332.22)

## Your book (DeepSeek) — marked at this snapshot
- Equity **$99,975.78** (-0.024% vs $100,000 start) | Cash $94,000.00 | Gross 6.0% | Net +6.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XLE | long | 94.9818 | 63.17 | 62.91 | -24.22 | -0.40% | 5.98% | 58.00 | 75.00 |

## Your book (Qwen) — marked at this snapshot
- Equity **$99,987.41** (-0.013% vs $100,000 start) | Cash $70,019.56 | Gross 30.0% | Net +30.0% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| QQQ | long | 14.7254 | 679.10 | 694.05 | +220.17 | +2.20% | 10.22% | 665.00 | 720.00 |
| GLD | long | 26.4072 | 378.69 | 366.84 | -312.79 | -3.13% | 9.69% | 360.50 | 400.00 |
| BTC-USD | long | 0.067964 | 73,424.02 | 74,406.41 | +66.77 | +1.34% | 5.06% | 70,000.00 | 85,000.00 |
| XLF | long | 85.7426 | 58.20 | 58.35 | +13.29 | +0.27% | 5.00% | 55.00 | 65.00 |

## Your book (GLM) — marked at this snapshot
- Equity **$99,889.36** (-0.111% vs $100,000 start) | Cash $46,663.06 | Gross 53.3% | Net +53.3% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC-USD | long | 0.093409 | 74,939.58 | 74,406.41 | -49.80 | -0.71% | 6.96% | 70,000.00 | 92,000.00 |
| TLT | long | 122.003 | 81.97 | 80.86 | -135.42 | -1.35% | 9.88% | 79.20 | 88.00 |
| GLD | long | 18.4274 | 379.87 | 366.84 | -240.11 | -3.43% | 6.77% | 362.00 | 420.00 |
| QQQ | long | 20.2859 | 686.32 | 694.05 | +156.81 | +1.13% | 14.10% | 663.00 | 748.00 |
| IWM | long | 35.2825 | 281.86 | 283.35 | +52.57 | +0.53% | 10.01% | 270.00 | 305.00 |
| ETH-USD | long | 2.66631 | 2,051.37 | 2,090.87 | +105.32 | +1.93% | 5.58% | 1,878.00 | 2,560.00 |

## Your book (Mistral) — marked at this snapshot
- Equity **$99,494.94** (-0.505% vs $100,000 start) | Cash $89,521.60 | Gross 10.0% | Net +10.0% | Realized P&L $-531.55

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| XLF | long | 170.908 | 58.20 | 58.35 | +26.49 | +0.27% | 10.02% | 55.30 | 63.00 |

Recent closes: STOP GLD @ 367.25 (-531.55)

## Your book (Kimi) — marked at this snapshot
- Equity **$99,653.06** (-0.347% vs $100,000 start) | Cash $80,000.00 | Gross 19.7% | Net +19.7% | Realized P&L $0.00

| Ticker | Side | Qty | Entry | Now | Unrealized P&L | P&L % | Weight % NAV | Stop | Target |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GLD | long | 26.4072 | 378.69 | 366.84 | -312.79 | -3.13% | 9.72% | 362.00 | 410.00 |
| NVDA | long | 28.2998 | 176.68 | 176.29 | -10.90 | -0.22% | 5.01% | 160.00 | 205.00 |
| BTC-USD | long | 0.066886 | 74,754.13 | 74,406.41 | -23.26 | -0.47% | 4.99% | 68,000.00 | 85,000.00 |

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
