# 55 — CAN YOU RAISE THE CEILING? WHAT A BREAKOUT IS WORTH, AND WHERE RISK PAYS
**Aug 26, 2026.** Matt: *"Neither I know, nor does anyone else, how to raise the ceiling without
guess work… I do think it is possible to take selective risk."* Tested rather than argued. He is
right about the value of breakouts, wrong about being able to pick them, and right that selective
risk is possible — but only in one specific place.

---

## THE ANSWER, IN FOUR LINES

1. **Breakouts decide your season.** Each player who returns >1.35× his projection roughly
   **doubles your title odds**: 0 breakouts → 4.7%, one → 14.4%, two → 26.8%, three → 54.6%.
2. **You cannot pick which player it will be.** Three draft-day signals tested against outcomes,
   **all null.** The "market is sleeping on him" signal is the *worst* of the three.
3. **You can pick WHERE.** Breakouts happen at **17.0%** per player in ADP 121–180 versus
   **2.1–6.2%** in ADP 25–84 — a real, sourced 3–8× difference in rate.
4. **So: risk late, never early.** A global upside tilt **costs $22–41 of expected payout,
   p=0.003.** A tilt confined to round 9 and later costs nothing and is mildly positive
   (+$2 to +$7, not significant). **Late risk is a free option; early risk is a tax.**

---

## PART A — NEW MACHINERY: THE SIMULATOR NOW HAS REAL OUTCOME VARIANCE

Everything before doc 54 scored players at exactly their projection. **A simulator with no
projection error structurally cannot answer a question about ceilings**, which is why doc 54's
p90 result was uninformative. Fixed here.

### A1. The outcome model, decomposed and sourced

For each player-season with both a projection and a result, joined to the **clean preseason ADP
registry** (doc 53):

```
form = (actual points / games played) / (projected points / 15.32)    <- per-game quality
gp   = games actually played                                          <- availability
```

Splitting them matters: a season ruined by a torn ACL is a `gp` event, not a `form` event, and
conflating them was double-counting the injury discount ESPN already applies.

**n = 324 player-seasons (2022 and 2024 — the years where ESPN still serves games-played).**
Draws are bootstrapped as `(form, gp)` **pairs** so their correlation (+0.245) survives.

| ADP band | n | form mean | form **sd** | form p90 | games mean |
|---|---|---|---|---|---|
| 1–24 | 48 | 0.99 | **0.24** | 1.26 | 14.7 |
| 25–48 | 48 | 0.96 | **0.21** | 1.25 | 14.8 |
| 49–84 | 71 | 0.95 | **0.26** | 1.30 | 13.7 |
| 85–120 | 69 | 0.92 | **0.32** | 1.22 | 13.6 |
| **121–180** | 88 | 0.95 | **0.45** | **1.57** | 13.9 |

**Dispersion nearly doubles from the top of the draft to the bottom, while the mean is flat.**
Late picks are not worse bets — they are *wider* bets. That is the entire basis for selective risk.

### A2. The league is now simulated whole

All 12 rosters are drafted, all 12 keepers assigned (`predicted_keepers_v5`), all 12 lineups
scored weekly, and standings resolved by **head-to-head record** with a random 14-week schedule,
points as tiebreak. Objective set: mean points, P(1st), P(top 6), and **expected payout** against
the real $1,200 structure.

**Realism check:** simulated between-manager sd is **171–184 points**; doc 41 measured 104–202 on
real seasons. Passes.

---

## PART B — TWO DEFECTS FOUND WHILE CALIBRATING, BOTH CORRECTED

### B1. THE OPPONENT NOISE MODEL OVER-DISPERSED LATE PICKS — doc 53 corrected

Doc 53 recommended `sd = 0.30 × ADP`. That was fitted on ADP 1–48 and **extrapolated**. Checked
against the observed residuals across the whole board:

| ADP band | observed sd | `0.30 × ADP` | `0.30 × min(ADP, 70)` |
|---|---|---|---|
| 24–48 | 12.1 | 10.9 | 10.9 |
| 49–84 | 16.4 | 19.9 | 19.9 |
| 85–120 | 22.0 | **30.6** | **21.0** |
| 121–180 | 25.5 | **43.3** | **21.0** |

**Beyond pick 84 the proportional model over-disperses by 40–70%.** In the simulator this made
opponents draft players 100 picks out of position, which flattered every roster measured against
them. **Corrected everywhere to `sd = 0.30 × min(ADP, 70)`.** Doc 53's headline (0.135 was
2.4× too small) is unaffected — it was measured on ADP 1–48, inside the cap.

### B2. THE SIMULATOR CANNOT MEASURE MATT'S ABSOLUTE WIN PROBABILITY — stated, not fixed

Matt's board and the scoring share one projection, so his roster is optimal **by construction**
against the yardstick. Uncorrected, the sim had him winning 47–57% of titles, which is absurd.

This is the same circularity that killed the breakout definitions earlier this project. It cannot
be removed without an independent projection. It is **bounded** instead: opponents were given a
cheat-sheet behaviour (take the best VBD among the N players nearest the top of their noisy
board) and N was swept against doc 41's finding that a VBD rule is statistically level with these
managers.

| opponent window | Matt vs league | P(1st) | consistent with doc 41? |
|---|---|---|---|
| 1 (pure ADP) | +228 | 0.44 | no |
| 8 | +134 | 0.26 | no |
| **22** | **+64** | **0.10** | **yes — inside CI [−89.5, +62.3]** |

**Every result below is reported at window 22 with window 8 as a robustness check, and the two
agree on every sign.** Absolute probabilities are still not to be quoted as Matt's real odds.

---

## PART C — WHAT A BREAKOUT IS ACTUALLY WORTH

1,800 simulated seasons, current engine, window 22. A **breakout** is `form > 1.35` with 12+
games played.

| breakouts on your roster | seasons | **P(1st)** | P(top 6) | mean pts | E[payout] |
|---|---|---|---|---|---|
| 0 | 446 | **4.7%** | 52.9% | 1343 | $66 |
| 1 | 728 | **14.4%** | 73.6% | 1436 | $146 |
| 2 | 414 | **26.8%** | 84.8% | 1489 | $222 |
| 3 | 163 | **54.6%** | 95.7% | 1585 | $355 |
| 4 | 37 | **67.6%** | 97.3% | 1642 | $406 |

**Each breakout roughly doubles the title, and the returns are convex — the third is worth more
than the first.** You draw 0 about 25% of the time, 1 about 40%, 2 about 23%, 3+ about 12%.
`corr(breakouts, points) = +0.576`.

Busts matter less per unit: 1 bust → 31.0% title, 7 busts → 6.2%. `corr = −0.415`.

**Matt's instinct was correct.** Chasing breakouts is not a distraction from value; it is where
the title lives.

---

## PART D — BUT YOU CANNOT PICK THEM. THREE TESTS, THREE NULLS.

Against per-game `form`, n=324, everything observable at draft time:

| draft-day signal | spearman vs form | p |
|---|---|---|
| ADP (cheaper = more upside?) | −0.065 | 0.242 |
| projection level | +0.004 | 0.950 |
| **ADP rank minus projection rank** ("the market is sleeping on him") | **−0.079** | **0.157** |

**All null.** And the third one — the signal this project has circled for months — points the
*wrong way*. Split into quintiles:

| market-vs-projection gap | n | breakout rate | bust rate |
|---|---|---|---|
| market **highest** on him | 68 | 10.3% | 22.1% |
| q2 | 63 | 11.1% | 14.3% |
| q3 | 63 | 11.1% | 33.3% |
| q4 | 65 | 10.8% | 18.5% |
| **market lowest on him** | 65 | **3.1%** | 26.2% |

**The players the market is coldest on relative to the projection break out at one third the rate
of everyone else.** `[TESTED]` If anything, "sleeper by ADP gap" is a negative signal. It is not
significant on its own (p=0.157) so the honest statement is **no signal**, but there is certainly
no positive one.

**What IS predictable is dispersion, not direction:** `|form − median|` against ADP,
rho = **+0.256, p<0.001**; against projection level, rho = **−0.295, p<0.001**. Cheap players are
reliably *wider*. Nobody knows which way.

---

## PART E — SO DOES DELIBERATE RISK-TAKING HELP? SWEEP AND PAIRED TEST

Rule: `score = rollout + λ × (projection × the band's upside above its mean)`. λ=0 is the current
engine. **N=400 paired seasons, identical opponents and identical season luck across rules.**

**Window 22 (primary):**

| rule | mean pts | P(1st) | E[payout] | vs engine, paired |
|---|---|---|---|---|
| **rollout + LATE tilt, round 9+ (λ=1.5)** | **1442.7** | **18.5%** | **$162** | **+$1.9 [−9, +13], p=0.73** |
| rollout (current engine) | 1441.9 | 17.8% | $160 | — |
| static VBD + caps | 1429.0 | 14.8% | $145 | −$15.2 [−32, +2], p=0.18 |
| rollout + upside tilt everywhere (λ=1.0) | 1427.6 | 14.2% | $138 | **−$21.9 [−39, −6], p=0.10** |

**Window 8 (robustness):**

| rule | mean pts | P(1st) | E[payout] | vs engine, paired |
|---|---|---|---|---|
| **rollout + LATE tilt, round 9+** | **1479.1** | **31.5%** | **$230** | +$6.6 [−8, +21], p=0.18 |
| rollout (current engine) | 1476.2 | 28.8% | $224 | — |
| static VBD + caps | 1473.1 | 27.0% | $214 | −$10.0 [−27, +8], p=0.53 |
| rollout + upside tilt everywhere | 1447.0 | 21.5% | $182 | **−$41.4 [−60, −23], p=0.003** |

### Verdict

- **Chasing upside in rounds 1–8 is a measurable, significant mistake.** −$41 at window 8,
  p=0.003, and the same sign and a zero-excluding interval at window 22. It costs mean points
  *and* title odds. This is the clearest result in the document.
- **Chasing upside from round 9 is free and probably slightly good.** Positive on mean points,
  P(1st) and payout at both calibrations — **but not statistically resolved** (p=0.73 / p=0.18).
  Treat it as a **costless option, not a proven edge.**
- **The mechanism is arithmetic, not mysticism.** By round 9 the value gaps between candidates
  are a point or two, so buying dispersion costs almost nothing; in round 3 the gaps are 20+
  points, so buying dispersion costs real expected value.

---

## PART F — HOW MUCH IS DECIDED AT THE DRAFT AT ALL?

45 draft realisations × 45 season realisations, engine fixed, all cells sharing season luck.

| source of variation in your point total | share | sd |
|---|---|---|
| **which players you ended up with** | **1.9%** | 16 pts |
| **how the season went** | **67.6%** | 98 pts |
| interaction | 30.6% | — |

**Season luck is 6× larger than draft luck.** Best-vs-worst draft spread: 69 points.
Best-vs-worst season spread: 374.

And on title odds specifically, once corrected for sampling error the between-draft variance
in P(1st) is **zero** — the apparent 0.09–0.33 range across drafts is entirely the noise of
measuring each draft with only 45 seasons.

**Read this correctly.** It does **not** say the draft is irrelevant: doc 54 showed pick *rules*
differ by up to 84 points, and Part E shows a bad risk policy costs $41. It says that
**conditional on running a good rule, which particular players happen to fall to you is not what
decides your season.** Execute the policy; do not agonise over any single pick.

---

## WHAT THIS CHANGES

1. **Do not chase upside before round 9.** Costs $22–41 of expected payout. This is the
   actionable finding.
2. **From round 9, prefer the wider bet when candidates are within ~2 points.** Free, plausibly
   worth a little. Rounds 9–12 are picks **104, 113, 128, 137**.
3. **Stop hunting sleepers by ADP-versus-projection gap.** Tested, null, and directionally
   negative. This retires a line of inquiry that has consumed months.
4. **Keep the "keeper audition" logic in §6 — it already does the right thing** by concentrating
   speculative picks late.
5. **Update §4.12 to `sd = 0.30 × min(ADP, 70)`.**
6. **Never quote a simulated absolute win probability.** The board and the yardstick share a
   projection. Relative comparisons only.

## LIMITS

1. **n=324 player-seasons over two years** for the outcome model. Everything in Parts C–E rests
   on it. 2023's projections are dead and 2021/2025 lack games-played, so this cannot be widened
   without a new data source.
2. **The circularity in B2 is bounded, not removed.** All absolute probabilities are artifacts of
   the opponent calibration.
3. **`form` is drawn independently of player identity.** The simulator therefore *cannot* reward
   player-selection skill even if it existed. That is a deliberate consequence of Part D's nulls —
   but if a real breakout signal is ever found, Part E must be re-run before concluding anything.
4. **The late tilt is not significant.** Do not present +$2 to +$7 as an edge.
5. **Head-to-head standings use a random weekly schedule**, not the league's real one.
6. **The dispersion tilt uses ADP band as the risk proxy** because no per-player dispersion
   measure exists in the historical data. `FantasyPros_ECR_BestWorstStdDev.csv` exists for 2026
   but there are no historical Best/Worst files, so it cannot be backtested. **Untested.**

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **2022 and 2024 outcome dispersion transfers to 2026.** *Invalidated by:* a season where late
   picks stop being wider than early ones. Two seasons is thin; the band pattern is monotone and
   large, which is the reassuring part.
2. **Breakouts are unforecastable.** *Invalidated by:* any signal clearing significance against
   `form` out of sample. Three have now failed. This is the assumption most worth attacking, and
   the highest-value place to attack it is a per-player dispersion measure (expert rank spread,
   depth-chart security, age) rather than another value-versus-market construction.
3. **Expected payout is the right objective.** It embeds the $1,200 structure and dominates raw
   points as a target, which was Matt's original objection and is now answered — the engine is
   evaluated on dollars, not points.

**What would most improve this:** **historical FantasyPros Best/Worst/StdDev files.** They are the
one available per-player uncertainty signal, and without a historical capture the single most
promising remaining idea in Part D cannot be tested at all.
