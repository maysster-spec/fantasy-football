# 76 — DRAFT-NIGHT AUTOMATION: WHAT TO SCHEDULE AND WHAT NOT TO

**Aug 29, 2026.** Answers the "put it all in Task Scheduler" question.
**Headline: two scheduled tasks, not five. And the HTML already opens itself.**

---

## 1. TWO CORRECTIONS FIRST

**(a) `live_board.html` DOES launch on its own.** `live_draft.py` line 229 calls
`webbrowser.open()` immediately after the engine loads. No task, no batch step needed.

**(b) …but NOT in `--replay` mode.** The replay path returns at line 227, before the browser call.
**During the weekend test you must open `live_board.html` yourself**, or you will conclude the
replay failed when it worked. This is not documented anywhere else.

## 2. WHY NOT FIVE SEPARATE TASKS

The tempting design is one task per step: pull, keepers, swap, inject, launch. It is wrong here.

Every step depends on the one before it, and **Task Scheduler has no notion of "the previous step
succeeded."** If `keeper_swap` fails at 7:05 and `live_draft.py` launches on schedule at 7:55, the
tool comes up on a stale board, prints normal-looking output, and drafts all night against the
wrong player pool. That is the exact silent-failure class this project has found twenty-three
times. Independent timers convert a loud failure into a quiet one.

**One batch file, run once, in order, with a human gate at each irreversible step.** The gates are
cheap — Matt is sitting there anyway — and they are the only thing standing between a failed step
and a ruined draft.

## 3. THE PLAN — exactly two tasks

| # | when | task action | what it does |
|---|---|---|---|
| **1** | **Sat Sep 5, 8:00 AM** | `G:\My Drive\_Fantasy\2026\Scripts\refresh_pull.bat` | re-pulls 2026 projections with the mandatory flags, logs to `pull_log.txt` |
| **2** | **Mon Sep 7, 6:55 PM** | `G:\My Drive\_Fantasy\2026\Scripts\draft_night.bat` | the whole sequence: verify tree → fetch keepers → swap board → inject prerank → launch live board |

Nothing else gets a timer.

### Creating both in one pass (Task Scheduler, ~4 minutes)

1. Win+R → `taskschd.msc` → Enter.
2. Right pane → **Create Basic Task**.
3. Name `FF 2026 - Sept 5 projection pull` → Next.
4. Trigger **One time** → Next → date **9/5/2026**, time **8:00:00 AM** → Next.
5. Action **Start a program** → Next → Program/script:
   `G:\My Drive\_Fantasy\2026\Scripts\refresh_pull.bat` → Next → Finish.
6. **Create Basic Task** again. Name `FF 2026 - DRAFT NIGHT` → Next.
7. Trigger **One time** → Next → date **9/7/2026**, time **6:55:00 PM** → Next.
8. Action **Start a program** → Next → Program/script:
   `G:\My Drive\_Fantasy\2026\Scripts\draft_night.bat` → Next → Finish.
9. For **both**: double-click the task → General tab → confirm **"Run only when user is logged
   on"** is selected. This matters — the ESPN cookies live in your user profile's browser session
   context, and a task running as SYSTEM has a different environment.

**Test both by right-clicking → Run, today.** A scheduled task that has never been executed is not
a scheduled task — same rule as a guard that has never fired.

## 4. THE KEEPER STEP — now automated, with a manual escape hatch

`fetch_keepers.py` is new. After the 7:00 PM lock it reads the 12 actual keepers off ESPN and
writes `actual_keepers.csv` in the format `keeper_swap.py` expects (which only needs a `Player`
column — team names are cosmetic).

```
py fetch_keepers.py --dry      # show what ESPN reports, write nothing
py fetch_keepers.py --write    # archive the old file, write the new one
```

It tries `view=mRoster` first (pre-draft, a keeper team's roster should hold exactly its keeper),
then falls back to `view=mDraftDetail` (doc 58: ESPN carries the 12 keepers inside the pick feed).

**It refuses to write unless it finds exactly 12.** A partial file is worse than none — it would
make `keeper_swap.py` rebuild the board against the wrong set, silently. On refusal, `draft_night.bat`
opens `actual_keepers.csv` in Notepad and the manual path takes over.

**[UNTESTED — this is the one thing here that has never run.]** Nobody has confirmed which ESPN
view exposes pre-draft keepers, because the lock has not happened. **Run `py fetch_keepers.py --dry`
this weekend.** It will almost certainly report 0 rows now, and that is fine — what you are checking
is that it authenticates and fails cleanly rather than throwing. If it 401s, the cookies are stale
and that is worth knowing nine days early, not at 7:02 PM.

## 5. WHAT IS STILL ON MATT'S PLATE AFTER ALL THIS

1. **Confirm `teamId=9`** — open the ESPN team page, read the number after `teamId=`. Still the
   highest-consequence unverified thing in the project.
2. **The weekend test kit** — injector twice, replay, ESPN UI check. ~15 minutes.
3. **Print three sheets** before Sept 7: `DRAFT_CARD`, `FALLBACK_BOARD`, `INJURY_CONTEXT_SHEET`.
4. **Right-click `Scripts\live_draft\` → "Available offline"** in Google Drive, so a sync stall
   cannot hang a 60-second pick. Untested, free, no downside.
5. **Sit at the machine at 6:55 PM.** The batch file has gates; it is not a robot.

That is the whole list. Everything else is now scripted.
