# 229 — THE DRAFT-STRATEGY CATALOG, MATCHED TO WHAT WE ALREADY MEASURED

*2026-09-08. Matt: "use some of the examples we surface to find matches for draft strategies
online and I think you will find it more rewarding!, and don't dismiss everything because you
can't be easily find justification." And, mid-run: "What we already surfaced should inform your
research methods and scoping."*

*Doc 227 did this for waivers. This is the draft side. Scoped his way: every search term was
seeded from one of OUR findings, and the catalog is ordered by whether the outside claim can be
TESTED against data we already hold — not by how well written the article was.*

---

## 1. THE LIST

1. **A NEW KEEPER RULE, AND IT INVERTS THE USUAL ONE.** Among top finishers, the ones who were
   CHEAP repeat at **22.7%** and the ones who were EXPENSIVE repeat at **56.0%** — a 33-point gap,
   four positions out of four pointing the same way, p=0.0004. Our keeper cost is flat (round 15
   for anybody), so cost cancels and only repeat rate is left. **Next August, when you are choosing
   between two eligible keepers, take the one who cost the most, not the one who was the bargain.**
2. **AND THE ELIGIBILITY RULE FIGHTS YOU.** A keeper must have been drafted round 5+, which
   restricts your entire candidate pool to the low-repeat band by construction. That is the same
   thing doc 138 measured from the other side (a kept RB returns +6.7, not +81). **Among your
   round-5+ candidates, prefer the one drafted CLOSEST to round 5.**
3. **ONE NEW LIVE SIGNAL: THE TIGHT END'S DECEMBER DRAW.** An easier weeks 15–17 slate is worth
   about **+3.4 points at tight end and nothing at quarterback, back or receiver**. Best draw vs
   worst is about **9 points across the three weeks**. It is a tiebreak between two tight ends you
   rate the same — never a reason to move off a better one.
4. **A LINE ON THE WIRE SHEET WAS WRONG AND IS FIXED.** It said matchup is measured at zero for
   receivers and tight ends, full stop. True week to week (doc 212); NOT true for the tight end's
   weeks 15–17 draw. Sentence rewritten, and the sheet now prints the draw.
5. **STOP CARRYING "WATCH THE ROOM FOR A QB RUN" AS A LIVE WORRY** (§7, from doc 142 §4a). In five
   drafts this room has produced **no quarterback run at all** — 14 observations of a pick following
   a QB in rounds 1–3, and rounds 4–6 point the other way. Underpowered, but there is nothing there.
6. **DO NOT QUOTE "runs make you overpay."** Raw, it looks like −7.3 picks at p=0.002. Round-demeaned
   it is −2.9 picks at p=0.31 — the raw number was a round artifact.
7. **RUN THIS ONE COMMAND** when you next have a minute at the machine:
   `py wire.py --check` — it is the only untested half of the sheet, and the December-draw box
   needs the schedule pull that lives behind it.
8. Nothing else to run. Everything below was done here.

---

## 2. METHOD, AND WHY THE SCOPING RULE CHANGED THE ANSWER

The first instinct was to search "fantasy football draft strategy" and grade what came back. That
produces a hundred August listicles and a verdict of "thin," which is the failure mode Matt named:
*"don't dismiss everything because you can't be easily find justification."*

Scoped his way instead, the procedure was:

1. Take a finding WE measured. 2. Search for the outside claim that touches the same object.
3. Write down what would have to be true for the outside claim to hold **in our league, on our
data** (§0.5(a2)). 4. Run it. 5. Where it cannot be run, log it as `[HYPOTHESIS]` **with the test
named**, which is not the same as discarding it.

Two rules did real work. **§0.6 (state the population):** three of the outside claims are correct
about a population that is not ours — a different scoring format, a different roster, a pooled
sample that hides the split we care about. **§4.24(b) (power vs prediction):** one outside claim is
30× smaller than anything our sample could see, so "we did not find it" says nothing about it.

---

## 3. THE CATALOG

Every source's publication date is stated before use (`ERROR_PATTERNS` B7).

| # | outside claim | source, dated | ours | verdict |
|---|---|---|---|---|
| A | Top finishers repeat about half the time (RB1 56.25%, WR1 48.84%) | Dynasty Nerds, **26 May 2026**, 2009–2025 | doc 138 (keeper value does not persist) | **POOLED OVER PRICE. Split, it is 22.7% vs 56.0%. See §4.1 — the single most useful thing in this batch.** |
| B | Strength of schedule is nearly worthless for the season but useful in two specific spots | Fantasy Football Blueprint, **7 Aug 2026** (headline only — the body sits behind a redirect I could not read) | doc 212 (D/ST matchup is 108% of the between-unit spread; WR/TE null) | **ONE of the two spots found independently: the tight end's weeks 15–17 draw. See §4.2.** |
| C | Defences do not repeat year to year, so SOS cannot be forecast | Footballguys, **30 July 2015** | doc 131: defensive quality persists at r=+0.204 | **RIGHT OBJECT, WRONG MEASURE.** They measured fantasy points allowed by position — small and noisy. On EPA per play a defence carries ~4% of next year's variance. Not zero, and enough for the tight-end case. |
| D | Players taken at the end of a positional run go ~0.25 spots earlier than usual — runs make you overpay | Fantasy Footballers, **19 Aug 2021, updated 15 Aug 2025**, 15 mock drafts | §7's "watch the room for a QB run" | **NOT REPRODUCED, AND WE COULD NOT HAVE SEEN IT.** See §4.3. |
| E | Handcuffing your own back does not help | *Judgment and Decision Making* (Cambridge), 1,350 Sleeper leagues / 12,590 teams / 188,426 picks, 2017 season | doc 227 §1 row H (untested) | **EXTERNAL NULL AND IT IS THE BETTER EVIDENCE:** 51.04% vs 50.56%, Bayes factor 4.2 *for no difference*. Ours cannot resolve it — 10 of 60 manager-seasons ever did it. |
| F | Rosters that spend less on kickers and defences win above .500 | same paper | §4.8 (+105.6 pts/manager-season) | **CORROBORATED from an independent 12,590-team sample.** |
| G | Positional runs are real: each WR taken last round adds ~0.5 expected WR picks this round | Fantasy Footballers, dated above; run behaviour also measured in the Cambridge paper | §5 opponent model | **THE BEHAVIOUR IS REAL, THE PAYOFF IS NOT.** The paper measures teams that follow a run at 51.0–51.2%, BF 4.7–8.8 for no difference. |
| H | Hit rate by draft round: "round 10 is the largest QB1 concentration, 68.75%" | Fantasy Trading Room, **8 June 2025**, 2016–2024, FFPC, "hit" = top-4 at position | §4.13 (ratio bar) and §4.13b (absolute bar) | **DOES NOT REPRODUCE — their cell is 11 of 16.** On our rows QB top-12 falls 80% → 46% → 24% with price. Third definition, same shape. See §4.4. |
| I | Zero RB: backs are fragile, so let other people buy them and inherit the survivors | RotoViz, original Nov 2013, guide **2 June 2016** (paywalled; mechanism taken from the public framing) | doc 42, doc 131 (RB 12.94 g vs WR 12.95 g) | **THE FRAGILITY PREMISE IS DEAD FOR A THIRD TIME:** RB 10.66 g vs WR 10.90 g, p=0.551. **The INHERITANCE channel is untested and is the live half — see §5.** |
| J | Prior-season games missed and career games-missed rate predict future availability; a games-missed model reaches R²=0.401 against 2.6% for the best benchmark | Draft Sharks, **28 Sep 2020**, ~300 variables, ~3,500 player-seasons | §4.22 / doc 203 (−19.4, p=0.00004) and doc 204 (null among established veterans) | **CORROBORATED, AND IT NAMES A VARIABLE WE HAVE NOT USED: time since the last soft-tissue injury.** Doc 204's veteran null used last season and a 3-year rate; theirs uses career rate + severity + recency. `[HYPOTHESIS — test named in §5]` |
| K | Optimal best-ball position allocation (e.g. two QBs if you take one early, three if you wait) | Establish The Run, **15 May 2026** | §6 doctrine, `CAPS = {'QB':2,'TE':2}` | **NOT TRANSFERABLE, and saying so is not dismissing it.** That format is 20 rounds, full PPR, no kicker, no defence, no playoffs, and no start/sit. Four of the five things that make our allocation binding are absent. |
| L | Tier-based drafting (Boris Chen and successors) | tier tools, no published head-to-head | §4.10's rule race | **NO OUTSIDE MEASUREMENT EXISTS.** Our own race puts a full-lookahead rollout ahead of static VBD by +4 to +9 and VONA at −8.8. Tiers were never entered. `[HYPOTHESIS]` |

---

## 4. THE TESTS

### 4.1 REPEAT RATE, SPLIT BY PRICE — the finding

**CLAIM IN TESTABLE FORM, written before the run:** the published ~50–56% repeat rate is pooled
over price; split by what the player cost in the season he hit, a cheap top finisher repeats
materially less often than an expensive one.

**POPULATION:** 2021–2024 top-12 finishers at RB and WR and top-6 at QB and TE, scored weeks 1–14
in this league's scoring, who carried a §1.1 preseason ADP in the hit season **and** were priced
again the following season (the second condition is what makes "repeat" a fair question rather
than a survivorship count). **n = 135.**
**BASELINE:** repeat = finished top-12 (top-6 at QB/TE) again the next season, weeks 1–14.

| position | cheap (ADP 61+) | rich (ADP ≤ 60) | Fisher p |
|---|---|---|---|
| RB (top-12) | 27.3% (n=11) | 57.1% (n=35) | 0.165 |
| WR (top-12) | 15.4% (n=13) | 47.1% (n=34) | 0.091 |
| **QB (top-6)** | **10.0% (n=10)** | **66.7% (n=12)** | **0.011** |
| TE (top-6) | 40.0% (n=10) | 70.0% (n=10) | 0.370 |
| **POOLED** | **22.7% (n=44)** | **56.0% (n=91)** | **0.0004** |

`[TESTED]` Four of four positions the same sign; the pooled gap is **+33.3 points**. The finer
ladder is monotone at three of the four positions (RB 57.7 / 55.6 / 25.0 / 33.3 across ADP 1–24 /
25–60 / 61–120 / 121+).

**Why it matters here and not everywhere.** In most keeper leagues you pay the round you drafted
him, so a cheap hit carries a cost advantage that offsets a lower repeat rate. **Our rule charges
round 15 for anybody**, so that offset does not exist and the repeat rate is the whole of the
decision. This is the same result doc 138 reached on a different outcome (a kept RB returns +6.7
VBD14, not the +81 that was assumed) and it now has a second, cleaner form.

**And the eligibility rule interacts with it, badly.** Round 5+ only, which is roughly ADP 50+, so
the candidate pool is drawn almost entirely from the band that repeats at ~23%. That is not a
reason to skip keeping — one per team is compulsory in effect — it is a reason to take the most
expensive eligible name rather than the best story.

### 4.2 THE PLAYOFF SLATE

**CLAIM IN TESTABLE FORM:** a player whose weeks 15/16/17 opponents allowed more points to his
position **last** season scores more in weeks 15–17 **this** season, controlling for his price.
Preseason-knowable: it is the schedule plus last year's defence, both in hand on draft day.

**POPULATION:** player-seasons 2022–2025, QB/RB/WR/TE, §1.1 preseason ADP ≤ 180, at least one game
played in the window. **n = 551.** **BASELINE:** what log(preseason ADP) predicts, fit within
season × position. **CLUSTERED BY NFL TEAM** — every player on a team shares one slate (A5).

| position | n | per +1 sd of easier draw | p (clustered) |
|---|---|---|---|
| QB | 71 | −0.71 | 0.85 |
| RB | 177 | −0.39 | 0.66 |
| WR | 233 | −0.47 | 0.64 |
| **TE** | **70** | **+3.39** | **0.031** |
| all | 551 | −0.00 | 1.00 |

**Control arm — the identical test on weeks 1–14 slate against weeks 1–14 points: null at all four
positions** (QB +3.32 p=0.67, RB −3.04 p=0.33, WR +2.46 p=0.38, TE −1.79 p=0.64). So this is a
three-week property, not a season property, which is what the Blueprint headline claims and what
our own doc 212 (week-level, WR/TE null) would predict.

**Robustness on the one live cell.** Positive in all four seasons taken alone (r = +0.44, +0.05,
+0.25, +0.37). Leave-one-season-out β from **+2.54 to +4.35** (p 0.018 to 0.111). The per-game
version holds: **+1.12 points a game, p=0.027.** Quartiles are monotone — **−4.9 / +0.3 / +0.9 /
+4.4**, so softest minus hardest is **+9.3 points across the three weeks**, MWU p=0.093.

**Mechanism, and it is the honest reason to believe a three-week effect where there is no season
effect.** The slate measure's spread over three weeks is 1.5–2.5× its spread over fourteen, because
fourteen opponents average out and three do not. Tight end has the widest ratio (**2.47×**) and by
far the widest relative spread: last season teams allowed between **6.4 and 17.5** tight-end points
a game — a factor of 2.7, against roughly 1.4 at receiver.

**HOW TO HOLD IT.** One live cell out of ten tests. The season-by-season consistency and the
monotone quartiles are more than chance usually gives, and there is a mechanism, but this is one
measurement. **Use it to split two tight ends you rate the same. Nine points over three weeks is
smaller than the gap between a good tight end and a bad one, and §4.3's tier structure still
governs.** `[TESTED — one live cell, four seasons]`

### 4.3 DO RUNS MAKE YOU OVERPAY?

**POPULATION:** 680 true selections 2021–2025 carrying a §1.1 preseason ADP, of 834 total — the
154 without a price are mostly kickers, defences and deep names, and they are excluded, not
imputed. **OUTCOME:** earliness = preseason ADP − overall pick; positive means you paid up.
**"In a run"** = the 2nd or later pick of a same-position streak of 3+ consecutive picks.

Raw, it looks decisive and backwards: in-run **−3.7** against outside **+3.6**, difference −7.3
picks, MWU **p=0.002**. **It is a round artifact.** Runs cluster in the early rounds, where
earliness is negative for everyone. Demeaned within year × round, the difference is **−2.9 picks,
p=0.307** — null.

**And the power statement matters more than the null.** sd of round-demeaned earliness is 20.9
picks; at n=110 followers the 80%-power minimum detectable difference is **6.3 picks**. The
published effect is **0.25 picks**. **This test could not have seen it if it were 25× larger.**
§4.24(b)'s distinction, exactly: failed POWER, not PREDICTION. Do not cite our null against them.

**The quarterback half is a real finding, though.** There has never been a QB run in this room.
Max same-position streak at QB across five drafts is 3. P(next pick is a QB | this pick was a QB):
rounds 1–3 **14.3% (2 of 14)** against a 10.4% base; rounds 4–6 **4.2%** against 13.2%; later bands
below base. `[TESTED, underpowered]` §7 carries "watch the room for a QB run" as the soft spot under
doc 142 §4a. **It is a smaller worry than it reads.**

### 4.4 A THIRD DEFINITION OF A HIT

§4.13 used a ratio bar, §4.13b an absolute bar; the published round tables use **top-4 at
position**. Same rows (2021–2025, priced ≤ 180, weeks 1–14):

| preseason ADP | n | top-4 | top-12 | startable (≥ replacement ppg) |
|---|---|---|---|---|
| 1–24 | 119 | 32.8% | 60.5% | 96.6% |
| 25–48 | 117 | 10.3% | 33.3% | 76.1% |
| 49–84 | 176 | 8.5% | 24.4% | 55.7% |
| 85–120 | 174 | 2.3% | 20.1% | 41.4% |
| 121–180 | 249 | 3.2% | 10.8% | 19.7% |

`[TESTED]` **Three definitions, one shape: everything that is not a ratio falls with price.**
§4.13b's warning stands and is now stronger — the 17% ratio-breakout figure at ADP 121–180 is the
ONLY bar on which late players look good, and it looks good because the price is near zero.

The published "round 10 QB1 at 68.75%" does not survive contact: their cell is **11 of 16**. Ours,
QB top-12 by price: 80% (1–24), 77.8% (25–48), 50% (49–84), 46.4% (85–120), 24.2% (121–180).

### 4.5 THE ZERO-RB PREMISE, A THIRD TIME

Among priced players (ADP ≤ 180, 2021–2025): **RB 10.66 games, WR 10.90 games, difference −0.24,
MWU p=0.551** (n=273 / 346). Doc 42 said it, doc 131 said it again at 12.94 vs 12.95, and this is
the third independent look. **Backs are not more fragile than receivers.**

**This does not kill Zero RB and I am not claiming it does.** It kills one stated premise. The
strategy's other channel — that an RB vacancy converts into a startable replacement far more often
than a WR vacancy does — is a different claim and is **untested here**. Doc 12's waiver table leans
against it (RB adds hit 22%, WR 31%), but that is a waiver population, not a vacancy population.

---

## 5. WHAT I COULD NOT TEST, AND THE TEST EACH ONE NEEDS

Logged rather than dropped, per Matt's instruction.

1. **The Zero-RB inheritance channel.** Test: identify every starter-week lost to injury 2021–2025
   by position; measure what share of the direct replacements cleared replacement ppg over the
   following three weeks. Data on hand — nflverse weekly, snap counts and injury reports 2021–2025.
   `[HYPOTHESIS]`
2. **Time since the last soft-tissue injury** (Draft Sharks' top-five predictor, which we have never
   used). Test: re-run doc 204's veteran model with weeks-since-last-soft-tissue-designation and a
   career games-missed rate, not last season and a 3-year rate. Data on hand — `nfl/injuries_2021..2025`.
   This is the one honest challenge to doc 204's null. `[HYPOTHESIS]`
3. **Quarterback / pass-catcher stacking in redraft.** Every published treatment is best ball or
   DFS, where correlation buys tournament variance we do not want. Test: same-team QB+WR pairs vs
   matched unpaired pairs, on weekly variance and on our §2 lineup. `[HYPOTHESIS]`
4. **The Blueprint's second spot.** I found one of their two independently. I could not read the
   article body. `[OPEN]`
5. **Tiers versus the rollout.** Nobody has published a head-to-head. Our rule race has the harness
   for it and never entered a tier rule. `[HYPOTHESIS]`

---

## 6. WHAT CHANGED ON THE SHIPPING FILES

- **`Source\pos_allowed_2025.csv` (new)** — 128 rows, last season's half-PPR points allowed per
  game by team and position, built from nflverse weeks 1–18 under §2 scoring. ESPN team codes.
- **`Scripts\wire.py`** — gains `load_posallow()` and `te_playoff_slate()`, a December-draw box on
  the sheet, and a console echo. **Four negative controls were run first and all four fire:** no
  schedule, no allowed table, a schedule missing week 17, and the happy path with the ordering
  asserted. A missing input prints why it is missing; it never renders an empty box (§0.2).
- **`Scripts\wire.py`, corrected prose** — "matchup is measured at zero for receivers and tight
  ends, never move one for it" now reads "week to week … the single exception is the box below."
  §0.2's enumerate-every-downstream-use rule: doc 212's null is a WEEK-level result and the new
  finding is a three-week-window result, and the old sentence covered both.

---

## 7. OPEN THREADS (§0.5(e))

- `py wire.py --check` — still the only untested half of the sheet, and the December-draw box
  depends on the schedule pull behind it.
- `py waivers.py` — four seasons of trade history, still not pulled.
- The scheduled tasks: `setup_tasks.bat`, then `schtasks /run /tn "FF2026 - 2 Thu lineup"`.
- Roster: drop Shough → Hockenson; drop Spears → stash Brian Robinson Jr.
- Doc 226 §5 catalog: trades (in progress), standings → waiver order, drops.
- The five `[HYPOTHESIS]` rows in §5 above.
- Doc 227 §1's `[OPEN]` rows — G (bye/trade arbitrage) and H (denying a handcuff), the second of
  which now has adjacent external evidence in row E and is still not the same object.
- The board's universe still lets a Tyreek Hill be invisible.
