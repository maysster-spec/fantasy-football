# 279 — He was right, my number was the wrong object, and the lever is volume

Matt, 2026-09-10, on doc 278's conclusion: *"I think it does makes a difference. gosh"*

**He is right, and doc 278's argument was wrong in a way worth writing down, because I made the
error while quoting a rule that forbids it.**

---

## 1. What I did wrong, twice

**THE ARGUMENT WAS BACKWARDS.** Doc 278 says the edge is *"unclaimed rather than worthless"* and
then uses the room's inaction as the reason not to chase it. An unexploited edge is a cheap edge.
The sentence contained its own refutation and I shipped it anyway.

**AND THE DENOMINATOR WAS WRONG (§0.5 a2).** The 5.8% is the share of **all** free-agent adds that
land inside a live game window. Most adds in this league are routine streaming — a kicker, a
defence, a bye-week body — and those *should* happen on Thursday. The question was never "what
share of all adds are fast." It was **"of the adds where speed could have decided it, who won."**
Different object, and I attached a percentage to the wrong one.

---

## 2. The right object, measured

**POPULATION: every EXECUTED skill-position add in this league 2022–2025, weeks 1–14, matched to a
weekly line, n=721. THE EVENT: an add that became a startable player for SIX OR MORE WEEKS —
a role someone inherited, not a one-week matchup pick. BASELINE: the position's measured
replacement rate (QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25).** That gives **79 season-changing adds
in four seasons.**

**34% OF THEM — 27 of 79 — WERE MADE OFF-THURSDAY.** `[TESTED]` Friday 8, Saturday 9, Sunday 10.
A third of every good outcome in this league is found outside the batch, and doc 278's headline
figure hid that completely.

**And the manager doing it most is the best manager in the room.**

| manager | season-changing adds | off-Thursday | all his adds, off-Thursday |
|---|---|---|---|
| **Multiple Scorgasms (Taylor — §5: "best manager, never worse than 5th")** | **9** | **6 (67%)** | **50 of 89 = 56%** |
| Olave Garden | 5 | 4 (80%) | 16 of 26 = 62% |
| Ekeler's Edge | 4 | 3 (75%) | 9 of 29 = 31% |
| Bloodied Castaways | 6 | 2 (33%) | 21 of 47 = 45% |
| **Matt (Junkyard Juggers)** | **4** | **1 (25%)** | **5 of 23 = 22%** |

**Taylor moves off-Thursday more than twice as often as Matt does.** That is exactly the pattern
Matt's instinct was pointing at, and it is on the board with names attached.

---

## 3. But the mechanism is NOT the one either of us named

**Per add, moving early does not convert better.** `[TESTED, null]` Same 721 adds:

| when the add was made | n | became a 6+ week startable player |
|---|---|---|
| Friday / Saturday / Sunday / Monday | 258 | **10.5%** |
| the Thursday batch | 463 | **11.2%** |

**Difference −0.8 points, permutation p=0.66.** Moving early does not make a given add better.

**So what separates Taylor from Matt is VOLUME, not timing — and the direction is not flattering
to the volume leader either.** Taylor made **89** skill adds and hit on 9 = **10.1%**. Matt made
**23** and hit on 4 = **17.4%**. **Matt picks better and swings a quarter as often.** Nine hits
beats four because eighty-nine shots beats twenty-three, not because Saturday beats Thursday.

**One lane does move, and it is the opposite of the intuition:** a WAIVER claim filed off-Thursday
hits **17.3%** (n=52) against **11.6%** in the batch, while free agency goes the other way — 8.7%
off-Thursday against 10.6%. Small cells, unresolved, and mentioned only so nobody quotes the
headline as though every lane behaved alike.

---

## 4. What NEITHER measurement can see, and this is why Matt's claim survives the null

**A LOST FREE-AGENT RACE LEAVES NO RECORD.** `waiver_report_*.csv` holds adds that *happened*. If a
player was taken free on Sunday, the manager who wanted him on Thursday never files anything and
never appears. The population is winners only.

The one place a loss IS recorded proves the point by contrast: **259 claims failed with
`FAILED_INVALIDPLAYERSOURCE` — 22.4% of every claim ever filed — and all 259 lost inside the same
Thursday batch, on priority, at a zero-hour gap.** Contests are common. But those are the ones the
system logs. **The free-agency contests are structurally invisible**, which is §0.6 again: the
dataset cannot contain the event being argued about.

**So: the per-add null does not refute him.** It says an add you *made* early is no better. It says
nothing about the player you never got. `[BLOCKED — the exact missing input is a record of
attempted-and-lost free-agent adds, and ESPN does not publish one. There is no workaround in this
file.]`

---

## 5. What changes

**The Sunday 7:30pm task stays** — it costs nothing, it is the only instrument watching the other
eleven backfields, and a third of the season-changing adds live in that window.

**THE ACTIONABLE FINDING IS VOLUME, AND IT IS NEW.** Matt's hit rate is the best on the table and
his shot count is near the bottom. Against a room where the champion-tier manager takes four times
as many swings at a *lower* rate, **the cheapest available point is more adds, not faster ones** —
and §4.31 already established that a claim here is free: no FAAB, no limit, priority resets weekly,
and the only cost is the drop.

**A NUMBER THAT MUST NOT BE QUOTED AGAIN:** doc 278's "5.8%, nobody races" as an argument against
acting early. The figure is correct and the use was wrong.

**NOT YET RUN, input named:** whether Matt's low volume is a preference or a consequence of the
bench being full. `drop_costs()` in `sheet_engine.py` already prices what every one of his bodies is
worth; the test is whether he had a droppable zero at the time of each week he made no add.
