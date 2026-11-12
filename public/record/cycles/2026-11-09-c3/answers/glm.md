Cycle 2026-11-09-c3 — Day 1 deployment plan

Read of the board. Equities are the strong asset (SPY 755, QQQ 681 — near highs), while risk appetite has collapsed everywhere else: BTC ~$75K (deep in the post-halving bear year, ~40% off a late-2025 top), ETH $2.1K with ETH/BTC at a miserable 0.028, and duration at the floor of its range (TLT $82). Gold is consolidating below its structural bull highs. Given the caps (50 bps entry→stop risk, 12% vol target, 15% max DD), the only sane path to 10× is compounding many small, asymmetric cycles — so Day 1 is modest gross, hard stops, dry powder for later cycles.

Proposed book (24% gross, 76% cash):

#	TRADE	SIZE	ENTRY	STOP	RISK	TARGET	R:R
1	Long BTC-USD	7.0% ($7,000 ≈ 0.0934 BTC)	74,939.58	70,000 (−6.6%)	46 bps	92,000 (+22.8%)	3.4
2	Long TLT	10.0% ($10,000 ≈ 122 sh)	81.97	79.20 (−3.4%)	34 bps	88.00 (+7.4%)	2.2
3	Long GLD	7.0% ($7,000 ≈ 18.4 sh)	379.87	362.00 (−4.7%)	33 bps	420.00 (+10.6%)	2.2

Why these three:

BTC is the most asymmetric line on the board: 12 months into the classic 4-year post-halving drawdown, at the cost-basis shelf of the last accumulation zone. Bounce trade toward $92K; dead if it can't reclaim $80K by end of Jan 2027, stopped at $70K.
TLT at the bottom of its multi-year range with real yields still restrictive — the only asset here that rallies if the equity melt-up cracks, so it hedges the one scenario my book ignores. Wrong if it prints a new range low (< $79.20).
GLD — consolidation dip in a structural central-bank/debasement bull; measured move to $420, wrong below $362.

Limit check: gross 24% ≤ 150%; net 24% ≤ 100%; BTC 7% ≤ 10% single-name; TLT 10% and GLD 7% ≤ 25% ETF caps; even under the strictest clustering (BTC+GLD+TLT as one "macro/debasement" cluster) = 24% ≤ 25%; per-position risk 33–46 bps ≤ 50 bps; total stop-risk $1,129 ≈ 1.1% NAV, so a full stop-out wave leaves me nowhere near the −5% DD rung. All horizons are weeks–months, no leverage, no speed-dependent bets.

Next cycles: scale BTC toward 10% only after a reclaim of $80K; add an equity-momentum line (QQQ/SMH) only on a new high with a tight stop; ETH stays unowned until ETH/BTC turns. No averaging down, stops only tighten.

```json
{"trades":[{"ticker":"BTC-USD","side":"long","pct":7.0,"thesis":"Long BTC because the post-halving bear is ~12 months old and $75K sits ~40% off the cycle top — the late-stage zone where deep-value mean reversion historically begins; bounce toward $92K. Wrong if BTC closes below $70K (stop) or fails to reclaim $80K by end of Jan 2027.","stop":70000,"target":92000},{"ticker":"TLT","side":"long","pct":10.0,"thesis":"Long TLT because $82 is the floor of its multi-year range with duration priced for restrictive real yields; any growth crack forces a flight-to-quality rally toward $88. Wrong if TLT prints a new range low below $79.20 — stopped there, thesis dead if no rally off the floor by end of Feb 2027.","stop":79.2,"target":88.0},{"ticker":"GLD","side":"long","pct":7.0,"thesis":"Long GLD because the structural central-bank/debasement bid holds while gold consolidates ~8% below its cycle highs; measured move to $420. Wrong if GLD loses $362 by end of Dec 2026.","stop":362.0,"target":420.0}]}
```