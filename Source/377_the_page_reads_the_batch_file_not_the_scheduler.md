# 377. THE PAGE READS THE BATCH FILE, NOT THE SCHEDULER, AND I QUOTED IT AS PROOF THE FILE HAD RUN

*19 September 2026, 13:00 ET. Written because Matt asked a maintenance question and the answer
required retracting something I told him four hours earlier. Population for every timing claim
below: `Scripts\ff_log.txt` as of 19 Sept 11:51 ET, 260,534 bytes, 16 run headers from 11 Sept
20:14 to 19 Sept 11:51; and `Source\waiver_report_2026.csv` as written by his 11:50 ET run, 55 rows
across weeks 1 and 2, all twelve teams' transactions. Doc 376 previous.*

---

## 0. WHAT TO DO

1. **Matt: run `Scripts\setup_tasks.bat` from an administrator prompt.** Still open. I said it was
   done and I could not have known that. Section 1.
2. **Matt: one `.\ff.bat` run.** Your 11:51 run ended `kit 1`; the five stale pins behind it are
   re-pinned, and step 7 has never executed on your Python 3.12.
3. **`py waivers.py --live` IS DONE, 11:50 ET.** Ticked, with the artifact as evidence. Section 2.
4. **A NUMBER THAT IS NOW KNOWN: your league's waivers settled at 03:11 ET Saturday and 03:26 ET
   Thursday.** Two observations, so a pattern and not yet a rule, but the 07:30 daily task lands
   after both. Section 2.
5. **A RULE, in `METHOD_TRAPS.md` as item 15: a generated page cannot prove the thing it describes
   was EXECUTED.** Section 3.

---

## 1. THE RETRACTION

Earlier today I told Matt that `COMMANDS.html` reporting a fifth scheduled task proved
`setup_tasks.bat` had run. **~~It does not, and that sentence must not be quoted again.~~**

`make_commands.py`, line 93, builds that table from *"the live schedule, parsed out of
`setup_tasks.bat`'s own schtasks lines."* **It opens the batch file and reads the text.** It never
asks Windows Task Scheduler anything. So the table is evidence that the FILE now contains five
`schtasks /create` lines, which is true because I wrote the fifth one into it this morning. It is
not evidence that any of them are registered.

**The page even labels itself wrongly**, calling a parse of a source file "the live schedule",
which is how a reader ends up believing it. That wording is now the example in the rule.

**WHAT I CAN ACTUALLY PROVE FROM THE LOG, and it is a partial answer.** `ff.bat` stamps whoever
invoked it at the top of every run. Sixteen runs since 11 Sept:

| marker | times | latest |
|---|---|---|
| `SUNam`, `SUNpm` | 1 each | Sun 13 Sept 11:45:00 and 15:30:00 |
| `TUE` | 1 | Tue 15 Sept 06:00:01 |
| `THU` | 1 | Thu 17 Sept 17:30:00 |
| `DAILY` | **0** | never |
| `BY HAND` | 12 | Sat 19 Sept 11:51:23 |

**So the ORIGINAL FOUR tasks are registered and firing, to the second.** The fifth cannot be
distinguished yet, because it was added to the file at about 11:00 this morning and fires at 07:30;
its first opportunity is 07:30 tomorrow. **The log is silent either way, which is exactly why the
status is UNKNOWN rather than "probably fine".**

**AND THE LOG IS THE FALSIFIER, so neither of us has to remember to check.** The daily task passes
the word `DAILY` to `ff.bat`. If it is registered, `ff_log.txt` gains a `======== DAILY ====` header
at 07:30 Sunday. If Sunday morning's log has no such line, the file was never run.

---

## 2. THE SATURDAY CLAIMS, WITH A TIME ON THEM

`py waivers.py --live` ran at 11:50 ET and I verified the artifact rather than the exit code:
`waiver_report_2026.csv`, 5,776 bytes, 55 rows, weeks 1 and 2, eleven team names plus his own.

**The row he was asking about is there.**

| filed | settled | what |
|---|---|---|
| 2026-09-18 23:07, PENDING | **2026-09-19 03:11, EXECUTED** | add 4702555, drop 4362478 |

That is the Coleman claim, and **it was the only transaction in the whole league at that run**. The
previous settlement in the file is 2026-09-17 03:26 ET, where four of his five claims resolved at
once: one EXECUTED, one `FAILED_PLAYERALREADYDROPPED`, one `FAILED_INVALIDPLAYERSOURCE`, one more
already-dropped.

**TWO SETTLEMENTS, 03:11 AND 03:26 ET.** Doc 374 said the fix for the Saturday blind spot was a
daily 07:30 pull and gave no reason for the hour beyond "morning". **The hour is now supported: a
07:30 pull lands about four hours after both observed settlements.** n=2, so this is a pattern and
not a rule, and it should be re-checked after two more weeks rather than written into the
environment section.

---

## 3. WHERE THE FIX WENT

Per 0.5(f), the lesson goes into the instruction that is read when the job runs, not only into the
ledger. This one is a test-design failure, so it goes to `METHOD_TRAPS.md`, which now carries it as
item 15 under **C. WHAT COUNTS AS AN ANSWER**:

> **A generated page cannot prove that the thing it describes was EXECUTED. Ask what the builder
> READ.** Evidence for "it ran" is something the RUN wrote and nothing else could have written: a
> log line, an output file's timestamp, a row only that run produces.

**This is section 0.2's exit-code rule one level out.** There the mistake is checking the return
value instead of the artifact. Here the artifact WAS checked, and it was the wrong artifact: a page
downstream of the input rather than downstream of the run. The same shape will appear anywhere a
generated page describes a thing it also reads from, and `COMMANDS.html` describes eleven of them.

**THE OTHER HALF IS THE TRACKER, AND IT IS THE REASON THE QUESTION AROSE AT ALL.** Matt's list
showed `[ ]` against two items he had already done, because nothing ticks an item off when the work
happens. He read the list as a run queue, which is the only sane reading of it. `matt_todo.txt` now
opens with a dated block naming the two live commands and the one dated for Tuesday, and saying
plainly that the rest is done, dated or read-only. **That is a caption on the defect, not the fix.
The fix is doc 374 batch F and it is still NOT YET RUN.**

---

## 4. OPEN

- **[OPEN] NOT YET RUN -- batch F**, the trackers. The to-do file records asks and never
  completions; `open_threads.py` still scrapes its own output. Owner: me. **This doc is the second
  time in two days that its absence cost a round trip.**
- **[OPEN] BLOCKED -- whether `setup_tasks.bat` has been run.** Exact missing input: the output of
  `schtasks /query /tn "FF2026 - 5 daily post-waiver"` on Matt's machine, or a `DAILY` header in
  `ff_log.txt`. Where it would come from: the 07:30 Sunday firing, or a shell on that machine.
  Tried: yes, the log and the commands page, and neither can answer it today.
- Carried from doc 376 and unchanged: batch A, widened by doc 375; batches B, E, F;
  `make_online.py` not on the drive; `LINEUP_CHECK.html` kickoff times blocked on a schedule column.

*Sources: `Scripts\ff_log.txt` (16 run headers, 11 to 19 Sept); `Scripts\make_commands.py` line 93
and its docstring; `Scripts\setup_tasks.bat` lines 46 to 57; `Source\waiver_report_2026.csv` (55
rows, written 19 Sept 11:50 ET); `Source\METHOD_TRAPS.md`; docs 144, 374, 375, 376.*
