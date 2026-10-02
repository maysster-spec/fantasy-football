#!/usr/bin/env python3
r"""
check_kit.py - STALE-COPY DETECTOR for the ONE canonical script tree.
Run:  py check_kit.py          (from anywhere)

CANONICAL LAYOUT, set 2026-08-28:
  G:\My Drive\_Fantasy\2026\Scripts\             everything Matt executes
  G:\My Drive\_Fantasy\2026\Scripts\live_draft\  the 5-file draft kit, self-contained
  G:\My Drive\_Fantasy\2026\Source\              documents, findings, data. Nothing runs here.

Catches ONE failure mode: the same filename holding different bytes in different
places. It does NOT verify that any file is CORRECT.
Re-pin deliberately with a new hash after an intentional change.
"""
import hashlib, os, sys

MANIFEST = {  # name: (bytes, sha256[:16])
    'live_draft.py':                 (134716, 'f711550878c6c5f0'),
    'code_live_engine.py':           (19135, 'bd580c023577074f'),
    # doc 267: RE-PINNED. The 7:00 PM keeper swap on Sept 7 rewrote both this and
    # player_context.csv, and neither pin was updated -- so check_kit has been reporting two
    # mismatches on every run since draft night and nobody read them. doc 260 again.
    # doc 295: RE-PINNED, and doc 267's re-pin is the reason these were wrong. board_v8_fixed.csv,
    # board_v7_kdst_separate.csv and player_context.csv have not changed on the drive since 7 Sept
    # (the 7:00 PM keeper swap and the midday context build), so the doc-267 numbers cannot have come
    # from the drive -- the same container-copy defect the setup_tasks.bat note below warns about.
    # check_kit has reported all three STALE on every run since 10 Sept. Pinned now at the drive's bytes.
    'board_v8_fixed.csv':            (41100, '0798189eb807c11d'),
    'board_v7_kdst_separate.csv':     (3511, 'aaa9fc381eaf64b8'),
    'ESPN_prerank_with_ids.csv':     (31704, 'fd95c162225c3fb7'),
    # doc 307: RE-PINNED, and the SIZE DID NOT CHANGE, which is why this needs a note.
    # depth_map.py WRITES this file, and doc 307's job-ceiling guard swapped Green Bay's
    # 152 for 241 in five rows. Three characters for three characters, so the byte count is
    # identical and only the hash moves. I re-pinned depth_map.py and forgot its OUTPUT,
    # which is section 0.5(d)'s own rule: anything that rewrites the board re-pins whatever
    # legitimately changed. depth_map.py and player_context.csv re-pin TOGETHER, always.
    'player_context.csv':           (109468, '875e492bdc35b679'),
    'Espn_pull_projections.py':      (15194, 'd0c6f891d56d0c2c'),
    'espn_draft_injector_Gemini.py':  (7618, '573dd1ebbf5e8da1'),
    'code_rebuild_spine_v5.py':       (8079, '917cdb488e960c4f'),
    'espn_api_python_script_historical_trans.py': (2997, 'a92aea6ed806fa34'),
    'espn_historical_scores.py': (3086, 'ca5f29e1485cd834'),
    'Espn_league_score-draft_2021_2024.py': (1861, '269573bcc6b3fd43'),
    # doc 260: RE-PINNED. The pin said 2,997 bytes -- the byte count of
    # espn_api_python_script_historical_trans.py, copied by hand and never right for this
    # file. It was already stale at 6,437 bytes before today's patch, and check_kit was
    # reporting a mismatch nobody read. Now 7,182: the transaction-type census.
    # doc 270: SEASONS was (2022,2023,2024,2025) -- the live season was never pulled, so no
    # file on the drive carried this year's transactions. Derived from the date now.
    # doc 342: (a) the de-dup key was (transaction id, WEEK). ESPN returns the live season's
    # transactions under EVERY scoringPeriodId, so waiver_report_2026.csv held 624 rows for 48
    # real moves, 13x. Completed seasons are unaffected and byte-identical, which is the control.
    # (b) --check called mTeam, a view ESPN serves on a session it no longer honours; it now
    # proves mTransactions2. (c) the zero-trades banner said ACROSS EVERY SEASON on a one-season
    # run. (d) a run that finds nothing now prints what the payload actually contained.
    'waivers.py': (12075, 'bcb79e09f9330b29'),
    # doc 267: the in-season sheet was never pinned. It now carries LANE 3, the potential
    # screen, so a stale copy would silently drop the only lane that is not about today.
    # doc 269: re-pinned -- the pedigree dict was leaking into WIRE_<date>.csv as a column,
    # and wire.py now also writes Source\\MY_ROSTER.csv every run.
    # doc 291: RE-PINNED. One team-code map shared with sheet_engine.py (Washington was off both
    # pages), the week read from the roster payload, the do-not rule, per-game rates, the
    # one-slot bye and the defence run's bye rule. Negative controls: ctl.py, 33 of 33.
    # doc 292: RE-PINNED. Also writes Source\\FREE_UNRANKED_<date>.csv, every free skill player the
    # board never rated, and a missing ownership number no longer crashes the run (latent on the 291
    # code). research\\redteam\\redteam_controls.py C17: 44 of 44; the pre-296 code fails 3 of them
    # and dies on the missing ownership number.
    # doc 321: RE-PINNED, AND THE PREVIOUS PIN IS THE WARNING. The comment below has claimed
    # doc 314's LAST COMPLETED GAME row since 16 Sept 02:02 -- and the file it was pinned to did
    # not contain it. The touches plumbing had been lost to a stale edit base, the pin was
    # recomputed from whatever shipped, and check_kit reported OK every time. A pin proves the
    # file has not CHANGED since I pinned it. It proves nothing about what is in it. What caught
    # this was reading the artifact: WIRE_20260915.csv had no touches column and WEEK_SHEET.html
    # said "contested" zero times. The guard for it is redteam_controls.py C21, not this table.
    # Restored here, plus doc 320's usage_depth() re-rank of the depth chart from week three.
    # doc 339: `E(` for `_esc(` on line 1276, a single-occurrence typo in a branch that only
    # runs when Matt is NOT first in the waiver order. It had therefore never executed until
    # 17 Sept, when ESPN returned a real order and the page build died with NameError AFTER
    # WEEK_SHEET.html was already written. Negative control run first (the original line does
    # raise), then the real write_page against the real Source folder with his own order.
    # doc 380: lineup.py builds a page Matt reads (LINEUP_CHECK.html) and was never pinned, so it
    # could have reverted to any earlier version without a sound (doc 345). Pinned from now.
    'lineup.py':                     (14215, '146d359b376eb717'),
    # doc 383: todo_page.py builds MY_TODO.html, a page Matt reads, and was never pinned (doc 380 §5).
    'todo_page.py': (3583, 'bae0db33217a6a89'),   # 21 Sept 23:10 RE-PINNED, doc 381: the header prints the next kickoff
    'wire.py': (159897, '176626dfa96794fa'),   # 1 Oct RE-PINNED, doc 469: the free rows carry ESPN's clear time for the card; doc 468's streaming sentence; doc 464's write_schedule. History in _archive and AUDIT_LEDGER.
                                               # the routine block that told him to run a
                                               # command his scheduler had already run. Doc 372/374   # doc 342: load_form() returned THREE
    # values on its normal path and TWO on all three of its error paths, so a missing,
    # unreadable or all-in-progress form_2026.csv killed the whole run with an unpacking
    # error instead of printing the reason it was written to print. Doc 320 added the
    # third value and changed only the last return. All three branches forced and shown
    # passing. It is also why redteam_controls.py has been failing its own base control
    # since doc 320 -- that harness does not copy form_2026.csv.
    # doc 330: ADD OR CLAIM. The pull already asked
    # ESPN for FREEAGENT and WAIVERS both; the parser read injuryStatus off `player` and
    # threw the availability on the ENTRY away, so every row said "check the button" for
    # a fact already in the payload. New `avail` column, the plain words on the row, and a
    # LOAD_PROBLEM when ESPN serves nothing rather than a guess.
    # THIS LINE USED TO SAY "Verified by C22 and C22c in redteam_controls.py, 65 of 65".
    # IT IS NOT (doc 345). The harness on the drive runs 60 checks, C0 to C23, and contains
    # no C22 at all; no archive holds a 65-check version. So the LOAD_PROBLEM branch is
    # NOT YET RUN, and the testable form is written down here so the next session does not
    # have to invent it: mock kona_player_info returning {'players': []} and assert the wire
    # page prints the load-problem line and NOT an empty free pool read as 'nobody is free'.
    # The pin proves this file has not changed since it was pinned and NOTHING about what is
    # in it (doc 321) -- which is exactly how a comment could keep citing a control that was
    # never written.
    # doc 316: the masthead name is read
    # from mTeam (mRoster never carried it) and the other eleven rosters are written out
    # instead of discarded. doc 314: load_form() now returns the
    # LAST COMPLETED GAME beside the cumulative row, and `touches` rides onto every free row --
    # the number the rest of the league actually files on. doc 311: the waiver order is READ from
    # ESPN's mTeam view; the page said "you are near the back of the line" as a
    # hard-coded string and priority resets weekly, so it was wrong most weeks.
    # doc 310: the week sheet is no longer
    # behind --html, whose help text named a DIFFERENT page; it builds by default and
    # --no-sheet opts out. doc 308: wire.py now reads
    # Source\form_2026.csv and tags the week-1 workload screen (2 of 3 = 38%
    # startable against a 13.9% base). Before this NOTHING on either page had seen
    # a snap of 2026 football. doc 307: RE-PINNED twice. the team AND THE BYE come from the
    # live pull, not the frozen board, and a moved player loses his old team's job number.
    # The bye was the same defect one column over: all seven corrected rows kept the bye of
    # the club they left.
    # doc 300: the sheet's masthead follows his
                                             # ESPN team name, read from mRoster   # doc 296: the man who inherits must be a
                                             # man who is PLAYING; the reason prints on the page   # doc 295: passes the week to the sheet, and a free
                                             # row now carries its ESPN status onto the page
    # doc 273: the week sheet's arithmetic, imported by wire.py --html. A stale copy
    # would keep printing a bar grid that no longer matches the lineup solver.
    # doc 319/321: RE-PINNED. a bye-week fill now prints what he is worth against the man you
    # would claim instead, not only against an empty slot -- 6.1 and 0.6 are the same tight end.
    # doc 325: RE-PINNED. the contested band says "carries and targets", not "touched the ball" --
    # build_form writes targets+carries, so the old wording overstated every pass-catcher.
    'todo_page.py': (3583, 'bae0db33217a6a89'),   # doc 342: rebuilds MY_TODO.html and
    # re-stamps the week sheet's link, with no network and no ESPN session, so the to-do
    # list is never hostage to a pull. It calls sheet_engine.write_todo_page -- the same
    # function wire.py calls -- so the two routes cannot drift.
    os.path.join('research', 'redteam', 'redteam_controls.py'): (34559, 'fff7b42874e36f25'),
    # doc 350: 65 checks, C0 to C24. C24 is anchored to the SEAT LIST heading and it
    # FAILED on the rename before the marker moved, which is the anchor working.
    'sheet_engine.py': (282389, '9dc486fdf3b43f97'),   # 2 Oct RE-PINNED, doc 472: the matchup number beside the rate on the roster rows and the drop ladder, RB and TE only (finding 4.49). Before that, doc 470: a cell under ten men prints no rate and sorts last on the lane; a weekly position enters THE CALL only as a hole fill; doc 469's card and odds. History in _archive and AUDIT_LEDGER.
                                                       # for five pages, section anchors. Doc 372   # 18 Sept 13:50 RE-PINNED: TODO_CMDS
    # gained `done "<some words>"`, so it shows on the to-do page AND on COMMANDS.html from the
    # one list. Before that, 18 Sept 13:15 RE-PINNED: THE SEAT
    # FILTER RAN ON THE WRONG POPULATION. Its availability/rostered test sat inside
    # `if not yours`, so any row whose man ahead is on Matt's own roster skipped it -- Dylan
    # Sampson led the list on INJURY RESERVE for a day because he is behind Judkins. The test
    # now runs on every row; `yours` only picks the alternative bar. Doc 354. Before that,
    # 18 Sept 13:00 RE-PINNED: the masthead
    # link now uses p.jump, the SAME rule the to-do page's jump links use (it was in TODO_CSS,
    # so only that page could reach it), and carries a second link to COMMANDS.html. Before
    # that, 18 Sept 12:45 RE-PINNED: Matt asked
    # for the to-do link on its own line under the kicker instead of running on after it, so it is
    # now a <p class="todoline"> sibling of <p class="kick"> and not a tail inside it. Before that,
    # doc 350: RE-PINNED. The section is THE
    # SEAT LIST now (one name he and the page both use), and each row says what the man
    # ACTUALLY DOES -- carries against catches, the role that implies, his snap share, his
    # NFL round and pick, and any live note. Printed, never scored: whether role breadth
    # predicts inheritance is NOT YET RUN. doc 349: the seat block
    # now rides at the TOP with the pickups (Matt asked three times; it was already merged into
    # the same list and then sorted below the five-row cap, which is merged and invisible), the
    # bar moved BELOW the priced pool, and the seats drop anyone rostered in this league or
    # carrying a multi-week designation, NAMED under the table. C24 covers all of it.
    # doc 345: doc 316's cap
    # exception is back -- the five-row cap on Priority pickups no longer eats a row whose
    # own contest band says to claim him first. It went missing in the 16 Sept 08:05 file
    # and nothing noticed for two days, because nothing pinned it and no control covered
    # it. C23 covers it now and was shown FAILING on the pre-restore code first.
    # doc 343: every seat now carries
    # its OWN odds of the job opening, from that back's share of his backfield in week one
    # -- 0.48 / 0.44 / 0.53 / 0.64 on 126 team-seasons -- so the seat table is ordered by
    # what it is worth rather than by the size of the job, which is all it could do while
    # every row shared one rate. The 3.02 weeks did NOT change and doc 343 says why it
    # failed its own test. 17 controls.
    # doc 342: the to-do list is a
    # page of its own, MY_TODO.html, linked from the masthead. It was showing SIX of
    # forty-three, first line only, at the bottom of section 0, with a stylesheet that
    # clipped every line at the box width. Twelve negative controls, including the
    # refusal to write a list whose parsed count does not match the file's own.
    # doc 317: every man's drop
    # cost is printed, net of the best free body at his position, so the page stops hiding
    # fourteen of the fifteen numbers it already computes. doc 316: the five-row cap no
    # longer hides a row the page itself flags 'put him first', and a played week is faded.
    # doc 314: the seat lane now
    # joins its own touch count off the free pool, so the man with the biggest workload stops
    # being the one row that says nothing. contest() prints how
    # many rivals file on a man and tells him to claim the contested one FIRST. doc 308: the workload bet lane,
    # the five-row cap, and the screened rows' magnitude is a TOTAL over the hold and
    # no longer says 'a week' (it was overstating by 6.4x). doc 307: the starter's status renders
    # beside the STARTER. doc 305: only a MULTI-WEEK designation is
                                             # demoted; a one-week OUT keeps its rank (Matt's
                                             # correction). doc 303: deleted a dead first build of
                                             # cost_line that was overwritten unread and still
                                             # carried "prices byes and not injuries", false since
                                             # real_price() shipped. doc 300: section 0 rebuilt on
                                             # his 12 Sept notes. doc 295: the ranked move.
    'keeper_swap.py':                 (16073, '823617362e3acff4'),
    'fetch_keepers.py':               (15797, 'd71f5bb38cb8553a'),
    'sept5_check.py':                 (8226, '40dd7047673737d8'),
    'board_audit.py':                 (11613, 'c425581513014d99'),
    # doc 174: gained the ADP_GRID link, which sync_desk_copies already dated.
    'make_shortcuts.py':              (9273, '949219f3e674d3d2'),
    'weekend_check.py':               (5049, '57a43831241ed4b0'),
    'cookie_jar.py':                  (5534, '7813460bee3d87fa'),
    # doc 295: RE-PINNED. wire.py, waivers.py and lineups.py joined its FILES list on 8 Sept, the day
    # those scripts shipped with cookies in them, and the pin never moved. A legitimate change reported
    # as STALE on every run since.
    'set_cookies.py':                 (7131, '034ac03096f241fe'),
    'tidy_duplicates.py':             (4281, '72bffe0e5a57655a'),
    'verify_prerank.py':              (5764, '41fa0ea242c31e98'),
    # doc 96: the dress-rehearsal harness. Pinned because it is the only thing that has
    # ever driven the live tool through a CHANGING draft, and a stale copy would rehearse
    # the wrong shape.
    # doc 97: the board correction path. A stale copy of apply_news.py or a lost
    # news_overrides.csv would silently restore a suspended player to the board.
    'apply_news.py':                 (7939, '566402dff928f7d7'),
    # doc 97: the paper board's builder. It had none, which is why the paper could not be
    # corrected when the board was.
    'make_fallback.py':              (7776, 'f28a8379257d1124'),
    # doc 102: the depth-chart parser behind the DART flag and the late-RB sheet.
    'depth_map.py':                  (12945, 'ea42a88a47b7e302'),   # doc 307: a job's worth may
    # not fall because its holder left the team. doc 275: FB_OFFSET
    # doc 108: adds YOUR OWN call to the live board.
    'my_take.py':                   (7045, '2723b505b5f08d99'),
    # doc 108: retires superseded reference docs to _archive.
    # doc 169: RE-PINNED. --root was a hardcoded list from Aug 30; all twelve entries had
    # already been moved and the root had refilled with fifteen NEW files it did not name.
    # Now rule-based, and it derives the protected desk stems from sync_desk_copies.py
    # rather than keeping a second copy of that list.
    'tidy_docs.py':                 (12992, 'd2de1ca1890f263e'),
    # doc 109: re-freezes ADP without rebuilding VBD.
    'refresh_adp.py':               (7008, '1b7f0c63a9668d2d'),
    # doc 109: rebuilds the three paper companion sheets.
    'make_sheets.py':               (11874, 'ad535f9e30d219cb'),
    # doc 111: the desk-copy sync.  Unpinned until now, which is how the root ended up
    # holding both an 0830 and an 0831 copy of three sheets.
    # doc 168: RE-PINNED. The doc-146 staleness guard was restored to this file on Sep 4
    # (5,674 -> 7,863) and the manifest was never updated, so check_kit.py -- which runs
    # inside draft_night.bat at 6:55 PM -- would have gone red on Monday against a file
    # that was CORRECT. A false STALE at 6:55 is the doc 97 s5 failure: it trains you to
    # wave the checker through on the one night it matters.
    'sync_desk_copies.py':           (8715, 'ada0d36ba2a19084'),
    # doc 111: provenance for 4.19 / 4.17b. Declares its own hit-rate bar at the top.
    'waiver_study.py':               (7595, '4268fdcc681584c6'),
    # doc 113: loads the Gemini injury sweep and, more importantly, reports what it MISSED.
    'import_injury_sweep.py':        (9591, '25ace3aecc2c8160'),
    # doc 114: where the board and the market disagree AND nobody has explained why.
    'delta_gaps.py':                 (10139, '889262c008a90d34'),
    # doc 116: ONE board. Replaces five paper artifacts.
    'make_board.py':                (30953, 'cf451a8aa371863a'),
    # doc 128: the "opportunity environment" measurement. 7.5% vs 93%; no flag was built.
    'env_study.py':                  (14065, 'e95ba5bff1533862'),
    # doc 129: the anchoring test, and the prior-year-availability finding behind the 12g badge.
    'anchor_study.py':               (15249, '303211efb22331f6'),
    # doc 126: rebuilds the ESPN prerank so it does not list a player ahead of his price.
    'make_prerank.py':               (8216, '5d5e1cbe11113f09'),
    # doc 137: the Chrome-extension bridge listener -- the draft-night pick source.
    'bridge_server.py':              (24240, 'af257da551acda2b'),
    # doc 139: the equivalence + speed harness for the _lineup rewrite. Pinned because a
    # stale copy would 'prove' a version of the engine that is not the one being run.
    'bench_lineup.py':                (3815, '5213a6f0e845c673'),
    # doc 137: the Chrome extension itself. Five files, and a stale hook.js is INVISIBLE --
    # it reconnects, prints nothing, and simply never forwards a pick.
    'background.js':                  (939, '87dca83acab4a0c7'),
    'hook.js':                       (4827, 'c4e8d976c04ae4ea'),
    'INSTALL.txt':                   (2858, '6a51abda1bf46c8e'),
    'manifest.json':                  (818, '06cb74dfe283129f'),
    'relay.js':                       (361, 'e83773808374edf7'),
    # doc 136: which ESPN url carries a draft WHILE it is happening.
    'probe_sources.py':              (6011, '74468d6ae1dae527'),
    # doc 132: the offensive line. Persistent, and still not actionable.
    'ol_study.py':                   (11567, '512f3862306032d5'),
    # doc 116: turns the Gemini analyst sweeps into analyst_takes.csv.
    'parse_takes.py':               (6389, '2b3653b11fc6cacd'),
    'rehearsal.py':                  (9260, '3a6a151fc63b09d2'),
    # doc 146: the value ladder's two halves. parse_ladder rebuilds values.csv off the
    # refreshed board; mkvalue prints it. Pinned because they are now steps 7 and 8 of the
    # post-refresh sequence, and a stale copy of either prints a ladder off an old board.
    'parse_ladder.py':               (9322, 'ef674766927a46db'),
    # doc 169: RE-PINNED. The page-break estimator is gone -- it never counted the header
    # block, so it was wrong from page 1 and left half of page 2 empty. Blocks now refuse
    # to split and the renderer paginates; 4 pages -> 3, no number left to go stale.
    'mkvalue.py':                   (14118, '40e598005086cb11'),
    # doc 62 Option A: the players the board cannot honestly be made to show.
    'mkoverride.py':                 (8197, '0d033b8cc449c4df'),
    # doc 146: makes the PDFs. wkhtmltopdf is NOT installed on this machine, so without this
    # every rebuild updates the web page and leaves the PDF where it was -- silently. This is
    # the file that stops last week's board reaching the desk.
    'to_pdf.py':                    (11061, 'cd4ed3f2f31d28a8'),
    # doc 163: make_howto.py joins the manifest. It regenerates HOW_TO_READ_IT.html from
    # live_draft.COLGLOSS and REFUSES to write if the board stopped drawing a badge the page
    # describes -- and sept5_after.bat now calls it, so a stale copy of it silently freezes
    # the only page that explains the board. Same reason the two batch files are pinned.
    'make_tiers.py':                 (13262, '05de1e35063c0285'),
    # doc 199: make_gridboard.py was NEVER pinned, and it builds DRAFT BOARD GRID -- a desk
    # sheet, and step 9 of sept5_after.bat. It was also the one file still printing s4.2's
    # RETRACTED pick-8 margin, found by Matt sitting down to read the grid for the first time.
    # A builder of a printed artifact belongs here for the same reason the batch files do.
    'make_gridboard.py':            (39110, '7e111dfc39cb72f0'),
    # doc 208: check_plain.py refuses to let the PAPER talk like the DOCS -- section numbers,
    # p-values and sample sizes on a page read at 60 seconds a pick. It is step 12 of
    # sept5_after.bat and it caught a live one on its first run, so it is pinned like any
    # other guard: a stale copy of a checker is worse than no checker.
    # doc 291: RE-PINNED. The pin was 5,240 bytes and the drive held 5,481 since 8 Sept, so this
    # checker has reported it STALE on every run since. It now also scans WEEK_SHEET.html.
    'check_plain.py':                (5611, '98847d50e567c052'),
    'make_howto.py':                (15413, '8f12a17ff2e68346'),
    # doc 146: THE TWO BATCH FILES THAT DRIVE A WHOLE EVENING, pinned for the first time.
    # draft_night.bat was still starting the OLD live board -- the one that reads picks from
    # ESPN's API, which doc 136 proved does not publish a draft until after it has ended. It
    # would have shown nothing all night and nothing would have said so. That is exactly the
    # "wrong file gets run" failure this checker exists for, so both are now hashed.
    'draft_night.bat':               (6405, '633b10b91385af1e'),
    'sept5_after.bat':               (9173, '060d7f27a8c6c171'),
    # doc 261: THE IN-SEASON PAIR, pinned for the first time -- same argument as doc 146's,
    # one season later. setup_tasks.bat registers the whole weekly schedule and ff.bat is
    # what all four tasks actually run; between them they drive every week from here to
    # week 14, unattended, with nobody watching the window. Both were unhashed.
    # Sizes and hashes taken from the files ON MATT'S DRIVE, not from a container copy.
    'setup_tasks.bat':               (5641, 'a6d45c443f3b21d0'),   # 19 Sept 20:00 RE-PINNED again, doc 379:
                                     # the WHAT EXISTS NOW block still said FOUR and told Matt to
                                     # delete the fifth task it had just made. Before that, RE-PINNED: the fifth
                                     # task, a daily 07:30 pull, because waivers settle on
                                     # ESPN's clock and that is none of the other four. Doc 374
    # doc 291: RE-PINNED at the bytes on the drive. ff.bat gained the WEEK_SHEET line on 10 Sept
    # (doc 273) and the pin was never moved, so every run since has reported it STALE.
    'done.py':                       (4883, '5e191a3d0059bb9a'),   # doc 355: NEW. The command
    # that lets MATT close an item instead of waiting for me to notice. It refuses on zero
    # matches and on two, printing the candidates; both refusals were shown firing before it
    # shipped. It archives the file, then calls todo_page.main() -- the same path ff.bat uses.
    'done.bat':                      (557, '681f5122046efa16'),   # doc 355: the one-word front
    # door for done.py, so it is `done ff.bat` and not a python invocation.
    'make_commands.py':              (13501, 'cfdaa6a8abc7b2d7'),   # 19 Sept RE-PINNED: the copy
                                     # button restored, and eleven CSS rules that had shipped as
                                     # literal {{ }} and never once applied. Doc 369   # doc 353: NEW, and pinned
    # on its first day. It regenerates COMMANDS.html from sheet_engine.TODO_CMDS plus the batch
    # files themselves, so the command page cannot drift from the tree. Its guard was shown
    # FAILING first, on a deliberately absent research\close_check.py, before it was shipped.
    'ff.bat': (13004, 'b125d3e4d6d3cd49'),   # 30 Sept RE-PINNED, doc 454: the projection pulled once a day (proj_due.py gate at half a day), the report and the prune after a pull. History in _archive and AUDIT_LEDGER.
    'build_news.py': (10029, 'c33b4e434842a785'),   # 24 Sept RE-PINNED, doc 414: an informationless row is filtered at source; 585 of the first 800 were status Active with nothing else. History in _archive and AUDIT_LEDGER.
                                     # step 6 check_vintage.py, then step 7 check_pages.py.
                                     # Doc 374, doc 376
    # doc 374: NEW AND PINNED FROM BIRTH. It fails the run when a page prints a rate this
    # season already refutes, which is the defect that produced four wrong recommendations in
    # twenty-four hours. A guard nothing pins can revert silently (doc 345), and this one is
    # the last thing that should.
    # doc 422: NEW AND PINNED FROM BIRTH. Every error on 24 Sept passed every internal-consistency
    # check because every file agreed; this one tests what an OUTSIDE field MEANS. Its seven
    # controls reproduce the real defects from docs 281, 417, 419 and 420 and must fire on them.
    'check_sources.py':              (13507, '2b64e1afba5e00e3'),
    # doc 425: NEW AND PINNED FROM BIRTH. It answers the question no other guard can: which
    # defects slip past ALL of them. It re-introduces eight failures this project actually
    # shipped and reports which ones nothing catches. Its FIRST run found SEVEN OF EIGHT.
    # Copies mutation testing (Trail of Bits, 18 Sept 2025): coverage measures execution, not
    # correctness-checking, so you break the thing on purpose and watch what stays silent.
    'check_guards.py':               (24019, 'f6cfa4c3971902ab'),   # 1 Oct RE-PINNED, doc 467: the harness pool carries every free kicker and defense (the hand-made Jets row is gone); doc 466's --fixture; docs 461 and 462's clock strip and re-aim.
    # doc 440: NEW AND PINNED FROM BIRTH. The page LOGIC guard doc 425 named as the missing layer: it reads
    # what WEEK_SHEET.html says against MY_ROSTER.csv (slot_id 21) and shares no engine code. 17 controls.
    'check_page_logic.py':           (71332, '6109e8962d5d6446'),   # 2 Oct RE-PINNED, doc 473: P12 (a second tight end is not on THE CALL this week) and P13 (the total counts this week's rows only); doc 472's P11; 72 controls. Before that, doc 470: P8b (a defense or kicker on THE CALL is a hole fill); doc 469's P6b, P7, P10; 63 controls.
    # doc 442: NEW AND PINNED FROM BIRTH. The spot-check card: one name, every number the pages used for him and
    # every number held that no page prints. Read-only; it is how the Joshua/Josh Palmer join miss was found.
    'spot.py':                       (29068, '957cdb963cc7dcb8'),
    # doc 443: NEW AND PINNED FROM BIRTH. The weeks-ahead box on the week sheet; sheet_engine.py imports it inside
    # one guarded call, so a stale or missing copy costs the page one box and prints one console line.
    'lookahead_box.py':              (7080, '6cfe3582c78d98ef'),
    # doc 443: PINNED FOR THE FIRST TIME. ff.bat has run it every day since doc 430 and nothing pinned it (doc 345's
    # lesson: a script nothing pins can revert without a sound). It now reports the pocket sheet's snapshot date.
    'make_online.py':                (8569, 'c3e37a8f83f249d8'),
    # doc 448: NEW AND PINNED FROM BIRTH. A local read before it is assigned, found statically in every shipped script;
    # it fired on the wire.py that died at 20:06 on 29 Sept and is quiet on the fixed one. Runs in ff.bat after this check.
    'check_locals.py': (9660, '733d05e1353befac'),   # 30 Sept RE-PINNED, doc 453: scans rookie_screen.py too.
    # doc 450: NEW AND PINNED FROM BIRTH. The standing rules a page states, against the directive's retractions and
    # section 2; it fired on the wire page that still said Tuesday night. Runs in ff.bat after the logic check.
    'check_page_rules.py':           (8557, 'de8b7503f61cf732'),   # 1 Oct RE-PINNED, doc 469: the v9.38 trigger sentence and the tight-end-at-zero sentence retired, the odds line and the RB/TE tiebreak live; six controls
    # doc 453: PINNED FOR THE FIRST TIME, the two builders ff.bat runs at the top of every run (doc 345's lesson: a script
    # nothing pins can revert without a sound). build_form.py writes the form file the sheet blends on; build_inherit.py
    # the seat lane's file. And the in-season screen's measurement, pinned from birth.
    os.path.join('research', 'wk1', 'build_form.py'):   (19400, '83a9bb7cca56647b'),
    os.path.join('research', 'build_inherit.py'):       (21846, '40a4ea773118b9fe'),
    os.path.join('research', 'wk1', 'rookie_screen.py'): (8793, '5063e794cfd7aadc'),
    os.path.join('research', 'wr_pair.py'): (11015, 'df463a8be6d3dc22'),   # 30 Sept, doc 456: the same-team receiver pair, null
    os.path.join('research', 'job_slope.py'): (14041, '8820e95a7b852343'),   # 30 Sept, doc 456: the relief rate against the job, null
    os.path.join('research', 'wk1', 'reach_gate_test.py'): (4842, 'eb9ac67328026e9e'),   # 30 Sept, doc 456: the reach gate on the screened men
    os.path.join('research', 'wk1', 'te2_split.py'): (6303, '9f1a303e2c2f3560'),   # 1 Oct, doc 457: the workload screen split by the man ahead
    os.path.join('research', 'own_quality_dst.py'): (4041, '2de4a085f5e0c28f'),   # 1 Oct, doc 458: a defense's own record against the line, null
    os.path.join('research', 'own_quality_dst2.py'): (4353, '69ee4b1afec0ad57'),   # 1 Oct, doc 458 section 2: tier by matchup band, the tie-break
    os.path.join('research', 'claim_rank.py'): (5154, '1d11b561721eda72'),   # 1 Oct, doc 463: a claim's landing rate by the claimant's waiver rank; --check guards claims.by_rank_band
    os.path.join('research', 'playoff_odds.py'): (12421, 'be32f4d1e305e266'),   # 1 Oct RE-PINNED, doc 469: live_numbers() for the week sheet's standings line; doc 464's backtest and convexity
    os.path.join('research', 'seat_weeks.py'): (5277, '3231fefa0d6ae7be'),
    os.path.join('research', 'audit_directive.py'): (9151, 'd3d75836b7d69d67'),   # 1 Oct, doc 468: the keeper table checked on the list and freeze it names (predicted_keepers_v5.csv, 09-03), the post-lock table printed as information; 51 of 51 ok
    os.path.join('research', 'matchup_term.py'): (7736, '5bce65e4b4d494e7'),   # 1 Oct, doc 468: the opponent's points allowed to the position, net of the man's own rate and the line, 2021 to 2025; RB and TE about a point a week between quartiles, WR nothing   # 1 Oct, doc 465: seat-weeks held against startable weeks delivered, drafted men against added men
    os.path.join('research', 'wk1', 'tail_tickets.py'): (11749, '2b54d4b4177a5cb4'),   # 1 Oct, docs 460, 463, 464: --check guards the cells; --last-game is the level reading, tested null
    # doc 451: NEW AND PINNED FROM BIRTH. Exit 0 when the newest projection pull is more than five days old; ff.bat
    # pulls on that, not only on the Tuesday task, after the 29 Sept Tuesday ran a batch file with no pull step.
    'proj_due.py': (9290, '354c03ab3ae04c7f'),   # 30 Sept RE-PINNED, doc 454: the gate at half a day, --report and --prune.
    'check_vintage.py':              (17369, '96e3386bd41362c9'),   # 24 Sept RE-PINNED, doc 418: it asked whether the printed rate equalled this season, which since the blend shipped fails a CORRECT page -- it did, on five men, in capitals. It now checks the page's number against the blend the page itself declares, which is stricter. Controls 6 and 7 are that false positive and its twin. History in _archive and AUDIT_LEDGER.
    # doc 376: NEW AND PINNED FROM BIRTH, same reason as the one above. It refuses a page
    # carrying an unsubstituted template, a local link with nothing behind it, or a cell
    # that says None. Its ten controls were run FIRST: six reproduce defects this project
    # shipped and must fire, four reproduce the shapes that LOOK like them -- nested CSS
    # closes, prose about the bug, percentages, a link that resolves -- and must not.
    'check_pages.py':                (26436, '085039f8e4717a52'),   # 29 Sept RE-PINNED, doc 443: C6, THE CALL's first row must print a vintage word, the man ahead for a back and one held input (a warning until 6 Oct, a failure after); C7, the pocket sheet's dated note; 28 controls, counted as they run. Before that, doc 380: C5, a pull-built page without a machine-readable read time; three new controls, 13/13. Before that: doc 353: step 4 builds
    # COMMANDS.html, which is generated now instead of hand-written, and the artifact check
    # covers it. weekly.bat and gameday.bat are stubs that call this file. Before that, doc 342:
    # EXTENDED, not
    # duplicated -- it already was the one-double-click file, and a second NAME for one JOB
    # is doc 146's after_pull.bat defect. Now also builds MY_TODO.html and runs check_kit,
    # and logs how old form_2026.csv is. Since doc 439 it also runs build_form.py, which now
    # writes through a temp file, so a failed fetch leaves the last good file.  doc 295: opens
    # the sheet when it changed
}
# doc 100: player_context.csv joins the kit as the 6th file -- the injury sheet's AVOID /
# DISCOUNT / NEUTRAL grades, shown as badges on the live board. live_draft treats it as
# OPTIONAL (missing = no badges, never fatal), but it is pinned so a stale one is caught.
KIT     = ['live_draft.py', 'code_live_engine.py', 'board_v8_fixed.csv',
           'board_v7_kdst_separate.csv', 'ESPN_prerank_with_ids.csv', 'player_context.csv',
           # doc 137/139: the bridge IS the draft-night pick source now -- doc 136 proved
           # ESPN's read replica publishes a draft only AFTER it ends. These three live in the
           # kit folder because live_draft.py --bridge, bridge_server.py and bench_lineup.py
           # all address the kit's own CSVs relatively. They were EXTRA files to this checker
           # until now, which meant every run reported FAIL on the newest part of the kit.
           'bridge_server.py', 'bench_lineup.py', 'probe_sources.py']
BRIDGE  = ['manifest.json', 'hook.js', 'relay.js', 'background.js', 'INSTALL.txt']
# EVERY script lives here. G:\...\2026\Scripts is the only script location.
# OneDrive\Fantasy\Scripts is retired -- verified byte-identical or older, 2026-08-28.
SCRIPTS = ['Espn_pull_projections.py', 'espn_draft_injector_Gemini.py',
           'code_rebuild_spine_v5.py',
           'espn_api_python_script_historical_trans.py', 'espn_historical_scores.py',
           'Espn_league_score-draft_2021_2024.py', 'waivers.py', 'wire.py', 'sheet_engine.py', 'lineup.py', 'todo_page.py', 'keeper_swap.py',
           # doc 80: both are draft-path scripts and were unpinned. fetch_keepers.py runs at
           # 7:00 PM; sept5_check.py decides FREEZE vs REBUILD. Neither should drift unnoticed.
           'fetch_keepers.py', 'sept5_check.py',
           # doc 86: rewrites the cookies in all four ESPN-facing scripts. A stale copy of THIS
           # would silently write the wrong cookies into the draft path.
           'set_cookies.py', 'cookie_jar.py', 'weekend_check.py', 'make_shortcuts.py', 'board_audit.py', 'tidy_duplicates.py', 'verify_prerank.py',
           'rehearsal.py', 'apply_news.py', 'make_fallback.py', 'depth_map.py', 'make_sheets.py', 'refresh_adp.py', 'my_take.py',
           # doc 111: the desk-copy sync. Unpinned until now.
           'sync_desk_copies.py', 'tidy_docs.py', 'waiver_study.py',
           'import_injury_sweep.py', 'delta_gaps.py',
           'make_board.py', 'parse_takes.py',
           # doc 128 / 129: measurement scripts. Pinned so their conclusions stay reproducible.
           # doc 139: bridge_server.py moved OUT of this list -- it lives in the kit
           # folder next to live_draft.py, and expecting it here reported MISSING in
           # Scripts\ and EXTRA in Scripts\live_draft\ for the same one file.
           'env_study.py', 'anchor_study.py', 'ol_study.py',
           'make_prerank.py',
           # doc 146: the post-refresh sequence and its three newest steps, plus the two
           # batch files that drive a whole evening between them.
           'parse_ladder.py', 'mkvalue.py', 'mkoverride.py', 'to_pdf.py',
           # doc 163: make_howto.py is a step of the Saturday chain now, not a one-off.
           'make_howto.py', 'make_tiers.py', 'make_gridboard.py', 'check_plain.py',
           'sept5_after.bat', 'draft_night.bat',
           # doc 261: the in-season schedule and its runner.
           'setup_tasks.bat', 'ff.bat', 'make_commands.py', 'done.py', 'done.bat',
           # doc 374, doc 376: the two page guards, checked like any other shipped script.
           'check_vintage.py', 'check_pages.py',
           # doc 440: the page logic guard, run by ff.bat after check_pages.py.
           'check_page_logic.py', 'spot.py',
           # doc 443: the weeks-ahead box and the online copy, both run or imported every ff.bat run.
           'lookahead_box.py', 'make_online.py',
           # doc 448: the order guard.
           'check_locals.py', 'check_page_rules.py', 'proj_due.py',
           # doc 345: THE HARNESS IS PINNED FOR THE FIRST TIME, and it is the file that
           # most needed it. On 16 Sept it held 44 checks at 08:05 and 56 at 19:15; on
           # 17 Sept at 21:30 it held the 08:05 BYTES AGAIN, hash-identical -- four
           # controls gone and no sound. A guard nothing pins can revert to a version
           # that still passes, which is worse than one that fails.
           os.path.join('research', 'redteam', 'redteam_controls.py'),
           os.path.join('research', 'wk1', 'build_form.py'), os.path.join('research', 'build_inherit.py'),
           os.path.join('research', 'wk1', 'rookie_screen.py'),
           os.path.join('research', 'wr_pair.py'), os.path.join('research', 'job_slope.py'),
           os.path.join('research', 'wk1', 'reach_gate_test.py'),
           os.path.join('research', 'wk1', 'te2_split.py'), os.path.join('research', 'own_quality_dst.py'),
           os.path.join('research', 'own_quality_dst2.py'), os.path.join('research', 'wk1', 'tail_tickets.py'),
           os.path.join('research', 'claim_rank.py'), os.path.join('research', 'playoff_odds.py'),
           os.path.join('research', 'seat_weeks.py'), os.path.join('research', 'audit_directive.py'),
           os.path.join('research', 'matchup_term.py')]
# after_pull.bat is deliberately NOT pinned. It was a duplicate of sept5_after.bat and is now
# a two-line stub that calls it; the moment Matt deletes it, a pinned entry would turn that
# tidy-up into a FAIL. doc 146.
# actual_keepers.csv is deliberately NOT pinned -- Matt edits it at the 7:00 PM lock.
# my_takes.csv is deliberately NOT pinned either, for the same reason: it is Matt's sheet,
# he edits it whenever he likes, and `py my_take.py --file` re-pins the FILE IT WRITES
# (player_context.csv) rather than the sheet it read.
# After `keeper_swap.py --write`, TWO hashes flag STALE by design and that is expected:
# board_v8_fixed.csv always, and board_v7_kdst_separate.csv WHENEVER A K OR D/ST WAS KEPT
# (doc 164 -- 2026 is such a year: Brandon Aubrey). Re-pin post-draft, not on the night.

# The only files whose duplication can change what happens on draft night.
DRAFT_PATH = ['Espn_pull_projections.py', 'espn_draft_injector_Gemini.py',
              'keeper_swap.py', 'fetch_keepers.py', 'ESPN_prerank_with_ids.csv'] + KIT

BASE = r'G:\My Drive\_Fantasy\2026'
CANONICAL = [
    (os.path.join(BASE, 'Scripts'),               SCRIPTS, False),
    (os.path.join(BASE, 'Scripts', 'live_draft'), KIT,     True),   # exact set
    # doc 139: the Chrome extension is now part of the draft path and was never checked.
    (os.path.join(BASE, 'Scripts', 'live_draft', 'espn_bridge'), BRIDGE, True),
]
# Superseded. These must end up EMPTY of kit/script files or the confusion returns.
LEGACY = [
    (os.path.join(BASE, 'Source', 'live_draft'),        KIT),
    # doc 79: Source\ still held a 3,143-byte board_v7_kdst_separate.csv -- the pre-ESPN_ID
    # version whose missing column silently disabled the D/ST already-drafted filter. Only the
    # three kit CSVs are worth flagging here; Source\ legitimately holds analysis .py files.
    (os.path.join(BASE, 'Source'),
     ['board_v8_fixed.csv', 'board_v7_kdst_separate.csv', 'ESPN_prerank_with_ids.csv']),
    # Only DRAFT-PATH files are worth flagging here. espn_historical_scores.py and
    # friends are season-review utilities -- a stale copy of one cannot affect Sept 7,
    # and warning about them every run trains you to ignore the warning that matters.
    (r'C:\Users\wmatt\OneDrive\Fantasy\Scripts',         DRAFT_PATH),
    (r'G:\My Drive\Fantasy\Scripts',                     DRAFT_PATH),
]
# NOTE the kit's ESPN_prerank_with_ids.csv lives in Scripts\live_draft\, not Scripts\ --
# the injector addresses it there absolutely. It is intentionally NOT in SCRIPTS.

# Text files get their line endings normalised before hashing. A file round-tripped
# through a Windows editor gains a CR on every line -- 94 extra bytes on the injector,
# zero change in behaviour. Flagging that as STALE trains you to ignore the checker,
# which is worse than having no checker on the one night it matters.
TEXT = ('.py', '.csv', '.md', '.txt', '.bat', '.ps1')

def sha(p):
    h = hashlib.sha256()
    if p.lower().endswith(TEXT):
        with open(p, 'rb') as f:
            h.update(f.read().replace(b'\r\n', b'\n'))
    else:
        with open(p, 'rb') as f:
            for b in iter(lambda: f.read(65536), b''): h.update(b)
    return h.hexdigest()[:16]

def size(p):
    """Normalised byte count, to match sha() above."""
    if p.lower().endswith(TEXT):
        with open(p, 'rb') as f:
            return len(f.read().replace(b'\r\n', b'\n'))
    return os.path.getsize(p)

SELF = os.path.join(BASE, 'Scripts', 'check_kit.py')
# Doc 78 chunk 4, closed here: "the checker checking itself". check_kit cannot carry its own
# hash (chicken-and-egg), but the failure it needs to prevent is concrete -- Matt runs a STALE
# COPY of this file and it cheerfully certifies a tree it does not understand. Source\ held a
# 3,324-byte copy of a 6,739-byte checker for exactly that long. So: prove WHICH file is running,
# and name every other copy on disk.
SELF_LOOK = [os.path.join(BASE, 'Source'), os.path.join(BASE, 'Scripts'),
             os.path.join(BASE), r'C:\Users\wmatt\OneDrive\Fantasy\Scripts',
             r'G:\My Drive\Fantasy\Scripts']

def self_check():
    """Returns the number of problems. Runs BEFORE anything else is certified."""
    me = os.path.abspath(__file__)
    bad = 0
    if os.path.normcase(me) != os.path.normcase(os.path.abspath(SELF)):
        print('!! YOU ARE NOT RUNNING THE CANONICAL CHECKER')
        print(f'   running : {me}')
        print(f'   canonical: {SELF}')
        print('   A stale checker certifies a stale tree. Everything below may be wrong.')
        print(f'   Re-run as:  py "{SELF}"')
        bad += 1
    others = []
    for d in SELF_LOOK:
        c = os.path.join(d, 'check_kit.py')
        if os.path.exists(c) and os.path.normcase(os.path.abspath(c)) != os.path.normcase(me):
            others.append((c, size(c), sha(c)))
    if others:
        mine = (size(me), sha(me))
        print(f'!! {len(others)} OTHER cop(ies) of check_kit.py on disk '
              f'(this one is {mine[0]:,}B {mine[1]}):')
        for c, n, h in others:
            same = 'identical' if (n, h) == mine else 'DIFFERENT BYTES'
            print(f'   {c}   {n:,}B {h}   <- {same}')
            if (n, h) != mine: bad += 1
        print('   Delete or archive them. One checker, one name, one location.')
    if not bad:
        print(f'self      {me}   (canonical, no divergent copies)')
    print()
    return bad

def main(canonical=CANONICAL, legacy=LEGACY):
    bad = self_check()
    print('=== CANONICAL ===')
    for folder, names, exact in canonical:
        if not os.path.isdir(folder):
            print(f'MISSING FOLDER  {folder}'); bad += 1; continue
        for n in names:
            p = os.path.join(folder, n)
            if not os.path.exists(p):
                print(f'MISSING   {p}'); bad += 1; continue
            got, want = (size(p), sha(p)), MANIFEST[n]
            if got != want:
                print(f'STALE     {p}\n          want {want[0]:,}B {want[1]}\n'
                      f'          got  {got[0]:,}B {got[1]}'); bad += 1
            else:
                print(f'ok        {p}')
        if exact:
            # Generated at runtime by the tool itself. Their presence proves it ran.
            # doc 95: live_board.html.tmp is the atomic-write scratch file. It is deleted by
            # os.replace() on every successful write, but a Ctrl+C at the wrong instant can
            # leave one behind, and that must not read as a corrupted kit.
            RUNTIME = {'__pycache__', 'live_board.html', 'live_board.html.tmp',
                       'sept5_last.txt', 'adp_vintage.txt',
                       'feed_evidence',   # doc 122: raw ESPN payloads, kept on purpose
                       # doc 137/139: what the bridge writes. bridge_picks.json is the live
                       # handoff, .tmp is its atomic-write scratch (removed by os.replace,
                       # but a Ctrl+C can leave one), _REPLAY is --replay's separate file,
                       # and the .jsonl is the append-only raw socket log.
                       'bridge_picks.json', 'bridge_picks.json.tmp',
                       'bridge_picks_REPLAY.json', 'bridge_raw.jsonl',
                       'DRAFT_ROOM_RECON.txt',
                       # doc 189: written by `live_draft.py --replay`, which doc 163 ran
                       # on 09-04. It has been reported EXTRA on every run since -- a
                       # checker that always says FAIL is a checker you stop reading,
                       # which is the same reason line endings are normalised above.
                       'replay_log.txt'}
            # Not generated -- source that belongs here but cannot be hashed as a
            # file. espn_bridge gets its own CANONICAL entry above.
            SUBTREE = {'espn_bridge'}
            for e in sorted(set(os.listdir(folder)) - set(names)):
                if e in RUNTIME:
                    print(f'runtime   {os.path.join(folder, e)}   (generated, ignored)')
                    continue
                if e in SUBTREE:
                    print(f'subtree   {os.path.join(folder, e)}   (checked separately)')
                    continue
                print(f'EXTRA     {os.path.join(folder, e)}'
                      f'   <- kit folder must hold exactly {len(names)} real files'); bad += 1

    print('\n=== SUPERSEDED (should be empty of these files) ===')
    stragglers = 0
    for folder, names in legacy:
        if not os.path.isdir(folder):
            print(f'gone      {folder}'); continue
        found = [n for n in names if os.path.exists(os.path.join(folder, n))]
        if found:
            print(f'STRAGGLER {folder}\n          still holds: {", ".join(found)}')
            stragglers += len(found)
        else:
            print(f'clean     {folder}')
    # 'gone' above means the path does not exist on this machine -- that is a PASS,
    # not an error. G:\My Drive\Fantasy\Scripts exists in Google Drive but is not
    # synced to a local path, so nothing can be run from it.

    print()
    if bad:        print(f'FAIL: {bad} problem(s) in the canonical tree')
    else:          print('PASS: canonical tree matches the manifest')
    if stragglers: print(f'WARNING: {stragglers} superseded copies still on disk. '
                         f'Archive or delete them - they are how the wrong file gets run.')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
