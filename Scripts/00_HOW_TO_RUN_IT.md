# HOW TO RUN IT — every command, by the situation you are in

**Rebuilt 2026-09-01. Replaces the Aug 26 version in full.**

**Two folders. Only one script lives in the second one.**

```powershell
cd "G:\My Drive\_Fantasy\2026\Scripts"              # everything below unless it says otherwise
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"   # live_draft.py ONLY
```

**PowerShell rule: any URL goes in double quotes.** Unquoted, PowerShell splits the command at the
first `&` and treats `{ }` as a script block.

---

## A · DRAFT NIGHT — Monday Sept 7

| when | command | from |
|---|---|---|
| **7:00 PM** — the whole lock sequence, gated, 5 steps | `.\draft_night.bat` | Scripts |
| 7:55 PM — start the board | `py live_draft.py` | **live_draft** |
| if the board dies | reopen `live_board.html`, or re-run `py live_draft.py` — it holds no state and re-reads every pick | live_draft |
| if the board is wrong or frozen | use the printed **DRAFT_BOARD** and keep drafting | — |

**`py live_draft.py` takes no arguments on draft night.** League 21985, team 9 and slot 8 are all
built in, and it now verifies the slot against ESPN's published draft order before pick 1.

**What `draft_night.bat` runs, if you ever need the steps by hand:**

```powershell
py check_kit.py                      # 1/5  the files are the right files
py fetch_keepers.py --dry            # 2/5  what ESPN says the 12 keepers are
py fetch_keepers.py --write          #      accept it
py keeper_swap.py --check            # 3/5  does the board need rebuilding
py keeper_swap.py --write            #      rebuild it
py board_audit.py                    # 3b   the rebuilt board is still arithmetically right
py espn_draft_injector_Gemini.py     # 4/5  push the prerank to ESPN
py verify_prerank.py                 #      read back what ESPN actually stored
```

---

## B · SOMETHING IS WRONG WITH THE LIVE BOARD

| symptom | command |
|---|---|
| it says something you do not believe | `py live_draft.py --probe` |
| a 404, or "cookies?" | `py live_draft.py --probe` — it tests the same cookies against league 21985 and tells you which is broken |
| cookies really are stale | `py cookie_jar.py` (from **Scripts**), then re-run |
| you want the raw truth | `Scripts\live_draft\feed_evidence\` — every run saves ESPN's first reply and its first failure |

---

## C · REHEARSING

**Rehearse the TOOL — no ESPN, nothing written, this is the tested lane:**

```powershell
py rehearsal.py --realtime              # 8s a pick, ~25 min, holds 25s on your picks
py rehearsal.py --realtime --from 60    # start 60 picks in
py rehearsal.py --pace 0.5              # fast: the whole draft in ~90 seconds
```

**Rehearse against ESPN's PRACTICE DRAFT — this works now. [doc 209, corrects doc 126.]**

Doc 126 said don't, and it was right at the time: ESPN's read API serves a practice room's
opening state and never its live picks. That stopped mattering the day the bridge went in
(doc 137). The picks come out of the **browser**, and the extension matches all of
fantasy.espn.com — so a practice room is hooked exactly like the real one.

Three windows, same as draft night, plus one flag:

```powershell
# window 1 -- the listener, leave it open
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"
py bridge_server.py

# window 2 -- Chrome: click Practice Draft on the league page, leave the room open

# window 3 -- the board
py live_draft.py --bridge --mock
```

**`--mock` is not optional.** It turns off keeper depletion and keeper-row detection. A practice
room has no keepers in it; without the flag the board runs 12 picks ahead of the room all night
and says nothing about it (doc 149).

**How to tell:** if George Pickens is sitting in the practice room's available pool, that room has
no keepers and `--mock` is correct. If the twelve kept players are already gone, drop `--mock`.

**IT ALWAYS HAS A DIFFERENT leagueId, AND YOU MUST RESTART THE LISTENER FOR EACH ROOM.
[doc 210 — both learned the hard way on Sept 7.]** ESPN mints a new practice league every time:
four rooms in seventeen minutes had four different ids. And `bridge_server.py` clears its pick file
when **it** starts, not when a room opens — so room 2's picks pour into room 1's file, dedupe by
player id keeps the FIRST one, and a player you drafted stays on someone else's roster with nothing
said. That is exactly what happened. **Ctrl+C the listener, run it again, then open the new room.**

Read the leagueId out of the address bar and pass the room's own URL, **in quotes** (PowerShell
splits on `&`):

```powershell
py live_draft.py --bridge --mock --url "https://fantasy.espn.com/football/draft?leagueId=XXXX&seasonId=2026&teamId=N"
```

And if ESPN's read API refuses that league id, give the shape yourself and it skips ESPN entirely:

```powershell
py live_draft.py --bridge --mock --slot 8 --teams 12
```

---

## D · SEPT 5 — the T-48h refresh

```powershell
.\refresh_pull.bat        # re-pull projections and ADP, gated; writes pull_log.txt
py sept5_check.py         # the verdict: FREEZE or REBUILD
.\sept5_after.bat         # 5 gated steps if it says REBUILD
```

`sept5_after.bat` runs: `refresh_adp.py --write` → `board_audit.py` → `depth_map.py` →
`make_sheets.py` → `make_fallback.py`.

---

## E · THE BOARD AND THE PAPER

```powershell
py make_board.py             # THE board: one list, 180 players, everything on the row
py make_prerank.py           # audit: is the prerank telling you to reach?
py make_prerank.py --write   #        rebuild it -- then RE-INJECT, or ESPN never sees it
py depth_map.py              # who is behind whom, and how open the job is
py make_sheets.py            # the three companion sheets
py make_fallback.py          # the old-style paper board
.\sync_desk_copies.bat       # dated copies to the 2026 desk, old ones swept
```

**Run these in order after ANY board change:** `depth_map.py` → `make_board.py` → `sync_desk_copies.bat`.

---

## F · PUTTING INFORMATION IN

```powershell
py apply_news.py                          # audit a news override (a player ruled out)
py apply_news.py --write                  # apply it
py import_injury_sweep.py sweep.csv       # audit a Gemini injury sweep
py import_injury_sweep.py sweep.csv --write
py parse_takes.py ..\10_Gemni\*.md --write   # fold analyst sweeps into the board and the cards
py my_take.py "Player Name" up "why"      # one take
py my_take.py --file                      # a whole sheet: my_takes.csv
py my_take.py --list                      # what you have said
```

---

## G · ASKING QUESTIONS OF THE DATA

```powershell
py delta_gaps.py             # where the board and the market disagree with no analyst on file
py delta_gaps.py --prompt    # write the Gemini tasking file for those 20
py delta_gaps.py --wide      # the 85 players nobody has said anything about
py waiver_study.py           # your own waiver hit rate, by position
py board_audit.py            # 39 checks: does the board say the right things
py check_kit.py              # are the files the right files
```

---

## H · HOUSEKEEPING

```powershell
py tidy_docs.py              # dry run: retire superseded docs
py tidy_docs.py --move
py tidy_docs.py --root       # dry run: tidy the 2026 desk
py tidy_docs.py --root --move
py tidy_duplicates.py        # find the same file living in two places
```

---

## THE FIVE THAT MATTER MOST

1. `py check_kit.py` — before anything, and at 7:55 PM.
2. `py live_draft.py` — draft night. No arguments.
3. `py live_draft.py --probe` — when the board says something you do not believe.
4. `py rehearsal.py --realtime` — the only honest rehearsal of the tool.
5. `.\draft_night.bat` — the 7:00 PM sequence, so nothing is remembered under pressure.
