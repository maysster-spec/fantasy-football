# 302 -- the second back was often the first, and the squeeze was the denominator

**13 September 2026. Second reader on docs 291 to 300.** Six attacks in the order they were
ranked. Two findings die, one dies and is replaced by a bigger one, three survive intact and are
recorded as surviving. Every table below is **2021-2024**, not 2021-2025.

**BLOCKED, exact missing input named (0.5a4): `stats_player_week_2025.csv`.** nflverse's public
release, read from its own asset list, carries 2012 through 2024 and 404s on 2025. The 2025 file is
on Matt's machine because docs 297, 299 and 300 ran on it. **Both scripts shipped with this doc take
`--years` and will pick 2025 up on his tree with no edit.** Until then every n here is about four
fifths of the doc's.

Scripts: `Scripts\research\wk1\wk1_redteam.py`, `Scripts\research\f1\squeeze_redteam.py`. Stdlib
only, paths resolved against the script's own folder, no scipy, no shell-out.

---

## 1. DOC 300 -- the arithmetic reproduces, the startable half does not survive

**It reproduces almost exactly**, which is the first thing worth saying. On four of the five seasons:

| RB2's share of week-1 backfield work | n | wks 2-14 ppg | reached 9.92 | doc 300 |
|---|---|---|---|---|
| under 20% | 32 | 4.97 | 6% | 4.99 / 7% |
| 20 to 30% | 29 | 4.94 | 7% | 5.22 / 11% |
| 30 to 40% | 33 | 8.31 | 39% | 8.35 / 39% |
| 40% or more | 24 | 10.46 | 50% | 10.28 / 50% |

**AND THE 35% CUT IS NOT CHOSEN.** I ran every split from 15% to 45%: all seven separate, ppg
`p<=0.0103` at every one, and the **cut-free rank correlation between share and points is +0.464**.
The bands do not have to be trusted for the scoring result to stand. That objection is closed.

### 1a. The confound the design does not exclude does NOT kill it

**Testable form, stated before the run:** *if the week-1 share only predicts because a high-share
backfield belongs to a lead back who later gets hurt, then among team-seasons whose lead back played
every week 2 to 14 the gradient disappears.*

**It does not disappear.** On the 47 team-seasons where the lead back never missed a week:
3.94 / 4.06 / 7.39 / 11.38, and **35%+ against under 35% is +5.10 ppg, p<0.0001**. Scoring RB2 only
in the weeks the lead back had a line gives the same answer. `[TESTED, n=47 and n=117]`

**But the predictor IS correlated with the confound, and that changes how it must be used.**

| band | lead back missed a game | mean weeks missed |
|---|---|---|
| under 20% | 59% | 2.25 |
| 20 to 30% | 48% | 1.62 |
| 30 to 40% | 58% | 1.58 |
| **40% or more** | **79%** | **2.92** |

A near-even week-1 split partly marks a lead back the team is already managing. **So the share and
the seat model's job-opens probability are not substitutes, and doc 300 section 3 proposes to treat
them as substitutes.** See item 6 below.

### 1b. THE KILL: in the top band the second back was usually the first back

`week1_share.py` ranks by week-1 work and takes `lst[0]` as the lead. **The docstring's exclusion --
"the team's leading week-1 back must have PLAYED in week 1 (if he did not, the job was already open,
doc 294's event)" -- is true by construction and excludes nothing.** Doc 294's event is fully inside
the population.

Checked directly: did the man labelled the lead back lead his own team in weeks 2-14 carries plus
targets?

| band | labelled RB1 did NOT keep the lead |
|---|---|
| under 20% | 10 of 32 (31%) |
| 20 to 30% | 7 of 29 (24%) |
| 30 to 40% | 13 of 33 (39%) |
| **40% or more** | **14 of 24 (58%)** |

The top band contains **James Conner behind "lead back" Chase Edmonds, Jahmyr Gibbs behind David
Montgomery, Bijan Robinson behind Tyler Allgeier, Rhamondre Stevenson behind Damien Harris, Kyren
Williams behind Cam Akers (0% of the rest-of-season work), Jerome Ford behind Nick Chubb (3%), Tony
Pollard behind Ezekiel Elliott.** These are not handcuffs who broke through. They are starters the
labelling put in the wrong column.

**On the 74 team-seasons where the labelled lead back really was the lead back:**

| band | n | ppg | reached 9.92 |
|---|---|---|---|
| under 20% | 22 | 4.42 | 0% |
| 20 to 30% | 22 | 4.44 | 5% |
| 30 to 40% | 20 | 6.15 | 20% |
| 40% or more | 10 | 7.57 | **20%** |

**35%+ against under 35%: ppg +2.12, p=0.0063; startable rate +2 points, p=0.5553.** `[TESTED, n=74]`

**The scoring half survives at half its size. The startable half is gone.** Doc 300's headline number
is 50% and the ledger row 29 carries it into the Tuesday read; on this cut it is 20% against a 9%
base. The doubling survives. **The 50% does not, and it should stop being quoted.**

**And the tie-break is arbitrary at exactly the place it matters.** `lst.sort(reverse=True)` on
`(work, player_id)` breaks a 50/50 split on the player-id string. 2021 Arizona is 50/50: sorted one
way the row is James Conner at 16.8 a game, sorted the other it is Chase Edmonds at 8.8. **Nine rows
sit at 45% or above.** At a near-even split there is no second back, there are two backs.

### 1c. The population is not the claimable population, but this does NOT hurt Black

**21 of 118 team-seasons, and 9 of the 24 in the top band (38%), are men who were startable fantasy
backs the previous season** -- Gibbs, Conner, Ezekiel Elliott, Najee Harris, Kenyan Drake, Gus
Edwards, Melvin Gordon, James Robinson, Nyheim Hines. In a 12-team league none of them was a claim.

Restricted to backs who were NOT startable the prior season, the table gets **stronger**, not weaker:
4.66 / 4.58 / 7.97 / **10.83 at 60%** (n=97, ppg +4.37, p<0.0001). **So the contamination is not what
carries the result, and Kaelon Black's own case is not weakened by removing it.**

**The cell Black is actually in -- a claimable back whose lead man misses time -- is n=62 and its top
band is 10.70 a game at 57% (p=0.0027).** The cell where the lead man stays healthy has **one** row
in the top band. **The signal is real and it is conditional on the man ahead, which is the opposite
of what doc 300 section 3 plans to do with it.**

---

## 2. DOC 297 -- three problems, one of them in a shipping constant

**(a) The rates re-measured, and the QB cell is not stable.** Same design, 2021-2024:

| pos | n | share of weeks missed | shipping |
|---|---|---|---|
| QB | 46 | **8.7%** | 13.7% |
| RB | 94 | 18.0% | 17.1% |
| WR | 96 | 13.4% | 15.0% |
| TE | 47 | 16.2% | 13.7% |

RB and WR reproduce. **QB is off by 5 points, and doc 297's own per-season row explains why: 8 / 13 /
13 / 22.** A cell that runs 8% to 22% across four seasons is not, as the doc says two lines earlier,
*"stable and not one bad year"*. **That sentence is contradicted by the numbers printed beside it**,
and the QB rate is one of the two inputs to the Shough result the doc leans on.

**(b) The intervals are Monte Carlo, not uncertainty.** `-0.98 +/- 0.02` is the standard error of the
mean over 6,000 draws. The uncertainty that matters is in the 17.1% RB rate, measured on 94 player
seasons, which is roughly 2 percentage points clustered by player -- an order of magnitude more than
the quoted interval carries. **0.2 says a severity estimate must be measured; it must also be
reported with the interval of the thing that is actually uncertain.**

**(c) Independence understates depth, in a known direction.** The drop cost is the expected best legal
nine with the man minus without him, and best-legal-nine is a maximum over the available set, so it
is convex in the availability vector. Independent per-man draws produce fewer weeks with several men
out at once than reality does, and several-out-at-once is the only state in which a bench body enters
the lineup. **So every drop cost in section 3 is a lower bound on the value of holding the body.**

**(d) The streamer rate is the wrong counterfactual for a drop, and it errs the expensive way.**
Doc 12's numbers are rest-of-season points from an add Matt chose in advance. A refill after a drop
happens at the moment the hole appears, with the injury already known. **Doc 259 measured his actual
best free bodies at RB 6.51 and WR 8.94 against doc 12's 5.43 and 6.54.** The wire recomputes the
free pool every week; use its best-available at the position, not a four-year average add.

**(e) Yes, the handcuff bracket depends entirely on the relief rate applying only in Jeanty's missed
weeks, and the doc says so.** The residual problem is a collision: **doc 297 uses 11.2 (doc 244,
n=40) and `sheet_constants.json` ships `seat.relief_ppg` at 12.13 (n=51) for the same object.** Two
numbers for one quantity is 0.5(c)4 applied to a constant. Also 11.2 is a MEDIAN used as an
EXPECTATION, which is only right if Washington is the median relief back, and doc 300's own share
table is the thing that would tell you which side of it he is on.

---

## 3. DOC 299 -- the placebo fires, and the confirmed half is the denominator

**Testable form, stated before the run:** *if the arrival squeezes THE ROOM BELOW, then (i) the same
test on the 2nd receiver, whom the claim says nothing about, should be null or weaker, and (ii) the
effect should survive taking the arrival out of the denominator.*

**Both fail.**

**The null choice is fine and that part is closed.** Doc 299 permutes the arrival label within team.
Permuting within season instead gives the same direction at the same or smaller p on every slot.
The within-team null is the conservative one, correctly chosen.

**DESIGN 1, doc 299 as published -- share of all team WR targets:**

| slot | arrival | none | difference | p (within team) |
|---|---|---|---|---|
| 1st, the incumbent | -0.031 | -0.006 | -0.025 | 0.275 |
| **2nd, the placebo** | **-0.032** | **+0.017** | **-0.049** | **0.0018** |
| 3rd + 4th (doc 299) | -0.001 | +0.021 | -0.022 | 0.0138 |

**The 2nd receiver, who is outside the claim, is hit twice as hard as the room below.** That is the
placebo failing.

**DESIGN 2 -- the same men in the denominator on both sides, arrival excluded:**

| slot | arrival | none | difference | p (within team) |
|---|---|---|---|---|
| 1st, the incumbent | +0.000 | -0.025 | +0.025 | 0.87 |
| **2nd** | **-0.032** | **+0.013** | **-0.045** | **0.011** |
| 3rd alone | +0.009 | +0.021 | -0.011 | 0.32 |
| 4th alone | +0.025 | +0.027 | -0.002 | 0.27 |
| **3rd + 4th** | **+0.016** | **+0.023** | **-0.008** | **0.21** |

**The 3rd-and-4th effect vanishes. What is left is the 2nd receiver.** `[TESTED, n=42 vs 59
team-seasons]`

A share is a share of one hundred percent. Adding a man who takes targets lowers everyone's share
whether or not anybody was squeezed, and the arrival is in this season's denominator and not last
season's. **Doc 299's claim 1 measured that arithmetic.** Doc 299 names the mechanism -- *"when a
receiver arrives, team targets rise and every share falls a little for reasons that are not a
squeeze"* -- and then applies the correction only to claim 2. It belongs to claim 1 as well, and once
applied, claim 1 is where claim 2 already was.

**The sign flip the doc leans on goes too.** *"Without an arrival that group GROWS (+0.027); with one
it shrinks"* becomes +0.023 against +0.016. Both grow.

**AND THE LIVE ROW MOVES TO A DIFFERENT MAN.** Denver's squeezed receiver is not Pat Bryant, the
4th man. On the only design that separates a squeeze from dilution it is **Troy Franklin, the 2nd**
(104 targets in 2025). **Matt's own words survive better than the doc's test of them:** he said the
arrival compresses everyone below, and the reallocation is real, it is just not concentrated where
doc 299 looked. **Take the arrival caution off Bryant's 3-of-3 tag and put a watch line on Franklin.**

**AUDIT_LEDGER row 27 needs amending**: claim 1 is confirmed only in the arithmetic sense, and the
claim-2 form remains unresolved for the room below and newly suggestive for the second man.

---

## 4. THE P-VALUES -- multiplicity is not what threatens either doc

Counted, per doc, and stated plainly because the honest answer is boring.

**Doc 300** reports four bands and one split against two outcomes, about ten comparisons. Its ppg
p is under 0.0001; Bonferroni at ten leaves it under 0.002, and the cut-free rank correlation
(+0.464) needs no correction at all. **Multiple comparisons do not touch it. The population does.**

**Doc 299** pre-stated both claims, and reports three vacated-share bands. The unreported degree of
freedom is the slot grouping -- 2nd, 3rd, 4th, 3+4, 2+3+4 is five choices and only one was published.
Bonferroni at six still leaves p=0.03. **Multiple comparisons do not touch it either. The denominator
does.** The slot choice matters for a different reason: the untested slot is where the effect is.

**Doc 294** is the one that ran dozens and it says so, labels section 4 SUGGESTIVE, and reports the
committed script disagreeing with the first draft (+4.6 p=0.63 against +17.9 p=0.061). At roughly
thirty comparisons a p of 0.003 is about 0.09 corrected. **The SUGGESTIVE label is the right call and
no change is needed.** Doc 292's *"none clears the multiple-comparison bar"* is likewise correct.

---

## 5. THE [INHERITED] NUMBERS NOW SHIPPING -- seven defects in one file

`Source\sheet_constants.json`, `absence` block added 12 Sept 16:48, and `seat`.

1. **`absence.rate.K = 0.137` is not a kicker number.** The note says the kicker cell *"is not used"*,
   but the value sits in a dict a lookup will find, and 0.137 is the QB and TE rate. The measured
   kicker rate is 0.213, so if anything reads the key it under-states kicker absence by a third.
   **Delete the key or set it to 0.213.**
2. **`absence.streamer.K = 7.5` has no source.** The note attributes QB, RB, WR, TE and D/ST and says
   nothing about K. Section 3 calls that `[NO SOURCE]`.
3. **RB 5.43, WR 6.54 and TE 5.53 inherit from doc 12, which 4.17 has already re-tagged
   `[SOURCED, n irreproducible]`.** Only the QB number was re-derived. `[INHERITED]` is doing a lot of
   work there and should read `[INHERITED from doc 12, n irreproducible per 4.17]`.
4. **The population is written two ways.** The JSON says nflverse **2022-2025**; doc 297 says
   **2021-2025**. Same measurement, two spans, and 0.6 exists because of exactly this.
5. **The doc and the artifact disagree about whether anything shipped.** Doc 297 section 6:
   *"No code change shipped today. The sheet still prices byes only and says so on its own face."*
   The JSON note: the block exists *"so the page can price a bench body instead of printing 0.0 for
   him."* One of those is wrong, and if it is the doc, **the page's own printed disclaimer is now
   false**, which is worse than either.
6. **`seat.p_opens_note` asserts a null the ledger has already reopened.** It states flatly
   *"It does NOT vary by history: 45.9% ... against 46.3% ..., p=0.60"*, with no flag. AUDIT_LEDGER
   row 2 records doc 276's null as under re-check under catalog B4, because its population held only
   backs healthy through week 4.
7. **Two numbers for the relief rate**, 12.13 in the constants and 11.2 in doc 297's bracket, and
   **`potential.next_season.three_of_three` ships 30.2% on n=43 against 4.30's 39.4% on n=33** with
   nothing saying which supersedes.

---

## 6. THE CODE -- the 12 September changes have no control, and the timestamps prove it

`redteam_controls.py` was last written **12 Sept 13:09:08**. `sheet_engine.py`, `wire.py`,
`sheet_constants.json` and `check_kit.py` were all written **12 Sept 16:48:5x**. **The whole of doc
300's commit landed three hours and thirty-nine minutes after the controls were last touched.**

Doc 300's *"44 of 44 red-team controls pass against the production path"* is true and is a regression
test. It is not coverage. Doc 296 set the right bar itself: *"Every control here was run against the
pre-291 code first and failed there, so a pass means something."* **No 16:48 change has a control
that fails on the pre-change tree.**

Read against the 44 checks, these are uncovered:

* **The section-0 THIS WEEK / CALENDAR split.** Nothing asserts that a later-week fill stays out of
  THIS WEEK, nothing asserts the ordering key is no longer season points, nothing asserts a calendar
  row is labelled projected and keyed to its claim week. **This is the change Matt asked for and the
  defect he reported, and it is the one thing with no negative control.** Doc 300 says the calendar
  *"was exercised with a planted kicker and defence"*; there is no such plant in the file. `MOCK_EXTRA`
  is used for C16's undrafted back and unowned receiver and nothing else. **A guard shown firing once
  by hand is not a guard (0.2).**
* **The `absence` block.** No control reads it, mutates it, or checks a bench body's price responds to
  it. C13 and C14 assert the handcuff price is UNCHANGED under mutation, which is the opposite test.
* **The drop-cost box moved above the picks.** No check that it exists or where it sits.
* **The team name read from ESPN.** The harness's `fake_get('mRoster')` returns
  `{'id': MY_TEAM_ID, 'roster': {...}}` with **no name field at all**, so the mock cannot exercise the
  change even in principle, and no control plants a rename.

**And one defect in the harness itself, which is about doc 298.** C16's base check asserts
`len(fb) == 0` -- the recorded 10 Sept pool produces **zero** off-board free players. The live 11 Sept
pool produced **71**, and doc 292 says 71 is typical. **The off-board path, which is the entire
mechanism behind doc 298's Jayden Higgins find, is exercised only on one planted synthetic row and
has never been run against a realistic population.** Refreshing the recorded pool to an 11 Sept
snapshot would fix it and costs nothing.

---

## 7. What survives, stated as readily as what died

* **Doc 300's scoring gradient.** Robust to the cut, to the cut-free test, to the injury exclusion,
  to the claimability filter, and to both at once. It is a real signal and it is worth wiring in.
* **Doc 299's null choice.** The within-team permutation is the conservative one and the result does
  not depend on it.
* **Doc 297's central answer to A1.** Yes, the missing absence model changes the drop order; yes,
  the missing streaming model is the larger of the two distortions; yes, they push opposite ways.
  Every one of my objections makes the case for A1 stronger, not weaker.
* **Doc 296's C17 and its self-criticism** are the best work in the batch. The observation that a
  grep token matching a legitimate row can neither close nor hold a ledger row is the kind of thing
  that only gets found by someone looking for it.
* **Doc 294's discipline.** It states its forking paths, reports which cut came from reading output,
  and labels the result accordingly. Nothing in it needed correcting.

## 8. Open threads from this doc

* **NOT YET RUN:** every table here on 2025. `--years` is already wired; the file is on his tree.
* **NOT YET RUN:** doc 300 section 3's wiring job, restated. **Do not replace the 46% job-opens term
  with the week-1 band. Multiply them.** The band's startable half is 20% where the man ahead is
  durable and 57% where he is not.
* **NOT YET RUN:** the 2nd-receiver squeeze as a live watch rule, and whether it survives on 2025.
* **BLOCKED:** `stats_player_week_2025.csv`, named above.
* **For the ledger:** row 27 amend, row 29 amend, and new rows for the constants in section 5.
