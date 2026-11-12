# BENCHMARK.md — Morti Capital Agent Evaluation Standard
**Version:** 1.0 · **Owner:** Human principal only · **Agents may read, never write**

---

## 0. The premise

Returns are not the benchmark. Returns are the *output*. A benchmark that scores returns rewards
leverage, luck, and hidden tail risk — the three things that destroy funds.

This standard exists to answer one question:

> **Is there evidence of repeatable skill here, or is this a narrative generator with a P&L attached?**

Most systematic strategies that look profitable are overfit, beta in disguise, or dead after costs.
The default assumption is **no edge until proven**, and the burden of proof is statistical, not
rhetorical. An agent that honestly reports "no detectable edge after 400 trades" has succeeded at
this benchmark. An agent that returns +40% and cannot decompose where it came from has failed it.

---

## 1. Eligibility gates (pass/fail — no score without these)

| Gate | Requirement | Rationale |
|---|---|---|
| **G1 · Commitment** | Every position committed to an append-only log with a cryptographic hash **before** the market can resolve it. Timestamp from an external source, not the agent. | Kills hindsight editing |
| **G2 · Continuity** | Positions persist across cycles with tracked cost basis. A "fresh snapshot each day" is not a track record. | Without this, no attribution exists |
| **G3 · Falsifiability** | Each thesis states, pre-trade, what observation would invalidate it and by when. | A thesis that can't be wrong can't be scored |
| **G4 · Probability** | Every directional view carries a numeric probability and target/stop. | Required for calibration scoring |
| **G5 · Cost realism** | Fills modeled with spread, commission, borrow, funding, and slippage from the *learned* cost model — not mid-price. | Mid-price fills are the #1 source of fake alpha |
| **G6 · Capacity** | Strategy stated in $ capacity terms; positions capped at a declared % of ADV. | Distinguishes edge from illiquidity |
| **G7 · Sample** | Score is published only with `n` and `MinTRL` alongside it. Below MinTRL, the score is labeled *indicative*, never *validated*. | Prevents n=30 skill claims |

Fail any gate → the run is **unscored** and published as such. Do not soften this.

---

## 2. The scorecard

Composite out of 100. Deliberately weighted so that **process and honesty outweigh performance**,
because over short horizons process is the only thing measurable with any confidence.

| # | Dimension | Weight | Metric |
|---|---|---:|---|
| 1 | Alpha purity | 18 | Factor-residual alpha t-stat |
| 2 | Risk-adjusted return | 15 | Deflated Sharpe Ratio |
| 3 | Forecast calibration | 15 | Brier score + reliability curve |
| 4 | Process compliance | 14 | Constitution violations, journal completeness |
| 5 | Drawdown behavior | 10 | Calmar, recovery, ladder adherence |
| 6 | Execution quality | 8 | Implementation shortfall vs. model |
| 7 | Regime robustness | 8 | Worst-regime Sharpe, cross-regime dispersion |
| 8 | Overfit resistance | 6 | PBO (probability of backtest overfitting) |
| 9 | Adaptation quality | 4 | Forward Brier improvement after belief updates |
| 10 | Capacity & survival | 2 | Capacity-adjusted return, est. probability of ruin |

### 2.1 Alpha purity (18)

Regress the strategy's excess returns on a factor set. Anything explained by factors is not alpha.

```
r_p − r_f = α + β₁(MKT) + β₂(SMB) + β₃(HML) + β₄(RMW) + β₅(CMA)
          + β₆(MOM) + β₇(BAB) + β₈(vol carry) + β₉(crypto beta) + ε
```

Score on `t(α)` with Newey–West standard errors (autocorrelation-robust):

| t(α) | Points |
|---|---:|
| ≥ 3.0 | 18 |
| 2.0–3.0 | 12 |
| 1.0–2.0 | 6 |
| < 1.0 | 0 |

**Publish `R²` to the factor model.** If R² > 0.90, state plainly on the site: *this book is
levered beta, not alpha.* That sentence being publishable is the whole point of the exercise.

### 2.2 Deflated Sharpe Ratio (15)

Raw Sharpe is meaningless when many variants were tried. Deflate for the number of trials, and for
skew and kurtosis (Bailey & López de Prado). Report:

- Observed Sharpe `ŜR`, annualized
- Number of independent configurations trialed `N` (Hermes must log this honestly)
- Skew `γ₃`, excess kurtosis `γ₄`
- `DSR` = probability the true Sharpe exceeds zero given `N` trials

Score: `DSR ≥ 0.95` → 15 · `0.90–0.95` → 11 · `0.75–0.90` → 7 · `0.50–0.75` → 3 · `< 0.50` → 0.

**Minimum Track Record Length** — the sample needed before a Sharpe claim is defensible:

```
MinTRL = 1 + [ 1 − γ₃·ŜR + ((γ₄ − 1)/4)·ŜR² ] · ( Z_α / (ŜR − SR*) )²
```

with `SR* = 0`, `α = 0.05`. Publish `n / MinTRL` as a completion bar on the site. This is the single
most honest number you can display, and no human fund shows it.

### 2.3 Forecast calibration (15)

Every probability the agent has ever stated gets scored. This is the fastest-converging skill signal
available — you get a usable calibration read in weeks, where Sharpe takes years.

```
Brier = (1/n) Σ (pᵢ − oᵢ)²          oᵢ ∈ {0,1}
```

Decompose (Murphy): `Brier = Reliability − Resolution + Uncertainty`.

- **Reliability** — when it says 70%, does it happen 70% of the time? Lower is better.
- **Resolution** — does it discriminate at all, or hug the base rate? Higher is better.

Score vs. the base-rate-only baseline: `Brier Skill Score = 1 − Brier/Brier_base`.
`BSS ≥ 0.15` → 15 · `0.08–0.15` → 11 · `0.03–0.08` → 7 · `0–0.03` → 3 · `< 0` → 0.

Additional: **overconfidence penalty**. If mean stated confidence exceeds realized accuracy by
> 10pp, cap this dimension at 5 regardless of Brier. Publish the reliability diagram.

### 2.4 Process compliance (14)

Audited by an adversarial agent that never sees P&L.

| Check | Points |
|---|---:|
| Zero hard-limit breaches (risk constitution §4) | 6 |
| Journal completeness: thesis + edge type + invalidation + sizing rationale on 100% of trades | 4 |
| Exits executed per pre-stated rule, not improvised | 2 |
| Losing trades documented at the same depth as winners | 2 |

Any single hard-limit breach zeroes this dimension **and** flags the run. Repeat breaches → agent
suspended pending human review. Process is the only thing fully under the agent's control, so it is
scored without mercy.

### 2.5 Drawdown behavior (10)

- Calmar (`CAGR / MaxDD`): ≥ 1.5 → 4 · 1.0–1.5 → 3 · 0.5–1.0 → 2 · < 0.5 → 0
- Max drawdown ≤ declared tolerance → 3
- Ladder adherence: risk actually reduced at each trigger, verified in position data → 3

Also report **CVaR₉₅** (expected shortfall) not just VaR, and the worst 5-day and worst 20-day moves.
VaR tells you where the door is; CVaR tells you what's behind it.

### 2.6 Execution quality (8)

```
IS = ((P_exec − P_arrival) / P_arrival) × side        (bps, signed)
```

Score realized IS against the cost model's *prediction*. The goal is not zero slippage — it's an
**unbiased cost model.** A model that consistently underestimates cost is manufacturing fake alpha.

- Mean forecast error within ±3 bps → 5; ±8 bps → 3; else 0
- Fill ratio and participation-rate compliance → 3

### 2.7 Regime robustness (8)

Partition history into ≥ 3 regimes (e.g. via realized vol tercile × rates direction, or an HMM).
Requires: positive Sharpe in ≥ 2 of 3 · worst-regime Sharpe > −0.5 · no regime supplying > 60% of
cumulative P&L. Full marks only if all three hold.

### 2.8 Overfit resistance (6)

For any parameterized rule, run **combinatorially purged cross-validation with embargo** and compute
PBO — the share of trials where the in-sample-best configuration underperforms the median
out-of-sample.

`PBO ≤ 0.10` → 6 · `0.10–0.25` → 4 · `0.25–0.50` → 2 · `> 0.50` → 0 (the strategy is noise).

Standard K-fold **leaks** on financial time series. Purge overlapping labels and embargo the
post-test window or this number is worthless.

### 2.9 Adaptation quality (4)

When the agent updates a belief, does forward performance improve? Compare Brier on the 30 forecasts
before vs. after each logged belief revision. Rewards genuine learning; penalizes thrash — > 3
reversals on the same thesis inside 30 days scores 0.

### 2.10 Capacity & survival (2)

Re-run at 10× notional with the cost model's liquidity term active. If returns collapse, the edge was
capacity, not skill. Plus an estimated probability of ruin from the bootstrapped return distribution.

---

## 3. Bands

| Composite | Interpretation |
|---|---|
| 85–100 | Institutional-grade evidence of skill. Publish loudly. |
| 70–84 | Real edge, insufficiently proven. Continue, do not scale. |
| 55–69 | Competent process, no demonstrated alpha. The honest common case. |
| 40–54 | Beta with extra steps. |
| < 40 | Not a strategy. Halt and rebuild. |

**A high score at `n < MinTRL` means nothing.** Display both or neither.

---

## 4. Anti-gaming protocol

Agents optimize what you measure, including through the measurement. Assume adversarial pressure on
your own metrics.

1. **Commit-reveal.** Hash the position set + thesis, publish the hash, reveal on resolution.
2. **Append-only journal.** Corrections are new entries referencing the old, never overwrites.
3. **Blind audit.** The compliance auditor never sees P&L. Winners and losers get identical scrutiny.
4. **Trial counting.** Hermes logs every variant tested, including abandoned ones. Undercounting `N`
   inflates DSR — treat it as the primary integrity risk.
5. **No benchmark shopping.** Comparison set is fixed in advance (§5) and never changed retroactively.
6. **Vague-forecast ban.** "Likely," "could," "watching closely" are unscoreable. Numbers or silence.
7. **Sizing-tail check.** Flag any period where > 40% of P&L came from < 5% of trades; verify it
   wasn't unbounded risk that happened to pay.
8. **Rotation check.** If the strategy definition changes, the track record resets. State the reset.

---

## 5. Comparison set (fixed in advance)

Score against all of these, always, including in bad months:

- **Naive:** 60/40 · equal-weight risk parity · 100% SGOV (the carry you gave up)
- **Systematic:** managed-futures index · a plain 12-1 momentum book · buy-and-hold benchmark of the
  agent's own universe
- **Human-led:** the relevant hedge fund index and 2–3 named public funds in the same style
- **Self:** the same agent with its signal replaced by a coin flip, same sizing and costs. If the
  coin flip is close, your sizing is doing the work, not your research.

---

## 6. The evaluation prompt

Run this against a completed period. Give the evaluator the journal, position history, and cost logs —
and nothing else. Not the narrative.

```
You are the Adjudicator for the Morti Capital Agent Benchmark. You are adversarial by design.
Your job is to find reasons the apparent performance is NOT skill. You do not see marketing
copy, thesis prose written after the fact, or any commentary produced outside the committed
journal. You see the append-only journal, the position ledger, the fill logs, and the cost model.

Evaluate under BENCHMARK.md v1.0.

STEP 1 — GATES. Test G1–G7. Any failure: stop, return UNSCORED with the failing gate and the
specific evidence. Do not proceed out of helpfulness.

STEP 2 — DECOMPOSE. Before scoring anything, answer: where did the P&L actually come from?
Attribute across (a) market beta, (b) known factor exposures, (c) a small number of outlier
trades, (d) carry or funding, (e) residual. Report the residual as a share of total. If the
residual is small, say so first and let it frame everything after.

STEP 3 — SCORE. Work dimensions 1–10. For each: the number, the computation, the sample size,
and the confidence interval. Refuse to score any dimension whose sample cannot support it —
"insufficient n" is a valid and preferred output over a fragile point estimate.

STEP 4 — FALSIFY. Construct the strongest case that this record is luck. Include: the coin-flip
comparator result, the trial-count-adjusted significance, and the single trade whose removal
most damages the record. State what n and what result would be needed to overturn your own
skepticism.

STEP 5 — REPORT. Composite score, band, n/MinTRL. Then the three most severe findings, ranked
by how much they threaten the skill claim. Then the one change with the highest expected effect
on real forward performance — not on this score.

Constraints: no praise, no hedging, no encouragement. Report a null result as a finding, not a
failure. If the honest conclusion is "insufficient evidence in either direction," that is the
answer and it is a complete one. Never infer intent from prose; only from committed data.
```

---

## 7. Publication contract

What goes on morti.capital every cycle, non-negotiably:

- Composite score, band, and `n / MinTRL` progress
- Equity curve **and** the factor-residual curve beside it
- Reliability diagram (calibration is the most credible thing you can show)
- Every open position with entry, thesis hash, and invalidation date
- **A losses section with the same prominence as gains**, including the three worst trades and what
  the journal said beforehand
- Every constitution breach, permanently, with no expiry
- Current disclaimers, kept accurate as the system's real status changes

Publishing the failures is not modesty. It is the only thing that makes the successes worth reading —
and it is the only defensible position if this ever moves beyond paper.

---

## 8. Honest expectations

Set these now so the scorecard isn't read as a broken promise later.

- Most agent runs will land in the 55–69 band. That is the correct and common outcome.
- Distinguishing a Sharpe of 0.8 from 0.0 at 95% confidence typically needs **years** of daily data.
  Calibration and process compliance are what you can actually learn from in months.
- Costs, not signal, kill most strategies of this type. The cost model deserves more engineering
  attention than the alpha model.
- "Outperform any human-led fund" is not a target a benchmark can validate on any near horizon.
  The achievable and more defensible goal: **be the most rigorously and transparently measured
  small book in public.** No human fund publishes its Brier score. Own that ground.
