Existing book

SPY: hold. It is flat against entry, and the thesis and stops are unchanged.
SMH: hold, and tighten the stop from 460 to 478 to protect the +2.7% gain while keeping room for normal swings.
GLD: hold. It is down 3.3% and about 1.4% above its 362 stop, so I’m not adding without a new thesis. If the stop hits, the loss is small and the position closes automatically.

New trades

XLE long, 5% NAV: energy is uncorrelated with the equity and gold exposure already in the book. It risks about 29 bps to the stop.
BTC-USD long, 4% NAV: a small crypto sleeve for asymmetric upside. It risks about 40 bps to the stop.

That keeps equity-beta cluster exposure at about 18%, below the 25% cap, with roughly 60% cash still in reserve.

```json
{"actions":[{"ticker":"SPY","action":"hold","stop":0,"target":0},{"ticker":"SMH","action":"hold","stop":478,"target":0},{"ticker":"GLD","action":"hold","stop":0,"target":0}],
 "trades":[{"ticker":"XLE","side":"long","pct":5.0,"thesis":"Long XLE for energy exposure that diversifies the equity and gold book; wrong if it closes below 59.5 or the sector loses relative strength by mid-December.","stop":59.5,"target":71.0},{"ticker":"BTC-USD","side":"long","pct":4.0,"thesis":"Long BTC as a small asymmetric-upside sleeve; wrong if it breaks below 66,000 by early December.","stop":66000,"target":90000}]}
```