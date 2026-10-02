# 132 — The offensive line: knowable, and still not actionable

*2026-09-01. Matt, from the car: "have you done any analysis on the offensive line?"*

**Short answer: the project surveyed it (doc 12 §2.7) and killed the RB version (doc 28's dead
list). The QUARTERBACK version was flagged live and untested. I have now tested it.**

**It corrects a piece of the project's reasoning — pass protection IS forecastable, more so than
almost anything else measured here — and it still does not change a pick.**

---

## 1. What already existed

- **Doc 12 §2.7** surveys the public work. Team-level OL quality correlates ~0.43 with team
  fantasy points (4for4, n=32, one season) but only ~0.25 at the player level (PFF, 2008–2010).
  Its own reconciliation: *"use OL to adjust team environment, not to pick between two RBs."*
  It also warns that 4for4's headline 0.591 is a restricted-range artefact — do not quote it.
- **Doc 28's dead list** carries **"offensive-line quality for running backs"** among the
  eighteen retired factors.
- **Doc 28 also flags the open piece:** *"offensive-line quality for QUARTERBACKS — the RB
  version is dead; the QB version has never been tested."* That is what this doc closes.

## 2. CORRECTION — pass protection persists, and doc 28's reason for doubting it was the wrong quantity

Doc 28 wrote off forecastability with *"2024→2025 line-continuity churn is r=−0.01, so history
does not forecast it."* **Continuity is personnel; sack rate is performance. They are different
quantities, and only one of them is stable.**

Team sack rate allowed = sacks ÷ dropbacks, nflverse, **2020–2025, n=160 transitions**:

| team trait | year-to-year r |
|---|---|
| **sack rate allowed (pass protection)** | **+0.399** |
| offensive EPA per play *(doc 131)* | +0.382 |
| team rush EPA per carry | +0.368 |
| team yards per carry *(crude — includes the back)* | +0.314 |
| defensive EPA per play *(doc 131)* | +0.204 |

**Pass protection is the most persistent team trait measured anywhere in this project** — above
offensive efficiency, nearly double a defence. It is genuinely knowable in August.

**And it is not just the quarterback.** Splitting the same 160 transitions by whether the team's
primary passer changed:

| | n | sack rate persists |
|---|---|---|
| same primary QB both years | 95 | **r = +0.444** |
| **QB CHANGED** | 65 | **r = +0.245**, p=0.049 |

**Roughly half the persistence survives a new quarterback**, so the line and the scheme carry a
real, forecastable share — and the residual +0.245 is still above a defence's +0.204. `[TESTED]`

## 3. NULL — and it still does not move a quarterback's fantasy points

The whole point of a stable, knowable trait is that you can price it in August. So:

| predictor of a QB's beat vs his projection | r | p | effect |
|---|---|---|---|
| **prior-season** team sack rate *(knowable in August)* | **+0.092** | 0.53 | +5.7 pts per +1% sack rate |
| same-season sack rate *(hindsight — an upper bound)* | −0.160 | 0.27 | −9.6 pts per +1% |

n=50 QB-seasons (2022 + 2024, preseason ADP registry). League sack rate is 6.7% ± 2.0%, so a
one-sd line is worth about 11 points on the point estimate — and the interval swallows it whole.

**`[UNDERPOWERED — not "no effect".]`** The sd of a QB's beat is **108 points**. With n=50 an
effect below roughly 25 points is invisible here. Note also that the two rows disagree in *sign*,
which is what noise looks like.

**VERDICT: no board change.** The QB version joins the RB version as not actionable — but for a
different reason, and the distinction matters if anyone revisits this. **The RB version failed
prediction. This one failed power.** With the two missing ESPN projection pulls (2023, 2025) it
would go to n≈100 and become answerable.

## 4. Why I would not chase it further before Sept 7

Even at the optimistic end, this is a QB-side effect, and §4.2 already closed pick 8 in favour of
the best board player with QB later, while §4.17b prices QB2 at +5 to +11. A line-quality tilt
would have to beat those to change anything, and it cannot do so from a null.

There is one thing worth carrying, though, because it is cheap and it is now measured: **when two
quarterbacks are otherwise tied late — the §4.18 draft-night rule at 104/113 — the one behind the
better-protected line is the better tiebreak than a coin flip.** That is a preference, not a
number, and it should never move a pick with real margin behind it. Same standing as byes (§4.11).

## Assumptions

1. **Sack rate is a proxy, not a grade.** It bundles the line, the scheme, the back's blitz
   pickup and the quarterback's own time-to-throw. The QB-changed split (§2) is the only control
   applied, and it is a coarse one.
2. **Run blocking is measured worse than pass blocking here.** Team yards per carry includes the
   running back, so its +0.314 is not a clean line signal. nflverse has no adjusted line yards;
   that would be a PFF pull (doc 6 §8 ranks it third on that list).
3. **n=50 for the payoff test**, the same two-season limit as docs 128–131.

## 5. Reproducing it

```
py ol_study.py
```
Needs `Source\nfl\w<year>.csv` for 2020–2025, the two ESPN projection pulls and the ADP registry.
Run 2026-09-01; the output above is that run.
