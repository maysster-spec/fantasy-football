# 221 — The bad-team dart, tested: Tennessee's touchdowns are real, the general rule is not

**2026-09-08 (draft +1).** Matt, on dropping Tyjae Spears:

> *"if he doesn't take over he has zero for FF, and if he does take over he has little upside
> because the team is just that bad… There will not be enough TDs to justify the pick."*

**Two claims, and they resolve differently.** The Tennessee-specific one is confirmed by the board's
own projection. The general one — that a dart on a backup behind a bad offence pays less — looks
strong pooled and dies the moment you vary the input. §0.5(a2): the testable form was stated before
the run, and it is quoted in §2 below.

---

## 1. THE TENNESSEE CLAIM IS CONFIRMED — `[TESTED]`

Team offensive touchdowns, projected, from the **09-03 pull's `raw_stats`** summed over every
rostered player (rushing id 25 + receiving id 43; §3's stat-id rule — these are the *projection*
ids, checked on real rows):

| rank | team | projected rush + rec TDs |
|---|---|---|
| 1 | LAR | 55.5 |
| 2 | BUF | 54.6 |
| 3 | DET | 51.0 |
| … | | |
| 29 | ARI | 29.6 |
| **30** | **TEN** | **29.2** |
| 31 | CLE | 26.4 |
| 32 | MIA | 25.3 |

**League mean 38.9, median 41.4. Tennessee is 30th of 32, twelve touchdowns below the median.**
He is right, and the board already knew it — the number was simply never surfaced anywhere he
could read it.

Combined with §4.20's `job worth` of **171** for the Tennessee backfield, the arithmetic on Spears
is closed without any of what follows: **the whole job, won outright, is an RB3 season on the
third-worst scoring offence in the league.**

---

## 2. THE GENERAL CLAIM — STATED, THEN TESTED, THEN KILLED

**THE TESTABLE FORM, written before the run (§0.5(a2)):** *among running backs priced in the dart
band, the beat against price is lower for a back joining a bad offence than for one joining a good
offence, and this gap is larger for darts than for early-round backs.*

**POPULATION:** 171 RB player-seasons, 2022→2023 through 2024→2025, from the doc-189 panel.
**BASELINE — state it every time: half-PPR points, weeks 1–14 of year *t+1*, regressed on
log(preseason ADP) within season. BEAT = the residual.** ADP from the §1.1 registry, never a
historical `espn_adp`.
**PREDICTOR:** the offence he is *joining*, graded on the season the drafter can actually see —
that team's rushing + receiving touchdowns in year *t*, from nflverse weekly, expressed as a
within-season percentile. Team resolved as the player's modal team in the outcome season.
**ERRORS CLUSTERED BY TEAM**, because team offence is a team constant (§4.24(c), `ERROR_PATTERNS`
A5 — the trap that has now bitten this project four times).

### 2a. Pooled, it looks like a finding

| population | worst-to-best offence, points of beat | p |
|---|---|---|
| **all RBs** | **+31.2** (se 13.1) | **0.018** |
| early RBs, ADP < 90 | **+48.5** (se 20.5) | **0.018** |
| darts, ADP ≥ 90 | +22.3 (se 18.0) | 0.215 |

By band, all RBs: **top-10 offence +7.3 · middle 12 −1.9 · bottom-10 −16.0.** Monotone, and in
Matt's direction.

### 2b. And then ONE SEASON turns out to carry all of it — `ERROR_PATTERNS` A19

| transition | coefficient | p | n |
|---|---|---|---|
| 2022 → 2023 | **−8.0** | 0.779 | 45 |
| 2023 → 2024 | +25.7 | 0.196 | 64 |
| **2024 → 2025** | **+63.0** | **0.000** | 62 |

**Leave-one-season-out:** without 2022 **+44.6**, without 2023 **+34.3**, **without 2024 +11.8,
p=0.526.** Drop the single season that carries it and the effect is indistinguishable from zero.

**This is doc 189's M4 shape exactly** — the draft-capital finding that looked real at −13.0 and
collapsed to 2022 reversing outright. It is why the by-season cut is run before anything is
believed. `[TESTED — NOT ESTABLISHED]`

### 2c. And the dart half points the WRONG way

The interaction Matt's mechanism requires (§0.5(a3): always look for it, expect substitution):

| term | effect | p |
|---|---|---|
| team offence percentile | **+45.9** | 0.021 |
| dart (ADP ≥ 90) | −14.3 | 0.402 |
| **offence × dart** | **−27.7** | **0.328** |

**Null, and the point estimate is NEGATIVE — offence quality matters LESS for a dart, not more.**
The split-sample numbers say the same thing: +48.5 for backs priced under 90, +22.3 for darts.
**If joining a good offence is worth anything, it is worth it to the back you are paying for, not
to the lottery ticket.** That is the opposite of the mechanism as stated.

The one cell that does support him: **darts on a bottom-10 offence beat by −12.8**, against +1.3
for the middle twelve. Twenty-two player-seasons. **A shape, not a finding.**

### 2d. Other positions, for the record

Same model, all price levels: **WR +12.7 (p=0.069) · TE +2.0 (p=0.881) · QB +65.5 (p=0.011).**
The QB number is unsurprising and probably mechanical — a quarterback *is* his offence — and was
not pursued.

---

## 3. WHAT THIS CHANGES

**Nothing on any board, and that is the point.** The Spears decision stands on the two numbers in
§1: a 171-point job on the 30th-ranked scoring offence. It does not need a general rule, and the
general rule it looked like it might support is one season of data.

**The standing instruction this earns:** *do not fade a dart for playing on a bad team as a rule.*
Fade the specific job when the specific job is small. §4.20's **buy the job, never the name** now
has a companion — **grade the job, not the team.**

**What would resolve it:** the 2021→2022 and 2025→2026 transitions, which would take n from 171 to
roughly 280 and would say whether 2024 was the outlier or the other two were. §4.24(b)'s
distinction applies: this failed **POWER and STABILITY**, not prediction. Post-season item.

---

## 4. TWO DEFECTS IN `MY_PLAYER_CARDS_2026.html`, BOTH MINE, BOTH FIXED

1. **"The only player you drafted carrying ALL THREE measured back signals"** — false. **Jeanty is
   also 3/3**, and his own card said so four cards earlier. The composite is 3/3 for Jeanty
   (14.8% target share, 17 games, NFL pick 6) and Spears (12.0%, 13 games, NFL pick 81).
2. **"N rankers higher than the market."** Wrong object. `calls_up` counts **podcast target calls**,
   which is what `live_draft.COLGLOSS` itself says — *"CALLS: podcast target calls only"* — and it is
   a far weaker thing than a ranking panel. Relabelled on all five cards that carried it.

**And the provenance of the Spears calls matters, because he asked for them:** all three
(Chris/Fantasy Endgame, Justin Boone, Pat Fitzmaurice) carry `episode_date = UNKNOWN` in
`raw-analyst-calls-v2.csv`, the scrape **doc 103 graded unusable** — mixed 2024 and 2025 vintages
and phonetic transcription errors. Two of the three render him **"Tai Spears."** Matt's own read —
*"those takes were from earlier grades when there was hope for Ten"* — is consistent with the file
and cannot be confirmed from it, because the file has no dates. `[SOURCED, undated]`

---

## 5. THE RECORD ON HIS TAKES (`ERROR_PATTERNS` F4)

F4 says a **price or process** he calls wrong is evidence, and a **causal mechanism** he proposes is
a hypothesis. **This one split down the middle, in a single message.** The price read — Tennessee
will not score enough to justify the pick — is confirmed at 30th of 32. The mechanism — bad teams
cap darts generally — is not established. Both halves behaved exactly as F4 predicts.
