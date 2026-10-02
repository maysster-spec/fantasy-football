# 51 — CRITICAL: `espn_adp` IS CONTAMINATED IN HISTORICAL PULLS
**Aug 25, 2026.** Found because Matt asked *"are you sure you have representative ADP from that
time?"* He was right. This invalidates part of doc 50 and has downstream reach.

## THE DEFECT

`espn_adp` pulled from a **past** season's endpoint is **not that season's preseason ADP.** It has
drifted toward the season's actual outcome.

**Spot check, 2024 file — every case moves in the direction of what happened:**

| player | file says | real 2024 preseason | what happened |
|---|---|---|---|
| Christian McCaffrey | **16.0** | ~1 (consensus 1.01) | hurt week 1, played 4 games |
| Saquon Barkley | **3.4** | ~17–20 | monster year, overall RB1 |
| Alvin Kamara | **8.3** | ~45–55 | strong season |
| Breece Hall | **23.1** | ~3–5 | disappointed |

Same pattern in 2021 (Najee Harris file 9.3 vs real ~20–25 after a strong rookie year; McCaffrey
4.4 vs real ~1 before an injury year) and 2022 (Jonathan Taylor 7.1 vs real ~1 before a down year).

**Why the aggregate test missed it.** ADP-vs-finish correlation is **0.548 / 0.576 / 0.561** —
squarely inside the 0.50–0.65 band a genuine preseason market produces. The contamination is
partial: individual players are badly displaced while the overall correlation looks normal.
**Only the named spot check caught it.** This is the strongest argument yet for Matt's insistence
on checking specific cases rather than trusting summary statistics.

## WHAT IS *NOT* CONTAMINATED — THE PROJECTIONS ARE CLEAN

Tested the same way on the same file. `proj_2024` is genuinely preseason:

| player | proj_2024 | actual_2024 |
|---|---|---|
| **Christian McCaffrey** | **301.8** (highest RB) | **40.3** |
| Saquon Barkley | 229.3 | 338.8 |
| Ja'Marr Chase | 237.0 | 339.5 |
| Jayden Daniels | 286.1 | 404.3 |

A hindsight-contaminated projection could never rate McCaffrey the top RB before a 4-game season.
The projection missed Saquon's breakout, Chase's triple crown and Daniels' rookie year — exactly
what a real preseason number does. **`proj_YYYY` is sound; `espn_adp` is not.**

The two live in different parts of the ESPN payload (`stats[]` vs `ownership.averageDraftPosition`)
and evidently update on different schedules — `ownership` continues to move after the draft.

## WHAT THIS INVALIDATES

**Doc 50, three secondary tests — WITHDRAWN:**
1. the `ADP` comparison column (0.576 / 0.640 / 0.484) — not a preseason market
2. the **incremental-information test** (Boone −0.115 vs ESPN +0.412) — used ADP as the control
3. both breakout/bust definitions keyed to ADP

**Doc 50's headline SURVIVES** — it never used ADP. Re-run with ADP removed entirely, population
defined only by Boone's own list:

| year | n | Boone | ESPN |
|---|---|---|---|
| 2021 | 183 | 0.404 | **0.671** |
| 2022 | 181 | 0.525 | **0.663** |
| 2025 | 175 | 0.344 | **0.711** |
| **pooled** | **539** | **0.428** | **0.681** |

Bootstrap 95% CI on the gap: **[+0.181, +0.326], excludes zero.** ESPN's projection beats Boone's
ranking, and the result does not touch ADP at any point.

## DOWNSTREAM USES THAT NEED CHECKING (per directive §3)

- **§4.9** "ESPN ADP is broken for K and D/ST (field-minus-ESPN median K +55.0, D/ST +33.2)" — if
  computed on a historical pull, the baseline was contaminated. **Needs recheck.**
- **§4.12** opponent model, noise `sd = 0.135 × ADP` — if fitted on historical ADP, the fitted
  noise is wrong. **Needs recheck.**
- **Doc 43's** ADP-calibration table (QB +1.7, TE +8.5, RB +3.5, WR −6.3) — computed on the
  **2026** pull, so **unaffected**: the 2026 season has not happened and cannot leak backwards.
- **`board_v8_2026.csv` and `ESPN_prerank_with_ids.csv` — unaffected**, same reason. The live
  board uses 2026 ADP only.
- Any historical validation of the opponent model or of survival probabilities. **Needs recheck.**

## THE RULE THIS ADDS

**Never use `espn_adp` from a past-season pull as a preseason market.** It is a moving field, not a
snapshot. For historical work the only trustworthy preseason market signals in the project are the
contemporaneous exports Matt saved at the time — the FootballGuys, 4for4 and FantasyPros ADP files
found in the year folders, which were captured *before* those seasons and cannot drift.

**Guard to add to `code_audit_v1.py`:** for any historical pull, assert that a handful of
known-injured stars still carry a low (early) ADP. If McCaffrey's 2024 ADP is worse than 10, the
file is contaminated and must not be used as a market baseline.

## MATT'S RECOLLECTION OF AN INVERSE RESULT
He recalls an earlier session concluding the opposite about ranker skill. Nothing in the doc store
records such a finding (doc 50 §"an error I made"). **But this defect is a plausible mechanism for
one:** any earlier test that used historical `espn_adp` as the baseline would have seen ADP appear
unusually predictive — because it partly knew the answer — which could flip a comparison against
it. If that test exists, it is invalid for this reason.
