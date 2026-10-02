# 380. THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT YESTERDAY: TWELVE SOURCES, NINE DATED, ONE CHANGE, AND THE CHANGE IS SHIPPED

*21 Sept 2026, 19:05 ET. Fable, running SECTION C's "THE OUTSIDE READ ON A PAGE THAT IS CORRECT ABOUT
YESTERDAY" from `Source\REDTEAM_TASKING_PROMPT.md`. The research and the build were done Saturday night;
the commit stalled on a tool error at 20:16 ET and nothing reached the drive until tonight, so every
page built on 20 and 21 Sept was built by the old code. Doc 379 is the previous number; 380 reserved
by listing the folder. No em dashes.*

---

## 0. WHAT TO DO

1. **Nothing to run.** The next `ff.bat` (Tuesday 06:00, or by hand) is the first build with the change.
   Open the week sheet afterwards: under the section nav there is a box headed **What this page was
   built from**, and the masthead says **built Tuesday 22 September 06:00 (TUE)** rather than a bare
   date. If the box is not there, the build used the old code and I want to know.
2. **The change, in one sentence: every page built from an ESPN read now says WHEN each of its inputs
   was read and WHICH run read it, and your browser writes a line when you open the page that turns
   the box red once a waiver settlement window has passed since the build.** Section 3 has the exact
   text. This is the published practice, not an invention: twelve sources, nine of them dated and three marked undated, section 2.
3. **A guard now refuses the defect:** `check_pages.py` C5 fails the run when a pull-built page carries
   no machine-readable read time. Run against the pages on the drive as of Saturday, it fires on all
   three (they had none); against pages built by the new code, it is quiet. 13 of 13 controls.
4. **Ledger row 126 moves from BLOCKED to measured, in part.** The waiver run times were "behind your
   ESPN settings page". They are in `waiver_report_2026.csv`: every settlement this season ran at
   **03:11 to 03:26 ET** (three settlements, 10, 17 and 19 Sept; n=3, observed, not ESPN's stated rule).
   The page prints that sentence off the file, so it updates itself. The lineup lock is still not on
   any page; section 5.
5. **The daily task is registered: no check needed.** `ff_log.txt` carries `======== DAILY ====` at
   07:30 on Sunday and again on Monday. The to-do item is ticked with that line as the proof.
6. **A number that must not be read as a failure:** the vintage check prints `FAILED` on every run
   now, by design (it reports, it does not correct). It printed on all six runs since Saturday.
7. **Two things queued, both mine:** the next kickoff on the inputs box (the deadline half of the
   practice), and `lineup.py`, which builds a page you read and was never pinned; it is pinned from
   tonight. Section 5.

---

## 1. THE QUESTION AND THE TESTABLE FORM

**The job:** people build decision pages on top of scheduled data pulls for a living. What is the
published practice for a page that is not wrong, but is answering a question about yesterday? Who
publishes it, what is the date on it, where do we differ, and is the difference on purpose?

**Testable form, from the job:** there is at least one dated, published practice for communicating
input freshness on a decision page that this project does not implement. **Falsifier:** "nobody
publishes this" is a legitimate result (section 4.31 is the precedent). The result: the practice is
published, repeatedly, by standards bodies and by the people who sell dashboards, and this project
implemented none of it before tonight. The falsifier holds for two of the seven practices below,
and they are reported as nulls rather than dressed up.

**The live case, restated so the table has something to be measured against.** Friday 18 Sept 23:07
Matt filed a claim. ESPN settled it Saturday 03:11. The pages on the drive had been built Thursday
17:30. Saturday morning every one of them described Friday's roster, none said when ESPN had last been
read, and nothing looked broken. The fix taken Saturday was a fifth run at 07:30 (doc 374), which
shortens the window and says nothing about it.

**What the pages said before tonight, read off the files, not from memory:**

| page | its stamp on Saturday | what it did not say |
|---|---|---|
| `WEEK_SHEET.html` | "built 19 September 2026" (a date; two builds on one day were the same page) | when ESPN was read; that every pts/wk came from a projection pulled 7 Sept 12:58; when `form_2026.csv` was rebuilt |
| `THE_WEEKLY_WIRE.html` | "Built by the scheduler, Saturday 19 September, 19:17" | that 19:17 was BY HAND, not the scheduler; the label was hard-coded |
| `LINEUP_CHECK.html` | "built by the scheduler, Saturday 19 September, 19:17" | the same |
| the sheet's footer | "Rebuilt every time the wire runs: Tuesday 6am, Thursday 5:30pm and twice on Sunday" | typed by hand; false since Saturday, when the fifth run was added |

---

## 2. THE PRACTICES, WHO PUBLISHES THEM, THE DATE ON EACH, AND WHERE WE STOOD

Every source below was loaded, not snippet-read. Dates are the ones printed on the source (B7); "undated"
means the page carries none and the fetch date is given instead.

| # | practice | publisher, date, the words | ours, Saturday | ours, tonight |
|---|---|---|---|---|
| 1 | **Stamp the read time of the data on the display, at the top, on every display that carries delayed data.** | Nasdaq, *US Equities and Options Data Policies* v2.6, 21 April 2023: *"The delay message must prominently appear on all displays containing Delayed Data, such as at or near the top of the page."* Microsoft Learn, *Add last refresh date to a Power BI report*, last updated 6 May 2025: *"it helps users understand how current the data is."* W3C, *Data on the Web Best Practices*, Recommendation 31 January 2017, BP 21: *"Humans and software agents will be able to determine when the data was last updated and whether it is suitable for their use."* | A build date on the sheet; a time labelled "the scheduler" on the other two. No input carried its own time. | **Done.** The masthead is the read time plus the run label; the box lists each input with when it was read. |
| 2 | **Stamp what period the numbers describe separately from when the page was produced.** | NWS point forecast page (forecast.weather.gov, page undated, fetched 19 Sept 2026): two stamps, *"Last Update: 4:53 pm EDT Sep 10, 2026"* and *"Forecast Valid: 6pm EDT Sep 10, 2026-6pm EDT Sep 17, 2026"*, and a third for the observation. Apache Airflow docs 3.3.2 (undated, fetched 19 Sept 2026): *"Each Dag run in Airflow has an assigned 'data interval' that represents the time range it operates in."* | Nothing. A projection pulled 7 Sept and a week-one snap share printed side by side with no label. | **Half done.** Each input carries its vintage (*a preseason projection*, *this season, measured*, *fitted on past seasons*). The "valid until" half, the next kickoff, is not printed. Section 5. |
| 3 | **A staleness threshold with two levels, warn and error, on the age of the most recent data.** | dbt Labs, *Source freshness* reference, docs.getdbt.com, last updated 16 September 2026: `warn_after` / `error_after`, *"How old the most recent data can be before a freshness check reports a warning."* Google, *The Site Reliability Workbook*, O'Reilly 2018, ch. 13: freshness SLOs of the form *"The oldest data is no older than Y."* IBM Think, *What is stale data?*, Krantz and Jonker, 14 May 2026: *"Establishing thresholds, and alerting when data exceeds them, is a foundational step."* | None. `ff.bat` writes the usage file's date to the log, and only the log. | **Done, one colour.** Red when a settlement window (03:30 ET) has passed since the build, red when the page is over a day old. No amber level. |
| 4 | **Measure staleness at the moment of USE, not at the moment of build.** | IETF RFC 9111, *HTTP Caching*, June 2022, Standards Track: *"The 'Age' response header field conveys the sender's estimate of the time since the response was generated"*; *"a 'stale' response is one where [its age has exceeded its freshness lifetime]."* IBM, 14 May 2026: *"The simplest measure of staleness is the gap between when data was last updated and when it is being used."* | None. A static page knew its build date and nothing else; the reader supplied the arithmetic or did not. | **THE CHANGE.** The browser computes the age when the page is opened and writes it under the box. This is the row the Saturday claim needed: the page built Thursday would have said, on Saturday morning, *"A settlement window (03:30 ET) has passed since, so the roster and the pool on this page can be yesterday's. Run ff.bat before you act on it."* |
| 5 | **Serve stale only when it is marked, and refuse when the source forbids it.** | RFC 9111 §4.2.4: *"a cache MUST NOT generate a stale response unless it is disconnected or doing so is explicitly permitted."* RFC 5861, May 2010: `stale-while-revalidate`, *"caches MAY serve the response ... after it becomes stale ... SHOULD attempt to revalidate it while still serving stale responses."* | Partly there already: `ff.bat` opens the sheet only if the file changed in that run, and a refused ESPN read is printed in red. But a page on the desk never refuses to be read. | **Different on purpose.** A printed page must render; refusal is not available on paper. The marking (row 4) is the substitute, and the schedule runs while the stale page is up, which is `stale-while-revalidate` in batch form. |
| 6 | **Stale is better than incorrect; never let stale look current.** | Google SRE Workbook, 2018: *"Stale data is almost always better than incorrect data."* IBM, 2026: stale data *"creates the appearance of reliability without the substance of it ... The failure is silent and cumulative rather than immediate and visible."* | The worse failure. Doc 373: a preseason 5.8 printed beside a man who had already scored 16.4, with nothing saying which vintage it was. | **Reported, not corrected.** `check_vintage.py` names the men whose rate this season refutes (ten on every run since Saturday); the page still prints the projection. Doc 374 batch A, the other session's, is the correction. |
| 7 | **State the freshness promise as a schedule.** | Tableau Cloud help, *Set a Data Freshness Policy* (undated, fetched 19 Sept 2026): *"Tableau Cloud refreshes cached data every 12 hours by default"*, with per-workbook overrides. Monte Carlo, Barr Moses, 23 December 2020: freshness is *"is my data up-to-date? What is its recency? Are there gaps in time when the data has not been updated and do I need to know about that?"* | The schedule existed (five runs) and the sheet's footer described four of them, by hand. | **Done.** The footer reads the run times off `setup_tasks.bat` through `make_commands.schedule()`, the same parser the commands page uses, so it cannot say four when the file says five. |

**Two nulls, reported as nulls.** (a) *Degrade a number to a range when its input is stale.* No source
above or in the search does this; the nearest is RFC 9111's serve-it-but-carry-its-Age, which is row 4.
Not implemented, not a defect. (b) *Print the pull time against the decision deadline.* No dashboard or
data-engineering source pairs the two; the NWS two-stamp page is the nearest published form. The
deadline half is queued (section 5), and it is a NOT YET RUN, not a BLOCKED: the schedule loader in
`wire.py` already has the kickoffs.

**Where we differ on purpose, in one line each:** no refusal on paper (row 5); the vintage defect is
reported rather than corrected until batch A lands (row 6); one red level rather than amber and red
(row 3), because the two conditions that matter to a claim are both "do not act on this page".

---

## 3. WHAT THE PAGES SAY NOW (the deliverable), AND WHAT WAS BUILT

**The masthead of the week sheet:** *The Poetry of Junkyard Juggers · built Tuesday 22 September 06:00
(TUE)*. The wire: *Read from ESPN Tuesday 22 September 06:00 (TUE).* The lineup check: *Week N · read
from ESPN Tuesday 22 September 06:00 (TUE).* The label is whatever `ff.bat` was started with: TUE, THU,
SUNam, SUNpm, DAILY, or BY HAND; a bare `py wire.py` prints *by hand*.

**The box under the sheet's section nav, built from the synthetic tree here (the times are the test's):**

> **What this page was built from**
> - **Roster, free agents and injury statuses:** ESPN, read Saturday 19 September 19:17 in this run (BY HAND). *this season, live.*
> - **Points a week, every pts/wk on this page:** the ESPN projection pulled Monday 7 September 12:58, 12 days old, divided by seventeen. *a preseason projection.*
> - **Week-one workload, snaps and target share:** form_2026.csv, written Saturday 19 September 10:23, 9 hours old. *this season, measured.*
> - **The bars, the screen rates and the seat odds:** sheet_constants.json, written Friday 18 September 07:27, 36 hours old. *fitted on past seasons, not weekly.*
> - **Waivers settle on ESPN's clock, not on this page's.** The 3 settlements this season ran at 03:11 to 03:26 ET, the last on Saturday 19 September 03:11. A page built before 03:30 and read after it can be describing yesterday's roster.
>
> *Opened 5 minutes after it was built.*

The last line is written by the browser. Opened Saturday morning on Thursday's build it reads: *Opened
2 days after it was built. A settlement window (03:30 ET) has passed since, so the roster and the pool
on this page can be yesterday's. Run ff.bat before you act on it.* and the box turns red. On paper the
line says it is blank on paper. Run in headless Chromium here on three build times: five minutes old,
quiet; Thursday 17:30, red with that sentence; a clock ahead of the build, a sentence saying the two
clocks disagree rather than a negative age.

**Every line in the box is read off a file, none is typed.** The projection's time is in its filename
(`espn_projections_2026_20260907_1258.csv`); the usage file and the constants carry their modified
time; the settlement sentence is the distinct EXECUTED minutes of WAIVER rows in `waiver_report_2026.csv`,
so the next `py waivers.py --live` updates it; the run label is `FF_WHO`, which `ff.bat` now sets from
its own argument. The one typed number is 03:30, the edge after the three observed settlements, and the
box says it is an edge.

**Files changed, all compiled on 3.12's escape check, all pinned:**

| file | what changed | pin (bytes, sha16, CRLF-normalised) |
|---|---|---|
| `Scripts\sheet_engine.py` | `build_meta`, `input_rows`, `inputs_block`, `age_line`, `settlements`, `schedule_sentence`; `render()` takes `inputs` and `sched`; `write()` passes them; the masthead stamp; the footer sentence; CSS for the box | 142876, `542881796149460a` |
| `Scripts\wire.py` | guarded import of the two helpers; the header is the read time and label, carries `data-built`, and the age line follows it | 111757, `b850ec981e78d55f` |
| `Scripts\lineup.py` | the same two edits. **Pinned for the first time**: it builds a page Matt reads and nothing checked it | 14010, `04e50d8cca32bfd3` |
| `Scripts\ff.bat` | `set FF_WHO=%WHO%` after the label is decided. CRLF preserved, checked by bytes | 6637, `d5baca9e3aaa235f` |
| `Scripts\check_pages.py` | C5: a pull-built page (the three above) without `data-built="<epoch ms>"` fails the run. Three controls added, 13 of 13 pass; run against Saturday's shipped pages it fires on all three | 12968, `4eab832761a93c77` |
| `Scripts\check_kit.py` | the five pins above and `lineup.py` added to `SCRIPTS` | re-pinned |

**Tested on the object production builds (0.2):** `sheet_engine.write()` rendered a full sheet from a
ten-man synthetic roster and the real `sheet_constants.json`; `wire.write_page()` and `lineup.page()`
each wrote their page in a tree with the new `sheet_engine.py` beside them; the new `check_pages.py`
passed all three on C5 and failed Saturday's real pages on C5. **Not run here:** `ff.bat` itself, which
is Matt's machine and ESPN. If the helpers fail on his machine the guarded imports make the cost a
missing stamp, not a missing page, and the sheet's box is wrapped so a broken row prints its own error.

---

## 4. THE THREE ANSWERS

- **TESTED:** the practice is published (seven forms, twelve sources of which nine carry a date, section 2). Four of the seven
  were absent here on Saturday; three are built tonight, one is half built, two differ on purpose, and
  two sub-practices are nulls. The guard that refuses the defect is `check_pages.py` C5, shipped and
  shown firing on the real pages first.
- **NOT YET RUN:** the next kickoff on the inputs box (row 2's second half). Testable form: the sheet
  and the wire each print *"next lock: Thursday 20:15 ET"* read off `wire.py`'s schedule loader, and the
  on-open line goes red when the page was built before a lock that has since passed. Mine.
- **BLOCKED:** nothing in this job. Row 126's second half (the lineup lock as ESPN states it) stays
  BLOCKED behind the settings page, but the kickoffs are the same thing in practice and are on file.

---

## 5. OPEN, BY NAME

- The next kickoff on the inputs box, and the red line for a passed lock: NOT YET RUN, Fable's.
- Doc 374 batch A, the vintage correction on the page itself (row 6): the project session's, not started.
- `todo_page.py` builds `MY_TODO.html` and is not pinned either; same defect as `lineup.py`'s. Not fixed
  tonight because it was not staged; one line in `check_kit.py`.
- JOB 4, the riser as keeper: written and unrun, Fable's.
- THE DIRECTIVE READ BY SOMEONE WITH NO STAKE IN IT: needs a third model or the fresh chat.

Ledger row 156. The SECTION C status box in `REDTEAM_TASKING_PROMPT.md` marks this job RUN.
