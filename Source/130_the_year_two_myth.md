# 130 — The year-two comeback: a null, and the case that inspired it was a premium

*2026-09-01. Matt, on doc 129: "the Saquon Barkley year — he broke out 2 years after injury. The
first year back his numbers slumped, but I got him the next when his value was still depressed and
he went off that year."*

**The pattern is real in Barkley's stat line and false in the market. Measured across 338
player-seasons: the year-two player is neither cheap nor better. And Barkley in 2022 was drafted
17 slots EARLIER than his projection warranted — he was a premium, not a discount.**

**What the test DID find is worth more than what it was looking for: the year-one penalty is
dose-dependent, and the board badge is now shaded accordingly.**

---

## 1. The test

Same machinery as doc 129 — the two seasons with both a preseason ADP registry entry and a usable
ESPN projection (2022, 2024). Adding a second lookback year means nflverse 2020 as well. Players
need **both** prior seasons on the field to be classified, which drops rookies and second-year
players: 413 joined, **338 classified**.

| cohort | n | market discount vs projection | **mean beat** | beat > 0 |
|---|---|---|---|---|
| **A** healthy both years | 179 | −1.1 slots | **−13.3** | 39.7% |
| **B** hurt LAST year (doc 129's cohort) | 89 | +1.0 | **−25.4** | 34.8% |
| **C** **YEAR 2 BACK** — healthy last year, hurt two years ago | 70 | +1.6 | **−10.8** | **42.9%** |

*(cheap > 0 = the market drafts him later than his projection rank; mean beat is negative for every
cohort because ESPN projects ~15.3 of 17 games and injuries happen — compare across rows, not to zero.)*

**C vs A: +2.4 points, p=0.77. A null.** Market discount vs A: +2.7 slots, p=0.54 — **also a null.**

C vs B is **+14.6 points, p=0.14** — directionally exactly the shape you described, year two much
better than year one, but not resolved at n=70 vs 89.

**The reading: the injury discount fully unwinds after one healthy season.** A player who missed
time two years ago and then played a full season is, to the market and to the outcome, an ordinary
player. There is no lingering depression to buy.

## 2. Barkley 2022 was not cheap

He is in the data, in cohort C, in one of the two testable seasons.

| | |
|---|---|
| preseason ADP | **22** — rank **19** on the joined board |
| ESPN projection rank | **36** |
| divergence | **−17 slots — the market paid a 17-slot PREMIUM over his projection** |
| projected / actual | 202.0 → **255.5**, beat **+53.5** |

**Your memory of the outcome is exactly right and your memory of the price is not.** He beat his
projection by 53 points. But the market was ahead of the projection on him, not behind it — the
thing that was "depressed" was ESPN's number, and ESPN's number is what your board is built from.
Buying him was a bet against the projection, and it happened to be the right one. That is the same
trade doc 129 measured 409 times and found loses on average (rho **−0.173**, p<0.001).

## 3. And cohort C was a coin flip that year

The 2022 and 2024 year-two-back players, in ADP order, with what they returned:

**Worked:** Chase +102 · Ekeler +67 · Burrow +65 · Chubb +65 · **Barkley +53** · McBride +47 ·
Kittle +32
**Did not:** Dak −192 and −123 (both seasons) · Deebo −86 · Damien Harris −83 · Sutton −50 ·
Breece Hall −43 · Fournette −40 · Mixon −28

**43% beat their projection against a 40% baseline for players healthy in both years.** Three
points, on n=70. Deebo Samuel and Damien Harris were the same cohort in the same season as Barkley
and cost 85 points each.

**This is survivorship, and it is not a criticism — it is how memory works.** The pick that
returned +53 is the one that stays with you; Deebo went to somebody else's roster. The measurement
exists precisely because recall cannot do this job.

## 4. WHAT THE TEST ACTUALLY FOUND — severity, and it changes the board

Splitting doc 129's year-one cohort by **how much** time was missed:

| games played the prior season | n | **mean beat** | market's discount |
|---|---|---|---|
| **1–6 games** | 19 | **−40.8** | +7.7 slots |
| 7–9 games | 30 | −27.1 | +1.0 |
| 10–12 games | 40 | −16.9 | −2.1 |
| 13+ (baseline) | 249 | −12.6 | — |

**Monotonic, and the market's discount scales the right way but nowhere near far enough** — it asks
7.7 slots for a player who then misses 28 points more than baseline. At the mild end (10–12 games)
the penalty is barely distinguishable from healthy, which means **doc 129's binary badge was too
blunt**: an eleven-game season and a four-game season are not the same warning.

`[SUGGESTIVE, NOT RESOLVED]` The pooled correlation is **r=+0.083, p=0.128, n=338** — the bands are
monotonic but hold only 19/30/40, and requiring two prior seasons drops the population from doc
129's 402 to 338, which is also why cohort B's penalty softens here (−12.1, p=0.145) against doc
129's controlled −16.2, p=0.025. **Carry doc 129's number as the finding and this as the shape.**

**SHIPPED:** the `12g` badge is now **shaded in three tones** — ≤6 games darkest, 7–9 mid, 10–12
lightest. 12 players on the board sit in the worst band, 21 in the middle, 27 in the lightest.
The two that should stop you: **Jayden Reed (5 g) and Chris Godwin Jr. (9 g) both carry BUY.**

## 5. What this does and does not change

- **Doc 129 stands.** Year one back is the penalty and it is real.
- **Year two back is nothing.** Do not pay up for a bounce-back narrative and do not expect a
  discount to still be there. `[TESTED, n=70, null]`
- **Severity matters more than the flag.** Read the number on the badge, not just its presence.
- **Nothing here moves a VBD number.** Same call as doc 42 and doc 129: surfaced, not scored.

## Assumptions, and what would break them

1. **n=70 in the cohort that matters.** A true year-two effect smaller than about 20 points could
   not be detected here. The null is "no evidence of an effect," not "proof of none."
2. **Two seasons again.** Preseason ESPN pulls for 2023 and 2025 would roughly double every cohort
   and are the single input that would resolve docs 128, 129 and 130 together.
3. **Games played is a crude injury proxy.** It does not distinguish a Week-2 ACL from a
   three-game hamstring, or injury from benching. The dose bands partly stand in for that.

## 6. Reproducing it

```
py anchor_study.py --year2
```
Needs nflverse `w2020.csv` in addition to doc 129's requirements. Run 2026-09-01; the output above
is that run.
