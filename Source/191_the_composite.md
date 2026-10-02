# 191 — Matt was right: the signals work TOGETHER better than one at a time

**2026-09-06 (T−1).** Matt: *"I do think some of those indicators taken together probably make a
difference than trying to do each one individually."*

**TESTED. HE IS RIGHT, AND THIS IS A METHOD ERROR OF MINE.** Docs 185–190 tested every mechanism
**one at a time** and reported each as live or dead on its own. The composite was never tried.

---

## 1. THE RESULT

**BASELINE: half-PPR points wks 1–14 of year t+1, regressed on log(§1.1 preseason ADP) within
season. BEAT = residual. Running backs, n=252, 117 unique players, player-clustered SE, 2022–2025.**

**Each signal alone:**

| signal | effect | p |
|---|---|---|
| top-quartile target share | **+19.2** | **0.006** |
| played 13+ games | **+17.6** | **0.016** |
| drafted rounds 1–3 | +13.3 | 0.057 |
| second-year player | −3.0 | 0.732 |
| age ≤ 26 | −2.3 | 0.710 |

**The three that carry it, as a 0–3 count:**

> **+12.2 points per signal, se 3.6, p=0.0008.**

| signals | n | mean beat | median |
|---|---|---|---|
| 0 of 3 | 41 | **−24.4** | −47.1 |
| 1 of 3 | 82 | −19.3 | −32.7 |
| 2 of 3 | 86 | −0.4 | +2.3 |
| **3 of 3** | **43** | **+7.8** | +3.9 |

**3-of-3 minus 0-or-1: +28.7 points, p=0.011.** Monotone across all four rungs.
Variance explained: target share alone **R² 0.025** → the count **0.031** → the three as separate
terms **0.047**. **Together they explain nearly twice what the best single explains.**

## 2. TWO HONEST CAVEATS

**(a) 2022 reverses.** By season, 2+ signals minus 0–1: **2022 −15.1 · 2023 +23.2 · 2024 +36.9 ·
2025 +50.6.** Three of four strongly positive, one negative (n=51). Same shape that made me call
draft capital "not established" in doc 189, so it must be said here too. **The direction is
supported 3 of 4 seasons; the size is not stable.**

**(b) They are SUBSTITUTES, not complements.** The target-share × availability interaction is
**−36.0, p=0.031** — negative. A back with both does *not* get double credit. **So the composite
works because two independent signals each carry information, not because they compound.** The
count is a reliability instrument, not a multiplier. Matt's intuition is right about the outcome and
the mechanism is not the one the phrase "taken together" implies.

**(c) The availability term contradicts §4.22(c) at RB.** §4.22 measured the prior-games effect as
**entirely a WR effect, RB null (+5.7, p=0.63)**. Here, as a binary against a price residual on
nflverse, RB is **+17.6, p=0.016**. Different outcome, different framework, opposite verdict.
**Flagged as an OPEN CONFLICT, not a new finding.** Post-draft work.

## 3. THE LIVE BOARD — RBs scored 0–3

Draft slot **sourced from nflverse rosters**, never from memory (§3). Target share from 2025
nflverse weekly. Quartile cut from the 2021–25 panel (10.8%).

**3 of 3, inside Matt's range:**

| player | adp | VOR | tgt share | games | NFL pick |
|---|---|---|---|---|---|
| Ashton Jeanty | 21.8 | +79.6 | 14.8% | 17 | 6 |
| **Tyjae Spears** | **147.4** | −38.9 | **12.0%** | 13 | 81 |

**Spears is the find** — the only back past pick 100 to clear all three, and a live name at 137.

**2 of 3, notable:** Judkins (48) · Swift (52) · **Tuten (61) — but on availability and draft slot,
his target share is 2.9%** · Henderson (77) · **Gainwell (100), 16.3% share, undrafted so S3=0** ·
Corum (126) · Harvey (126) · Charbonnet (154).

**1 of 3:** Irving (57) · Warren (86) · Dowdle (95) · Hubbard (109) · Dobbins (112) · Aaron Jones
(114) · Monangai (124) · Croskey-Merritt (136) · Mason (139) · Marks (152) · Pacheco (162).
**0 of 3:** Chris Rodriguez Jr. (164).

## 4. THE BURDEN FIVE — 1 of 5 SURVIVED

The pre-batch profile was: year 2 · played 13+ games · the man ahead didn't · unsettled job ·
both analyst panels ahead.

| signal | verdict |
|---|---|
| played 13+ games | **LIVE** (§4.22c at WR; +17.6 p=0.016 at RB here) |
| year 2 | **null** — doc 189, and −3.0 p=0.73 here |
| the man ahead didn't play | **null as a predictor** — doc 189, r=+0.039 p=0.699 |
| unsettled job | real flag, **but it does not pick the winner** — §4.20, p=0.604 |
| both analyst panels ahead | **predicts WORSE** — §4.13d, −0.244 p=0.0009 |

Matt's three additions to the Burden case (Caleb Williams improving, more team scoring, better
scheme) are all §4.21: team environment is **7.5%** of a receiver's variance and close to
unforecastable. **Tiebreak standing only, which is how he used them.**

## 5. ON SAMPLE SIZE — the analysts were never the sample

The 54 analyst takes are the **hypothesis source**. Every test ran on **nflverse: 252 RB-seasons,
390 pass-catcher-seasons, 807 player-seasons total, four preseason ADP vintages.** More analysts
would widen the *pool of ideas to test*, not the *power of the tests*. Power is not the constraint;
**ideas are.** That is the argument for mining more takes, and it is a different argument from the
one about sample size.
