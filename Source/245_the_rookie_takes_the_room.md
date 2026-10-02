# 245 — He was right about receiver turnover, my null was the wrong object, and the displacer is a first-round ROOKIE

**2026-09-09.** Matt, pushing back on doc 244's receiver null:

> *"That's because we haven't uncovered it, and are not looking in the right place. Stud WRs are
> hard to get in the NFL, like QBs can be, and there is too scarcity at those upper tiers. There
> wouldn't be turn over at the WR position if not. Switching teams is one, perhaps speed is another,
> as well as separation. If a new and up and coming WR can prove that by year 3, they will get the
> chance."*

**HE IS RIGHT THAT THE TURNOVER EXISTS, MY NULL WAS ABOUT A DIFFERENT EVENT, AND THE ARCHETYPE IS
NOT THE ONE EITHER OF US NAMED.**

---

## 1. THE §0.5(a2) ERROR, MINE, STATED FIRST

Doc 244 measured **a within-season injury cameo**: a receiver fills in for two weeks and then the
starter comes back. That was null (−0.9 pp) and it is still null. **I then wrote "the mechanism
isn't there at receiver," which generalised a two-week object into a career-arc claim.** Matt is
talking about a **season boundary** — a young receiver taking a room over an offseason. Nobody gets
Wally Pipped at receiver in two weeks; he gets displaced in a year. **Different object, and the
sentence I wrote covered both.** That is the exact failure this project has now logged nine times.

---

## 2. THE TESTABLE FORM, AND THE EVENT IS REAL

> *Does a young receiver on the roster out-target his team's WR1 the following season, with the
> WR1 still on the team?*
> **POPULATION:** every team-season 2021–2024 where one receiver led the team with 60+ targets and
> was still on the roster the next year, paired with each teammate at 3 years' experience or fewer.
> **372 pairs.** **OUTCOME:** the young teammate finishes with more targets. **DIRECTION:** positive.

**BASE RATE: 9.9%. THIRTY-SEVEN DISPLACEMENTS ACROSS FOUR OFFSEASONS.** `[TESTED, n=372]`

And they are not all weak incumbents. **Puka Nacua over Cooper Kupp · Emeka Egbuka over Mike Evans ·
Jaxon Smith-Njigba over Tyler Lockett · Tre Tucker over Davante Adams · Malik Washington over Tyreek
Hill · Jordan Addison over Justin Jefferson (108–100) · Rome Odunze over DJ Moore · Michael Wilson
over Marvin Harrison Jr. · Wan'Dale Robinson over Malik Nabers (140–35).**

**Matt's core claim — "there wouldn't be turnover at the position if not" — is confirmed by count.**

---

## 3. EVERY INDICATOR HE NAMED IS NULL, AND ONE POINTS BACKWARDS

Same 372 pairs. Displacement rate, split each way:

| his indicator | with | without | difference | p |
|---|---|---|---|---|
| challenger separates more than 2.82 yds | 25.0% (n=40) | 19.5% (n=41) | +5.5 pp | 0.60 |
| challenger separates more **than the incumbent** | 25.0% (n=44) | 18.9% (n=37) | +6.1 pp | 0.61 |
| challenger's forty under 4.45 s | 13.0% (n=108) | 11.0% (n=109) | +2.0 pp | 0.68 |
| challenger faster **than the incumbent** | 11.7% (n=94) | 8.8% (n=91) | +2.9 pp | 0.63 |
| **challenger changed teams** | **4.8% (n=63)** | **11.0% (n=309)** | **−6.2 pp** | 0.16 |
| **challenger entering year 3** | **7.6% (n=92)** | **10.7% (n=280)** | **−3.1 pp** | 0.46 |
| incumbent is 28 or older | 13.0% (n=123) | 8.4% (n=249) | +4.6 pp | 0.20 |

**In combination (§0.5a3):** separation + air-yards share both above median = 27.3% on **n=11**;
faster AND separates more = 17.6% on **n=17**; year ≤3 AND separation above median = 24.1% on n=29.
**Every cell is too small to resolve anything.** `[TESTED, all null]`

**TWO HONEST WARNINGS ON THOSE ROWS.**
- **The separation rows run on 81 of 372 pairs**, because a receiver only gets an NGS season line
  once he has real volume. So that test is run *inside* a pre-selected high-volume group whose base
  rate is already 22%, not 9.9%. It is §4.23's selection trap in a new place and the +5.5 should not
  be read as a signal.
- **Underpowered throughout.** Against a 9.9% base rate, this design needs a difference of roughly
  10–12 points to see anything. **Report the null, and report what would resolve it** (§4.24b).

**Switching teams and year-3 are the two he named most confidently and both lean the WRONG way.**
That is worth saying plainly: a receiver who moves teams is *less* likely to take a room over, and
year 3 specifically is *below* the base rate.

---

## 4. THE ARCHETYPE THE DATA DOES SHOW, AND NEITHER OF US NAMED IT: THE INCOMING FIRST-ROUND ROOKIE

Of the 37 displacements, by the challenger's year in the league:

| year 1 | year 2 | year 3 | year 4 |
|---|---|---|---|
| **14** | 8 | 7 | 8 |

**The single largest group is first-year receivers**, and their NFL draft round is the story:

| the rookie | round | displaced |
|---|---|---|
| Chris Olave | **1** | Marquez Callaway |
| Garrett Wilson | **1** | Elijah Moore |
| Jordan Addison | **1** | **Justin Jefferson** |
| Quentin Johnston | **1** | Josh Palmer |
| Xavier Legette | **1** | Adam Thielen |
| Malik Nabers | **1** | Darius Slayton |
| Xavier Worthy | **1** | Rashee Rice |
| Tetairoa McMillan | **1** | Xavier Legette |
| Emeka Egbuka | **1** | **Mike Evans** |
| Wan'Dale Robinson | 2 | Kenny Golladay |
| Elic Ayomanor · Chimere Dike | 4 · 4 | Calvin Ridley (both) |
| **Puka Nacua** | **5** | **Cooper Kupp** |
| Rashid Shaheed | undrafted | Marquez Callaway |

**Nine of the fourteen are first-round picks.** `[TESTED, n=37 displacements]`

**So the answer to "where does receiver turnover come from" is: mostly it walks in the front door
with high draft capital.** Not a year-3 riser proving himself, not a free-agent arrival — the two
shapes Matt named. **His instinct that the event exists was right; the mechanism is a different one,
and it is far easier to see, because draft position is published in April.**

---

## 5. WHAT THIS MEANS FOR TYSON, AND IT CLOSES THREE DOCS AT ONCE

**Jordyn Tyson was the 8th overall pick of the 2026 NFL draft, first round, to New Orleans.**
`[SOURCED: nflverse draft_picks, 2026 season]`

Our board projected him at **82.0 points, 81.5 BELOW receiver replacement**, with a price inside
§4.14's fabricated-ADP blob (doc 242). **The single column that would have flagged him — where the
NFL drafted him — is free, is in one file, is keyed by name, and covers 2026.** It is not on the
board, not on the cards, not on the tier sheet, and not in `depth_map.csv`.

**And it is not only him.** 2026 first- and second-round receivers: **Carnell Tate (4, TEN) ·
Jordyn Tyson (8, NO) · Makai Lemon (20, PHI) · KC Concepcion (24, CLE) · Omar Cooper Jr. (30, NYJ) ·
De'Zhaun Stribling (33, SF) · Denzel Boston (39, CLE) · Germie Bernard (47, PIT).**
**Matt named Concepcion and Tyson on his own wanted list. Cary drafted Tyson at 117 and Stribling
at 93.** My grade charged Cary 139 points for those two picks (doc 242).

**THE BUILD THIS EARNS — and it is one column, not a model: put NFL draft round and overall pick on
the board.** §4.13's RB composite already uses "NFL rounds 1–3" and it was never extended to
receivers, which doc 243 §5 named as the gap. This is that gap, with a measured population behind it
now instead of a hypothesis.

---

## 6. THE OUTSIDE RESEARCH HE ASKED FOR

`ERROR_PATTERNS` B7 — dates first.

- **4for4, "The Most Predictable Wide Receiver Stats," 8 July 2024.** Ranks 23 receiver stats by
  year-to-year correlation. **The most stable thing about a receiver is not his production — it is
  his ROLE: slot rate 0.75**, ahead of targets per game 0.70, fantasy points per game 0.68, aDOT
  0.65 and targets per route run 0.64. Least stable: route rate 0.01, contested-catch rate 0.02,
  drop rate 0.14, TD rate 0.19. Most predictive of *next* season's points: yards per game 0.59 …
  yards per route run 0.59, first downs per route run 0.57.
- **The "third-year receiver breakout" is a whole published genre** (CBS Sports, FantasyPros,
  Fantasy Life, 4for4 — 2025 and 2026 editions all live). **Our own measurement puts year 3 BELOW
  the base rate for displacement**, which does not refute the genre — it measures a different
  outcome (taking the room, not scoring more) — but it is a flag that the popular framing and the
  measurable event are not the same object. `[OBSERVED]`

**THE ONE INDICATOR THE RESEARCH POINTS AT THAT WE HAVE NOT TESTED IS THE ONE MATT ALREADY NAMED IN
HIS OWN WORDS:** *"there isn't one type of WR."* **Slot rate is the most persistent receiver trait
measured anywhere in this research — 0.75, higher than production** — and nothing in this project
distinguishes a slot from an X from a Z. **BLOCKED, input named:** nflverse carries `ngs_position`
on the roster file and alignment can be approximated from NGS cushion and intended air yards, but a
true slot rate is a PFF field. **Not yet run; the approximation is buildable from files already on
disk.**

---

## 7. WHAT IS NOW IN HAND THAT WAS NOT THIS MORNING

| his indicator | source, downloaded today | column |
|---|---|---|
| separation | nflverse `nextgen_stats/ngs_receiving`, 2016–2025 | `avg_separation`, `avg_cushion`, `percent_share_of_intended_air_yards` |
| speed | nflverse `combine` | `forty` |
| switching teams | nflverse `rosters` | `team` vs `draft_club` |
| year in the league | nflverse `rosters` | `years_exp` |
| **NFL draft capital** | nflverse `draft_picks`, **through 2026** | `round`, `pick` |

**None of this needed a source we do not have. All five were two downloads away.**

---

## 8. OPEN THREADS

- **Draft capital on the board** — the build §5 earns. Not started.
- **Slot / alignment** — BLOCKED on a true slot rate; an NGS approximation is buildable. Not run.
- **The displacement test is underpowered** and every combination cell is n≤29. Adding 2016–2020
  would roughly double it; NGS covers 2016 and the roster files go back further.
- Carried: the Aug-8 depth chart is a month stale; `draft_analysis.json`'s back half needs a real
  comparator (doc 242); the hypothesis register is still unbuilt (doc 243).
