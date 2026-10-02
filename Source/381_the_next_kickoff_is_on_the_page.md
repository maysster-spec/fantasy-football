# 381. THE NEXT KICKOFF IS ON THE PAGE: THE DEADLINE HALF OF DOC 380, READ OFF ESPN'S OWN SCHEDULE

*21 Sept 2026, 23:10 ET. Fable, at Matt's instruction ("run the two queued jobs, next kickoff then JOB
4"). Closes doc 380 §4's NOT YET RUN. Doc 380 is the previous number; 381 reserved by listing the
folder at 19:05 and re-checked against the store. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run.** Tuesday's 06:00 wire fetches the schedule again (the file on the drive has no
   kickoff column, so the refetch is forced once) and every page built after it carries the next lock.
2. **What the pages say now.** The sheet's inputs box gains one line: *Lineups lock at kickoff. Your
   first man locks Sunday 27 September 13:00 (week 3, LAR at PHI); the week's first game is Thursday
   24 September 20:15 (week 3, MIA at BUF).* The wire and the lineup check carry *next kickoff on file:
   Thursday 24 September 20:15 (week 3, MIA at BUF)* in their headers. When you open a page after a
   kickoff it was built before, the box turns red and says so, ahead of the settlement sentence.
3. **A number that is measured, not typed:** the kickoff is ESPN's own `date` field on each game
   (epoch milliseconds), written into `sched_2026.csv` as a `kick` column by `wire.fetch_schedule()`.
   Nothing on the page assumes Thursday 20:15 or Sunday 13:00; a London 9:30 or a Saturday game prints
   as ESPN carries it. A game whose start is still to be announced (`startTimeTBD`) is skipped, and if
   your whole roster is on such games the line falls back to the week's first game.
4. **Ledger row 126 closes** (it was half closed at doc 380): the settlement clock and the lineup lock
   are both on the page now, both read off files.

---

## 1. WHAT WAS BUILT, AND HOW IT WAS TESTED

| file | change | pin |
|---|---|---|
| `Scripts\wire.py` | `fetch_schedule()` writes `kick` (epoch ms) and `tbd` beside week, team, opp, side, and refetches a fresh file that lacks the column; the header prints the next kickoff | 113060, `f0c75fc3866ae644` |
| `Scripts\sheet_engine.py` | `kickoffs()` and `next_lock(src, after, teams)`; `build_meta()` takes `src` and `teams` and returns `lock` and `lock_text`, and stamps `data-lock` and `data-locktext`; the inputs box's lock line; the on-open script's kickoff check | 146614, `8bbfacd2345a4c33` |
| `Scripts\lineup.py` | the header prints the next kickoff | 14296, `5b4b57da0c2f57f5` |
| `Scripts\check_kit.py` | the three pins | re-pinned |

**Tested here, on the objects production builds:** `fetch_schedule()` against a payload in the exact
shape ESPN returned this evening for KC at MIA (`{"awayProTeamId":12,"date":1790528400000,
"homeProTeamId":15,...,"startTimeTBD":false}`, which is Sunday 27 September 13:00 ET): a four-day-old
file without the column is refetched, a file with it is left alone. `next_lock()` on a synthetic
week: the roster's first lock, a roster whose only game is TBD (falls back), a build after Monday
night (none). The three pages rendered with the line and passed `check_pages.py` C5. In headless
Chromium: a page built Thursday 17:30 with a Thursday 20:15 kickoff opened Monday reads *"A kickoff
(Thursday 17 September 20:15) has passed since this page was built, so some of the lineups on it are
already locked"* and is red; a page built three minutes ago with a Sunday kickoff is quiet.

**Not run here:** the real fetch. ESPN's league-read host is refused from this container, so the
payload shape was confirmed through one read of the live endpoint and the parser tested on a copy of
it. The first real column lands at Tuesday 06:00.

**One line that is still hand-typed, and it is the schedule's caveat, not a time:** the box says
*"Kickoff times are not on file yet"* when the column is absent. That sentence is true by construction
and goes away on its own.

---

## 2. OPEN, BY NAME

- `todo_page.py` unpinned (doc 380 §5). One line in `check_kit.py`; not this batch.
- Doc 374 batch A, the vintage correction on the page: the project session's.
- JOB 4, the riser as keeper: next, doc 382.

Ledger row 157. Doc 380 §4's NOT YET RUN is closed in `threads_closed.txt`.
