# 272 — The hot kicker, and a number of mine it corrects

2026-09-10. Matt: *"not sure it works, but i sometimes remember to look for a kicker who is
performing well on waivers and pick him up if the value seems worth it. And then keep that kicker."*

**It works. It is worth about +1.25 points a week for the rest of the season, and it corrects a
number I gave him an hour earlier.**

---

## This is not doc 213's question, and that matters

Doc 213 asked whether a team's **kicking tendency carries from one season to the next** and found it
barely does — stall rate in field-goal range persists at r=+0.200, field-goal-range drives at
+0.052, kicker points at +0.259. That closed the **draft-day** question.

Matt's claim is about **within one season**: does what a kicker has done through week W predict what
he does after week W. Different object, and it turns out a different answer. §0.5(a2) — saying so
before running is the whole point of the rule.

## Testable forms, stated before running

**T1 persistence.** POPULATION: team-kicker seasons 2021–2025, weeks 1–14, scored under this
league's own kicker rules — n=2,055 kicker-weeks, mean **7.99**, sd **4.59**. PREDICTOR: points per
game through week W. OUTCOME: points per game from W+1 to 14.

**T2 the swap.** At week W, the best-scoring kickers **not drafted in this league that year**
against the **median drafted** kicker. OUTCOME: rest-of-season points per game. That is the move he
described, measured as he would make it.

**T2c the falsifier, fixed before computing.** The same swap, but choosing three free kickers **at
random** instead of by what they have done. If the random three do as well, the edge is "free
kickers are underrated," not "the hot one is."

---

## T1 — within a season, kicker scoring does persist

| through week | n | r | p | hot half, after | cold half, after | gap |
|---|---|---|---|---|---|---|
| 4 | 159 | +0.123 | 0.120 | 8.07 | 7.72 | +0.35 |
| **6** | 158 | **+0.217** | **0.0055** | 8.09 | 7.49 | **+0.60** |
| **8** | 156 | **+0.208** | **0.0082** | 8.15 | 7.55 | **+0.60** |
| 10 | 151 | +0.167 | 0.039 | 8.20 | 7.83 | +0.37 |

`[TESTED, n≈158 team-seasons]` **Real, and small on its own.** The better half of kickers through
week 6 beats the worse half by six tenths of a point a week afterwards.

**The regression slope is the usable form: 0.222 at week 6, 0.243 at week 8.** So a kicker who is a
point a week ahead right now projects about **a fifth of a point** ahead going forward.
**Take a fifth of the gap you can see.** To be worth a real point a week you need to be looking at a
visible gap of four or five.

## T2 — the swap he actually makes is bigger than T1

| at week | n swaps | mean | median | 95% CI | beat the holder |
|---|---|---|---|---|---|
| **6** | 15 | **+1.25/wk** | +0.93 | **[+0.28, +2.32]** | 60% |
| 8 | 15 | +0.79/wk | +0.95 | [−0.24, +1.86] | 67% |

`[TESTED, top three free kickers, five seasons, bootstrap 4,000]` **At week 6 the interval clears
zero.** At week 8 it does not — the edge in this data is a week-6 phenomenon, and on fifteen swaps
that difference is itself inside the noise. Carry the week-6 number.

**Why the swap beats T1's +0.60:** two things stack. The persistence, and the fact that a *drafted*
kicker was chosen on a preseason projection that is close to worthless, so the median rostered
kicker is simply an average kicker while the best free one carries the signal as well.

## T2c — the falsifier, and it is what makes this a finding

| at week | top three by what they have done | three at random off the same free list | the signal is worth |
|---|---|---|---|
| **6** | **+1.25/wk** | **−0.04/wk** | **+1.29** |
| 8 | +0.79/wk | +0.56/wk | +0.23 |

**At week 6 the random three are worth nothing and the hot three are worth +1.25.** The edge is the
signal, not the pool. **That is his mechanism, isolated.**

## "And then keep that kicker"

**The +1.25 already is the keep-him number** — the outcome is rest-of-season points per game, weeks
7 through 14, not the week he claims him. Nothing here supports treating it as a one-week rental,
and nothing here needs a separate durability test, because durability is what was measured.

**Over eight remaining weeks that is +8 to +10 points** — the same size as filling one of his three
empty weeks, out of a habit he described as "sometimes remember to."

---

## And it corrects a number of mine from an hour earlier

Doc 271 said the kicker pool is flat — *"the top eight free kickers sit within half a point of each
other, so losing your first choice costs about a tenth of a point"* — and concluded that scarcity at
kicker is nearly free.

**That was measured on preseason projections, and at kicker the projection is close to worthless.**
Doc 213 measured kicker points persisting between seasons at r=+0.259, which is what a projection
has to work with. On **what kickers have actually done**, the pool is not flat at all: through week
6 the best free kicker averages **9.66** against a median drafted **7.65**, a gap of two points a
week — four times the spread I quoted.

**The correction:** the kicker pool is flat *before* the season and spreads out *during* it. My
"scarcity is nearly free at kicker" line is right in September and wrong from about week 6, and
doc 271's kicker row should be read with that attached.

## What changes on the plan

The week-7 kicker add was a **rental** for Pineiro's week-8 bye. It should now be a **replacement
test**:

**Around week 6, compare Pineiro's actual points per game to the best unowned kicker's. If the gap
is four or five a week or more, take him and keep him.** That one move covers the week-8 bye *and*
banks the +1.25, and it dissolves the roster-spot problem doc 271 ran into — a replacement needs no
second body.

If the gap is small, the old plan stands: rent one in week 7, drop him after week 8.

**The cost of being wrong is zero.** Kickers are free agents, not waiver claims; the pool is 22 deep;
and a kicker carries no keeper value at all (§4.18b: K and D/ST become keepers 0% of the time), so
dropping Pineiro costs nothing but the roster slot he was already using.

**Shipped:** `Scripts\research\kick.py`, and the kicker rule on `Source\WEEK_SHEET.html`.

## Open, with inputs named

- **Underpowered, and named as such:** fifteen swaps across five seasons. §4.24(b)'s distinction —
  this failed nothing, it simply cannot separate the week-6 and week-8 readings. Two more seasons
  would.
- **Not yet run:** the same test at defence. D/ST churns more than any position in this league (248
  of 1,230 adds) and nobody has asked whether in-season D/ST scoring persists the way kicker scoring
  does. The weekly file already exists — `dst_weekly_2021_2025.csv`.
- **Not yet run:** whether the gap should be read against *his own* kicker rather than the median
  drafted one. The measurement compares to the median holder; Pineiro is not the median holder.
