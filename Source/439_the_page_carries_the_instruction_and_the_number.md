# 439. The page carries the instruction and the number

*29 Sept 2026, 08:20 ET. Matt's seven-point review of `WEEK_SHEET.html` (07:30 DAILY build, week 4). Population: his roster and the free pool as `wire.py` read them at 07:30. Tested on an offline replay of `wire.py`'s sheet call on the 07:30 files; the production build is the next `ff.bat`.*

## 1. What he asked, and what was done

| his item | what changed |
|---|---|
| 1. strike the verbose notes, e.g. *"Your claims run Thursday, before dawn, while you are asleep"* | Cut throughout. Page text 32.1K to 21.6K characters (a third shorter). Gone: that line, the claims-run history, the "On paper this line is blank" note, every section standfirst that explained method, the worked example, "You asked when a week is a good week", the card commentary column, the false footer sentence (it said points a week were a season projection over 17 games; the page blends and prices the games left). The standing rules are one line each (`sheet_constants.json`). Kept: every number and every instruction |
| 2, 3. The Call's caption is a clipped text box and the section scrolls | `_tbl()` put every caption INSIDE the scrolling table, uppercase at 11px, as wide as the widest row. Captions are plain paragraphs above their tables now. The width came from unwrappable notes (`.meta`, the colspan note, the bet's "out of reach" cell); they wrap. At 1280px three tables scrolled (1354, 1841, 1464px in a 1178 box); none do now |
| 4. the seat list caption | Same fix, and cut to one line |
| 5. the left-off list; move the bet up | The bet is section 1, directly under THE CALL and the bye weeks, above the seat list. The left-off list came out, then came back at his second message the same morning, folded shut: one line, "Left off: 9 men, and why", full list on a click and no longer capped at eight |
| 6. are the weekly commands already scheduled? | **No.** All five tasks run `ff.bat`, and `ff.bat` ran none of the three. Now it runs `build_form.py` and `snaps_2026.py` at the top of every run, and `Espn_pull_projections.py` on the TUE task only (5.6 MB a pull). The to-do lines are ticked |
| 7. is the bar the only place to see byes? | **No**, and it was never the useful one. The calendar under THE CALL listed the weeks a position goes empty; it is titled "Bye weeks" now, sits directly under THE CALL, and prints every bye on the roster by week |
| 8. | arrived blank |

## 2. Found on the way

- **THE CALL's total was wrong.** It added every row before dropping the losing ones: "Taking all 3 nets +12.1" over two printed rows worth +12.6. It counts printed rows only now.
- **`build_form.py` would have died from week 6.** It required 32 clubs in every finished week. Week 5 has two clubs on bye (CAR, KC), so week 5 would have sat out of the cumulative row as "in progress" for a week, and the moment week 6 arrived every run would have exited "partial feed". It now expects 32 less that week's byes from `byes_2026.csv`.
- **`build_form.py` wrote `form_2026.csv` before its last check**, which is the reason doc 353 kept it out of `ff.bat`. It writes a temp file and swaps it in only after every check passes.

## 3. Tests

- **Page:** old and new engine on the same inputs. No table overflows at 1280px. `check_plain.py` clean. `check_pages.py`: the only failures are links to sibling pages the sandbox did not build. All eight `check_guards.py` anchors still match exactly once.
- **build_form, positive control:** old and new on the same live nflverse feeds give byte-identical files (weeks 1 to 3, no byes).
- **build_form, the defect:** a synthetic feed with CAR and KC on bye in week 3 and a week 4 behind it. Old: `FAILED: week 3 ... 30 of 32 clubs`. New: `week 3: 30 of 30 clubs`, file written.
- **build_form, the guard still fires:** Dallas removed from week 2 (not a bye). New: `FAILED ... 31 of 32 clubs`, and the previous file is untouched.
- **ff.bat:** not runnable here (no cmd.exe). `make_commands.bat_steps` parses the new file and lists the three new steps first. The first DAILY and TUE runs are the test; on `claude_todo.txt`.
- **Pins:** `check_kit.py` re-pinned `sheet_engine.py` 208,708 / `453a4aec26507eb3` and `ff.bat` 9,720 / `aada41fa1067464a`; both old files read STALE against the new pins through check_kit's own functions.

## 4. Open

- NOT YET RUN: the first new `ff.bat` runs (Wed 30 Sept 07:30 DAILY; Tue 6 Oct 06:00 for the projection pull).
- NOT YET RUN: the first real bye week through `build_form.py` (week 5, logged Tue 6 Oct).
- NOT DONE: the same trim on `THE_WEEKLY_WIRE.html`, `MY_TODO.html` and `LINEUP_CHECK.html`.
