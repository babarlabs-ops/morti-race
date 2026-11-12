This is a paper-trading task, so I’m treating it as a risk-management exercise rather than advice. Nothing here is financial advice.

Book review (NAV ≈ $100,070, 41% gross, 59% cash)

SPY (10.06%): At the 10% single-name cap and the 25% ETF cap I’m fine, but there’s little reason to add. Stop at 738 is ~2.9% away. I’ll hold and tighten the stop to 745, which locks in a small gain over entry (755.28 is above it, so it’s still a loss if hit, but it caps downside).
SMH (8.35%): Best performer at +4.5%, and the stop at 495 sits only ~3.2% below the market. I’ll tighten to 500 to protect most of the gain. Semis are volatile, so I won’t add.
GLD (9.61%): Down 3.85%, only ~0.9% above its 362 stop. It’s a losing position with no new thesis to add, and I won’t loosen the stop. Hold and let the stop do its job.
XLE (4.98%): Flat, small, stop well below. Hold.
BTC (4.04%): Modest gain, wide stop at 68,500 (~7.9% away). Hold, and tighten the stop to 70,000 to lock in more of the cushion.
QQQ (3.99%): Flat. Hold. Overlaps with SMH and SPY on mega-cap tech beta, so I won’t add.

New trades

With 59% in cash and a book that is entirely long equity beta plus gold, the main gap is diversification, not more of the same risk. I want modest additions with per-trade risk under 50 bps of NAV.

XLV long, 5% NAV: Defensive healthcare sleeve with low correlation to the semis/QQQ tilt. At 188.30 with a stop at 180 (4.4% risk), that is ~22 bps of NAV, well under the cap. Target 205.
IEF long, 5% NAV: Intermediate Treasuries as a hedge against an equity drawdown. At 90.93 with a stop at 88.5 (2.7% risk, ~13 bps). Target 96.
XLI long, 4% NAV: Industrials adds cyclical breadth outside tech. At 170.79 with a stop at 163 (4.6% risk, ~18 bps). Target 187.

Resulting gross is ~55%, net ~55%, no theme or cluster near limits, and cash stays at ~45%, which keeps dry powder in a market where my existing positions are already showing mixed signals.

```json
{"actions":[{"ticker":"SPY","action":"hold","stop":745,"target":0},{"ticker":"SMH","action":"hold","stop":500,"target":0},{"ticker":"GLD","action":"hold","stop":0,"target":0},{"ticker":"XLE","action":"hold","stop":0,"target":0},{"ticker":"BTC-USD","action":"hold","stop":70000,"target":0},{"ticker":"QQQ","action":"hold","stop":0,"target":0}],
 "trades":[{"ticker":"XLV","side":"long","pct":5.0,"thesis":"Long XLV as a defensive, low-correlation sleeve against a tech-heavy book; wrong if it closes below 180 by 2026-12-31.","stop":180,"target":205},{"ticker":"IEF","side":"long","pct":5.0,"thesis":"Long IEF as a Treasury hedge against an equity drawdown; wrong if it closes below 88.5 by 2026-12-31.","stop":88.5,"target":96},{"ticker":"XLI","side":"long","pct":4.0,"thesis":"Long XLI for cyclical breadth outside tech; wrong if it closes below 163 by 2026-12-31.","stop":163,"target":187}]}
```
