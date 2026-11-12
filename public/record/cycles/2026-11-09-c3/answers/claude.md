I’m treating this as a paper-trading exercise, not financial advice. I took a modest, diversified posture on day one: risk is sized at about 48 to 50 bps per position, and about 72% of the book stays in cash. I haven’t pulled any news or macro data beyond your snapshot, so these are trend-and-diversification calls, not a view built on fresh research.

- **SPY long, 10%:** Core equity beta in a market that has held its levels. The stop is about 4.9% below entry, so risk is about 49 bps.
- **SMH long, 8%:** Semis lead the tape, and the stop is about 6% below entry, so risk is about 48 bps. SPY and SMH together are 18% of NAV, inside the 25% correlation-cluster cap.
- **GLD long, 10%:** A diversifier against the equity exposure, with a stop about 4.7% below entry (risk about 47 bps).

```json
{"trades":[{"ticker":"SPY","side":"long","pct":10.0,"thesis":"Long SPY for core equity beta because the trend remains intact and a day-one book needs market exposure; wrong if it closes below 718 (about -4.9%) by 2026-12-31.","stop":718,"target":830},{"ticker":"SMH","side":"long","pct":8.0,"thesis":"Long SMH because semis lead the tape and AI capex momentum is underpriced in a trending market; wrong if it closes below 460 (about -6%) by 2026-12-31.","stop":460,"target":560},{"ticker":"GLD","side":"long","pct":10.0,"thesis":"Long GLD as a diversifier against the equity exposure, because gold has trended up and offsets equity drawdowns; wrong if it closes below 362 (about -4.7%) by 2027-01-31.","stop":362,"target":420}]}
```