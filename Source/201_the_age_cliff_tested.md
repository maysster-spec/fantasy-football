# 201 — The RB age cliff, tested as the tail; and what Matt's rule actually costs

*2026-09-06, T−1. Matt: **"At no point will i take Henry in the first. Wont even cross my mind as
the next man up. I don't want to be on the wrong side of his age cliff even though you say it's not
a thing — i don't see any 40 year old running backs out there."***

---

## 0. ACTIONABLE FIRST (§0.1 v7.8)

1. **His rule stands and it costs 0.0 points.** At pick 8 Henry is the **#2** row behind St. Brown
   (−7.9), so he never binds. In the only state where he is #1, **James Cook III is −0.0** and
   Achane −0.1.
2. **Bonus, not a reason:** Cook's bye is week 7. Henry's is week 13, the pile §4.11b names
   (Taylor, Jeanty, Henry, Hall, Bowers, Flowers, Warren).
3. **The age claim itself is NULL and underpowered — not disproved.** Do not tell him it is "not a
   thing." That was my word and the data does not support it either way.

---

## 1. WHAT WOULD HAVE TO BE TRUE (§0.5(a2), stated before running)

His claim is about a **tail**: backs at the top of the age range fall off faster than their price
allows. The earlier "age is dead" result was a **continuous fit across all RBs** — the mean. Wrong
object for a cliff claim, and exactly the failure (a2) was written for.

**Testable form.** POPULATION: 273 RB seasons, 2021–2025, carrying a §1.1 preseason ADP ≤ 180
(registry only — never historical `espn_adp`). OUTCOME: half-PPR weeks 1–14. BASELINE: minus what
`log(preseason ADP)` predicts, fit **within season**; the residual is BEAT. **sd(beat) = 55.1.**
DIRECTION he predicts: the old band is materially negative — the market does not discount enough.

## 2. RESULT — NULL, DIRECTION HIS WAY, UNDERPOWERED

| age at Sep 1 | n | mean beat | median | mean adp |
|---|---|---|---|---|
| <24 | 75 | −8.9 | −4.1 | 83.9 |
| 24–25 | 82 | +6.4 | +0.5 | 78.9 |
| 26–27 | 69 | +8.9 | +6.4 | 74.6 |
| **28–29** | **35** | **−12.1** | −15.4 | 88.0 |
| **30+** | **12** | **−4.0** | −21.3 | 85.1 |

- **age ≥ 28: −12.1 pts, p=0.209, bootstrap CI [−29.4, +6.1]**
- **age ≥ 29: −6.1, p=0.608** · **age ≥ 30: −4.2, p=0.831**

**Against sd 55 at n=47, anything under about 22 points is invisible.** §4.24(b)'s distinction:
**this failed POWER, not PREDICTION.** The point estimate leans his way and cannot be separated
from zero.

**There is no monotone cliff.** 30+ is *less* negative than 28–29. If the mechanism were age
itself, it would deepen; it does not.

**The tail is bimodal, and violently.** Every 29+ season in the window, worst and best:

| worst | | best | |
|---|---|---|---|
| Mostert 2021 (29.4) | −97.6 | Mostert 2023 (31.4) | **+149.1** |
| Conner 2025 (30.3) | −90.0 | Kamara 2024 (29.1) | +97.1 |
| Mostert 2024 (32.4) | −67.4 | **Henry 2024 (30.7)** | **+89.4** |
| Edwards 2024 (29.4) | −63.3 | McCaffrey 2025 (29.2) | +69.5 |
| Elliott 2024 (29.1) | −58.8 | Conner 2024 (29.3) | +52.0 |

**Raheem Mostert is the −97.6 and the +149.1**, two years apart, at 29 and 31.

**Henry's own three seasons in the window: +38.4 at 29.7 · +89.4 at 30.7 · −9.1 at 31.7.**

## 3. WHY THE POPULATION IS TINY, AND WHAT THAT MEANS

Twelve 30+ RB seasons carry a drafted ADP in five years. **There are no 40-year-old running backs
because teams stop handing them the job, not because a 33-year-old who HAS the job collapses.** The
survivors are selected on exactly the thing that matters. That is §4.20 restated —
**buy the job, never the name** — and it is the strongest argument *against* reading the thin tail
as evidence either way.

## 4. THE COST OF THE RULE — MEASURED, PRODUCTION ENGINE

`recommend(8, top=12, rollout_inner=60)`, board 09-06 freeze.

| state | #1 | #2 | #3 |
|---|---|---|---|
| top seven by eff_pick gone | **St. Brown** +0.0 | Henry **−7.9** | Cook −8.2 |
| top seven **+ St. Brown** gone | **Henry** +0.0 | **Cook −0.0** | Achane −0.1 |

**Passing on Henry costs 0.0 points.** He is only ever the recommendation in a room that has taken
all eight of the top names by pick 8, and Cook is a dead-even substitute there.

**METHOD NOTE — this nearly shipped wrong.** My first instrument removed Henry from the engine's
pool entirely, which returned −8.5. That measures *a world in which Henry never existed* — the
rollout's whole future gets worse for every candidate — not the decision in front of Matt. **The
decision is `cost vs #1` within the same state.** Same object-versus-question error §0.5(a2) names,
caught before it was quoted. Two in one day.

## 5. WHAT I OWE HIM

He wrote *"even though you say it's not a thing."* **I did say that, and it was not a measured
statement when I said it.** §0.2: a claim asserted before it was tested. It is tested now, and the
honest answer is *underpowered, direction yours, cost of acting on it zero* — which is a different
sentence from either "you're right" or "it's not a thing."

*Reproduce: nflverse weekly 2021–2025 + rosters for `birth_date`, joined to
`Source\adp_registry\preseason_adp_YYYY.csv` on a suffix-stripped name key; RB only, adp ≤ 180.*
