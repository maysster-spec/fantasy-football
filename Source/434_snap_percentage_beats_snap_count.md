# 434 — snap percentage beats snap count

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 27 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 434" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `snaps_2026.py`, line 3

```

[doc 434] Matt, 27 Sept, one question: "do we have number of snaps?" No. `form_2026.csv` and the
wire carry `snap_pct` and nothing else, and a percentage is a SHARE with the denominator thrown
away. That is the same defect the reach gate fixed for targets (doc 432), one layer down and still
live: the screen ranks men on share of plays while the pies differ by 35%, from Houston's 79.5 a
game to Tennessee's 51.5.

WHAT IT CHANGES, measured on the men on the board at the time:
    Cade Otton        93% of snaps, 57.0 a game, Tampa runs 61.0
    Xavier Worthy     82% of snaps, 61.0 a game, Kansas City runs 74.5
```

### `claude_todo.txt`, line 41

```
                 "great matchup" point at all. Name it every time rather than reasoning around it.
[x] MEASURED, doc 434, and it KILLS the version of this item I wrote first. Snap PERCENTAGE
                 beats snap COUNT at predicting the next four weeks, at every position: all .2896
                 vs .2719, WR .3686 vs .3438, TE .3306 vs .3185, RB .4600 vs .4304, n=18,382
                 player-weeks 2021-2025. Adding team plays to the percentage adds NOTHING (.2896
                 to .2896). Team play counts swing week to week and the SHARE is the stable role
                 measure. Matt's arithmetic is right (a high share of 30 is not a high share of 50)
                 and it does not PREDICT. Two different claims; only the first holds.
                 DO NOT swap the screen to counts. Do not rebuild this.
[ ] WHAT THE COUNT IS STILL FOR, and it is a constraint and not a forecast: snaps_2026.csv
```

## The measured line, as the to-do file carries it

`claude_todo.txt` (27 Sept) records the result under this number: snap PERCENTAGE beats snap COUNT at
predicting the next four weeks at every position (all .2896 vs .2719, WR .3686 vs .3438, TE .3306 vs
.3185, RB .4600 vs .4304, n=18,382 player-weeks 2021 to 2025), and adding team plays to the percentage
adds nothing. No script or output file for that measurement is on the drive; the number is carried by
the to-do line only, so treat it as [TESTED, script not retained] and re-run before building on it.
