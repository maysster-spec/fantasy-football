# 185 — Breakout archetypes: the catalog, and Batch A

**2026-09-06 (T−1).** Matt: *"There will not be one profile for break out potential, they can come
in different flavors. This is why I want you to RESEARCH to find other potential signals… don't
bite off more than you can chew and instead please do it in batches… go through the players with a
fine tooth comb. I want us to mine for value."*

Two research passes closed (WR/TE and RB/QB). This doc is the **catalog** — every candidate
archetype, what it is measured at, and whether this project can compute it — followed by
**Batch A** (his picks 41 / 56 / 65). Batches B and C are not run yet.

---

## 1. WHAT THE DATA ACTUALLY SUPPORTS — a correction to my own last answer

I told him YPRR, age, target share and red-zone share were **not computable**. That was wrong. It
was a claim about our own files that I made without listing them. `Source\` holds the
Pro-Football-Reference 2025 exports, and between them they carry:

| field | file | archetype it unlocks |
|---|---|---|
| **Age** | `Advanced_Receiving_2025`, `Standard_Rushing_2025` | age curves |
| **Inside-20 / inside-10 targets, and the TD on each** | `RedZone_Receiving_2025` | **A2 — the strongest one we have** |
| **Inside-5 rush attempts and share** | `RedZone_Rushing_2025` | goal-line role |
| **Targets, target share, targets/game, ADOT, YAC/R, BrkTkl, Drop%** | `Advanced_Receiving_2025` | role vs efficiency |
| **Att, Y/A, Succ%, A/G** | `Standard_Rushing_2025` | efficiency-without-volume |
| 2026 projected targets / rush attempts | `raw_stats` ids 58 / 23 | pass-catching back, rushing QB |

Still genuinely absent: **routes run** (so no true YPRR), **snap share**, **PFF grades**, and
**NFL draft round** — that last one I looked up and sourced by hand for the 17-man year-2 cohort.

**Name-join control (§3):** the PFR files carry no `espn_id`, so the key is normalised name.
**Zero** live WR/TE with 2025 games failed to match. 2026 rookies correctly carry no 2025 row.

---

## 2. THE CATALOG

### KEPT — computed, and used in the sweep

| # | archetype | what it rests on | provenance |
|---|---|---|---|
| **A1** | **Year-2 pass-catcher.** 2025 rookie, WR/TE. | RotoViz: 38 second-year WRs have hit 200 pts, 26 of them since 2010; *"if you aren't a top-24 WR by your third year, it's very unlikely you will become one."* | `[SOURCED, external]` |
| **A2** | **Red-zone role without the touchdowns.** ≥5 inside-10 targets or ≥12 inside-20, with an inside-10 TD rate ≤25%. | **OURS, §4.5, n=37:** inside-10 targets persist at **r=+0.59**, RZ target volume **+0.51**, RZ target share **+0.48** — and **RZ TD rate is r=+0.02, noise.** The role sticks, the finishing doesn't. | `[TESTED, ours]` |
| **A4** | **Rushing QB.** ≥5.5 projected rush att/game. | 12+ starts and ≥5.5 rush att/g → 18.7 ppg and **30 of 34 QB1 finishes**; rush att/g persists at **r=0.89** against passing TD rate **0.37**. | `[SOURCED, external]` |
| **A5** | **Pass-catching back.** ≥45 projected targets (≈10% of a team's targets). | A target is worth ≈2× a carry; **57 of 69** RBs averaging 15+ ppg since 2015 had a ≥10% target share. | `[SOURCED, external]` |
| **A6** | **Unsettled backfield with a big pie.** `depth_map` UNSETTLED and job ceiling ≥180. **RB only.** | **OURS, §4.20.** With its own caveat attached: the flag does **not** pick the winner (incumbent − challenger +8.2, **p=0.604**). Buy the job, never the name. | `[TESTED, ours]` |
| **A8** | **Efficiency without volume, RB.** ≥4.6 ypc on ≤170 carries. | §4.6: after-contact ability is the one input ESPN does **not** already price. Tiebreaker, never a thesis. | `[TESTED, ours]` |

### DROPPED — measured failures. Do not use these, and do not let a podcast reintroduce them.

| archetype | why it is dead |
|---|---|
| **Handcuff without standalone value** | 54 handcuffs drafted rds 7–15 (2011–2017): **32 offered ≤3 top-24 finishes**. Across **105 games the starter actually missed**, the handcuff hit weekly top-24 **34%** of the time. |
| **"New quarterback" as a positive** | It is **negative**: 11.3% top-24 on a new-QB team vs **14.5%** with the QB returning; a rookie QB is **3.9%**. |
| **Slot → perimeter move** | No published base rate exists. It is a story, not an archetype. |
| **New OL / new scheme** | **OURS, §4.24:** dead at RB (doc 28), and at QB the payoff is r=+0.092, **p=0.53** — underpowered, not proven absent. |
| **"The market is sleeping on him"** (ADP rank − projection rank) | **OURS, §4.13** retired it (rho −0.079, its coldest quintile breaks out at 3.1%); **§4.22(b)** replicated it *stronger* on a different market: **rho −0.173, p<0.001, n=409.** When the market and the projection disagree, **the market is right.** |
| **Post-hype / bounce-back year two** | **OURS, §4.22(d):** year-2-after-injury vs healthy is **+2.4, p=0.77**, and the market discount is **+2.7 slots, p=0.54.** Neither cheap nor better. |
| **Analyst disagreement** | **OURS, §4.13d:** controlling for ADP level, disagreement predicts finishing **worse** — **−0.244, p=0.0009.** |

### BUILT AND KILLED THIS SESSION

**QB-continuity flag.** Derived team-by-team from the 2025 scoring leader vs the 2026 projected
starter. It fires on exactly **three** teams and **one of the three is a false positive** — it
labelled Cincinnati "new QB" because Flacco outscored an injured Burrow in 2025. A flag with three
fires, one of them wrong, carrying a published effect of **3 percentage points**, is not worth
shipping. Not merged, not on the board. `[BUILT, KILLED]`

### DEMOTED — real but too weak to move anything

- **Vacated targets.** PFF (2020) finds it meaningful only for top-24 outcomes; Dynasty Football
  Factory (2021) found half of 14 teams' target totals simply *declined*. **OURS, §4.21:** clustered
  by team, **r=+0.125, p=0.50.** Targeting list only.
- **TE sophomore leap** (33% → 94% of career baseline): **n=10.**
- **Contract year** (+11.9%): weak, and not computable from our fields anyway.

### THE ONE THAT FIGHTS US — and our measurement wins

**A3, "target earner who didn't play"** (≥5.5 targets/game on ≤12 games) reads like an upside
archetype. **§4.22(c) says the opposite:** a player under 13 games last season beats his projection
by **−16.2 points** (p=0.025), entirely a WR effect (**−25.4**, n=45, p=0.003), and **§4.22(e)**
shows it is dose-dependent — 1–6 games **−40.8**, 7–9 **−27.1**, 10–12 **−16.9**, 13+ **−12.6**.
**So A3 is carried as a WARNING, not a buy**, and the number on the badge is what matters, not its
presence. This is the same call §4.22 already shipped; the archetype sweep does not get to reverse it.

---

## 3. BATCH A — picks 41 / 56 / 65 (adp 36–86)

Effective ADP at those turns is ~51 / ~66 / ~75 (§2.1c). 36 skill players in the window.

### The five that the signals actually surface

**1. Tyler Warren (TE IND, adp 52.0, VOR +28.08) — 2 signals, the most in the batch.**
Year-2 TE, first-round capital (1.14), and the A2 case is loud: **19 inside-20 targets, 11
inside-10 targets, 2 touchdowns.** 22% target share over 17 games. §4.5 says the 11 sticks and the
2 does not. §4.3 has him as TE3 at +28.1 behind Bowers (+51.2) and McBride (+47.6) — this is the
first measured reason to think that gap is smaller than the board says. **At pick 41 he is a live
name; at 56 he is very unlikely to be there.**

**2. Courtland Sutton (WR DEN, adp 81.3, VOR +6.20) — the purest A2 on the board.**
**17 inside-20 targets, 7 inside-10 targets, ZERO inside-10 touchdowns**, 22% target share,
17 games played. Nobody else in the window has a red-zone role that large with no conversion.
**The bear is on the same page:** Jaylen Waddle is now a Bronco at adp 52 with a 22% share of his
own. The role was real; the 2026 competition is new. Not a recommendation — a name whose price
(+6.2 VOR at pick 80's doorstep) does not reflect a role that our own strongest finding says persists.

**3. TreVeyon Henderson (RB NE, adp 77.3, VOR +9.33) — 3 signals, the most of any player in Batch A.**
Pass-catching back (46.6 projected targets), unsettled job (ceiling 182), efficiency (**5.1 ypc,
51.7% success on 180 carries**), round-2 capital (2.38). Age 23, 17 games.

**4. Luther Burden III (WR CHI, adp 74.8, VOR +4.77) — 1 signal, and this corrects my own last answer.**
When I built a five-signal profile *from Burden*, he scored 4 of 5. That was circular and I said so.
Scored against archetypes built from outside research, he scores **1** — year-2 WR, and that is all.
His 2025: **0 inside-10 targets, 4 inside-20 targets, 11% target share, 4.0 targets/game.**
The one genuinely good number is **10.87 yards per target**, second-highest in the batch — efficiency
without volume, which is the shape §4.13/§4.22(b) says the market prices correctly.
**Head to head with Henderson: 3 signals to 1, and Henderson is 2.5 picks cheaper.**
Matt's question was *"TreVeyon at 9 and Luther at 5 — where do I push my chips."* The archetypes
answer Henderson, and they answer it on named evidence rather than a hunch. **I was leaning Burden
and the sweep says I was leaning wrong.**

**5. Jaxson Dart (QB NYG, adp 83.2, VOR 0.00) — the rushing-QB archetype at the replacement line.**
**100.8 projected rush attempts = 5.93/game**, over the 5.5 bar that separates 18.7-ppg QBs
(30 of 34 QB1 finishes). 2025: **5.7 ypc, 66.3% success, 7 inside-5 attempts.** First-round capital.
His VOR is exactly **0.00** — he *is* QB12, the replacement line — which is precisely what the
archetype says is mispriced. Relevant to the §4.18 draft-night rule at 104/113: Dart at 83 is a
different, earlier question, and Batch B has to price him against Nix before this goes anywhere.

### Signals worth noting but not acting on

- **Davante Adams (adp 46, VOR +35.0)** — **23 inside-10 targets, 11 TDs.** Triple anyone else's
  inside-10 volume in the window, and he already converted it, so A2 does not fire. Age 33.
  The board already ranks him 2nd in the batch by VOR.
- **D'Andre Swift (adp 51.8, VOR +27.8)** — 4.9 ypc, 54.7% success, **10 inside-5 carries at a 45.5%
  share**, unsettled job ceiling 195. One signal, strong underlying numbers.
- **Bucky Irving (adp 56.7, VOR +20.0)** — pass-catcher + open job, but **3.4 ypc and zero inside-5
  attempts.** He had no goal-line role at all. Mixed, and 10 games in 2025 puts him in the warning band.

### The A3 warnings that fired in this window — read the number, not the badge (§4.22e)

**Mike Evans 8 g** and **Garrett Wilson 7 g** sit in the **−27 to −41** dose band. **LaPorta 9 g**,
**McLaurin 10 g**, **Kittle 11 g**, **Odunze 12 g**, **Marvin Harrison Jr. 12 g** are in the
**−17 to −27** bands. All seven look like "he was productive per game and just got hurt." That is
the exact population §4.22(c) measured losing money.

---

## 4. WHAT THIS DOES NOT DO

- **Nothing is scored into `board_v8_fixed.csv`.** Surfaced only — same call as §4.22's `12g` badge
  and for the same reason: archetypes measured on external populations do not become VBD coefficients
  the day before a draft.
- **Draft capital is the strongest published signal on the RB side and we still cannot compute it
  at scale** — 71.4% of first-round RBs finish top-24 as rookies against **1.3%** for Day 3 (2 of 160).
  I sourced it by hand for the 17-man year-2 cohort only.
- **Batches B (picks 80–113) and C (128–161) are not run.**
