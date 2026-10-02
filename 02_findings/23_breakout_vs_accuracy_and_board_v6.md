# 23 — BREAKOUTS vs ACCURACY, THE RANKER PANEL, AND POSITIONAL DEADLINES
**Aug 23, 2026.** Everything here is tested against data in the project.

---

## 1. YOUR HYPOTHESIS WAS RIGHT, AND HERE IS THE NUMBER

You said: *"the accuracy ratings just show analysts that were close to ADP anyway… a ranker
could hit on all the breakouts and another could have the most accurate rankings and catch
zero of them."*

**Tested on the 2025 season, 240 skill players projected 40+ preseason.**

Define a breakout as finishing 40+ ranks above your preseason projection AND landing top-40.
In 2025 that was **5 players of 240 — 2.1%**: Jaxon Smith-Njigba, Jaxson Dart, George Pickens,
Travis Etienne Jr., Chris Olave.

| ranker | mean rank error |
|---|---|
| matches ESPN's projection order exactly | 38.8 |
| **nails every single breakout**, ESPN-average on everyone else | **37.4** |
| **10% tidier than ESPN on the ordinary players only**, blind to all breakouts | **35.0** |

**Being mildly better at the boring players is worth 2.80× as much accuracy score as perfect
foresight on every breakout.** The five breakouts account for **3.4%** of total rank error.

**The FantasyPros accuracy contest is structurally incapable of detecting breakout skill.**
That is not a criticism of the contest — it measures what it says it measures. It is a
reason to stop using it to pick who to follow. Your instinct here was better than the
instrument, and it is now the fourth time that has happened (`ERROR_PATTERNS` F4).

---

## 2. THREE ANALYST EDGE COLUMNS WOULD HAVE BEEN THE SAME COLUMN THREE TIMES

You asked for `Edge H | Edge JJ | Edge VOR` and told me to run the numbers first. I did.

`sources/Yahoo_Top_300_6rankers_20260817.csv` — **already in the project, never used** — carries
six named rankers: **Boone, Smyth, Harmon, Pianowski, Winks, Norris.** Matt Harmon is one of
them. (This is `ERROR_PATTERNS` D7: the file the project kept saying it did not have.)

Measured against ESPN ADP across 157 shared players, their deviations correlate:

| | Boone | Smyth | Harmon | Pianowski | Winks | Norris |
|---|---|---|---|---|---|---|
| **Boone** | — | 0.80 | 0.86 | 0.77 | 0.82 | 0.81 |
| **Smyth** | | — | 0.82 | 0.70 | 0.72 | 0.79 |
| **Harmon** | | | — | 0.86 | 0.85 | 0.87 |
| **Pianowski** | | | | — | 0.83 | 0.78 |
| **Winks** | | | | | — | 0.83 |

**Mean pairwise 0.81.** They are not six opinions. They are one opinion — *"ESPN's board is
wrong in these same places"* — measured six times.

*A trap I nearly walked into:* my first pass measured each ranker against the six-ranker
average and got **negative** correlations, which looked like beautiful independence. That is
an artifact — each ranker is inside the average, so the deviations are forced to sum to zero.
Measuring against an **external** baseline (ESPN ADP) is what makes the number mean anything.

**Also worth knowing:** Harmon is the *least* bold of the six against the consensus
(mean deviation 5.5 ranks vs Winks 7.6). His edge is not in this list — it is in Reception
Perception charting, which we do not have.

### What the board carries instead

| column | what it is | why |
|---|---|---|
| **EDGE** | six-ranker field minus ESPN ADP | the visual you like, white/red, and it carries ~90% of what three columns would |
| **SPLIT** | highest minus lowest of the six | genuinely independent of EDGE. High split = the experts are fighting about him. **This is where a breakout thesis lives** — but note `ERROR_PATTERNS` A8: controlling for ADP level, disputed players finish *worse* (−0.244, p=0.0009). It marks uncertainty, not value. |
| **VOR** | points above the worst startable player at his position | your value anchor |

Most contested players right now: **Jordyn Tyson** (Smyth 81, Pianowski 219 — a 138-rank
fight), Kenyon Sadiq, Cam Ward, Isiah Pacheco, Brenton Strange.

---

## 3. THE ANSWER TO "WHAT IS THE LOWEST TIER BEFORE I'M NO LONGER EXECUTING ON VBD"

This is the best question you have asked and it was computable the whole time.

For each of your 14 picks I computed the **survival-weighted value of the best player still
on the board at each position** — so it already prices in who gets taken ahead of you.

| pick | 8 | 17 | 32 | 41 | 56 | **65** | 80 | **89** | 104 | 113 | 128 | 137 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| QB | +77 | +37 | +30 | +28 | +19 | +13 | +6 | **+2** | −7 | −14 | −21 | −25 |
| RB | +132 | +96 | +63 | +46 | +25 | +15 | +5 | **+2** | −3 | −6 | −13 | −19 |
| WR | +111 | +64 | +37 | +29 | +17 | **+10** | −2 | −7 | −14 | −17 | −23 | −26 |
| TE | +51 | +51 | +43 | +20 | +7 | +5 | +3 | **+1** | −4 | −8 | −15 | −18 |

**WR DEADLINE: pick 65. QB, RB and TE DEADLINE: pick 89.**

Past a position's deadline, every player left at it projects below the worst startable player
at that position. Taking one there is filling a hole, not drafting value.

**Wide receiver is the binding constraint of your entire draft** — it dies 24 picks before
everything else. That is the concrete argument for a WR in the opening, and it is independent
of the strategy simulation.

Both artifacts now show this: the grid has a **"Still worth a pick here?"** column that turns
red past a deadline; the board has four live meters that go red at the same point.

---

## 4. THE BREAKOUT SCREEN — and its failed gate, stated up front

You asked for something stronger than "upside." Built from the only factor family that ever
passed gate testing (directive 4.5): **inside-10 targets r=+0.59, red-zone target volume
r=+0.51, red-zone target share r=+0.48.** Red-zone TD *rate* is excluded — r=+0.02, noise.

The screen ranks live players by **sticky red-zone opportunity minus what the market already
paid for it.**

**Its own backtest gate failed.** 2024 red-zone opportunity did not predict 2025 breakouts:
r=+0.04, p=0.63, and the top quintile produced 0 breakouts against a 2.2% base rate. But with
**3 breakouts in 138 receivers** that is `UNDERPOWERED, NOT REFUTED` (`ERROR_PATTERNS` A1).

**So use it as a tiebreaker between similar players, never as a reason to reach.** Marked with
a gold star on the board and a sheet in the grid.

Top of the current list — pass catchers: **Hunter Henry, Romeo Doubs, Quentin Johnston (Q),
Dalton Schultz, Mark Andrews, Jake Ferguson.** Backs: **Zach Charbonnet (OUT — flagged),
Blake Corum, Jacory Croskey-Merritt, Kyle Monangai (Q), Jaylen Warren.**

---

## 5. NAME-JOIN COLLISION, OCCURRENCE 9

The ranker file uses first-initial names. `B. Robinson, ATL, RB` matches **both Bijan Robinson
and Brian Robinson Jr.** — same initial, same surname, same team, same position. The documented
minimum key (name + position + team) is **not sufficient here**. First pass had Bijan's field
rank at 163.8 and an EDGE of −162, which would have told you to fade the RB2 overall.

Caught by looking at the output rather than trusting the join. Resolved by rank proximity:
match the candidate whose ESPN rank is closest to the ranker file's own rank.

**New rule for `ERROR_PATTERNS` C1: any file that abbreviates first names needs a numeric
tiebreaker on top of name + team + position.**
