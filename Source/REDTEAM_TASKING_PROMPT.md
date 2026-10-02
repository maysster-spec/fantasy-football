# REDTEAM_TASKING_PROMPT

*Rewritten 16 Sept 2026, 08:40; JOB 3 added 22:45; JOB 4 added 17 Sept 00:20; SECTION C added
19 Sept 12:30, four jobs, NAMED not numbered. Previous copies in
`_archive\REDTEAM_TASKING_PROMPT_20260916b.md` and `_20260916c.md`.*

*Original note: the previous target was docs 291 to 300, and its two Fable jobs came
back as docs 319 and 320; both are now IN THE CODE (`usage_depth()` in `wire.py`, the both-ways fill
sentence in `sheet_engine.py`, controls C18 to C20), so the file is re-aimed. Old copy in
`_archive\REDTEAM_TASKING_PROMPT_20260916.md`. One name, no version.*

> **THE LETTER "A" MEANS TWO THINGS AND IT COST A ROUND TRIP ON 17 SEPT. READ THIS FIRST.**
> **SECTION A is a CLAUDE job**: a second reader on docs 314 to 321, pasted into a new chat in this
> project. **SECTION B holds the FABLE jobs, numbered 1 to 4.** They are independent. Neither waits
> on the other and there is no order between them.
> **Fable's first result came back in a file Matt named `rable run A.txt`, and that file is
> SECTION B's JOB 1, not section A.** Same letter, two objects, and the confusion was entirely
> reasonable. **Fable's runs are JOB 1, JOB 2, JOB 3, JOB 4. Never "run A".** Its content is
> `Source\327_one_currency_the_order_holds_and_the_numbers_do_not.md`.
>
> **STATUS, 17 Sept 22:30: SECTION A is RUNNING. SECTION B's JOB 1 is DONE (doc 327). JOB 2 is the
> next one to send to Fable, and its amendment box is below. JOBS 3 and 4 are queued.**
>
> **AND THERE IS A SECTION C NOW, ADDED 19 SEPT. Four jobs, named rather than numbered, out of
> doc 374's catalog. Its own status box corrects two lines of the one above: JOB 3 has RUN
> (doc 352), and JOB 4 has RUN (doc 382, 22 Sept; it was WRITTEN AND UNRUN until then). THE FIRST JOB TO SEND IS SECTION C's TAKE CONTRACT, not JOB 2.**

> **NAMING FIX, and it bit once already.** The heavy jobs below are **JOB 1** to **JOB 4**, never
> B-numbers. Doc 290's catalog already owns B1 to B11 and F1 to F3, and doc 319 opened by calling
> this file "the catalog", which put two different B1s in the same project. Letters are the
> catalog's. Jobs are numbered.

---

## A. PASTE THIS INTO A NEW CHAT IN THIS PROJECT

> **READ THIS BOX FIRST, 17 SEPT 22:00. SECTION A HAS NOT BEEN RUN, AND IT SHOULD NOT BE PASTED
> AS IT STANDS: two of its six targets were answered tonight and three of its numbers are stale.**
> Paste it WITH this box, so the reader does not spend a session re-finding what already shipped.
>
> **ITEM 5 IS PARTLY ANSWERED. Do not re-measure `p_opens`.** It is no longer 0.46 flat. Doc 343
> shipped a per-man P(the job opens), read off the backup's share of his team's week-1 RB carries
> plus targets: **0.476 / 0.438 / 0.533 / 0.636** across bands <20 / 20-30 / 30-40 / 40%+, n=126
> team-seasons 2022-2025, permutation +0.36 at p=0.027 on the seats-only cut. `seat.p_opens_by_band`
> is in the constants and `inherit_2026.csv` carries `wk1_share` and `wk1_band`. **WHAT IS STILL
> SOFT AND IS NOW THE WHOLE OF ITEM 5: `relief_ppg` 12.13 (n=51) and `weeks_played` 3.02.** Doc 343
> tried to move the weeks and failed its own falsifier at p=0.286; that is UNDERPOWERED, n=6 in the
> top band, and 2021 resolves it. Trace those two, and the rest of the `contest` block, exactly as
> the item says.
>
> **ITEM 6'S THREE NUMBERS ARE ALL WRONG NOW, AND ITS EXAMPLE IS FIXED.** `wire.py` is **110,233**
> bytes, `sheet_engine.py` is **115,530**, and `redteam_controls.py` runs **44 checks, not 56** --
> the count moved and this file never did, which is the defect it is asking about, one level up.
> **`form_2026.csv` IS NOW ON THE HARNESS'S INPUT LIST** (doc 342, ledger row 86), so doc 321's
> example is closed and the workload lane is exercised by a control for the first time. **The item
> stands as written otherwise, and it is still the most valuable of the six: find the NEXT input
> the harness does not supply, and the next change with no control over it.**
>
> **AND TWO NEW ROWS TO ATTACK THAT DID NOT EXIST WHEN THIS WAS WRITTEN.** `AUDIT_LEDGER.md` is
> **89 rows, not 60**. Rows 85 and 89 are tonight's and both are about verification failing rather
> than arithmetic failing: a `return` that handed back two values where the caller unpacked three
> and killed every run, and a commit that reports `written` while the drive keeps the previous
> version. **Row 89 carries a negative control that reproduces the second one. Try to break that
> control** -- if the commit behaviour is not what it says, every "verified on the drive" claim in
> this project is worth less than it reads.
>
> **CORRECTION, 17 SEPT 22:45, AND IT IS THE MOST IMPORTANT LINE IN THIS BOX: DOCS 316 AND 317 DO
> NOT EXIST.** Checked two ways, a directory listing of `Source\` and the project doc store: the
> range runs 312, 313, 314, 315, **[no 316, no 317]**, 318, 319, 320, 321. **The WORK shipped and
> the DOCS were never written.** That is mine, and it is 0.5(c)5's missing-file check failing on a
> tasking prompt rather than on a printed page.
> **SO ITEM 2 BELOW POINTS AT NOTHING, AND ITS SUBJECT IS REAL.** The drop-cost ladder exists in
> three places and the item should be run against these instead of doc 317:
> **(a) `drop_costs()` in `Scripts\sheet_engine.py`** — the shipping arithmetic, which is the
> object that matters; **(b) doc 327 section 3**, which prints the whole ladder in two currencies
> side by side (Hockenson 0.0 on the page against 2.7 in one currency, Washington 0.0 against 6.1,
> Pineiro unpriced in both); **(c) `Source\matt_todo.txt`, the two 16 Sept entries**, which is
> where doc 316's four fixes were recorded instead of in a doc. **Item 2's two questions are
> unchanged and both are good.**
> **AND DOC 316's SUBJECT IS ALSO REAL:** the five-row cap on Priority pickups, which cut Kaelon
> Black at 6th on worth (2.4 against a 5th place of 3.3) before his own 56%-contested warning could
> be read. The cap now keeps any row the page says to claim first. `sheet_engine.py` is the object.
>
> **THE DOC RANGE IS UNCHANGED: 314 to 321.** Docs 342 and 343 are context, not targets; attacking
> them is a different session and section B's JOB 2 already carries their open threads.


You are the second reader on eight documents written between 15 and 16 September 2026, docs 314 to
321 in `G:\My Drive\_Fantasy\2026\Source\`. They are all mine. Your job is to try to break them,
not to summarise them. The project directive in your instructions governs, sections 0.2 and 3 in
particular: every stored finding carries its baseline, its population and its sample size, and a
tested claim can still be the wrong claim.

Read these first, in this order, and read the files rather than a summary of them:
`AUDIT_LEDGER.md` (60 rows, what this audit has already killed), then **314, 317, 318**, which carry
the new numbers, then **319 and 320**, which are Fable's and are now implemented, then **321**, which
is the regression that shipped past every check we had. Then `Scripts\research\rival_need.py`,
`Scripts\research\b1\`, `Scripts\research\b2\` and `Scripts\research\redteam\redteam_controls.py`.

**ATTACK THESE SIX, IN THIS ORDER. Ranked by what it costs us if they are wrong.**

1. **Doc 314's contest bands** (under 5 touches to 15-plus: 1.17 to 2.27 filers, 14% to 56%
   contested, n=403, r=+0.296, p=0.00005). Newest and most load-bearing, because it now ORDERS the
   claim list and the order is the whole of the strategy (4.32: only the first winning claim comes
   at his real priority). **The selection problem I can name and have not fixed: the rows are
   EXECUTED transactions, so a man nobody filed on has no row at all.** Is "filers per man"
   therefore a count conditioned on at least one filer? Rebuild the zero-filer population from the
   week-by-week free pool doc 252 already reconstructed, re-run the bands on it, and say whether
   they survive. Then find the selection problems I have not named.
2. **Doc 317's drop-cost ladder**, which is on the page and is what he reads before every claim.
   Each man is netted against the best free body at his position. Two things: is "best free body"
   the right counterfactual when the same free pool is being depleted by the add that motivated the
   drop, and are K and D/ST honestly "not priced" rather than silently skipped?
3. **Doc 319's floor, now printed.** The page computes the second figure deterministically as
   `tot - len(empty) * min(weekly, streamer)`. Your arm C is about 0.6 higher for Schultz because it
   also draws absences. I have called the printed number a FLOOR. Find a case where it is not:
   a player, a bye pattern or a bar shape where the deterministic figure EXCEEDS the simulated one.
   If it exists the sentence is wrong, not conservative.
4. **The p-values across 314 to 320.** I ran several band splits and reported the ones that
   separated. Count the comparisons actually made in each doc and say which findings survive a
   correction for them. Doc 314's p=0.00005 and doc 320's McNemar p=0.043 are the two that matter,
   and the second is the thinner.
5. **Every inherited number in `Source\sheet_constants.json`'s `contest` block.** Trace each to the
   doc that measured it and say whether that doc's population matches the use on the page. The seat
   constants are the known soft spot: `p_opens` 0.46 (n=115) is flagged UNDER RE-CHECK in ledger row
   2 and catalog B4, and `relief_ppg` 12.13 comes from n=51.
6. **The code and the controls.** `Scripts\wire.py` (107,443 bytes) and `Scripts\sheet_engine.py`
   (94,113) and `Scripts\research\redteam\redteam_controls.py` (56 checks). **Doc 321 is the brief
   for this one: the harness passed 44 of 44 for five days while the page's entire workload lane was
   switched off, because `form_2026.csv` was not in its input list.** Find the next input the
   harness does not supply, and the next change with no control over it.

**RULES.** State each claim in its testable form in one line before you test it. Report a result
that kills a finding as readily as one that confirms it. Anything you cannot test, label BLOCKED
with the exact missing input. Archive to `2026\_archive\` before overwriting anything, and do not
touch `Scripts\` unless a defect requires it. Never file a waiver claim, drop anybody, or write to
ESPN. Reply in section 0.1 form: a numbered list of what changed, then two to five short paragraphs.
Never use em dashes.

---

## B. THE FABLE JOBS

Four, all genuinely expensive, all queued rather than blocked. JOB 3 was added 16 Sept 22:45
after Matt pressed the young-backup claim for the third time; doc 326 is its brief. JOB 4 was
added 17 Sept 00:20 on his keeper-riser claim; doc 329 is its brief. **JOB 3 and JOB 4 are NOT the
same job: 3 is the bench band, ADP 90 to 180, outcome beat-vs-price. 4 is the keeper-eligible band,
ADP 50 plus, outcome next-season VBD14. Different populations (section 0.6). Do not merge them.** Same design as JOB B1 and B2 last
time: one draw reused across every arm, the falsifier fixed before the run, the population restated
in the output.

### JOB 1. ONE CURRENCY FOR THE WHOLE PAGE

**The priority list ranks three lanes in one column and they are not priced on the same scale.**
A certain fill charges an empty slot at ZERO. A bet is an expected value spread over the weeks a hit
lasts. A seat is an inheritance value that only exists if the man ahead goes down. Doc 319 measured
the first of those at roughly five points too high for a tight-end fill, and fixed the SENTENCE.
**The sort was not touched, and the sort is what he acts on.**

**Build the add-minus-drop matrix.** For every free player in the newest `Source\WIRE_*.csv` and
every man on `Source\MY_ROSTER.csv`: the change in weeks 1 to 14 starting-nine points from making
that swap, with every man's weekly availability drawn at the `absence` rates in
`Source\sheet_constants.json`, an empty slot filled at the streamer rate, and ONE draw reused across
every cell so the differences are paired. Then re-sort the priority list on it.

> **TESTABLE FORM, written before the run:** on the live wire, re-pricing all three lanes in one
> currency changes the TOP FIVE of the priority list.
> **FALSIFIER, fixed first:** if the top five, and the top man in each of the three lanes, are the
> same under both arms, the lane mixing costs nothing the page acts on and JOB 1 closes as a null.

Deliverable: the matrix as a CSV, the two orderings side by side, and the largest single row change
in points. Inputs are all on the drive: `Scripts\sheet_engine.py` for `_lineup()` and `season()`,
`Source\MY_ROSTER.csv`, the newest `Source\WIRE_*.csv`, `Source\sheet_constants.json`. Your own
`Scripts\research\b1\b1_absence_bar.py` already has most of the harness.

### JOB 2. THE INHERITOR'S SHARE, NOT HIS NAME

> **AMENDED 17 SEPT 21:45, AFTER JOB 1 CAME BACK AND AFTER DOC 343. READ THIS BOX BEFORE THE
> BRIEF BELOW IT — two of its sentences are now stale and one of its two halves is partly
> pre-empted.**
>
> **1. THE LANE IS NO LONGER FLAT, AND THE BRIEF SAYS IT IS.** Doc 343 shipped a per-man
> P(the job opens), read off the backup's share of his team's week-1 RB carries plus targets:
> **0.476 / 0.438 / 0.533 / 0.636** across bands <20 / 20-30 / 30-40 / 40%+, n=126 team-seasons
> 2022-2025. Permutation at a 35% split, on the seats-only population: **+0.36, p=0.027.**
> `seat.p_opens_by_band` is in `sheet_constants.json` and `inherit_2026.csv` carries `wk1_share`
> and `wk1_band`. **What is STILL flat is the RATE (12.13) and the WEEKS (3.02), and those are
> what JOB 2 should test.**
>
> **2. JOB 1'S CLOSING LINE IS NOW ANSWERED AND THE ANSWER IS "JUST".** Doc 327: *"the seat
> constants (p_opens 0.46, ledger row 2) are still the soft spot and would need to reach about 0.6
> before any seat clears Hockenson."* **The top band measures 0.636.** Carried into JOB 1's own
> currency that is a gross seat of roughly 2.8 against a cheapest drop of 2.7 — **break-even, and
> that is an INFERENCE across two currencies, not a measurement.** Re-running the JOB 1 matrix with
> the per-band odds is the cheap way to settle it and it is now the FIRST thing JOB 2 should do.
>
> **3. THE FALSIFIER'S SECOND HALF IS NARROWED, NOT SATISFIED.** It reads *"if it is flat across
> predicted share too, the seat lane is right to apply one number."* One term is now measured as
> NOT flat, so that sentence can no longer be applied to the lane as a whole. **Test the SCORING
> rate specifically**, and say which of the three terms your answer is about.
>
> **4. NAME THE PREDICTOR, BECAUSE THERE ARE TWO AND THEY ARE NOT INTERCHANGEABLE.** Doc 300's
> measure is the second back's share of TEAM week-1 RB work, **leader IN the denominator**. Doc
> 292's T5 is his share of **NON-LEADER** snaps, leader excluded. On a clean two-man room the
> second is roughly double the first. Doc 343 used doc 300's. **Running T5 as an independent second
> band on the same rows is an open thread of mine and JOB 2 is the right place for it** — if the
> two disagree about a man, neither should be trusted until that is understood.
>
> **5. THE ONE ADDITION WORTH THE COMPUTE, AND IT IS CHEAP: ADD 2021.** Doc 343 tried to make the
> seat bigger by measuring how long the inheritor HOLDS the job and killed its own result: the raw
> gradient is 1.24 / 1.91 / 4.20 / 6.00 weeks, but counted only from the first absence onward it is
> +1.15 at **p=0.081**, and after dropping men who already led the room before any absence, +0.75 at
> **p=0.286**. `[UNDERPOWERED, NOT DISPROVED — n=6 in the top band.]` **2021 is already on JOB 2's
> input list and takes the top band from 22 to about 28.** Reproduce with
> `Scripts\research\wk1\job_opens.py`; its own header carries the testable form.
>
> **6. AND JOB 1 RAISED A QUESTION NOBODY HAS ANSWERED:** whether a seat should be netted against a
> drop at all, when the claim is a stash for a man who is not yet hurt. **[OPEN]** — it is Fable's,
> it is good, and it decides whether "every seat is negative" is even the right sentence.


Doc 320 measured WHO inherits: usage order 72.1% against the chart's 62.2%, and 85.0% against 68.8%
in a settled backfield. **The seat lane on the page does not price who, it prices HOW MUCH**:
`relief_ppg` 12.13 over `weeks_played` 3.02, from n=51, applied flat to every seat. Doc 320's own
open item, in its words: whether the inheritor's SHARE (median 68%) is itself predicted better by
usage than by the chart.

> **TESTABLE FORM:** across 2021 to 2025 backfield absences, the usage order's predicted inheritor
> captures a larger share of the vacated carries plus targets than the chart's does, and the relief
> SCORING rate varies with that predicted share.
> **FALSIFIER, fixed first:** doc 318 already measured the relief rate as flat across lead-back
> quality. If it is flat across predicted share too, then the seat lane is right to apply one number
> and JOB 2 closes as a null on its second half, whatever the first half shows.

Inputs: nflverse `stats_player_week_2021-2025.csv` and `depth_charts_2021-2025.csv` (the first four
weekly files are cached in `Scripts\research\_nflverse_cache\`), `Scripts\depth_map.csv`, and the
`seat` block in `Source\sheet_constants.json`.

### JOB 3. THE YOUNG BACKUP. MATT'S CLAIM, AND IT HAS NEVER BEEN TESTED

**His claim, 16 Sept, in his words: *"Better to take chances on younger talent but i never got any
traction in that during draft strategy... In short, high value backups and rookies are important!!
I don't think we value them correctly here."***

**Read doc 326 first.** It states why this is open rather than closed, corrects section 4.25b's
gloss (that null is about MISPRICING, not decline), and gives the honest count on his mechanism:
doc 141 +8.2 p=0.604 leaning his way, section 4.27's "younger than the starter" +10.8 pp p=0.079
leaning his way, and doc 251's first-round receiver result at 60.0% against 3.3%, p=0.000001, which
is the same claim confirmed at another position. **Three cuts lean his way and the only properly
powered one confirms him. Nobody has run the running-back version.**

> **TESTABLE FORM, written before the run.**
> POPULATION: running backs with a section 1.1 preseason price, ADP 90 to 180, seasons 2021 to 2025,
> who were NOT the highest-projected back on their own team that preseason. State n.
> SPLIT: NFL experience, years 1 to 2 against years 4 and up, matched on price.
> OUTCOMES, BOTH, and report them separately because section 4.13b says they point opposite ways:
> (i) half-PPR weeks 1 to 14 minus what `log(preseason ADP)` predicts, fit within season;
> (ii) **did he reach RB replacement, 9.92 half-PPR a game, at all.**
> MATT PREDICTS: the young man wins both, and by more on (ii).
>
> **FALSIFIER, FIXED FIRST.** If the young cohort is at or below the veteran cohort on (ii) with a
> CI excluding a 5-point gap, his claim is dead at running back and doc 326 says so in its own
> section 1. If the CI spans it, this is UNDERPOWERED and you say what n would resolve it, per
> section 4.24(b). **Do not report an underpowered null as a refutation. That error is what the
> v8.7 retraction of the F4 mechanism line was about.**

**THEN THE SECOND ARM, WHICH IS THE ONE I EXPECT TO CARRY IT.** Doc 251's lesson was that youth
alone was null and **youth plus draft capital** was a factor of eighteen. So re-split the same
population on **NFL draft round 1 to 3 against round 4 and later**, and on the interaction with the
starter ahead of him being fragile (missed a game the prior season, section 4.27's gate 1 before
doc 276 removed it). Report the interaction's DIRECTION and do not assume it: section 0.5(a3) says
running backs substituted and receivers compounded, on the same project.

**AND ONE INSPECTION, WHICH NEEDS NO SIMULATION AND IS ALREADY DONE IN DOC 326 SECTION 5.** The
draft spine `Source\code_universe_v5.csv` carries no age, no NFL round, no NFL year and no depth
position, and sorts on `vbd`. Section 4.28 v8.9 ordered the draft-capital column onto the board for
receivers and it was never added, never extended to backs, and never made part of the sort. **If the
first arm confirms anything at all, say what the column would have to be worth to justify entering
the sort, against the risk that a board tilt on an underpowered coefficient is exactly what
section 4.23(a) refused to do for the RB-WR calibration.**

Inputs: `Source\adp_registry\` through `code_adp_guard.load_preseason_adp`, nflverse
`stats_player_week_2021-2025.csv` (four seasons cached in `Scripts\research\_nflverse_cache\`),
`Source\nfl_draft_picks.csv` for round and pick, `Source\draft_history_2021_2025.csv`, and
`Scripts\research\build_pedigree.py` for the join pattern already in use.

**NEVER use a historical `espn_adp` as a market. Section 1.1, and it is the single most expensive
mistake available in this dataset.**

### JOB 4. THE RISER AS A KEEPER. THE WORD "ASCENDING" IS IN THE DOCTRINE WITH NOTHING BEHIND IT   (RUN, doc 382, 22 Sept: measured Matt's way; inside rounds 5 to 8 the riser carries +52 VBD14 net of price and price carries nothing; round 9+ stays a dart; directive v9.10, §4.34)

**Matt, 16 Sept: *"the model steered me to players who don't have that upside potential as keeper
candidates because they are not risers. That value was never measured."* He is right about the
second sentence and doc 329 confirms the first by inspection of his own roster.**

**THE INSTRUMENT PROBLEM, ALREADY ESTABLISHED, DO NOT RE-DERIVE IT.** Three numbered rules govern
who becomes a keeper audition and every one of them is a PRICE or a ROUND:
- section 6: concentrate auditions in rounds 5 to 8.
- section 4.26(a): among eligible candidates prefer the one drafted CLOSEST to round 5.
- section 4.18b: a round-9-or-later keep returned minus 2.5, so the late picks are darts not
  auditions.
Against those, section 6's *"prefer the plausible 2027 role, young, ascending, secure"* is one
bullet with no number. **A tiebreak with no number loses to three rules with numbers, every time,
and that is the whole of the steering he is describing.** On his own 2026 roster it produced an
audition band of Hurts, LaPorta, Dowdle and Dobbins, two of them sixth-year backs, while the two
players on his roster whose roles are actually expanding sit in rounds 10 and 11 where section 6
demotes them to darts.

> **TESTABLE FORM, written before the run.**
> POPULATION: player-seasons 2021 to 2024, QB RB WR TE, carrying a section 1.1 preseason ADP of 50
> or higher in season N (that is the keeper-eligible band: round 5 or later, per section 2.1a) AND
> priced again in season N+1. State n per position and pooled.
> PREDICTOR, the riser variable, and it must be knowable in August when the keeper is declared, so
> it is computed from the season that just ENDED, not from next season: his share of team
> opportunity (carries plus targets at RB, targets at WR and TE, attempts at QB) in weeks 10 to 14
> MINUS the same share in weeks 1 to 5. Report a second variant on year N against year N-1 share.
> CONTROL: log(preseason ADP) in season N. **This is mandatory, not optional.** Section 4.26(a)
> already measured that price predicts repeating, so an uncontrolled riser test re-finds the price
> effect and calls it trajectory.
> OUTCOMES, BOTH, reported separately: (i) season N+1 VBD14 on section 4.18b's baseline, weeks 1 to
> 14 minus the same season's RB30 / WR30 / QB12 / TE12; (ii) whether he was startable at all in
> N+1, the section 4.13b absolute bar.
> MATT PREDICTS: at equal price, the riser beats the flat or declining player on both.
>
> **FALSIFIER, FIXED FIRST, AND IT CUTS BOTH WAYS SO THE RUN IS WORTH IT EITHER WAY.**
> If trajectory adds nothing over price with a CI excluding a 10-point VBD14 gap, then section 6's
> "ascending" bullet is not a tiebreak, it is noise, and it should be STRUCK from the doctrine so it
> stops competing with section 4.26(a). If trajectory carries 10 points or more net of price, then
> section 4.26(a)'s "prefer the one closest to round 5" is the wrong instruction for this league and
> the audition band has to be re-cut. **If the CI spans both, say what n would resolve it; do not
> report an underpowered null as a refutation (section 4.24b).**

**THE SECOND ARM, AND IT IS THE ONE THAT DECIDES A BENCH SPOT TODAY.** Split the same population by
whether the riser is also YOUNG (three years or less of NFL experience). Doc 251 found youth alone
null and youth-plus-draft-capital a factor of eighteen at receiver; section 4.30's composite reaches
39.4% on young non-startable receivers. **So test trajectory, youth, and their interaction, and say
which of substitution or amplification the number showed (section 0.5a3). Do not assume the
direction.**

**A WARNING ABOUT THE OUTCOME, because this is where it will go wrong.** Section 4.18b measured that
a late hit *"regresses THROUGH replacement: a late hit is, on average, a role that existed for one
year."* That population was defined by PRICE (ADP 97 or later), so it pools a one-year fluke role
with a genuine role expansion. **Separating those two is the entire point of this job. If you end up
re-measuring section 4.18b you have measured the wrong object.**

Inputs: `Source\adp_registry\` through `code_adp_guard.load_preseason_adp`, nflverse
`stats_player_week_2021-2025.csv` (four seasons cached in `Scripts\research\_nflverse_cache\`),
`Source\nfl_draft_picks.csv`, `Source\draft_history_2021_2025.csv` for what this league actually
kept, and `Scripts\research\build_pedigree.py` for the join pattern.

**NEVER use a historical `espn_adp` as a market. Section 1.1.**

### NOT A FABLE JOB, so nobody picks it up twice

**Catalog B4, doc 276's fragility null, is under re-check** because its population held only backs
who were healthy through week 4. That is a re-run of an existing script and it is mine, not a paired
simulation. Same for pinning `redteam_controls.py` in `check_kit.py`, which needs a third folder
group in the manifest and has to be tested against Matt's own tree before it ships.

---

## C. THE PAGE AND TAKE JOBS, ADDED 19 SEPT. NAMED, NEVER NUMBERED.

> **THESE FOUR HAVE NO NUMBER ON PURPOSE, AND THE REASON IS IN THE LEDGER.** Section B's jobs are
> `JOB 1` to `JOB 4`. The handover kits shipped as `JOB 4`, `JOB 5` and `JOB 6` in a different file
> (`FABLE_HANDOVER_TEST.md` says "FABLE JOB 6" on its first line and "replaces the JOB 5 kit"), so
> **`JOB 4` already names two different jobs**, and the ledger's standing note is *"the next kit
> should not be called JOB n."* Numbering these 5 to 8 would have recreated that collision on its
> third file. **Each job below is named by its subject. Cite them by name. Do not renumber them.**

> **STATUS OF SECTION B, CHECKED 19 SEPT 12:30 ET, because two of its four are easy to mark done
> by mistake.**
> - **JOB 1, one currency:** DONE. Doc 327.
> - **JOB 2, the inheritor's share:** partly pre-empted by doc 343's per-band odds. Its amendment
>   box is current. Not confirmed run in this session.
> - **JOB 3, the young backup:** RUN. `FABLE_JOB3_seat_lane.md`, results in doc 352, ledger rows
>   114 and 115. **Task B closed DEAD on its own kill condition** — the odds-times-rate product did
>   not beat the odds alone.
> - **JOB 4, the riser as a keeper: RUN, doc 382, 22 Sept 00:20 ET** (it was WRITTEN AND UNRUN from 17 to 21 Sept,
>   and doc 357's kit that carried its name was a different job). Directive v9.10 and §4.34 carry the rule.

The four below come out of doc 374's catalog and one addition. **Doc 374 listed eight batches and
implied all eight append here. Four of them do not belong to Fable at all** — they end in a guard
committed to the drive, which is my work under section 0.4, not a brief that returns a document.
Those four are named at the bottom of this section so nobody picks them up twice.

**THE STANDING CONSTRAINT ON EVERY JOB IN THIS SECTION, and it is the one this project keeps
breaking: a batch is not finished when the defect is described. It is finished when something
refuses to build.** A job whose whole output is a document has not finished; it has produced the
brief for the thing that finishes it, and it must say so in its own last line.

**RUN THE TAKE CONTRACT FIRST. RUN THE DIRECTIVE LAST, AND NOT ON THE MODEL THAT WROTE IT.**

> **STATUS, 19 Sept 18:35 ET: THE TAKE CONTRACT has RUN (Fable, doc 378, `Source\take_contract_scores.csv`,
> ledger rows 151 to 153). Its single-part claim died; the count of missing parts predicts a correction
> (44% vs 21%, p=0.002). Part 4 was amended (the roster after the move) and the contract shipped as §0.1(h)
> in directive v9.9. WHICH INSTRUMENT GOVERNS A TWO-SIGNAL PLAYER has also RUN (Fable, doc 379, 20:20
> ET): a labelling failure, not a measurement conflict; the sheet's sentence now carries the group.
> THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT YESTERDAY has RUN (Fable, doc 380, 21 Sept 19:05 ET):
> twelve sources, nine dated; the change is built and shipped (read time and run label on every
> pull-built page, the inputs box on the sheet, the on-open age line, `check_pages.py` C5 as the guard).
> One job remains queued, the directive read, and it cannot run on Fable, which wrote v9.9's block.**

---

### JOB: THE TAKE CONTRACT   (RUN, doc 378)

**This is the one Matt asked for.** 19 Sept: *"The lack of consistency for player takes has been an
ongoing issue and we need it scoped fully so all potential issues are nipped in the bud."*

**FOUR PLAYER TAKES WERE WRONG IN TWENTY-FOUR HOURS AND NO TWO FAILED THE SAME WAY.** That is the
finding, and it is why "be more careful" is not a fix:

| the take | what it got wrong |
|---|---|
| drop Demercado for a kicker | roster shape. it left him with two kickers, and kickers are excluded from keeper eligibility entirely |
| cancel the Coleman claim | half of section 6's own bench-RB rule. the job was priced, the fragility of the man ahead was not |
| Schultz at 11.1 | a population base rate quoted as a player forecast. the same 11.1 prints beside Mayer |
| Vele at 5.8 | vintage. a preseason projection quoted for a man who had already scored 16.4 |

**THE CONTRACT, five parts. Each one is the part that a different take skipped.**
1. **VINTAGE.** Which number, and is it a preseason projection or something this season measured.
2. **POPULATION.** If the number is a rate over a group, its population and its n, printed beside it.
3. **THE MAN AHEAD.** For any back, and for any seat, the fragility of the incumbent — checked, or
   explicitly recorded as not available. Never silently absent.
4. **THE STANDING RULE.** Which of Matt's own rules the take touches, quoted rather than
   paraphrased. Roster caps, keeper eligibility, the no-Henry rule, never three QBs.
5. **THE COUNTERFACTUAL.** What is given up, priced in the same currency as what is gained.

> **TESTABLE FORM, WRITTEN BEFORE THE RUN.** POPULATION: every player take that reached a doc in
> `G:\My Drive\_Fantasy\2026\Source\` or a line in `Source\matt_todo.txt` between 1 and 19 September
> 2026. A take is a named player plus a recommended action (claim, drop, start, sit, hold, trade).
> State n. OUTCOME: whether that take was later corrected, reversed or retracted in a subsequent doc.
> CLAIM: takes missing one or more of the five parts were corrected at a higher rate than takes
> carrying all five, and **one part's absence predicts correction better than the others.**
>
> **FALSIFIER, FIXED FIRST.** If the four takes in the table above each score five-of-five when the
> contract is applied mechanically, then the contract is not the instrument, the misses have another
> cause, and this job closes by naming what that cause is instead. **Say that plainly rather than
> loosening the contract until it fits.**

**THE POPULATION HAS A HOLE AND IT MUST BE NAMED IN THE OUTPUT (section 0.6).** A take made in a
chat reply and never written into a doc or the to-do file is **not in this population and cannot
be**. That is section 0.5(e)'s tracker defect one level up: the doc scan can only see what somebody
wrote down. Report how many of the four table rows above were recoverable from files alone, because
that number is the honest ceiling on every count in this job.

**DELIVERABLE, and the document is not the end of it.** (a) A CSV, one row per take, five columns
scored PASS / FAIL / NOT-APPLICABLE, plus the correction outcome. (b) The per-part failure count and
the one part whose absence best predicts a later correction, with its n. (c) **The contract written
as a block short enough to sit in section 0.1**, worded so a session checks itself before sending
rather than after. (d) The last line names what would have to REFUSE TO BUILD for this to be
finished, and who owns building it.

**INPUTS.** `Source\` docs 340 to 375 at minimum, `Source\matt_todo.txt`, `Source\AUDIT_LEDGER.md`
for takes already recorded as corrected, and docs 368, 370, 371 and 373, which are the four table
rows written up. **Do not re-litigate those four.** They are the labelled training rows; the job is
the other n.

---

### JOB: WHICH INSTRUMENT GOVERNS A TWO-SIGNAL PLAYER   (RUN, doc 379: the falsifier was the result, two populations, a label not a measurement; the page string is fixed)

**The week sheet's screen prints 38% for a man clearing two of three workload marks. Section 4.30
measures 7.1% for two of three. That is a factor of five, it has been live on a page Matt reads,
and on 19 September it decided a recommendation** — Schultz and Mayer are both two-of-three, and
the choice between them was argued from one of those two numbers without naming which.

> **TESTABLE FORM, WRITTEN BEFORE THE RUN.** POPULATION: section 4.30's, restated in full in your
> output rather than inherited (section 0.6 rule 1). OUTCOME: reaching the startable bar, defined as
> section 4.13b's absolute bar, stated explicitly. CLAIM: the two-of-three rate has a confidence
> interval that excludes at least one of 38% and 7.1%.
>
> **FALSIFIER, FIXED FIRST, AND IT IS THE LIKELIEST RESULT SO TEST IT BEFORE THE REST.** If the two
> numbers are measured on **different populations** and each is correct for its own, then there is
> no arithmetic conflict at all and the defect is that the page prints one of them **without naming
> which population it came from**. That outcome is a labelling fix, not a measurement, and it must
> be reported as such rather than dressed as a finding. **Check this first. Do not build a
> measurement on top of a conflict that does not exist.**

**AND SAY WHICH DIRECTION THE SIGNALS MOVED (section 0.5a3).** Doc 191 measured substitution at
running back, doc 248 measured amplification at receiver, and both are real. **Do not assume the
direction; report which one this population showed.**

**INPUTS.** Doc 248 and section 4.30 in `Source\DIRECTIVE_FINDINGS.md`, the screen code in
`Scripts\sheet_engine.py` that prints the 38%, `Source\form_2026.csv`, and whatever doc 248's
population was originally built from.

**DELIVERABLE.** The two populations side by side with their n. The interval. One sentence saying
whether this was a measurement conflict or a labelling failure. And the exact string the page should
print instead.

---

### JOB: THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT YESTERDAY   (RUN, doc 380: the practice is published; three of seven forms built, one half built, two differ on purpose, two nulls kept as nulls; C5 guards it)

**Section 0.5(c)6, and it is the cheapest batch in any catalog with the best record here.** The
receiver composite came off a 2020 article, the handover rewrite came off two named authors, and the
`target="_blank"` reversal came off WCAG 2.2 SC 3.2.5 — where Matt's instinct turned out to match
the published standard and my change had differed from it **by accident**, which is the whole reason
this batch exists.

**THE QUESTION.** People build decision pages on top of scheduled data pulls for a living. **What is
the published practice for a page that is not wrong, but is answering a question about yesterday?**
Freshness stamps, staleness thresholds, refusing to render, degrading a number to a range, showing
the pull time against the decision deadline. Who publishes it, and **what is the date on it (B7)**.

**THEN SAY WHERE WE DIFFER, AND WHETHER ON PURPOSE.** Differing deliberately is an answer. Differing
by accident is a defect. The live case is the Saturday claim that settled while every file on the
drive still described Friday's roster: **no page was wrong, and that is worse, because nothing
looked broken.**

> **TESTABLE FORM.** There is at least one dated, published practice for communicating input
> freshness on a decision page that this project does not implement.
> **FALSIFIER.** *"Nobody publishes this"* is a legitimate result and section 4.31 is the precedent
> for reporting it as one. Do not manufacture a source to avoid a null.

**DELIVERABLE.** Each practice with its publisher and date, our current behaviour beside it, and
**one row marked as the change to make**, specific enough to be built.

---

### JOB: THE DIRECTIVE, READ BY SOMEONE WITH NO STAKE IN IT

**RUN THIS LAST, AND NOT ON THE MODEL THAT WROTE IT.** A file cannot audit whether it is being read
past, and the session that has been reading it all night is the worst available judge of that.

**THE SITUATION.** v9.8 split the directive four ways by read cadence, on the measurement in ledger
row 149: the resident set had reached about 42,000 tokens a turn and roughly two thirds of it was
either a draft that ended on 7 September or the story of how a rule came to exist. **The split was
proved by line multiset, not asserted.** That work is done and is not the target here.

**THE QUESTION THE SPLIT DID NOT ANSWER: is the resident file load-bearing, or is it read past?**
On 18 and 19 September it did not stop four errors of one kind, **and the rules that should have
stopped every one of them were in the resident set at the time.**

> **TESTABLE FORM, WRITTEN BEFORE THE RUN.** For each of the four takes in the take-contract table,
> name the rule in the resident set that should have stopped it, and classify it as exactly one of:
> **(a) ABSENT** — no rule covers this; **(b) PRESENT BUT NOT APPLICABLE** — a rule is near it and
> does not reach it; **(c) PRESENT, APPLICABLE, NOT APPLIED.**
> **If most land in (c), the file is being read past and more text is not the fix.**
> **FALSIFIER, AND IT POINTS THE OPPOSITE WAY, WHICH IS WHY THE JOB IS WORTH RUNNING.** If most land
> in (a), the file is incomplete, more text IS the fix, and that must be said plainly rather than
> bent toward the more fashionable conclusion.

**TWO CONSTRAINTS, BOTH HARD.**
1. **This is not a licence to propose a rewrite.** Every prose map in this project went stale within
   hours (section 9), and the proof standard for any further move is the defrag's: the line multiset
   identical before and after, **measured, never asserted** (docs 351 and 367).
2. **Report in section 0.5(a4)'s three answers.** TESTED, NOT YET RUN with the testable form written
   down, or BLOCKED naming the exact missing input. *"That isn't measurable"* is not one of them.

**INPUTS.** `00_PROJECT_DIRECTIVE.md` v9.8 and its three companions, docs 368, 370, 371 and 373 for
the four errors, `AUDIT_LEDGER.md`, and `Source\METHOD_TRAPS.md`.

---

### NOT FABLE'S. MINE, AND HERE SO NOBODY PICKS THEM UP TWICE.

Doc 374's catalog has eight batches. **Four of them end in a guard committed to Matt's drive and
pinned in `check_kit.py`, which is section 0.4 work and does not fit a brief-and-return-a-document
shape.** Handing them to Fable would be asking somebody else to do my job.

| doc 374 batch | state, 19 Sept |
|---|---|
| **A** the page tells you what a number is | **MINE, NOT STARTED.** `check_vintage.py` reports; it does not correct. The sheet still prints 5.8 for Vele and a 0.0 drop cost. **Doc 375 widened this: `half_ppr` scores neither passing nor kicking, so every consumer that differences it against a league-scored projection carries the same defect — `sheet_engine`, `wire` and `lineup` all read that file.** A's real scope is now "one league-scored column in `build_form`", which fixes every consumer at once |
| **B** a base rate may not wear a player's name | **MINE, NOT STARTED.** Depends on the two-signal job above resolving whether this is a measurement or a label |
| **C** the generated-page linter | **MINE. SHIPPED 19 Sept** as `Scripts\check_pages.py`, wired into `ff.bat`, negative controls run first |
| **E** every hand-written constant that reaches a page | **MINE, NOT STARTED.** `STATIC_TOP`, `STATIC_BOTTOM`, the standing-rules block. Doc 372 found two false assertions in `STATIC_TOP` alone |
| **F** the trackers | **MINE, NOT STARTED.** `open_threads.py` scrapes its own output, 21 nested rows. The to-do list records asks and never completions |
