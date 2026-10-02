# 286 — Sutton: he is not the only one, he is the consensus, and the doubt is already in the price

**2026-09-10.** Matt: *"well you should know how I feel about cortland Sutton. Am I the only one
doubting his talent?"*

**FIRST, THE PART THAT IS MINE: I did not know, and it was not in any of the 333 docs.** His reads
live in replies and replies scroll away — **the exact defect `matt_todo.txt` exists to fix on my side
of the ledger, unfixed on his.** `Source\matt_reads.md` is new and now holds every opinion he has
expressed about a player, a team or a mechanism, with what happened when it was tested.

---

## 1. THE TESTABLE FORMS (§0.5a2), because "talent" is not one

His question splits into two and they resolve differently:
1. **Is Sutton's per-target production actually poor?** → **PARTLY. He is median.**
2. **Is he alone in doubting it?** → **No. The market is already there, and it is settled.**

---

## 2. THE TALENT QUESTION — MEDIAN, ON A HARD JOB

**POPULATION: the 33 receivers with 90+ targets in 2025. SOURCE: `pff_receiving_2025.csv`.**

| Sutton, 2025 | | the median of the 33 | rank |
|---|---|---|---|
| targets | 120 (21.2% of Denver's) | — | — |
| **yards per target** | **8.47** | **8.36** | **15 of 33** |
| yards per route run | 1.62 | 1.87 | below |
| catch rate | 61.7% | 65.8% | below |
| average target depth | **13.3** | — | high |
| contested catch rate | **53.1%** | — | good |

**His own four seasons:** yards per target 7.82 → 8.93 → 8.19 → **8.47**; drop rate 8.6 → 10.6 →
11.0 → **6.3**. `[SOURCED]`

**So the honest verdict is ORDINARY, not bad — and the two numbers that look worst are partly his
job.** A 13.3-yard average target depth mechanically depresses catch rate and yards per route; the
contested-catch rate is the part that is actually his skill and it is good. **On the one measure that
is volume-neutral he is exactly the median of a high-volume field.** His doubt is directionally
supported; *"doubting his talent"* is a stronger claim than the data carries.

---

## 3. AND HE IS NOT ALONE — HE IS THE CONSENSUS

| source | where Sutton sits |
|---|---|
| **FantasyPros ECR** | **rank 84, WR36** — best 50, worst 114, avg 84.5 |
| ESPN ADP | **81.8** |
| **ESPN's own 2026 projection** | **Jaylen Waddle 174.8 ahead of Sutton 169.5** — and Waddle's ADP is **53** |

**Nobody prices him as a star.** WR36 on a 12-team board is a flex body, and Denver's own projection
now has Waddle as the number one receiver.

**AND THE PANEL IS NOT UNUSUALLY SPLIT ABOUT HIM, WHICH I NEARLY WROTE AND CHECKED FIRST.** His
standard deviation across rankers is **15.0** against a **median of 13.9** among the 70 receivers
inside rank 180 — **29 of 70 are more disputed.** This is not a live argument; it is a settled,
boring agreement that he is a WR3/4. (The genuinely disputed receivers are Stribling at 56.0,
Diggs 49.0, Nailor 42.8.)

**THE RED-TEAM HALF, AND IT IS THE POINT: A DOUBT THE MARKET ALREADY HOLDS IS NOT AN EDGE.** §4.22(b)
measured that when the market and the projection disagree, the market is the one that is right — here
they **agree**, so there is nothing to arbitrage in either direction. And §4.13d measured that
ranker disagreement, controlling for ADP level, predicts finishing **worse** (−0.244, p=0.0009), so
even a split panel would not have been an opportunity. **Being right about Sutton earns nothing on
its own. Where it pays is downstream.**

---

## 4. WHERE IT DOES PAY — AND IT IS THE BEST ARGUMENT FOR BRYANT ANYONE HAS MADE

**Denver's 2025 target distribution** (`pff_receiving_2025.csv`, 566 team targets):

| | targets | share | yards per target |
|---|---|---|---|
| Courtland Sutton | 120 | 21.2% | 8.47 — **median of the field** |
| **Troy Franklin** | 102 | 18.0% | **6.95 — 31st of 33** |
| Evan Engram (TE) | 71 | 12.5% | 6.49 |
| RJ Harvey (RB) | 57 | 10.1% | 6.25 |
| Marvin Mims Jr. | 51 | 9.0% | 6.31 |
| **Pat Bryant** | **47** | 8.3% | **8.04** |

**Denver spent 39% of its targets on a median receiver and a bottom-three one — and Bryant's 8.04
yards a target on 47 looks was within half a yard of Sutton's 8.47 on 120.** `[SOURCED]`

**That is a better case for Bryant than the Payton quote, and it is the one to keep.** Doc 284
measured that moving up the order pays most where the receiver room is big, and Denver's room took
**61% of the team's targets and fed four men**. **The gap between Bryant and the two men ahead of him
is volume, not measured ability** — which is exactly the state doc 284 says a promotion cashes in.

**THE CAUTION, STATED BECAUSE IT IS THE SAME TRAP AS EVERY OTHER TIME: 47 targets is a rate on a
small base**, the same objection that keeps McMillan behind Bryant on four games. Bryant's 8.04 is
suggestive and it is not a finding. `[SOURCED, not modelled]`

---

## OPEN AFTER THIS

- **`matt_reads.md` is hand-maintained and §9 records that every prose map in this project went stale
  within hours.** It is the right file and it is the wrong mechanism. `[OPEN]` — the durable version
  would have `open_threads.py` scrape his quoted reads out of the docs the way it already scrapes my
  markers, and nothing in it currently does.
- **Sutton's own 2026 projection is 169.5 against Bryant's 58.5** — a 111-point gap the room's own
  numbers do not obviously support. Whether ESPN is anchored on Sutton's volume rather than his rate
  is `NOT YET RUN`; the testable form is whether a receiver's projection tracks last season's targets
  after controlling for his yards per target.
