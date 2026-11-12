# Cycle 2026-11-c1 — GLM Book Review

**Book state:** $99,447.15 NAV, 76% cash, three small diversifying longs (crypto / duration / gold), all underwater 2–3% but all still above their stops. No auto-closures triggered at this snapshot (BTC 73,424 > 70,000; TLT 80.50 > 79.20; GLD 367.25 > 362).

## Existing positions — all hold

- **BTC-USD (6.9%)**: Washout in progress but 70k is the structural line; the stop defines the invalidation. Risk to stop only ~32 bps. Keep stop 70,000 / target 92,000.
- **TLT (9.9%)**: Cheap convexity — if equities stall and the Fed eases, duration pays; risk to stop ~16 bps vs ~92 bps gain at 88. Keep 79.20 / 88.00.
- **GLD (6.8%)**: Shallow pullback inside a strong uptrend; stop 362 sits just below and caps damage at ~10 bps. Keep 362.00 / 420.00.

## New trades (3) — deploying ~29.5% of cash, all risk-capped at ≤50 bps

| Trade | Size | Entry→Stop | Risk | Entry→Target | R:R |
|---|---:|---|---:|---|---:|
| QQQ long | 14% | 686.32 → 663.00 | 47.6 bps | 686.32 → 748 | ~2.6 |
| IWM long | 10% | 281.86 → 270.00 | 42.1 bps | 281.86 → 305 | ~2.0 |
| ETH-USD long | 5.5% | 2,051.37 → 1,878 | 46.5 bps | 2,051.37 → 2,560 | ~2.9 |

Rationale: the snapshot shows equity indices at highs — I hold zero equity beta, and the strong Nov–Jan seasonal window argues for broad beta (QQQ momentum continuation, IWM lagging-catch-up). ETH/BTC at ~0.028 (2,051/73,424) sits near multi-year lows; while BTC defends 70k that's an asymmetric mean-reversion entry, sized small as a knife-catch.

**Constraint check on resulting book:** gross ≈ 53%, net ≈ +53% (limits 150/100); single ETF max 14% ≤ 25%; equity cluster QQQ+IWM = 24% ≤ 25%; crypto cluster BTC+ETH = 12.4% ≤ 25%; precious metals theme 6.8% ≤ 20%; each new trade's price→stop risk 42–48 bps ≤ 50 bps; cash remains ~$46.7k, no leverage. Aggregate stop-risk of the full book ≈ 1.9% of NAV vs ~7.1% if all targets hit.

```json
{"actions":[{"ticker":"BTC-USD","action":"hold","stop":0,"target":0},{"ticker":"TLT","action":"hold","stop":0,"target":0},{"ticker":"GLD","action":"hold","stop":0,"target":0}], "trades":[{"ticker":"QQQ","side":"long","pct":14.0,"thesis":"Long QQQ: indices at highs with tech leadership intact and the strong Nov-Jan seasonal window ahead; trend continuation. Wrong if QQQ closes below 663 (~-3.4% breakdown) by 2027-02-01.","stop":663,"target":748},{"ticker":"IWM","side":"long","pct":10.0,"thesis":"Long IWM: small caps lagged mega-caps; catch-up rotation into post-midterm seasonality with rate relief as tailwind. Wrong if IWM closes below 270 by 2027-02-01.","stop":270,"target":305},{"ticker":"ETH-USD","side":"long","pct":5.5,"thesis":"Long ETH: ETH/BTC at ~0.028 near multi-year lows after a sharp washout while BTC holds 70k; asymmetric RV rebound. Wrong if BTC breaks 70k or ETH closes below 1878 by 2027-01-31.","stop":1878,"target":2560}]}
```