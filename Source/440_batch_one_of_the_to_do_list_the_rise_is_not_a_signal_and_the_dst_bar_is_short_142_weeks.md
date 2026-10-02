# 440. BATCH ONE OF THE TO-DO LIST: THE RISE IS NOT A SIGNAL OVER THE LEVEL, AIR YARDS STAY DISPLAY, AND THE D/ST BAR IS SHORT 142 TEAM-WEEKS

*29 Sept 2026. Claude (Cowork), on Matt: "complete the to do list... do it in batches if needed to ensure fidelity." Batch one is
the measurements that could run on data already in hand and the guard fixes. 440 reserved by listing `Source\` at 09:20 (439 is
the page review, another session, the same morning). No em dashes.*

---

## 0. WHAT TO DO

1. **Read a claim candidate's LEVEL, never his rise.** Your 27 Sept claim, "counts on the field and targets combined are a signal
   for a player whose role could expand", is tested (finding 4.38) and on a four-week horizon it does not hold: at the same snap
   share and targets this week, the man who just ROSE to them is about 7 points less likely to be startable over the next four
   than the man who was already there (minus 6.7, se 0.9, n=9,393, every season, every position). The raw both-rose cell is 1.4
   points better than the pool, and that is the level showing through. A rise is not extra credit; at a given reading it is a
   little caution. Two-game expected points and snap share are the read (4.37, and doc 434 on snaps).
2. **Air-yards share and WOPR stay display columns.** As a fourth signal on the workload screen's 2-of-3 bar they add +0.1 and
   +0.8 points of spike rate (p=0.90 and 0.21); the falsifier was +2. Same verdict as expected points. The top-fifth cuts, if
   you want them on the page: WOPR 0.461, air-yards share 25.2%.
3. **A rise in expected points from one game to the next is also nothing over the level** (+0.03 a point against +0.60 for the
   level). Closed.
4. **The D/ST replacement number is wrong and it is mine to fix in batch two: 5.99 becomes about 5.5.** `build_dst.py` writes a
   row only when the defence recorded an event, so 142 team-weeks whose score is the points-allowed band alone (mean minus 3.9)
   are missing from the file every D/ST number was measured on. On all 2,718 team-weeks D/ST12 is 5.57, and 5.51 with the two
   terms the file never carried (blocked kicks +0.15 a week, fumbles lost minus 0.13). A D/ST week is 4.99, sd 6.59, not 5.46,
   sd 6.28. Until batch two ships, do not quote 5.99 as measured; it is a number from an incomplete file.
5. **The two tight-end rows are now from the fixed script, not a hand rebuild.** Two ordinary tight ends platooned: minus 0.03
   a week, a null (t minus 0.50, n=528); with any quality gap the pair loses. Doc 428 corrected in place.
6. **Four guards shipped and every one fired on its negative control first:** `check_page_logic.py` (a man in the IR slot
   offered as a drop in THE CALL or named cheapest; 17 controls; runs in `ff.bat` after the page check), `check_guards.py`
   (a guard missing from disk is now reported and fails the run; two mutations for the parked-man drop), the registry's AVG
   guard (2021's AVG is not derivable from its site columns and its MANIFEST row now says so; 2025's average excludes
   Real-Time), and `check_inputs.py` reads the finding ids from the directive's index with a left boundary.
7. **The kicker rule is unchanged.** `dst_k_supply.py` deducted missed PATs, which we do not score: 0.086 a week, the usable
   count moves by 0.4, the "mild fall" holds. Fixed. K12 8.26 never deducted it.
8. **One check only you can make (on your list):** open one ESPN D/ST box score in our league for a week with a known return
   fumble lost (DEN D/ST, week 1 2025, the Mims muffed punt) and see whether it shows minus 2. That settles whether the fumble
   term belongs in the bar.
9. Nothing to run. The next `ff.bat` runs the new guard; the RESULT line gains `logic`.

---

## 1. THE RISE, TESTED (finding 4.38)

**Testable form, stated before the run:** among non-startable RB, WR and TE in week w (doc 438's claimable pool, REG 2021 to
2025, weeks 2 to 16, n=9,999), does a rise in BOTH snap share and targets against his previous game predict startable over
the next four weeks (2+ games, n=9,393) over and above the level of either? Falsifier: under +3 points net of the levels, the
level alone is the signal.

| cell, startable over the next four | n | rate |
|---|---|---|
| both rose | 2,383 | 18.8% |
| only snaps rose | 2,452 | 17.4% |
| only targets rose | 1,416 | 19.5% |
| neither | 3,142 | 15.5% |
| the pool | 9,393 | 17.4% |
| both rose 10+ snap points and 3+ targets | 675 | 20.9% |

Net of the week-w snap share and targets, both-rose is **minus 6.7 points (se 0.9)**; RB minus 6.2, WR minus 7.9, TE minus 6.4;
every season between minus 5.2 and minus 8.2; the strict rise minus 8.9. The interaction (both minus the sum of the single
rises) is minus 2.6 pooled and minus 4.9 at WR: substitution, not amplification. Horizon is four weeks; a longer one is NOT YET
RUN and is on the list. Script `Scripts\research\wk1\delta_screen.py`, output beside it.

## 2. THE AIR-YARDS THRESHOLD (finding 4.35, addendum)

On doc 389's population (n=8,718, reproducing its rates), the 2-of-3 bar is n=1,350 at 12.1% spike. WOPR at its top-fifth cut
as a fourth signal: 12.2% with (n=1,143) against 11.6% without (n=207). Air-yards share: 12.9% (n=869) against 10.6% (n=481),
+2.3 with-against-without at se 1.8. Both under the +2-over-the-bar falsifier. Startable next four moves +0.9 and +2.6. The
count 0-of-4 to 4-of-4 on air yards: 1.8 / 5.3 / 8.1 / 11.7 / 14.5% spike.

## 3. THE DELTA IN EXPECTED POINTS (finding 4.37 (g))

Level +0.60 (se .01), delta +0.03 (se .01). Top fifth by delta 24.2% startable next four against 38.9% by level; delta-only cell
17.1% against the pool's 17.4%. Falsified on both halves.

## 4. THE D/ST FILE IS SHORT 142 TEAM-WEEKS

`Scripts\research\build_dst.py` iterates the defensive events it counted and writes a row per team-week that had one, so a
week with no sack, interception, recovery, safety or defensive score, whose score is the band alone, is absent: 24 / 28 / 23 /
38 / 29 by season, mean minus 3.88. The shipped file has 2,576 rows; a full file has 2,718 (2022 has 542: Buffalo at
Cincinnati was cancelled). Reproduced first: the price script rebuilds all 2,576 shipped rows with zero mismatches, then adds
the missing 142 and the two terms section 2 scores and the file never carried.

| number | as published | all 2,718 rows, no new terms | all rows, blocked kicks and fumbles lost added |
|---|---|---|---|
| a D/ST week, mean (sd) | 5.46 (6.28), n=2,576 | 4.97 (6.51) | 4.99 (6.59) |
| D/ST12, weeks 1 to 14 | 5.99 | 5.57 | 5.51 |
| supply curve, defenses above the bar early / late | 13.5 / 13.6 | 13.6 / 13.4 | 13.8 / 13.4 |

Blocked kicks: 188 in five seasons, +0.146 a week (a field goal, extra point or punt blocked, +2 to the blocking team).
Fumbles lost by the return or defensive side: 161, minus 0.125 a week. Net +0.02: immaterial. The missing rows are the
material part, minus 0.42 on the bar. Two more omissions priced as asides: kickoff-return touchdowns (32, +0.07 a week, the
script's own-team test excludes them) and punt-coverage recoveries of a muff (113, +0.08). **NOT ESTABLISHED, and it is the
one input that settles the fumble term: whether ESPN charges the D/ST slot for a return fumble lost.** The settings line sits
under the merged Defense / Special Teams and Misc header and nothing on disk holds an ESPN D/ST actual. One box score
settles it (§0, item 8). Batch two ships the rebuilt file, the fixed builder, and the new bar in `sheet_constants.json`,
`dst_k_supply.py`, the directive and its DO-NOT-QUOTE table. Script `Scripts\research\price_dst_k_terms.py`.

## 5. THE TIGHT-END SCRIPT

`te_pair.py` built one generosity per defence per season from weeks 1 to 14 and mapped it onto every scored week, so each
week-2-to-14 game sat inside its own matchup term. Fixed: for a game in week w the mean over weeks 1 to w-1 only; `--in-sample`
reproduces the retracted rows byte for byte below two header lines; `--selftest` adds 100 points to one 2023 game against
Baltimore and asserts the in-sample term moves (minus 0.85 to +6.60) and the ex-ante term does not. Rows, weeks 2 to 14, softer
matchup minus always start TE1: elite + streamable minus 1.77 (se 0.10, n=288; was minus 0.86) · mid + streamable minus 0.95
(se 0.07, n=288; was minus 0.37) · two streamable minus 0.03 (se 0.06, n=528; was +0.50). Doc 435's hand rebuild confirmed to
the decimal; doc 428 bannered from the run; ledger row 191 closes. The cache path was container-absolute and now resolves
against the script.

## 6. THE GUARDS

- **`check_page_logic.py`, new.** Doc 425 named the missing layer: every guard recomputed from the engine, so an engine
  defect passed through all of them. This one parses `WEEK_SHEET.html` and reads slot 21 from `MY_ROSTER.csv` itself: no man in
  the IR slot in THE CALL's drop column, none in the cheapest table or the cost line. 17 controls (8 fire, 9 quiet). The
  mutated engine rebuilt doc 436's exact defect ("take Mayer / drop Jonah Coleman, Injured Reserve, 0.0") and the guard fired;
  the real engine passes (drops Washington, Perine, Vele). `ff.bat` runs it after `check_pages.py`; RESULT carries `logic`.
- **`check_guards.py`.** A guard named in GUARDS and absent from disk was skipped with a bare `continue`; the staged tree
  reproduced it live (no `check_plain.py` there) and the harness printed doc 425's numbers without naming the gap. Now reported
  by name before any build, counted as a failure (exit 3), and the selftest's first control is that case. Two priority-1
  mutations drop the parked-man predicate at THE CALL and at the cheapest table; both caught by the new guard.
- **The registry.** `adp_registry_from_fp.py` tests every subset of site columns against AVG on every row (tolerance 0.05) and
  writes the MANIFEST clause from the result. 2021: 253 of 295 rows with a site value are off, 200 rows carry an AVG and no
  site value at all; the build now refuses 2021 unless `--avg-not-derivable "<reason>"` is passed, and refuses that flag on a
  page that IS derivable (2023 tried). 2022 is Yahoo and Sleeper; 2023 and 2024 all three; 2025 is Yahoo, Sleeper and RTSports
  on all 389 rows and Real-Time on none. Rebuilt 2021, 2022, 2023 and 2025 byte-identical to the drive; 2024 differs on 30 D/ST
  name spellings only (doc 383's earlier build), every ADP identical, not replaced. `MANIFEST.csv` replaced with the checked
  clauses.
- **`check_inputs.py`.** The "uncited findings" scan reads the ids from the directive's index (lettered ones included, no
  hand-typed stop at 4.36) and carries a left boundary: 4.4 passed on "14.4" and 4.7 on "+14.7".

## 7. THE TWELVE UNCITED FINDINGS, CLASSIFIED

Draft-era, correctly unwired: 4.10, 4.12, 4.13, 4.15, 4.29. Measured null or tiebreak only, correctly unwired: 4.21 (it
forbids an environment column), 4.24, 4.25. **Used without a citation, now cited:** 4.11 (`wire.py` `bye_plan()` prices a
bye at its lineup loss), 4.18 and 4.18b (`wire.py` `drop_table()` applies the round bands every week, so the index row saying
"draft" is wrong and goes to "both" at v9.34), 4.20 (`depth_map.py` and `build_inherit.py`, the seat lane), 4.35 (the
air-yards columns, display). Forgotten live season findings: none. The scan now lists 4.1b, 4.11b, 4.13c, 4.13d, 4.18c, 4.25b,
4.26, 4.34 and 4.37 as well; 4.37 is cited in `wire.py` as of this doc, the rest are draft-era or nulls except 4.13d, 4.25b,
4.26 and 4.34, which are live "both" findings with no page term yet and go on the list as one line.

## 8. OPEN, BY NAME

- **Batch two, mine, in this order:** the D/ST bar (fix `build_dst.py`, rebuild the file, 5.51 into `sheet_constants.json`
  and `dst_k_supply.py`, the directive at v9.34 with a DO-NOT-QUOTE row for 5.99 and 5.46); routes on the 2023 to 2025
  participation files; Vegas lines; red zone from play-by-play; the daily depth chart and practice status; the RB opportunity
  share.
- **Batch three:** the page and engine wiring (xfp columns, the blend beside the measured rate, inherit columns, the form join,
  the QB look-ahead, the check_pages display rule, the claim-order pairing, the spot-check card, the pocket sheet).
- **Batch four:** the directive diet diff, and v9.34 (index rows 4.38, 4.18 to "both", the D/ST retraction).
- **NOT YET RUN:** the rise on an eight-week horizon (4.38 scope).
- **Matt's:** the ESPN D/ST box-score check (item 8).
