# 436. The IR seat is not a drop

*28 Sept 2026, 23:05 ET. Written by a fresh session on its first read of the drive. Population: Matt's roster as `wire.py` wrote it at 22:35 (`MY_ROSTER.csv`, 18 rows: 15 active, 3 in slot 21) and the week sheet built from it in the same run.*

## 1. What the page said

THE CALL on `WEEK_SHEET.html` (22:35, week 3), top row:

> Kalif Raymond WR · +8.2 · **drop Jonah Coleman RB, Injured Reserve** · 0.0 · net +8.2 · this week

Coleman sits in the injured-reserve slot (`slot_id` 21), with Nacua and Dowdle. The other fifteen fill the roster.

## 2. Why it cannot work

**The load-bearing sentence (0.5(a5)): a man in the IR slot does not hold one of the fifteen, so dropping him frees no roster seat.** That premise is not new and it is measured in this league: doc 390 and ledger row 166, Nacua parked on 22 Sept left fourteen active and a free seat, and three adds needed two drops. Settings line 29 lists IR separately from the fifteen.

So the printed claim runs as sixteen of fifteen and fails on the roster limit, the failure the same page tells him to prevent everywhere else. Dropping a parked man frees a seat only through a second step: moving an eligible (Out or IR) man into the slot he left. Today nobody on the active fifteen is eligible.

**Not observed as a FAILED row, and cannot be from what is on the drive:** `waiver_report_*.csv` carries no slot, so no past claim can be shown to have named a parked man. BLOCKED on that input. The conclusion rests on the measured premise above, not on a failure count.

## 3. Every downstream use (section 3: enumerate, do not patch the spot)

`ir_box()` already knew who was parked. Nothing else asked it. In `sheet_engine.render()`:

| use | before | after |
|---|---|---|
| the seat count | `len(mine)`, parked men included: 18 today; with 14 active and 1 parked it would read 15 and say "roster full" with a seat free (doc 390's error, second instance) | parked men subtracted, joined on ESPN id |
| the cheapest-thing table, the floor, the cost line | Coleman first at 0.0 | parked men excluded |
| THE CALL's drop ladder | Coleman offered | parked men never offered |
| the starting-slot floors in THE CALL | parked men counted as bodies that can start | not counted |
| the full drop table | no mark | each parked man's row says dropping him frees no seat, and names the eligible man if one could take the slot |
| **THE CALL with an open seat** | `_rows_acc` skips "the open spot", so every add was charged a real man even with a seat free | the first adds take the open seats at 0.0. Found by the control below, not by reading |

`ir_picture()` now also returns `parked_ids`.

## 4. Tested on the object production builds

An offline replay of `wire.py`'s sheet call (lines ~1857 to 1915) on the 22:35 files reproduces THE CALL and the cheapest-thing table exactly, defect included. Then:

| roster | old engine | new engine |
|---|---|---|
| today (15 active, 3 parked) | Raymond / Coleman 0.0; Ty Johnson / Malik Washington 0.9 | Raymond / **Perine 0.0**; Ty Johnson / Malik Washington 0.9. Net unchanged, +11.4 |
| control: Perine removed (14 active, 3 parked) | "your roster is full", Raymond / Coleman | Raymond fills the open seat; Ty Johnson / Malik Washington |

None of the three drops is keeper-eligible: Perine, Malik Washington and Coleman were not drafted by JUG (`DRAFT_RECAP_2026.html`; Coleman went at 141 to another team).

Guards: `check_kit.py` re-pinned to 216,828 / `009ff58379e90977`, and the old engine reads STALE against the new pin through check_kit's own `sha()` and `size()`. All eight `check_guards.py` anchors still match exactly once. `check_pages.py` on the rebuilt page: no template or missing-value failure (its dead-link failures are pages the sandbox did not build).

**The production pages on the drive were NOT rebuilt from here.** The replay is close but not identical to `wire.py` (it priced 209 men where production priced 261), so the next `ff.bat` on his machine is the real build: the Tuesday 06:00 task, and the 08:54 task republishes the online copy after it.

## 5. Found on the way, fixed in the trackers

- `matt_todo.txt` said "A DIFFERENT drop on EVERY claim". `THE_WEEKLY_WIRE.html` says the same drop on several claims is his hedge and it works (31 for 31). Same mechanism, two intents: different drops to land both, the same drop to land only the first winner. The to-do now says which is which.
- `matt_todo.txt` week 9: "If you ever drop Shough, add a QB for week 10." Shough is gone; Hurts is the only QB and his bye is week 10. The line now says to claim one.
- Ledger row 162 (the "man he covers" named a back on another team) is fixed in code, the same-team test near `ahead_of_fp`, and the 22:35 page printed J.K. Dobbins for Coleman. Closed.

## 6. Open

- **NOT YET RUN:** the Tuesday 06:00 build is the production test. THE CALL must name no man from slot 21 and the log's RESULT line must stay all zero. On `claude_todo.txt`.
- **No guard catches this defect coming back.** `check_guards.py` has no mutation for it and none of its three guards reads THE CALL's drop column. On `claude_todo.txt`.
- **Not handled:** the one legal route through a parked drop (drop him, park an eligible man). The row names it; the ladder does not price it.
