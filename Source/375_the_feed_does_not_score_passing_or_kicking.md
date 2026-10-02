# 375 — the feed does not score passing or kicking, and the pocket sheet was subtracting anyway

**2026-09-19, Saturday, scheduled Pocket Sheet refresh.** Population: `Source\form_2026.csv` as
written by the 11:51 ET rebuild, week 1 rows, n=1,118 players. Baseline: the league-scored
projections in `Source\WEEK_SHEET.html` (6-pt passing TD, 0.5 PPR, per §2).

## What happened

The Pocket Sheet's whole design is three numbers side by side: the sheet's **projection**, the
player's **actual**, and the **bar**. The actual comes from `half_ppr` in `form_2026.csv`. The page
then prints the difference as "N vs the sheet".

**`half_ppr` does not score passing, and does not score kicking at all.** So at quarterback and
kicker that subtraction was between two different scoring systems, and the page printed the
remainder as if it were a bad week.

## The claim in its testable form, stated before the test

*If `half_ppr` counts passing production, the week-1 quarterback distribution cannot be ranked by
rushing volume and cannot have a near-zero median.*

It is ranked by rushing volume and the median is near zero.

| measure | value |
|---|---|
| QB rows, week 1 | n=37 |
| median QB `half_ppr` | **1.4** |
| max QB `half_ppr` | 18.5, Caleb Williams, **10 carries** |
| next two | Josh Allen 14.3 (6 car), Lamar Jackson 10.0 (7 car) |
| corr(QB carries, `half_ppr`) | **r = 0.640**, n=37 |
| K rows, week 1 | n=32, **all 32 read 0.0** |
| D/ST rows | **none exist in the file** |

The kicker column is the independent confirmation: a metric that scored kicking could not return
0.0 for every kicker in the league. The file measures production from scrimmage and nothing else.

## The numbers that must not be quoted again

The version of the Pocket Sheet published 18 September carried these, and they were artifacts:

- ~~Jalen Hurts, week 1 actual **4.6**, **−17.0 vs the sheet**, under the bar~~ — 4.6 is his
  rushing line. It is not his fantasy week and it cannot be differenced against 21.6.
- ~~Eddy Pineiro, week 1 actual **0.0**, **−9.1 vs the sheet**, under the bar~~ — the feed scores
  no kicker. There was never a measurement here.
- Chiefs D/ST already read "no week 1 line", which was correct for the wrong reason: the file has
  no defences at all, rather than one missing row.

**Running back, receiver and tight end are unaffected.** Their scoring is entirely rushing and
receiving, 0.5 PPR is half PPR, and the two numbers are on the same scale. Every RB/WR/TE
difference on that page stood and still stands.

## What was done

The refreshed page shows a note instead of a number on the QB, K and D/ST rows, saying in plain
words what the feed does and does not count. The footer now says the same thing once, so the reader
is told why three of fifteen rows look different rather than being left to guess.

## Two other defects the same rebuild cleared

- **George Pickens was on the page as "K · DAL · bye n/a".** He is the keeper, WR, DAL, bye 14.
  `MY_ROSTER.csv` ships him with blank `pos`, `team`, `bye` and `value` (so do Eddy Pineiro and
  Chiefs D/ST), and the previous build filled the blanks by position in the file rather than by
  looking the man up. Position now resolves from `form_2026.csv` and the week sheet's own drop
  table, both of which carry him correctly.
- **The roster moved and the page had not noticed.** Emari Demercado is gone; **Jonah Coleman**
  (RB, DEN, bye 10, projected 3.9, drop cost 0.0) is in.

## Open

**[OPEN] NOT YET RUN — the same subtraction lives in the builders, not only in the pocket page.**
Anything that differences a league-scored projection against `form_2026.csv`'s `half_ppr` has this
defect. `sheet_engine`, `wire` and `lineup` all read that file. The testable form: *for each
consumer of `half_ppr`, is the other side of the comparison league-scored?* Owner: me. Not attempted
in this run, which was a read-only publish with a lineup lock approaching.

**[OPEN] NOT YET RUN — decide whether `build_form` should carry a league-scored column at all.**
Adding one fixes the comparison everywhere at once; leaving it fixes nothing and every consumer has
to remember. Owner: me.

*Sources: `Source\form_2026.csv` (built 10:23 ET 19 Sep), `Source\WEEK_SHEET.html` and
`Source\MY_ROSTER.csv` (both 11:51 ET 19 Sep), `Source\WIRE_20260919.csv` (11:51 ET 19 Sep).
Injury designations and kickoff times: the league's own week 2 injury report and week 2 schedule,
both loaded 19 Sep. Artifact republished to its existing URL as version 2.*
