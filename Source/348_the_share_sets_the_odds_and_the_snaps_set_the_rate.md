# 348 -- THE WEEK-ONE SHARE SETS THE ODDS, THE SNAPS SET THE RATE, AND NOTHING SETS THE WEEKS

**2026-09-18, 07:40 EDT.** JOB 2 of `REDTEAM_TASKING_PROMPT.md` section B, as amended 17 Sept
(the 21:45 box). Continues doc 327 (JOB 1), doc 343 (the per-band odds), doc 320 (the usage order)
and doc 344 (the section-A red team); written beside docs 346 and 347, which the other session
filed while this ran (the Brooks reply and the seat list's three void rows). Five things were run, every testable form was fixed before its
run, and one of the two halves of the headline claim died on its own falsifier. All the code is in
`Scripts\research\j2\`, every number below comes from a file named there, and nothing touched
ESPN, a claim, or a drop.

---

## 0. THE CLAIMS AS FIXED, AND WHAT HAPPENED TO EACH

| # | the claim, in its testable form | verdict |
|---|---|---|
| 1 | With each seat priced at its own per-band odds (`seat_odds()`, the production function), at least one free seat's one-currency value net of the cheapest skill drop is above zero | **passes trivially, and for the wrong reason:** the cheapest skill drop on today's roster is Chris Brooks at **0.01** in one currency. Against the cheapest man who carries a real projection (Worthy, 4.91) **no seat can clear at any odds** -- the break-even odds run 1.04 to 1.17 |
| 2a | Across 2021-2025 backfield absences the usage order's predicted inheritor captures a larger share of the vacated carries plus targets than the chart's does | **passes.** 0.575 against 0.532 over the spell, +0.043, one-sided sign-flip p=0.015 on 105 paired events; where the two arms name different men, 0.454 against 0.279, +0.174, p=0.016 |
| 2b | The relief SCORING rate varies with that predicted share, on the page's own predictor (the week-one share, doc 300) | **DIES.** 12.13 / 11.71 / 13.11 / 12.45 across the four bands; rho −0.05, p=0.63; the 35% split −0.71, p=0.68. **The seat lane is right to apply one rate to the page's column.** The weeks are flat too |
| 2c | T5 (doc 292: the second back's share of the non-leader RB snaps) run as an independent second band on the same rows | **T5 orders the RATE and the week-one share does not:** T5 to date 9.3 / 10.2 / 12.9 / 14.1 a game across its four bands, rho +0.27, p=0.003; 70%+ against under, +3.9 a game, p=0.002. And T5 does **not** order the ODDS (0.556 / 0.536 / 0.474 / 0.549). Two predictors, two terms |
| 3 | Adding 2021 keeps the top band above the bottom on P(the job opens) | **holds, narrower.** 0.510 / 0.474 / 0.564 / 0.621 on n = 51 / 38 / 39 / 29, against 0.476 / 0.438 / 0.533 / 0.636. Seats-only split +0.34, p=0.019. The four-season numbers reproduced exactly first, as the control |
| 4 | Whether a seat should be netted against a drop at all when the claim is a stash for a man not yet hurt | **yes, and on this wire it does not matter which way you net it:** every seat's whole gross (≤ 2.1) is below the cheapest real drop (4.9), so the seat loses even if landing him after the news were impossible; and it clears the two zero-cost seats even at the worst odds |

---

## 1. STEP 1 -- THE JOB 1 MATRIX WITH THE PER-BAND ODDS (`j2_seat_odds_matrix.py`)

**POPULATION, restated (0.6):** the 317 free players ESPN prices on the 18 Sept pull minus the
twelve rosters in `LEAGUE_ROSTERS.csv` (257 of them on `WIRE_20260918.csv`), against
`MY_ROSTER.csv` of 18 Sept 06:29 EDT (Vele and Chris Brooks on it, Hockenson and Shough gone).
Weeks 1-14, N=1,500 paired draws, seed 20260918, the same harness as doc 327 with two changes:
the seat odds come from `seat_odds()` per row instead of the flat `p_opens`, and because the odds
enter the value linearly, the flat number, the per-band number and the **break-even odds** for
every seat against every drop are all solved from ONE draw. Control first: arm A reproduced
`price()` on all 317 men and `drop_costs()` on all 15 (worst gap 0.049; the `price()` control now
allows 0.05 a live week because `price()` rounds each week, ledger row 92 -- the Browns row is 0.16
a week printed as 0.2 thirteen times, and JOB 1's flat 0.11 tolerance would have failed on it).

**THE PAGE'S OWN LIST IS UNCHANGED BY THE ODDS.** Top five under the flat rate and under the bands
are the same five in the same order: Schultz, Mayer, Browns D/ST, Malik Washington, Raymond. No
seat is in the top five under either. The seat lane's own order moves by one tie-break (Ty Johnson
first on the page at 1.1, Bigsby first in one currency at 2.1).

| seat man | band | odds | if it fires | page (band / flat) | one currency gross (band / flat) | break-even odds vs Brooks 0.01 | vs Vele 0.23 | **vs Worthy 4.91** | vs Washington 6.29 |
|---|---|---|---|---|---|---|---|---|---|
| Tank Bigsby | <20 | 0.476 | 2.4 | 1.1 / 1.1 | 2.10 / 2.03 | 0.00 | 0.05 | **1.06** | 1.27 |
| Ollie Gordon II | -- | 0.460 | 2.4 | 1.1 / 1.1 | 2.06 / 2.06 | 0.00 | 0.05 | **1.04** | 1.24 |
| Ty Johnson | -- | 0.460 | 2.4 | 1.1 / 1.1 | 2.04 / 2.04 | 0.00 | 0.05 | **1.05** | 1.25 |
| Emari Demercado | <20 | 0.476 | 2.4 | 1.1 / 1.1 | 2.01 / 1.95 | 0.00 | 0.05 | **1.10** | 1.31 |
| Samaje Perine | 20-30 | 0.438 | 2.4 | 1.1 / 1.1 | 1.93 / 2.03 | 0.00 | 0.05 | **1.06** | 1.26 |
| DJ Giddens | -- | 0.460 | 2.0 | 0.9 / 0.9 | 1.92 / 1.92 | 0.00 | 0.06 | **1.12** | 1.31 |
| Brian Robinson Jr. | 20-30 | 0.438 | 1.9 | 0.8 / 0.9 | 1.76 / 1.85 | 0.00 | 0.06 | **1.17** | 1.38 |

A dash in the band column is a man with no week-one line, priced at the flat 0.46 and starred on
the page. **The odds move a seat by at most 0.1** (Bigsby 2.03 → 2.10, Robinson 1.85 → 1.76). Two
of the seven are void rows by doc 347 §3, written while this ran: Demercado is on Dallas, and
Giddens has no week-one line and sits behind McGowan. Dropping them changes nothing below.

**THE BREAK-EVEN INFERENCE IS SUPERSEDED BY THE ROSTER, NOT SETTLED BY THE ODDS.** Doc 327's
"gross seat about 2.8 against the cheapest drop 2.7" was on the 16 Sept roster, where the cheapest
drop was Hockenson. He is gone. Today the two cheapest drops in one currency are **Chris Brooks 0.01
and Devaughn Vele 0.23**, so every seat clears them at any odds above 5%; and the cheapest man who
carries a projection is **Worthy at 4.91**, against whom no seat clears at odds of 100%. There is
no roster on which the odds bands decide this question, because a seat's whole value at certainty
(4.2 to 4.7 points) sits below Worthy's drop cost.

**AND THE TWO ZEROS ARE THE FROZEN PROJECTION TALKING.** Brooks costs 0.01 to drop because the
matrix scores him at his preseason projection, which is the number ledger row 42 already showed
did not move when he became part of a Green Bay timeshare (doc 346 §2 has the week-one line: 56%
of snaps, 7 carries, on the losing side of it). The one-currency arm
inherits the page's projections; it cannot see a situation the projection has not priced. Read
"Brooks costs nothing" as "the board thinks Brooks is nothing", which is the row-42 defect, not a
verdict on the man. Vele's 0.23 is the same statement about a receiver ESPN projected at 4.6 a
game.

Drop costs in one currency, for the record: Brooks 0.01 · Vele 0.23 · Worthy 4.91 · Washington
6.29 (his handcuff value behind Jeanty at the relief rate, doc 297 arm D) · Dobbins 8.85 · Dowdle
12.63 · Adams 29.09 · Pickens 30.79 · Jeanty 31.82 · Judkins 34.56 · LaPorta 36.71 · Hurts 55.15 ·
Nacua 90.03. Kickers and defences are unpriced against a streamer in every arm because the
constants carry none (doc 327 §4), so Pineiro's 118.7 and the Chiefs' 0.0 are the deleted
constant, not findings.

Files: `J2_seats_by_odds.csv` (every seat, both odds, break-even against all fifteen drops),
`J2_orderings.csv`, `J2_add_minus_drop_matrix.csv`, `J2_drop_costs.csv`, `J2_matrix_summary.json`,
`run_j2_matrix_20260918.txt` (1,569 s).

---

## 2. FIRST HALF -- THE USAGE MAN TAKES MORE OF THE VACATED WORK (`j2_share_and_rate.py`)

**POPULATION, restated (0.6):** doc 320's events, built by the same function
(`b2_depth_order.build_events()`) so they are doc 320's rows: every team-week 2021-2025, weeks
2-14, where the back who led his team in carries plus targets to date played the previous week and
has no line this week while his team plays; one event per absence, its first week. **n=114
(2021: 32 · 2022: 25 · 2023: 20 · 2024: 21 · 2025: 16), 111 with a preseason chart, 105 where both
arms name a man.** The SPELL is the run of consecutive team-played weeks from that week in which the
leader has no line, **capped at week 14**, the sheet's horizon: mean 3.06 weeks, median 2 (3.97
through week 18). The pie while the leader is out is 26.8 RB carries plus targets a week against
26.5 before the absence -- **the work is redistributed, not lost** (101%), so "share of the spell
pie" is the vacated work.

**OUTCOME:** each named man's carries plus targets over the spell weeks, divided by the team's.
**PAIRED:** the same events under both arms; a sign-flip permutation on the differences, 10,000
draws, one-sided in the claimed direction.

| | chart's man | usage's man | usage minus chart | one-sided p |
|---|---|---|---|---|
| all 105 paired events | 0.532 | 0.575 | **+0.043** | **0.015** (two-sided 0.030) |
| the 26 where the arms disagree | 0.279 | 0.454 | **+0.174** | **0.016** |
| weeks 2-4 (n=24) | 0.531 | 0.538 | +0.007 | -- |
| weeks 5-9 (n=48) | 0.517 | 0.554 | +0.038 | -- |
| weeks 10-14 (n=33) | 0.555 | 0.633 | +0.078 | -- |

The arms name the same man on 79 of 105, so the whole difference lives in 26 events, and there the
usage man takes 45% of the vacated work to the chart man's 28%. The gap grows with the season, as
doc 320's hit rate did. Largest swings the usage order got right: Charbonnet over DeeJay Dallas
(SEA 2023, 0.87 to 0.13), Ray Davis over Ty Johnson (BUF 2024, 0.85 to 0.15), Swift over Penny
(PHI 2023, 0.78 to 0.10), Tracy over Gray (NYG 2024, 0.80 to 0.20), Gainwell over Kaleb Johnson
(PIT 2025, 0.78 to 0.22). Where it got it wrong: Trenton Cannon over Sermon (SF 2021, 0.00 to
0.94) and DeeJay Dallas over Homer (SEA 2021, 0.00 to 0.27). Over the spell the usage man scores
**11.66 a game to the chart man's 10.75**, on the same **2.6 weeks** with a line. `[TESTED, n=105]`

---

## 3. SECOND HALF -- THE RATE IS FLAT ON THE PAGE'S PREDICTOR, AND NOT FLAT ON THE SNAPS

The seat's price on the sheet is **odds × rate × weeks**: `p_opens_by_band` (doc 343) ×
`relief_ppg` 12.13 × `weeks_played` 3.02. The amendment asked which of the three terms a
share-of-the-backfield predictor moves. Four predictors were fixed before the run, every one
knowable BEFORE the absence, on the usage man (the man the page names since doc 320):

- **A** -- the week-one share, doc 300's measure and the column `inherit_2026.csv` carries:
  his share of the team's week-one RB carries plus targets, the leader IN the denominator.
  Blank, never zero, when he has no week-one line (n=94 of 112).
- **B** -- the same ratio over the weeks to date (n=112).
- **C** -- T5 at week one, doc 292's measure: his week-one offensive snaps over all RB snaps that
  week EXCLUDING the leader's, so a clean two-man room reads 100% (n=99).
- **D** -- T5 over the weeks to date (n=112).

Snaps came from nflverse `snap_counts_2021..2025.csv`, joined to the weekly file on `pfr_id` →
`gsis_id` through `players.csv` with name plus team as the fallback: **zero unjoined RB rows in
2021-2024, 7 of 1,612 in 2025 (Nathan Carter, ATL)**, printed by the run. The relief RATE is the
usage man's half-PPR per game in the spell weeks he had a line -- by construction he has at least
one, because both arms step past a man with no line in the first week (doc 296). On this population
it is **11.68 a game against the constant's 12.13**, and the weeks with a line are **2.59 against
3.02** -- close enough that the constants and this population are the same animal.

| predictor | band | n | **rate** | weeks | share of pie | startable |
|---|---|---|---|---|---|---|
| **A** week-one share (the page) | <20 | 30 | **12.13** | 2.53 | 0.583 | 0.600 |
| | 20-30 | 16 | 11.71 | 2.75 | 0.628 | 0.562 |
| | 30-40 | 18 | 13.11 | 2.06 | 0.585 | 0.556 |
| | 40+ | 30 | **12.45** | 2.77 | 0.592 | 0.500 |
| **B** share to date | <20 | 28 | 8.75 | 2.57 | 0.487 | 0.321 |
| | 20-30 | 33 | 11.20 | 2.88 | 0.605 | 0.515 |
| | 30-40 | 34 | 13.78 | 2.38 | 0.633 | 0.647 |
| | 40+ | 17 | 13.21 | 2.47 | 0.589 | 0.529 |
| **C** T5 at week one | <50 | 24 | 8.91 | 3.04 | 0.491 | 0.417 |
| | 50-70 | 13 | 12.55 | 2.85 | 0.665 | 0.615 |
| | 70-85 | 11 | 14.69 | 2.91 | 0.666 | 0.818 |
| | 85+ | 51 | 12.98 | 2.12 | 0.605 | 0.510 |
| **D** T5 to date | <50 | 30 | **9.33** | 2.63 | 0.500 | 0.367 |
| | 50-70 | 26 | 10.18 | 3.54 | 0.565 | 0.462 |
| | 70-85 | 23 | 12.91 | 1.96 | 0.673 | 0.609 |
| | 85+ | 33 | **14.12** | 2.24 | 0.604 | 0.606 |

| predictor | rate: rho (p) | rate: split (p) | weeks: rho (p) | share: rho (p) |
|---|---|---|---|---|
| **A** | **−0.050 (0.63)** | **−0.71 at 35% (0.68)** | +0.039 (0.71) | −0.069 (0.51) |
| B | +0.244 (0.012) | +1.72 at 35% (0.135) | −0.057 (0.55) | +0.124 (0.21) |
| C | +0.174 (0.085) | **+3.10 at 70% (0.021)** | −0.152 (0.13) | +0.128 (0.21) |
| **D** | **+0.269 (0.003)** | **+3.90 at 70% (0.002)** | −0.119 (0.21) | +0.202 (0.032) |

Spearman rho with a 6,000-draw permutation p; the split is the one-sided permutation at 35% (A, B)
or 70% (C, D), the cuts job_opens.py and doc 292 used, so the numbers compare. `[TESTED]`

**THE FALSIFIER FIRES ON A.** The rate does not move with the page's predictor in any direction
that survives a permutation, and neither do the weeks. **For the column the page carries, one rate
and one weeks number are right, and JOB 2's second half closes as a null.** The odds bands (doc
343) are the whole of what the week-one share buys.

**AND THE RATE IS NOT UNPREDICTABLE -- IT ANSWERS TO THE SNAPS.** A man who takes 85% or more of the
non-leader snaps to date scores **14.1 a game** in relief; a man under 50% scores **9.3**, below the
9.92 startable bar. That is a factor of 1.5, against the odds bands' factor of 1.2 (0.51 to 0.62),
and it holds inside every week band (weeks 2-4: 13.0 against 7.3; 5-9: 12.5 against 10.4; 10-14:
16.4 against 10.1, T5 to date 70%+ against under). **Doc 292 measured T5 on the first game only and
left "over the whole absence" NOT YET RUN; this is that run, on doc 320's events, and it holds.**

**SO THE TWO PREDICTORS SPLIT THE TERMS, AND THIS IS THE ANSWER TO THE AMENDMENT'S ITEM 4:**

| term | week-one work share (doc 300, the page) | T5 non-leader snaps (doc 292) |
|---|---|---|
| **odds** -- P(the job opens) | orders it: 0.51 / 0.47 / 0.56 / 0.62, five seasons | **flat**: 0.56 / 0.54 / 0.47 / 0.55 |
| **rate** -- what he scores while it is open | **flat**: 12.1 / 11.7 / 13.1 / 12.5 | orders it: 9.3 / 10.2 / 12.9 / 14.1 (to date), 8.9 / 12.6 / 14.7 / 13.0 (week one) |
| **weeks** -- how long it stays open | flat | flat, and if anything reversed (below) |

They are not the same number wearing two denominators: on the same 94 men rho between A and C is
only +0.35, 28 of 94 sit two bands or more apart, and **where they disagree, C is right about the
rate**: A high and C low (n=9) scores 8.9; A low and C high (n=22) scores 13.0, the same as both
high (n=39, 13.6). Sony Michel 2021 (A 6%, C 100%, 14.1 a game over two weeks), Perine 2022 (A
14%, C 100%, 17.9), Monangai 2025 (A 4%, C 100%, 21.3), Dowdle 2025 (A 21%, C 92%, 31.4) are the
shape: a man who barely touches the ball while the starter is healthy but is the ONLY other back on
the field. The work share cannot see him; the snap share can.

**THE WEEKS, OBSERVED AND NOT PRE-REGISTERED.** A T5-to-date man at 70%+ plays **2.1** relief weeks
against **3.1** under 70% (two-sided permutation p=0.030), and the reason is the ABSENCE, not the
backup: the leader's spell is 0.84 weeks shorter when his direct backup already holds the backup
snaps, inside every week band (3.1 against 4.5 · 2.9 against 4.3 · 1.4 against 1.9). Part of it
is the horizon cap (later events have shorter spells, and T5 to date falls with the week, rho
−0.21), part is not. **A shape, not a finding**; it was not fixed in advance and it is one cut.

**THE HISTORY OF THE TWO INSTRUCTIONS THIS SETTLES.** `job_opens.py`'s header says the two measures
"must never be swapped"; that stands, and it now has a reason on each side: swap them and the odds
go flat and the rate goes flat.

Files: `J2_events.csv` (every event, both men, all four predictors, all three outcomes),
`J2_A_vs_C.csv`, `J2_live_bands_2026.csv`, `run_j2_share_and_rate.txt`, `J2_share_summary.json`.

---

## 4. THE LIVE 2026 SEAT ROWS UNDER BOTH BANDS, AND TWO JOIN DEFECTS

The 32 rows of `inherit_2026.csv` with the page's own `wk1_share` (A) and T5 at week one (C)
from `research\wk1\snap_counts_2026.csv`, `J2_live_bands_2026.csv`:

| next man | team | A (page) | band | C (T5 wk 1) | band | behind |
|---|---|---|---|---|---|---|
| Kaelon Black | SF | 0.46 | 40+ | 1.00 | 85+ | McCaffrey |
| RJ Harvey | DEN | 0.47 | 40+ | 0.90 | 85+ | Dobbins |
| Rico Dowdle | PIT | 0.45 | 40+ | 0.93 | 85+ | Warren |
| Tyjae Spears | TEN | 0.44 | 40+ | 1.00 | 85+ | Pollard |
| Tyler Allgeier | ARI | 0.56 | 40+ | 0.94 | 85+ | Love |
| Jordan Mason | MIN | 0.52 | 40+ | 0.83 | 70-85 | Aaron Jones |
| Kyle Monangai | CHI | 0.39 | 30-40 | 1.00 | 85+ | Swift |
| Woody Marks | HOU | 0.30 | 30-40 | 1.00 | 85+ | Montgomery |
| Braelon Allen | NYJ | 0.31 | 30-40 | 1.00 | 85+ | Hall |
| **Brian Robinson Jr.** | ATL | 0.23 | 20-30 | **1.00** | **85+** | Bijan -- **the bands disagree** |
| **Justice Hill** | BAL | 0.22 | 20-30 | **1.00** | **85+** | Henry -- **disagree** |
| Keaton Mitchell | LAC | 0.25 | 20-30 | 0.81 | 70-85 | Hampton |
| Chris Rodriguez Jr. | JAX | 0.22 | 20-30 | 0.79 | 70-85 | Tuten |
| Rachaad White | WAS | 0.30 | 30-40 | 0.81 | 70-85 | Croskey-Merritt |
| Blake Corum | LA | 0.33 | 30-40 | 0.64 | 50-70 | Kyren |
| Jonathon Brooks | CAR | 0.25 | 20-30 | 0.65 | 50-70 | Hubbard |
| Mike Washington Jr. | LV | 0.19 | <20 | 0.57 | 50-70 | Jeanty |
| Tank Bigsby | PHI | 0.05 | <20 | 0.38 | <50 | Barkley |
| Tyrone Tracy Jr. | NYG | 0.07 | <20 | 0.07 | <50 | Skattebo |
| Dylan Sampson | CLE | 0.00 | <20 | 0.00 | <50 | Judkins |
| Ollie Gordon II | MIA | -- | | 0.50 | 50-70 | Achane |
| Jadarian Price | SEA | 0.48 | 40+ | -- | | Charbonnet (no week-one snaps for the leader: C blank) |
| Chris Brooks | GB | 0.36 | 30-40 | -- | | Jacobs (no week-one snaps for the leader: C blank) |
| Samaje Perine · Kenny Gainwell | CIN · TB | 0.27 · 0.29 | 20-30 | -- | | no snap row joined (below) |
| Pacheco · Giddens · Ty Johnson · Blue · Kamara · Henderson | | -- | | -- | | no week-one line at all: the page's flat 0.46, starred |

On the two rows where the bands disagree by two or more, section 3 says the snap band is the one
that carries the RATE: Robinson and Hill are each the only other back on the field, and the history
scores that man 13.0 a game, not the 8.9 of a man who splits the backup snaps. **The page prices
both at the 20-30 odds (0.474) and at the one rate, which is right for the odds and blind to the
rate.** Hill is not a free seat (Henry's backup is rostered); Robinson is, and he is 7th of 7 in
section 1 at the 20-30 odds.

**TWO JOIN DEFECTS, both section 3's identity rule, both live on the page tonight:**

1. **`share_2026()` joins on the NAME ALONE and one row takes its share from another club's
   backfield.** (Doc 347 §3a, filed while this ran, found the same row's TEAM is stale, built off
   the 7 Sept pull; this is the other half: even with the team fixed, the join cannot tell.) The KC row names Emari Demercado behind Kenneth Walker III and prints `wk1_share`
   0.100; **Demercado's week-one line is Dallas's** (2 carries of a 20-touch DAL backfield), and he
   has no Kansas City line at all. The seat is priced off a share of the wrong pie. Ledger row 43
   already corrected his club on the wire; the seat file did not get the memo, and the join could
   not tell. The fix is the rule already in the file's own comment (name + team, blank on a miss),
   and it belongs to the session that owns `job_opens.py`.
2. **The seat file carries ESPN's club codes and nflverse carries its own** -- ARZ against ARI, LAR
   against LA (WSH/WAS and JAC/JAX would be next). A team-aware join without the map returns blank
   for Allgeier and Corum; a name-only join hides it. `j2_share_and_rate.py` maps the four.
   Separately, **Kenny Gainwell is `Kenneth Gainwell` in the snap file** and joins to nothing; a
   nickname alias is not in the normaliser and one man on the live list is blank for it.

---

## 5. 2021 ADDED, THE CONTROL, AND A VINTAGE NOBODY HAD PINNED (`j2_bands_2021.py`)

`job_opens.study()` (doc 343's script) was run unchanged, twice, with its cache pointed at a
directory of the seasons wanted. **CONTROL FIRST: on 2022-2025 it reproduces the shipped bands
exactly** -- 0.476 / 0.438 / 0.533 / 0.636 on n = 42 / 32 / 30 / 22 -- **but only on the drive's own
cache files.** On the weekly files nflverse serves today (downloaded 16 Sept and again this
morning: 114 columns, 6.8 MB, last modified May 2025) the 30-40 band is 0.517 on n=29 and 40+ is
0.652 on n=23: two team-seasons sit on the 30/40 edge and the two releases put them on opposite
sides. **The drive's 2022-2024 files are a different release -- 150 columns, 8.4 MB, 2022 holds
1,581 regular-season RB rows against 1,545** -- and nothing records which release a number was
computed on. `job_opens.py` reads whatever is in `_nflverse_cache\`. The 2025 file is the same in
both. **This is the section-1.1 provenance rule one level down: a cache without a vintage is an
ADP without a capture date.** Direction and verdict are unaffected; the third decimal is.

**FIVE SEASONS, on the drive's files plus a fresh 2021 (n=157):**

| band | four seasons | n | **five seasons** | n | on the current release |
|---|---|---|---|---|---|
| <20 | 0.476 | 42 | **0.510** | 51 | 0.510 (51) |
| 20-30 | 0.438 | 32 | **0.474** | 38 | 0.474 (38) |
| 30-40 | 0.533 | 30 | **0.564** | 39 | 0.553 (38) |
| 40+ | 0.636 | 22 | **0.621** | 29 | 0.633 (30) |

2021 alone opens 0.645 of the time on n=31, the highest season, which is why every band rises and
the spread narrows (top minus bottom 0.11 against 0.16). Seats-only permutation at a 35% split:
**+0.34, p=0.019** (was +0.36, p=0.023); all rows +0.05, p=0.34 (was +0.10, p=0.21, never
significant unfiltered). **The falsifier -- a reversed gradient or a lost seats-only significance --
does not fire.** The 2021 season leaves the direction alone and shrinks the size by a third, which
is the conservative way for a constant to move, and it is now in `sheet_constants.json`
(section 6).

**T5 ON THE SAME ROWS, FOR THE ODDS:** 0.556 / 0.536 / 0.474 / 0.549 on n = 18 / 28 / 19 / 91.
Flat (70%+ against under: −0.007, p=0.60). 91 of 156 backfields are 85%+ on week-one snaps -- most
rooms are two men deep on the field in week one -- so the measure has no room to order them. The
week-one work share does order them, weakly. `[TESTED, n=156]`

---

## 6. THE NETTING QUESTION (ITEM 6), IN NUMBERS

*Should a seat be netted against a drop at all when the claim is a stash for a man not yet hurt?*
The alternative to the stash is not "no seat"; it is **claiming him AFTER the news**, when the
drop is only spent if the job actually opened. Write F for what the seat is worth if it fires (the
relief rate over the bar, for the weeks it stays open), p for the odds, D for the drop's cost over
the horizon, D' for its cost over the weeks that remain once the job opens (D' ≤ D), and q for the
chance you land him after the news (bounded by doc 344's claimant's-seat contest rate, 30% to 82%
by touches, and by where the order puts you that week):

- stash now: **p·F − D**
- claim after the news: **p·q·(F − D')**
- the stash is right when **p·F·(1 − q) + p·q·D' > D**

So yes, the stash IS netted against a drop -- the drop is paid whether or not the job opens, and
the post-news claim only pays it when it does -- and the netting is against the drop you would
actually make, not the cheapest one in the file. **On this wire the answer does not depend on q.**
The seat's whole value at certainty (F, solved from the break-even columns in `J2_seats_by_odds.csv`)
is 4.2 to 4.7 points; against Worthy at 4.91 the stash loses even at q = 0, and against Brooks at 0.01 it wins
even at q = 1. The question would bite on a roster whose cheapest real drop sat between about 2 and
4 points, which is where the 16 Sept roster was (Hockenson 2.7) and where doc 327's inference came
from. It is not where the 18 Sept roster is.

---

## 7. WHAT WAS WRITTEN, AND HOW IT WAS VERIFIED

| file | what | verified |
|---|---|---|
| `Scripts\research\j2\j2_seat_odds_matrix.py` | doc 327's harness with `seat_odds()` and the break-even solve | run in full, control PASS, output beside it |
| `Scripts\research\j2\j2_share_and_rate.py` | sections 2, 3, 4 | run in full; `J2_events.csv` 114 rows |
| `Scripts\research\j2\j2_bands_2021.py` | section 5 | control reproduces the shipped bands to the third decimal before the extension runs |
| `Scripts\research\j2\J2_*.csv`, `J2_*_summary.json`, `run_*.txt` | every table above | the doc's numbers were read from these files, not from memory |
| `Source\sheet_constants.json` | `seat.p_opens_by_band` and `_n` to the five-season numbers; the note says what it replaces and the vintage | staged back off the drive and read by content; `json.load` clean |
| `Source\AUDIT_LEDGER.md` | rows 106 to 111 | staged back, row count checked |
| `Source\matt_todo.txt` | one comment line under the open `ff.bat` item: the rebuild also picks up the five-season odds | staged back |

**NOT changed, deliberately:** `sheet_engine.py`'s two captions still say "on four seasons" (lines
1228 and 1300). The file is pinned in `check_kit.py` and is open in the other session; a two-word
edit there needs a re-pin in a third file, and the risk of a stale-copy commit across sessions
(ledger rows 56, 81, 89) is larger than the cost of a caption that is one season out for one
rebuild. It is on the open list for that session. The seat scripts on Matt's machine need
`stats_player_week_2021.csv` and `snap_counts_2021..2025.csv`, which the scripts fetch into
`_nflverse_cache\` on first run (internet), and `snap_counts_2026.csv`, which `build_form.py`
already writes.

---

## 8. OPEN, BY NAME

- **A rate band on the seat lane, keyed on T5 to date.** Section 3's 9.3 → 14.1 is a bigger lever
  than the odds bands the page just gained, and the input (`snap_counts_2026.csv`) is on the drive
  since doc 309. NOT YET RUN as a page change; the measurement is done. Whether it also needs a
  "same man on both bands" guard (Robinson, Hill) is part of it.
- **`share_2026()`'s name-only join** (section 4, Demercado) and the club-code map; the Gainwell
  alias. Owner: the session that owns `job_opens.py`.
- **The two "four seasons" captions in `sheet_engine.py`.** Owner: the other session, with the
  re-pin.
- **A vintage stamp for `_nflverse_cache\`** -- which release each file came from -- or a fetch
  that always takes the current one. Nothing records it now (section 5).
- **The weeks reversal** (section 3): pre-register it and re-run on the 2026 events at season's end.
- **JOB 3 and JOB 4**, queued in the tasking prompt, not started.
- Carried from doc 344 and doc 345: the contest sentence on the claimant's-seat rate; C22; the K
  and D/ST double count in the ladder; the script behind 12.13 and 3.02 (section 3 reproduces both
  within 4% and 14% on doc 320's population, which is a second population, not the script).
