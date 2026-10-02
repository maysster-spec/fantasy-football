# 189 — Mining the analyst takes for mechanisms: five die, one already lived

**2026-09-06 (T−1).** Matt: *"I learned that take about pass protection long ago, and I heard it
from an analyst. Just because their takes are not always right, doesn't mean there isn't an angle
worth exploring."*

**He is right, and the distinction he is drawing is one this project had not made.**

---

## 1. THE DISTINCTION, BECAUSE §4.13d LOOKS LIKE IT FORBIDS THIS AND DOES NOT

§4.13d says the analyst panel **cannot be followed**: the accuracy contest is structurally blind to
breakout skill, six rankers are one opinion measured six times (mean pairwise r **0.81**), deep
unanimity in ADP 100–170 is arithmetic rather than insight, and **disagreement predicts finishing
worse (−0.244, p=0.0009)**.

**Every one of those is about analysts as a RANKING SOURCE. Matt is proposing to use them as a
HYPOTHESIS SOURCE — mine the reasoning, not the ranking.** Those are different objects and §0.2
forbids sliding between them. The evidence he cites is decisive: **doc 188's receiving-role finding
— the strongest result in this project, +27 points against price — came out of an analyst's
pass-protection take that he remembered.** The method has already paid once.

So: I read every take we hold (`analyst_takes.csv` n=54 with bull/bear/concrete, plus
`analyst_calls_joined.csv`, the Gemini writeups and `sweep_20260831.csv`), pulled out the
**mechanisms** rather than the players, and tested the computable ones.

---

## 2. THE CATALOG — mechanisms the analysts actually argue from

| # | mechanism | how often it appears | computable? |
|---|---|---|---|
| **M1** | **"His share collapses when teammate X is on the field"** | **most common by far** — Jameson Williams/LaPorta, Pitts/London, Andrews/Likely, Egbuka/Evans, Burden/Odunze, Worthy/Kelce, St. Brown, DeVonta Smith, Pittman, Lemon | **YES** — with/without game splits |
| **M2** | **Age cliff / "30-year-old back"** | Henry, Barkley, McCaffrey, Aaron Jones, Adams, Kelce | **YES** — nflverse rosters |
| **M3** | **Prior-year workload burn ("413 touches", "342 touches", 370-carry curse)** | McCaffrey, Barkley, Cook | **YES** |
| **M4** | **NFL draft capital / "elite prospect pedigree"** | MHJ, Sadiq, Lemon, Tate, Judkins, Jeanty | **YES — doc 185 called this NOT COMPUTABLE and was wrong** |
| **M5** | New coordinator with a higher pass rate | J. Williams (Petzing), St. Brown, Pitts (Stefanski), Murray (O'Connell), Jeanty (Kubiak), Goff | **NO** — no coordinator table, and §4.21 already killed the team-volume version |
| **M6** | Contract extension = secure role | Pitts, Hall, Barkley | **NO** — no contract data; external research puts it at +11.9%, weak |
| **M7** | After-contact / explosive-run / YAC efficiency | Mason, Likely, Pierce, Burden, Cook | partly — §4.6 already has it as a tiebreaker |
| **M8** | Quarterback upgrade | Pittman/Rodgers, Nabers/Dart, Tate, Mayfield | **built and killed** — doc 185 §2 |

**Doc 185's "not computable" list is now shorter.** `nflverse` roster releases carry **`draft_number`,
`birth_date`, `entry_year` and `years_exp` for every player.** Age and NFL draft capital are both
available, for every season, for the whole board. Still genuinely absent: routes run (so no true
YPRR), snap share, PFF grades, coordinator identity, contract status.

---

## 3. RESULTS — same framework as doc 188, so the numbers are comparable

**BASELINE — state it every time: half-PPR points, weeks 1–14 of year *t+1*, regressed on
log(preseason ADP) within each season. BEAT = the residual. n=807 player-seasons, 2022–2025,
sd(beat) = 57.5.** ADP from the **§1.1 registry**, never a historical `espn_adp`.

### M1 — "he disappears when the other guy plays": TRUE AS DESCRIPTION, WORTHLESS AS PREDICTION

Every pass-catcher with ≥40 targets was paired with his team's next-highest-target teammate, and his
weekly target share split by whether that rival played. **n=205 player-seasons:**

> **Target share WITH the rival: 0.170. WITHOUT him: 0.200. Lift +3.0 points of share, p<0.0001.**

**The analysts are describing something real.** Then the test that matters — does last year's
dependence predict this year's beat, for WR/TE?

> **r = +0.039, p = 0.699, n=100.** Most-dependent quartile **−13.4**; least-dependent **−19.8**.
> **The point estimate leans the wrong way for the fade.**

**It is a description of what happened, not a forecast of what will.** `[TESTED — NULL]`

The named 2025 splits, for the record, because they are the reason the takes exist:

| player | rival | share with | share without | lift |
|---|---|---|---|---|
| **Luther Burden III** | **Rome Odunze** | **0.101** (11 g) | **0.211** (4 g) | **+0.109** |
| Kyle Pitts Sr. | Drake London | 0.201 (12 g) | 0.292 (5 g) | +0.091 |
| DeVonta Smith | A.J. Brown | 0.241 (15 g) | 0.284 (2 g) | +0.043 |
| Emeka Egbuka | Cade Otton | 0.235 (15 g) | 0.247 (2 g) | +0.012 |

**Burden's is the largest dependence in the named set.** His bull case — *"steps into a massive
target vacuum"* — is, measured, a bet that Odunze is off the field. In the eleven games they shared,
Burden ran at a **10.1%** share. That is a third strike against the Burden case (doc 185: one
archetype signal; doc 187: 0 inside-10 targets), and it is the most concrete of the three.

### M2 — THE AGE CLIFF IS A NULL AT EVERY POSITION

| position | n | r | p |
|---|---|---|---|
| RB | 252 | +0.031 | 0.622 |
| WR | 331 | −0.017 | 0.758 |
| TE | 116 | +0.135 | 0.149 |
| QB | 108 | +0.041 | 0.670 |

RB by band: **21–24 −11.5 · 25–26 −8.5 · 27–28 −6.3 · 29+ −9.5** — the youngest backs are the
*worst*, not the best. WR 29+ is the weakest band (−17.2) but 21–24 is −12.8, so there is no cliff
to trade on. **The market already prices age.** Six analyst takes rest on this. `[TESTED — NULL]`

### M3 — THE WORKLOAD CURSE IS BACKWARDS, AND ITS INVERSE IS DOC 188 IN A HAT

Prior-year carries against the beat, RB: **r=+0.160, p=0.011** — *more* carries, *better*, the
opposite of the curse. Bands: **<150 carries −17.8 · 150–249 +5.1 · 250–299 −14.8 · 300+ −9.0**
(n=11 at 300+, untestable).

**Then the control that matters:** add doc 188's prior-year target share and **carries collapse to
p=0.118 while target share holds at +141, p=0.034.** Add prior games and age and carries go to
p=0.312 while target share stays significant at p=0.042.

> **The workload "signal" was the receiving role wearing a different hat.** The 370-carry curse is
> not supported, and neither is its inverse as a separate finding. `[TESTED — SUBSUMED]`

### M4 — DRAFT CAPITAL: NOT ESTABLISHED AT RB, NULL AT WR

Doc 185 quoted the published figure — 71.4% of first-round RBs finish top-24 as rookies against
**1.3%** for Day 3 — and said we could not check it. We can, and it does not survive.

RB, Day-3 indicator: **−13.0 points, p=0.087** with player-clustered errors — **not significant**.
With prior-role controls it falls to **−7.6, p=0.273**. And by season:
**2022 +19.4 · 2023 −10.3 · 2024 −12.9 · 2025 −48.1.** **One year carries almost all of it and 2022
reverses outright.** That is `ERROR_PATTERNS` A19 territory and the reason to run the by-season cut
before believing anything. `[TESTED — NOT ESTABLISHED]`

WR: **+5.5, p=0.222**, and the raw bands lean the *other* way — first-round receivers **−18.5**,
Day-3 receivers **−8.6**. `[TESTED — NULL]`

### BONUS — §4.22(c) REPLICATED ON A DIFFERENT DATASET, BY ACCIDENT

In the WR draft-capital regression, prior-season **games played** came out **+1.29 points per game,
p=0.032**, player-clustered. That is §4.22(c)'s availability finding — measured on ESPN pulls with a
different outcome and a different baseline — reproducing on nflverse. **An independent replication
of the one injury signal this project carries.**

---

## 4. THE SCORECARD, AND WHAT IT SAYS ABOUT THE METHOD

| mechanism | verdict |
|---|---|
| pass protection → **receiving role** (doc 188) | **LIVE. +27 points against price, survives every control.** |
| teammate dependence | real in-season, **null as a predictor** |
| age cliff | **null**, four positions |
| workload burn | **null**, and subsumed by the receiving role |
| draft capital, RB | **not established** — one season carries it |
| draft capital, WR | **null** |

**One live signal from six mechanisms. That is a good hit rate for this kind of work, and the live
one is the largest edge in the project.** Matt's premise holds: analyst reasoning is a legitimate
hypothesis generator even though analyst rankings are not a ranking source. The two claims never
conflicted.

**And every test here strengthens doc 188 rather than competing with it.** Carries, age, games and
experience all wash out; **prior-year target share is the only thing that stays significant in every
specification it appears in.**

**Red team run on all of it:** player-clustered standard errors throughout (117 unique backs, 149
receivers), by-season breakdowns on both surviving candidates, controls for prior role, and a pure
random placebo (**r=+0.011, p=0.866**) confirming the pipeline does not manufacture significance.

---

## 5. STILL UNTESTED — the honest remainder

- **M5 (coordinator identity)** and **M6 (contract status)** need tables we do not have.
- **M7 (after-contact / YAC)** has PFR data behind it and never got a payoff test in this framework.
  It is the one live candidate left in the catalog. Not run — out of time, not out of interest.
- The teammate test uses the team's **top other pass-catcher** as the rival. An analyst usually
  names a *specific* one. A per-pair version would be sharper and is not built.
- **No board edits from any of this.** Surfaced, not scored.
