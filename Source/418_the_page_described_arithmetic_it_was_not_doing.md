# 418 — the page described arithmetic it was not doing, and the guard failed it for being right

**24 Sept 2026.** Matt ran `ff.bat` after the blend shipped and read the box at the top of the sheet.
Three things came out of what he found, and two of them were the page lying about itself.

---

## 1. THE PROVENANCE BOX WAS A HAND-WRITTEN CONSTANT AND IT WENT STALE THE SAME MORNING

The box said, in the one place a reader opens to find out what the numbers are:

> *Points a week, every pts/wk on this page: the ESPN projection pulled Thursday 24 September 07:40,
> 11 hours old, **divided by seventeen. a preseason projection.***

`rates()` had become a measured blend of this season and the projection six hours earlier (doc 417).
**The sentence was a string literal.** It could not move, so the page spent the day describing
arithmetic it was no longer doing.

**A provenance box that is hand-written is a second source of truth** (§0.5(c)4), and it is the worst
possible place for one: everything else on the page is checked against it. It is generated now, from
`BLEND_W` and from `_blend_count()`, which counts the vintage on the same dicts the table prints. It
cannot claim a blend the table did not apply.

## 2. "WHY IS IT RUNNING ON THURSDAY?"

> *"i don't understand the logic of running on Thurs when i need the data sooner for waiver
> decisions. Doesn't ESPN publish sooner than Thurs?"*

**Nothing runs on Thursday.** Every one of those timestamps was from the run he had just started, and
24 September is a Thursday. But **the box named the weekday of every input**, and a weekday on four
consecutive lines reads as a schedule. The question was the page's fault, not his.

Rewritten: **age first, and the command that resets it**, with the weekday gone. Each row now carries
its own refresh line, so the cadence is visible where the staleness is:

| row | refresh |
|---|---|
| Roster, free agents and injuries | `.\ff.bat` — live every run |
| This season's half of the blend | `py research\wk1\build_form.py`, Monday night |
| The projection half | `py Espn_pull_projections.py`, Tuesday |
| The bars and the seat odds | fitted on past seasons; age is not staleness |

And a row goes red when it is past its own cadence: `STALE_DAYS` is 7 days for the projection, 8 for
the form file. **Nothing was stale on his run** — the summary says so rather than making him check.

**COLLAPSED, at his request**, *"only expanded when i wish to reference"*. The provenance rows fold
into a `<details>` whose summary still carries the one actionable fact (`every input is current`, or
`2 inputs are past due`). **The settlement clock, the kickoff lock and the age line stay OPEN**,
because those are deadlines rather than provenance and burying a deadline is not tidying.

## 3. THE VINTAGE GUARD FAILED A CORRECT PAGE, IN CAPITALS

`check_vintage.py` printed this on his run:

```
  VINTAGE CHECK FAILED -- 5 printed rate(s) this season already refutes:
  Ryan Miller   5.7 / 14.2 · Mike Gesicki 9.0 / 16.3 · Davante Adams 14.1 / 19.8 ...
*** THE PAGE IS PRINTING A RATE THIS SEASON ALREADY REFUTES ***
```

**Every one of those five numbers was right.** Adams: projection 10.85, this season 19.8 on two
games, week-3 weight 36%, so the page correctly printed **14.07**. The guard was asking *"does the
printed rate equal this season?"* — which WAS the defect in doc 373, when every rate was a preseason
projection. Since the blend, the printed rate sits deliberately between the two, and at week 3 it is
64% of the way toward the projection. **The guard was built for a page that no longer exists.**

A guard that fails a correct page is worse than no guard, because the next real failure gets ignored.

**THE QUESTION IT ASKS NOW, and it is stricter, not looser:** *does the printed number match the
blend the page itself declares?* Every `pts/wk` cell carries `data-vintage="36% of 2 games"` (and a
`title` the reader sees on hover — Matt, on the news feed: *"I'll also be able to fact check your
numbers in real time"*). The guard recomputes `w × season + (1-w) × projection` from
`sheet_engine.rates()`, the object production builds, and demands the page's number equals it. That
catches a wrong weight, a wrong join, a stale rate **and** a mislabelled row. A cell with no blend
label still gets the original doc 373 test.

**Controls 6 and 7 are the false positive and its twin**, run first: the exact Adams row (guard must
stay quiet) and the same row labelled 36% while printing this season raw (guard must fire). Both use
the shape production builds, with an ownership `36%` elsewhere in the row as a decoy. All seven pass.

---

## WHAT SHIPPED

| file | |
|---|---|
| `Scripts\sheet_engine.py` | generated provenance box, collapsible, `rate_cell()` carries the vintage |
| `Scripts\check_vintage.py` | checks the blend it declares; controls 6 and 7 are the false positive |
| `Scripts\check_kit.py` | both re-pinned |

## OPEN

- **[OPEN]** `STATUS_LOG.csv` records only Matt's own roster, 45 rows. The pool's statuses are in
  `WIRE_*.csv` every run and are not logged, so the WHEN of a league-wide status flip — the input
  doc 396 is BLOCKED on — is being thrown away six times a week. **NOT YET RUN.**
