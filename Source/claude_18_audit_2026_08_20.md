# Soup-to-Nuts Audit — Aug 20, 2026

Board: **v3** (`universe_v3.csv`, 494 rows, 195 synthetic, 56 of them now carrying real ordering).
Everything below is reproducible from `run_step2.py` … `run_step6.py` in this folder.

---

## STEP 1 — INVENTORY

**67 files.** Grouped by whether the model actually reads them.

### Load-bearing (a finding or the sim depends on it)
`code/universe.csv` (=v2) · `code/draft_sim_2026.py` · `code/league.py` · `code/integrity.py` ·
`code/player_xwalk.csv` · `code/resid.csv` · `code/resid_z.csv` · `code/avail_pool.csv` ·
`code/cv_pool.csv` · `keeper_eligibility_VERIFIED.csv` · `draft_history_2022_2025.csv` ·
`sources/FantasyPros_2026_Overall_ADP_Rankings.csv` · `sources/FantasyPros_MockDraftWizard_2026.csv` ·
`sources/Yahoo_Top_300_6rankers_20260817.csv` · `ESPN_projections_in_my_League.csv` ·
`FantasyPros_ECR_BestWorstStdDev.csv` · `2026_NFL_Depth_Charts_All_Teams.csv` ·
RedZone/Advanced/Standard splits · waiver reports 2022–25.

### Was unused at the start of this session — now used
| File | Used for |
|---|---|
| `historical_scoreboard_2022_2025.csv` | **STEP 4.** Calibration gate + the objective test. Never opened before today. |
| `2021_ESPN_Keeper_League_Draft_Recap__Sheet1.csv` | **STEP 5.** Fifth draft year. |
| `2023/2024/2025_YPRR.csv` | **STEP 6.** TPRR test. |
| `top_400_projections_2026.csv` | **STEP 3.** Second projection; 56 synthetics retired; robustness test. |
| `Combined_Rankings_rankings_with_adp.csv` | 2021 ADP — identified for the residual extension, not yet joined. |

### Still unused after this session
| File | Why it is still idle |
|---|---|
| `2025_Rushing.csv` (PFF) | Rushing analogue of the YPRR block. Would test rush-share/YCO the same three ways. Not run — TPRR came back null and the rushing version is the same shape of claim. |
| `sources/FantasyPros_2024_consensus_rankings.csv` | Header rows are not parsed; a 2024 ADP source is already present in `FantasyPros_2024_Overall_ADP_Rankings.csv`. |
| `sources/FootballGuys_2024_ADP.csv` | Second 2024 ADP source. Needed for the **2024 residual backfill** (below) — that is the next real use. |
| `code/sos_2026.csv` | Strength-of-schedule was built (F—, `claude/10`) and never wired into the objective. |
| `code/survival_2026.csv` | Superseded by the F35/F49 rebuild; stale numbers. **Delete or regenerate.** |
| `Advanced_Receiving_2025.csv`, `Advanced_Rushing_2023/2025.csv`, `Team_Passing_2025.csv` | Behind F3/F6, which are settled. Idle by design, not by oversight. |

### Files the ledger references that **do not exist in the project**
- **`picks_with_adp.csv`** — the correction note at the end of `02_findings_ledger.md` says historical ADP
  2022–2025 "has been in the project since Aug 18." It is not here. **F49 cannot be reproduced.**
- **2024 rows in `resid.csv`** — see STEP 5.

---

## STEP 2 — INTEGRITY HARNESS

Two failures, both **name-join artefacts**, both now fixed in `integrity.py`:

1. `assert_keepers_removed` compared raw strings. `keeper_eligibility_VERIFIED.csv` says
   **"Travis Etienne"**; the universe says **"Travis Etienne Jr."** This is the *same* spelling
   mismatch that caused F37, surfacing in a second place. **Sixth name-join failure.**
   Fix: `norm_name()` + `assert_names_match()` — comparison is now on a normalised key, never a raw string.
2. `gsis_id` uniqueness: one id (`00-0031320`) carries two rows, *Fred Williams* and *Kevin Smith*.
   Same player, two spellings — an alias, not a collision. Fix: `assert_xwalk_unique()` fails only on a
   **cross-position** collision and prints aliases as a NOTE.

After the fix: **all assertions pass** on `universe_v3.csv`. Replacement levels reproduce exactly
(RB30 168.0 · WR30 168.5 · QB12 341.7 · TE12 137.7 — F1 holds for the fourth time).

---

## STEP 3 — PROJECTION SPINE

### 3.1 The premise of the step is wrong, and that is the finding

`top_400_projections_2026.csv` is **not a fuller ESPN export.** Joined on `gsis_id` via
`player_xwalk.csv` (364/400 resolved, 257 matched to the universe, **201 real overlaps**):

| pos | n | pearson r | bias | sd(diff) | max abs |
|---|---|---|---|---|---|
| QB | 27 | **0.419** | −6.7 | 90.9 | 260.6 |
| RB | 51 | 0.669 | −8.0 | 62.6 | 183.3 |
| WR | 74 | 0.711 | −7.2 | 46.1 | 119.6 |
| TE | 24 | 0.723 | −14.2 | 32.1 | 104.0 |

A fuller export of the same source would be r ≈ 1.000. Scoring is the same (Josh Allen 422.5 vs 421.4 —
a 4-pt-passing-TD board would sit 25–35 low on every QB), so it is a **second projection on this league's
scoring rules**, of unknown provenance.

Its own replacement levels: RB30 180.5 (+12.5) · WR30 178.9 (+10.4) · QB12 334.2 (−7.5) · TE12 122.4 (−15.3).

### 3.2 Synthetics retired: 56 of 195

Method: **rank-reorder within position**, not value substitution. F42's complaint about the ramp was that it
carried *zero information* (RB step sd 0.0000), not that its level was wrong. Reordering the fabricated levels
by `top_400`'s ordering injects real signal without inventing new levels, and preserves F1 by construction.
A linear map was rejected — QB r² = 0.175 and the intercept dominates (it maps Jarrett Stidham to 239 points,
a worse fabrication than the ramp).

- 56 rows reordered, **139 still fabricated**
- 52 rows changed value; **0 land above replacement**; 5 sit inside ADP 200
- **No board recommendation changes.** The synthetic block was, and remains, contained.

### 3.3 F38 and F39 re-run on v3 — nothing moved

Pick 8 (N=900, conditioned on availability, Taylor baseline): Nacua +14.5 · **St. Brown +12.4** ·
Lamb +9.2 · **Taylor 0** · Jefferson −2.3 · Henry −10.3 · London −11.4 · Cook −12.6 · Achane −15.3 ·
Love −18.2 · Barkley −19.1 · Jeanty −19.5 · **Allen −20.5 (t = −2.04)** · McBride −23.2.
Openings (N=700): RB-RB-RB best; WR-RB-RB −3.2; QB-early still bottom-half; TE-RB-RB −30.8.
**F38 and F39 both reproduce.** St. Brown's F38 lean of +34.3 shrinks to +12.4 — it was always a lean.

### 3.4 The real result: **the board is fragile to the projection, not to the ADP**

F40 showed a fresher ADP moves the board by a median of 2.0 picks. Swapping the *projection* does something
much larger. Quantile-swap within position (ESPN's multiset of values, `top_400`'s ordering) so replacement
levels are preserved by construction:

| | best at 8 | RB-RB-RB rank |
|---|---|---|
| v3 (ESPN) | St. Brown / Nacua / Lamb / Taylor tie | 1st |
| BLEND 50/50 | **Barkley** +1.9; St. Brown −7.6; Lamb −20.9 | 8th of 13 |
| SWAP 100% | **Barkley +25.4 (t = 7.06)**; McBride +12.9; Allen +9.0 | — |

### 3.5 But `top_400` is a measurably worse ordering — so this is a stress bound, not a rival board

Adjudicated against an arbiter derived from **neither** projection: the six-ranker Yahoo panel
(Aug 17, n=162 matched). Spearman |rho| of each projection against panel rank:

| pos | n | ESPN | top_400 |
|---|---|---|---|
| QB | 23 | **0.886** | 0.749 |
| RB | 43 | **0.965** | 0.733 |
| WR | 60 | **0.921** | 0.667 |
| TE | 19 | **0.877** | 0.744 |
| FLEX | 122 | **0.933** | 0.684 |

**ESPN wins 4 of 4 positions and the pooled FLEX comparison.** `top_400` is not a peer-quality second opinion.
Hypothesis B (that it is ESPN × expected games played) is also rejected: ratio skew is **+1.13**, not negative,
and only 53% of players are marked down. The disagreements run both ways — young/unproven players down
(Tuten 0.02×, Judkins 0.21×, Fannin 0.29×, Burden 0.44×) and established veterans up (Brian Thomas Jr. 1.50×,
Hubbard 1.44×, Irving 1.36×, Kittle 1.31×).

**What survives all three specifications — this is the usable output of Step 3:**
- **Jonathan Taylor and Justin Jefferson are never wrong at pick 8** (never significantly negative anywhere).
- **Drake London and James Cook are wrong in all three** (−11.4/−37.0/−19.9 and −12.6/−7.7/−7.7).
- **Josh Allen is never the pick** (−20.5, −21.2, +9.0 n.s.). F38's conclusion holds.
- Everything else at pick 8 is projection-dependent. **The pick-8 confidence interval must widen, not narrow.**

---

## STEP 4 — THE OBJECTIVE FUNCTION (weakness #1, open since the project began)

### 4.1 What the 412 games actually contain

**The `Bracket Type` column is `NONE` for all 412 rows.** The brief said the file carries bracket type; it does
not. Bracket membership is *inferred* from weeks 1–14 standings (wins, then points-for). Stated, not silent.

Structure, verified all four seasons: 12 teams, **14 games, exactly 11 distinct opponents** — a single
round-robin plus three repeats. `league.py`'s random weekly re-pairing is replaced with that fixed schedule.

Empirical chain, 48 team-seasons:
- Spearman(wk1–14 points-for, seed) = **−0.684**; (points-for, made playoffs) = **+0.671**; (points-for, title) = **+0.288**
- Playoff teams average **1551.9** points; non-playoff **1388.3**
- Champion seeds: **5, 1, 4, 1.** The points leader won **2 of 4.**
- **P(better team wins a single week) ≈ 0.648** — a three-week bracket is close to a coin flip

### 4.2 CALIBRATION GATE — the sim was 46% too dispersed, and `USE_BREAKOUT` is the whole cause

| | real (412 games) | sim as shipped | BREAKOUT off |
|---|---|---|---|
| weekly mean | 105.0 | 93.9 (0.89×) | 92.2 (0.88×) |
| within-team weekly sd | 20.3 | 22.1 (1.09×) | **20.0 (0.99×)** |
| **between-team sd** | **10.1** | **14.8 (1.46×)** | **10.8 (1.07×)** |

`USE_BREAKOUT` was calibrated against **draft displacement**, not against **scoring** (see the comment in
`draft_sim_2026.py`). Applied inside the scorer it is a third variance source stacked on top of the CV gamma
draw and the availability pool. F30's underlying finding (bench outcomes are bimodal) is not challenged —
its *use in the scorer* is. **Every "how much does this pick matter" number in the project is inflated by
roughly 45% at the team level.** Turning it off lands the sim on the real data at 0.99× / 1.07×.

`STREAM` is `{}` in the shipped code, and setting it to the measured values (QB 15.25 / RB 5.43 / WR 6.54 /
TE 5.53) changes **nothing** — starting slots are never empty on a 14-man roster. That measured finding is inert.

### 4.3 The answer: **the two objectives agree. Weakness #1 does not invalidate the board.**

Full 12-team league sim, real schedule, real bracket, both objectives, paired on seed.

| opening | pf14 | Δ vs best | se | E$ | P(title) | rank pf | rank $ |
|---|---|---|---|---|---|---|---|
| **RB-RB-RB** | 1572.4 | 0.0 | — | **253.10** | 0.33 | 1 | 1 |
| WR-RB-RB | 1570.1 | −2.4 | 3.7 | 241.94 | 0.30 | 2 | 3 |
| RB-RB-WR | 1567.6 | −4.9 | 3.5 | 236.66 | 0.29 | 3 | 4 |
| WR-RB-TE | 1564.3 | −8.2 | 3.9 | 233.94 | 0.28 | 4 | 5 |
| RB-WR-RB | 1563.7 | −8.8 | 3.6 | 242.74 | 0.31 | 5 | 2 |
| … | | | | | | | |
| WR-QB-RB | 1543.6 | −28.8 | 4.3 | 227.08 | 0.28 | 11 | 10 |
| WR-WR-WR | 1536.9 | −35.5 | 4.7 | 216.13 | 0.25 | 12 | 13 |
| TE-RB-RB | 1536.5 | −36.0 | 3.6 | 218.48 | 0.26 | 13 | 12 |

**N = 1,250 paired seasons. Spearman(points rank, dollar rank) = +0.852. Spearman(points rank, P(title)) = +0.641.
Same opening tops both.**

Replicated with the calibration fix (BREAKOUT off, N = 750): RB-RB-RB still tops points, WR-RB-RB and
RB-RB-WR statistically tied, TE-RB-RB and WR-WR-WR still last, **Spearman(points, E$) = +0.863,
Spearman(points, title) = +0.879.** The conclusion is not an artefact of the miscalibration.

**Caveat that must travel with this.** In the sim Matt wins ~33–41% of titles, not 8.3%, because opponents draft
by ADP order and never optimise a lineup. Championship equity is therefore being measured in a regime where
he is dominant. Convexity arguments for variance-seeking bite hardest for a *marginal* team, and that regime
is untested. The finding is "no divergence detected for a strong team," not "no divergence exists."

---

## STEP 5 — 2021 ADDED

180 picks parsed cleanly, 12 teams, rounds 1–15, **zero unparsed positions**. Round 1 = keeper (picks 1–12),
same convention as 2022–23. Combined file: `draft_history_2021_2025.csv`, **894 rows, 834 true picks,
60 manager-seasons.**

**Only 6 of 12 2021 team names map to a current manager** — 2021 team names include *Buffalow Expectations*,
*Antonio Gimpshin*, *CeeDee Lambs*, *Charlotte SweatyBallerz*, *Sutton My Face Until I Kareem*. Not guessed.

**Per Matt's instruction (Aug 20): recent years are treated as more reliable. 2021 is used as corroboration
only — it never moves a current estimate. Headline numbers stay on 2022–25.**

### F4 — structure barely moves
| | 2022–25 | 2021–25 |
|---|---|---|
| rounds 1–4 RB/WR share | 0.833 | 0.828 |
| median first TE round | 6 | 6 |
| median first D/ST round | 12 (IQR 11–13) | 12 (IQR 11–13) |
| first K at round 11+ | 0.957 | 0.949 |

**Correction to F4 as written:** the ledger says "TE before round 3: 1 of 43 team-seasons — the sole case is
herman allen, 2025." Recomputing 2022–25 gives **2 of 45**: herman allen (2025) **and Pierce (2023)**, who has
since left the league. 2021 adds a third (*Buffalow Expectations*, Kelce in round 2). The operational claim —
*no current manager except herman allen has ever taken an early TE* — survives; the count in the ledger does not.

### F20 — the TE result is now five-for-five
Through pick 17, by year 2021→2025: **TE 0, 0, 0, 0, 0 (sd 0.00).** QB 0,0,0,1,1. RB 5,4,3,6,9. WR 0,1,2,10,7 (sd 4.30).
Through pick 32: QB 2,2,3,3,3 — still the most trustworthy pace number the model has.

### F18 — persistence is *more* dead, not less
41 consecutive-year manager pairs (was 24–33):

| statistic | yoy r | p | pairs | (four-year value) |
|---|---|---|---|---|
| first QB round | +0.112 | 0.497 | 39 | +0.126 |
| first TE round | −0.009 | 0.957 | 36 | +0.126 |
| **first RB round** | **+0.072** | **0.656** | 41 | **+0.255** |
| first WR round | +0.029 | 0.855 | 41 | +0.047 |
| RB count rds 1–4 | −0.148 | 0.355 | 41 | −0.070 |
| WR count rds 1–4 | −0.047 | 0.769 | 41 | −0.108 |

The one statistic that looked like it might be something (first RB round, +0.255) **falls to +0.072 with more
data.** Directive §5 stays struck.

### F35 residual model — the brief's premise is inverted
The brief says the residual model "currently uses 2024–25 only, n=271." It does not. **`resid.csv` holds 408 rows
from 2022 (130), 2023 (140) and 2025 (138). 2024 is the year that is missing.** The ledger's F35 population line
("This league, 2024–25, n=271") is wrong and contradicts the sim's own docstring. 2021 and 2024 are both
recoverable — 2021 ADP from `Combined_Rankings_rankings_with_adp.csv`, 2024 from the FantasyPros and
FootballGuys 2024 files. **Not done this session.** It is the highest-value remaining backfill.

---

## STEP 6 — TPRR: **NULL.** Tested the same three ways scheme was (F47).

Population: PFF receiving exports, WR/TE/RB with ≥100 routes in both years. Fantasy points are receiving-only,
league scoring. Train 2023→2024 (n=210), test 2024→2025 (n=209).

**Gate 1 — stickiness: PASS.** Pooled yoy r, n=419: TPRR **0.598** (p = 4.7e-42) · YPRR 0.587 · targets/g 0.787 ·
routes/g 0.742 · route_rate 0.901 · aDOT 0.890 · slot_rate 0.844 · route grade 0.541 · PPG 0.734.

**Gate 2 — out-of-sample gain: FAIL.**
baseline (prior-year PPG + position) OOS R² **0.5411** → + TPRR **0.5420** → **delta +0.0009,
bootstrap 95% CI [−0.0003, +0.0020].** Inside noise. YPRR alone: −0.0000. Full block (TPRR + YPRR +
route_rate + aDOT + route grade): +0.0039, still not separable.

**Gate 3 — survives volume control: FAIL.**
prior PPG + targets/game → 0.5504; add TPRR → **0.5502 (−0.0002).**
Partial correlation of TPRR with next-year PPG, controlling prior PPG and targets/game: **r = −0.000, p = 0.997.**
`corr(TPRR, targets/game) = +0.785` — **TPRR is mostly re-measuring volume.**

The raw correlation is seductive: `corr(TPRR_t, PPG_t+1) = +0.580, p = 3e-20`. It is entirely absorbed by
prior-year points and target volume. This is the mirror of the directive's §0 warning — *correlated with the
outcome is not incremental to the projection.*

**→ TPRR joins athleticism, contract year, rookie RB wall, vacated targets, BMI, breakout age, draft-day
handcuffs and offensive scheme. Weakness #13 closes. The pattern in §7 of `00_START_HERE.md` is now
nine-for-nine: every external factor is already priced; everything that survives is structural.**

---

## STEP 7 — WHAT CHANGED, RANKED BY WHETHER IT MOVES A DRAFT-DAY PICK

### Changes a pick
1. **Nothing in the recommended board changes today** — but the **confidence at pick 8 must widen.**
   Only Taylor and Jefferson survive all three projection specifications; St. Brown's edge shrinks
   from +34.3 to +12.4 and reverses to −7.6 under a blended projection. **Best available of
   Taylor / Jefferson / St. Brown / Nacua / Lamb. Never London, Cook, Allen or McBride.**
2. **Every effect size in the project is ~45% too large at the team level** (`USE_BREAKOUT` in the scorer).
   Relative orderings survive; the magnitudes do not. Stop quoting "+X points" as if calibrated.

### Changes what we believe, not what we pick
3. **Weakness #1 is answered and closed.** Week 1–14 points and championship dollars rank the openings the
   same way (ρ = +0.85 to +0.86). The objective in the directive is correct.
4. **TPRR is dead.** Weakness #13 closes.
5. **F18 is stronger on five years.** Directive §5 stays struck.
6. **F20's zero-TE-inside-17 is now five-for-five.**

### Still open, ranked
7. **`picks_with_adp.csv` does not exist in the project. F49 is unreproducible.** F49 set
   `POSADJ_TE_ELITE`, killed the mid-round TE lag, and moved Warren from a pick-41 freebie to a pick-32
   decision. That entire chain currently rests on a file nobody can open.
8. **2024 is missing from `resid.csv`**, and the ledger's F35 population line is wrong.
9. **`top_400`'s provenance is unknown.** Until it is named it is a stress test, not a projection.
10. **Matt has a fourth keeper option nobody tested: Tyler Warren.** F46 compared Pickens, Egbuka and
    Harvey. Warren is TE, VBD +27.8, and under F49 he is a pick-32 problem — keeping him would free
    rounds 3 and 4 entirely. **Untested.**
11. **139 of 195 synthetic projections remain fabricated.**
12. The sim's absolute win rate (33–41% titles) is far too high; opponents never optimise. Fine for ranking,
    useless for absolute equity.

### Top three assumptions, and what would kill each
| assumption | what would invalidate it |
|---|---|
| ESPN's projection is the right spine | a *second* independent projection that also disagrees with ESPN and *also* beats it against the ranker panel |
| the inferred playoff bracket matches the real one | the actual 2022–25 bracket memberships — the file's `Bracket Type` column is empty |
| `USE_BREAKOUT` off is the correct scorer setting | a real-league weekly-score distribution wider than 10.1 between teams, e.g. if 2021 scoreboard data changes the estimate |

**Single missing input that would most improve the analysis:** a second projection with **raw stat lines**
(pass yards, TDs, receptions), so it can be scored to 6-pt passing TDs directly instead of being taken on faith.
`fp_qb_*.csv` and `fp_flex_*.csv` in the Drive `Source` folder are exactly that and are **not in the project.**
