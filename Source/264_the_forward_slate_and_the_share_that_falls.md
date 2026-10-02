# 264 — The forward D/ST slate, and the rule it inverts

**Date:** 2026-09-09. Matt: *"please start."* Doc 259 called this *"the highest-value build left"*
and it had been sitting in a doc, unworked — which is what `open_threads.py` now exists to stop.

---

## 1. THE HEADLINE, AND IT QUALIFIES §4.33

**§4.33 says: "AT DEFENCE TAKE THE SCHEDULE. AT EVERY OTHER POSITION TAKE THE PLAYER."** That is a
**per-week** statement and it survives. **What nobody had asked is what happens to it over a
HOLD.**

**Schedule's share of the movable spread, by how many weeks you are claiming for:**

| horizon | schedule | the unit itself | schedule's share |
|---|---|---|---|
| **1 week** | 2.66 | 2.29 | **54%** |
| 2 weeks | 4.15 | 4.59 | 47% |
| 3 weeks | 4.27 | 6.88 | 38% |
| **4 weeks** | **4.88** | **9.17** | **35%** |
| 6 weeks | 6.58 | 13.76 | 32% |
| 8 weeks | 8.64 | 18.35 | 32% |

**Monotone, and it flattens near a third.** `[TESTED, 32 defences, 2026 schedule]`

**THE MECHANISM, and it is arithmetic rather than football: a unit is the same unit every week, so
its edge multiplies by the horizon exactly — 2.29 at one week becomes 18.35 at eight, a clean 8×.
A schedule edge does not, because NOBODY GETS FOUR SOFT OPPONENTS IN A ROW.** Soft weeks cancel
against hard ones and the schedule term grows only 3.2× over the same span.

**SO THE TWO STANDING INSTRUCTIONS PULL APART AND BOTH ARE RIGHT:**
- **Streaming a defence week to week — chase the matchup.** §4.33 unchanged.
- **Claiming a defence to HOLD for a month or for the playoffs — take the better unit.** New.

**And it RECONCILES §4.33 with doc 212 rather than contradicting either.** Doc 212's *"3.56 over
one week, 11.72 over four — the horizon roughly triples the signal"* is about ABSOLUTE signal and
it reproduces here (total spread 4.95 → 27.0 from one week to eight). **The horizon triples the
absolute schedule signal while halving its SHARE.** Neither doc had decomposed it.

## 2. THE BUILD

**POPULATION — state it every time: all 32 defences, 2025 regular season, 515 team-weeks from
nflverse play-by-play, scored under THIS LEAGUE'S OWN D/ST rules, projected onto the 272-game 2026
regular-season schedule. Nothing excluded.**

**THE SCORING WAS READ, NOT ASSUMED, AND IT IS NOT ESPN'S DEFAULT** (`2026_League_Settings.txt`,
lines 74–95): sack 1 · INT 2 · fumble recovery 2 · safety 4 · every defensive and return TD 6 ·
and points allowed at **0 → +10 · 1–6 → +7 · 7–13 → +4 · 14–17 → +1 · 22–27 → −1 · 28–34 → −4 ·
35–45 → −7 · 46+ → −10.** ESPN's defaults are +5 / +4 / +3 / +1 / −1 / −3 / −5 / −5. **This league
pays double for a shutout and charges double for a blowout — a 20-point band spread against ESPN's
10.** Every published D/ST ranking is scored on the wrong scale for us.

**TWO INDEPENDENT REPRODUCTIONS OF DOC 212, which is what says the rebuild is right:**
- D/ST points a week: **mean 5.09, sd 6.32** against doc 212's **5.10 / 6.56** on five seasons.
- Best-to-worst opponent swing: **8.2 points a week**, doc 212's figure exactly.

**BASELINE: an offence's generosity = the mean D/ST points its opponents scored against it.**
Most generous 2025: **LV 10.2 · TEN 9.2 · NYJ 8.9 · MIN 8.8 · CLE 8.6.** Stingiest: **BUF 2.0 ·
LA 2.1 · DAL 2.1 · DEN 2.3 · CHI 2.4.**

**BOTH TERMS ARE SHRUNK ON DOC 212'S MEASURED PERSISTENCE — opponent generosity r=+0.325, a
defence's own quality r=+0.269.** Two thirds of 2025 does not carry. That is why this is a tilt,
and it is also why the raw 8.2-point swing becomes 2.7 once it is made forward-looking.

## 3. WHAT IT SAYS RIGHT NOW

**Weeks 2–5, total (schedule + unit):**

| take | | avoid |
|---|---|---|
| **SEA · HOU · PIT · NO · CLE** | | WAS · ARI · CIN · DAL · NYJ |

**Weeks 15–17, the playoff window:**

| take | | avoid |
|---|---|---|
| **PIT · IND · MIN · ARI · SEA** | | NYG · GB · NYJ · CIN · DAL |

**PITTSBURGH IS TOP-FIVE IN BOTH WINDOWS AND IS THE ONE NAME TO HOLD.** Best-to-worst is **10.25
points over weeks 2–5** and **7.31 over the playoff window** — against a league where the whole
D/ST position was written off as free.

**NOT MODELLED, and doc 212 said the same: home field · 2026 roster and coaching turnover · weather
· in-season injuries.** The model explains about a quarter of a D/ST week.

## 4. AND ONE MORE "BLOCKED" THAT WAS NOT

**§4.31 lists the D/ST waiver hit rate as *"blocked — §2 records no D/ST scoring rules."* The rules
are in `2026_League_Settings.txt` and doc 212 had already rebuilt them.** That is the third time in
two days (docs 262, 263) and the rule from doc 263 now has a third instance: **before calling
anything BLOCKED, list the folders — and read §2's own source file.**

**§2 ITSELF SHOULD CARRY THESE BANDS.** It is the fixed-environment section and it has never held a
D/ST line. Queued for v9.3.

## 5. SHIPPED, AND WHAT IS STILL MATT'S

`Scripts\research\`: **`build_dst.py`** (play-by-play → `dst_weekly_2025.csv` + `generosity_2025.csv`)
and **`slate.py`** (`--from W --n N`, or `--playoffs`), plus `sched_2026.csv`. Standard library
only, paths resolved from the script, 3.12-clean (§0.4).

**THE ONE THING THAT NEEDS HIS MACHINE:** which of these defences is actually FREE in his league.
The container cannot reach ESPN (403). `wire.py` already reads his league with his cookies — the
next step is crossing this ranking against the free pool there, and that is one run.

## 6. NOT YET RUN, INPUTS NAMED (§0.5a4)

- **The D/ST waiver hit rate by week**, now unblocked — the 248 D/ST adds §4.31 excluded, against
  `dst_weekly_2021_2025.csv` rebuilt for the earlier seasons the same way this doc rebuilt 2025.
- **Whether the claim is worth the drop.** This ranks defences; it does not price one against the
  bench spot it would cost (doc 240's method).
- **`dst_weekly_2021_2025.csv` and `k_weekly_2021_2025.csv` do not exist on the drive** — doc 212's
  reproduce line names four files and only two were ever committed. `build_dst.py` regenerates the
  2025 half; the 2021–2024 half is one loop away.
