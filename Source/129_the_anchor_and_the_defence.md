# 129 — Two guesses tested: the defence/QB mechanism, and drafter anchoring

*2026-09-01. Matt, on doc 128: "teams who have great defense and not great QB play lean on the run
more I would guess. plus, the average drafter may not be as keen and be biased by previous years
targets/production."*

**Both were testable. The first is half right and unforecastable. The second is right about the
market and backwards about the payoff — and chasing it leads straight into the one injury signal
this project CAN test, which says do the opposite.**

---

## 1. THE MECHANISM: good defence, bad QB, more running  `[TESTED, n=128 team-seasons]`

nflverse 2022–2025. Pass rate = attempts / (attempts + carries). Defence measured as total
offensive EPA opponents generated against the team (lower = better). QB quality as passing EPA
per attempt.

| | r with pass rate | p |
|---|---|---|
| QB passing EPA per attempt | **−0.184** | 0.038 |
| defensive EPA allowed (higher = worse D) | +0.104 | 0.242 |
| both, standardised | QB −0.174 · defence +0.085 | R² = **0.041** |

**The defence half matches your direction but does not reach significance. The QB half is
significant and points the opposite way** — teams with *worse* QB play threw **more**, not less.
That is game script beating coaching intent: a bad offence trails, and trailing teams throw. The
coach's plan to lean on the run survives about as long as the second-quarter deficit.

Together the two explain **4%** of pass-rate variance.

## 2. AND IT IS NOT KNOWABLE A YEAR AHEAD  `[TESTED, n=96 transitions]`

| prior-year predictor → next-year pass rate | pooled r |
|---|---|
| prior defensive EPA allowed | **−0.115** *(sign flips vs the contemporaneous +0.104)* |
| prior QB EPA per attempt | −0.183 |
| **prior pass rate** | **+0.440** |
| *and: defensive quality's own year-to-year stability* | **+0.204** *(corrected — doc 131)* |

**NFL defences persist weakly — r = +0.204 season to season** on EPA per play allowed, n=160
transitions 2020–2025. *(This corrects the +0.113 first published here, which used season-TOTAL EPA
on a 3-transition window — see doc 131. The direction survives; the number was wrong by nearly 2×.)*
An offence persists at +0.382, so a defence carries about **4%** of next year's variance and an
offence about **15%**. Weak, weaker than the offence, but **not zero** — and nowhere near enough
to know in August which defence will be good in November. The best available predictor of
next year's pass rate is last year's pass rate, and that is already inside ESPN's projection.

This does not change doc 128's magnitude. A better story about the 7.5% is still the 7.5%.

## 3. THE MARKET *IS* ANCHORED ON LAST YEAR — you are right  `[TESTED, n=409]`

Using the sanctioned preseason boards only (`code_adp_guard.load_preseason_adp`: 2022 FantasyPros
ADP, 2024 FantasyPros consensus rank), never `espn_adp` from a historical pull (§1.1). Regress
ADP rank on ESPN's projection rank **and** last season's fantasy-point rank, standardised:

| season | n | loading on the PROJECTION | loading on **LAST YEAR'S POINTS** | R² |
|---|---|---|---|---|
| 2022 | 174 | +0.726 | **+0.093** | 0.638 |
| 2024 | 235 | +0.608 | **+0.263** | 0.693 |

**After the projection is accounted for, the market still leans on last year's box score.** Your
read of the room is correct, and it is measured on an independent market, not ESPN's own board.

## 4. BUT FADING THE ANCHOR LOSES MONEY  `[TESTED, n=409]`

Divergence = ADP rank minus projection rank. Positive means the market is *cheaper* than the
projection — exactly the player an anchoring story says to buy.

| season | n | rho(market is cheap, beats his projection) | p |
|---|---|---|---|
| 2022 | 174 | **−0.275** | <0.001 |
| 2024 | 235 | −0.093 | 0.156 |
| **pooled** | **409** | **−0.173** | **<0.001** |

Negative. **The players the market prices below the projection go on to MISS the projection by
more, not beat it.** This is an independent replication of §4.13's retired signal — rho −0.079 on
324 player-seasons, a different population and a different ADP source — and it comes back
*stronger* here. When the market and the projection disagree, the evidence says the market is the
one that is right.

So the anchoring is real and it is not a mistake. Drafters are not being dumb about last year;
last year carries information the projection under-weights.

## 5. WHICH INFORMATION? AVAILABILITY. AND IT IS THE SHARPEST THING IN THIS DOC

Split the same 402 players by how many games they played the **previous** season:

| last season | n | market's discount vs the projection | **mean beat vs projection** |
|---|---|---|---|
| played 13+ games | 294 | median −10.0 slots (mean −1.5) | **−12.4 pts** |
| **missed time (≤12 games)** | **108** | median −2.0 slots (mean +4.0) | **−28.2 pts** |

The market does discount them — by about **5 to 8 rank slots** depending on which centre you take
— it simply does not discount them nearly enough.

**Difference −15.8 points, Welch p=0.039.** Controlled for position, log(ADP) and season:
**−16.2, se 7.2, p=0.025.**

**By position it is entirely a receiver effect:**

| | n hurt | mean beat | n healthy | mean beat | difference | p |
|---|---|---|---|---|---|---|
| **WR** | 45 | −37.3 | 130 | −11.9 | **−25.4** | **0.003** |
| RB | 40 | −6.9 | 83 | −12.6 | +5.7 | 0.63 |

**The mechanism is recurrence, and that half rests on a large sample** `[TESTED, n=1,806 pairs]`:
prior-season games played predicts next-season games played at **r = +0.50** overall. A WR who
missed time last year averages **9.1 games** the following season against **12.7** for one who did
not — **3.7 games fewer**. RB −4.3, TE −4.7, QB −6.5, all the same direction.

**This closes a gap doc 42 left open.** Doc 42 established that ESPN prices *average* availability
(it projects 15.32 games, actual 14.46) and correctly refused a flat per-position haircut as
double-counting. What it could not test was whether availability is *differentially* predictable —
its historical `injuryStatus` is stamped at the 2026 capture date, not preseason, so August flags
remain untestable. **Games played last season carries no such contamination, and it is predictive.**
The market discounts these players by about 5.5 rank slots. Against a 3.6-game shortfall, that is
not nearly enough.

### The board did not carry this, and it changes live rows

The injury sweep asks *is he hurt now*. This asks *did he miss time last year*, which is a
different question with a measured answer. Cross-referenced against `player_context.csv`, these
drafted-range WRs played ≤12 games in 2025 and are graded **NEUTRAL, "no injury news found"**:

**Drake London (12 g, adp 19) · Garrett Wilson (7 g, adp 37) · Terry McLaurin (10 g, adp 60) ·
Rome Odunze (12 g, adp 65) · Marvin Harrison Jr. (12 g, adp 82) · Travis Hunter (7 g, adp 120) ·
Jayden Reed (5 g, adp 132) · Chris Godwin Jr. (9 g, adp 133)**

Three of them — Harrison, Reed, Godwin — carry **BUY**, meaning both analyst panels have them
ahead of ADP. **McLaurin at 60 and Odunze at 65 are live at picks 56 and 65; Harrison at 82 is
live at pick 80.** These are not hypothetical rows.

**SHIPPED: `make_board.py` now prints a `12g` badge** on any player who played fewer than 13 games
in 2025, from a committed `Source\games_2025.csv` (static — 2025 is over, so it is a file, not a
script). 46 of 180 rows carry it. **Surfaced, deliberately not scored** — the same call doc 42 made
for injury status, and for the same reason: turning −25.4 points into a VBD haircut would be
inventing a coefficient off one measurement.

## 6. HOW MUCH TO TRUST §5

**The recurrence half is solid**: n=1,806 pairs, four transitions, same direction at every
position. **The dollar half is one measurement on a thin sample**: 45 hurt WRs across two seasons,
and I tested two positions and one hit, which halves the effective significance. The controlled
pooled estimate (−16.2, p=0.025) is the more conservative number and the one to carry.

Two confounds I did not resolve: coming-off-injury players may be older, and "≤12 games" lumps a
Week-2 ACL in with a three-game hamstring. Both would be worth splitting with more seasons.

**Treat as: a WR who missed real time last season is likely to miss more, the projection does not
know it, and the market only half knows it. Worth a badge and a pause. Not worth a number.**

## Assumptions, and what would break them

1. **Two seasons of preseason ADP joined to two seasons of ESPN projections.** 2023's projection
   pull is empty; 2021's and 2025's were never taken. A third season could move §4 and §5 either
   way — §5 more than §4, because §4 replicates an existing result and §5 does not.
2. **2024's "ADP" is a FantasyPros consensus *rank*, not a true ADP** (registry manifest says so).
   Rank and ADP correlate tightly but are not identical; the 2022 row uses a real ADP and shows
   the *stronger* §4 effect, so the conclusion does not depend on the proxy.
3. **§1's defence measure is EPA allowed, not points allowed.** Special teams and field position
   are absent. The instability result (r=+0.113) is robust to this; the level is not.

**Most valuable missing input:** preseason ESPN projection pulls for 2023 and 2025. The same two
files that would resolve doc 128 would take §5 from 45 hurt receivers to roughly 90.


---

## 7. Reproducing it

`Scripts\anchor_study.py` — every number above.

```
py anchor_study.py              all six sections
py anchor_study.py --mechanism  §1-§2 only (nflverse only, no ESPN files needed)
py anchor_study.py --market     §3-§6
```

Needs the two usable ESPN projection pulls (2022, 2024), the preseason ADP registry, and nflverse
weekly stats **2021**–2025 in `Source\nfl\`. It never reads `espn_adp` from a historical pull
(§1.1). Run end to end 2026-09-01; the output in this doc is that run.

`Scripts\make_board.py` + `Source\games_2025.csv` carry the badge. `DRAFT_BOARD.pdf` rebuilt from
the same inputs as the 09-01 12:17 build (`board_v8_fixed.csv` 41,082 B and `player_context.csv`
76,603 B, both byte-matched against the live kit before rebuilding) — 46 of 180 rows badged.
