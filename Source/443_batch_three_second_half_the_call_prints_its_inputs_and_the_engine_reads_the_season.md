# 443. BATCH THREE, SECOND HALF: THE CALL PRINTS THE TAKE CONTRACT, THE ENGINE PRINTS THE SEASON BESIDE THE BLEND, THE WEEKS AHEAD REACH THE SHEET, AND THE STASH LANE STOPS OFFERING A JOB THAT IS ALREADY OPEN

*29 Sept 2026, evening. Claude (Cowork), the second half of batch three of "complete the to do list... in batches to ensure
fidelity" (docs 440, 441 and 442 were the earlier batches). 443 reserved by listing `Source\` at 18:48 ET. No em dashes.*

---

## 0. WHAT TO DO

1. **Every row of THE CALL now prints the take contract's three checkable lines under the name**: what the rate is
   (this season with its games and the price the page used, or `proj` when he is on the projection alone), the man ahead
   for a running back (name, games last season, today's tag, or "not checked"), and one input the project holds (the last
   two games actual and expected, the pregame line for a defense or a quarterback, or "not held"). Tonight's page:
   Michael Mayer, 6.9 this season (3 g) priced at 5.8 a week, last 2: 7.2 actual / 5.3 expected; Tyler Allgeier, 4.6 this
   season (3 g) priced at 6.3, behind Jeremiyah Love with no injury tag today, last 2: 2.9 / 4.1. `check_pages.py` reads
   the first row (rule C6): a warning until 6 October, a failure after. It passes tonight.
2. **The measured rate prints beside the blend everywhere your men are priced**: section 5 and the drop table read
   "16.7 blend · 16.3 this season (3 g)" for Jeanty, and blank, never zero, for a man with no season line. The lineup page
   prints no rate of any vintage, so there was nothing to put beside; the fix went where the blend is.
3. **The five weeks ahead are on the week sheet**, under THE CALL and the bye calendar: who is off, and the best free
   quarterback and defense each week with the number they were ranked on (the line where every game that week has one,
   last season otherwise). It was computed in `wire.py` since week one and reached only the wire page and the console.
4. **The stash lane no longer offers a backup behind a starter who is already out.** Tonight's wire had Ollie Gordon II
   "behind De'Von Achane, job pays 261" with Achane on injured reserve, and the same man in the IN DOUBT lane. Doc 411's
   rule on the week sheet (a seat is an option on a job that is still held) now governs the wire's stash list too, on the
   same predicate, and the teams set aside are named under the table. One rule, both pages.
5. **The seat lane prints the man ahead's record and the next man's best fortnight**: "played 9 of 17 last season · at
   risk: no injury tag today" beside the holder, "best two weeks last season: 13.2 a game" beside the backup. Both were
   in `inherit_2026.csv` and read by nothing. Printed, never sorted on.
6. **The engine's form join is the wire's key** (name, position, team, exact, then the first-name variant on the same team
   and position when it is the only candidate): 182 of 191 skill rows on the page carry a measured rate, up from 181
   (Joshua Palmer), and 330 of 443 priced men on the whole pull join the season, up from 329. The nine still unjoined are
   named in §3 and none joined before.
7. **The last two games print on every row that has them** (19 tonight) with the wire's own flag word carried across
   rather than re-derived, and the inputs box says "snaps through week 3" beside the form file's age.
8. **Four live findings with no page term, one line each (§4)**: 4.13d is a prohibition and stays uncited on purpose;
   4.25b and 4.26(b) were already implemented under other names and are cited where the code is; 4.34 cannot run before
   week 10 and its two missing inputs are named.
9. **The pocket sheet keeps the snapshot practice and says so on the page**: a dated note (27 September), `make_online.py`
   reports its age every run, and `check_pages.py` (rule C7) warns past seven days. No builder, because no script
   produces it and one that pretended to would be an exit code (0.2).
10. **The first `ff.bat` run after docs 440 to 442 is checked**: 18:16 tonight, RESULT with form, snaps, depth, lines,
    inherit, kit, pages and logic all 0, the logic block naming the three parked men, the lines file 272 games, the
    daily chart 574 rows. Two lines close on the list.
11. **Nothing to run.** The next `ff.bat` builds the sheet on this engine. `lookahead_box.py` and `make_online.py` are
    pinned (the second for the first time; it had run daily since doc 430 unpinned).

---

## 1. THE CALL AND THE TAKE CONTRACT

Directive 0.1(h) has required five lines beside every take since doc 378, and doc 433 found the page printing none of
the three that can be checked. `take_facts()` in `sheet_engine.py` builds them from the take's own free row (every move,
sure, bet or seat, now carries its row) and from `inherit_2026.csv` for the man ahead. The man-ahead line prints for a
running back only, as the contract says; a defense or a quarterback prints the pregame line as its held input when
`wire.py` passed one (`opp_total`, `own_total` on the free row, finding 4.39), a receiver or tight end the last two games.
"Not held" and "not checked" are printed words, never a blank, because a blank reads as nothing to say.

`check_pages.py` C6 parses THE CALL's first row for a vintage word, the man ahead (RB only) and a held input; "on the
line" and "implied total" count as held inputs. It fired on the 29 Sept page shape as a warning (W6, until 6 October)
and passes on tonight's render. The selftest counts its controls as they run (28 tonight) rather than by a hand sum,
which went stale the first time a control was added.

## 2. THE SEASON BESIDE THE BLEND, THE SEAT LANE, THE JOIN

`rates()` returns `measured_g`, `act2` and `xfp2` on every priced row; `this_season_text()` and `last_two_text()` print
them, blank when the form row is absent. The flag word (mirage, quiet volume) is read off the wire row's own flag text
when the row has one and applied from the same two cells (8+ actual on under 5 expected, 8+ expected on under 5 actual)
when it has not; `wire.py` now passes `flags` on every free row so the sheet prints what the wire printed.

The seat lane reads `starter_g25`, `at_risk` and `best_2wk_2025` (doc 276's rule holds: last season's games missed does
not predict this season's, so it is printed and never filtered on; the live tag is the separate channel).

The join: `form_lookup()` keys `season_actual` on name, position and team exactly as `wire.py` does, and `_form_variant()`
is one copy of the doc 442 rule. Still unjoined, all skill rows, none of which joined before: Sean Tucker and Kene Nwangwu
(no form row), Kyle Juszczyk, Alec Ingold, Michael Burton, Connor Heyward and Adam Prentice (form says FB, ESPN says RB),
Hollywood Brown and Drew Ogletree (Marquise and Andrew: not a first-name prefix, so the variant rule correctly stays
blank).

## 3. THE WEEKS AHEAD, THE STASH LANE, THE FIRST RUN

`lookahead_box.py` renders `wire.py`'s own `look_ahead()` (the computation stays in one place) inside one guarded call
from the engine: a failure inside the box, or a missing module, prints one console line and costs the page nothing;
the negative controls (a raised error, the module removed) both returned an empty box and a built page.

The stash lane: `next_man_up()` takes `holder_status`, ESPN's status for every man in the league (the free pool's from
the player read, the rostered men's from the new `league_status()` off the team read), and sets aside a team whose
depth-1 man carries a status in `sheet_engine.GONE_FOR_WEEKS`. Achane on injured reserve: MIA set aside, Gordon stays in
IN DOUBT NOW; Achane questionable: nothing changes; no status passed: the lane behaves exactly as before. This is the
second half of doc 442's NOT YET RUN line answered by rule rather than measurement: a usage leader who is out keeps
depth 1 in `usage_depth()` (the chart is still the tiebreak and the freshness source), and the lane that would have
sold his backup as "before the injury" now says the job is open. The first half, whether the practice report's Out
should be the step-past trigger beside ESPN's status, is still not run.

The first `ff.bat` run after docs 440 to 442 (BY HAND, 18:16): `RESULT: form 0, snaps 0, depth 0, lines 0, inherit 0,
projections skipped, ... kit 0, sources 0, vintage 0, pages 0, logic 0`; lines as of 18:06, weeks 4 and 5 of the
look-ahead on the line and week 6 on last season, the daily chart at 13:59 UTC with one nameless NYG row dropped and
named, 24 men on today's chart only and 16 August men off it. The Wednesday DAILY and the Tuesday 6 October projections runs (doc 439) are still
to be seen.

## 4. FOUR LIVE FINDINGS WITH NO PAGE TERM

- **4.13d**: a prohibition (no ceiling number exists), nothing to add; the reach gate is a target-share ceiling a man
  held, not a points ceiling, and the pickups text already says "a screen, not this man's forecast". Stays uncited.
- **4.25b**: already carried as the seat lane's `starter_g25` and `why` in `build_inherit.py`; cited there.
- **4.26**: (b) already carried by `te_playoff_slate()`; cited there. (a) is a draft-night keeper rule with no in-season
  term, and 4.34 replaced its tiebreak inside rounds 5 to 8.
- **4.34**: cannot run before week 10 (the predictor is weeks 10 to 14 against weeks 1 to 5). Where it goes: one
  roster-table column, "keeper riser", for every man drafted rounds 5 to 8, from `form_2026.csv` shares by week. Missing
  inputs, named: the weeks 1 to 5 baseline (storable from week 5), and the 2026 draft round for his men, which is in no
  file in the tree (the ESPN 2026 draft recap, or `draft_history` extended to 2026).

## 5. OPEN, BY NAME

- **Batch four:** the directive diet diff (doc 435 batch D), written as a diff for Matt; v9.35 only if a rule changes
  (candidates: §2's claim-order BLOCKED line is a filling input; the stand-in seat rule, ledger 211; the stash-lane rule
  above, which is doc 411 applied and not new text).
- **NOT YET RUN:** the practice report's Out as `next_man_up()`'s step-past trigger; the rise on an eight-week horizon
  (4.38); the 4.34 column from week 10; the trim of the other three pages (doc 439); the Wednesday and 6 October runs.
- **Matt's:** the two claim-order runs each week; the routes purchase; the ESPN D/ST box score.
