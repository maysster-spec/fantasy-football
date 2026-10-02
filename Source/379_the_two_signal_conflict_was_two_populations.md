# 379. THE TWO-SIGNAL "CONFLICT" WAS TWO POPULATIONS: 38% AND 7.1% ARE BOTH RIGHT, NEITHER IS SCHULTZ'S FORECAST, AND THE PAGE NOW SAYS SO

*19 Sept 2026, 20:20 ET. Fable, running SECTION C's "WHICH INSTRUMENT GOVERNS A TWO-SIGNAL PLAYER" from
`Source\REDTEAM_TASKING_PROMPT.md`, the job doc 378 said to run next. Also in this doc, because they were
found on the way: what tonight's `ff.bat` and this morning's `py waivers.py --live` produced, a defect in
`setup_tasks.bat` that told Matt to delete the task it had just created, and handover v9 for the fresh
chat. Doc 378 is the previous number; 379 reserved by listing the folder. No em dashes.*

---

## 0. WHAT TO DO

1. **A number to reinstate: Schultz at 38% was never wrong.** Doc 371 item 2 said *"A number that must
   not be quoted: Schultz at 38%"* because §4.30 says 7.1% for two signals. The two rates are measured on
   different men, different signals, different outcomes and different horizons, and the one that applies
   to a week-one workload man is the 38% (doc 308, n=45, 95% interval 25% to 52%). §4.30's 7.1% is a
   next-season rate for receivers in NFL years one to three with pedigree signals; Schultz, a veteran
   tight end scored on week-one usage, is not in that population at all. Section 1.
2. **The page changed, not the measurement: every screen rate on `WEEK_SHEET.html` now prints its
   population, n and horizon on the row, and the words "a rate over that group, not his own forecast".**
   `sheet_engine.py` edited, re-pinned in `check_kit.py`; the exact string is in section 2. It shows on
   the next `.\ff.bat`.
3. **`setup_tasks.bat` told you to delete the fifth task it had just created.** Its "WHAT EXISTS NOW"
   block still queried four names and printed *"EXPECTED: EXACTLY four ... Any fifth name is a
   duplicate: delete it"*. Fixed and re-pinned. **If you ran it and followed that line, re-run it once as
   administrator; it is safe twice.** The ten-second check either way is on your list. Section 3.
4. **Confirmed from the files: `.\ff.bat` ran at 19:17 ET tonight** (kit PASS, pages OK, and the vintage
   check named ten men whose preseason rate this season already refutes, which is the guard doing its
   job, not a failure). **`py waivers.py --live` ran at 11:50 ET** and its file shows your Coleman claim
   filed 18 Sept 23:07 and EXECUTED 19 Sept 03:11 ET. Whether `setup_tasks.bat` registered the daily task
   is not visible in any file (doc 377); the first proof will be a `DAILY` line in `Scripts\ff_log.txt`
   at 07:30 Sunday. Section 3.
5. **Start the fresh Opus chat by pasting `Source\00_START_HERE.md`, now version 9.** Agreed that it is
   needed; the reasons and the new chat's first three jobs are in section 4.
6. **A queued job is now closed and one is re-scoped:** WHICH INSTRUMENT GOVERNS A TWO-SIGNAL PLAYER is
   RUN (this doc). Doc 374's batch B ("a base rate may not wear a player's name") was waiting on it and
   is now a guard-only job: the string is fixed, what remains is `check_pages.py` refusing a rate beside
   a name without its group. Still the project session's.
7. Nothing else to run.

---

## 1. THE FALSIFIER WAS THE RESULT, AND THE JOB SAID TO TEST IT FIRST

**Testable form, from the job:** the two-of-three rate has a confidence interval that excludes at least
one of 38% and 7.1%. **Falsifier, fixed first:** if the two numbers are measured on different populations
and each is correct for its own, there is no arithmetic conflict and the defect is a label.

| | the week sheet's 38% | §4.30's 7.1% |
|---|---|---|
| measured in | doc 308, `wk1_wr_composite.py` | doc 248 |
| population | every WR and TE, 2022 to 2025, who played week 1 with 1+ target, was BELOW his position's replacement rate the prior season, and played 4+ of weeks 2 to 14; **n=517** | WR seasons 2021 to 2024, NFL years 1 to 3, not startable that season, 4+ games, and 4+ games the next season; **n=185** (152 with complete data) |
| the three signals | week 1: 8+ targets, 80%+ of team snaps, 20%+ of team targets | career: NFL rounds 1 to 3, yards per target over 7.13, targets per game over 3.20 |
| outcome | half-PPR ppg over weeks 2 to 14 reaching WR 9.62 / TE 8.25 | startable the FOLLOWING season |
| base rate | 13.9% | 11.4% |
| two of three | **17 of 45 = 37.8%, 95% interval 25% to 52%** | **4 of 56 = 7.1%, 95% interval 3% to 17%** |
| three of three | 13 of 31 = 41.9% [26%, 59%] | 13 of 33 = 39.4% [25%, 56%] |
| shape (0.5a3) | **substitution**: 6 → 19 → 38 → 42, the jump is one signal to two | **compounding**: 0 → 5 → 7 → 39, the jump is two to three |
| does Schultz belong to it | yes: TE, played week 1 with targets, below the TE bar in 2025 | no: he is not a receiver in years 1 to 3 |

**The intervals do not overlap, and that is not a conflict, because they are intervals on two different
quantities.** Doc 308 said this in terms when it shipped the screen (*"do not port 4.30's 'you need all
three' across"*), and `sheet_constants.json`'s own `workload_note` says *"A DIFFERENT POPULATION FROM every
other rate in this block and it must never be compared with them (0.6)"*. Doc 371 compared them. That is
a population error of the kind 0.6 exists for, and it is the fourth "number read off a page without its
population" in the same twenty-four hours, this time by the red team rather than the page.

**The direction, since the job asked:** both directions are real and they belong to different objects. A
week's workload is three views of one thing, so the second view adds most and the third little
(substitution). Pedigree, efficiency and volume are three near-independent facts, so the third multiplies
(compounding). Doc 308 measured exactly this and named it.

**One sentence, as the deliverable asked: this was a labelling failure, not a measurement conflict.**

---

## 2. THE STRING THE PAGE PRINTS NOW (deliverable), AND WHY IT IS ON THE ROW

Before, beside Schultz and Mayer alike:

> *He was on the field and being thrown at in week one, and 38% of the men who do become startable.
> That is worth about 29 points to your lineup over the 6 weeks a hit lasts, 4.6 a week, ...*

After, from the same `sheet_engine.py` line, using the n the constants already carried:

> *He was on the field and being thrown at in week one, and 38% of the 45 men who cleared two of the three
> week-one marks (NFL-wide, 2022 to 2025) reached the starting bar over weeks 2 to 14. That is a rate over
> that group, not his own forecast. It is worth about 29 points to your lineup over the 6 weeks a hit
> lasts, 4.6 a week, ...*

The other screens get their own group in the same sentence: the pedigree screen's 33% now reads *"of the
24 men this league added on the same three signals (2022 to 2025) were startable from the add week to
week 14"*, which is the sheet's in-season measurement on this league's adds, not §4.30's 39.4%. The
"11.1 points, expected" pill is unchanged: it is 29.3 if he hits times the group's rate, and the sentence
under it now says whose rate.

**Where it was and what changed:** `Scripts\sheet_engine.py`, the bet-lane `line` string (about line
1617) plus a `POP` dict beside `SAYS`. Compiles clean with warnings as errors on 3.12's escape check,
which also turned up one pre-existing invalid escape in a docstring (`2026\COMMANDS.html`, line 464,
section 0.4's rule); fixed in the same edit. `check_kit.py` re-pinned for `sheet_engine.py` and
`setup_tasks.bat`. Not run here: `ff.bat` is Matt's machine. The next run is the test, and the negative
control is that Schultz's row must read "of the 45 men".

---

## 3. WHAT THE FILES SAY ABOUT TONIGHT'S COMMANDS

**`.\ff.bat`, 19:17 ET, from `Scripts\ff_log.txt`:** kit `PASS: canonical tree matches the manifest`;
`check_pages` no problems on all six pages; vintage check `FAILED -- 10 printed rate(s) this season
already refutes` (Jeanty 14.5 against 29.7, Vele 5.8 against 16.4, Adams 11.7 against 4.1, Pickens,
Nacua, Dowdle, Freiermuth, Judkins, Shaheed, Dobbins). **That FAILED line is the expected outcome**: the
check reports, it does not correct (doc 374 batch A), and the ten names are the ones to read the sheet
with in mind. `RESULT: BY HAND -- lineup 0, wire 0, to-do 0, commands 0, kit 0, vintage 1, pages 0.` The
run was by hand: 19:17 is none of the scheduled minutes.

**`py waivers.py --live`, 11:50 ET:** `Source\waiver_report_2026.csv` rewritten as one row per event, 55
rows, weeks 1 and 2, statuses EXECUTED 25 / PENDING 13 / CANCELED 9 / FAILED 8. A claim appears twice,
once PENDING when filed and once EXECUTED at the run. **Your Coleman claim: filed 18 Sept 23:07, EXECUTED
19 Sept 03:11 ET, add 4702555 drop 4362478.** The 19:17 roster carries Coleman and not Demercado.
Handover section 6 now says to count the EXECUTED row.

**`setup_tasks.bat`: not knowable from files, and the script itself was working against you.** The
schedule lives in Windows Task Scheduler, which no file here reads (doc 377). The script's own output
block queried four names and told you a fifth was a duplicate to delete. Fixed: it queries five, says
five, and its header lists the fifth. **Ten-second check on your machine, on your list:**
`schtasks /query /tn "FF2026 - 5 daily post-waiver"`. If it prints a Next Run Time, done. If it says the
system cannot find the file, run `Scripts\setup_tasks.bat` once more as administrator. Either way the
first proof that costs you nothing is a `======== DAILY ====` line in `ff_log.txt` at 07:30 Sunday.

---

## 4. THE FRESH CHAT: YES, AND HERE IS WHAT IT GETS

**Agreed, for a measured reason and not a feeling.** The old chat wrote four wrong takes in twenty-four
hours (docs 368 to 373) and its own doc 373 traced all four to one habit. Since it opened, the directive
has changed twice (v9.8, v9.9) and the resident set it was reading is not the one in the project now. A
long chat's recall of its own instructions falls as it fills (doc 366's outside sources), and the fix for
that is a new window, not a better reminder.

**What it gets: one paste, `Source\00_START_HERE.md` version 9**, 3,313 words. Version 8 was 2,929 and
the ratchet argument in `FABLE_HANDOVER_TEST.md` part E stands; the four additions are the take contract
(section 7), the fifth scheduled run and the vintage check (sections 1 and 5), the transaction file's new
shape (section 6) and the second model's queue (section 9). Each closes a way the new chat would have
been wrong on its first day. The regression test on the paste (doc 367 item 5) is still not run, so the
new chat's first job is to be that test.

**Its first three jobs, in order, and none of them is Matt's:** (1) the regression probes on the v9.9
paste, the two fileless probes plus Part A of the handover kit, scored the same way as doc 365; (2) the
guards doc 378's last line names, `check_pages.py` refusing a rate beside a name without its group and
`todo_page.py` refusing a take line without the five lines under it, negative controls first; (3) doc 366
item 4, the to-do split into tasks and notes with a status field, which this week's scoring hit again.
Not its job and not Fable's: SECTION C's last job, the directive read by someone with no stake in it,
because both of us have now written parts of it.

---

## 5. OPEN, BY NAME

- THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT YESTERDAY: queued, Fable's, web research, not started.
- JOB 4, the riser as keeper: written and unrun, Fable's.
- THE DIRECTIVE READ BY SOMEONE WITH NO STAKE IN IT: needs a third model or a reader that has written
  none of it.
- `check_pages.py` rate-without-group rule and `todo_page.py` take-line rule: the project session's, not
  started (doc 378 last line).
- The regression test on the v9.9 paste: the fresh chat's first job.

Ledger rows 154 and 155.
