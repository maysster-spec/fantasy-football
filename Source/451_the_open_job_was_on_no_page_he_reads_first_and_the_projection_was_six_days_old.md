# 451. THE OPEN JOB WAS ON NO PAGE HE READS FIRST, AND THE PROJECTION WAS SIX DAYS OLD

*29 Sept 2026, 22:40 ET. Claude (Cowork). Matt, tonight: Ollie Gordon II and Chris Bell (both Dolphins) are widely
recommended waiver pickups, still free in the league, and neither is on the week sheet; is there a reason, or is a run
pending? Both, and one of the reasons is a defect. 451 reserved by listing `Source\` (no doc has landed since 450).
Population for every 2026 number: `form_2026.csv` and `snaps_2026.csv`, weeks 1 to 3, this league's pull of 21:26 tonight.
No em dashes.*

---

## 0. WHAT TO DO

1. **Wednesday night, claim Ollie Gordon II first, then Michael Mayer. Gordon's drop is Malik Washington (the sheet's
   pairing, a waiver add, no keeper cost) and Mayer's is Samaje Perine (0.0, a waiver add, no keeper cost).** The five
   lines the take contract asks for are in section 1. Gordon is contested (20 touches last game; men like that are
   contested 56% of the time) and you are 8 of 12 this week, so expect to lose him to a team ahead of you: ranking him
   first costs nothing, because a losing claim spends no priority. If he lands, Mayer runs at 12th and is contested
   14% of the time.
2. **Chris Bell: no claim, and his absence is not a defect.** He is 32nd of 104 free receivers on the projection and
   under your receiver bar (10.3) every week on the blend. His week 3 (7 targets, 71% of the snaps, a third of the air
   yards) came with Caleb Douglas out; Douglas is questionable again. Section 2.
3. **The defect, fixed: a job that is already open now reaches THE CALL.** Achane is on injured reserve for the season
   (ACL, 28 Sept, return 15 Feb 2027). The wire put Gordon at the top of its IN DOUBT lane; the week sheet had no home
   for him: the seat list drops an open job by rule (doc 411) and its inherit row paired him with Jaylen Wright, the
   chart's stand-in RB1, at a 7.45 job, so the row fell under the ten-row cap, unnamed. THE CALL now prices an open job
   at the relief rate for the weeks the holder is out, with no odds term. On tonight's pull Gordon is its first row at
   +24.5 over ten weeks. Section 3.
4. **The projection is six days old and the batch file heals it tomorrow.** Today's Tuesday 06:00 task ran `ff.bat` as
   it stood the night before, with no projection step (doc 439 shipped it later that day), so every rate on the page is
   blended on a pull from Thursday 24 Sept, before week 3 was played. `ff.bat` now pulls on any run when the newest pull
   is more than five days old (`proj_due.py`); the 07:30 run tomorrow pulls it and rebuilds the sheet. Nothing to run.
5. **A guard reads for this now:** `check_page_logic.py` P3 fails a run when the wire marks a job as open and the week
   sheet does not name the man. It fires on tonight's shipped pages and is quiet on the fixed ones. Nothing to run.

---

## 1. THE TAKE: OLLIE GORDON II, RB, MIAMI

- **Vintage.** 2026, 3 games. Week 3, in relief: 61 of 73 snaps (84%), 17 carries and 3 targets, 13.0 points against
  14.1 expected. Weeks 1 and 2, as the backup: 4 and 11 snaps, 0.7 points in week 2. ESPN's projection (the 24 Sept
  pull, made before week 3) is a backup's, which is why the sheet prices him at 3.9 a week on the blend.
- **Population.** 12.1 a game is what a backup scores while a job is open, the seat constant (five seasons, a group rate,
  not his forecast); the sheet uses the same figure for every seat it prices. Against your bar over the ten weeks he
  plays (his bye is week 6) that is 24.5 expected. 56% contested is the rate for men with 20 touches the game before, a
  group rate again.
- **The man ahead.** De'Von Achane, injured reserve, ACL, out for the season. Jaylen Wright is the chart's RB1 and is
  questionable (foot); he played 4 and 3 snaps in weeks 1 and 2, did not play in week 3, and missed 8 games in 2025. The job is Gordon's
  to lose, and the room agrees: 20 touches the week the starter went down is 4.27's trigger, production in relief.
- **The standing rule and the roster after.** 4.19 says four of five backs you add never give a startable stretch; that
  is your record on adds in general, and 4.27 is the case it carves out. Buy the job, never the name (4.20): this job is
  open by an injury already done, not by one you are betting on. After Gordon for Malik Washington: five active backs
  (Jeanty, Judkins, Dobbins, Washington Jr., Perine) with Coleman and Dowdle parked, four active receivers with Nacua
  parked; the seven backs you already hold against a limit of six say the parked men do not count. Mayer for Perine
  makes a second tight end, which section 6 allows for the week 6 hole and no longer.
- **The counterfactual.** Malik Washington costs 1.1 on paper: Miami's most-targeted man (27.1% of the targets, 2026, 3
  games) on a 14-point offence, 7.7 a week on the blend, never in your nine. What the claim buys is a lead back on the
  same 14-point offence: the 12.1 is an average across offences, and Miami's implied total at Minnesota this week is 14,
  the lowest of the 32 on the line, so read the 24.5 as the group's number and his week 3 (13.0) as the one measurement of him
  in the job. If Miami splits him with Wright, less. Nothing here is his forecast.

## 2. CHRIS BELL, WR, MIAMI: THE CEILING, NOT THE PRESENT

The question a claim asks is where he tops out (0.5(a6)). The present: week 3, 7 targets, 71% of the snaps, 33% of the
air yards at 18 yards a target, 8.7 points against 11.3 expected; the season, 10 targets and 11.7 points in 3 games. That
week came with Caleb Douglas (26% of the targets in week 1, 13% in week 2) out; Douglas is questionable for week 4. The
ceiling is what Malik Washington (27.1%) and Douglas leave behind on an offence quarterbacked by Malik Willis with a
14-point number this week, in a deep-shot role, the highest-variance kind. On the sheet he is under the bar every week;
4.35 says the best week-before signal lifts a claimable receiver from about 4% to 10% startable; 4.38 says a rise at a
given reading is a caution, not a signal; your own receiver adds work one in eight. The recommendations he is getting are
the same week-3 line read as a trend. If Douglas sits again he keeps the snaps, and the wire's pool ranks him where the
projection puts him. No claim.

## 3. THE DEFECT, WHERE IT LIVED, AND THE FIX

Three files each did their part and the man fell between them. `build_inherit.py` reads the daily chart, which lists
Wright RB1 and Achane RB3, and wrote the Miami row with Wright holding a 7.45 job (its own `why` column says so). The seat
list read that row, ranked it by what the job pays, and cut it under the ten-row cap without a name (doc 345's defect,
the cap eating the row; cap cuts are named now). The wire's `next_man_up()` reads the usage order, saw Achane's status,
set Miami aside as "the job is already open" and `in_doubt()` put Gordon first in that lane, correctly; nothing carried
that lane to the sheet. The free-body table priced him on the blend, a backup's projection and two backup weeks, under
the six men shown.

The fix: `wire.py` hands `sheet_engine.write()` the doubt rows whose holder is out for weeks (`open_jobs`, one predicate,
`GONE_FOR_WEEKS`, both pages), and THE CALL prices each at the relief rate for the weeks the holder is out: the news
feed's return date where there is one (Achane, not this season; Coleman, 25 Oct; Etienne, 11 Oct), else four weeks for
injured reserve (the NFL minimum, a rule) and the seat constant's three for a one-week Out. No odds term: the injury has
happened. A man ESPN projects at nothing cannot be priced and is named under the picks (Kendre Miller, Trevor Etienne
tonight). The wire marks those rows "the job is open, see THE CALL". `take_facts()` prints the man who is out as the man
ahead, so the take contract's line (b) names Achane and not Wright.

Guards: P3 in `check_page_logic.py` (five controls, 22 of 22; it fires on the 21:26 pages and is quiet on the fixed
ones); `check_guards.py`'s working copy now carries the wire page and its render passes the open jobs, so P3 measures a
mutation and not the harness (the same seven blind spots as before, the two parked-man mutations caught); `proj_due.py`
(three controls); the sheet with no open jobs renders line for line as before but for the named cap cuts;
`check_pages` C6, `check_plain`, `check_vintage`, `check_page_rules`, `check_locals` (23 files) all quiet. Every changed
script re-pinned; the wire.py and sheet_engine.py pin comments cut to one clause each (section 9 rule 7).

## 4. OPEN, BY NAME

- **Matt's:** the claims Wednesday night (Gordon first, Mayer second, a drop on each); the v9.36 go (given tonight, applied
  next); the claim-order runs; the routes purchase; the D/ST box score; the Opus chat (blocked).
- **Mine, waiting on events:** the 07:30 run tomorrow (projections 0 for the first time, then wire 0, logic 0, and a
  sheet with Gordon on THE CALL on the new projection); the Tuesday 6 October run; the status pairs from about 20
  October; the 4.34 column from week 10; wiring item 7.
- **Mine, next:** `build_inherit.py` writes the stand-in as the holder when the chart demotes an injured starter (Miami
  and Green Bay tonight); the seat list survives it because an open job is not a seat, but the inherit row is still
  wrong about whose job it is. Low, and named so it is not dropped.
