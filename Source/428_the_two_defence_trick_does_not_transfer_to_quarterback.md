# 428 — The two-defence trick does not transfer to quarterback, and the reason says when it would

> **BANNER, 28 Sept 2026 (doc 435), reproduced cold.** The QB numbers stand and get stronger without hindsight: elite QB1 plus streamer platoon minus 2.31 (se 0.35) in weeks 15 to 17 reproduces, and is minus 2.59 over weeks 2 to 14 and minus 5.63 with a top-3 elite; two streamers +0.31 (se 0.23) reproduces and is +0.12 ex ante, a null with a positive tilt. **The tight-end rows do NOT stand as published: `te_pair.py`'s docstring says leave-one-out and the code used the plain in-sample season mean, so the generosity included the game being scored. CORRECTED FROM A RUN, 29 Sept (doc 440): `te_pair.py` is fixed (for a game in week w the defence's TE generosity is the mean over weeks 1 to w-1 only; `--in-sample` reproduces the retracted rows exactly; `--selftest` proves the lookahead is gone) and the rows are now from the script, not from doc 435's hand rebuild, which they confirm to the decimal. Weeks 2 to 14, start the softer matchup minus always start TE1, a week: elite TE1 + streamable TE2 minus 1.77 (se 0.10, n=288 pairs; was minus 0.86) · mid TE1 + streamable TE2 minus 0.95 (se 0.07, n=288; was minus 0.37) · two streamable TEs minus 0.03 (se 0.06, t minus 0.50, n=528; was +0.50, and when the rule benched the first streamer it lost 0.11 a week and won exactly 50% of the time, n=1,651). Weeks 15 to 17 were already ex ante and move by 0.04 to 0.15. What still carries hindsight in weeks 2 to 14 is WHO is elite (tiers fixed on weeks 1 to 14), the same assumption 1 below makes for quarterbacks.** The six-row "monotone in the gap, crosses zero near 1 point" chart mixed three baselines, three windows and two instruments; on one footing, bigger gap is worse and nothing positive is measured at a zero gap. The roster clock artifact was corrected the same day.

*25 Sept 2026. Matt: "At some point it may make sense to roster two quarterbacks but I forget what
we discussed. But again, the goal was to have a solid QB matchup or something along those lines so
that I can go the distance when it comes to playoffs and such."*

---

## 1. WHAT WAS ALREADY ON FILE, which is what he forgot

**§4.17b, doc 111.** QB2 is worth **+5 to +11, low end better supported**. The mechanism is not
matchup, it is absence: **a drafted starting QB is missing 2.98 weeks a season** (median 1, p75 5,
n=48 team-seasons). Goff at 19.20 over a re-measured waiver QB at 17.38 is 1.8 to 2.6 ppg across
those 2.98 weeks. **The QB2 case on file has always been injury insurance.**

**§6 doctrine** says that when he does take one, the second is chosen *"for complementarity, not for
value: easy matchups in the weeks the first one is hard."* **That clause was never measured.** This
doc measures it.

---

## 2. THE TESTABLE FORM, STATED BEFORE THE RUN (§0.5(a2))

Over **weeks 15-17**, does starting whichever of {QB1, QB2} faces the softer defence beat simply
always starting QB1? **Ex ante:** opponent generosity and the tiers are computed from **weeks 1-14
only**, so the rule uses nothing from the weeks it is scored on. Population: nflverse REG 2021-2025,
QB starts, scored under §2. This is doc 267's `pairs.py` question asked of quarterbacks.

---

## 3. THE RESULT, AND IT SPLITS ON THE QUALITY GAP

| pairing | n pairs | always start QB1 | start the softer matchup | difference |
|---|---|---|---|---|
| **elite QB1 + streamable QB2** | 252 | **24.80** | 22.49 | **−2.31, se 0.35, t = −6.57** |
| **streamable + streamable** | 363 | 18.83 | 19.14 | **+0.31, se 0.23, t = +1.33** |

`[TESTED]` **With an elite QB1 the marriage is actively harmful.** The rule benched QB1 in about a
third of pair-weeks, and when it did it lost **6.75 a week and won only 28% of the time** (n=259).

**With two mid quarterbacks it runs his way and is underpowered:** +0.31 a week, and when it swapped,
+0.95, winning 55% of the time (n=358). That is a coin flip with a small positive tilt.

---

## 4. WHY IT WORKS FOR DEFENCES AND NOT FOR QUARTERBACKS

**Doc 267 measured the defence pair at +0.79 a week and found 115% of the gain came from choosing
complementary schedules rather than from owning two bodies.** The two findings agree once you put
them side by side: **the marriage pays when the two men are close in quality and matchup is the only
thing separating them.** The best single defence ran 5.63 a week against a pair at 6.42 — a spread
of under a point. At quarterback the quality gap is **24.80 against 18.40, about 6.4 points**, and
the matchup slope is **0.448 per point of opponent generosity** (doc 427). Matchup cannot move six
points. It moves one or two.

**So the rule is not "two bodies marry two schedules." It is "marry two schedules when the bodies are
interchangeable."** Defences are. Quarterbacks are not, unless both of yours are streamers — which is
exactly the state he lands in if Jalen Hurts goes down, and is the one case where §6's
complementarity clause survives.

---

## 5. WHAT THIS MEANS FOR HIS PLAYOFF QUESTION

1. **Do not hold a QB2 to play matchups while Hurts is healthy.** Measured at −2.31 a week.
2. **Weeks 15-17 carry no byes**, so a playoff QB2 is purely insurance against Hurts missing time.
3. **The supply curve is the reason to act early, not the matchup.** Doc 252: usable free
   quarterbacks fall from **4.0 in week 2 to 1.5 at week 11 and 1.0 at week 12**. Today there are six
   free between 16.5 and 21.6.
4. **§4.17b's +5 to +11 is a FULL-SEASON hold** against a bench spot doc 267 priced at about +7 for
   its best alternative use. **That is a coin flip and it always has been.** What breaks the tie is
   not the value of the second QB, it is whether one exists when he needs one.

## OPEN / NOT YET RUN

- **The value of a QB2 held only from week W to 17**, rather than all season, against the same bench
  spot. §4.17b's 2.98 missed weeks is a season figure and pro-rating it is arithmetic I have not
  measured. Mine.
- ~~**The same pair test for TIGHT END**, where the quality gap is much smaller than QB and may behave
  like the defences.~~ RUN, doc 440: the fixed `te_pair.py`; two streamable TEs are a null (minus 0.03) and any
  quality gap makes the pair a loss. See the banner.

## ASSUMPTIONS

1. Tiers fixed on weeks 1-14 ppg among QBs with 8+ games: elite 1-6, streamable 13-24.
2. A pair-week is scored only when QB1 actually started; weeks he missed are the injury question,
   not the matchup question, and are priced in §4.17b instead.
3. Opponent generosity is a season-to-week-14 mean, not a rolling form measure. A rolling version
   would be a different and probably noisier instrument.
