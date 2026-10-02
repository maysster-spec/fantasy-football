# 455. THE RED-TEAM CATALOG, AND THE CROWD CHECK NONE OF THE GUARDS COULD SEE

*30 Sept 2026, 10:40 ET. Claude (Cowork). Matt, 30 Sept: "1. Chris Bell is still not a priority add. 2. directive is
updated. 3. based on pattern of errors such as signals that were not written such as rookie pedigree, do we have adequate
guards in place now? ... 5. If you were to red team this project, and in addition consider other potential gaps, and
strategies to add value, what do you recommend?" 455 reserved by listing `Source\` (454 is the pull cadence). No em dashes.*

---

## 0. WHAT TO DO

1. **Tonight, two claims, not three: Ollie Gordon II first, drop Devaughn Vele; Michael Mayer second, drop Samaje Perine.**
   Bell is off the list (your call). The sheet's third row, Kalif Raymond for J.K. Dobbins at +4.8 net, is a WR ticket paid
   for with an RB starter because the page may not pair a drop at the add's own position; that is inside the noise and against
   the bench rule (RB to the cap), so skip it. **Keep the third seat for Sunday: Nacua is questionable with a return date of
   this Sunday and Dowdle of Thursday; if either is active you need an active seat to start him, and the man to cut then is
   Malik Washington (the next-cheapest, 0.1).** Vele over Malik Washington for Gordon is 0.2 points on the sheet, a coin flip;
   the sheet's pairing stands.
2. **No, the guards were not adequate against the class you named, and they still are not the whole answer.** Every guard on
   file checks that a thing on the page agrees with a rule or another file. None can see a thing that should be on the page
   and is not. The three misses of the last three days (Gordon, Bell, Miller under the cut) were found by your eye, your eye
   and one guard; the guards found the third only because doc 451 wrote it the night before. Section 1 is the scorecard,
   with the mutation harness's honest count: of ten known defects, one caught, four uncaught, five that the harness cannot
   test on today's roster at all.
3. **Built today, the one thing that catches the class at its source: the crowd table.** ESPN's +/- (the most-added column
   you asked for on 23 Sept, doc 395) has been written to every wire file since and printed nowhere. The week sheet now
   prints the ten most-added free men with this page's answer beside each name (THE CALL row, a pick, an open job, a seat,
   a rate against your bar, or "not priced" with the reason), and P4 in `check_page_logic.py` fails the run if any of the ten
   has no answer. On today's inputs it names Jaylen Wright, the third most-added man in ESPN and on no page of ours: he holds
   the Miami seat the chart still gives him, at 4.4 a week. That is the analysts' list, mechanically, every run, on the day
   it matters (the column moves on Wednesday after other leagues' waivers run; it read near zero on Monday and Tuesday).
4. **Also fixed today: the open job under the cut.** P3 fired on its first live run (Kendre Miller, priced at 2.3 for the one
   week Etienne is out, cut by the five-row cap and named nowhere); DeeJay Dallas at 6.9 was cut the same way and the guard
   missed him because his name sat in the seat lane's left-off line. The sheet now names every open job below the cut with
   its price; P3 reads the decision band only. The wire's "job, worth 261" for Miami was the August board's number beside a
   sheet pricing the same job at 104; it now says "on the August board".
5. **The catalog is section 2, in the order I would work it. The next batch is A3, the run-to-run decision diff (what changed
   on THE CALL since the last build, by name), then A2, the blank-by-population check.** Say the word and I re-order.
   One thing to run: `.\ff.bat` once tonight before the claims, so the crowd table, the open jobs under the cut and the
   two-claim CALL are on the sheet you read (the 07:30 run does it otherwise). RESULT must show logic 0 and kit 0.

---

## 1. ARE THE GUARDS ADEQUATE? THE SCORECARD

**The claim in testable form:** the guards on file would have fired on the three misses of 28 to 30 Sept before Matt saw
them. **Result: 0 of 3.** Gordon (open job on no page): no guard, Matt found it, doc 451 wrote P3 afterwards. Bell (a rookie
the preseason screen could not read): no guard, Matt found it, doc 453 built the in-season screen. The stale projection (six
days old the night before claims): found while chasing Gordon, not by a guard; the inputs box printed the age and nothing
failed on it. Miller under the cut on 30 Sept: P3 fired, one day old.

**What the guards are.** `check_kit` (the files are the pinned files), `check_pages` (every placeholder substituted, links
resolve, the first CALL row prints its vintage), `check_plain` (no doc voice), `check_vintage` (every rate is the blend the
page says), `check_page_rules` (the rules a page states are the live ones), `check_page_logic` (no parked man as a drop; every
open job named; from today, every most-added man answered), `check_inputs` (every decision input file is read),
`check_locals`, `check_citations`, and `check_guards` (ten known defects mutated into the engine). Every one of these is an
internal-consistency check: a thing that exists is compared with a rule or another file. The class you named is absence: a
signal, a man or a freshness that should be on the page and is not. An absence check needs an enumerated list of what must
exist, and the list is the cost; the three shipped today are P3 (the wire's open jobs), P4 (ESPN's most-added) and C6 (the
CALL row's three required inputs), and each covers exactly its list.

**The mutation harness, re-read honestly.** Doc 451 reported seven blind spots. Today's run reads: caught 1 (the blend
switched off), uncaught 4 (the divisor back to 17; a weekly position priced on a season rate; an add paired with a drop at
its own position; a negative drop cost inflating the net), and **no effect 5**: the two parked-man mutations, the losing move,
the emptied slot and the man replacing himself leave today's page byte-identical, because the roster has no man in the state
the mutation breaks. The harness printed those as SURVIVED, which said "no guard covers it" about defects it had not put on
the page. It now says NO EFFECT and lists them. What it proves changes with the roster every day; a fixed fixture roster
(A5) is what makes it prove the same thing every day.

**The limit that no guard removes.** A guard cannot find a signal nobody has measured; 4.43 was that (the screen had never been
read on three weeks). That is the outside check's job (0.5(c)6) and yours, and the record says your eye is the best detector
this project has: three of the last three. The crowd table is that comparison made mechanical for the one consensus that is
free and daily; the podcast and analyst reads remain yours to supply.

## 2. THE CATALOG, IN WORKING ORDER

Each item carries one of 0.5(a4)'s three answers. "Changes a decision" means a claim, a drop or a start this season.

**A. Absence guards (the class you asked about).**
- **A1 DONE today: the crowd table and P4.** Changes what you read tonight (Wright).
- **A2 Blank by population.** For every screen or term the page prices on, the share of the decision set (free skill men on
  the wire, the doubt lane, the seat lane) with a blank value, named by subgroup. Bell's shape: the pedigree screen blank for
  every rookie receiver. NOT YET RUN; a script over the wire CSV, one evening. Changes a decision only when it finds one.
- **A3 The decision diff.** THE CALL, the picks and the open-job lines diffed against the previous build: names in, names out,
  moves over two points, printed to the log and on the page ("since 07:30: Raymond in, Bell out"). NOT YET RUN; cheap. Makes
  every disappearance visible the day it happens, which is what Miller's needed.
- **A4 Freshness for every input.** `STALE_DAYS` covers the projection and the form file; news, snaps, lines, depth, rosters
  and the constants only print their age. A guard that fails on any input older than its cadence. NOT YET RUN.
- **A5 A fixture roster for the harness.** A synthetic fifteen with one parked cheap man, two defenses, one kicker, a same-
  position pair, so all ten mutations bite every day. NOT YET RUN; half a day.
- **A6 The four real blind spots.** A `check_call.py` that re-derives each CALL row from the page's own numbers: net = worth
  minus max(0, cost), no drop at the add's position, a defense or kicker row printing a weekly rate, one printed rate
  recomputed from the projection CSV over the weeks left. NOT YET RUN. These are the engine's own rules, so the check is
  mechanical.

**B. The pricing engine (would change a decision).**
- **B1 One relief rate for every open job.** THE CALL prices Gordon on Achane's job and Badie on Coleman's at the same 12.1 a
  game. Doc 411 measured that nothing about the BACKUP predicts his relief scoring (62 absences); it did not test whether the
  JOB does. Testable form: on relief stretches 2021 to 2025 (nflverse), the relief man's points a game against the absent
  starter's prior points a game; if the slope is real, 4.20's "buy the job" belongs in the open-job price and not only in the
  seat lane's sort. NOT YET RUN; one script on the cache. Changes the order of open jobs from the second one on.
- **B2 The return date is an editorial guess.** Weeks open come from `news_2026.csv`'s return date (Etienne 11 Oct, Coleman
  25 Oct). Its accuracy against the first game actually played is unmeasured. NOT YET RUN, dated: status pairs from about 20
  Oct.
- **B3 The same-position rule turns a WR add into an RB cut** (Raymond for Dobbins tonight). Doc 417's rule is right for the
  arithmetic; the row should say when it crosses the bench rule (0.5(b): surface the preference at the moment it binds).
  NOT YET RUN; a sentence on the row.
- **B4 The seat lane's holder when ESPN blanks the absent man.** Achane is projected at nothing now, so the stand-in rule of
  doc 453 cannot fire and Wright is the holder at 103.5 with Gordon "below the cap"; usage says the reverse (20 touches to 2).
  The chain should read the men doing the job when the pull blanks the starter. NOT YET RUN; THE CALL is unaffected, the
  seat lane's Miami row is wrong.
- **B5 Caps by count.** Five picks and ten seats, cut by count; a 6.9 was cut and a 4.0 shown (re-admitted for "put him
  first"). A cut by value (everything above the cheapest drop plus two) would be more honest. Judgement call, low.

**C. Inputs.**
- **C1 DONE today:** the wire's job worth says its vintage.
- **C2 The IR return needs a seat.** No page says "if Nacua is active Sunday you need an active seat, and the man to cut is X".
  A Sunday-morning line on the lineup check, from the IR view and the drop ladder. NOT YET RUN; changes what you do Sunday.
- **C3 The +/- column's cadence.** Read near zero Monday and Tuesday, 48 on Wednesday, this week. Log it each run for three
  weeks and say on which day it moves. NOT YET RUN, dated.

**D. Value beyond guards.**
- **D1 Rival claims from the rosters on file.** The contest rate (56% for Gordon) is a group rate. The seven teams above you
  in priority are on `LEAGUE_ROSTERS.csv` with their positions and bench seats; a claim-competition line ("four of the seven
  above you have an RB seat open") is buildable tonight. Validation is BLOCKED: rosters at past claim times are not held, so
  the line can be built but not measured until it has run for a month.
- **D2 The playoff draw.** 4.33 and 4.26(b): the D/ST schedule and the TE weeks 15 to 17 draw are the one schedule effect. A
  page term from week 10. Dated.
- **D3 The trade lane.** No trade page exists; three trades a season league-wide (behavioural). Surplus at RB after Gordon
  against a week-6 TE hole. Judgement call, low until a partner shows.
- **D4 The weekly high score** ($10 a week, $140 a season, a tenth of the pot). No page chases it. Low.

**E. Process.**
- **E1 The outside check, dated (0.5(c)6).** Standard practice in data pipelines is a declared set of tests per source and
  model: not-null, unique, accepted values, referential relationships, and source freshness against a stated cadence (dbt's
  documented data tests and source-freshness reference, docs.getdbt.com, read 30 Sept 2026), with null rate by segment and
  change-since-last-run alerts on top in the observability tools. We hold schema (the pins), relationships (id joins,
  `check_inputs`) and one freshness rule; we differ by accident, not on purpose, on null rate by segment (A2), freshness per
  source (A4) and change detection (A3). That is the whole of the class you named, and it is three scripts.
- **E2 The store.** 336 docs before this one; the milestone table says check `knowledge_size` after any session writing more
  than five docs. This session writes its fifth. Checked at the push below.

## 3. WHAT CHANGED IN THE BUILDERS TODAY

`sheet_engine.py`: open-job moves carry `open_job` and `oj_short`; a move worth 0.05 or less is named in the not-priced line;
after the five-row cut, every open job below it prints with its price and weeks; `crowd_table()` and the `crowd` parameter on
`write()` and `render()`; two CSS lines. `wire.py`: the crowd list (every wire row and every off-board row with ESPN's +/-)
passed to the sheet; `flags()` prints "on the August board" after a job's worth. `check_page_logic.py`: P3 reads band 0 only
(id="s0" to id="byes") and fails outright without the anchors; P4 with `most_added()` and `crowd_on_sheet()`; 29 controls,
including the 30 Sept case in each direction (a name only in the seat lane fires; a name only in the crowd table is quiet).
Both fired on this morning's live page (Miller and Dallas for P3; the whole table missing for P4) and are quiet on the
rebuilt one. `check_guards.py`: NO EFFECT for a mutation that leaves the page byte-identical (the build stamp and the footer
stripped before comparing); its render passes the crowd list. `check_kit.py`: the four re-pinned. `check_plain`, `check_vintage`,
`check_page_rules`, `check_inputs`, `check_locals` quiet on the rebuilt pages. The seven sandbox-only `check_pages` problems are
the commands page, which only ff.bat builds.

## 4. THE TAKE: TWO CLAIMS TONIGHT

- **Vintage.** Gordon: 2026, 2 games, 6.8 a game, 20 carries and targets last game, ESPN's rest-of-season projection moved from
  22.8 to 142.3 in today's pull; priced at 8.7 a week on the blend. Mayer: 2026, 3 games, 6.9 a game.
- **Population.** Gordon's 27.8 is the seat constant's relief rate (12.1 a game while a job is open, a group rate, not his
  forecast) against your bar over ten weeks. Mayer's 11.4 is the week-1 workload screen's 38% (a screen, not his forecast).
- **The man ahead.** Gordon: De'Von Achane, injury reserve, back not this season; Jaylen Wright questionable, 2 touches in 2
  games. Mayer: Brock Bowers holds the job, active, rostered by WGTS, 13 targets last game; Mayer is the second tight end on
  81 to 87% of the snaps with 7, 4 and 3 targets (2026, 3 games), a week-6 cover and not a starter while Bowers plays.
- **The standing rule and the roster after.** Place Wednesday night; every claim carries its own drop; never a parked man.
  After both: RB Jeanty, Judkins, Dobbins, Washington Jr., Gordon (Coleman and Dowdle parked); WR Adams, Pickens, Tucker,
  Malik Washington (Nacua parked); TE LaPorta, Mayer; QB Hurts; two defenses; one kicker. Fifteen, every cap met. Gordon is
  56% contested and you are 8 of 12: expect to lose him; ranking him first costs nothing.
- **The counterfactual.** Vele at 0.0 (10.2 a game this season, never in your nine); Perine at minus 1.7. The third seat, held
  for Nacua or Dowdle coming off the IR slot, is worth more than Raymond's +4.8 ticket paid with Dobbins.

## 5. OPEN, BY NAME

- **Matt's:** the two claims tonight and `py claim_order_log.py` after; the Thursday pair; the routes purchase; the D/ST box
  score; the Opus chat and the podcast source (he is the blocker, his words).
- **Mine, next:** A3 the decision diff, then A2 blank by population, then B1 the job slope; the directive line for the crowd
  check at the next version (no paste tonight).
- **Mine, on events:** the 07:30 run on 1 Oct (crowd table and P4 on the live build, logic 0); the in-season cell re-fit at
  week 6; ESPN's cadence off the report lines and the +/- column in three weeks; the Tuesday 6 Oct run; status pairs from 20
  Oct; 4.34 from week 10; wiring item 7 (low).
