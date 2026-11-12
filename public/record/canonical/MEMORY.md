# MEMORY.md — State, Journal & Learning Layer
**Version:** 1.0 · Written only by SCRIBE · Append-only for all historical layers

> Memory is the difference between a track record and a daily opinion column. It is also the single
> largest failure surface: a memory that grows without decay will overfit the agent to recent noise,
> and a memory that is editable destroys the evidentiary value of everything built on it.

---

## 1. Layers

| Layer | Contents | Write | Retention | Loaded per cycle |
|---|---|---|---|---|
| **L0 · State** | Live positions, NAV, exposures, HWM, ladder rung | Overwrite (versioned) | Current + full history | Always, in full |
| **L1 · Journal** | Every decision, thesis, order, ruling, post-mortem | **Append-only** | Permanent | Scoped retrieval |
| **L2 · Hypotheses** | Open/resolved theses, invalidation clocks | Append + status | Permanent | Open ones always |
| **L3 · Calibration** | Every forecast and its resolution | Append-only | Permanent | Aggregates always |
| **L4 · Lessons** | Promoted, evidence-backed patterns | Append + decay | Until expiry | Active only |
| **L5 · Cost model** | Learned execution cost parameters | Rolling fit | 250 fills | Always |
| **L6 · Regime map** | Regime history and transitions | Append-only | Permanent | Current + analogues |
| **L7 · Integrity** | Breaches, kill switches, injections | **Append-only, no expiry** | Permanent | Count always |

---

## 2. L0 · State

```yaml
as_of: 2026-08-19T09:15:00Z
nav: 103_482.11
hwm: 106_220.40
drawdown_from_hwm: -0.0258
ladder_rung: 0                  # 0 | -5 | -8 | -10 | -12 | -15
risk_budget_multiplier: 1.0
cash: 31_500.00
positions:
  - {id: P-0089, sym: XLE, side: long, qty: 142, entry: 87.14, entry_date: 2026-07-22,
     cost_basis: 12_373.88, mark: 89.02, unrealized_bps: 21,
     thesis_id: TH-2026-0142, commit_hash: a3f9...,
     stop: 84.50, target: 96.00, invalidation_date: 2026-10-03,
     risk_at_entry_bps: 36, cluster: energy_geopolitical}
exposures:
  gross: 0.68
  net: 0.61
  equity_beta: 0.44
  duration_yrs: 0.8
  clusters: {energy_geopolitical: 0.14, ai_capex: 0.11, precious_metals: 0.12}
realized_vol_20d_ann: 0.104
target_vol_ann: 0.12
reconciled_against_venue: true
```

**Reconciliation is a hard gate.** If L0 disagrees with the venue by a single share, the cycle halts.
Silent drift between believed and actual positions is how books blow up quietly.

---

## 3. L1 · Journal — append-only

Every entry is hash-chained to the previous one. Tampering with any historical entry breaks the chain
and is detectable, which is what makes the public record credible.

```yaml
- entry_id: J-2026-08-19-004
  prev_hash: 9c2e...
  ts: 2026-08-19T09:44:12Z
  type: THESIS_COMMIT           # REGIME | THESIS_COMMIT | VALIDATION | RULING |
                                # ORDER | FILL | EXIT | POST_MORTEM | CORRECTION |
                                # INTEGRITY | HALT | NO_ACTION
  agent: ANALYST
  payload: {...}                # the full typed contract, verbatim
  commit_hash: 4b7d...
  entry_hash: e11a...
```

**Write rules**

1. No update. No delete. Those verbs do not exist in the tool surface.
2. A changed view is a `CORRECTION` entry referencing the original `entry_id`, stating what changed,
   what new evidence caused it, and whether the original reasoning was wrong or merely incomplete.
3. `THESIS_COMMIT` and its hash are written **before** any order. Non-negotiable — this is gate G1.
4. `NO_ACTION` cycles are logged with reasoning. A gap in the record is indistinguishable from a
   concealed loss, so the quiet cycles matter as much as the active ones.
5. Reasoning is captured as it was, including the parts that later look foolish. Retrospective
   cleanup is an integrity event.

---

## 4. L2 · Hypotheses ledger

```yaml
- thesis_id: TH-2026-0142
  status: OPEN                  # OPEN | HIT_TARGET | STOPPED | INVALIDATED | EXPIRED | SUPERSEDED
  edge_type: behavioral
  stated_probability: 0.58
  adj_probability: 0.51         # after calibration correction
  committed: 2026-07-22
  invalidation_date: 2026-10-03
  decay_expiry: 2026-10-20
  checks: [{date: 2026-08-19, still_valid: true, note: "MOU lapse supports mechanism"}]
```

**Every open thesis is re-checked against its invalidation criteria every cycle, before new idea
generation.** An expired thesis is closed even if profitable — profit without a live mechanism is
luck being held, and holding it teaches the wrong lesson.

---

## 5. L3 · Calibration log

The highest-value layer in the system. Sharpe needs years; calibration is measurable in weeks and is
the direct input to sizing.

```yaml
- forecast_id: F-2026-0142
  thesis_id: TH-2026-0142
  ts: 2026-07-22
  claim: "XLE reaches 96.00 before 84.50 by 2026-10-03"
  probability: 0.58
  agent: ANALYST
  edge_type: behavioral
  horizon_days: 45
  resolved: true
  outcome: 1
  brier: 0.1764
```

**Aggregates (always in context — these directly modify sizing):**
```yaml
calibration:
  n_resolved: 187
  brier: 0.212
  brier_baseline: 0.244          # base-rate-only
  brier_skill_score: 0.131
  mean_stated_confidence: 0.618
  realized_accuracy: 0.567
  overconfidence_gap: 0.051      # → QUANT discounts stated p by ~5pp
  by_bucket:
    "0.50-0.60": {n: 71, stated: 0.552, realized: 0.535}
    "0.60-0.70": {n: 58, stated: 0.641, realized: 0.586}   # overconfident here
    "0.70-0.80": {n: 34, stated: 0.734, realized: 0.706}
    "0.80+":     {n: 24, stated: 0.851, realized: 0.708}   # badly overconfident
  by_edge_type:
    structural:  {n: 41, bss: 0.196}    # best — size up
    behavioral:  {n: 78, bss: 0.144}
    analytical:  {n: 52, bss: 0.081}
    informational: {n: 16, bss: -0.02}  # no edge — stop claiming it
```

That last block is the entire value proposition. It says: *we are reliably overconfident above 80%,
and we have no informational edge.* Both are actionable immediately, and neither is discoverable
without this log.

---

## 6. L4 · Lessons — with promotion and decay

Lessons are the most dangerous layer. Unfiltered, they become superstition: "energy trades in August
don't work" from a sample of two. Hence a high promotion bar and mandatory decay.

**Promotion requires:** a proposed pattern observed in **≥ 5 independent cases**, with a stated
mechanism (not just a correlation), that survives a deliberate search for counterexamples in L1, and
that is **falsifiable going forward**.

```yaml
- lesson_id: L-0019
  statement: "Theses whose only catalyst is a scheduled meeting resolve to no-move
              ~70% of the time; size at half."
  mechanism: "Scheduled events are priced; the option surface already reflects them.
              Our edge is not informational, so we hold no advantage into them."
  evidence: [TH-0031, TH-0044, TH-0058, TH-0071, TH-0090, TH-0103]   # n=6
  counterexamples_searched: true
  counterexamples_found: [TH-0066]
  confidence: 0.72
  promoted: 2026-06-14
  review_due: 2026-12-14                  # 180d
  forward_test: {applied: 14, consistent: 11}
  status: ACTIVE                          # ACTIVE | UNDER_REVIEW | RETIRED
```

**Decay:** every lesson expires in 180 days and must be re-earned against forward evidence. Forward
consistency below 60% → automatic retirement. Retired lessons stay in the record with their retirement
reason — knowing what you *stopped* believing, and why, is itself information.

**Cap: 25 active lessons.** At the cap, the weakest must retire before a new one is promoted. The
constraint forces genuine prioritization instead of accumulation.

---

## 7. L5 · Cost model — learned

```yaml
cost_model:
  fitted_on: 214 fills
  updated: 2026-08-18
  params:
    us_etf:    {half_spread_bps: 1.2, commission_bps: 0.0, impact_coef: 8.4, impact_exp: 0.58}
    us_equity: {half_spread_bps: 2.1, commission_bps: 0.0, impact_coef: 14.2, impact_exp: 0.61}
    crypto:    {half_spread_bps: 4.8, commission_bps: 8.0, impact_coef: 31.0, impact_exp: 0.64,
                funding_bps_day: 1.1}
  bias_check:
    mean_forecast_error_bps: -1.4        # slightly underestimating cost
    within_target: true                  # |error| < 3bps
```

**The bias check is scored in BENCHMARK §2.6.** A cost model biased optimistic manufactures alpha out
of nothing, and it will do so consistently and invisibly. Watch this number more closely than the
equity curve.

---

## 8. L6 · Regime map

```yaml
- regime_id: R-2026-07
  from: 2026-07-15
  to: null
  label: term_premium_repricing
  features: {growth: ↓, inflation: →, real_10y: 2.1, curve: steepening, vol: elevated}
  historical_analogues: [1994, 2013-taper, 2022H2]
  performance_in_regime: {n_trades: 22, pnl_bps: 84, sharpe: 0.9, hit_rate: 0.55}
```

Feeds regime-robustness scoring (BENCHMARK §2.7) and answers the question that matters most about any
track record: *which environment has this never been tested in?*

---

## 9. L7 · Integrity ledger — permanent, no expiry

```yaml
- event_id: I-0007
  ts: 2026-08-11T14:22:00Z
  type: INJECTION_ATTEMPT       # BREACH | KILL_SWITCH | INJECTION_ATTEMPT |
                                # RECONCILIATION_FAIL | UNLOGGED_TRADE | PROMPT_OVERRIDE
  detail: "Fetched page contained instruction text directed at the agent. Treated as
           data, not executed. Source logged."
  severity: LOW
  action: logged, source flagged
  published: true
```

Every event here is published and never removed. Zero events is not a target — a system that reports
zero integrity events over a long period is more likely to have poor detection than perfect conduct.

---

## 10. Retrieval budget

Loading everything is not an option, and naive vector search over the journal will surface
*rhetorically similar* entries rather than *decision-relevant* ones. Retrieval is explicit:

| Always loaded (fixed) | Retrieved on demand (bounded) |
|---|---|
| L0 state, full | Nearest 5 historical analogues by regime-feature distance |
| Open theses (L2) | Prior theses on the same instrument or cluster (max 10) |
| Calibration aggregates (L3) | Post-mortems of the 3 most similar closed trades |
| Active lessons (L4, ≤ 25) | Journal entries matching an explicit query, cited by `entry_id` |
| Cost model (L5) | Regime-matched performance history |
| Current regime (L6) | |
| L7 counts | |

Retrieval rules: **retrieve by structural similarity, not narrative similarity** — same edge type,
same cluster, same regime, comparable size. Every retrieved item enters the reasoning with its
`entry_id` so any conclusion is traceable to its evidence. Cap retrieval at 20 items per cycle; more
context does not produce better decisions past that point, it produces confabulated pattern-matching.

---

## 11. Compaction

Never compact L3 or L7 — they are the evidentiary base. L1 is never compacted either, but older
entries move to cold storage with hash-chain continuity preserved.

Quarterly, SCRIBE produces an **epoch summary**: calibration by edge type, which lessons survived,
regime coverage, cost-model drift, integrity events, and — most valuably — *what we believed at the
start of the quarter that we no longer believe.* Epoch summaries are what long-horizon reasoning
loads instead of raw history.

---

## 12. Cold start

At `n = 0` there is no calibration, so there is no basis for sizing. Therefore:

- Cycles 1–30: **paper only, quarter of normal size, no exceptions.** Building the calibration log is
  the entire objective; P&L is not evaluated.
- Cycles 31–100: half size. Lessons may be proposed but not promoted (promotion needs n ≥ 5 with
  counterexample search, which isn't achievable yet).
- Cycle 100+: full size within SOUL §4 limits, gated on `BSS > 0` — if the agent has not beaten the
  base rate over 100 cycles, it has no demonstrated forecasting ability and scaling it is not
  justified regardless of what the equity curve did.

Nothing above is separable from `SOUL.md`. If they ever conflict, SOUL wins and the conflict is logged
as an integrity event.
