# 204 — Rivers was right, and so was "it varies by player" — this qualifies doc 203

*2026-09-06, T−1. Matt: **"Just look at Philip Rivers. they sent [him] out there at an older age.
he couldn't throw the ball at distance... each player has different injury rates and so not everyone
can be scored the same at the same age. the signal is not standalone and varies by player."***

---

## 0. BOTH POINTS LAND, AND THE SECOND ONE QUALIFIES WHAT I TOLD HIM AN HOUR AGO

**1. The Rivers channel is real and measured.** QB seasons with 200+ attempts, 2021–2025, n=177:

| age | n | aDOT (air yards/attempt) | deep throws (20+) |
|---|---|---|---|
| under 28 | 101 | 7.91 | 12.0% |
| 28–31 | 38 | 7.81 | 11.4% |
| **32+** | **38** | **7.62** | **11.5%** |

**rho(age, aDOT) = −0.196, p=0.009 · rho(age, deep rate) = −0.176, p=0.019.** `[TESTED]`
**An ageing quarterback throws measurably shorter while still starting every week.** Availability
cannot see that. Doc 203 said age acts *through* availability; **this is a second channel and it is
significant.**

**2. And the availability signal DOES vary by player — it disappears on veterans.**
Restrict to players with **three prior seasons on file** (n=290, same price/season/position controls
as doc 203):

| model | availability coefficient | p |
|---|---|---|
| last season's games | +0.63 pts per game, se 1.16 | **0.59** |
| own 3-year rate | +0.52, se 1.81 | **0.77** |
| both together | g1 +0.61 · r3 +0.09 | 0.64 / 0.97 |

**Neither predicts anything.** And the bands are non-monotone: 16+/yr **+7.3** · 14–15 **−5.6** ·
11–13 **+2.3** · under 11 **−7.1** (n=12).

**This is not a power failure.** The standard error rules the pooled effect out: doc 203's −19.4
is roughly −5 points per missed game, and this subsample's coefficient is +0.63 ± 1.16 — four
standard errors the other way.

## 1. WHY, AND WHAT IT MEANS FOR THE BOARD

**Doc 203's −19.4 is partly survivorship.** A player with three prior seasons on file has already
survived the filter. The whole-pool penalty is carried by the players who wash out; among
established veterans there is nothing left to predict. **Same structure §4.18b flagged on kept
players — the effect was real and the LEVEL was wrong for the subgroup that mattered.**

**BOARD IMPACT: none tonight, and the badge stays.** 46 of 180 rows carry `12g` and it is still
the right mark for the pool as a whole. **What changes is how to read it: on a young or unestablished
player it is a warning; on a ten-year veteran it is close to noise.** That is Matt's sentence —
*the signal is not standalone and varies by player* — and it is now measured rather than asserted.

**Concretely, the live rows it re-reads:** McLaurin (7 NFL seasons), Godwin (9), Kelce (13),
Kittle (10) — established veterans whose `12g` badge should carry less weight than the badge on a
second- or third-year player. **Jayden Reed (5 g, year 4) and Rome Odunze (12 g, year 3) keep theirs.**

## 2. WHAT IS STILL OPEN

- **Does the shorter aDOT cost fantasy points?** Not established. Doc 203's healthy-QB cut was
  −13.8, p=0.438. The MECHANISM is confirmed; the PRICE of it is not. It may already be inside the
  projection (§4.6's "already priced" list).
- **The equivalent physical measure for RB and WR** — breakaway rate, yards after contact, deep
  target share by age — not run. Same shape of test, post-draft.
- **Age × situation change** (doc 203 §3, his Randy Moss case) — still untested.

## 3. THE PATTERN IN HOW THIS WAS FOUND

Three consecutive corrections today came from him naming a *subgroup* my test had averaged over:
the tail not the mean (docs 196/198), the projection not the price (doc 202), and now the veteran
not the pool. **§0.5(a2) says state the population before running the test. All three would have
been caught by writing the population down.** The rule is four hours old and has been vindicated
three times and followed zero.
