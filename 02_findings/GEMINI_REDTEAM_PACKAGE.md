# RED TEAM BRIEF — E-Discovery Keeper League 2026
**To:** Gemini Pro (or any second model) · **From:** Claude · **Updated Aug 22, 2026 · Draft Sept 7**

> **CHANGED SINCE THE AUG 21 DRAFT — read this box first.** A deterministic audit of all 32
> source files found 18 failures, two of them structural, and the 2025 holdout backtest has now
> been run. Four things in the version you may have already seen are **withdrawn**:
> 1. **The board's ADP column was a rank, not average draft position.** Zero of 341 rows matched
>    ESPN's real ADP. Every survival probability and the whole effective-ADP table inherit it.
>    Section 7 item 6 below — *"managers draft ~5 picks ahead of ADP"* — is almost certainly
>    this artifact and not behaviour.
> 2. **D/ST projections were never missing.** They were dropped by a name join. Real spread is
>    55.4 to 128.4 points.
> 3. **`herman allen is the only early-TE manager` is false.** Cary is the second, and he holds
>    1.01. First TE off the board by year: pick 22, 30, 20, 41, 22.
> 4. **The backtest headline is dead.** The value rule "beat" the owner by 277.5 points in 2025;
>    99% of that came from three season-ending injuries. Excluding them: +0.7, CI [−30.5, +32.6].
>
> **The one live result from the backtest, and the thing we most want you to attack:** the rule's
> outcome variance is **14% of a real manager's** (sd 76 vs 202 across twelve managers), and it
> lost to exactly the three managers independently rated best. See section 11.

## HOW TO USE THIS

Do not agree with me. Three specific jobs, in this order:

**(A) FACT-CHECK.** Every number here is claimed, not proven to you. Where a number is
checkable against public sources, check it. Where a claim rests on one season or one
source, say so and say what it would take to break it. **Search the web.** I have listed
sites below that I could not reach.

**(B) FIND WHAT WE LEFT OFF.** This is the main job. The owner's stated complaint is that
I only test what he names, and that he cannot be expected to think of every angle. Bring
metrics, benchmarks, roster-construction ideas, game-theory angles and in-season mechanics
that do not appear anywhere in this document. **A consideration we never thought of is
worth more than a correction to something we did.**

**(C) REVIEW THE DRAFT BOARD ITSELF** — the artifact, not just the analysis. Layout,
information density, what it shows at the moment of a 60-second pick, what it hides.

---

## 1. THE LEAGUE — unusual in three ways that matter

ESPN, 12 teams, 15 rounds, snake, **60 seconds per pick**. Starters 1QB 2RB 2WR 1TE 1FLEX
1DST 1K. Bench 6. **IR 3, separate from the bench.** Trades functionally dead (3 league-wide
per season). Payouts of $1,200: 1st **$525** · 2nd $225 · 3rd $150 · 4th $85 · 5th/6th $25.
Playoffs are 6 teams, weeks 15-17. Waivers reset weekly to inverse standings (not FAAB).

**Scoring, twelve components, verified to reconstruct ESPN's own totals to a max error of
0.197 points:** pass yd 0.04 · **pass TD 6** · INT −2 · rush yd 0.1 · rush TD 6 ·
rec yd 0.1 · rec TD 6 · **rec 0.5** · fumble lost −2 · **2PT +2 · kick-return TD +6 ·
punt-return TD +6.**

Nearly all public rankings assume full PPR and 4-point passing TDs. **The last three
components are scored by this league and ignored by essentially every ranking source.**

**Keepers.** One per team, charged to round 15, so the owner makes **14 selections: 8, 17,
32, 41, 56, 65, 80, 89, 104, 113, 128, 137, 152, 161. Pick 176 does not exist.** But all 12
keepers leave the board before pick 1, so the pool is depleted from the start: effective ADP
at pick 32 is ~37, at 41 is ~51. Both facts hold simultaneously and reviewers routinely
collapse them into one.

Owner drafts slot 8. Keeper: George Pickens (WR, bye 14).

---

## 2. THE OWNER'S RECORD — the model is not aimed at his actual failure

| season | wk 1-14 points | rank | seed | outcome |
|---|---|---|---|---|
| 2022 | 1580.2 | 2nd | 5 | won all three playoff weeks |
| 2023 | 1506.4 | 4th | 5 | lost wk16 by **1.4** (100.1-101.5) |
| 2024 | 1632.2 | 3rd | **1** | **lost the final 115.4-130.1** |
| 2025 | 1484.2 | 6th | 3 | **eliminated wk15 with a 70.6 (11th of 14), then scored 147.4 — the league's highest — the following week** |

He outscored the field in the postseason all four years (327/270, 384/267, 374/311,
330/292) and has no title. **The model optimises weeks 1-14. His losses are entirely in
15-17.** Attack this gap.

---

## 3. WHAT SURVIVED TESTING

- **Objective.** *(Now contested — see section 11.)* Week 1-14 starting-lineup points, validated against championship equity on
  1,250 paired seasons with the real schedule and bracket: Spearman +0.852 (replicated
  +0.863 under a corrected scorer). *Caveat: the sim gives the owner 33-44% title odds
  because simulated opponents never optimise a lineup. Convexity favours variance most for
  a MARGINAL team, and that regime is untested.*
- **Openings** (N=600): WR-RB-RB 1511.6 tops; RB-RB-WR, RB-RB-RB, WR-RB-TE, WR-RB-WR all
  within one SE (~8). **RB in round 2 appears in all six leading openings.** TE-RB-RB last.
- **Pick 8** (N=700): only Nacua beats Taylor (+32.1, t=2.85). Firmly negative: McBride
  −33.7, London −26.3, Allen −25.9, Jeanty −22.8, Love −18.8, Barkley −16.6, Cook −12.9.
- **Keeper**: Pickens beats Warren by 44.3 (t=−12.95, CI [−51.0,−37.6]) and Harvey by 67.1.
  Egbuka is the only live alternative (−4.0, t=−1.73).
- **Structure, five years of true picks, keepers excluded (n=834):** zero TEs inside pick 17
  in **all five years**; QBs through pick 32 = 2,2,3,3,3; rounds 1-4 are 82.8% RB/WR;
  median first D/ST round 12; first K round 11+ in 94.9%.
- **Franchise bias is real.** herman allen over-drafts Washington **z=4.08**; Kam over-drafts
  Kansas City z=3.46; Snyder over-drafts Buffalo z=2.32. *Caveat: ~384 manager-team
  combinations tested; only allen clears Bonferroni. The method earns credit because
  Snyder-Buffalo, identified by years of human observation, falls out unprompted.*
- **Variance-seeking is punished.** Sweeping a ceiling bias through the draft policy, 450
  paired seasons each: ceiling +15 costs **−$62.67** (t=−4.97) and 10 points of title rate;
  mild *safety* (−15) gains +$25.37 (t=+2.18). But **confined to running backs**, a mild
  youth tilt is free (+$0.85 at strength 5, title rate 0.438 vs 0.420).

---

## 4. WHAT DIED — twelve factors, three gates each

Gates: (1) year-over-year stickiness, (2) out-of-sample R² gain over prior-year points per
game with a bootstrap CI excluding zero, (3) survival after controlling for volume.

| factor | died at |
|---|---|
| offensive scheme | gate 2 |
| targets per route run | gate 2 (+0.0009, CI [−0.0003,+0.0020]); gate 3 partial r −0.000 |
| yards per route run | gate 2 (−0.0000) at every route floor from 25 to 200 |
| pass rate over expected | gate 2 (+0.002, team-clustered CI [−0.002,+0.006]); gate 3 partial r **−0.156, wrong sign** |
| NFL draft capital | cross-validated AUC 0.777 → **0.740**, worse |
| experience / year-2 leap | rookies 4.7%, yr2 **2.7%**, yr3 5.1%, yr4-5 4.9% — flat |
| vacated targets | partial r +0.007, p=0.88; per returning pass-catcher −0.011 |
| strength of schedule | **premise fails.** Defense-allowed-to-position does not persist within a season (RB +0.22/−0.20, WR −0.23/+0.18, TE +0.10/+0.07) or year to year |
| ranker disagreement | correlates 0.863 with ADP level; controlling for it, disputed players finish **worse** (−0.244, p=0.0009) |
| manager positional timing | 41 pairs, all \|r\| ≤ 0.15, all p ≥ 0.35 |
| athleticism · contract year · breakout age · BMI · OL quality · handcuffs | earlier sessions |

---

## 5. FOUR ERRORS I CAUGHT IN MY OWN WORK — look for more of this kind

1. **"GC was the best 2025 ranker, rho 0.665."** Artifact. I correlated (ADP − ranker)
   against (ADP − finish); they share a term. Partial correlation is **−0.423**: following
   GC *hurt*.
2. **"Team shrinkage slope 0.697."** One row had actual = 0 and levered the fit. Correct on
   n=32 is **0.371** (SE 0.049, t vs 1 = −12.81).
3. **"ESPN ADP is the worst market of seven" — RETRACTED THIS WEEK.** Built on a 183-player
   spreadsheet. Replicated on an independent 521-player FantasyPros export against the same
   2025 outcomes: ESPN **0.741** vs AVG 0.745, NFL 0.744 — statistically tied, and **2nd of
   6 inside the draftable range**, best of all at RB (0.74). The original was a coverage
   artifact. **The draft board's framing was built on this. That framing is now unsupported.**
4. **Name-join collisions, seven occurrences.** Most recent: first-initial + surname +
   position merged Javonte, Jameson and Josh Williams into one player and produced a fake
   league-leading edge. Adding team to the key cut matches from a phantom 280 to a real 166.

---

## 6. THE ONE UNEXPLOITED EDGE I FOUND, AND WHY I DISTRUST IT

**This league scores kick-return TDs, punt-return TDs and two-point conversions. Almost no
ranking source does.** ESPN's own projection contains them; the market's does not.

- 97 of 396 skill players carry return points in ESPN's 2026 projection
- 92 total return points and **204 two-point-conversion points** sit on the board
- correlation(return points, ADP) = **+0.203** — return men go late, the market is not paying
- but the top carrier is only **5.2 points** (Rashid Shaheed), mean among carriers 1.0

**So the mechanism is real and the magnitude looks trivial.** Two questions for you:
(a) is ESPN's projection *underestimating* return TDs, given they are high-variance events
a projection will regress toward zero? (b) 204 points of 2PT scoring across the board is
not trivial — who accumulates it, and is it priced?

---

## 7. WEAKNESSES — ranked. Break these.

1. **One season of projection-vs-outcome data. 24 breakouts total.** Every conditional
   subgroup test ran on 10-21 players. Several "nulls" above are **underpowered, not
   disproven.** Biggest hole in the entire project.
2. **The projection sources are a monoculture.** Within position, ESPN, FantasyPros-
   excluding-ESPN, six individual human rankers, consensus rankings and multi-site ADP
   correlate **0.915 to 0.992**. "Nothing beats the projection" may only mean "nothing
   beats consensus."
3. **Per-player disagreement survives that and is unexploited.** 30% of the top 150 have a
   30+ rank spread across six rankers, 11% have 50+. Jordyn Tyson: Boone 88, Pianowski 219.
   **I have not found a way to turn this into a decision and I believe one exists.**
4. **The playoff window is unmodelled** (see section 2). Schedule strength failed its
   premise, so what else raises weeks 15-17 specifically?
5. **The board's central column may be worthless.** It ranks by one analyst's deviation from
   ADP, measured on n=174, one season. The owner now says that analyst has turned
   conservative. **Assume the board needs a new organising principle and propose one.**
6. **Survival probabilities are likely optimistic.** League residuals show nearly every
   manager drafting *ahead* of ADP (mean ≈ −5 picks) beyond what keeper depletion explains.
   **WITHDRAWN Aug 22 pending recomputation.** The comparison ran board rank against observed
   pick numbers. Mean(rank − real ADP) across the same range is ≈ −5. Do not treat this as a
   behavioural finding until it is re-run on `adp_pick`.

---

## 8. WHAT WE COULD NOT GET — tell us where to find it

The owner names these analysts as the ones who actually find breakouts: **Matt Harmon
(Reception Perception), JJ Zachariason (Late-Round Fantasy), Shawn Siegele (RotoViz), Dwain
McFarland (Fantasy Life), Evan Silva (Establish The Run), Ben Gretch (Stealing Signals),
Ian Hartitz.** We have **no individual rankings from any of them.** Every file in hand is a
consensus or an aggregate: FantasyPros ECR gives only rank, best, worst and standard
deviation — no names behind the numbers.

**Please find, and tell us how to get:**
- individual expert rankings by name, current and historical, with dated snapshots
- **route-win-rate / Reception Perception** charting data (success vs man, press, zone)
- **PFF or Fantasy Life utilization** data: targets per route run, route participation,
  weighted opportunity, expected fantasy points
- **historical accuracy scoring of individual analysts** — FantasyPros publishes an
  Accuracy Contest; if the historical tables are reachable, that would settle empirically
  which analysts to weight, which is the question the whole project is stuck on
- anything giving **preseason projection AND outcome for the same players across 3+ seasons**

Sites we could not reach: fantasypros.com (accuracy contest and expert rankings),
receptionperception.com, establishtherun.com, rotoviz.com, fantasylife.com,
playerprofiler.com, 4for4.com, pff.com. **If any of this is free or has a free archive, say
exactly which URL and what it contains.** If it is paid, say which subscription buys the
most of the above for the least money before Sept 7.

---

## 9. THE DRAFT BOARD — critique the artifact

Two deliverables exist. Both are attached separately.

**A live HTML board.** Single file, offline. A sortable table of 364 players: position,
name, positional rank, team, ESPN ADP, one analyst's rank, the gap between them, VBD, bye.
Click to grey out a drafted player, shift-click to add to your own roster, undo. Buttons per
pick (8, 17, 32 ...) filter to only players live at that pick. Gold rules mark tier breaks
within a position. A right-hand panel holds hard rules, who picks in each gap and what they
need, franchise biases, and a fade list.

**An Excel grid** in the owner's own long-standing format: one row per round, columns for
QB / RB / WR / TE, each cell holding 3-4 ordered names, plus a column naming the positional
demand from the teams picking before his next turn.

**Questions:**
- What does a 60-second pick actually require on screen, and what is noise?
- The board sorts by an analyst-versus-market gap whose foundation just weakened
  (section 5, item 3). **What should the primary sort be instead?**
- What is missing entirely — roster balance state, positional run detection, opponent
  roster construction, bye distribution, something else?
- Is a single table right, or should it be position columns like the owner's own sheet,
  which he has used successfully for fifteen years?

---

## 10. FORMAT OF YOUR REPLY

Numbered sections matching 1-9. For every metric or strategy you propose, give:
**the metric · the exact data source and URL · the gate it must clear · the result that
would make you abandon it.** A proposal without a falsifier is not a proposal.

---

## 11. THE NEW QUESTION — attack this hardest

The 2025 holdout backtest ran the greedy value rule for **all twelve managers** on their real
draft slots, with ground-truth availability (the pool at each pick is everyone actually taken
later in the real draft, so the survival model is removed from the test entirely).

| | mean | **sd** | range |
|---|---|---|---|
| what the twelve managers actually scored | 1686 | **202** | 1498 – 2133 |
| what the rule would have scored | 1788 | **76** | 1634 – 1936 |

The rule beat 9 of 12 and **lost to exactly the three the opponent model already names as best**:
Lobsinger −196.3 (reigning champion), R Taylor −182.0 (never worse than 5th), Rychlicki −41.1.

`corr(actual, delta) = −0.929` is mechanical and we know it — delta is `rule − actual`. The part
that is not mechanical is the **variance of the rule's own output**, measured across twelve
independent draft positions.

**The owner's payout structure is 44% of the pot to first place, and his losses are entirely in
weeks 15–17. He has finished 2nd, 4th, 3rd and 6th in points with no title.** A rule that
compresses outcomes into a 300-point band is buying a floor he does not need.

This directly contradicts the project's own simulation, which found variance-seeking punished
(ceiling +15 costs −$62.67, t = −4.97) — but that sim was calibrated on opponents who never
optimise a lineup and gives him 33–44% title odds, which is not a real regime.

**Four things we want from you on this, each with a falsifier:**
1. Is the variance compression real or an artifact of a one-season, season-total scoring rule?
2. What is the correct objective for a payout structure this top-heavy in a 12-team, 6-team-
   playoff league? Show the maths, not an opinion.
3. What roster-construction choices actually raise a weeks-15-to-17 ceiling, given that strength
   of schedule survives only as a tiebreaker (whole 32-team spread: 10.4 points at RB over
   fourteen weeks, ≤5.5 in weeks 15–17)?
4. The obvious test is to re-run the manager-level backtest on 2022, 2023 and 2024. That needs
   preseason projections for those years, which we do not have. **Where do free, dated,
   historical preseason fantasy projections live? Name URLs.**

---

End with: **the three things we are most likely to be wrong about, ranked.**
