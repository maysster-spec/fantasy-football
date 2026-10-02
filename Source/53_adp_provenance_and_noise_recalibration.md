# 53 — ADP PROVENANCE RULE, AND §4.12'S NOISE COEFFICIENT IS 2.4× TOO SMALL
**Aug 26, 2026.** Triggered by Matt's rule: *"ADP before the draft is the correct measure for
projecting 2026, and for prior years draft prep. The prep doesn't include knowing the actual ADP
when the draft is over."* Two things came out of enforcing it — one guard, one live finding that
changes the draft plan.

---

## THE ANSWER, IN ONE LINE

**Every survival number this project has produced is overconfident.** §4.12's opponent-noise
coefficient (`sd = 0.135 × ADP`) was fitted on contaminated ADP. Refitted on five seasons of
genuine preseason boards: **k = 0.323, bootstrap 95% CI [0.279, 0.363]** — 2.4× larger.
**Recommend 0.30.** The practical effect is that the 32→41 cliff in §2.1's turn-structure table
is roughly half as steep as advertised, and pick 41 is not the dead zone the directive says.

---

## PART A — THE PROVENANCE RULE, MADE ENFORCEABLE

### A1. Why this is a hard refusal, not a threshold

ESPN's player endpoint serves ONE `averageDraftPosition` field. Re-pulled after a season ends it
has drifted toward what happened. **The drift is not a broad shift — it is concentrated in exactly
the players whose outcome diverged from their preseason price**, which is the worst possible
place for it, because those are the players a backtest turns on.

| season | player | ESPN historical `espn_adp` | contemporaneous preseason | what happened |
|---|---|---|---|---|
| 2024 | Christian McCaffrey | **16.0** | consensus rank **1** | missed the season |
| 2024 | Saquon Barkley | **3.4** | consensus rank **17** | MVP-caliber year |
| 2024 | Alvin Kamara | **8.3** | consensus rank **~50** | RB1 pace early |
| 2023 | Puka Nacua | **44.0** | Underdog ADP **216** | undrafted → WR5 |
| 2022 | Jonathan Taylor | **7.1** | FantasyPros ADP **1** | injured, RB25 finish |

`[SOURCED: espn_projections_{2022,2023,2024}_20260824.csv vs the registry in A3]`

### A2. THE DETECTOR I TRIED TO BUILD, AND WHY IT IS WITHDRAWN

**Hypothesis:** a contaminated column can be detected by `|spearman(adp, actual)|`, because a real
preseason market predicts the finish only weakly (doc 51 measured 0.352 clean vs 0.594 dirty).

**[TESTED]** — and it fails in **both** directions on the population `adp ≤ 180`:

| file | rho | verdict at a 0.48 threshold |
|---|---|---|
| clean 2022 contemporaneous board | **0.551** | **rejected — FALSE POSITIVE** |
| contaminated 2023 ESPN pull | **0.339** | **accepted — FALSE NEGATIVE** |

Clean seasons span 0.26–0.62; contaminated seasons span 0.18–0.80 depending on where the
population is cut. **The distributions overlap completely. No threshold separates them.** The
cause is A1: drift concentrated in a handful of players barely moves an aggregate rank
correlation. **Aggregate checks cannot find this defect.** Withdrawn, and recorded in the guard
so it is not rebuilt.

> Worth naming: doc 51's 0.352-vs-0.594 contrast is real but it is **not a usable test**. It
> separates those two specific files; it does not separate the classes. I nearly shipped it as a
> guard on the strength of a single comparison. Caught by running the negative control.

### A3. WHAT SHIPS INSTEAD — a preseason ADP registry, and an unconditional refusal

`code_adp_guard.py` exposes two calls:

- `load_preseason_adp(season)` — the only sanctioned way to get a completed season's market.
- `refuse_historical_espn_adp(df, season)` — raises unconditionally for any season < 2026.

**Registry built this session. All five are genuine preseason captures; none existed in the
project before today:**

| season | n | source | note |
|---|---|---|---|
| 2021 | 200 | `Combined_Rankings_rankings_with_adp.csv :: ADP#` | |
| 2022 | 196 | `Rankings vs ADP - 2022.xlsx :: FP_ADP` | |
| 2023 | 311 | `nfl_rankings-1.xlsx :: Underdog ADP` | **best-ball market — disperses wider than redraft** |
| 2024 | 348 | `FantasyPros-consensus-rankings 2024 :: consensus rank` | **rank proxy, not an ADP** |
| 2025 | 183 | doc 52 `backtest_2025 :: nine-site ADP` | |

Sanity: 2021 opens McCaffrey/Cook/Henry; 2022 Taylor/Ekeler/McCaffrey; 2023 Jefferson/Chase/
McCaffrey; 2024 McCaffrey/Lamb/Hall; 2025 Chase/Bijan/Barkley. All are the correct preseason
boards for their year.

**Side effect worth flagging: 2023 is now partially alive again.** Its *projections* remain dead
(docs 40/41, confirmed three ways), but its *draft market* is recoverable, so any ADP-based test
can now include 2023. That is why the refit below has five seasons and not three.

---

## PART B — THE LIVE FINDING: §4.12's NOISE COEFFICIENT

### B1. Method

For each season: rank the real non-keeper picks 1…N, re-rank the contemporaneous preseason board
over the **keeper-depleted** pool, and measure the residual. **Removing keepers from both sides is
essential** — the first attempt left them in and produced a mean residual of +11.3 in the early
band, pure artifact of 2021–23 keepers occupying round 1. Corrected, mean residuals sit at −5.6 to
+1.9 across all five seasons, i.e. no systematic bias, pure dispersion.

The observed residual is not the parameter — sorting noisy draws re-orders the board, so the
observed dispersion runs **~1.2–1.3× larger** than the underlying `k`. The mapping was simulated
(600 reps per grid point, 12 keepers pulled from ADP 21–48 to match this league) and inverted.

**Population: ADP 1–48 only.** Later bands carry selection bias — players who went undrafted are
absent from the sample, so the drafted survivors artificially fill early slots. Band (120, 200]
shows exactly that, mean residual −10 to −14 in every season.

### B2. Result — five seasons, five independent sources, two keeper structures

| season | keeper round | matched n | early n | mean resid | observed k |
|---|---|---|---|---|---|
| 2021 | 1 | 129 | 47 | −1.1 | 0.365 |
| 2022 | 1 | 128 | 47 | +0.3 | 0.391 |
| 2023 | 1 | 140 | 47 | −2.3 | 0.574 |
| 2024 | 15 | 151 | 47 | −5.6 | 0.362 |
| 2025 | 15 | 132 | 48 | +1.9 | 0.347 |
| **pooled** | — | **680** | **236** | — | **0.414** |

**k = 0.135 would produce an observed 0.155. We observe 0.414.**

**[TESTED] Inverted point estimate k = 0.323, bootstrap 95% CI [0.279, 0.363], n = 236.**
2023 is the high outlier at 0.574 and the reason is known — Underdog is a best-ball market, which
disperses wider than this league's redraft behaviour.

**Leave-one-season-out — no single season drives it:**

| dropped | k | | dropped | k |
|---|---|---|---|---|
| none | 0.320 | | 2023 | **0.290** |
| 2021 | 0.331 | | 2024 | 0.331 |
| 2022 | 0.326 | | 2025 | 0.334 |

Worst case — dropping the best-ball season — is still **2.1× the directive's value**.

### B3. RECOMMENDED CHANGE

> **CORRECTION, Aug 26 (doc 55 §B1).** The proportional form below was fitted on ADP 1–48 and
> extrapolated. Checked against the observed residuals across the whole board, it over-disperses
> by 40–70% beyond pick 84 (band 121–180: observed sd 25.5, proportional model 43.3). The
> corrected form is **`sd = 0.30 × min(ADP, 70)`**, which reproduces every band. The headline
> finding — 0.135 is 2.4× too small — is unaffected, having been measured inside the cap.

**§4.12: `sd = 0.135 × ADP` → `sd = 0.30 × min(ADP, 70)`.** 0.30 sits inside the CI and matches the
conservative drop-2023 case. The TE +15 correction and the Snyder q≈0.85 behavioural term are
untouched by this and stay.

### B4. WHAT IT DOES TO THE DRAFT PLAN

p(available), old k=0.135 → new k=0.30, 8000 sims on `board_v7_2026`, keeper-depleted `eff_pick`,
TE +15 applied. Full table in `survival_v9.csv`.

**Pick 17 — the top of round 2 is far more open than modelled:**

| player | pos | eff ADP | old | new |
|---|---|---|---|---|
| Ashton Jeanty | RB | 16.6 | 0.10 | **0.49** |
| Saquon Barkley | RB | 15.8 | 0.05 | **0.42** |
| Derrick Henry | RB | 19.1 | 0.44 | **0.66** |
| Drake London | WR | 18.6 | 0.37 | **0.63** |
| James Cook III | RB | 12.6 | 0.00 | 0.15 |

**Pick 32 — things the model called dead are live:**

| player | pos | eff ADP | old | new |
|---|---|---|---|---|
| Breece Hall | RB | 31.1 | 0.07 | **0.45** |
| Malik Nabers | WR | 32.5 | 0.16 | **0.51** |
| Josh Jacobs | RB | 33.4 | 0.21 | **0.54** |
| Lamar Jackson | QB | 34.4 | 0.27 | **0.58** |
| Trey McBride | TE | 20.4 | 0.36 | **0.62** |
| A.J. Brown | WR | 26.1 | 0.00 | 0.22 |

**Pick 41 — this is the biggest correction in the document. §2.1 calls 41 the steep-attrition
pick. It is not:**

| player | pos | eff ADP | old | new |
|---|---|---|---|---|
| Brock Bowers | TE | 23.2 | 0.05 | **0.40** |
| Jayden Daniels | QB | 40.6 | 0.13 | **0.48** |
| Jalen Hurts | QB | 41.2 | 0.16 | **0.51** |
| Emeka Egbuka | WR | 39.3 | 0.08 | **0.43** |
| Davante Adams | WR | 38.4 | 0.06 | **0.42** |
| Ladd McConkey | WR | 41.4 | 0.16 | **0.51** |
| Kyren Williams | RB | 36.5 | 0.02 | **0.34** |

**§2.1's cited attrition figures (Warren 0.90→0.15, Egbuka 0.79→0.05, Daniels 0.94→0.30,
Lamar 0.40→0.00) are all built on k=0.135 and overstate the drop.** Corrected: Warren 0.92→0.48,
Egbuka 0.70→0.43, Daniels 0.73→0.48, Lamar 0.58→0.25.

**Pick 56 — round 5 is a different pick than modelled:** Odunze 0.05→0.51, Swift 0.05→0.51,
Warren 0.03→0.48, DJ Moore 0.02→0.44, Burrow 0.00→0.33.

### B5. THE STRATEGIC READ — and it cuts both ways

Higher noise does **not** simply mean "you can wait." It means the board is less predictable in
both directions. Two consequences:

1. **Name-based plans get weaker; tier-based plans get stronger.** "Bowers at 41" was 0.05 and is
   now 0.40 — still a coin flip you lose more often than not. But *"one of Bowers / McBride /
   Warren at 41"* is now a strong favourite where before it was near-hopeless. Plan the tier.
2. **Players you assumed were locked at your pick are not.** A.J. Brown, Nico Collins and Omarion
   Hampton all drop from 0.97 to 0.88 at pick 17. Nothing above eff-ADP ~26 is safe at 17 any more.

**This does not reopen §4.10's strategy ranking** (WR-RB-RB etc.) — those were paired sims whose
relative ordering is not obviously noise-sensitive. **`[HYPOTHESIS]` that it survives; untested.**
Re-running §4.10 at k=0.30 is the single most valuable outstanding compute job.

---

## LIMITS

1. Five seasons, one league, n=236 early-band observations. The CI reflects it.
2. Sources are heterogeneous by necessity — 2023 is best-ball, 2024 is a consensus rank not an
   ADP. Both are contemporaneous, which is the property that matters, but they are not the same
   instrument. The leave-one-out table is the defence.
3. The sort-compression inversion is simulated against a stylised 180-player pool, not this
   league's exact structure. It moves the estimate by ~20%; a mis-specification there would not
   close a 2.4× gap.
4. The refit says nothing about *whose* picks are noisy. Per-manager noise is unmodelled and
   §4.12's `[HYPOTHESIS]` on RB/WR pace gaps is untouched.
5. `survival_v9.csv` excludes the Snyder/Josh Allen behavioural override, so **Allen's numbers
   there are not comparable to §4.2's 0.14** — that figure carries the q≈0.85 term and this one
   does not.

---

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **The five registry files are genuine preseason captures.** *Invalidated by:* a datestamp
   inside any of them post-dating that season's Week 1, or a top-5 that includes a player who was
   not a first-round name that August. Checked by eye; not checked against file metadata.
2. **Residual dispersion in ADP 1–48 identifies the model's noise parameter.** *Invalidated by:*
   the dispersion being driven by systematic manager preference (a tier the league collectively
   ranks differently) rather than randomness. The near-zero mean residual argues against it but
   does not rule it out.
3. **k is constant across the board.** The band table shows implied k falling from ~0.36 early to
   ~0.20 by pick 100. *Invalidated by:* it already is, partly — but the later bands carry the
   selection bias in B1, so a proportional model is the honest default rather than a fitted decay.

**What would most improve this:** a **sixth season, or a second league's draft history**, to break
the n=5 ceiling. Second-best: the actual ESPN live-draft timestamps from 2025, which would let
per-manager noise be fitted instead of assumed common.
