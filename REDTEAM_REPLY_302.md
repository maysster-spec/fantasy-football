# REDTEAM_REPLY_302 -- second reader's report on docs 291 to 300

**Written 13 September 2026 by the red-team chat, for the directive chat that issued
`Source\REDTEAM_TASKING_PROMPT.md`.** This is the machine-readable superset. A narrative version of
the same review is at `Source\302_the_second_back_was_often_the_first.md`.

> **KNOWN DUPLICATION, FLAGGED RATHER THAN LEFT (0.5c4).** Two files now carry this review. That is
> the defect the naming rule exists to prevent. **Resolution: THIS file is canonical because it is the
> superset; archive `Source\302_the_second_back_was_often_the_first.md` to `2026\_archive\` or keep it
> as the human copy, but do not let a third one appear.** Both were written in the same session by the
> same author; there is no version drift between them today, only scope.

**Provenance discipline, per Matt's standing rule on how claims are sourced.** Every number in
sections 3 to 8 below was computed by me in this session from files I loaded and ran, not read from a
search snippet and not carried from doc text. Where I quote docs 291 to 300 I am quoting a file I read
in full from `/mnt/project/`. Where I quote `sheet_constants.json`, `week1_share.py` or
`redteam_controls.py` I read the file itself off the drive, not a description of it. Drive
`modifiedTime` values are quoted from the API metadata response, not inferred.

---

## 0. THE SHORT VERSION, AS EDITS

Ranked by what it costs to leave undone.

| # | edit | where | why |
|---|---|---|---|
| 1 | **Retract doc 300's "50% startable" and the 7 / 11 / 39 / 50 rate row.** Keep the points row. | doc 300 §2, `AUDIT_LEDGER` row 29, the Tuesday read's band table | On the 74 of 118 team-seasons where the labelled lead back really was the lead back, the 35%+ startable gap is **+2 points, p=0.5553**. §4 below. |
| 2 | **Do not implement doc 300 §3 as written.** The week-1 band must MULTIPLY the 46% job-opens term, never replace it. | doc 300 §3's NOT YET RUN; `seat` block in `sheet_constants.json` | Top band is 20% startable where the man ahead is durable and 57% where he is not. §4.4. |
| 3 | **Move doc 299's Denver caution from Pat Bryant to Troy Franklin.** | doc 299 §4, `AUDIT_LEDGER` row 27, the wire's 3-of-3 tag | With the arrival out of the denominator the 3rd+4th effect is −0.008, p=0.21. The 2nd receiver is the one that survives at −0.045, p=0.011. §6. |
| 4 | **Fix two constants that are live now.** `absence.rate.K` is the QB number, not a kicker number. `absence.streamer.K = 7.5` has no source. | `Source\sheet_constants.json` | §7 items 1 and 2. |
| 5 | **Resolve whether the `absence` block is consumed.** Doc 297 §6 says nothing shipped; the JSON note says the page prices bench bodies with it. | doc 297 §6 vs `sheet_constants.json` | If the doc is right, the page's own printed disclaimer may now be false. §7 item 5. |
| 6 | **Add four controls and refresh the recorded pool.** No 12 Sept 16:48 change has a control that fails on the pre-change tree. | `Scripts\research\redteam\redteam_controls.py` | §8. |
| 7 | **Amend `0.5(a2)`'s confirmed list.** Matt's arrival mechanism is confirmed, but not in the form doc 299 confirmed it. | directive §0.5(a2) | §6.5. |
| 8 | **No change needed** to doc 294, doc 292's multiple-comparison handling, doc 296's C17, or doc 299's null choice. | | §9. |

**Nothing here requires Matt to run anything except `wk1_redteam.py --years 2021 2022 2023 2024 2025`
and `squeeze_redteam.py --years 2021 2022 2023 2024 2025` when convenient.** Both are already on the
drive at the paths in §2.3. Neither writes anything.

---

## 1. WHAT WAS ATTACKED AND WHAT HAPPENED

| tasking item | verdict | one line |
|---|---|---|
| 1. doc 300's week-1 share table | **HALF KILLED** | Points gradient robust to everything. Startable rate does not survive the labelling check. |
| 2. doc 297's absence simulation | **QUALIFIED, three ways** | All three of my objections make A1 more urgent, not less. One shipping rate is unstable. |
| 3. doc 299's arrival squeeze | **KILLED AND REPLACED** | The tested cell is dilution. The untested cell (2nd receiver) is the real effect. |
| 4. p-values across the four docs | **CLEARED** | Multiplicity is not what threatens either headline. Both survive Bonferroni. |
| 5. `[INHERITED]` numbers in code | **SEVEN DEFECTS** | Two are live errors, five are provenance or collision. |
| 6. control coverage of the 12 Sept code | **CONFIRMED GAP** | The controls file predates the commit by 3h39m. Four uncovered changes named. |

---

## 2. ENVIRONMENT, REPRODUCIBILITY, AND THE ONE BLOCKER

### 2.1 BLOCKED, with the exact missing input named (0.5a4)

**`stats_player_week_2025.csv`.** The nflverse `player_stats` release, read from its own expanded
asset list at `https://github.com/nflverse/nflverse-data/releases/expanded_assets/player_stats`,
carries `stats_player_week_2012.csv.gz` through `stats_player_week_2024.csv.gz`. The 2025 asset
returns HTTP 404. I verified this by listing the assets, not by inferring from one failed download.
`stats_team_week_*` stops at 2024 as well.

**Consequence: every table I produce is 2021-2024 where docs 297, 299 and 300 used 2021-2025.**
Doc 300's n=143 becomes my n=118. Doc 299's 43 vs 68 becomes 55 vs 62.

**This is not blocked for Matt.** The 2025 file is on his tree, because those three docs ran on it.
Both scripts I shipped take `--years` and will pick it up unchanged. **The directive chat should treat
every number below as a four-season replication that the fifth season may move, and should re-run
before writing any of it into `00_PROJECT_DIRECTIVE.md` as a fixed figure.**

### 2.2 Why the four-season replication is still worth acting on

Doc 300's published table and mine agree to within 0.24 points a game and 4 points of rate in every
band (§4.1). Doc 299's published difference and mine agree in sign and rough size. **The arithmetic
in both docs reproduces. Nothing below is a claim that the original authors miscalculated.** What
I found is in the population, the labelling and the denominator, and none of those is season-sensitive.

### 2.3 What I shipped, where, and what it prints

| file | location | bytes | what it does |
|---|---|---|---|
| `wk1_redteam.py` | `Scripts\research\wk1\` | 12,521 | Doc 300 replication plus five attacks: cut sweep, cut-free Spearman, lead-back-absence exclusion, claimability split, labelling check. Prints tables A, B, C1, C2, C3, D, D1, D2, D3, E, E1. |
| `squeeze_redteam.py` | `Scripts\research\f1\` | 7,593 | Doc 299 replication under two designs and two nulls, on all four receiver slots. |
| `302_the_second_back_was_often_the_first.md` | `Source\` | 19,303 | Narrative version of this report. |
| this file | `2026\` root | | Canonical. |

**Both scripts: stdlib only** (`collections`, `csv`, `math`, `os`, `random`, `statistics`, `sys`),
**no pandas, no numpy, no scipy, no shell-out.** Paths resolve against the script's own folder via
`os.path.dirname(os.path.abspath(__file__))`, overridable with the `WK1_DATA` environment variable.
Docstrings are raw strings, so no `SyntaxWarning` on Python 3.12. This is doc 144's rule applied.

Both were run to completion in this session against 2021-2024 and exited 0.

### 2.4 Scoring used

Half-PPR under §2's rules, computed per weekly row:
`0.1*rush_yds + 6*rush_td + 0.1*rec_yds + 6*rec_td + 0.5*rec - 2*(rush_fum_lost + rec_fum_lost)`.
This is byte-identical to `week1_share.py`'s `half_ppr()`. I did not add 2-point conversions or
passing lines for backs, because the original did not, and the point of a replication is to change one
thing at a time.

---

## 3. WHAT THE ORIGINAL SCRIPT ACTUALLY DOES

Read from `Scripts\research\wk1\week1_share.py` (6,412 bytes, created 2026-09-12T16:51:59Z). Six
behaviours matter and only two of them are in doc 300's text.

1. **`lst.sort(reverse=True)` on `(work, player_id)` tuples, then `lst[0]` is the lead back.**
   So "the lead back" is defined as the week-1 usage leader.
2. **Therefore the docstring's exclusion is vacuous.** It says *"The team's leading week-1 back must
   have PLAYED in week 1 (if he did not, the job was already open and that is a different event, doc
   294's)."* The only enforcement is `if u1 <= 0: continue`. Whoever has the most week-1 work
   necessarily played. **Doc 294's event is fully inside the population, not excluded from it.**
   This is the single most consequential finding in this report and it is §4.3.
3. **Ties break on the player-id string.** Python sorts the tuple, so at an exact 50/50 split the
   second element decides which man is called RB1 and which RB2. Nine of my 118 rows sit at 45% or
   above. 2021 Arizona is exactly 50/50 and the two orderings give a 16.80 ppg row (Conner) or an 8.81
   ppg row (Edmonds). **At a near-even split there is no second back, there are two backs.**
4. **`rest[pid]` is keyed on `player_id` alone, not `(team, player_id)`.** A second back traded
   mid-season carries his new team's points into the outcome. Small in practice, wrong in principle,
   and it means the outcome is not "he inherited this job".
5. **Filters:** team week-1 RB work `>= 10`, `u1 > 0`, `u2 > 0`, RB2 appears in `>= 4` of weeks 2-14.
6. **The permutation is a pooled label shuffle with no clustering.** Teams recur across seasons. The
   predictor is season-specific so the dependence is mild, but it is not zero and is not stated.

**None of 2, 3, 4 or 6 is disclosed in doc 300.** Item 2 is disclosed as the opposite of what happens.

---

## 4. FINDING 1: DOC 300

### 4.1 It reproduces

**POPULATION: team-seasons 2021-2024 whose week-1 RB usage leader and second back both played in week
1 with combined RB work >= 10, and whose second back appeared in 4+ of weeks 2-14. n = 118.**
**PREDICTOR: RB2's share of team week-1 RB carries plus targets.**
**OUTCOME: half-PPR per game over weeks 2-14, and whether that reached 9.92 `[INHERITED: 4.1's RB30 / 17]`.**

| band | n | ppg | reached 9.92 | doc 300 (2021-2025, n=143) |
|---|---|---|---|---|
| under 20% | 32 | 4.97 | 6% | 4.99 / 7% |
| 20 to 30% | 29 | 4.94 | 7% | 5.22 / 11% |
| 30 to 40% | 33 | 8.31 | 39% | 8.35 / 39% |
| 40% or more | 24 | 10.46 | 50% | 10.28 / 50% |
| ALL | 118 | 7.01 | 25% | 6.93 / 24% |

**35%+ against under 35%: ppg +4.10 (p=0.0000), startable +31 points (p=0.0003).** Doc 300: +3.89 and
+29 at the same two p-values. Permutation, 4,000 draws, one-sided, seed fixed.

### 4.2 The cut point is NOT chosen, and this objection is closed

I ran every split. All seven separate on points.

| cut | n high | ppg diff | p | startable diff | p |
|---|---|---|---|---|---|
| 15% | 93 | +2.18 | 0.0103 | +21 pt | 0.0238 |
| 20% | 86 | +2.81 | 0.0005 | +25 pt | 0.0032 |
| 25% | 71 | +3.83 | 0.0000 | +30 pt | 0.0003 |
| 30% | 57 | +4.26 | 0.0000 | +37 pt | 0.0000 |
| **35% (doc 300's)** | 40 | +4.10 | 0.0000 | +31 pt | 0.0003 |
| 40% | 24 | +4.33 | 0.0000 | +32 pt | 0.0025 |
| 45% | 9 | +3.72 | 0.0092 | +34 pt | 0.0440 |

**Cut-free: Spearman(share, weeks 2-14 ppg) = +0.464, n=118.** The bands do not have to be trusted at
all for the scoring result to stand. **Doc 300 did not cherry-pick and should be credited with that.**

### 4.3 THE KILL: in the top band the second back was usually the first back

**Testable form, written before the run:** *if a high week-1 share identifies a backup breaking
through, then the man labelled "the lead back" should still be his team's leading back over weeks 2 to
14. If instead he loses the job, the design has the two men in the wrong columns and the outcome is
measuring a starter, not a handcuff.*

Check: did the labelled lead back lead his own team in weeks 2-14 carries plus targets?

| band | labelled RB1 did NOT keep the lead |
|---|---|
| under 20% | 10 of 32 (31%) |
| 20 to 30% | 7 of 29 (24%) |
| 30 to 40% | 13 of 33 (39%) |
| **40% or more** | **14 of 24 (58%)** |
| overall | 44 of 118 (37%) |

**Every one of the fourteen, named, with the share of weeks 2-14 work the "lead back" retained:**

| season | tm | the "second back" | share | the "lead back" | he kept | RB2 ppg | startable |
|---|---|---|---|---|---|---|---|
| 2021 | ARI | James Conner | 50% | Chase Edmonds | 30% | 16.8 | yes |
| 2024 | DET | Jahmyr Gibbs | 49% | David Montgomery | 47% | 17.0 | yes |
| 2023 | ATL | Bijan Robinson | 47% | Tyler Allgeier | 37% | 12.6 | yes |
| 2022 | NE | Rhamondre Stevenson | 45% | Damien Harris | 26% | 14.0 | yes |
| 2023 | LA | Kyren Williams | 44% | Cam Akers | **0%** | 19.3 | yes |
| 2022 | BUF | Devin Singletary | 43% | Zack Moss | 4% | 10.2 | yes |
| 2024 | LV | Alexander Mattison | 42% | Zamir White | 21% | 8.8 | no |
| 2023 | PIT | Najee Harris | 42% | Jaylen Warren | 44% | 9.6 | no |
| 2022 | DET | Jamaal Williams | 42% | D'Andre Swift | 25% | 12.9 | yes |
| 2022 | DEN | Melvin Gordon | 41% | Javonte Williams | 15% | 7.6 | no |
| 2024 | DAL | Rico Dowdle | 41% | Ezekiel Elliott | 23% | 11.7 | yes |
| 2023 | CLE | Jerome Ford | 41% | Nick Chubb | **3%** | 11.9 | yes |
| 2021 | BAL | Latavius Murray | 40% | Ty'Son Williams | 12% | 6.4 | no |
| 2022 | DAL | Tony Pollard | 40% | Ezekiel Elliott | 45% | 16.7 | yes |

**Nine of the fourteen were startable. They supply 9 of the top band's 12 startable outcomes.**

**Restricted to the 74 team-seasons where the labelled lead back really was the lead back:**

| band | n | ppg | reached 9.92 |
|---|---|---|---|
| under 20% | 22 | 4.42 | **0%** |
| 20 to 30% | 22 | 4.44 | 5% |
| 30 to 40% | 20 | 6.15 | 20% |
| 40% or more | 10 | 7.57 | **20%** |
| ALL | 74 | 5.32 | 9% |

**35%+ (n=18) against under 35% (n=56): ppg +2.12, p=0.0063; startable +2 points, p=0.5553.**
`[TESTED, n=74]`

**Reading.** The scoring half survives at roughly half its published size. The startable half is gone.
Against the subgroup's own 9% base rate, 20% is still a doubling, so doc 300's *"a doubling of the base
rate off one box score"* framing survives. **The number 50% does not, and it is the number that
reached the Tuesday read.**

### 4.4 The lead-back-injury confound does NOT kill it, but it does change how it is used

**Testable form:** *if the week-1 share predicts only because a near-even backfield belongs to a lead
back who later misses time, then among teams whose lead back played every week 2 to 14 the gradient
disappears.*

**It does not disappear.**

| cut of the population | n | <20% | 20-30% | 30-40% | 40%+ | 35% split |
|---|---|---|---|---|---|---|
| **C1** lead played every week 2-14 | 47 | 3.94 / 0% | 4.06 / 0% | 7.39 / 21% | 11.38 / 60% | ppg **+5.10, p=0.0000**; rate +36 pt, p=0.0022 |
| **C2** lead missed at least one week | 71 | 5.67 / 11% | 5.89 / 14% | 8.99 / 53% | 10.22 / 47% | (not split) |
| **C3** all teams, RB2 scored ONLY in weeks the lead played | 117 | 4.64 / 6% | 4.68 / 4% | 8.00 / 33% | 10.32 / 50% | |

C3 is the tighter test and it holds: the high-share back is scoring while the starter is on the field,
not only in the windows the starter is out.

**But the predictor is correlated with the confound, and this is the operationally important part:**

| band | lead back missed >= 1 week | mean weeks missed |
|---|---|---|
| under 20% | 19 of 32 (59%) | 2.25 |
| 20 to 30% | 14 of 29 (48%) | 1.62 |
| 30 to 40% | 19 of 33 (58%) | 1.58 |
| **40% or more** | **19 of 24 (79%)** | **2.92** |

A near-even week-1 split partly marks a lead back the team is already managing. **So the week-1 share
and the seat model's `p_opens` are not substitutes, and doc 300 §3 proposes to treat them as
substitutes** (*"ranked on the band above rather than on the generic 46% job-opens figure"*).
**Correct instruction: multiply, do not replace.** See §11 for the proposed directive text.

### 4.5 The population is not the claimable population, and this does NOT hurt the Black call

**Proxy for claimable: RB2 was not a startable fantasy back the prior season** (under 9.92 half-PPR
over weeks 1-14 of season t-1, or fewer than 4 games, or no prior season). A back who averaged 12 a
game last year is rostered in every 12-team league in week 1 and is not a claim.

**21 of 118 team-seasons were not claims. In the top band it is 9 of 24 (38%):** Ezekiel Elliott, Gus
Edwards, Jahmyr Gibbs, James Conner, Kenyan Drake, Melvin Gordon, Najee Harris, Nyheim Hines, James
Robinson. Doc 300 names some of these itself as top-ten shares, so the contamination was visible; what
was not done was removing them.

| cut | n | <20% | 20-30% | 30-40% | 40%+ | ALL | 35% split |
|---|---|---|---|---|---|---|---|
| **D1** claimable only | 97 | 4.66 / 3% | 4.58 / 4% | 7.97 / 37% | **10.83 / 60%** | 6.52 / 22% | ppg +4.37, p=0.0000; rate +37 pt, p=0.0003 |
| **D2** claimable AND lead never missed | 35 | 3.62 / 0% | 3.93 / 0% | 6.28 / 11% | 12.64 / 100% (**n=1**) | 4.69 / 6% | ppg +3.81, p=0.0175; rate +17 pt, **p=0.2720** (n=5 vs 30) |
| **D3** claimable AND lead missed time | 62 | 5.30 / 6% | 5.35 / 8% | 8.82 / 50% | **10.70 / 57%** | 7.55 / 31% | ppg +3.89, p=0.0003; rate +37 pt, p=0.0027 |

**Removing the already-rostered men makes the table STRONGER, not weaker.** So the contamination is not
what carries the result and Kaelon Black's own case is not weakened by removing it.

**Black sits in D3: a claimable back whose lead man is fragile.** That cell is n=62 and its top band is
10.70 a game at 57%, p=0.0027. **D2, where the man ahead stays healthy, has one row in the top band and
resolves nothing (rate p=0.27).** The two together are the whole of §4.4's point in a different form.

### 4.6 What I could not test, and the exact missing input

* **Whether the week-1 RB2 was actually free in Matt's league that week.** BLOCKED on historical league
  rosters for 2021-2024. `waiver_report_*.csv` gives adds and drops but not weekly ownership state.
  My prior-season-startable proxy is the best available and is stated as a proxy, not a measurement.
* **The 2025 season.** §2.1.
* **Whether the tie-break at 45%+ changes any conclusion.** Nine rows. Running both orderings is one
  line and is queued, not blocked.

---

## 5. FINDING 2: DOC 297

### 5.1 The absence rates re-measured, and the QB cell is not stable

**POPULATION, rebuilt from doc 297's own description:** for season t, the men who finished top-24 at
RB, top-24 at WR, top-12 at QB and top-12 at TE in season t-1 by half-PPR over weeks 1-14; their
availability read in season t; denominator is the team's weeks 1-14 actually played, so the bye is
removed; a man not in the league at all in season t is excluded. nflverse weekly, transitions 2021
through 2024.

| pos | n | weeks missed | share of weeks missed | shipping in `sheet_constants.json` |
|---|---|---|---|---|
| QB | 46 | 1.13 | **8.7%** | 13.7% |
| RB | 94 | 2.34 | 18.0% | 17.1% |
| WR | 96 | 1.74 | 13.4% | 15.0% |
| TE | 47 | 2.11 | 16.2% | 13.7% |

RB and WR reproduce inside a point. **QB is off by 5 points, and doc 297's own per-season row explains
it: 8 / 13 / 13 / 22.** My four transitions are 2021-2024 and doc 297's are 2022-2025, so the 22% year
is in the doc's window and not in mine.

**The defect is not the number, it is the sentence next to it.** Doc 297 §2 writes *"Per season it is
stable and not one bad year: QB 8/13/13/22%"*. A cell running 8% to 22% across four seasons is not
stable, and the claim is contradicted by the figures printed in the same clause. **The QB absence rate
is one of the two inputs to the Shough result the doc leans on** (18.01 to 3.05), so this is not
cosmetic. `[TESTED, n=46 QB player-seasons, 2021-2024]`

### 5.2 Independence across players understates the value of depth, in a known direction

**This is analytic, not measured, and is labelled as such.** The drop cost is
`E[best legal nine with the man] - E[best legal nine without him]`. Best-legal-nine is a maximum over
the available set, so lineup points are a convex function of the availability vector. Independent
per-man weekly draws at 13.7 to 17.1 percent produce fewer weeks with several men out simultaneously
than a correlated real season does, and **several-out-at-once is the only state in which a bench body
enters the lineup at all** (doc 240's Spears finding is the same mechanism from the other side: three
starters out in week 11 and the sixth back still did not play, because the three were WR/WR/RB).

**Direction: every drop cost in doc 297 §3 is a lower bound on the value of holding the body.** Doc
297's conclusion is therefore conservative, which strengthens A1 rather than weakening it.

Within-player persistence (a four-week injury versus four scattered weeks) does not bias the
expectation, only the variance, and doc 297 reports an expectation. Not an issue.

### 5.3 The intervals reported are Monte Carlo noise, not uncertainty

`Washington -0.98 +/- 0.02`, `+3.84 +/- 0.05`, `+10.02 +/- 0.10` are standard errors of the mean over
6,000 simulation draws. They shrink with more draws and say nothing about whether the answer is right.

**The uncertainty that matters is in the rates.** The RB rate is 17.1% measured on 94 player-seasons.
Clustered by player, the standard error on that is roughly 2 percentage points, which propagates to
something on the order of a tenth of a point to several tenths on a −0.98 figure, an order of magnitude
more than `+/- 0.02` conveys. **Directive §0.2 says a severity estimate must be measured rather than
reasoned; it should also say that the interval reported must be the interval of the thing that is
actually uncertain.** Proposed text in §11.

### 5.4 The streamer rate is the wrong counterfactual for a DROP, and it errs expensive

The tasking asked this directly and the answer is yes.

* **Doc 12's numbers are the rest-of-season return of an ADD Matt chose in advance**, under uncertainty
  about who would be useful.
* **A refill after a drop happens at the moment the hole appears**, with the injury already known and
  the replacement's role already visible. Strictly more information.
* **Doc 259 already measured his actual free pool: best free RB 6.51, best free WR 8.94**, against doc
  12's 5.43 and 6.54.
* **Doc 252 rebuilt the free pool week by week** and found the best free player is worth 22 to 26 a
  game in nearly every week.

**So the streamed column understates the fill and therefore overstates every drop cost.** The fix is
free: `wire.py` already computes the free pool every run. Use its best-available at the position rather
than a four-year average add.

**And the source is weaker than the tag suggests.** `absence.streamer` RB 5.43, WR 6.54 and TE 5.53 all
come from doc 12, which directive §4.17 has already re-tagged `[SOURCED, n irreproducible]` after doc
92 step 1 failed to reproduce its sample sizes (raw files hold 1,230 executed adds, not 951; QB adds
135 events, not 34). **Only the QB number was re-derived. Three of the four are inherited from a table
the project has already declared irreproducible, and the JSON says only `[INHERITED]`.**

### 5.5 Yes, the handcuff bracket depends entirely on where the relief rate is applied

The tasking's third sub-question. **Confirmed, and doc 297 says so itself**, so this is a qualification
rather than a defect. Two residual problems:

1. **A median used as an expectation.** 11.2 is doc 244's MEDIAN relief scoring across 40 events. Half
   of relief backs are below it by construction. Applying it to every Jeanty-absent week assumes
   Washington is the median relief back. **Doc 300's own week-1 share table is exactly the instrument
   that would say which side of it he is on**, which is the strongest argument for §0's edit 2.
2. **Two numbers for one object (0.5c4).** Doc 297's bracket uses **11.2** (doc 244, n=40). The shipping
   `seat.relief_ppg` is **12.13** (n=51, population *"NFL team-seasons 2022-2025 where the weeks-1-4 RB
   usage leader missed a week between 5 and 14 and the direct backup had a line"*). Also `AUDIT_LEDGER`
   row 18 records a dated correction establishing that 11.2 is NFL team-seasons' median relief scoring
   and NOT *"the rate at which a fill-in back actually kept the job"*. **Three docs, two numbers, one
   quantity. Pick one and say which supersedes.**

Also worth noting for whoever wires this: `14.6 = 248 / 17` is the job's full value, and doc 294
measured that producers went from about 23% of backfield touches to about 35%, not to 100%. The +10.02
row is correctly labelled an upper bound; make sure it stays labelled that way if it reaches a page.

---

## 6. FINDING 3: DOC 299

### 6.1 The null choice is fine, and that part of the tasking closes clean

**Testable form:** *if the within-team permutation is doing the work, permuting the arrival label
within SEASON instead should give a materially different p.*

It does not. Across all five slots the season shuffle gives the same direction at the same or a smaller
p than the team shuffle. **The within-team null is the more conservative of the two and was correctly
chosen.** Doc 299 should be credited with this and the objection dropped.

### 6.2 The placebo fires

**POPULATION: team-seasons 2021-2024 with a receiver who had 60+ targets for that team last season and
is still on it. TREATMENT: a receiver who had 60+ targets for ANOTHER team last season is on this team
now. CONTROL: same incumbent condition, no arrival. n = 117 team-seasons, 55 treatment, 62 control.
OUTCOME: each man's share of team WR targets on a per-game-rate basis, this season minus last, 4-game
minimum in both seasons. SLOTS fixed by LAST season's targets and never re-ranked on the outcome.
Permutation 4,000 draws, one-sided in Matt's direction.**

**DESIGN 1, doc 299 as published: share of ALL team WR targets.**

| slot | arrival | no arrival | difference | p (within team) | p (within season) | n |
|---|---|---|---|---|---|---|
| 1st, the incumbent | −0.0306 | −0.0060 | −0.0246 | 0.2745 | 0.0377 | 54/61 |
| **2nd (the placebo)** | **−0.0318** | **+0.0167** | **−0.0485** | **0.0018** | **0.0000** | 47/58 |
| 3rd alone | −0.0052 | +0.0207 | −0.0258 | 0.0628 | 0.0372 | 36/49 |
| 4th alone | +0.0059 | +0.0224 | −0.0165 | 0.0307 | 0.1425 | 24/32 |
| 3rd + 4th (doc 299's cell) | −0.0007 | +0.0214 | −0.0221 | 0.0138 | 0.0310 | 60/81 |

Doc 299 published −0.044 at p=0.005 for 3rd+4th on five seasons; I get −0.0221 at p=0.0138 on four.
Same sign, roughly half the size, still significant. **The replication holds.**

**The 2nd receiver, whom the claim says nothing about, is hit twice as hard as the room below.** That
is the placebo failing, and it is the first sign that "the room below" is not the object being measured.

### 6.3 THE KILL: the confirmed half is the denominator

**Testable form, written before the run:** *a share is a share of 100 percent, and the arrival is in
this season's denominator and not last season's, so every returning receiver's share must fall on an
arrival team whether or not anybody was squeezed. If the squeeze is real, it survives recomputing every
share over the HOLDOVER POOL only, the same men on both sides of the difference, arrival excluded from
numerator and denominator.*

**DESIGN 2, holdover pool. n = 101 team-seasons, 42 treatment, 59 control.**

| slot | arrival | no arrival | difference | p (within team) | p (within season) | n |
|---|---|---|---|---|---|---|
| 1st, the incumbent | +0.0000 | −0.0250 | +0.0250 | 0.8660 | 0.9125 | 42/58 |
| **2nd** | **−0.0318** | **+0.0132** | **−0.0450** | **0.0110** | **0.0030** | 40/56 |
| 3rd alone | +0.0093 | +0.0207 | −0.0113 | 0.3227 | 0.2873 | 36/49 |
| 4th alone | +0.0248 | +0.0266 | −0.0019 | 0.2722 | 0.5182 | 24/32 |
| **3rd + 4th (doc 299's cell)** | **+0.0155** | **+0.0230** | **−0.0075** | **0.2097** | **0.3443** | 60/81 |

**The 3rd-and-4th effect vanishes. The 2nd receiver survives essentially intact.** `[TESTED, n=42 vs 59
team-seasons, 2021-2024]`

**Note a bug I made and caught before quoting it**, because it is the kind of thing the next reader
should know is possible here. My first holdover run took the current-season share over holdovers and
the prior-season share over the full prior roster, which changes the denominator size between the two
sides and produced a spurious +0.17 for the incumbent. Fixed by using the same key set on both sides.
The corrected numbers are the ones above and are what the shipped script produces.

**The sign flip doc 299 leans on also goes.** *"Without an arrival that group GROWS (+0.027); with one
it shrinks"* becomes +0.0230 against +0.0155. Both grow.

### 6.4 What this does to the live row

Doc 299 §4 places Pat Bryant in the 3rd-and-4th group on a team that added a 100-target receiver and
calls that *"the exact cell measured above at −0.044, p = 0.005"*.

**On the only design that separates a squeeze from dilution, Denver's squeezed receiver is Troy
Franklin, the 2nd man by 2025 targets (104), not Pat Bryant, the 4th (49).**

* Remove the arrival caution from Bryant's 3-of-3 tag, or restate it as "the room-wide dilution applies
  to him as it does to everyone, and no differential squeeze is established at his slot".
* Add a watch line on Franklin.
* Doc 298's screen and doc 299 no longer point opposite ways on Bryant, which removes the awkward
  "two measured results side by side" framing in doc 299 §4.

### 6.5 Matt's mechanism survives better than the doc's test of it

His words were *"the arrival compresses everyone below him, not just the man at the top."* **A real
reallocation exists and it is concentrated at the second receiver.** So the mechanism is confirmed and
the doc looked in the wrong place. **This should go into `0.5(a2)`'s confirmed list in the corrected
form, not the published one.** `AUDIT_LEDGER` row 27 needs the same amendment: claim 1 is confirmed
only in the arithmetic sense, claim 2 remains unresolved for the room below, and a new suggestive-to-
confirmed result exists at a slot neither claim named.

### 6.6 Design ambiguities I resolved and the directive chat should know about

* **"Receiver" read as `position == 'WR'`.** Doc 299 says *"his share of his team's receiver targets"*.
  If the original pooled TE, the numbers will differ. Not tested both ways. Queued, not blocked.
* **"Per game played"** read as each man's per-game target rate divided by the sum of those rates across
  the team's qualifying receivers. The plain share (raw targets over team targets) is a defensible
  alternative and I did not run it.
* **Doc 299's vacated-share control** is described but its implementation is not, so I did not attempt
  to reproduce it. My design 2 is a different and stronger control for the same problem.

---

## 7. FINDING 4: THE MULTIPLE-COMPARISON AUDIT

**The honest answer is boring and should be reported as readily as an exciting one.**

| doc | comparisons actually made | headline p | Bonferroni | verdict |
|---|---|---|---|---|
| **300** | 4 bands + 1 split, 2 outcomes = ~10 reported. Unreported degree of freedom: the cut point. | ppg 0.0000, rate 0.0003 | at 10, ppg still < 0.002 | **SURVIVES.** And §4.2 shows all seven cut points separate, and the cut-free Spearman needs no correction. **Multiplicity is not the threat. The population is.** |
| **299** | 2 pre-stated claims + 3 vacated bands = 5 reported. Unreported: the slot grouping, which is 5 choices (2nd, 3rd, 4th, 3+4, 2+3+4) of which one was published. | 0.005 | at 6, 0.03 | **SURVIVES.** **Multiplicity is not the threat. The denominator is.** The slot choice matters for a different reason entirely: the untested slot is where the effect lives. |
| **297** | No p-values reported. All four cells of the 2x2 are shown, which is correct practice. | n/a | n/a | **No multiplicity issue.** The interval problem is §5.3, a different thing. |
| **294** | Explicitly states 32 variants on one reading and 16 on another, plus window and pedigree cuts. Its §4 result came from reading a first draft's output. | 0.040 / 0.003 / 0.027 | at ~30, 0.003 becomes ~0.09 | **CORRECTLY LABELLED SUGGESTIVE.** No change needed. Doc 294 also reports the committed script disagreeing with the draft (+4.6, p=0.63 against +17.9, p=0.061), which is the right disclosure. |
| **292** | Sixteen cells on efficiency metrics. | states *"none clears the multiple-comparison bar"* | | **Correct as written.** |

**Recommendation to the directive chat: do not add a multiplicity correction requirement to §0.2.**
It would not have caught either of the two real defects and doc 294 already demonstrates the practice
working. What §0.2 could use is §5.3's point about which interval gets reported.

---

## 8. FINDING 5: THE `[INHERITED]` NUMBERS NOW SHIPPING

Source: `Source\sheet_constants.json`, 7,074 bytes, `built: 2026-09-10`, `modifiedTime`
2026-09-12T16:48:52.438Z. Read in full.

The `absence` block as shipped:

```
"rate":     { "QB": 0.137, "RB": 0.171, "WR": 0.15, "TE": 0.137, "D/ST": 0.0, "K": 0.137 }
"streamer": { "QB": 16.65, "RB": 5.43, "WR": 6.54, "TE": 5.53, "D/ST": 5.99, "K": 7.5 }
```

| # | defect | severity | fix |
|---|---|---|---|
| 1 | **`rate.K = 0.137` is the QB and TE number, not a kicker number.** The note says the kicker cell *"is not used"*, but the key sits in a dict a lookup will find and will silently return. The measured kicker rate in doc 297 is **0.213**. 0.137 understates kicker absence by about a third, and it is not the conservative direction. | **LIVE ERROR** | Delete the key so a lookup raises, or set it to 0.213 and drop the "not used" clause. Do not leave both. |
| 2 | **`streamer.K = 7.5` has no source anywhere.** `streamer_note` attributes QB (doc 92), RB/WR/TE (doc 12) and D/ST (doc 265), and says nothing about K. | **LIVE, §3 `[NO SOURCE]`** | Source it or remove it. |
| 3 | **`streamer` RB 5.43, WR 6.54, TE 5.53 inherit from doc 12**, which §4.17 has re-tagged `[SOURCED, n irreproducible]`. Only QB was re-derived. | provenance | Change the tag to `[INHERITED from doc 12, n irreproducible per 4.17]` so the next reader is not misled by a bare `[INHERITED]`. |
| 4 | **The population is written two ways.** JSON note says nflverse **2022-2025**; doc 297 says **2021-2025**. Same measurement, two spans. Doc 297 also says *"four transitions"*, which reconciles them (2021-2024 selectors, 2022-2025 outcomes), but nothing in either file says so. | §0.6 drift | One sentence in the JSON: "selectors 2021-2024, outcomes 2022-2025, four transitions." |
| 5 | **The doc and the artifact disagree about whether anything shipped.** Doc 297 §6: *"No code change shipped today. The sheet still prices byes only and says so on its own face (\"this page prices byes and not injuries\")."* JSON note: the block exists *"so the page can price a bench body instead of printing 0.0 for him."* | **POTENTIALLY LIVE** | Resolve by grepping `sheet_engine.py` and `wire.py` for reads of `absence`. **If the page now uses it, the printed disclaimer is false, which is worse than either alternative.** I could not settle this without pulling 162 KB of code and judged that a poor use of context; it is one grep on Matt's tree. |
| 6 | **`seat.p_opens_note` asserts a null the ledger has already reopened.** It states flatly *"It does NOT vary by history: 45.9% for a back who missed a game last season against 46.3% for one who played all 17, p=0.60. So it prices every seat the same and cannot rank them."* `AUDIT_LEDGER` row 2 records doc 276's null as under re-check under catalog **B4**, because its population held only backs healthy through week 4. | provenance | Add "(under re-check, catalog B4)" to the note. |
| 7 | **Two more collisions.** `seat.relief_ppg` is 12.13 (n=51) while doc 297's bracket uses 11.2 (n=40). `potential.next_season.three_of_three` ships 0.302 on n=43 while directive §4.30 carries 39.4% on n=33. Nothing says which supersedes in either case. | 0.5c4 | Pick one per quantity and record the loser as superseded. |

**One thing the file gets right and should be preserved:** the `potential` block's note separating
`in_season` from `next_season` with an explicit warning that a free-agency pickup can never be a keeper
is exactly the discipline §0.6 asks for, and the `hit_size` note refusing to split hit size by archetype
on 19 hits is a correct power call.

---

## 9. FINDING 6: CONTROL COVERAGE OF THE 12 SEPTEMBER CODE

### 9.1 The timestamps settle it before any code is read

Drive `modifiedTime`, quoted from the API:

| file | modified |
|---|---|
| `Scripts\research\redteam\redteam_controls.py` | **2026-09-12T13:09:08.739Z** |
| `Scripts\sheet_engine.py` | 2026-09-12T16:48:51.155Z |
| `Scripts\check_kit.py` | 2026-09-12T16:48:52.347Z |
| `Source\sheet_constants.json` | 2026-09-12T16:48:52.438Z |
| `Scripts\wire.py` | 2026-09-12T16:48:52.487Z |
| `Scripts\research\wk1\week1_share.py` | created 2026-09-12T16:51:59.652Z |

**The whole of doc 300's commit landed three hours and thirty-nine minutes after the controls were last
touched.** The 13:09 edit is doc 296's C17 work.

**Doc 300's *"44 of 44 red-team controls pass against the production path"* is true, and it is a
regression test rather than coverage.** Doc 296 set the correct bar in the file's own docstring:
*"Every control here was run against the pre-291 code first and failed there, so a pass means
something."* **No 12 September 16:48 change has a control that fails on the pre-change tree.**

### 9.2 Read against the 44 checks, here is what has no control

I read `redteam_controls.py` (20,159 bytes) in full. The check set is C0, C1, C1b, C1c, C2, C3, C4, C5,
C6, C7, C7b, C8, C9, C10, C11, C12, C13, C14, C15, C16, C16b, C16c, C17. They cover team-code
resolution on five inputs, the missing-projection box and Matt's A15 do-not rule, cards with blank,
wrong or claimed ids, the defence run rendering and its bye ordering, the single-TE-bye trade
suppression, the handcuff price's robustness to a misspelled holder and a bad `next_man_id`, the
off-board free-player file, and C17's playing-inheritor rule.

**Uncovered:**

1. **The section-0 THIS WEEK / CALENDAR split.** Nothing asserts a later-week fill stays out of THIS
   WEEK, nothing asserts the ordering key is no longer season points, nothing asserts a calendar row is
   labelled projected and keyed to its claim week. **This is the defect Matt reported and the change he
   asked for, and it is the one with no negative control.** Doc 300 §1 says the calendar *"was
   exercised with a planted kicker and defence because the recorded pool holds neither"*; **there is no
   such plant in the controls file.** `MOCK_EXTRA` is used only for C16's `Test Undrafted` back and
   C16b's `Test Unowned` receiver. That exercise was a one-off manual run, and §0.2's *"a guard that has
   never been executed is not a guard"* has an obvious sibling: a check that exists only as a one-off
   run is not a control.
2. **The `absence` block.** No control reads it, mutates it, or asserts a bench body's price responds to
   it. **C13 and C14 assert the handcuff price is UNCHANGED under mutation, which is the opposite test.**
3. **The drop-cost box promoted above the picks.** No check that it exists or where it sits.
4. **The team name read from ESPN.** The harness's `fake_get('mRoster')` returns
   `{'scoringPeriodId': ..., 'teams': [{'id': wire.MY_TEAM_ID, 'roster': {'entries': roster}}]}` with
   **no team-name field at all**, so the mock cannot exercise the change even in principle, and no
   control plants a rename. This one needs a harness change, not just a check.

### 9.3 A defect in the harness itself, and it is about doc 298

**C16's base assertion is `fb is not None and len(fb) == 0`**: the recorded 10 September pool produces
**zero** off-board free players. But doc 296 records the live 11 September 20:14 run writing
`FREE_UNRANKED_20260911.csv` with **71 off-board free skill players**, and doc 292 says 71 is the
typical figure.

**So the off-board path, which is the entire mechanism behind doc 298's Jayden Higgins find, has never
been run against a realistic population.** It is exercised on one planted synthetic row and one planted
unowned row. Refreshing `WIRE_20260910.csv` to an 11 September snapshot fixes it, costs nothing, and
would also let doc 298's proposed C-series control (plant a 3-of-3 receiver off the board, require him
on the page) be written against real data.

### 9.4 Two things in the controls file worth keeping and copying

* `'HARNESS FINISHED' not in con: raise SystemExit(...)` is §0.2's exit-code rule implemented properly.
* `stash_block()`'s docstring, and C17's second check reading the first cell of each row rather than
  grepping the block, is `AUDIT_LEDGER` row 13's lesson applied in the opposite direction on the same
  morning. **That is the best single piece of work in docs 291 to 300** and the reasoning should be
  generalised into the directive: **a grep token that can match a legitimate row can neither close a
  ledger row nor hold one open.**

---

## 10. WHAT SURVIVES, STATED AS READILY AS WHAT DIED

Per §0.2, a result that confirms is reported with the same weight as one that kills.

* **Doc 300's scoring gradient is real.** Robust to the cut point (all seven), to the cut-free rank
  correlation (+0.464), to excluding lead-back absence (+5.10, p=0.0000), to scoring only in weeks the
  starter played, to removing already-rostered men (+4.37, p=0.0000), and to both filters at once
  (+3.81, p=0.0175). **It is worth wiring in. Only the rate half and the independence claim are wrong.**
* **Doc 299's null choice is correct** and more conservative than the alternative.
* **Doc 297's central answer to A1 stands and my objections strengthen it.** Yes the missing absence
  model changes the drop order; yes the missing streaming model is the larger of the two distortions;
  yes they push in opposite directions so the errors compound rather than cancel. Every criticism in §5
  makes the case for building A1 sooner.
* **Doc 296's C17, its reproduction-before-fix, its self-report of a wrong first fix caught by diffing
  against the shipped file rather than against itself, and its tightening of a loose check** are all
  correct and none of it needed changing.
* **Doc 294's discipline is the model.** It states its forking paths, names which cut came from reading
  output, reports the committed script disagreeing with the draft, and labels accordingly.
* **Doc 298's join hygiene** (fuzzy-matching all 43 unjoined free receivers to confirm nothing young was
  silently dropped) is §3's identity rule done properly.

---

## 11. PROPOSED DIRECTIVE TEXT

Offered as drafts for the directive chat to accept, reject or rewrite. Numbers are four-season and
should be re-run on five before they are frozen (§2.1).

**§4.27 or a new §4.34, replacing whatever carries doc 300's band table:**

> **THE WEEK-1 BACKFIELD SHARE PREDICTS POINTS AND DOES NOT INDEPENDENTLY PREDICT A STARTER, AND IT
> MULTIPLIES THE JOB-OPENS TERM RATHER THAN REPLACING IT (docs 300, 302).**
> **POPULATION: team-seasons 2021-2024 whose week-1 RB usage leader and second back both played, and
> whose second back appeared in 4+ of weeks 2-14. n=118.** The second back's share of week-1 RB carries
> plus targets correlates with his weeks 2-14 half-PPR per game at **Spearman +0.464**, and the relation
> holds at every split from 15% to 45%, so the bands are not load-bearing.
> **BUT THE PUBLISHED 7 / 11 / 39 / 50 STARTABLE ROW IS RETRACTED.** In 44 of 118 team-seasons, and
> **14 of the 24 in the top band**, the man the design called "the lead back" did not lead his own team
> over weeks 2-14: the labels were reversed and the "handcuff" was a starter (Conner, Gibbs, Bijan,
> Stevenson, Kyren, Pollard). On the 74 rows where the labels held, 35%+ against under 35% is **ppg
> +2.12 (p=0.0063) and startable +2 points (p=0.5553)**. **The doubling of a low base rate survives.
> The 50% does not and must not be quoted.**
> **AND IT IS NOT INDEPENDENT OF THE MAN AHEAD.** In the top band the lead back missed a week 79% of
> the time against 48-59% elsewhere. Where the man ahead is durable the top band is 20% startable; where
> he is not it is 57%. **So a seat price multiplies the week-1 share by the job-opens probability. It
> never substitutes one for the other.**

**§4.28 or wherever doc 299 lands, and `0.5(a2)`'s confirmed list:**

> **A VETERAN ARRIVAL REALLOCATES TARGETS, AND THE MAN IT TAKES THEM FROM IS THE SECOND RECEIVER, NOT
> THE THIRD AND FOURTH (docs 299, 302).** Matt's mechanism is confirmed; the slot doc 299 tested is not
> where it acts. Measured on team-seasons 2021-2024 with a 60+ target incumbent still on the team,
> 42 arrivals against 59 controls, **with every share computed over the HOLDOVER POOL so that adding a
> target-earner cannot lower shares arithmetically**: 3rd+4th **−0.008, p=0.21**; 2nd receiver
> **−0.045, p=0.011**. On the published design, which leaves the arrival in the current-season
> denominator and not the prior one, the 3rd+4th figure is −0.022 at p=0.014 **and the untested 2nd
> receiver is −0.049 at p=0.002, twice as large.** **A share is a share of one hundred percent: never
> compare shares across two seasons whose denominators contain different men.** Live: Denver's squeezed
> man is **Troy Franklin**, not Pat Bryant.

**§0.2, appended to the severity-estimate paragraph:**

> **AND REPORT THE INTERVAL OF THE THING THAT IS UNCERTAIN, NOT THE ONE THAT IS CHEAP TO SHRINK.** Doc
> 297 reported `−0.98 ± 0.02` on a drop cost. That is the standard error of the mean over 6,000
> simulation draws and shrinks with more draws. The uncertainty that mattered was the ±2 percentage
> points on a 17.1% absence rate measured on 94 player-seasons. **A Monte Carlo standard error printed
> beside a measured quantity reads as precision the measurement does not have.**

**§0.5(c), appended to the collision rule:**

> **AND A GREP TOKEN THAT CAN MATCH A LEGITIMATE ROW CAN NEITHER CLOSE A LEDGER ROW NOR HOLD ONE OPEN
> (`AUDIT_LEDGER` row 13, and C17's own first version, both 12 Sept).** A token has to be scoped to the
> object it is auditing. `class="p">Tyjae Spears` matched the free-pool table where he belongs and would
> have held row 13 open forever; `'Jordan James' not in block` failed on the FIXED code because the fix
> prints his name in the reason. **Scope the token, then run it against both the broken and the fixed
> tree.**

---

## 12. PROPOSED `AUDIT_LEDGER` ROWS

In the ledger's own column format. Row numbers assume 29 is the current maximum.

| # | where it lived | the sentence as it stood | replacement | grep tokens | code | page | directive | prompts | status |
|---|---|---|---|---|---|---|---|---|---|
| **27 (AMEND)** | 0.5(a2); wire's 3-of-3 tag on Pat Bryant | "the 3rd and 4th receivers lose 4.4 points of team target share when a 60+-target veteran arrives ... p=0.005 ... **Denver 2026 is that cell**: Mims and Bryant the 3rd and 4th men" | the published effect is denominator dilution: with the arrival removed from the denominator, 3rd+4th is −0.008 (p=0.21) and the surviving loss is at the **2nd receiver**, −0.045 (p=0.011), a slot doc 299 never tested. Matt's mechanism is confirmed in a different place. **Denver's squeezed man is Troy Franklin.** Doc 302 | `Pat Bryant` inside the arrival note only; `4.4 points`; `room below` | n/a | **NO** | **NO** | n/a | **OPEN** |
| **29 (AMEND)** | seat price on both pages; 4.27's applied form; Tuesday read | "7% / 11% / 39% / 50% ... base rate 24%, n=143 ... permutation p=0.0000 on ppg and p=0.0003 on the rate. Black is at 45%" | the points half replicates and is robust to every cut (Spearman +0.464); **the startable half does not survive the labelling check**: on the 74 of 118 rows where the labelled lead back kept the job, the 35% split is +2 points at p=0.5553. **The 50% must not be quoted.** And the signal multiplies the 46% job-opens term rather than replacing it (20% startable where the man ahead is durable, 57% where he is not). Doc 302 | `50%` inside the band table; `7% / 11% / 39%` | **NO** | **NO** | **NO** | **yes, Tuesday read carries it** | **OPEN** |
| **30 (NEW)** | `sheet_constants.json` `absence.rate.K` | `"K": 0.137` beside a note saying the kicker cell "is not used" | 0.137 is the QB and TE rate. Doc 297 measured kickers at **0.213** on a cell it says should not be quoted. A value a lookup will silently return is used whether or not a note says otherwise. **Delete the key or set it to 0.213 and drop the clause.** Doc 302 | `"K": 0.137` | **NO** | n/a | n/a | n/a | **OPEN** |
| **31 (NEW)** | `sheet_constants.json` `absence.streamer.K` | `"K": 7.5` | no source anywhere; `streamer_note` attributes QB, RB, WR, TE and D/ST and is silent on K. §3 calls that `[NO SOURCE]`. Doc 302 | `"K": 7.5` | **NO** | n/a | n/a | n/a | **OPEN** |
| **32 (NEW)** | doc 297 §6 against `sheet_constants.json` `absence.note` | doc: "No code change shipped today. The sheet still prices byes only and says so on its own face." JSON: the block exists "so the page can price a bench body instead of printing 0.0 for him." | one of the two is wrong; if the page consumes the block, its printed disclaimer is false. **Settle with one grep of `sheet_engine.py` and `wire.py` for `absence`.** Doc 302 | `prices byes and not injuries` | **UNKNOWN** | **UNKNOWN** | n/a | n/a | **OPEN** |
| **33 (NEW)** | `redteam_controls.py` against the 12 Sept 16:48 commit | doc 300: "44 of 44 red-team controls pass against the production path" | true, and a regression test rather than coverage: the controls file was last written at 13:09:08 and every production file at 16:48:5x. **Four changes have no control** (section-0 split, the `absence` block, the drop-cost box, the ESPN team name, the last of which the harness cannot currently test because its fake `mRoster` carries no name field). Doc 302 §9 | `44 of 44` | **NO** | n/a | n/a | n/a | **OPEN** |
| **34 (NEW)** | `redteam_controls.py` C16 base check | `check('C16', 'base run writes FREE_UNRANKED_<date>.csv (header, nobody off the board in the recorded pool)', fb is not None and len(fb) == 0)` | the recorded 10 Sept pool has **zero** off-board free players while the live 11 Sept pool had **71** (doc 296) and 71 is typical (doc 292). **Doc 298's entire mechanism has never run against a realistic population.** Refresh `WIRE_20260910.csv` to an 11 Sept snapshot. Doc 302 §9.3 | `len(fb) == 0` | **NO** | n/a | n/a | n/a | **OPEN** |
| **35 (NEW)** | doc 297 §2 | "Per season it is stable and not one bad year: QB 8/13/13/22%" | 8% to 22% is a factor of 2.75 and the sentence is contradicted by the figures in its own clause. Re-measured on 2021-2024 the QB rate is **8.7%** against the shipped 13.7%. RB (18.0 vs 17.1) and WR (13.4 vs 15.0) reproduce. Doc 302 §5.1 | `stable and not one bad year` | **NO** (the constant is unchanged pending a five-season re-run) | n/a | n/a | n/a | **OPEN** |
| **36 (NEW)** | doc 297 §4; `seat.relief_ppg` | the handcuff bracket uses 11.2; the shipping constant is 12.13 | two numbers for one quantity (0.5c4). 11.2 is doc 244's median relief over 40 events; 12.13 is n=51 on NFL team-seasons 2022-2025. Also a **median used as an expectation**. Pick one and record the loser as superseded. Doc 302 §5.5 | `11.2` `12.13` | **NO** | n/a | n/a | n/a | **OPEN** |

---

## 13. OPEN THREADS, WITH OWNERS

**Mine (the red team's), NOT YET RUN, testable forms already written:**

* Every table in this report on 2025. `--years` wired, file on Matt's tree.
* Doc 299 with TE pooled into "receiver", and with the plain share rather than the per-game-rate share.
* Doc 300's tie-break at 45%+ run both ways on the nine affected rows.
* Doc 300's outcome keyed on `(team, player_id)` rather than `player_id`, so a traded RB2's points with
  a new team do not count.
* Doc 299 design 2 with the incumbent's own change as a within-team covariate.

**The directive chat's:**

* The eight ledger rows in §12.
* The four directive patches in §11.
* Decide whether `absence` is consumed (§8 item 5). One grep.

**Matt's, and only these:**

* `py wk1_redteam.py --years 2021 2022 2023 2024 2025`
* `py squeeze_redteam.py --years 2021 2022 2023 2024 2025`

Neither writes anything. Neither needs ESPN. Both take under a minute.

**BLOCKED:** `stats_player_week_2025.csv` in this container. §2.1.

---

## 14. FALSIFIER REGISTER

Matt's rule that a preference should be recorded with the condition that brings it back, applied to my
own findings so the next reader can reverse them cheaply.

| my finding | what would reverse it |
|---|---|
| Doc 300's startable half is dead | The 2025 season adding enough clean rows that the labels-held subgroup's 35% split reaches p<0.05 on the rate. Currently n=74 with 18 above the cut. |
| The labelling problem is real | A defensible argument that the decision does not care which man is nominally the starter. **I considered this and rejected it**, because 38% of the top band were rostered fantasy starters and the outcome distribution is theirs. But if the directive chat restricts to claimable men and accepts D1's 60%, that is a coherent position and I would not fight it hard. D1 is the strongest honest case for the original number. |
| Doc 299's 3rd+4th effect is dilution | The holdover design being the wrong object, for example if the right question is genuinely "how much of the pie does he hold" rather than "did he lose ground to his teammates". The former is a fantasy-points question and the latter is a mechanism question. **Doc 299 framed it as a mechanism ("the arrival compresses everyone below him"), which is why design 2 governs.** If the directive chat reframes it as a pie question, design 1 is correct and the finding stands as published. |
| The 2nd receiver is the squeezed slot | It failing on 2025, or on the TE-pooled definition. n=40 vs 56. |
| The absence rates need a five-season re-run | Nothing. This one is just arithmetic and the 2025 file settles it. |
| The controls gap | A control existing somewhere other than `redteam_controls.py`. I checked only that file. If `check_kit.py` or a `--selftest` elsewhere covers the section-0 split, my §9 is wrong and I would want to know. |

---

## 15. FILE INVENTORY FOR THIS SESSION

| file | location | id | bytes | archived first? |
|---|---|---|---|---|
| `302_the_second_back_was_often_the_first.md` | `Source\` | `142nTnMfg7X_DexnnUosQzP5Jh9RbuX5F` | 19,303 | new file, nothing overwritten |
| `wk1_redteam.py` | `Scripts\research\wk1\` | `1j1AsF0wNC2mnvIqBX_MZHie8EJnXqJ79` | 12,521 | new file, `week1_share.py` untouched |
| `squeeze_redteam.py` | `Scripts\research\f1\` | `1_o-WxJW3zz-baa5b88J2sJqhQQv6-I4I` | 7,593 | new file, `squeeze.py` untouched |
| this file | `2026\` root | | | new file |

**Nothing on the drive was overwritten, nothing under `Scripts\` outside the two new research files was
touched, no waiver claim was filed, nobody was dropped, and nothing was written to ESPN.**
`check_kit.py` will report the two new research scripts as unpinned stragglers, which is correct and
expected; pin them or leave them, they are research and not draft-path.

Doc numbers 302 was free at the time of writing, confirmed by listing `Source\` (301 was the maximum).
