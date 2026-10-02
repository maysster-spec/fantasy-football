# Findings Ledger

Every entry carries **baseline · population · sample size**. A finding without all three is not portable and will be misapplied. Overturned findings are shown with their correction, not silently replaced.

> **⚠ DIRECTIVE CONFLICT — READ FIRST (updated Aug 19, 2026).** Two blocks of the project directive are now contradicted by tested findings. **I cannot edit the directive; Matt must.**
>
> **(a) Section 5 — the per-manager opponent model.** Invalidated by F18 and F21. Strike the "QB timing (avg round of first QB)" line, the "Critical: Ray, Kam and Fleming …" line, and the "TE timing" paragraph. Downgrade §4.12's Snyder q≈0.85 from a calibration to a flagged assumption. Details in `claude/07_model_foundation_audit.md`.
>
> **(b) Section 4.2 — the Josh Allen pick-8 case.** Superseded by **F38**. The directive's "+24.2 ± 2.0 over Henry, best on mean and p10" was produced under a noise model now shown to be wrong (F35) and with a keeper erroneously left in the pool (F37). Rebuilt, Allen is **−18.2 ± 8.7 vs Jonathan Taylor at pick 8 (t = −2.09)** — significantly negative. Replace §4.2's conclusion with: *Allen is not the pick at 8.* Details in `claude/16_adp_refresh_and_noise_reversal.md`.
>
> **(c) Section 4.12 — noise sd.** The directive's original `sd = 0.135 × ADP` was **correct** and should stand. Any note added later saying dispersion is constant is wrong (F35).

> **Numbering note (Aug 19).** F22–F34 were produced in the Aug 18 sim-rebuild and objective-function work and live in `claude/08_adp_calibration.md`, `claude/09_sim_rebuild.md`, `claude/10_strength_of_schedule.md` and `claude/11_corrections_and_challenges.md`. They were never folded into this file. **F23 in particular is now reversed — see F35.** Folding them in is outstanding work.

---

## VALIDATED

### F1 — Replacement levels
`[TESTED]` **Baseline:** none (absolute). **Population:** 200-player ESPN export scored to league rules. **n=200.**
RB30 = 168.0 · WR30 = 168.5 · QB12 = 341.7 · TE12 = 137.7 · Elite VBD: Gibbs +163.5 · Nacua +126.5 · Allen +79.7 · Bowers +53.3. Reproduced twice. **Reproduced a third time Aug 19 on the rebuilt `universe_v2.csv`, exactly.**

### F2 — Consensus divergence
`[TESTED]` **Population:** startable (VBD > 0, non-K/DST). **n=80.**
FantasyPros ECR: TE +18.0 · QB +15.7 · RB +8.1 · WR −8.3 | Boone: TE +23.9 · QB +29.5 · RB +6.4 · WR −7.0 | **ESPN's own board: TE +5.0 mean / −1.5 median · QB +5.5 · RB +8.1 · WR −6.4**
Within-position Spearman (Boone/ECR): RB 0.90/0.94 · WR 0.88/0.93 · TE 0.93/0.94 · **QB 0.76/0.79 weakest.**
**Rule:** RANKINGS MODE edits ESPN's board — use the ESPN row; the FantasyPros TE block move does not apply there. **→ Confirmed six times over by F16, and a seventh time by F36.**

### F3 — Year-over-year stickiness
`[TESTED]` **Baseline:** self, prior season. **Population:** ≥10 RZ targets in both 2024 and 2025. **n=37.**
Inside-10 target volume **r=+0.59, p=0.0001** · RZ target volume +0.51 · RZ target share +0.48 · **RZ TD rate +0.02, p=0.90 → noise.** Rushing: yards before contact r=+0.64 > after contact r=+0.42.
*Re-derived Aug 18 from a clean pipeline: inside-10 r = 0.585, n=37 — exact. Doubles as pipeline validation for F11–F14.*

### F4 — Structural tendencies
`[TESTED]` **Population: true draft selections only, keeper rows excluded.** **n=666 true picks of 714 total, 2022–25; 48 manager-seasons.**
Rounds 1–4 are 83.3% RB/WR · **TE before round 3: 1 of 43 team-seasons** (herman allen, Bowers, pick 22, 2025) · median first TE round 7 · median first D/ST round 12 (IQR 11–13), only 14.6% in rounds 7–10 · first K at round 11+ in 95.8%, median round 14.
**→ Extended by F20: zero TEs inside pick 17 in ALL FOUR years (2022–25), not just 2024–25.** Also: K share of rounds 13–15 has risen 0.25 → 0.25 → 0.38 → 0.46 and D/ST 0.17 → 0.19 → 0.29 → 0.25 — the league pushes both later every year, supporting D/ST at 152 and K at 161.

### F5 — D/ST and K value not realizable
`[TESTED]` **Population:** all executed waiver transactions. **n=935 across 3 seasons.**
D/ST adds 43/76/68 · distinct D/ST 22/31/26 · teams adding ≥1: 11/12/11 of 12. Kickers: 18–28 distinct added/season by 11–12 of 12 teams.

### F6 — ESPN ADP broken for K and D/ST
`[TESTED]` **Baseline:** mean of 5 non-ESPN sources. **Population:** field ADP ≤250 with ≥3 sources. **n≈190.**
Field minus ESPN median: **K +55.0 · D/ST +33.2** · QB +10.7 · TE +4.4 · WR −3.4 · RB −10.8. **→ Exclude K and D/ST from keeper prediction entirely.** *RB −10.8 independently reproduced by F36 at −8.9.*

### F7 — Strategy ranking ⚠ **PARTIALLY SUPERSEDED BY F39**
`[TESTED]` **Baseline:** RB-RB-RB. **Objective:** starting-lineup points weeks 1–14, injury/bye-adjusted. **n=300 paired drafts.**
WR-RB-RB **+6.5 ± 1.9** · WR-QB-RB +2.2 · RB-QB-RB +1.3 · RB-RB-RB 0 · RB-RB-WR −6.4 · RB-WR-RB −20.1 · TE-RB-RB −20.3 · WR-WR-RB −21.3
**Top four span 6.5 points. The robust finding is RB in rounds 2 and 3.** Dead: Zero RB, pop-and-trade, Hero RB.
**⚠ Aug 19: re-run under the corrected noise model (F35) with the keeper bug fixed (F37). The RB-in-2-and-3 finding SURVIVES. The QB-early openings DO NOT — WR-QB-RB falls from 2nd to 12th of 13. Use F39's numbers, not these.**
**⚠ The objective itself is untested against championship equity — weakness #1. Blocked on the weekly-results data request.**

### F8 — Pick-8 decision ⚠ **SUPERSEDED BY F38**
`[TESTED]` **Baseline:** Derrick Henry. **n=400 paired, Snyder q=0.85.**
Josh Allen **+24.2 ± 2.3** · Taylor **+17.4 ± 0.7** · St. Brown **+10.9 ± 1.6** · Achane −1.6
**Sensitivity:** Allen at −5% → +11.8; at −10% → **−0.6.** St. Brown flat at +10.9/+11.1/+11.3.
**Taylor mechanism** (n=1500): 3 WRs in picks 1–7 → 0.01 available; 4 WRs → 0.88.
**⚠ THREE DOWNGRADES:** (a) conditioned on q=0.85, which **F21 undermines**; (b) **F20 shows the WR-count prior is unreliable** — observed WRs through pick 17 were 1, 2, 10, 7; (c) **Aug 19 — the whole table was computed under the wrong noise model (F35), with a keeper left in the pool (F37), and WITHOUT conditioning on availability. Rebuilt: Allen is −18.2 vs Taylor, not +6.8 ahead of him. Use F38.**

### F9 — Pick-32 QB rule rejected
`[TESTED]` **Baseline:** Judkins, both elite TEs removed. **n=350 paired.**
Kyren +3.7 · Adams +0.3 · **Burrow −1.7 · Daniels −5.2 · Warren −7.3.** Take the RB.
**→ Aug 19: independently reinforced by F39** (every QB-early opening now loses) **and by F41** (Daniels 0.88, Hurts 0.82, Burrow 0.69 all survive to 41 — no need to pay at 32).

### F10 — Stafford downgrade
`[TESTED]` VBD +21.1 but ECR 103, Boone 148. **→ Upgraded from 2 rankers to 6 by F16.** If a QB is needed, Burrow at 41, not Stafford at 56.

---

## F11–F14 — SOPHOMORE BLOCK (Aug 18) · full working in `claude/05_sophomore_model.md`

ESPN-independent spine: nflverse `stats_player_week` 2006–2025 + `draft_picks` + `combine`, scored to league rules.

### F11 — Rookie production extrapolates nearly as well as a veteran season
`[TESTED]` **Baseline:** same player, next season. **Population:** drafted RB/WR/TE/QB, rookie season 2006–2024, completed year 2; **no survivorship filter** (no year-2 season = 0 PPG). **n=1,190 rookie records vs 6,407 veteran season-pairs.**
RB **0.665** vs 0.719 · WR **0.723** vs 0.754 · TE **0.636** vs 0.723 · QB **0.701** vs 0.649.
**→ Kills the "year-1 is too small a sample" premise.** Era check 2015–2024: RB 0.672, WR 0.752, TE 0.621 — no era effect.

### F12 — Draft capital is the WEAKER leg; physical archetype is worthless
`[TESTED]` **Baseline:** year-1 PPG alone. **Time-split train 2006–2017 (n=641) / test 2018–2024 (n=411).**
OOS R²: capital only **0.261** · year-1 PPG only **0.505** · both 0.532 · full linear **0.550** · kNN k=40 0.544 · GBM 0.509.
Residual vs draft pick **r=−0.179, p<0.001** (real secondary signal). **Measurables add nothing: weight p=0.34, height p=0.19, forty p=0.32.** Residual vs yards-per-target **r=−0.136, p=0.006** (efficiency regression, tiebreaker only).
Replication at train ≤2019 / test 2020–24 (n=301): 0.527 / 0.537 / 0.243. Same ordering.
**→ Comp sets are for distributions, not point estimates. Do not build or buy athleticism scores.**

### F13 — Sophomore mispricing is a VARIANCE problem, not a bias problem
`[TESTED]` **Baseline:** ESPN ADP vs 4-platform mean. **Population:** skill players, ESPN ADP ≤200, by cohort. **n=115.**
Divergence median: rookie −2.9 · **soph −2.0** · yr-3 −0.7 · vet 0.0 — **KW p=0.85, no directional bias.** But **sd: soph 28.2 vs vet 14.4.**
ECR spread confirms: vet 61 · soph 68 · rookie 185 (KW p=4.3e-06).
Separate: median (ECR rank − ESPN-VBD rank) vet +9 · soph **+29** · rookie +63. **A divergence, not a verdict.**

### F14 — Tuten demotion
`[TESTED]` **Baseline:** ESPN's 187.8 pts / 11.05 PPG. **Population:** rookie RBs, yr-1 PPG 4.5–7.0, picks 70–150, ≥10 g, 2006–2024. **n=21.**
Median yr-2 **5.3 PPG** · **P(≥11.05) = 0.19** · **P(≤5.0) = 0.48.** Sensitivity across six band specs: P(≥11) spans **0.00–0.19** — the headline is the bull case.
**⚠ CONTRARIAN FLAG:** eleven sources place him at 46–67 (five ADP, six rankers, panel 55.8, spread 15). Nobody dissents.
**→ INDEPENDENT SUPPORT (Aug 18):** Jacksonville's Aug 11 depth chart lists **Tuten and Chris Rodriguez Jr. as co-starters** with LeQuint Allen on third downs. PFF (Aug 6) flags Rodriguez for goal-line work. Etienne left for New Orleans and Tuten *still* isn't the clear lead back. **Base rate and current depth chart agree. Co-primary at 56 stands.**
*Aug 19: new ADP has Tuten at 67 and Rodriguez at 181 (up from 200).*

---

## F15–F17 — RANKER PANEL (Aug 18) · full working in `claude/06_ranker_panel.md`

Source: `Yahoo_Top_300_as_of_817.csv`, **captured Aug 17, 2026**; rankers Boone, Smyth, Harmon, Pianowski, Winks, Norris. **Supersedes the Aug 4 Boone file.**
**Data integrity:** `[TESTED]` the file's `AVG` column substitutes a penalty for missing rankers — **149 of 357 rows off by >5, max 131.7, median error 0.0.** Coverage: Norris 306 · Boone 301 · Winks 300 · Pianowski 299 · Harmon 273 · **Smyth 231.** Always recompute as mean-of-available.

### F15 — ESPN rooms over-draft tight ends
`[TESTED]` **Baseline:** ESPN ADP. **Metric:** panel rank − ESPN ADP. **Population:** ESPN ADP ≤200, ≥5 rankers, non-K/DST. **n=164.**
Median gap: **TE +12.7** · QB +3.1 · RB −1.7 · WR −1.7. **KW p=0.0030; TE vs rest p=0.0021.**
ESPN ADP 40–160: **TE +15.1** · QB +5.8 · RB −8.0 · WR −8.4. **Sanity vs 4-platform ADP: TE +6.8 — the effect is ~2× on ESPN.**
Seven of the sixteen biggest ESPN reaches inside ADP 175 are TEs. **Kyle Pitts is a specific pick-56 fade** (ESPN 55, panel 86.3, VBD +7.1, panel sd 5.7).
**Estimate mid-round TE availability from ESPN ADP, never from panel rank.** **→ Third independent confirmation Aug 19: F36 measures +16.7 from mock drafts.**

### F16 — Six-ranker confirmation of F2 and F10
`[TESTED]` **Baseline:** league-scored VBD rank. **Population:** startable, non-K/DST (same as F2). **n=76.**
Cross-position bias, mean(rank − VBD rank): Boone QB +32.4 TE +24.0 · Smyth +20.3/+17.8 · Harmon +25.8/+20.2 · Pianowski +28.6/+18.4 · Winks +25.3/+23.2 · Norris +22.3/+23.4 — **all six, no exceptions.** RB +6.5 to +9.0, WR −4.3 to −6.4. **ESPN's board: QB +7.2, TE +6.0.**
Within-position Spearman: **QB — Winks 0.870 best, Boone 0.747 worst.** RB — Norris 0.950, Winks 0.944. **WR — Smyth 0.885, Harmon 0.797 worst.** TE — all ≥0.939 (n=10).
Stafford all six: ESPN ADP 68 → 148/104/109/115/102/106, panel 114.0, **closest is 34 spots later. F10 confirmed 6-for-6.**
**Panel mean (0.876) beats no individual (best 0.889) — do not average; use the spread.**
> **⚠ CIRCULARITY:** overall agreement-with-VBD is **not a skill ranking** — VBD comes from ESPN's projections. Weakness #9 in a new place. 1st-to-6th spread is 0.056 on n=76. **Do not drop a ranker on this table.**

### F17 — Panel disagreement is a usable uncertainty measure
`[TESTED]` **Baseline:** |panel rank − VBD rank|. **n=76.** **Panel sd vs that distance: r = 0.576, p < 0.0001.** Quartiles 2.7 / 5.0 / 7.2.
The project's first **non-simulated** uncertainty input. **Tiebreaker: within VBD noise, prefer the tighter panel.**
Widest in top 120: Coker 56 · Concepcion 55 · Stribling 52 · Pittman 52 · Golden 50 · Stafford 46 · **Harvey 37.** Tightest: Brooks 4.1 · Stevenson 3.8 · Pitts 5.7.
**→ Aug 19: a SECOND non-simulated uncertainty input now exists — the Mock Wizard `Std Dev` column (F35), which is a dispersion-of-outcome measure rather than a dispersion-of-opinion measure. They are different quantities; do not merge.**

---

## F18–F21 — OPPONENT-MODEL FOUNDATION (Aug 18) · full working in `claude/07_model_foundation_audit.md`

All four run on `draft_history_2022_2025.csv`, **true selections only, keepers excluded. n=666 picks, 48 manager-seasons.**

### F18 — Individual manager tendencies DO NOT persist year to year ⚠ kills directive §5
`[TESTED]` **Baseline:** same manager, previous season. **n=24–33 consecutive-year pairs.**

| Statistic | yoy r | p | pairs | within-mgr var ÷ total var |
|---|---|---|---|---|
| First QB round | +0.126 | 0.531 | 27 | 0.71 |
| First TE round | +0.126 | 0.558 | 24 | 1.08 |
| First RB round | +0.255 | 0.151 | 33 | 1.50 |
| First WR round | +0.047 | 0.794 | 33 | 1.01 |
| RB count rds 1–4 | −0.070 | 0.697 | 33 | 1.54 |
| WR count rds 1–4 | −0.108 | 0.549 | 33 | 1.22 |

**Not explained by draft slot** (slot vs first-QB r=−0.02 p=0.92; first-TE −0.14; first-RB +0.23; first-WR −0.20, all p>0.28). **Slot-residualised yoy stability: QB +0.18, TE −0.03, RB −0.19, WR +0.02, all p>0.5.**
**A manager's own year-to-year spread equals the spread across the whole league.**
**→ Strike directive §5's QB-timing averages, the "Ray/Kam/Fleming are early-QB" line, and the TE-timing paragraph.**
*Caveat: 9–12 pairs after residualising — low power. Read as "no measurable persistence," not proof of none. But §5 asserted persistence without testing it; the burden sits with the claim.*

### F19 — No positional runs exist ⚠ retires weakness #7
`[TESTED]` **Baseline:** within-year permutation null, 4,000 draws. **Population:** picks 1–100, all four years. **n=400.**
P(pick N = pos | pick N−1 = pos) vs base rate: QB 0.071 vs 0.124 (p=0.81) · RB 0.363 vs 0.335 (p=0.15) · WR 0.428 vs 0.435 (p=0.51) · TE 0.090 vs 0.100 (p=0.47).
Rolling 5-pick window variance ÷ binomial: QB 1.01 · RB 1.10 · WR 0.91 · TE 0.96.
**No clustering anywhere; QB slightly anti-clusters. Independent draws is the CORRECT specification, now tested.**
**→ Delete weakness #7 and the standing request to log live pick order for run dynamics. Remaining sim error is in the marginal noise distribution, not the dependence structure. → Aug 19: that remaining error is now identified and fixed (F35).**

### F20 — League pace is stable for TE and QB, volatile for RB and WR
`[TESTED]` **Population:** true selections, 2022–25. Counts through each cutoff.
Through 17: QB 0,0,1,1 (sd 0.58) · RB 4,3,6,9 (sd 2.65) · **WR 1,2,10,7 (sd 4.24)** · **TE 0,0,0,0 (sd 0.00)**
Through 32: QB 2,3,3,3 (sd 0.50) · RB 11,8,14,15 · WR 6,8,15,13 · TE 1,1,0,1
Through 56: QB 4,7,7,6 · RB 19,16,17,24 · WR 16,17,27,21 · TE 4,3,4,5
**→ (a) F8's 68/32 WR-count prior is unreliable — prepare for a 1–2 WR start the sim likely never generates. (b) Zero TEs inside pick 17 in all four years strengthens H2. (c) "3 QBs by pick 32" is the most trustworthy pace number the model has.**

### F21 — NFL-team affinity is at chance ⚠ weakens the Snyder assumption
`[TESTED]` **Baseline:** permutation null over the actual player pool, 2,000 draws. **n=35 consecutive-year manager pairs.**
Jaccard overlap of NFL teams drafted in consecutive years: **observed 0.225 vs null 0.223 (sd 0.015), p = 0.44.**
Raw concentration is a trap — Snyder 10.7% Buffalo looks high against a 1/32 = 3.1% baseline, but herman allen is 16.1% Washington, Kam 16.0% KC and Rychlicki is also 10.7% Buffalo. **Good teams supply more draftable players; 1/32 is the wrong null.**
**→ The Snyder-takes-Allen assumption is n=3 on one player with no supporting general tendency, in a league where neither positional timing (F18) nor team affinity persists. It may still be right, but q=0.85 is overconfident.**
*Aug 19 update: the old note here said a lower q "strengthens the max-floor (St. Brown) branch." Under F38 that framing is obsolete — **Allen is now negative at pick 8 at q=0.85**, and lowering q makes him MORE available, which makes taking him at 8 look better only if the projection is right. The sensitivity that matters is now the projection, not q.*

---

## F35–F38 — ADP REFRESH AND NOISE REVERSAL (Aug 19) · full working in `claude/16_adp_refresh_and_noise_reversal.md`

Sources ingested: `FantasyPros_2026_Overall_ADP_Rankings.csv` (663 rows) and `Fantasypros_Mock_Draft_wizard_Simulator_Sheet1.csv` (367 rows, carries **Std Dev** and **% Drafted**). **Neither carries a capture date; the ADP file demonstrably predates Aug 16** (still has Jeremiyah Love at 15, post-injury). Every entry below inherits that flag.

### F35 — Pick dispersion IS proportional to board rank ⚠ **REVERSES F23**
`[TESTED]` **Baseline:** observed sd of (actual pick − available-board rank). **Two independent populations.**

| Source | Population | Fit | r |
|---|---|---|---|
| This league, 2024–25 | **n=271** true picks, \|resid\| ≤ 60 | **sd = 0.1255 × rank + 5.31** | **0.991** |
| FantasyPros Mock Wizard | **n=41** players with untruncated ranges (avg pick ≤ 70) | **sd = 0.1261 × ADP + 1.38** | 0.908 |
| Directive §4.12 (original) | — | sd = 0.135 × ADP | — |

Standardising the real-league residuals by the fitted line gives z-sd of **0.93 / 1.03 / 1.02 / 1.03** across the four rank bands — the proportional form removes essentially all heteroskedasticity.

**Why F23 was wrong.** F23 saw sd = 25.5 at ranks 1–12 and concluded the relationship was non-monotone. That 25.5 is **two observations**: +123 (Kam, TE, 2024) and +126 (Lobsinger, RB, 2025). Drop them and the band's sd is **4.89**, on the line; the other 26 residuals run −3 to +23.

**Those two outliers are a separate, real mechanism** — a player whose ADP has not absorbed news. Rate: **7.1% at rank 1–12**, **4.3% at rank ≥121**, **0.0% in between (n=177)**. Now modelled as a distinct shock rather than smeared into every pick's variance. *Live instance: Jeremiyah Love, §F36 note.*

**Every downstream use of F23, enumerated (directive §3 rule):** `NOISE_SCALE=0.85` and the three-band bootstrap → replaced · `build_surv()` → rebuilt · every survival number in `03_draft_board` → rebuilt · **F7** → re-run · **F8** → re-run (see F38) · **weakness #9 → CLOSED, the noise model is now fitted.**

**Calibration honesty:** the sim's realised displacement now matches observed sd to within 3% for board ranks 1–120 but runs **19% too noisy past rank 121**. Late-round survival numbers are therefore **lower bounds**, consistent with directive §7.

### F36 — The mock population independently reproduces the TE lag
`[TESTED]` **Baseline:** ESPN ADP. **Metric:** FantasyPros mock avg pick − ESPN ADP. **Population:** both present, avg pick ≤ 180. **n=143.**

TE **+16.7** (n=12) · QB **+12.2** (n=14) · WR −0.7 (n=58) · RB **−8.9** (n=50)

The TE value lands on the sim's fitted `POSADJ['TE'] = +16.0` from a completely independent source. **H2 (+15) and F15 (+12.7 / +15.1) now have a third leg.** RB −8.9 matches F6's field-minus-ESPN RB −10.8.

**Do NOT adopt QB +12.2 for this league** — that is the general mock population; this league has four managers whose first QB averages round 2.5–3.2. `POSADJ['QB']` left at +2.0. *That value now rests on §5 averages which F18 showed do not persist — it is the weakest assumption in the rebuild.*

**Live stale-board instance:** Love is ESPN 15 / mock 28.1 (low 127, sd 5.94) — a ~13-pick fade against an RB baseline of −8.9, i.e. **~22 picks relative to position**, on a high-ankle sprain reported Aug 16. `[SOURCED: NBC Sports, NFL.com, CBS Sports, Aug 16–18 2026]`

### F37 — A keeper was never removed from the pool ⚠ error, not a finding
`KEEPERS` listed `'Travis Etienne'`; the universe lists `'Travis Etienne Jr.'`. Removal is `isin(KEEPERS)`, so he silently stayed — pool 483 where it should be 482. An extra RB (219.7 projected, board rank ~45) was available at picks 41 and 56 in **every simulation run before Aug 19**.

**Fifth name-join failure in this project, and the first the row-count assertion could not catch** — the row count was *supposed* to change. `integrity.py` now carries `assert_keepers_removed()`, which fails if any keeper name does not resolve to a universe row.

### F38 — Pick 8 rebuilt, conditioned on availability ⚠ **SUPERSEDES F8**
`[TESTED]` **Baseline:** Jonathan Taylor. **Objective:** starting-lineup points, weeks 1–14. **Paired, and conditioned on both players actually being available at pick 8 — F8 was not.** Snyder q=0.85.

**Availability at pick 8 (N=900):** McBride 1.00 · Henry 0.98 · Love 0.96 · Jeanty 0.95 · **Allen 0.95** · Barkley 0.91 · London 0.89 · Cook 0.82 · Achane 0.76 · Jefferson 0.60 · **Taylor 0.59** · Lamb 0.47 · **St. Brown 0.43** · Nacua 0.22

| Candidate | n both | vs Taylor | se | t |
|---|---|---|---|---|
| **Amon-Ra St. Brown** | 200 | **+34.3** | 15.9 | **+2.16** |
| CeeDee Lamb | 232 | +8.1 | 13.6 | +0.60 |
| Drake London | 466 | −3.5 | 9.5 | −0.37 |
| Puka Nacua | 110 | −5.6 | 18.1 | −0.31 |
| Derrick Henry | 517 | −7.9 | 2.6 | −3.02 |
| De'Von Achane | 382 | −10.1 | 3.2 | −3.17 |
| Justin Jefferson | 294 | −11.4 | 11.5 | −0.99 |
| Saquon Barkley | 476 | −15.6 | 2.1 | −7.58 |
| James Cook III | 415 | −16.9 | 2.9 | −5.86 |
| **Josh Allen** | 497 | **−18.2** | 8.7 | **−2.09** |
| Ashton Jeanty | 498 | −20.0 | 2.6 | −7.61 |
| Jeremiyah Love | 504 | −21.8 | 7.8 | −2.80 |
| Trey McBride | 528 | −29.2 | 8.6 | −3.42 |

**St. Brown, Lamb, London, Nacua, Taylor and Jefferson are statistically indistinguishable** — every pairwise |t| among them is under 2.2. **Clearly worse:** the mid-tier RBs (Barkley, Cook, Jeanty, Achane, Henry), **Josh Allen**, **McBride**.

**Do not read St. Brown's +34.3 as a computed answer** — se 15.9 on n=200 is a lean. The usable rule is: *best available of St. Brown / Nacua / Lamb / Taylor / London; never Allen, McBride, or a mid-tier RB.*

### F39 — Opening rebuilt ⚠ **partially supersedes F7**
`[TESTED]` **Baseline:** best opening. **Paired, N=700.** Same objective.

RB-RB-RB **1520.4** · RB-RB-WR −4.9 · WR-RB-WR −10.9 · QB-RB-RB −15.0 · WR-RB-RB −16.7 · WR-RB-TE −18.8 · RB-WR-RB −21.6 · WR-WR-RB −25.2 · RB-QB-RB −25.2 · WR-TE-RB −31.6 · TE-RB-RB −37.2 · **WR-QB-RB −45.2** · WR-WR-WR −49.5 (se ≈ 7–8 throughout)

**SURVIVES:** directive §4.10's robust claim — **RB in rounds 2 and 3**. All three top openings have it; every opening that breaks it loses.
**REVERSES:** **QB-early openings collapse.** WR-QB-RB was 2nd in F7 (1448.7) and is now 12th of 13. Under the corrected noise model Daniels (p41 = 0.35), Hurts (0.48) and Burrow (0.69) reliably reach pick 41 — a round-2 QB pays for something that arrives free.
**Apparent tension with F38 resolved:** F38 ranks *players*, F39 ranks *positions*. The RB slot at 8 takes Taylor whenever he is there (59%), and Taylor vs St. Brown is a 2σ call. **Round 1 is a near-tie on position; rounds 2 and 3 are not.**

### F40 — The ADP refresh barely moves the board
`[TESTED]` **Baseline:** prior `ADP_PPR_with_ESPN_column.csv`. **Population:** universe rows inside top 200 on either board. **n≈200.**
**Median absolute shift 2.0 picks; mean −1.6.** Largest top-30 move is Omarion Hampton 19 → 25. Only movers over ±20: Diggs 165→121, Gadsden II 216→158, Lemon 105→128, Spears 193→173, plus four deep WRs.
**Directive §2.1(c)'s depletion table survives unchanged** — only pick 32 moves 37 → 38 and pick 89 moves 99 → 100.
**Join quality:** 439/494 matched, **zero unmatched inside old ADP 250**, no team or bye disagreements inside ADP 200, all four F1 replacement levels reproduce exactly, full harness passed.
**→ The user's expectation that the fresher ADP "might change things" is not supported. What changed the board was the noise model (F35), not the ADP.**

### F41 — The 32 → 41 cliff is steeper than the directive states
`[TESTED]` **N=4,000 simulated drafts, keepers removed before pick 1.** `eff` = board rank after keeper depletion.
Every RB with eff rank ≤ 32 has **p41 ≤ 0.08**. The live board at pick 32 is: **Bowers 0.87 · Daniels 0.88 · Irving 0.83 · Hurts 0.82 · Judkins 0.82 · McBride 0.66 · Lamar 0.59 · Kyren 0.59 · Egbuka 0.36.** At 17: McBride 1.00 · Bowers 1.00 · Walker 0.78 · Henry 0.65 · Love 0.39 · Jeanty 0.31 · Cook 0.30 · Barkley 0.24 · Taylor 0.13 · **Allen 0.11**.
**→ Directive §2.1's "17→32 is the longest gap, 32→41 has the steepest attrition" is confirmed and the attrition is worse than the listed numbers.** Simulated; treat as lower bounds.

---

## HYPOTHESES

### H1 — Vacated opportunity unpriced
`[TESTED for pricing, UNTESTED for predictiveness]` **n=80 WR/TE, 51 RB.** Vacated target % → projected target change r=+0.21 p=0.067; vacated carry % → r=+0.07 p=0.61. **Tiebreaker use only.**

### H2 — TE lag magnitude — **NOW EFFECTIVELY CONFIRMED**
Fitted **TE effective ADP +15 picks** (SSE 4.1 of four models). **→ Aug 19: F36 measures +16.7 from a fully independent population (FantasyPros mock drafts, n=12 TEs), landing on the sim's fitted POSADJ of +16.0.** With F15 (+12.7 / +15.1) and F20 (zero TEs inside pick 17 in all four years), this now has four legs from three independent data sources. **Promote to VALIDATED at the next ledger pass.**
Bowers at 32 now reads **0.87** on the corrected model (was a 0.25–0.97 span); Warren at 41 reads **0.95**.

### H3 — RB and WR pace
Left uncorrected on 2 drafts. **→ F20 gives four years and shows the variance is much larger than assumed. → Aug 19: F36 supplies an external RB estimate of −8.9 (mock minus ESPN), consistent with F6's −10.8. The sim still carries no RB adjustment. Fitting it properly is blocked on historical ADP.**

### H4 — RJ Harvey *(arbitrage claim WITHDRAWN)*
ESPN ADP **118** (new file: **126**) · six-expert panel **106.5** · Sleeper/CBS/RTSports/Fantrax **69.8** · **FantasyPros mock avg 81.8 (Aug 19)**.
**The experts side with ESPN; the drafting platforms are the outlier. The mock population is a fourth source and it sides with the platforms, not the experts — but a mock draft is a drafting behaviour, not an evaluation, so it does not restore the arbitrage claim.**
**Survives:** availability is well supported (ESPN 126 *and* panel 106.5 both say he reaches 113); model read unchanged (+51.4 relative; comp n=22, median yr-2 10.3 PPG vs ESPN's 8.38, P(clear)=0.68); clearly better than Monangai.
**Complication:** **J.K. Dobbins is Denver's lead back**, Harvey the primary backup. **Contingent-value pick — fine at 113, not what the board implied.** Panel spread 37 → low confidence per F17.

### H5 — Fannin upgrade — SURVIVES
Model 157.0 pts → **VBD ≈ +19.3, not +8.0.** Rookie TE: 107 tgt / 72 rec / 731 yds / 6 TD at pick 67. Comp set n=2 — ignore; the regression carries this.
Panel: ESPN ADP 66 vs panel 81.5 = +15.5, **almost exactly the TE positional median.** No player-specific fade.
Cleveland's Aug 15 depth chart has **Fannin as TE1**; Njoku left for the Chargers. **Stays above Tuten.**
**Aug 19: new ADP has him at 65; corrected survival gives p65 = 0.71, p80 = 0.16.** Per F15/F36 do not reach past ADP 65.

### H6 — Reach-vs-ADP may persist where timing does not *(blocked on data)*
F18 kills per-manager *timing*. But **mean reach-vs-ADP** is a different and more plausibly stable statistic, measured on a continuous scale. **The only way to rebuild a per-manager model on a tested foundation. Blocked on historical ADP for 2022–2025.**

### H7 — The 2026 board carries at least one live "stale ADP" player *(new, Aug 19)*
F35 measures the stale-board rate at **7.1% for board ranks 1–12** and **4.3% for ranks ≥121**, **0.0% in between**. On a 12-keeper-depleted board that predicts roughly **one top-12 player and two-plus late players whose ADP will be badly wrong on draft night.** Jeremiyah Love is the identified top-12 case. **Actionable form: at picks 8 and 17, expect one player to be available who "should not" be, and treat that as news rather than value.** Untestable in advance; check it at T-60min.

---

## REJECTED — tested and killed

| Claim | Result |
|---|---|
| WOPR / air-yard share carries unpriced signal | Partial r=+0.16, p=0.17 after controlling for raw targets |
| Year-3 WR age breakout | r=+0.04, p=0.77, n=57 |
| Boone's Derrick Henry fade | All pick-17 alternatives lose: Jacobs −5.5 … Love −15.5 |
| Josh Allen "only worth considering at 32 or later" | Survival to 32 = 0.01 |
| Take the QB at 32 if both elite TEs are gone | F9, reinforced by F39 and F41 |
| Jeremiyah Love at pick 17 | −10.2 vs Henry; **and now −21.8 vs Taylor at pick 8 (F38), plus a high-ankle sprain** |
| "Year-1 production is too small a sample to extrapolate" | **F11.** Rookie 0.64–0.72 vs veteran 0.65–0.75 |
| Physical archetype predicts sophomore outcomes | **F12.** p = 0.19–0.34 on the residual |
| kNN comp sets beat regression as a point estimate | **F12.** 0.544 vs 0.550 on identical inputs |
| Rookies' RZ usage far less sticky than veterans' | Fisher Z=−1.38 p=0.17, range-restricted. **Superseded by F11** |
| "RJ Harvey is a 48-spot ESPN arbitrage" | **WITHDRAWN. H4.** |
| Averaging the six-ranker panel improves on individuals | **F16.** 0.876 vs best 0.889 |
| **Managers have stable, modellable positional tendencies** | **F18.** No persistence at any position, before or after controlling for slot |
| **Positional runs / panic dynamics drive this draft** | **F19.** No clustering at any position. Weakness #7 retired |
| **Snyder has a general Bills / NFL-team affinity** | **F21.** Team overlap is at chance (p=0.44) |
| **"Pick dispersion is constant at 16–24 picks regardless of board position" (F23)** | **F35. WRONG. Two outliers drove it. Dispersion is proportional, slope ~0.126, confirmed by two independent populations** |
| **Josh Allen at pick 8** | **F38.** −18.2 ± 8.7 vs Taylor, t = −2.09. The original +24.2 came from the broken noise model, an unremoved keeper, and no availability conditioning |
| **QB-early openings (WR-QB-RB, RB-QB-RB)** | **F39.** WR-QB-RB falls from 2nd to 12th of 13 (−45.2). Elite QBs reach pick 41 |
| **"A fresher ADP snapshot will move the board"** | **F40.** Median absolute shift inside the top 200 is 2.0 picks |

---

## ERROR LOG

| Error | Root cause | Caught by |
|---|---|---|
| Ranked strategies by total roster VBD | Objective undefined | Self |
| Greedy policy inflated WR-vs-RB gap to +43.6 (true +8.6) | Policy under-drafted WR | Self |
| Keeper rows counted as draft picks | Population not specified | Self |
| "Four managers took a TE before round 3" — three were keepers | Population not specified | Cross-check |
| ESPN ADP used to rank K/DST keepers after being proven broken | Finding not propagated | **User challenge** |
| Boone rankings file unused for weeks | No inventory step | **User challenge** |
| Board listed 15 picks including 176 | Directive wording | **User challenge** |
| Depletion mechanic re-explained to three models | Directive silent | **User challenge** |
| Draft capital sat unused in the depth-chart file for 10 days | No inventory step (2nd occurrence) | Self, Aug 18 |
| Travis Hunter dropped from a join — trailing `CB` broke the regex | Name-based join (1st) | Self, Aug 18 |
| Called a 4-platform ADP average "the field" and declared a 48-spot Harvey arbitrage | One source class treated as the whole market | **User-supplied data, Aug 18** |
| Ranker join produced 405 rows from 357 — "J. Williams" matched Javonte and Jameson | Key lacked position and team (2nd) | Self, Aug 18 (row-count assert) |
| 37 players silently dropped — ESPN glues injury flags to the name (`Alec Pierce O IND WR`) | Name-based join (3rd); skewed WR replacement 10 pts low vs RB 2.8, biasing every RB-vs-WR comparison | Self, Aug 18 |
| §5's per-manager opponent model built and used for weeks without testing whether manager behaviour persists | Stability assumed, never measured | **User challenge, Aug 18** |
| Claimed the elite-TE lag was +4.3 from n=3 and told the user Bowers/Warren were much less available than the board said | Conclusion from three observations | Self, Aug 18 (re-fit gave +16) |
| Abandoned the 2024 ADP data requirement after two failed fetches | Misapplied the "stop after 2–3 failures" rule to a *data requirement* rather than a repeated identical action | **User challenge, Aug 18** |
| Over-valued streaming by ~25% | Assumed rather than measured; 951 real adds gave QB 15.25 / RB 5.43 / WR 6.54 / TE 5.53 | Self, Aug 18 |
| First QB system-change pass compared movers vs stayers and called a shared improvement a "bounce-back" | No stayers-only baseline curve | **User challenge, Aug 18** |
| **Replaced a correct proportional noise model with a constant one, on the strength of two outlier observations, and carried it into every survival number, the strategy ranking and the pick-8 decision** | **Band statistic read without inspecting the underlying points; n=28 in the deciding band** | **Self, Aug 19 — but only because the user supplied the Mock Wizard file, which disagreed** |
| **`'Travis Etienne'` vs `'Travis Etienne Jr.'` left a keeper in the draft pool for the whole session** | **Name-based join (5th). Row-count assert could not catch it — the row count was supposed to change** | Self, Aug 19 (`assert_keepers_removed` added) |
| **Ran the pick-8 comparison without conditioning on the candidate actually being available at pick 8** | Paired design applied to the wrong estimand — "Nacua at 8" was really "Nacua 22% of the time, greedy otherwise" | Self, Aug 19 |

**Standing rules:** (1) When a finding invalidates a metric, enumerate every downstream use. (2) Every finding carries baseline, population, sample size. (3) Inventory every project file before analysis. (4) Join on `gsis_id`/`pfr_id`; otherwise key on name + position + team and **assert output rows == input rows.** (5) Never call one source class "the field" — name the sources. (6) Check any supplied consensus/average column against a recomputation. (7) Before modelling any per-entity tendency, test that the tendency persists. (8) **A data requirement is not closed until five distinct sources have been attempted and named.** (9) **NEW — before overturning a finding on a band or group statistic, print the underlying observations. Two points moved F23.** (10) **NEW — any paired simulation comparison must condition on the treatment actually being deliverable.**

---

## KNOWN WEAKNESSES, RANKED

1. **Objective stops at week 14.** Playoffs are 15–17; first place is 44% of the pot. **Blocked on league weekly-results data — request #3.** *(Partially probed: points→dollars ρ=0.74 but points→titles ρ=0.26; the pick-8 ordering was robust to the swap.)*
2. **~~No run dynamics.~~ RETIRED by F19.**
3. **The per-manager opponent model is dead (F18) and nothing replaces it.** H6 is the candidate; **blocked on historical ADP — request #1.**
4. **Snyder q=0.85 is overconfident (F21).** Less load-bearing than it was — under F38 Allen is negative at 8 regardless.
5. **The Allen case rests on one projection**, ±7% band. **Now the dominant sensitivity, having displaced q.**
6. **~~Bowers at 32 spans 0.25–0.97.~~ NARROWED by F41 to 0.87** on the corrected noise model.
7. **Survival numbers are simulated, not observed** — lower bounds. **Quantified Aug 19: matched to within 3% of observed dispersion for board ranks 1–120, but 19% too noisy past rank 121.**
8. **One projection source for everything.** Partly addressed by the nflverse spine; still needs a **historical ESPN projection archive — request #2.**
9. **~~The sim's noise model is one Gaussian sd for all positions, never fitted.~~ CLOSED by F35** — fitted to 271 real picks (r=0.991) and cross-checked against 41 mock-draft players.
10. **`POSADJ['QB'] = +2.0` rests on §5 averages that F18 showed do not persist** *(new, and it is now the weakest live assumption)*. The mock population says +12.2. Resolvable by fitting QB pace against ADP on `draft_history_2022_2025.csv` — **request #1 again.**
11. **Never built:** offensive line quality (PFF pull #3), coaching/scheme changes beyond the team-change analysis, rookie target competition, playoff-week matchups.
12. **Circularity:** ESPN projections → VBD, ESPN ADP → opponent model, then concluding ESPN diverges from VBD. Resolvable via the nflverse spine; not yet done.
13. **No route participation / TPRR** — the one variable class nflverse lacks. Blocks real tests of H5 and F14.
14. **F22–F34 were never folded into this ledger** *(new)*. They live in their source docs and are not portable to a new session in the form the directive requires.

---

## SOURCE INVENTORY AND CAPTURE DATES

| Source | Captured | Status |
|---|---|---|
| **`FantasyPros_2026_Overall_ADP_Rankings.csv`** | **no capture date; demonstrably pre-Aug 16** | **CURRENT board source. Supersedes `ADP_PPR_with_ESPN_column.csv`. Re-export Sep 5 and record the date** |
| **`Fantasypros_Mock_Draft_wizard_Simulator_Sheet1.csv`** | **no capture date** | **CURRENT. The project's only external dispersion measurement (F35). Std Dev past avg pick ~70 is truncation-contaminated — use the ≤70 subset only** |
| `Yahoo_Top_300_as_of_817.csv` (6 rankers) | **Aug 17, 2026** | current |
| `Boone_Rankings_HalfPPR_20260804.csv` | Aug 4, 2026 | superseded |
| `ESPN_projections_in_my_League.csv` | **no capture date** | **still the sole projection source. Re-export Aug 24 and Sep 5** |
| `ADP_PPR_with_ESPN_column.csv` | no capture date | **superseded Aug 19** |
| `FantasyPros_ECR_BestWorstStdDev.csv` | no capture date | re-export |
| `draft_history_2022_2025.csv` | — | 714 rows, 666 true picks. Verified |
| `keeper_eligibility_VERIFIED.csv` | — | authoritative for eligibility |
| nflverse weekly stats 2006–2025, `draft_picks`, `combine` | Aug 18, 2026 | free, re-pullable |
| Injury / depth-chart scan | **Aug 19, 2026** (Love) | re-run Sep 5 |
| **Historical ADP 2022–2025** | **NOT IN PROJECT** | **request #1 — highest value; unblocks H3, H6 and weakness #10** |
| **ESPN projection archive** | **NOT IN PROJECT** | request #2 |
| **League weekly lineups/results 2022–2025** | **NOT IN PROJECT** | request #3 — unblocks weakness #1 |
| PFF routes / TPRR / YPRR 2023–2025 | not yet pulled | request #4 |
| 2021 rankings/ADP files | uploaded | **worth zero without 2021 ESPN draft results. Supply them or drop the files** |

---

## F42–F47 — AUDIT BLOCK (Aug 19) · full working in `claude/17_audit_names_projections_scheme.md`

### F42 — 39% of the projections in the universe are fabricated ⚠ error
`[TESTED]` **Baseline:** the 200-row `ESPN_projections_in_my_League.csv`. **Population:** all 494 rows of `universe.csv`. **n=494.**
299 rows carry real ESPN projections. **195 do not** — they were filled with a linear ramp. Synthetic rows are identifiable by a non-2-decimal `TOT` and by constant consecutive differences: WR step 0.608 (sd 0.660, n=85) · TE 1.281 (0.777, n=57) · QB 4.260 (0.673, n=38) · **RB 3.4485 (sd 0.0000, n=15)** — eight RBs clamped to the identical value 28.84.
**Every synthetic row has ADP ≥ 157.6, median 355.** Damage is contained: the last flexible pick is 137 (effective ADP ~149), and only **3 of 28 board-recommended players** are affected (Gadsden II, Ja'Kobi Lane, Dalton Schultz). All four F1 replacement levels and every tier ladder come from the real 299.
**→ `universe_v3.csv` now carries a `synthetic` boolean. Never rank on a synthetic row. Export more rows from ESPN at the Aug 24 refresh.**

### F43 — A canonical player-ID crosswalk exists, is free, and resolves the whole board
`[TESTED]` **Source:** DynastyProcess `db_playerids.csv`, 12,472 players, maps `gsis_id · espn_id · pff_id · fantasypros_id · sleeper_id · yahoo_id · cbs_id · pfr_id · mfl_id`.
Resolution: universe skill players **418/421 (99.3%)** · **draftable board slots 1–168: 144/144 (100%)** · ESPN export 174/176 · FantasyPros 2026 ADP 544/572. Unresolved are all ADP 400+.
**Zero team disagreements inside ADP 180** — independently confirms the 2026 moves (Waddle→DEN, DJ Moore→BUF, Tate→TEN) that looked wrong on inspection.
**Trap:** name-only keys collide *inside the canonical file itself* — there is an LB named Justin Jefferson and a CB named Lamar Jackson. **Key on name + position, always.**
**→ Five name-join failures (Hunter, J. Williams, injury flags, team-changers, Etienne Jr.) are now structurally impossible. `universe_v3.csv` carries the IDs; join on `gsis_id` from here.**

### F44 — The scoring formula is verified for the first time
`[TESTED]` **Population:** 176 skill players in the ESPN export.
Recomputing `TOT` under **passing 0.04/yd, 6-pt passing TD, −2 INT, rush/rec 0.1/yd, 6-pt TD, 0.5 PPR** reproduces ESPN's value to **mean −0.81, median −0.60, sd 3.05**. The residual is the fumble-lost penalty, absent from the export's columns — which is why the gap is ~−8 on QBs and ~−0.5 on receivers. **4-pt passing TD misses Josh Allen by 52; 1.0 PPR misses Nacua by 63.** League scoring confirmed correct.

### F45 — Keeper-prediction uncertainty is NOT material
`[TESTED]` **Baseline:** the predicted keeper set. **Population:** 53 eligible players across 12 teams, K/DST excluded per F6. **n=25 randomised keeper sets × 400 drafts.**
**8 of 12 predictions have a runner-up within 30 ADP picks** (Ray 10 · Matt 13 · Grenier 14 · allen 16 · Fleming 22 · Brown/Collins 27 · Taylor 27 · Cary 27). That looked like the project's largest unquantified risk.
It is not. Across randomised sets, survival probabilities move only **±0.03–0.08**: Taylor p17 0.13 [0.10–0.17] · Henry 0.65 [0.62–0.68] · Bowers p32 0.87 [0.82–0.89] · McBride p32 0.68 [0.60–0.72]. Widest bands are **Egbuka p32 0.37 [0.28–0.58]** and **Kyren p32 0.62 [0.56–0.76]**. **No decision flips.**
*Assumption, stated not fitted: P(team takes its lowest-ADP eligible) = 0.5 + 0.5(1 − e^(−margin/25)). There is no data to fit it — the only evidence is 3-for-3 on n=3.*

### F46 — Matt has a keeper CHOICE; keep Pickens, but for the option value, not the projection
`[TESTED]` **Baseline:** George Pickens. **Paired sim, N=700, identical board and injury draws.**
Pickens 1519.7 · **Egbuka −2.72 ± 4.65 (t = −0.58, tie)** · **RJ Harvey −55.88 ± 7.65 (t = −7.31, clearly wrong)**
The projections are 4.5 points apart (Pickens 199.1 / Egbuka 194.6) and the keeper costs round 15 either way, so pick cost does not differentiate them. **The asymmetry does:** keep Pickens → Egbuka is still there at pick 32 **35%** of the time; keep Egbuka → Pickens is there **5%** of the time.
**→ Keep Pickens. But the directive states him as fixed when he is in fact a decision, and the margin over Egbuka is inside noise.**

### F47 — Offensive scheme fails all three gates ⚠ do not build it
`[TESTED]` **Data:** nflverse 2022–2025 — `pass_oe`, `pbp_participation.offense_personnel` (100% coverage 2022–25), `ftn_charting.is_motion` / `is_play_action`, shotgun / under-centre / no-huddle. **6 of 8 indicators in the taxonomy are measurable for free.** Not measurable anywhere public: **condensed vs wide splits** (no alignment field exists — needs tracking data, PFF or SIS) and **motion at the snap** specifically.

**Gate 1 — stickiness** (team yoy, n=96 pairs): 7 of 12 pass pooled (motion 0.75 · shotgun 0.62 · under-centre 0.55 · no-huddle 0.53 · PROE 0.48 · 11-personnel 0.44 · time-to-throw 0.41; heavy 0.35, play-action 0.31, box 0.28, pressure 0.26, screen 0.18 fail). **Split by play-caller retention, only `motion_rate` survives a coaching change (0.653, n=20)** — the other six collapse to ~0 or negative. Stickiness is "same coach, same behaviour," not a team property.

**Gate 2 — predictive value** (706 player-pairs ≥8 games both years; train 2022→23 + 2023→24, test 2024→25): baseline (prior-year PPG + position) OOS R² **0.7145** → with scheme **0.7148**, **delta +0.0003, 95% CI [−0.011, +0.012]. Inside noise.** Three coefficients appeared significant (shotgun p=0.010, under-centre p=0.002, time-to-throw p=0.017) — a **collinearity artifact**: shotgun and under-centre correlate at **r = −0.944** and each is null alone (p=0.66, p=0.19). Changed-team subgroup delta +0.0154, CI [−0.042, +0.077], n_test=49 — untested, not disproven.

**Gate 3 — already priced:** adding team offensive volume makes the scheme delta **negative (−0.0016)**. Volume adds nothing either. Prior-year PPG + position absorbs all of it.

**→ Joins the rejected list with athleticism (F12), contract-year, rookie RB wall, vacated targets, BMI, breakout age and draft-day handcuffs. The pattern is now unmistakable: almost every plausible external factor is already priced, and everything that has survived in this project is STRUCTURAL — keeper depletion, positional pace, tier cliffs, the noise model. That is where the remaining edge is.**
*Caveat: this tests scheme's effect on a player's own points. It does NOT test whether scheme predicts which of two similar teammates gets the volume — a within-team allocation question, different and harder.*

### F48 — Tiers are now computed, not inferred
`[TESTED]` **Method:** optimal 1-D k-class natural breaks (Jenks DP, minimising within-class SSE) on league-scored projected points within position, k = 10 (RB/WR) or 7 (QB/TE), over the top 64/76/26/26.
Result reproduces three established findings independently: **TE Tier 1 = Bowers + McBride ONLY** (§4.3) · **QB Tier 1 = Josh Allen alone** (§4.2's cliff) · **RB Tier 1 = Gibbs, Bijan, McCaffrey, Taylor**, then an 11-man Tier 2 (Henry → Chase Brown) — which is exactly why pick 8 and pick 17 are near-ties. **WR Tier 1 = Nacua alone.**
**→ Rendered in the draft-board artifact. Rule: never reach across a tier; always take the last player in a tier before a long gap.**

### F49 — The TE +16 lag is real ONLY for elite TEs ⚠ corrects H2 and the sim
`[TESTED]` **Baseline:** ESPN ADP. **Metric:** actual pick − ESPN ADP. **Population:** true selections 2022–2025 with ADP joined, **n=512.** *(All four years of ADP were already in the project — see the correction note below.)*

| Population | n | median lag | mean |
|---|---|---|---|
| **TE, ADP ≤ 40** | **8** | **+14.9** | +24.2 |
| TE, ADP 1–60 | 19 | +3.0 | +11.6 |
| TE, ADP 61–120 | 24 | **−3.7** | −3.4 |
| TE, all | 63 | **0.0** | −2.2 |
| QB, all | 68 | −0.1 | −3.5 |
| RB, all | 170 | −1.5 | −1.8 |
| WR, all | 211 | +1.0 | +1.8 (unstable by year: +5 / +20 / −2 / −2) |

**H2's +15 survives, but only at the top of the board.** The eight elite TEs: Kelce 14→30, Pitts 35→37, Kelce 6→20, Andrews 28→46, Kelce 24→41, Bowers 19→22, Kittle 35→35 (plus a Taysom Hill ADP-4→pick-128 outlier, a stale-board case per F35).

**The sim was applying +16 to EVERY tight end.** That is a population error — the directive's own rule, "filter to the population that matters," applied backwards. Corrected to `POSADJ_TE_ELITE = (ADP ≤ 40, +16)`.

**Board impact — mid-round TE survival was badly overstated:**

| player | ADP | p41 old | p41 new | p65 old | p65 new | p89 old | p89 new |
|---|---|---|---|---|---|---|---|
| **Tyler Warren** | 42 | 0.95 | **0.15** | — | 0.00 | — | — |
| Sam LaPorta | 55 | 0.97 | 0.72 | — | 0.05 | — | — |
| Kyle Pitts Sr. | 56 | 0.98 | 0.75 | — | 0.05 | — | — |
| Harold Fannin Jr. | 65 | — | 0.90 | **0.71** | **0.19** | — | 0.01 |
| Mark Andrews | 113 | — | 1.00 | — | 1.00 | **0.95** | **0.70** |
| Brock Bowers | 22 | 0.28 | 0.32 | — | 0.00 | — | — |
| Trey McBride | 17 | 0.10 | 0.10 | — | 0.00 | — | — |

Elite TEs barely move (they still carry the lag). Non-TE positions move <0.05. **Actionable: Warren is a pick-32 decision, not a pick-41 freebie. Fannin is a pick-56 target, not a pick-65 one.**
**⚠ n=8 in the deciding cell.** The true cutoff is somewhere between ADP 40 and 60 and cannot be resolved with this sample. Treat Warren-at-41 as genuinely uncertain (0.15–0.95 across the two specifications), not as 0.15.

Also refit: **QB +2.0 → 0.0** (median −0.1, n=68 — this closes weakness #10, which had rested on Section 5 averages F18 disproved) · **WR −4.0 → 0.0** (median +1.0 but year-unstable) · **RB 0.0** (unchanged).

### CORRECTION — request #1 was already satisfied and I kept asking for it
**Historical ADP for 2022–2025 has been in the project since Aug 18.** `picks_with_adp.csv` carries it at 130/140/150/138 true picks per year, sourced from the user's own uploaded ranking sheets (`Combined_Rankings_*` for 2021, `Rankings_vs_ADP__2022`, the 2024 FantasyPros/FootballGuys files) plus `adp2024.csv`. I listed it as the top missing input in `16_...`, in `17_...` and in `00_START_HERE.md` without checking whether it was already there.
**This is the third occurrence of the same failure mode: not inventorying before requesting or concluding.** Standing rule (3) already covers it and was not followed.
**What it unblocked, now done:** H3 (RB/WR pace — measured, both ≈0) and weakness #10 (QB pace — measured, 0.0). **F49 exists because of files the user supplied and I did not use.**

---

## ⚠ CALIBRATION NOTE ON THE AGENT ITSELF (Aug 19)

**The agent's "you don't need that data" judgments are unreliable and must not be trusted.**
Of 7 times the user supplied data the agent had not asked for or had actively deprioritised, **5 changed something material** — including the two largest corrections in the project (the noise model, F35; the TE lag, F49). The error log below counts 22 errors with 8 user-caught, but **that log only starts Aug 18** and omits several earlier sessions, so the true user-caught share is higher.

**Two separate mechanisms, do not conflate them:**
1. Negative calls about data value are wrong ~70% of the time. **Default to accepting any input the user can produce in under ~10 minutes.** Never tell him a source is not worth supplying.
2. **The larger effect is the re-run, not the data.** The Etienne keeper bug (F37), the 37 silently dropped players, the fabricated projections (F42) and the TE over-adjustment (F49) were not in any new file — they surfaced because new data forced the model to be run again. **Re-run the full `integrity.py` harness and the sim at every refresh checkpoint (Aug 24, Sep 5, Sep 7) whether or not anything new arrives.**

**Token discipline:** the user is cost-conscious. Prefer one batched run over exploratory back-and-forth; read findings from this ledger rather than re-deriving them; keep chat sessions short and start fresh ones rather than growing one long context.


---

## F50–F56 — SOUP-TO-NUTS AUDIT (Aug 20, 2026) · full working in `claude/18_audit_2026_08_20.md`

### F50 — The week 1–14 objective and championship equity rank strategies the SAME way ⚠ **CLOSES WEAKNESS #1**
`[TESTED]` **Baseline:** best opening. **Population:** 13 openings, full 12-team league sim on the REAL
schedule (single round robin + 3 repeats, verified against all four seasons) and the real 6-team / 3-week
bracket. **n=1,250 paired seasons.**
RB-RB-RB tops **both** objectives. **Spearman(rank by wk1–14 points, rank by expected dollars) = +0.852;
vs P(title) = +0.641.** Replicated under the corrected scorer (F51, N=750): **+0.863 and +0.879.**
Empirical support from 48 real team-seasons: points-for → seed ρ = −0.684, → made playoffs +0.671,
→ title +0.288; playoff teams 1551.9 pts vs 1388.3.
**→ The directive's objective is correct. Weakness #1 closes.**
*Caveat, stated: the sim gives Matt 33–41% titles because opponents never optimise a lineup. This tests
"no divergence for a STRONG team," not "no divergence exists." A marginal team's convexity is untested.*
*Data gap: the scoreboard file's `Bracket Type` column is `NONE` on all 412 rows — bracket membership is
INFERRED from wk1–14 standings, not read.*

### F51 — `USE_BREAKOUT` in the scorer makes the sim 46% too dispersed ⚠ error, inflates every effect size
`[TESTED]` **Baseline:** 412 real games, weeks 1–14, 2022–2025. **Population:** all 12 teams, 50 sim seasons.
| | real | sim as shipped | BREAKOUT off |
|---|---|---|---|
| weekly mean | 105.0 | 93.9 (0.89×) | 92.2 (0.88×) |
| within-team weekly sd | 20.3 | 22.1 (1.09×) | **20.0 (0.99×)** |
| **between-team sd** | **10.1** | **14.8 (1.46×)** | **10.8 (1.07×)** |
`USE_BREAKOUT` was fitted to **draft displacement**, then applied inside **scoring**, where it stacks a third
variance source on the CV gamma draw and the availability pool. F30's bimodality finding is not challenged;
its use in the scorer is.
**Every downstream use, enumerated (rule 1):** F7 · F38 · F39 · F46 · F50 · every "+X points" magnitude in
`03_draft_board`. **Orderings survive** (F50 replicates both ways; F38/F39 reproduce) — **magnitudes do not.**
Also: `STREAM = {}` and setting it to the measured values changes nothing — starting slots are never empty
on a 14-man roster. That measured finding is inert in this model.

### F52 — `top_400_projections_2026.csv` is a SECOND projection, not a fuller ESPN export
`[TESTED]` **Baseline:** ESPN `TOT`. **Population:** 201 real overlaps, joined on `gsis_id` via `player_xwalk`
(364/400 resolved). Pearson r by position: **QB 0.419 · RB 0.669 · WR 0.711 · TE 0.723**; pooled 0.791,
RMSE 57.2. Same scoring rules (Allen 422.5 vs 421.4). **Provenance unknown — flag on every use.**
Its own replacement levels: RB30 180.5 · WR30 178.9 · QB12 334.2 · TE12 122.4.
**Retires 56 of 195 synthetic rows** by rank-reorder within position (levels kept, ordering replaced —
a linear map was rejected, QB r²=0.175). 52 rows change, **0 above replacement**, no board pick moves.
**139 rows remain fabricated.**

### F53 — The board is fragile to the PROJECTION, where F40 showed it is robust to the ADP
`[TESTED]` **Baseline:** v3. **Method:** quantile-swap within position (ESPN's multiset of values,
`top_400`'s ordering) so F1 is preserved by construction. **N=900 (pick 8), 700 (openings).**
Pick 8 best: v3 → St. Brown/Nacua/Lamb/Taylor tie · BLEND 50/50 → **Barkley +1.9**, Lamb −20.9 ·
SWAP 100% → **Barkley +25.4 (t=7.06)**. RB-RB-RB falls from 1st to 8th under BLEND.
**Survives all three specifications:** Taylor and Jefferson never significantly negative; **London and Cook
negative in all three; Allen never the pick.** Everything else at 8 is projection-dependent.
**→ Widen the pick-8 interval. St. Brown's F38 lean (+34.3) is +12.4 on v3 and −7.6 under BLEND.**

### F54 — `top_400` loses to ESPN against an independent arbiter ⚠ bounds F53
`[TESTED]` **Arbiter:** six-ranker Yahoo panel (Aug 17), derived from neither projection. **n=162 matched.**
Spearman |rho| vs panel rank: QB **0.886/0.749** · RB **0.965/0.733** · WR **0.921/0.667** ·
TE **0.877/0.744** · FLEX **0.933/0.684** (ESPN/top_400). **ESPN wins 4 of 4 and pooled.**
The "it's ESPN × expected games played" explanation is also rejected: ratio skew **+1.13** (a one-sided
availability haircut would be negative), only 53% marked down, and the moves run both ways —
young/unproven down (Tuten 0.02×, Judkins 0.21×, Fannin 0.29×), veterans up (B. Thomas 1.50×, Irving 1.36×).
**→ F53 is a STRESS BOUND, not a rival board. Keep ESPN as the spine; do not blend.**

### F55 — 2021 added: F18 gets deader, F20's TE result goes five-for-five
`[TESTED]` **Population:** true selections only. **n=834 true picks of 894, 60 manager-seasons, 2021–2025.**
*(Per Matt's instruction Aug 20, 2021 is corroboration only and never moves a current estimate.)*
**F4:** rounds 1–4 RB/WR 0.828 (was 0.833) · median first TE round 6 · median first D/ST 12 (IQR 11–13) ·
first K at rd 11+ 0.949. **Correction: the ledger's "TE before round 3 = 1 of 43" is wrong — 2022–25 recomputes
to 2 of 45** (herman allen 2025 *and* Pierce 2023, since departed); 2021 adds a third. The operational claim
(no current manager but herman allen) survives; the count does not.
**F20:** through pick 17 by year 2021→25 — **TE 0,0,0,0,0 (sd 0.00)** · QB 0,0,0,1,1 · RB 5,4,3,6,9 ·
WR 0,1,2,10,7 (sd 4.30). Through 32: QB 2,2,3,3,3.
**F18:** 41 pairs (was 24–33). first_QB +0.112 (p=.50) · first_TE −0.009 (p=.96) · **first_RB +0.072 (p=.66,
was +0.255)** · first_WR +0.029 · cnt4_RB −0.148 · cnt4_WR −0.047. **The one statistic that looked live dies
with more data. Directive §5 stays struck.**
*Only 6 of 12 2021 team names map to a current manager; the rest are not guessed.*

### F56 — TPRR fails gates 2 and 3 ⚠ do not build it · **CLOSES WEAKNESS #13**
`[TESTED]` **Data:** PFF receiving exports 2023/2024/2025. **Population:** WR/TE/RB, ≥100 routes both years.
Receiving-only fantasy points, league scoring. Train 2023→24 (n=210), test 2024→25 (n=209).
**Gate 1 stickiness PASS:** pooled yoy r (n=419) TPRR **0.598** · YPRR 0.587 · tgt/g 0.787 · route_rate 0.901 ·
aDOT 0.890 · slot_rate 0.844 · route grade 0.541.
**Gate 2 FAIL:** baseline (prior PPG + position) OOS R² 0.5411 → +TPRR 0.5420. **Delta +0.0009,
bootstrap 95% CI [−0.0003, +0.0020].** YPRR alone −0.0000. Full route block +0.0039, not separable.
**Gate 3 FAIL:** prior PPG + tgt/g = 0.5504 → +TPRR = 0.5502 (**−0.0002**). Partial r controlling prior PPG
and targets/game = **−0.000, p = 0.997.** `corr(TPRR, tgt/g) = +0.785` — it re-measures volume.
Raw `corr(TPRR_t, PPG_t+1) = +0.580 (p=3e-20)` is fully absorbed. **The mirror of §0's warning: correlated
with the outcome is not incremental to the projection.**

---

## ERROR LOG — additions (Aug 20, 2026)

| Error | Root cause | Caught by |
|---|---|---|
| `assert_keepers_removed` compared raw name strings; `keeper_eligibility_VERIFIED.csv` says "Travis Etienne", the universe says "Travis Etienne Jr." | **Name-based comparison (6th).** F37 was patched at one site instead of at the class — rule 1 violated on the fix itself | Self, Aug 20 (`norm_name` + `assert_names_match` added) |
| `USE_BREAKOUT` calibrated on draft displacement, then applied inside the scorer; between-team spread 46% too wide for the whole project | Parameter validated against one quantity and reused for another; the scorer was never compared to real league scores | Self, Aug 20 (calibration gate against 412 real games) |
| F35's population recorded as "2024–25, n=271"; `resid.csv` actually holds 2022/2023/2025, n=408, and contradicts the sim's own docstring | Finding stored without checking it against the artefact it describes | Self, Aug 20 |
| F4's "TE before round 3: 1 of 43" — recomputes to 2 of 45 (Pierce 2023 omitted) | Count taken over current managers, reported as over team-seasons | Self, Aug 20 |
| `picks_with_adp.csv` recorded in the ledger as present since Aug 18; it is not in the project, so **F49 is unreproducible** | Output file of an analysis never written back to the project | Self, Aug 20 |
| Reported "the two objectives disagree (ρ = −0.03)" off N=25, where se on the dollar mean was ±$40 | Reading a rank correlation off a pilot run | Self, Aug 20 (N=1,250 gives +0.852) |
| `fp_qb_*.csv` / `fp_flex_*.csv` — FantasyPros projections with raw stat lines, in the Drive `Source` folder since Aug 11, never added to the project while "an independent projection" sat at #2 on the missing list | **No inventory step (4th occurrence)** — and the first where the file was outside the project directory | Self, Aug 20 |

**Standing rules — additions:** (11) **A parameter fitted against one quantity may not be reused for another
without re-validating against that second quantity.** (12) **Inventory is not limited to the project folder —
the Drive `Source` folder is part of the project and must be listed too.** (13) **Never read a rank
correlation off a pilot run; check the standard error of the underlying means first.**

---

## KNOWN WEAKNESSES — status after Aug 20

1. **~~Objective stops at week 14.~~ CLOSED by F50** (ρ = +0.85; same top opening on both objectives).
   Residual: untested for a *marginal* team.
5. **The Allen case rests on one projection.** ⚠ **GENERALISED by F53** — it is not just Allen; the whole
   pick-8 ordering is projection-dependent. Only Taylor and Jefferson survive all specifications.
8. **One projection source.** Still open, and now **quantified**. `top_400` is a second projection but a
   measurably worse one (F54). **Request #2 upgraded to #1: a projection with raw stat lines.**
13. **~~No route participation / TPRR.~~ CLOSED by F56 — null.**
15. **NEW — the sim's between-team spread was 46% too wide (F51).** Fixed setting known; every stored
    magnitude predates the fix.
16. **NEW — F49 is unreproducible** (`picks_with_adp.csv` absent). It sets `POSADJ_TE_ELITE` and moved
    Tyler Warren from a pick-41 freebie to a pick-32 decision. **Highest-priority backfill.**
17. **NEW — 2024 is missing from `resid.csv`** (2022/2023/2025 present). Both 2021 and 2024 are recoverable
    from files already in the project.
18. **NEW — Matt's keeper choice has an untested fourth option: Tyler Warren** (TE, VBD +27.8). F46 tested
    only Pickens / Egbuka / Harvey.


---

## ⚠ SAME-DAY CORRECTION BLOCK (Aug 20, 2026, second pass) — F52/F53/F54 PARTIALLY WITHDRAWN

Matt supplied the provenance of `top_400_projections_2026.csv` after the audit was written.
It is **an ESPN pull from his own league**, not an unknown third-party projection:

```
SEASON_YEAR = 2026 · LEAGUE_ID = 21985
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026/segments/0/leagues/21985?view=kona_player_info
x_fantasy_filter = {"players": {"limit": 400,
    "sortDraftRanks": {"sortPriority": 100, "sortAsc": True, "value": "STANDARD"}}}
```

### F52-R — `top_400` is a STALE ESPN pull, not a second projection ⚠ **REPLACES F52**
`[TESTED]` **Population:** 198 rows joined to the 200-row `ESPN_projections_in_my_League.csv`.
It is not the same numbers as the current ESPN board: **0% match within 0.01 points, 3% within 0.5, 8%
within 2.0, 47% within 20.** So the pull did not return the 2026 league projection for most players.

**Two rival explanations tested:**
- **2025 actual points — REJECTED.** Scoring the PFF 2025 exports to league rules (n=135 skill players):
  `r(top_400, 2025 actual) = 0.583` vs `r(top_400, 2026 ESPN projection) = 0.707`. It is closer to a
  projection than to a result. Bucky Irving 256.7 vs 107.5 actual; Chuba Hubbard 234.1 vs 113.3.
- **A one-year-stale (2025) ESPN projection — SUPPORTED, not proven.** Every large disagreement runs in
  the direction of 2025 roles, with no exceptions found:

| player | ESPN 2026 | top_400 | 2025 role |
|---|---|---|---|
| James Conner | **0.0** (out for 2026) | 227.3 | 2025 ARI starter |
| Alvin Kamara | 109.2 | 231.0 | 2025 NO starter |
| Tyrone Tracy Jr. | 79.1 | 187.0 | 2025 NYG starter |
| Malik Willis | 263.4 (MIA starter) | **2.8** | 2025 GB third string |
| Tyler Shough | 306.1 (NO starter) | 115.7 | 2025 rookie |
| Jaxson Dart | 342.9 (NYG starter) | 153.0 | 2025 rookie |
| Bhayshul Tuten | 187.8 | 4.5 | 2025 rookie |
| Cam Skattebo | 217.7 | 125.3 | 2025 rookie |
| Harold Fannin Jr. | 145.7 | 41.7 | 2025 rookie |
| Jonathon Brooks / Tank Dell | 146.3 / 86.5 | **0.0 / 0.0** | missed all of 2025 |

**Mechanism (hypothesis, not verified against the raw payload):** `kona_player_info` returns a `stats`
array per player holding several entries — 2025 actual, 2025 projected, 2026 projected, plus weekly splits.
The script appears not to filter it. **The fix is to select explicitly**, e.g.
`seasonId == 2026 and statSourceId == 1 and statSplitTypeId == 0`, and take `appliedTotal`.
Supporting detail: two 2026 rookies with no prior season — **Jeremiyah Love (245.82 vs 246.2) and Jadarian
Price (180.47 vs 180.50)** — come back on the current board, which is what a fallback-to-the-only-available-row
would produce. `top_400` carries 8 decimals where the ESPN UI export rounds to 1, so it *is* raw `appliedTotal`.

**→ `top_400` is NOT an independent projection. Weakness #8 and weakness #12 (circularity) remain fully open.**

### F53-R — the "board is fragile to the projection" claim is **WITHDRAWN** ⚠ **REPLACES F53**
The BLEND and SWAP perturbations (Barkley +25.4 at pick 8; RB-RB-RB falling to 8th) were built on
`top_400`'s ordering. That ordering is a **stale ESPN board**, not a rival opinion, so the exercise measures
*"what if you drafted off last year's projections"* — which is a known-bad input, not a live uncertainty.
**It is not evidence that the current board is fragile.**
**What survives, and is still worth carrying:** a one-year-stale projection reshuffles the pick-8 order
completely while leaving **Taylor and Jefferson never negative** and **Allen, London and Cook negative in
every specification**. That is a robustness note about *those five players*, nothing more.
**F38 stands unmodified. St. Brown's edge is +12.4 on v3 (was +34.3 in F38) — a lean, as F38 itself said.**

### F54-R — the arbiter test now has a clean interpretation ⚠ **REFRAMES F54**
ESPN beats `top_400` against the six-ranker panel at every position (FLEX 0.933 vs 0.684, n=162).
Read correctly, this is **not** "ESPN's projection beats a rival." It is a **staleness detector**: a
year-old board loses to a current one by ~0.25 of Spearman rho against expert consensus.
**Reusable as a diagnostic** — run it on any future projection before adopting it.

### F57 — F49 REPRODUCES EXACTLY ⚠ **CLOSES WEAKNESS #16**
`[TESTED]` `picks_with_adp.csv` was in the project manifest but absent from disk; Matt restored it.
**666 rows, 561 true picks with ESPN ADP joined, 2022 (130) / 2023 (140) / 2024 (153) / 2025 (138).**
| population | n | median lag | mean | ledger F49 |
|---|---|---|---|---|
| TE, ADP ≤ 40 | **8** | **+14.9** | **+24.2** | +14.9 / +24.2 ✔ |
| TE, ADP 1–60 | 19 | +3.0 | +11.6 | +3.0 / +11.6 ✔ |
| TE, ADP 61–120 | 24 | −3.7 | −3.4 | −3.7 / −3.4 ✔ |
**The deciding cell reproduces to the decimal. `POSADJ_TE_ELITE = (ADP ≤ 40, +16)` is sound, and
Warren-at-41 remains a pick-32 decision.** The n=8 caveat in F49 still applies and is unchanged.
*(Pooled "all" rows differ slightly — 70 TEs here vs 63 in F49 — a population definition difference, immaterial.)*

### F58 — 2024 residuals recovered; F35's proportional form survives a fourth year
`[TESTED]` `resid.csv` (the file the sim loads) holds **408 rows from 2022/2023/2025 — 2024 is missing**,
contradicting the ledger's F35 line ("2024–25, n=271") *and* the sim's own docstring. `picks_with_adp.csv`
supplies all four years, n=539 usable residuals.
Refit by ADP band: **sd = 0.1175 × rank + 8.23, r = 0.984** (four years) vs **0.1044 × rank + 9.70, r = 0.995**
on the sim's three-year file. Band sds (4yr): 8.3 / 14.3 / 19.9 / 24.4 at median ranks 11 / 43 / 90 / 145.
**The proportional form is confirmed on a year it was never fitted to.** The sim's constants
(0.1255 / 5.31) sit slightly tighter than either refit; binning differs, so these are not directly
comparable and the constants are **not** changed on this basis. **Rebuilding `resid.csv` from all four
years is the correct next step and has not been done.**

---

## ERROR LOG — additions (Aug 20, second pass)

| Error | Root cause | Caught by |
|---|---|---|
| Told Matt `picks_with_adp.csv` "does not exist in the project" and asked him to backfill it. It was in the project manifest; only the disk copy was absent. He spent time searching | **Inventory read the directory but not the manifest, and the two disagreed.** Fifth occurrence of the inventory failure mode | **User challenge, Aug 20** |
| Published F52/F53/F54 calling `top_400` "a second, independent projection" and "the board is fragile to the projection" | **Provenance was unknown and I proceeded anyway.** The directive requires flagging an incomplete-provenance source and flagging every recommendation that depends on it — I flagged it, then built three findings on it regardless | **User-supplied provenance, Aug 20** |
| Diagnosed `top_400` as "not FantasyPros" and asked for its origin, without first testing the two obvious stale-data explanations | Reached for a new data request before exhausting tests on data already held | Self, Aug 20 |

**Standing rules — addition:** (14) **A source with unknown provenance may be used to BOUND a result, never
to overturn one.** F53 overturned "the board is stable" on a file nobody could identify.
(15) **Inventory means the manifest AND the directory, and any disagreement between them is itself reported.**
