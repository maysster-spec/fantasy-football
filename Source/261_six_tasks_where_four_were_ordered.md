# 261 — Six tasks where four were ordered, and the delete that was piped to nul

**Date:** 2026-09-09
**Trigger:** Matt sent `task sched.jpg` — his own Task Scheduler window — and said *"OK, i didn't
run as admin."*
**Method note:** this is §0.5(d)'s milestone rule working as designed — **verify the ARTIFACT,
never the exit code.** `setup_tasks.bat` printed four SUCCESS lines. The window is the artifact,
and the window says something the SUCCESS lines could not.

---

## 1. WHAT THE WINDOW SHOWS

**The four tasks registered correctly, and the trigger that failed twice under PowerShell is
present:**

| task | trigger | next run |
|---|---|---|
| FF2026 - 1 Tue wire | Tue 06:00 weekly, from 9/9/2026 | 9/15/2026 6:00 AM |
| **FF2026 - 2 Thu lineup** | **Thu 17:30 weekly, from 9/9/2026** | **9/10/2026 5:30 PM** |
| FF2026 - 3 Sun early | Sun 11:45 weekly, from 9/9/2026 | 9/13/2026 11:45 AM |
| FF2026 - 4 Sun late | Sun 15:30 weekly, from 9/9/2026 | 9/13/2026 3:30 PM |

**The Thursday occasion is on the board with its own Next Run Time.** That is the thing that
silently went missing twice under `setup_tasks.ps1`, and it is the whole reason the design was split
into four separately-named tasks. `[SOURCED: Matt's Task Scheduler window, 2026-09-09]`

**`Last Run Result 0x41303` on all six is NOT an error.** It is Task Scheduler's literal *"the task
has not yet run"*, paired with the null sentinel `11/30/1999 12:00:00 AM` in Last Run Time. Correct
state for a task created today whose first trigger has not arrived.

## 2. AND TWO OLD TASKS SURVIVED THE CLEAN-UP

**`FF2026 - Tuesday wire`** (Tue 06:00, from 9/8/2026) and **`FF2026 - Lineup check`** (multiple
triggers defined, next run 9/10/2026 5:30 PM) are both still in the list.

**Both are named in `setup_tasks.bat`'s own delete list. Both were supposed to be gone.** And they
collide exactly:

| when | the new task | the survivor |
|---|---|---|
| Thu 9/10, 5:30 PM | FF2026 - 2 Thu lineup | FF2026 - Lineup check |
| Tue 9/15, 6:00 AM | FF2026 - 1 Tue wire | FF2026 - Tuesday wire |

**This is not cosmetic.** Both call `ff.bat`, which runs `lineup.py --html` and `wire.py --html` and
appends to one log. Two of them at the same minute means **two processes writing
`LINEUP_CHECK.html`, `THE_WEEKLY_WIRE.html` and `ff_log.txt` concurrently** — a half-written page,
interleaved log lines, or a failure that reads like ESPN refusing. The first Thursday of the season
was going to be the test.

**And `FF2026 - Lineup check` is the OLD one-task-many-triggers design** — "Multiple triggers
defined" is right there in the Triggers column. The design §0.1(f)'s case study was written about is
still live on his machine.

## 3. THE CAUSE, AND IT IS CONFIRMED BY HIM, NOT INFERRED

**Matt: *"OK, i didn't run as admin."*** That closes it without a guess (§0.2 — a diagnosis is a
claim and must be tested before the fix is written; here the claim was tested by the operator).

Non-elevated `schtasks` **can create** a task that runs as the current user — which is why all four
appeared. It **cannot delete** a task registered under a different context — which is why the two
older ones refused. The two halves of the same script had different privilege requirements and
nothing said so.

**WHY IT WAS INVISIBLE, AND THIS IS THE ACTUAL DEFECT:**

```
) do schtasks /delete /tn %%T /f >nul 2>&1
```

**Both streams to nul.** A delete that was refused for lack of elevation looked byte-for-byte
identical to a delete that worked. **§0.2's "an exit code is not a result" in its cheapest possible
form — the result was not even collected.** The script then printed four confident SUCCESS blocks
for the things it had created and said nothing about the two it had failed to remove.

**§0.5(c)5 again, and this is the general lesson:** the verification block at the end of
`setup_tasks.bat` queried **the four names it expected to find**. A check that looks only for what
*should* exist can never see what *should not*. Same shape as MarShawn Lloyd missing from a
180-row printed cut.

## 4. SHIPPED

`Scripts\setup_tasks.bat`, **2,882 → 4,697 bytes**. Old copy archived to
`2026\_archive\setup_tasks_20260909.bat`. Pure `cmd`, no dependencies (§0.4).

1. **The delete loop now reports.** A new `:killtask` subroutine prints `deleted` / `not there` /
   `*** REFUSED` per name, and on a refusal **re-runs the delete un-silenced so schtasks' own error
   text lands in the window.**
2. **The run ends by listing EVERY task whose name contains FF2026** —
   `schtasks /query /fo LIST | findstr /i "FF2026"` — with the expected count stated as four and
   the delete command for any fifth. That is the missing-row check pointed at leftovers.

**`check_kit.py`, 23,035 → 23,704 bytes: `setup_tasks.bat` and `ff.bat` are PINNED for the first
time.** Doc 146's argument, one season later — setup_tasks.bat registers the entire weekly schedule
and ff.bat is what all four tasks actually run, unattended, from here to week 14, with nobody
watching the window. Sizes and hashes were taken **from the files on his drive after the commit**,
not from a container copy, because a false STALE at the wrong moment is the doc-168 failure that
trains you to wave the checker through.

## 5. WHAT MATT DOES

**Re-run `setup_tasks.bat` from an ADMIN Command Prompt.** It is idempotent, and this time the
deletes will either say `deleted` or print the exact reason they could not. The FF2026 listing at
the end must show **four names and no more**.

## 6. OPEN, NAMED (§0.5a4)

- **Three pins were already stale before today and check_kit had been reporting it into a report
  nobody read** — `draft_night.bat` (pinned 6,405 / on drive 6,560) and `sept5_after.bat`
  (pinned 9,173 / on drive 9,389), alongside doc 260's `waivers.py`. **NOT YET RUN:** one
  `py check_kit.py` says whether those two are legitimate post-draft edits needing a re-pin, or
  drift. Do not re-pin either blind.
- **Whether the duplicate pair ever actually double-ran** — no, by construction: the survivors'
  first collision is Thursday 9/10 and today is 9/9. Nothing to recover.
