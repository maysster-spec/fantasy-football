# 195 — Boom/bust is real, I measured the wrong thing, and the cause is volume

**2026-09-06 (T−1).** Matt: *"I am certain boom or bust players exist for fantasy, I just can't
tell you exactly why, and that is an area I feel needs your research."*

**Numbered 195, not 194+1, because of a live collision — see §5.**

## 1. MY ERROR: I TESTED SEASON-TO-SEASON VARIANCE. BOOM/BUST IS WEEK TO WEEK.

Doc 194 reported "deep receivers are not boom/bust" from the **spread of season-long beat vs
price** (Levene p=0.572). That measures whether a *season* lands where the market expected. It has
nothing to do with the thing Matt is describing, which is **whether you can trust him in your
lineup on a given Sunday.** A player can be perfectly predictable across a season and wildly
volatile inside it — and the weekly one is what a manager actually lives with.

**Re-measured properly.** Week-to-week coefficient of variation of half-PPR points, plus the share
of weeks a player scored ≥2× his own average (**boom**) or ≤half of it (**bust**).
**n=500 player-seasons, WR/TE, ≥10 games and ≥5 ppg, 2021–2025.**

## 2. HE IS RIGHT ABOUT DEEP RECEIVERS — AND IT IS A SMALL EFFECT

| route depth | n | ppg | week-to-week CV | boom weeks | bust weeks |
|---|---|---|---|---|---|
| SHORT / slot (aDOT < 9) | 201 | 8.7 | 0.675 | 8.4% | 25.3% |
| INTERMEDIATE (9–12) | 173 | 9.9 | 0.671 | 8.5% | 24.9% |
| **DEEP (12+)** | 126 | 9.0 | **0.709** | 9.1% | **28.6%** |

corr(aDOT, CV) = **+0.101, p=0.024**. corr(aDOT, bust rate) = **+0.135, p=0.003**.
**Real, significant, and small.** `[TESTED]`

## 3. THE ACTUAL MECHANISM IS VOLUME, AND IT IS FIVE TIMES BIGGER

| | correlation with week-to-week CV |
|---|---|
| **targets per game** | **−0.543** (p=1e-39) |
| points per game | −0.475 |
| aDOT (route depth) | +0.101 |

Both in one regression, n=500: **targets/game −0.0475 (t = −14.5)** · **aDOT +0.0056 (t = +2.75)**.
Route depth survives the control and is **one ninth the size**.

**THE LADDER — this is the answer to "why":**

| targets per game | ppg | CV | boom weeks | **bust weeks** |
|---|---|---|---|---|
| **under 4** | 6.1 | 0.854 | 12.4% | **34.0%** |
| 4–6 | 7.2 | 0.726 | 9.7% | 28.9% |
| 6–8 | 10.3 | 0.635 | 7.3% | 23.6% |
| **8+** | 13.6 | 0.558 | 6.0% | **18.6%** |

**A receiver seeing fewer than four targets a game busts in a third of his weeks. One seeing eight
or more busts in fewer than one in five.** Boom/bust is *low volume*. Deep receivers are boomy
mostly **because deep receivers get fewer targets**, not because the routes are long. The route
depth adds a real sliver on top of that, and only a sliver.

**Matt's four names fit the volume story, not the depth story:** Christian Watson 2025 — aDOT 17.8,
**30% bust weeks**, and 11.5 ppg on low volume. Shaheed — aDOT 11.5, 24% bust. Against Nacua at
aDOT 9.8, high volume, **7% bust weeks and CV 0.49**, the steadiest in the set.

## 4. TWO THINGS THAT FOLLOW, AND ONE THAT DOES NOT

**(a) You can forecast boominess — by forecasting volume, not by labelling the player.**
Week-to-week CV barely persists year to year (**r=+0.195**). **aDOT persists at r=+0.783.**
So "he's a boom/bust guy" is mostly a description of a season that happened. What *does* carry is
targets per game, and that is already the thing the board projects.

**(b) Being boomy does NOT cost you against price.** Prior-year CV vs next-year beat:
**r=+0.063, p=0.260**, and the boomiest quartile actually beat by **+6.9 more** than the steadiest.
**So volatility is a real property and NOT a fade.** It changes how you use a player — start him or
bench him — not what he is worth on draft day. `[TESTED — NULL as a pricing signal]`

**(c) What I cannot test:** his within-game mechanism — long strides, defensive backs wearing down
late. That needs snap-level and coverage data. **aDOT is depth, not stride length.** The mechanism
may be right; nothing here speaks to it.

## 5. A LIVE DOC-NUMBER COLLISION, NAMED NOT FIXED

**The project store holds `claude/193_weekend_injury_sweep.md` from an earlier session, and I wrote
`Source\193_the_red_zone_test.md` tonight.** I checked `Source\` for the next free number as §0.2
requires and 193 was free *there* — **the rule says list the folder, and the project store is a
second folder it never mentioned.** Two files now claim 193.

**Not renumbering tonight.** `make_tiers.py` carries "doc 193" in its docstring and is pinned;
renaming at T−1 means a code edit, a re-pin and a re-render for a filing problem. **Post-draft:
renumber mine to 197/198 and extend §0.2's folder-listing rule to cover the project store.**
This doc is 195 to avoid making it three.
