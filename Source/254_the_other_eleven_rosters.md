# 254 — MODELLING WHAT THE OTHER ELEVEN NEED: NOT YET RUN, IT IS ITEM H IN THE CATALOG, AND IT BECAME RUNNABLE TODAY

*2026-09-09. Matt: "knowing what other teams need on the waiver wire... may help inform my priority*
*on the wire. assuming I'm ahead of that other manager in waivers. have we covered that strategy*
*yet?"*

**Answer: NO — and it is not a new idea, it is `227 §1.H`, logged as OPEN on 2026-09-08 and never**
**run. What changed today is that the missing input got built by accident.**

---

## 0. WHAT TO DO

1. **Nothing to run tonight.** This is a feasibility note plus the testable form, not a model.
2. **A tension between two of my own docs, named and resolved:** doc 250's *"the claim is free"* and
   doc 226's *"the first claim that clears is the only one you get at your real priority"* are both
   true at different scopes. **Across weeks free; WITHIN a week the order collapses after your first
   hit.** That within-week ordering is the only real cost — and it is exactly what his idea optimises.
3. **He is 5th of 12 this week** (doc 238). Four teams can take a name ahead of him: Lobsinger,
   R. Taylor, Rychlicki, Snyder.
4. **`wire.py` still hard-codes "near the back."** ESPN's `mTeam` view carries `waiverRank`. That
   line should print the real number; still `[OPEN]` from doc 238.

---

## 1. IS IT EVEN OBSERVABLE? YES — AND THAT WAS NOT OBVIOUS

**POPULATION: every WAIVER-type row, 2022–2025, grouped by (week, player).** A contested player-week
is one where two or more teams filed on the same man in the same run.

| season | waiver rows | player-weeks | contested | share | most filers on one man |
|---|---|---|---|---|---|
| 2022 | 355 | 165 | 41 | 24.8% | 5 |
| 2023 | 327 | 173 | 52 | 30.1% | **10** *(Jerome Ford, wk 3)* |
| 2024 | 471 | 232 | 73 | 31.5% | 7 |
| 2025 | 432 | 217 | 59 | 27.2% | 7 |
| **total** | 1,585 | **787** | **225** | **28.6%** | |

`[TESTED — feasibility only]` **Better still, the LOSERS are recorded.** The status vocabulary on
waiver rows is `EXECUTED 614 · FAILED_INVALIDPLAYERSOURCE 364 · PENDING 322 · CANCELED 152 ·
FAILED_PLAYERALREADYDROPPED 101 · FAILED_ROSTERLIMIT 24 · FAILED_POSITIONLIMIT 6 · FAILED_ROSTERLOCK 2`.
**So every filing is visible, not just every win.** Most published waiver work cannot see this at
all; we can, on 1,585 rows.

## 2. THE INPUT THAT WAS MISSING, AND IT GOT BUILT TODAY

The model needs **each rival's roster at the moment he files**, so a positional hole can be scored.
Nothing in the project had that. **Doc 252 §4 built it for a different purpose** — the free-pool
count by week — and it is the same object: the rostered set, rebuilt from the draft plus all 1,230
executed adds and drops in date order, walked week by week.

**That is the whole blocker, gone.** §0.5(a4): this moves from **BLOCKED** to **NOT YET RUN.**

## 3. THE TESTABLE FORM (§0.5(a2)), WRITTEN BEFORE ANY TEST

> **POPULATION:** the 787 waiver player-weeks above.
> **PREDICTOR, known before the run processes:** for each of the other eleven teams, whether that
> team had a HOLE at the player's position that week — no startable body at the slot, computed from
> the reconstructed roster plus the bye calendar plus the injury report.
> **OUTCOME:** the number of teams that actually filed on that player.
> **DIRECTION:** teams with a hole at the position file more often than teams without one.
> **THE DECISION IT SERVES:** for a player Matt wants, count the filers *predicted ahead of him in
> the order*. **Zero ahead → do not spend the claim; he clears and can be taken as a free agent.
> One or more ahead → claim him, and put him FIRST on the list**, because doc 226 measured that the
> first clear is the only one at his real priority.

**AND THE FALSIFIER, FIXED NOW:** if a positional-hole flag adds less than 0.3 expected filers over
a base rate of "how popular is this player," the model is noise and the honest answer is to rank by
value and stop. **Do not ship a rival model that cannot beat 'claim the best man available.'**

## 4. WHAT WE ALREADY KNOW THAT BEARS ON IT

- **Doc 224: Matt wins 56% of uncontested claims (51/91) and 16% of contested ones (10/63).** That
  gap is the prize. If the model can tell the two apart *in advance*, it converts a 16% lane into a
  choice rather than a coin flip.
- **Doc 226: 65% of team-weeks end with 0 or 1 claim landing**, and volume stops paying above 5–9
  filed. **His long list is not the problem; the ORDER of the list is.**
- **Doc 226: hoarding priority is NULL** (r = −0.022, n=266, p=0.715). Waiting does not improve the
  next claim. So the model is about *ordering within a week*, never about saving.
- **Doc 227 §1.H also holds his other untested idea** — *"blocking a claim, denying a handcuff to the
  owner of the starter."* Same machinery answers both.

## 5. WHY I AM NOT BUILDING IT TONIGHT

§0.5(c)2: a half-finished sweep reads as coverage. This needs the reconstructed rosters joined to a
weekly startable/not flag and to the injury calendar, and then a fit that has to beat a
player-popularity baseline. **That is a session, not a paragraph.** The feasibility, the input and
the falsifier are now on paper, which is what makes it a real queue item instead of an idea.

## 6. OPEN

- The model itself — **NOT YET RUN**, testable form above.
- **`wire.py`'s hard-coded "near the back"** — should read `waiverRank` from ESPN's `mTeam` view.
- Doc 252's legibility test and the D/ST hit rate by week, both still open.
