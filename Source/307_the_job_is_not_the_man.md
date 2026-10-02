# 307. THE JOB IS NOT THE MAN, AND THE TEAM IS NOT THE BOARD'S

**14 September 2026.** Started from one line of Matt's: *"Kaleb Johnson is indeed a RB for the
Green bay packers."* He was right, the wire said PIT, and chasing that one cell found three
defects, two of them live on the page he reads before a waiver claim.

**ALL THREE ARE FIXED, PINNED AND CONTROLLED.** `Scripts\research\redteam\ctl_307.py` runs the
negative controls from its own location and prints ALL CONTROLS PASS.

---

## 0. THE ACTIONABLE PART FIRST

1. **Kaleb Johnson is a Packer.** Week 1: **0 snaps, 0 carries.** Not a claim. The team correction
   closes the lane rather than opening it.
2. **STOP QUOTING 152 FOR THE GREEN BAY JOB. IT IS 241.** Everything downstream of that number was
   understating the one indefinitely vacant backfield in the league by 89 points.
3. **The free half of that backfield is Chris Brooks**, 11.5% owned, who took **56% of Green Bay's
   RB snaps in week 1**. `inherit_2026.csv`'s 13 Sept line calling him "RB3 on a 152-pt job" is
   retracted; week 1 refutes both halves of it.
4. **Kaelon Black stays ahead of him.** SF's job pays 302, Black out-carried McCaffrey 14 to 10 on
   43% of snaps, and he is 15.4% owned. Bigger job, better week 1.
5. **Matt ran all three and the artifacts verify** (section 7). **One more run of `wire.py` is
   needed** for the bye fix in 1b, which was found after his run. On `matt_todo.txt`.

---

## 1. `job_ceil` IS A TEAM CONSTANT AND A MOVED PLAYER CARRIES THE WRONG TEAM'S

**THE DEFECT.** `wire.py` built its `team` column from `b.get('team_c')` -- the FROZEN DRAFT BOARD.
Eight lines above, in the same loop, the off-board branch (doc 292, newer code) already used the
LIVE pull's `proTeamId`. Nobody had ever compared the two.

**WHY IT IS WORSE THAN A COSMETIC ERROR.** `depth_map.py` stamps `job` and `job_ceil` on every
player of a team, not on the player: every Green Bay row in `depth_map.csv`, Tucker Kraft and
Jordan Love included, reads "LEAD BACK, 241". Doc 224 had already asserted this for the stash lane
("reading job_ceil on a WR row gives you that team's running back"). Nothing asserted it here. So a
player who changed NFL teams after the board froze kept the OTHER team's backfield number, and the
row read as authoritative:

| on WIRE_20260914.csv | the truth |
|---|---|
| Kaleb Johnson, **PIT**, "unsettled job, worth 174" | a Packer. 174 is Pittsburgh's number. |
| Emari Demercado, **KC**, "lead back job, worth 249" | a Cowboy, 5 snaps (9%) behind Javonte Williams. 249 is Kansas City's. |

**MEASURED:** 7 of 482 board rows carry a stale team against the 09-07 pull, and nflverse's week-1
stats and rosters agree with the pull on every one of the six that played
`[TESTED: Boutte NE->HOU, Demercado KC->DAL, Atwell MIA->LAR, Joly DEN->MIA, Johnson PIT->GB,
Ewers MIA->JAX, Long JAX->ARI]`. The other eleven apparent mismatches were WAS against WSH, which
is why nobody saw the real six: the noise hid the signal.

**THE FIX.** The live team wins; the board is the fallback for a player ESPN serves with no pro
team. `flags()` takes a `moved_to` argument and **drops the job clause** when it is set, replacing
it with "moved to GB since the board". The grade and the player-level signals are his own and
survive. And the run **prints every moved row by name**, because a silent correction is how the
stale team survived four wire builds.


### 1b. AND THE BYE IS THE SAME DEFECT ONE COLUMN OVER, WHICH I SHIPPED AND THEN CAUGHT

**The first version of the team fix corrected seven rows and left all seven byes pointing at the
club the man left.** The bye came off the board beside the team, so correcting one and not the
other produced a row that is confidently wrong in a new way: **Kaleb Johnson read GB with bye 9,
which is Pittsburgh's; Green Bay is on 11.**

| row | team fixed to | bye it kept | bye it should carry |
|---|---|---|---|
| Kaleb Johnson | GB | 9 (PIT) | **11** |
| Emari Demercado | DAL | 5 (KC) | **14** |
| Kayshon Boutte | HOU | 11 (NE) | **8** |
| Tutu Atwell | LAR | 6 (MIA) | **11** |
| Justin Joly | MIA | 10 (DEN) | **6** |
| Quinn Ewers | JAX | 6 (MIA) | **7** |
| Greg Dortch | BUF | 6 (DET) | **7** |

**Seven of seven wrong, and every one exactly the old team's bye.** `[TESTED against byes_2026.csv,
which resolves all 32]`

**THIS IS WORSE THAN THE JOB FLAG IT SITS NEXT TO.** Section 4.32's first term is what a man adds
to the nine Matt starts **over the weeks he is needed**, and the bye is the only fully
deterministic part of that whole calculation. A wire row bought to cover week 9 that is actually
off in week 11 fails at the one thing the page can be certain about.

**Fixed:** `load_byes()` reads `Source\byes_2026.csv` through `team_key`, checks all 32 resolve,
and NAMES a miss on the page rather than defaulting (section 3). The bye is replaced only on a
moved row, so nothing else on the sheet changes. The run now prints `PIT -> GB  bye 9 -> 11`.

**AND THE CONTROL EARNED ITS KEEP THE WAY SECTION 0.2 ASKS.** Block H fired against the shipped
`WIRE_20260914.csv` and named all seven rows, including **Greg Dortch, whom I had missed** when I
listed the moved rows by hand. It also now reports a wire file older than its builder as **not
checked** rather than FAILED, because a checker that cries wolf is one you learn to ignore (doc 146).


---

## 2. A JOB'S WORTH FELL BECAUSE ITS HOLDER LEFT. THE JOB DID NOT SHRINK.

**THIS IS THE ONE THAT COST REAL POINTS.** Section 4.20 defines `job worth` as *"ESPN's projection
for the man currently holding the job."* When that man is removed from the team, **ESPN cuts HIS
projection**, and `depth_map.py` reads the cut number as what the JOB pays.

Josh Jacobs went on the Commissioner's Exempt List on 30 August 2026. Traced across every 2026 pull
on the drive:

| pull | top GB back | proj | ESPN status | 2nd | gap | label |
|---|---|---|---|---|---|---|
| 08-20 | Josh Jacobs | **241.0** | QUESTIONABLE | Lloyd 78.2 | 162.8 | LEAD BACK |
| 08-23 | Josh Jacobs | **241.0** | QUESTIONABLE | Lloyd 78.2 | 162.8 | LEAD BACK |
| 08-29 | Josh Jacobs | 241.0 | | | 162.8 | LEAD BACK |
| 08-30 | Josh Jacobs | 241.0 | | | 162.8 | LEAD BACK |
| **09-03** | Josh Jacobs | **152.5** | DAY_TO_DAY | Lloyd 124.4 | 28.1 | UNSETTLED |
| 09-05, 09-07 | Josh Jacobs | 152.5 | DAY_TO_DAY | Lloyd 124.4 | 28.1 | UNSETTLED |

**THE SAME ARITHMETIC PRODUCED ONE RIGHT ANSWER AND ONE WRONG ONE, WHICH IS WHY IT SURVIVED.**
The gap collapsing 163 to 28 **correctly** flips the label to UNSETTLED: the job genuinely is
unsettled now. The ceiling falling 89 points is **wrong**: the absent man's projection is not the
job. One input, two outputs, opposite verdicts.

**IT WAS ALSO SITTING IN TWO FILES AT ONCE AND NOTHING COMPARED THEM.** `depth_map.csv` on the
drive (6 Sept) still holds **241**; `player_context.csv` (7 Sept), which is what `wire.py` actually
reads, holds **152**. The pipeline contained both the right number and the wrong one, and the page
read the wrong one.

**THE THRESHOLD IS MEASURED, NOT CHOSEN.** Across all 32 teams between 08-23 and 09-07 the lead-RB
projection moved by a **median of 0.5 points, p90 3.0**, and the largest fall other than Green Bay
was **2.9** (NYG). Green Bay fell **88.6**. `[TESTED, n=32 teams, 8 pulls]` A guard at 40 cannot
reach the noise and cannot miss this.

**IT CANNOT KEY ON injuryStatus, AND THIS IS THE PART THAT WOULD HAVE BITTEN THE OBVIOUS FIX.**
ESPN carries Jacobs as **DAY_TO_DAY**, not OUT, because an exempt-list absence has no injury code.
A status guard would not have fired. The guard therefore keys on the only thing that is reliable:
**a job's worth may not fall below what the earliest 2026 pull says it is worth.**

**CONTROL, ALL FOUR CONDITIONS, RUN BEFORE THE FIX SHIPPED:**
* against its own baseline pull it lifts **nothing** (a guard that fires against itself measures noise)
* it lifts **GB 152 to 241** on all four post-exemption pulls and on none of the four before
* across all 8 pulls and 32 teams the set of teams ever lifted is exactly **{GB}**
* `job_gap` is untouched, so **GB still labels UNSETTLED**. The label was always right.

**WHAT IT CHANGES ON THE PAGE.** `load_seats()` in `sheet_engine.py` sorts the inheritance table by
`job_pays`. Green Bay was 30th of 32 in `inherit_2026.csv` at 152.5, and `free` was set to
`rostered` so it did not appear at all. Corrected, with Chris Brooks as the free next man, it
enters at **9th of 14** on that list, level with Dallas.

---

## 3. THE SEAT TABLE PRINTED THE STARTER'S STATUS UNDER THE BACKUP'S NAME

Found while checking what section 2 would do to the rendered page. `live_tag` is the **starter's**
status and it rendered in the **backup's** name cell. **Ten of the 32 seat rows carry one**, and it
was on the number-one recommendation: Kaelon Black's row read *"Kaelon Black, SF, bye 8, 15.4%
rostered, questionable"* when it is **McCaffrey** who is questionable. Chris Brooks' new row would
have read *"out"*.

**This is doc 301's defect exactly -- the row named the wrong man -- in a second place.** The tag
now renders beside the starter, in the cell that holds his name, as "questionable now" / "out now".

**OPEN, NOT FIXED, AND NAMED (section 0.5a4).** `p_opens` is a single constant, **0.46**, applied
to every seat as "the odds this job opens". **Green Bay's job is already open**, so its expected
value is understated by roughly 1/0.46. The obvious patch -- set p=1 when `live_tag` is `out` -- is
**refused**, because one week out and gone indefinitely are not the same event, and over-correcting
exactly that distinction is what doc 305 had to walk back on the moves list four days ago. What is
needed is a field that separates a week's absence from a vacancy, and `inherit_2026.csv` does not
carry one. **BLOCKED on that column; it is a build_inherit.py change, not a sheet_engine one.**

---

## 4. WHAT WEEK 1 SAYS ABOUT THE THREE BACKFIELDS THIS TOUCHES

`[SOURCED: nflverse stats_player_week_2026 and snap_counts_2026, retrieved 14 Sep 2026, 30 of 32
teams; DEN and KC are the Monday nighter and were not yet in the file]`

| | snaps | share | carries | targets |
|---|---|---|---|---|
| **GB** Chris Brooks | 38 | **56%** | 7 | 1 |
| **GB** MarShawn Lloyd (rostered) | 30 | 44% | **13** | 1 |
| **GB** Kaleb Johnson | **0** | 0% | 0 | 0 |
| **SF** Christian McCaffrey | 36 | 55% | 10 | 8 |
| **SF** Kaelon Black | 28 | 43% | **14** | 1 |
| **DAL** Javonte Williams | 41 | 71% | 12 | 5 |
| **DAL** Emari Demercado | 5 | 9% | 2 | 0 |

**Green Bay is a genuine split and week 1 did not resolve it: Brooks led snaps, Lloyd led carries.**
Green Bay ran only **20 RB carries** all game, which is a warning about the whole room and not just
about who wins it. Brooks is the claimable half at 11.5% owned; Lloyd is rostered at 79.6%.

**Kaelon Black is the better row on every axis** and stays the number-one claim.

---

## 5. THE METHOD POINT, BECAUSE IT WILL RECUR

Section 4.20's definition is *the man currently holding the job*. **When the holder is gone there is
no such man**, the definition has no referent, and the code silently substituted a ghost's
discounted projection rather than failing. That is the shape to watch for: **not a missing value,
but a definition whose subject stopped existing while its arithmetic kept running.**

The sibling of this is section 0.6's population drift and section 4.23's outcome-conditioning. All
three are the same family: **the number is computed correctly against an object that is no longer
the object you meant.**

**AND MATT FOUND IT FROM ONE CELL.** He did not know about the ceiling, the flags, or the seat
table. He knew that Kaleb Johnson plays for Green Bay. Doc 200 and doc 228 both started the same
way, and section 0.6 rule 4 already says it: **a conclusion that contradicts his direct experience
is a data question first.**

---

## 6. NOT YET RUN, WITH THE TESTABLE FORM WRITTEN

* **[OPEN]** `p_opens` is one constant applied to a job that is already open. Needs a vacancy field
  in `inherit_2026.csv`. **BLOCKED on that column.**
* **[NOT YET RUN]** *Does the snap leader or the carry leader in a split backfield predict who holds
  the job four weeks later?* Population: every team-season 2021 to 2025 where the top two backs were
  within 15 points of snap share in a week, outcome: usage share in weeks +2 to +5. Green Bay is the
  live case and I cannot answer it from week 1.
* **[NOT YET RUN]** *How many other rows on the board carry a team-constant flag whose team is right
  but whose number is stale for a different reason?* Doc 224 asserted it for WRs; the general audit
  has not been run.
* **[OPEN]** `WIRE_*.csv`'s `value` column is the preseason board VOR and **nothing in the pipeline
  moves a player whose situation changed after the freeze.** Brooks went from RB3 behind Jacobs to
  co-lead of a vacant backfield and his wire value did not move one point. The job flag is
  decoration; the sort key is frozen. This is the largest remaining defect in the wire and it is
  bigger than either fix above.


---

## 7. VERIFIED ON THE ARTIFACT, NOT THE EXIT CODE

Matt ran `depth_map.py`, `wire.py`, `check_kit.py`. Checked on his own files rather than taken on
his word (section 0.2, section 0.5d):

* **`depth_map.csv`**: GB reads **job_gap 28, UNSETTLED, job_ceil 241**. Every other team matches
  its pre-fix value to the point. Green Bay sits 13th of 32 by job worth, up from 30th.
* **`player_context.csv`**: five GB rows now carry 241; **no row anywhere carries 152.**
* **`WIRE_20260914.csv`**, rebuilt: **seven rows read "moved to X since the board" and none of
  them carries a job number.** Kaleb Johnson is on GB with Pittsburgh's 174 gone; Emari Demercado
  is on DAL with Kansas City's 249 gone; **Chris Brooks reads "unsettled job, worth 241".**
* **Still wrong on that file, and fixed in code after it was built: the seven byes** (section 1b).
