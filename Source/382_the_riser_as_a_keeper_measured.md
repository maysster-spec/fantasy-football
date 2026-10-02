# 382. THE RISER AS A KEEPER: MEASURED, MATT'S WAY, AND IT LIVES IN ROUNDS 5 TO 8 WHERE PRICE CARRIES NOTHING

*22 Sept 2026, 00:20 ET. Fable, running JOB 4 from `Source\REDTEAM_TASKING_PROMPT.md` at Matt's instruction
("run the two queued jobs, next kickoff then JOB 4"). Script and every output in
`Scripts\research\j4\`. Doc 381 is the previous number; 382 reserved by listing the folder. No em dashes.*

---

## 0. WHAT TO DO

1. **A rule changed, and it is the one you said was never measured.** Inside the audition band
   (rounds 5 to 8, preseason ADP 50 to 96), the man to keep is the one whose share of his team's
   opportunity ROSE from weeks 1 to 5 to weeks 10 to 14 of the season just ended. Net of price, the top
   third of risers returned **+52 VBD14** more than the bottom third the next season (95% interval 26 to
   78; n=107, 2022 to 2024) and were startable **56%** of the time against **25%**. Price inside the band
   carries nothing: ADP 50 against ADP 96 is worth 1.4 points, indistinguishable from zero. Section 6's
   "ascending" bullet is no longer a tiebreak with no number; **section 4.26(a)'s "prefer the one drafted
   closest to round 5" is withdrawn as a tiebreak inside the band** (it still holds across bands).
   Directive v9.10, findings entry 4.34.
2. **A rule that did NOT change: round 9 and later stays a dart, riser or not.** In the ADP 97+ band the
   trajectory adds 1.4 VBD14 per ten share points (se 2.0, n=227); a round-9+ man whose share rose was
   startable 29% of the time and returned minus 42. Section 4.18b stands. The riser matters where the
   price band already says audition, not where it says dart.
3. **A number that must not be quoted:** the pooled gap of 18 VBD14 (4 to 29). It is true and it is the
   wrong object, an average over a band where the effect is 52 and a band where it is 1. Quote the band.
4. **The second arm, youth times trajectory: amplification, in the direction 4.30 showed at receiver.**
   The riser is worth about 3 per ten share points for a man in his fourth season or later and about 12
   for a man in his first three (interaction +8.5, se 3.9); the same sign in all four populations run,
   significant in two. Not substitution.
5. **What this does to your 2027 keeper, and it starts in week 10.** The 2026 audition band on your
   roster is Hurts, LaPorta, Dowdle and Dobbins (doc 329). The number that decides among them is not on
   any page yet: each man's share of his team's carries plus targets (LaPorta: targets; Hurts:
   attempts) in weeks 10 to 14 against weeks 1 to 5. **That line on the week sheet is what finishes
   this job (section 5, mine, NOT YET RUN).** Until it ships, the rule is the sentence in item 1.
6. **Paste directive v9.10** (on your list). Nothing else to run.

---

## 1. THE TESTABLE FORM, AS THE JOB WROTE IT, AND WHAT WAS ACTUALLY BUILT

**Population:** player-seasons in year N at QB, RB, WR, TE with a section 1.1 preseason ADP of 50 or
later in year N and priced again in year N+1; N = 2022, 2023, 2024 (the nflverse weekly cache holds
2022 to 2025 and no 2021 file, so N=2021 is out, one season short of the job's 2021 to 2024).
**n = 334 pooled: WR 132, RB 97, TE 58, QB 47; by season 101, 141, 92.**

**Exclusions, named with their size (0.6):** 237 player-seasons met the ADP condition and were NOT
priced again in N+1 (41% of the matched band). That condition is the job's, and it selects on something
close to the outcome, so the whole analysis was re-run without it (n=433): every number below moves the
same way or strengthens. 43 had no game at all in one of the two windows (re-run with a missing window
scored as zero share: same result, smaller). 23 played fewer than four games in N+1. 71 registry names
did not match nflverse at the four positions; 56 of those are the kickers and defences the 2024 registry
carries, the rest are spellings the fallback could not resolve uniquely; 13 were matched by last name
plus first initial where that key was unique that season (Gabe/Gabriel Davis, Ken/Kenneth Walker).

**The registries are not one instrument** (MANIFEST.csv): 2022 is FantasyPros ADP, 2023 is Underdog
best-ball ADP, 2024 is a consensus rank proxy. Re-run without 2024: same result, larger.

**Predictor:** his share of team opportunity in weeks 10 to 14 of year N minus the same share in
weeks 1 to 5. Opportunity is carries plus targets at RB, targets at WR and TE, attempts at QB; the
denominator is his team's total over the team's games in the window, so a missed game is a zero for him.
Two variants were also run: the share only in games he played (availability held out), and year N
against year N-1.

**Control:** log preseason ADP in year N, and position. Mandatory, per the job, because 4.26(a) already
measured that price predicts repeating.

**Outcomes:** (i) year N+1 VBD14 on 4.18b's baseline, weeks 1 to 14 league-scored points minus the same
season's RB30 / WR30 / QB12 / TE12 weeks-1-to-14 total (2025: RB 110.5, WR 115.0, QB 261.4, TE 100.1);
(ii) startable at all in N+1, 4.13b's absolute bar, weeks 1 to 14 points per game played at or above
QB 20.09 / RB 9.92 / WR 9.62 / TE 8.25, four games or more.

**Falsifier, fixed before the run:** trajectory adds nothing net of price with an interval excluding a
ten-point gap, strike "ascending"; ten or more net of price, 4.26(a) is the wrong instruction; the
interval spans both, say what n resolves it.

---

## 2. THE RESULT

**Pooled, the job's own population (n=334).** VBD14 in N+1 on log ADP and position alone: log ADP
minus 25 (se 6). Add the riser: **+6.0 VBD14 per ten points of team share gained (se 1.8)**, and the
price coefficient does not shrink (minus 28.5), so this is not price re-found and renamed. Top third of
risers against bottom third, net of price and position: **+18.0 VBD14 [4.0, 29.4]**. Startable in N+1:
+0.24 in the log-odds per ten share points (se 0.09); adjusted at each man's own price, 37% against 29%.

**The falsifier's verdict on the pooled number:** the interval excludes zero and includes ten. By the
job's third branch, the n that resolves a ten-point gap at 80% power is about **405 per tercile** against
112 held (residual sd 51): roughly ten more seasons. **But the pooled number is the wrong object**, and
the split below is where the job's question is actually answered.

**By price band, which is the split the doctrine draws:**

| band | n | riser per +10 share pts, net of price | top third VBD14 (startable) | bottom third VBD14 (startable) | gap net of price | price inside the band |
|---|---|---|---|---|---|---|
| **ADP 50 to 96, rounds 5 to 8** | 107 | **+11.2 (se 3.3)** | **+3.7 (56%)** | **minus 48.9 (25%)** | **+52.1 [26.3, 78.3]** | +2.2 per log unit (se 30): ADP 50 against 96 is 1.4 points |
| ADP 97 and later, round 9+ | 227 | +1.4 (se 2.0) | minus 42.0 (29%) | minus 45.4 (22%) | not resolved | minus 37 per log unit |

Inside the audition band the falsifier's second branch is met with room to spare: the interval's floor
is 26. Inside the dart band the first branch is met on the point estimate and the interval is too wide to
strike anything; it does not matter, because 4.18b already sends round 9+ to the darts on a different
measurement and nothing here disturbs it.

**Within the band, by position** (top third against bottom third, small cells, read as direction):
RB (n=34) +37.6 and 75% startable against minus 40.2 and 21%; WR (n=41) +1.7 and 53% against minus 49.2
and 18%; TE (n=14) minus 5.1 against minus 13.6; QB (n=18) minus 39.8 against minus 86.3. **At every
position the man whose share fell is the one not to keep**, and at RB and WR the man whose share rose is
the keeper.

**Pooled by position, all bands:** RB +16.4 per ten share points (se 5.3, n=97; top against bottom
+34.5 [8.8, 61.9]); TE +8.9 (se 5.5); QB +3.5 (se 2.8); WR +0.7 (se 5.6). The WR null is the dart band's
mass (91 of 132 receivers are ADP 97+); inside rounds 5 to 8 the receiver responds like the back.

**The availability confound, held out.** Re-computed on his share in the games he PLAYED, so an injury in
weeks 10 to 14 does not move it: +6.6 per ten (se 2.4) pooled, RB +15.5 (se 5.9). The riser is a role
change, not a health record (4.22 is a separate, already-measured signal).

**Variant 2, year N share against year N-1** (n=187, where both exist): +2.9 per ten (se 2.3). The late
window of the season just ended carries the information; the year-over-year change is a weaker
instrument. Use the in-season variable.

**The four populations, side by side** (the gap is top third minus bottom third, pooled, net of price):

| run | n | riser per +10 | gap [95%] | youth interaction per +10 |
|---|---|---|---|---|
| the job's population | 334 | 6.0 (1.8) | 18.0 [4.0, 29.4] | +8.5 (3.9) |
| without "priced again in N+1" | 433 | 6.4 (1.6) | 21.0 [10.7, 32.8] | +11.1 (3.5) |
| a missing window scored as zero share | 370 | 4.1 (1.4) | 17.8 [5.1, 30.0] | +3.8 (3.1) |
| without 2024 (rank-proxy registry) | 242 | 8.7 (2.4) | 20.3 [3.1, 35.3] | +9.4 (5.9) |

---

## 3. THE SECOND ARM: YOUTH TIMES TRAJECTORY

Youth is three seasons or fewer of NFL experience in year N (nflverse rookie_season). Pooled, with the
interaction: riser for the older man **+3.3 per ten** (se 2.1); youth alone +6.9 (se 5.8); **riser times
youth +8.5 (se 3.9)**, so the riser is worth about **+11.8 per ten for a young man**. Cells, the job's own
population: young and rose (n=60) minus 23.7 VBD14, 42% startable; young and fell (n=44) minus 47.1, 25%;
older and rose (n=52) minus 36.4, 29%; older and fell (n=68) minus 39.8, 29%. **The trajectory does its
work on the young man and almost none on the veteran: amplification (0.5a3), the direction doc 248 found
at receiver, not doc 191's substitution at running back.** Same sign in all four populations, past two
standard errors in two of them. Suggestive, and consistent with 4.30, not a settled interaction.

---

## 4. THE 4.18b OBJECT, WHICH THIS JOB EXISTED TO SEPARATE

4.18b pooled a one-year fluke role with a real role expansion because its population was cut by price.
Among the **114 year-N hits** here (VBD14 in year N above zero): the man whose late share ROSE returned
**+3.9 VBD14** the next season and was above replacement 45% of the time; the man whose share FELL returned
**minus 18.0** and was above replacement 34%. Net of price and of the size of the hit, +4.2 per ten (se 5.8),
underpowered at 38 a cell. **And the size of the hit itself predicts nothing** (0.02 per point, se 0.20):
a bigger year is not a more durable one, which is 4.18b's "regresses through replacement" restated with
the variable that splits it named. Direction Matt's; magnitude open at this n.

**This league's own keepers, descriptive only** (draft_history_2021_2025.csv, 36 keepers 2023 to 2025,
33 joined): the room already leans toward risers, 17 of 33 in the top third against 11 expected; the
kept risers averaged +5.9 VBD14 and 65% startable, the kept flat men minus 48 and 40%. Matt's own three
in the join were Mattison (fell, minus 8), LaPorta (flat, minus 4) and Daniels (flat, minus 131): the
complaint the job opened with, on his own roster.

---

## 5. THE THREE ANSWERS, AND WHAT FINISHES THIS

- **TESTED.** Population, baseline, n, direction and the number, section 2. Matt's prediction holds in
  direction pooled (p about 0.001) and in size inside rounds 5 to 8 (+52, floor 26). The pooled magnitude
  against the ten-point line is open and needs about 405 a tercile.
- **NOT YET RUN, mine, and it is the finisher:** the keeper-riser line on `WEEK_SHEET.html`. Testable form:
  for every man on the roster drafted round 5 to 8, print his share of team opportunity over his last five
  games against his first five, from `form_2026.csv` (which `build_form.py` writes weekly), with the
  words "rounds 5 to 8: keep the one whose share rose; a fall is a reason not to". From week 10 the two
  windows are the ones this doc measured. A guard: the line must name every round-5-to-8 man on the
  roster or refuse (0.5c5).
- **BLOCKED:** nothing. The 2021 weekly file would add a fourth season and is a download, not a wall.

**Files:** `Scripts\research\j4\j4_riser_keeper.py` (standard library, pandas, numpy; paths against the
file; `--no-price-next`, `--missing-window-zero`, `--exclude-2024`), `J4_rows_<run>.csv` (one row per
player-season, every variable above), `J4_summary_<run>.json`, `run_j4_<run>.txt`. Directive v9.10 and
findings entry 4.34 carry the rule; ledger row 158.
