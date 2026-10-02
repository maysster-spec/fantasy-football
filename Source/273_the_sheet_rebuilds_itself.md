# 273 — The sheet rebuilds itself

2026-09-10. Matt: *"what to look for each week will change because people will drop players. this
means that I'm not going to be able to do all those calculations week to week. what is our plan for
doing those week to week? is it running that waiver script that you wrote or is it something else.
how am I going to receive these week to week waiver period to waiver recommendations?"*

**He is right that the sheet as delivered was a photograph.** Docs 268–272 computed everything in a
chat session, against a pool snapshot, and wrote the answers into a page. The moment another manager
drops somebody, that page is describing a league that no longer exists — and every number in it was
in my container, not on his machine. That is the §0.4 failure in its most durable form: not one task
handed back, but a whole weekly job that only runs when he asks for it.

---

## The plumbing already existed, and nobody had noticed

Four scheduled tasks have been on his machine since 2026-09-09:

| task | when | runs |
|---|---|---|
| FF2026 - 1 Tue wire | Tuesday 06:00 | `ff.bat TUE` |
| FF2026 - 2 Thu lineup | Thursday 17:30 | `ff.bat THU` |
| FF2026 - 3 Sun early | Sunday 11:45 | `ff.bat SUNam` |
| FF2026 - 4 Sun late | Sunday 15:30 | `ff.bat SUNpm` |

`ff.bat` runs `lineup.py --html` and `wire.py --html`, then **checks the artifacts rather than the
exit codes** and logs the result. It has been rebuilding `THE_WEEKLY_WIRE.html` and
`LINEUP_CHECK.html` four times a week the whole time.

**So the answer to "what is the plan" is not a new script and not a new schedule.** It is that the
arithmetic was never in the thing that already runs. The fix is to put it there.

---

## What shipped

**`Scripts\sheet_engine.py`** — the calculation and the page, standard library only.

- `bar_grid(roster)` solves, by bisection against the same best-legal-nine used everywhere in this
  project, **the rate a new player at each position must beat to change the starting nine, week by
  week.** The grid cannot drift from the model because it is solved *from* the model.
- `price(candidate, bar)` is the whole rule: `sum over weeks of max(0, his rate − the bar)`,
  skipping his bye.
- `rates(src)` reads **the newest projection pull, not the board** — deliberately. The board carries
  no kicker and no defence rows by design, and a bar grid missing two of the nine slots would price
  them silently at zero. §4.23(c) verified the pull's `proj_2026` is the same league-scored quantity
  (r=0.9925), so one source serves all nine slots.
- `render(...)` writes the page: the bar grid, the six best free bodies at every position with their
  week-by-week gain and a season total, the rival-shortage map, his roster, and the standing rules.

**Three negative controls run before it shipped**, because a guard that has never fired is not a
guard (§0.2): an **empty roster** raises rather than writing a sheet with no bar; a **missing
projections folder** returns *"no espn_projections_2026_*.csv in Source"*; a **missing constants
file** returns *"sections 3 and 5 are missing, not empty."* And a positive control: on his real
fourteen the engine reproduces the season total to **1865.8** and prices Boswell at **+10.20**,
Strange at **+8.10**, Daniel Jones at **+0.00** — the same numbers docs 268 and 270 published.

**`Source\sheet_constants.json`** — the fitted numbers that do **not** change week to week: the two
potential distributions (docs 269), the rival-shortage map (doc 271), the kicker slope and swap gain
(doc 272), the free defence partners (doc 267), and the seven standing rules in plain English.
Everything else on the page is recomputed from ESPN on every run. **When research changes a
constant, this one file changes; the weekly run does not.**

**`Scripts\wire.py`** — under `--html` it now also writes `Source\WEEK_SHEET.html`. The call is
wrapped so that a failure in the sheet **cannot take the wire page down with it**, and every failure
path prints why rather than leaving a stale page looking current.

**`Scripts\ff.bat`** — checks `WEEK_SHEET.html` on disk alongside the other two, so a silent failure
shows up in `ff_log.txt` as `*** NO WEEK_SHEET.html ON DISK`.

`check_kit.py` re-pinned: `wire.py` 63,720, `sheet_engine.py` and `ff.bat` pinned for the first time.

---

## So the weekly plan, in full

**Nothing to run.** Tuesday 6am, Thursday 5:30pm, Sunday 11:45 and 15:30, his machine pulls the live
free-agent pool and his live roster from ESPN and rebuilds three pages. `WEEK_SHEET.html` is current
as of that pull — the bar grid re-solved against whoever is actually on his roster that morning, and
every free body in the league priced against it.

**Tuesday 6am is the one that matters**, because ESPN processes waivers overnight and the Wednesday
run is the first claim window of the week (doc 213: daily at 3–5am ET, concentrated into Wednesday
and Thursday by the NFL calendar). The sheet is on his desk before he has to decide anything.

**What is still mine, and it is the judgement layer, not the arithmetic.** The page cannot read news,
cannot see that a starter limped off, and cannot decide whether the kicker gap is the real thing. It
prices what the projections say against his own lineup. **The right division is: the machine
publishes the numbers four times a week without being asked, and I am for the weeks something
changes that a projection cannot see.**

---

## Open, with inputs named

- **Not yet run:** nobody has executed `wire.py --html` with the sheet hooked in. Everything above
  was exercised against the same inputs on staged copies of his files, including all three negative
  controls — but the live path has not run once on his machine, and §0.2 is explicit that same logic
  on a different object is not a test. **It is on his list, and it is one command.**
- **Not yet run:** `py waivers.py --live`, so `waiver_report_2026.csv` still does not exist and the
  sheet's rival-shortage map is still counted off **drafted** rosters rather than current ones. That
  map is the one part of the page that is still a photograph.
- **Open:** whether a fifth scheduled run belongs on Wednesday evening, ahead of Thursday's waiver
  run. Four covers the week; a fifth costs nothing but has not been argued for.
