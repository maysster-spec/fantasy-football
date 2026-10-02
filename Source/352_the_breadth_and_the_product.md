# 352 -- THE BREADTH AND THE PRODUCT: BOTH DEAD, AND THE PAGE KEEPS RANKING BY THE ODDS

**2026-09-18, 08:55 EDT.** FABLE JOB 3 (`FABLE_JOB3_seat_lane.md`, written 18 Sept, read off the
drive). Both tasks were run with their testable forms and kill conditions as the brief fixed them,
and both died on those conditions. The brief asked for this file as `349_the_breadth_and_the_product`;
349, 350 and 351 were taken by the other session while the tasks ran (and 349 was claimed twice for a
quarter of an hour before one was renamed), so the name keeps the title and takes the next free
number, checked against the folder at commit time. Scripts and every output are in `Scripts\research\j3\`.
Nothing touched ESPN, a claim, a drop, or `sheet_constants.json`.

---

## 0. THE TWO CLAIMS AS FIXED, AND WHAT HAPPENED TO EACH

| task | the claim, as pre-registered in the brief | kill condition | verdict |
|---|---|---|---|
| **A** | Among direct backups who inherited an absence, the COMPOSITION of his pre-absence work (breadth: mixed against lopsided) predicts the share of the starter's vacated work he captures, over and above his TOTAL pre-absence work share; mixed captures more | under 3 points per 1.0 of breadth, or p above 0.10, is dead | **DEAD.** Breadth adds **-5.4 points**, se 10.2, **p=0.60** (team-clustered p=0.61), R-squared up 0.002 on n=112. The sign is the wrong way and nowhere near significant. Same verdict on the actual first-week inheritor (+10.9 points, p=0.21) and on every sensitivity |
| **B** | Expected relief points = P(inherits given the week-one share band) x relief ppg (given the T5 band), and the two are independent enough inside the seats that the product is a fair estimate | the product must beat the better single instrument by at least 0.05 of Spearman rho against realised relief points | **DEAD, decoration.** Against realised relief points on 156 seats: odds alone **+0.162** (p=0.039), rate alone **+0.041** (p=0.60), odds x rate **+0.139** (p=0.087). Product minus the better half **-0.023**, bootstrap 95% [-0.109, +0.044]. **The page keeps ranking by the odds and prints the rate as its own column** |

**Nothing live in `sheet_constants.json` changes.** No key, no value.

---

## 1. TASK A -- ROLE BREADTH (`j3_breadth.py`)

**POPULATION, restated (0.6):** doc 320's 114 absence events, 2021-2025, weeks 2-14: the team-week in
which the back who led his team in carries plus targets to date played the previous week and has no
line this week while his team plays; one event per absence, its first week. Rebuilt by the same
function (`b2_depth_order.build_events()`) on the same files as JOB 2, and the count asserted at 114.
The backup is the usage order's man, the man the page names (doc 320); the actual first-week
inheritor is a sensitivity. The spell is the run of team-played weeks from the event week with no
line for the leader, capped at week 14, as in JOB 2 and as the sheet prices.

**The filters, and what each costs:** 114 events; 112 have a named usage man (two backfields had no
second back with a line in the first absence week); 112 have a spell of at least one week and a
starter per-game rate; **112 backups touched the ball before the absence, so breadth is defined on
112 -- nothing was lost to the breadth definition.** Team clusters: 32.

**PREDICTOR:** breadth = 1 - |targets / (carries + targets) - 0.5| x 2 on weeks 1 to w-1. Median
pre-absence work 36.5 carries plus targets (IQR 22 to 62); median target ratio 0.23; median breadth
0.46. **OUTCOME:** the backup's carries plus targets over the spell, divided by the starter's
per-game carries plus targets before the absence times the spell length, capped at 1.0.
**The cap binds on 53 of 112 rows** (raw mean 0.98, capped mean 0.79): half the backups take MORE
work in relief than the starter had been averaging, because the starter's per-game work was already
shared with the backup and the backup keeps his own share on top of the vacated one. That is a
property of the brief's outcome definition, not of the men, and the uncapped outcome is run beside
it.

| model | n | R2 | share_pre | breadth |
|---|---|---|---|---|
| M1 captured ~ share_pre | 112 | 0.091 | **+0.761**, se 0.229, p=0.001 (clustered se 0.221, p=0.002) | -- |
| M2 captured ~ share_pre + breadth | 112 | 0.094 | +0.755, se 0.230, p=0.001 | **-0.054**, se 0.102, **p=0.596** (clustered se 0.106, p=0.612) |
| M3 captured ~ share_pre + target_ratio | 112 | 0.111 | -- | target_ratio -0.263, se 0.168, p=0.121 (clustered p=0.201) |

**Breadth adds -5.4 points of captured share per 1.0 of breadth, p=0.60: DEAD on the first kill
condition and on the second.** Total pre-absence work share is the whole of what is measurable
here: +0.76 of captured share per 1.0 of share (a backup at 30% of the pre-absence work captures
about 15 points more of the vacated job than one at 10%), and it carries the same coefficient with
or without breadth in the model. Breadth terciles say the same thing with the confound visible:
low 0.18 breadth / captured 0.775 / share_pre 0.265 · mid 0.46 / 0.833 / 0.317 · high 0.76 / 0.771 /
0.250. The middle tercile captures most because it has the most work, not because it is mixed.

**Which end, because the fold hides it:** carry-specialists (target ratio under 0.15, n=31) captured
0.768; mixed (0.15 to 0.50, n=74) 0.829; **target-specialists (over 0.50, n=7) 0.523.** That last
cell is the shape Matt described (a pass-catching back absorbs only the passing downs that were
already his), and it is seven men, with a raw target-ratio coefficient of -0.26 at p=0.12. A shape,
not a finding, and underpowered by a factor of about four.

**Sensitivities, all dead:** uncapped outcome, breadth -0.219, p=0.19 · backups with 10 or more
pre-absence touches (n=100), breadth -0.173, p=0.10 (clustered p=0.09), the WRONG sign for the claim ·
the actual first-week inheritor instead of the usage man (n=102, 53 capped), breadth +0.109,
p=0.21, clustered p=0.11, and its share_pre coefficient is +0.10 at p=0.54, so on that arm nothing
predicts capture at all.

**WHAT WOULD RESOLVE IT, the named input.** Breadth on TOUCHES is a noisy instrument for a man with
a median of 36 of them: a backup with 30 carries and 6 targets and one with 30 carries and 12
targets are a tercile apart on breadth and the same player on the field. The role measure that
would answer the claim is on SNAPS: the backup's pass-play snaps against his run-play snaps before
the absence. nflverse publishes it as the participation release (`pbp_participation_<season>.csv`,
one row per play with the offensive players on the field; which seasons it covers today was not
checked for this doc and is the first thing to check), and PFF's
receiving export carries `routes` (the drive's `pff_receiving_2022-2025.csv` are season totals; a
per-week cut would have to be pulled from PFF, which Matt has). Either gives a role split
that does not depend on whether the ball came to him. **NOT YET RUN**, and the participation file
is one fetch away; it was not fetched for this doc because the claim died on the touch measure with
room to spare in either direction, and a second instrument is a second test, not a rescue of this
one.

---

## 2. TASK B -- DO THE ODDS AND THE RATE MULTIPLY (`j3_product.py`)

**POPULATION, restated (0.6):** doc 348 section 5's seat rows, 2021-2025, n=157: every team-season
whose week-one RB usage leader and second back both played in week one with combined RB carries
plus targets of 10 or more; one row per team-season, the seat is the second back. Rebuilt with
`job_opens.py`'s own reader on the same cache files, and asserted equal to
`J2_job_opens_rows_2021_2025.csv` on every share and every opens flag before scoring. OPENS: the
leader misses a team-played week in 2-14 (84 of 157, 53.5%). REALISED RELIEF POINTS: the seat's
half-PPR over the leader's absence weeks in 2-14, zero when it never opened (mean 16.4, median 0.0);
REALISED RELIEF PPG over the absence weeks he had a line (77 seats, 11.24 a game). T5 joined on 156
of 157 (Samaje Perine, CIN 2025, has no week-one snap row).

**STEP 1 -- are the two instruments one signal?** rho(week-one work share, T5) = **+0.330, p=0.0002,
n=156**; Pearson +0.362, so they share 13% of their variance. Correlated, not the same thing: the
product is not a double count by construction. It fails below for a different reason.

**STEP 2 -- the cross.** T5 quartile cuts fall at 0.62 / 0.91 / 1.00, and **60 of 156 seats sit at
exactly 1.00** (a two-man room in week one), so the top two quartiles are 18 and 60 rows, not 39
and 39; the brief's quartile design cannot make four equal cells on this measure.

| share band | T5 Q1 (0.20-0.62) | Q2 (0.62-0.91) | Q3 (0.92-0.97) | Q4 (1.00) |
|---|---|---|---|---|
| <20 | n=19, opens 0.58, ppg 7.75 | n=14, 0.50, 10.76 | n=2 (no conclusion) | n=15, 0.47, 11.53 |
| 20-30 | n=12, 0.50, 9.76 | n=8, 0.50, 10.80 | n=7 (no conclusion) | n=11, 0.36, 10.89 |
| 30-40 | n=8, 0.63, 9.02 | n=12, 0.42, 11.84 | n=4 (no conclusion) | n=15, 0.67, 12.60 |
| 40+ | n=0 | n=5 (no conclusion) | n=5 (no conclusion) | **n=19, 0.68, 14.63** |

Margins: by T5 quartile the relief ppg runs **8.66 / 10.77 / 11.20 / 12.90** and P(opens) is flat
(0.56 / 0.46 / 0.56 / 0.57), which is doc 348's split of the terms reproduced on a second
population. By share band P(opens) runs 0.52 / 0.47 / 0.56 / 0.62, which is the constant by
construction, and relief ppg runs **9.91 / 10.35 / 11.23 / 13.82** (n 22 / 16 / 22 / 17). **That
last row is a correction to doc 348's reading, not to its number.** Doc 348 measured the relief rate
flat against the week-one share on the usage order's man at the absence week. On the week-one
SEATS, the same share is not flat on the rate: the 40+ seats that open score 13.8 a game and 27
relief points against 13 for the rest. Two populations, two men: the week-one second back and the
usage-order man at week w are the same person on most rows and different people on the rows that
matter. Neither share-band gradient reaches significance on 77 opened seats (odds score against
realised ppg, rho +0.19, p=0.09; T5 rate score, +0.16, p=0.16), so on this population the two
instruments are indistinguishable as rate predictors.

**STEP 3 -- three scores against realised relief points, n=156.** Odds = the five-season band
probabilities now on the page (0.510 / 0.474 / 0.564 / 0.621, in-sample on these seasons). Rate =
doc 348's relief ppg by week-one T5 band, measured on the 114 events (8.91 / 12.55 / 14.69 / 12.98,
and note it is not monotone: the 85+ band sits below 70-85). Product = odds x rate.

| score | rho against realised relief points | p |
|---|---|---|
| **odds alone** | **+0.162** | 0.039 |
| rate alone (doc 348 T5 bands) | +0.041 | 0.60 |
| odds x rate | +0.139 | 0.087 |
| rate alone, in-sample T5-quartile means (8.66 / 10.77 / 11.20 / 12.90) | +0.098 | 0.23 |
| odds x rate, in-sample rate | +0.154 | 0.053 |

**Product minus the better half: -0.023, bootstrap 95% [-0.109, +0.044] (2,000 draws). The
product does not clear +0.05 under either rate, so on the brief's own kill condition it is
decoration.** Why: realised relief points are zero on 73 of 156 seats, so the ranking is
dominated by whether the seat opened, and the rate half carries no information about that (its
rho alone is +0.04). Multiplying a weak opens-predictor by a term that does not predict opens
adds noise to the ranking of the zeros. The one place the product wins is the secondary view the
brief did not ask to be scored: among the 77 seats that opened, against realised PPG, the product
is +0.234 (p=0.038) to the odds' +0.194 and the rate's +0.164. That is the rate doing its job on
the men it was built for, and it is what a separate rate column is for.

**THE PAGE:** rank by the odds; print the T5 rate as its own column beside "if it fires" so the
reader can see a 9-a-game seat from a 14-a-game seat without the number entering the sort. That
is the same recommendation doc 348 section 8 made, now with the product tested and dead.

---

## 3. THE DELIVERABLE CSV

`Scripts\research\j3\J3_seats_2021_2025.csv`, 157 rows, one per seat: season, team, the leader,
the seat's name, week-one share and band, T5 and its quartile and doc 292 band, breadth and target
ratio (on the weeks before the first absence, or weeks 1-14 if it never opened; pre-absence carries
and targets beside them), whether it opened, the first absence week, absence weeks, weeks he had a
line, realised relief ppg and points, and the five scores from Task B step 3 (odds, rate, product,
in-sample rate, in-sample product). Task A's rows are `J3_breadth_events.csv`, 114 rows, both arms.

The largest realised seats, for the reader: Kyren Williams 2023 (share 0.44, T5 1.00, 12 absence
weeks, 154 points), Gus Edwards 2023 (0.30, T5 0.44, 135), Jerome Ford 2023 (0.41, 1.00, 122),
Chase Brown 2024 (0.32, 1.00, 98), D'Onta Foreman 2022 (0.11, 0.70, 91). Two of the five are in the
top share band, one is in the bottom, and one has a T5 under 0.5: the tail is where the instruments
are weakest, which is §4.13d's point about ceilings restated.

---

## 4. WHAT WAS WRITTEN, AND HOW IT WAS VERIFIED

| file | what | verified |
|---|---|---|
| `Scripts\research\j3\j3_breadth.py` | Task A; OLS with classical and team-clustered standard errors in numpy, a Student t by numerical integration (no scipy) | run in full; event count asserted at 114 |
| `Scripts\research\j3\j3_product.py` | Task B | run in full; the 157 seats asserted equal to doc 348's rows on every share and opens flag |
| `J3_breadth_events.csv`, `J3_seats_2021_2025.csv`, `J3_breadth_summary.json`, `J3_product_summary.json`, `run_j3_breadth.txt`, `run_j3_product.txt` | every number above | read from these files |
| `Source\AUDIT_LEDGER.md` | rows 113 to 117: the two deaths, the cap, the population qualification, the quartile collapse | staged back off the drive, row count checked |

Both scripts fetch `snap_counts_2021..2025.csv`, `players.csv`, `depth_charts_2021..2025.csv` and
`games.csv` into `research\_nflverse_cache\` if absent (internet), and read the weekly files
already there; on the drive `stats_player_week_2021.csv` must be present too, which `j2_bands_2021.py`
fetches (doc 348 section 5 on the cache's two vintages applies here unchanged).

---

## 5. OPEN, BY NAME

- **Breadth on snaps** (section 1's named input): nflverse `pbp_participation_<season>.csv` or PFF
  weekly routes. NOT YET RUN.
- **A T5 rate column on the seat lane, display only** (doc 348 section 8 and section 2 above).
- **The share band's rate gradient on the seats** (section 2, 9.9 to 13.8, n=17 in the top band):
  not significant, and the JOB 2 flat result stands for the man it was measured on; pre-register a
  rate test on the SEAT population if the page ever prices the rate by the share band.
- Carried from doc 348: the name-only join in `share_2026()`, the club-code map, the two "four
  seasons" captions, the cache vintage stamp, JOB 4, the store cap.
