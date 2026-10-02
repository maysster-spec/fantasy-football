# 271 — Everyone else has byes too

2026-09-10. Matt: *"other teams have bye weeks too and we need to factor in scarcity and how many
weeks/days ahead are optimal to fill that position without negatively impacting the rest of the
roster."*

**Two testable forms, both stated before running (§0.5a2).**

**T1, demand.** POPULATION: every EXECUTED add in this league 2022–2025 that maps to a position,
weeks 2–14 — **1,228 of 1,230 adds mapped, 0.2% lost**. PREDICTOR: how many of the twelve managers
have their drafted starter at that position on bye that week, from `draft_history_2021_2025.csv`
joined to the real NFL schedule. OUTCOME: adds at that position that week. DIRECTION: more managers
short → more adds.

**T2, lead time.** POPULATION: every (manager, season, position) in QB/TE/K/D-ST where the manager
drafted **one** body at the position and that body had a bye in weeks 2–14 — 114 cases. OUTCOME: the
week of his nearest add at that position minus the bye week.

---

## T1 — the spike is real at kicker and quarterback, and nowhere else

| position | r | p | adds when 0–1 rivals short | 2 short | 3+ short |
|---|---|---|---|---|---|
| **K** | **+0.572** | **0.0000** | 1.82 | 2.89 | **4.33** |
| **QB** | **+0.383** | **0.0034** | 1.92 | 2.60 | 3.25 |
| WR | +0.272 | 0.046 | 3.83 | 4.83 | 5.00 |
| RB | +0.142 | 0.310 | — | — | — |
| TE | +0.112 | 0.425 | 2.62 | 2.90 | 3.20 |
| D/ST | +0.058 | 0.683 | 3.95 | 4.00 | 3.67 |

`[TESTED, n=52 season-weeks per position]` **Matt's instinct is confirmed at the two positions
nobody carries a backup at, and is null at the two that churn all season anyway.** Tight end and
defence are added three to four times a week regardless of who is on bye, so a bye adds nothing
visible to a stream that never stops. Kicker is the opposite: 1.8 a week normally, 4.3 in the weeks
three managers lose theirs.

## T2 — the field fills in the bye week, or not at all

| position | holes | filled | median lead | in the bye week | a week early | 2+ early | never filled |
|---|---|---|---|---|---|---|---|
| kicker | 44 | 24 | **0** | 17 | 2 | 5 | **20** |
| defence | 38 | 23 | **0** | 13 | 3 | 7 | 15 |
| tight end | 19 | 9 | **0** | 5 | 3 | 1 | 10 |
| quarterback | 13 | 2 | 1 | 1 | 0 | 1 | **11** |

`[TESTED, n=114 manager-season-positions]` **Median lead is zero at every position, and roughly half
of all holes are simply eaten.** Eleven of thirteen managers with one quarterback took the zero
rather than stream a replacement. So **one week of lead puts him ahead of nearly the whole field** —
this is not a crowded auction, it is a room that mostly does not turn up.

## The half that decides it: how much a snipe actually costs

Demand tells you who else is looking. It does not tell you what losing the race costs, and on this
board the two disagree.

| position | best free | 8th free | a snipe costs | rivals chasing |
|---|---|---|---|---|
| kicker | 10.3/wk | 9.8/wk | **0.5 a week** | high — week 7 |
| tight end | 8.6/wk | 6.6/wk | 1.9 a week | low all season |
| **defence partner** | **+9.4 season** | **+5.5 season** | **3.9 for the season** | high — weeks 10–11 |

**The kicker pool is deep and flat: the top eight sit within half a point.** So the sharpest
bye-week demand effect in the league sits on the position where losing your first choice costs about
a tenth of a point. **The defence is the mirror** — no measurable bye-week rush, but only seven free
partners and four points between the best and the worst.

## And the cost of being early, priced

A week of lead costs one roster spot for one week. On this roster the spot's best alternative use is
a potential receiver worth **+1.53 over fourteen weeks ≈ 0.11 a week** (doc 269). So two weeks early
costs about **0.2 points**, against protecting a fill worth eight to ten. **Being early is close to
free at every position, and that — not the size of the risk — is what settles it.**

## The 2026 map, from the other eleven drafted rosters

| week | NFL teams off | rivals short at |
|---|---|---|
| 5 | 2 | TE 1, K 1 |
| **6** | 4 | TE 1, K 1, D/ST 2 — **your TE hole** |
| **7** | 4 | QB 1, **K 3**, D/ST 2 |
| **8** | 4 | TE 1, K 2 — **your K hole** |
| 9 | 2 | D/ST 1 |
| **10** | 4 | QB 1, K 1, **D/ST 3** |
| **11** | 6 | QB 1, TE 2, K 2, D/ST 2 — **your D/ST hole** |
| 13 | 4 | QB 1, K 1 |

**Week 7 is the kicker run and week 10–11 is the defence run.** Nobody chases a tight end all season.

## What changes, and what does not

- **Tight end, week 5 — unchanged.** One rival short in weeks 5 and 6. There is no race.
- **Kicker, week 7 — unchanged, and now for a stated reason.** Week 7 *is* the run, and buying in
  week 6 would mean holding two spare bodies at once on a 15-man roster. **It is not worth a drop:
  the whole prize for winning the race is a tenth of a point.** Considered and declined.
- **Defence partner, week 9 — unchanged, and this is the one where the lead time is the point.**
  Week 9 sits one week ahead of the run and is also when the pairing starts paying (doc 267).
- **Quarterback — needs no attention.** Matt: *"tyler shough is the least of my concern."* Correct,
  and measured: he already holds the backup that eleven of thirteen managers never bothered to get,
  so week 10 is covered.

**Shipped:** `Scripts\research\scarcity.py`, and section 5 of `Source\WEEK_SHEET.html`.

## Open, with inputs named

- **Not yet run:** the same question for injuries rather than byes. A bye is on a calendar; an injury
  is not, and the rush after a starter goes down is the version of this that cannot be planned.
- **A stated weakness:** rival shortages are counted off **drafted** rosters, so a manager who has
  since added a backup still shows as short. It reads high, and by design — running
  `py waivers.py --live` weekly is what would replace it with the real thing.
