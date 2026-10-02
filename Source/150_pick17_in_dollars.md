# 150 — Pick 17 in dollars: a decision (Henry, then Walker/Jeanty), then a tie — and Love vs Hall is the tie

**2026-09-03 · Fable · answers `FABLE_TASKING_PROMPT_5_pick17.txt` · supersedes doc 94 §2 for pick 17 ·
numbered 150 because `Source\` already holds 143–149 (the prompt's "143 should be free" predates them)**

**Love vs Hall is a tie** in every configuration tried — dollars within ±$7, points within ±1, CIs
±$12–15. **Neither shipped tool is measurably wrong about it.** The pick that matters at 17 is one
tier up: Henry, then **Walker or Jeanty over Hall by $14 [+1, +28]** — and both tools already
make that pick. The rest is a tie with two contaminated edges, one of which is a defect in the
outcome model that every dollar number this project has produced shares.

**PROVENANCE (§1.1, §3) — two halves that do not match, stated both:**
- **Market:** `adp_pick` / `eff_pick` / `gone_ahead` re-frozen **2026-09-03** to
  `espn_projections_2026_20260903_0902.csv` (`Scripts\live_draft\adp_vintage.txt`, read, not
  taken on trust). 426 of 480 `eff_pick` values differ from the 08-23 copy doc 94 ran on. On this
  board players at raw ADP 34.7–37.2 carry **`gone_ahead = 4`**, not §2.1's 3 — the depletion
  table has moved one keeper by pick 32 and nobody has re-solved it (doc 142 flagged this).
- **Points:** `proj_leaguepts` / `vbd` are still the **08-23 spine** — identical to doc 94's copy
  except Josh Jacobs zeroed by news (docs 143/144: cannot be rebuilt before Sept 7).
- `Source\games_2025.csv`: 479 rows, `espn_id` unique (the duplicate doc 140 found is gone).
- Pick-8 arm in every state and every arm: **best non-QB board player** (doc 70's arm; St. Brown
  72%, McCaffrey 10%, Taylor 5%, JSN 5%, Nacua 4%, Chase 2%, Bijan 1%, Gibbs 1%).

Machinery is doc 140's, pointed one turn earlier: **100 pick-17 states** from the §5 opponent model
(best-VBD-in-window-8, §4.12 affine noise on `eff_pick`, Snyder q=0.90) through the production
`code_live_engine.Engine` (`recommend(17, top=12, rollout_inner=60)`); **N=2000 paired drafts**
on common random numbers, doc-92 fills, H2H standings → §2 payout; `ctrl17` = best legal VBD at 17.
Sensitivities: opponent window 1 (the engine's own dispersion world) and 22, N=1000 each; the
§4.22(e) availability haircut as a separate column; and — new, forced by what the first pass
showed — the outcome pool with its 0–24 / 24–48 ADP bands merged, N=2000. Paired differences only.

---

## 0. The card

1. **If Henry is there (8%), take him. If not, Walker or Jeanty (one of them is there in 65% of
   drafts) — either; do not take Hall, Love, Lamb or anyone else over them.** Walker over Hall is
   **+$14–15 with the CI clear of zero in both outcome pools**; Jeanty over Hall is +$22 or +$7
   depending on the pool. The engine and the harness both already do this (87% / 90%).
2. **If none of the three is there (35% of drafts): Love ≈ Hall. Take whichever the board shows
   first.** Love − Hall on those drafts: **−$3.7 [−17.4, +9.6]** (banded pool) / **−$6.7 [−22.5,
   +9.1]** (merged), points −1.1 / −0.4. The engine's Love and the harness's Hall are the same pick.
3. **Do not override the board for Chase Brown or Lamb in that spot.** Their edges over Love
   (−$13 and −$43 in the first pass) are carried by a 3.5% step between two outcome-pool bands
   that is one standard error wide; merge the bands and they become +$7 and −$23, CIs spanning
   zero. Unresolved, and the board's ordering is not contradicted by anything robust.
4. **Hampton drops a tier on the badge.** 9 games in 2025 costs him **$12–17** in the adjusted
   column; unadjusted he ties Love/Hall, adjusted Love beats him +$17 [+5, +30]. Read the number
   on the badge (§4.22e).
5. **Still never at 17:** Jefferson −$20 [−30, −11], London −$34, Bowers/McBride **−$54/−55**,
   Allen −$37 [−109, +26] (n=35, unresolved, same lean as doc 94), Kyren/Collins/A.J. Brown/Nabers
   −$42 to −57. All CI-clear except Allen.

---

## 1. Falsifier, fixed before anything ran (same shape as #4)

- A candidate beats every other core name by > $15, CI clear → 17 has an answer.
- Core within ±$10, nothing CI-clear → CONFIRMED TIE.
- **Love vs top-VBD resolves either way with a clear CI → the headline** (two shipped tools disagree).

Result: **none of the three.** Not a flat tie — Walker/Jeanty beat Hall CI-clear; not a single
answer — no name clears every other; and **Love vs Hall does not resolve in any configuration**.
Love vs Lamb resolved for Lamb under the banded pool (−$43 [−72, −16], n=127) and un-resolved
when the bands were merged (−$23 [−52, +6]) — so it is not reported as a finding. `[TESTED]`

## 2. What the production engine says at 17 (100 states, inner=60)

| name | pos | VBD | eff ADP | engine **#1** | in top-3 | on board at 17 (sim) | harness #1 |
|---|---|---|---|---|---|---|---|
| Kenneth Walker III | RB | 81.2 | 25.0 | **31%** | 49% | 44% | **44%** |
| Ashton Jeanty | RB | 79.6 | 21.9 | **23%** | 30% | 29% | 12% |
| Jeremiyah Love | RB | 77.2 | 26.2 | **23%** | 65% | 69% | 0% |
| Derrick Henry | RB | 95.4 | 16.6 | 7% | 7% | 8.5% | 7% |
| Justin Jefferson | WR | 74.8 | 12.7 | 5% | 8% | 65% | 0% |
| Achane / Barkley / Cook | RB | 92.5 / 83.4 / 93.0 | 12–14 | 4 / 4 / 1% | — | 2 / 4 / 1% | 4 / 4 / 1% |
| Josh Allen | QB | 80.3 | 19.2 | 2% | 3% | 1.8% | 0% |
| Breece Hall | RB | 79.5 | 32.1 | 0% | 22% | 76% | **20%** |
| CeeDee Lamb | WR | 78.3 | 11.9 | 0% | 9% | 8% | 8% |
| Chase Brown | RB | 71.3 | 17.0 | 0% | **83%** | 92% | 0% |
| Omarion Hampton | RB | 67.3 | 18.3 | 0% | 15% | 99% | 0% |

Margin #1 over #2: median **3.50** (IQR 1.80–5.60, min 0.20). #1 is an RB in 93 states; #2 is
Chase Brown in 45, Love in 29. Engine and harness agree in **59/100**; the disagreements are
**Love over Hall (15), Jeanty over Walker (11), Love over Lamb (8), Jefferson over Hall (5),
Allen over Walker (2)**. Roll gaps where both are listed: Love − Hall **+4.9** (41 states, Love
ahead in all), Love − Lamb +3.2 (8), Love − Chase Brown +1.8 (59), Love − Hampton +5.2 (65);
Love − Walker **−3.6**, Love − Jeanty −4.6, Love − Henry −17.9. **The engine takes Love #1 only
when none of Henry/Walker/Jeanty is on the board — 0 of its 23 Love states had one.** When one
is, the engine takes one of them in 87% (the rest: Barkley, Achane, Cook — higher VBD — and Allen
twice), the harness in 90%. `[TESTED]`

`Source\decision_space.csv` (12 rooms, §4.12 noise only) lists Allen in 5/12 rooms at 17. That is
§4.15's failure mode — dispersion without Snyder — not corroboration of anything here; under the
calibrated model Allen is on the board at 17 in 1.8% of drafts.

## 3. Dollars

**(a) Policy — "take X at 17 if there," vs ctrl17, N=2000, banded pool.** Δ$ [CI] · Δpts · ΔP(1st)
pp · ΔP(top 6) pp · Δp10 pts.

| arm | avail | Δ$ | CI | Δpts | ΔP1 | ΔP6 | Δp10 |
|---|---|---|---|---|---|---|---|
| Henry | .085 | 0.00 | — | 0.0 | 0 | 0 | 0 |
| Barkley / Achane / Cook | ≤ .04 | −0.2 to +0.1 | within ±$0.9 | 0 | 0 | 0 | 0 |
| Lamb | .08 | −0.4 | [−1.7, +0.9] | 0.0 | 0.0 | +0.2 | 0.0 |
| Allen | .018 | −0.6 | [−1.9, +0.4] | −0.3 | −0.1 | −0.1 | −0.3 |
| Walker | .44 | −0.9 | [−3.0, +1.0] | −0.9 | −0.3 | −0.2 | −1.2 |
| Jeanty | .29 | −2.0 | [−5.0, +1.1] | −0.9 | −0.3 | −0.1 | −2.2 |
| Chase Brown | .92 | −8.8 | [−16.0, −1.8] | −1.0 | −1.7 | +1.0 | +3.5 |
| **Love** | .69 | **−9.8** | [−15.7, −3.9] | −4.0 | −1.7 | −0.6 | −0.7 |
| Hampton | .99 | −10.0 | [−17.1, −2.9] | −4.2 | −1.3 | +0.2 | −0.9 |
| **Hall** | .76 | **−11.8** | [−17.1, −6.8] | −7.1 | −2.2 | −1.0 | −2.2 |
| Jefferson | .65 | −13.3 | [−19.2, −7.3] | −7.3 | −2.1 | −1.2 | −2.1 |
| London | 1.00 | −33.6 | [−40.7, −26.5] | −22.6 | −5.8 | −4.0 | −18.6 |
| A.J. Brown | 1.00 | −44.6 | [−51.4, −37.7] | −31.3 | −7.3 | −6.9 | −22.2 |
| Kyren | 1.00 | −45.9 | [−53.4, −38.9] | −27.2 | −8.0 | −6.3 | −16.6 |
| Collins / McBride / Bowers | 1.00 | −53.9 / −53.9 / **−55.0** | all CI-clear | −36 to −39 | −8.7 to −9.2 | −7.9 to −9.0 | −29 to −35 |
| Nabers | 1.00 | −57.3 | [−64.2, −50.2] | −41.5 | −9.7 | −9.5 | −36.8 |

Henry is exactly 0.00 in all 2000 — the harness takes him on sight, as doc 94 found. The policy
column ranks *plans*: forcing Love or Hall whenever available costs $10–12 because it displaces
Walker/Jeanty/Henry in the drafts where they are there.

**(b) Head-to-head on the drafts where the choice is LIVE — no Henry, Walker or Jeanty on the
board (701 of 2000 = 35%), both names available, paired.** Two outcome pools, unadjusted:

| pair (row − col) | banded pool | **bands 0–24 / 24–48 merged** | n |
|---|---|---|---|
| **Love − Hall** | **−3.7 [−17.4, +9.6]** · pts −1.1 | **−6.7 [−22.5, +9.1]** · pts −0.4 | 525 |
| Love − Chase Brown | −13.1 [−24.4, −1.9] | **+7.0 [−5.7, +20.2]** | 667 |
| Love − Hampton | −9.4 [−20.7, +2.5] | +8.5 [−4.7, +21.8] | 667 |
| Love − Lamb | −42.8 [−71.7, −15.7] | −22.6 [−52.1, +6.2] | 127 |
| Hall − Chase Brown | −5.8 [−20.1, +7.7] | +17.8 [+3.0, +31.9] | 558 |
| Chase Brown − Hampton | +4.4 [−7.4, +15.9] | +3.8 [−6.8, +14.2] | 700 |

And across all common-availability seeds (the tier boundary):

| pair | banded | merged | n |
|---|---|---|---|
| **Walker − Hall** | **+15.4 [+3.2, +27.7]** | **+14.3 [+0.7, +27.6]** | 647 |
| Jeanty − Hall | +21.7 [+7.2, +36.5] | +6.5 [−10.4, +23.4] | 434 |
| Walker − Jeanty | −2.6 [−24.4, +19.3] | +1.9 [−17.7, +22.5] | 249 |
| Love − Walker | −9.8 [−24.2, +4.9] | −13.7 [−29.1, +1.4] | 475 |
| Love − Jeanty | −13.4 [−30.7, +5.1] | +6.2 [−13.6, +25.5] | 312 |
| Henry − Hall | +38.2 [CI clear] | — | 119 |

**Why there are two pools.** The first pass said Chase Brown beats Love by $13 and Lamb beats
Love by $43, CI-clear. Before writing that down I looked at what carried it: the outcome pool
draws a player's season by ADP band, and its **0–24 band has form mean 0.991 while 24–48 has
0.956** — a 3.5% step at pick 24, from n=48 seasons per band, SE ≈ 0.034: **one standard error
wide.** §4.23(b) measured the same gradient on a larger cut at ~1.1 points, a third of that. Chase
Brown (17.0), Lamb (11.9), Hampton (18.3) and Jeanty (21.9) sit on the good side of that line;
**Walker (24.97), Love (26.2) and Hall (32.1) sit on the other.** Every cross-boundary contrast
moved by $10–20 when the bands were merged; every same-side contrast (Love − Hall, Walker − Hall)
did not. **A contrast that flips on a one-SE feature of the simulator is not a finding**, and
that is why Chase Brown and Lamb are "unresolved" above rather than "better." `[TESTED, N=2000
each]`

**(c) Window sensitivity.** Under the engine's own dispersion world (window 1) a tier-2 RB is on
the board at 17 in 98% of drafts, so the Love/Hall question almost never arises; where it does,
Love − Hall is +$9.2 [−1.7, +20.4] over all common seeds (n=829) — same lean, still not clear.
Under window 22 the tier-2 RBs are always gone, Lamb is there 85% of the time and the
harness takes him; there Love beats *Lamb* by +$10 [+1, +19] (n=850). Love − Lamb therefore
changes sign across windows as well as across pools: **unresolved in both directions.**

## 4. The availability adjustment (§4.22e), same drafts re-scored

Relative haircut (≤6 g −28.2 · 7–9 g −14.5 · 10–12 g −4.3) from the current `games_2025.csv`,
178 of 480 board players touched. At 17 the touched names are **Hampton 9 g (−14.5), London 12 g
(−4.3), Bowers 12 g, Nabers 4 g (−28.2)**; Love (rookie), Hall 16, Lamb 13, Walker 17, Jeanty 17,
Henry 17, Chase Brown 17 carry none.

| conditional Δ$ vs ctrl17 | unadjusted | **adjusted** | WR-only (§4.22c) |
|---|---|---|---|
| Walker | −2.1 | −1.8 | −0.7 |
| Jeanty | −6.7 | −4.7 | −3.5 |
| Lamb | −4.9 [−20.6, +11.1] | −6.7 | −8.2 |
| Chase Brown | −9.5 | −5.5 | −7.9 |
| **Hampton** | **−10.1** | **−21.8 [−28.6, −14.6]** | −9.1 |
| Love | −14.2 | −12.1 | −14.3 |
| Hall | −15.5 | −16.4 | −16.4 |
| Jefferson | −20.6 | −19.5 | −18.2 |
| London | −33.6 | −32.9 | −34.4 |
| Nabers | −57.3 | −75.9 | −75.1 |

Live-subset head-to-heads after adjustment: Love − Hall **−5.2 [−18.4, +7.6]** (banded) / −13.8
[−28.3, +1.3] (merged) — still spanning zero; **Love − Hampton +3.7 → +17.5 [+5.1, +30.4]**
(merged), Chase Brown − Hampton +20.3 [+10.6, +30.6]. **The adjustment moves exactly one name at
17 — Hampton — and it moves him out of the tie.** Everything else is inside its own interval.

## 5. Verdict — a decision, then a tie, with two contaminated edges

- **Decision:** Henry > Walker ≈ Jeanty > the rest. Walker over Hall +$14 CI-clear in both pools;
  Henry over Hall +$38. Both tools already make this pick; the only measured slip is the engine's
  Allen-over-Walker in 2 of 100 states, and Allen at 17 is −$37 [−109, +26] (n=35) — unresolved,
  same lean as doc 94's −17.7 points.
- **Tie:** Love ≈ Hall, on the drafts where it is live, in every configuration (−$3.7 / −$6.7 /
  −$5.2 / −$13.8, all CIs spanning zero, points within ±1.2). **The engine is not reaching for
  Love and the harness is not reaching for Hall; they are picking the same coin.**
- **Contaminated edge 1 — Hampton:** ties unadjusted, loses by $17–20 once his 9 games are read.
- **Contaminated edge 2 — the outcome pool's 24-pick band step:** it manufactures a $13 Chase
  Brown edge and a $43 Lamb edge that merging the bands removes. Chase Brown and Lamb are
  therefore unresolved against Love, not ahead of him.
- **Jeanty over Walker** (engine, 11 states): −$2.6 / +$1.9 — a tie; either is fine.

## 6. What I could not check, and what this exposes

1. **The band step is in every dollar number this project has produced** — docs 70, 92, 94, 140
   and this one all draw RB/WR seasons from the same six-band pool (QBs and TEs draw from their
   own position pools and are untouched). It only matters for a contrast that straddles a band
   edge. Pick 8 (St. Brown 8.4 vs Allen, QB-conditioned) does not. **Pick 32 does not either:**
   its core — Kyren 31.2, Judkins 39.0, Hall 32.1 (band 24–48), Bowers and McBride (TE pool),
   Lamar (QB pool) — and its separated names (Egbuka 36.9, Adams 37.2, DeVonta 32.8, Nabers 31.0)
   all sit inside one band, so doc 140 stands as written. Pick 17 is the first place the edge
   falls between live candidates. Flagged for the post-draft rebuild of the outcome pool, which
   needs more than 48 seasons per band or a smooth fit across ADP instead of steps.
2. **QB survival** (doc 142's warning): the model still lets QBs survive on dispersion. At 17 no
   QB is in the core, so it enters only through the continuation, identically in every arm; the
   one QB arm (Allen) is unresolved on its own n. The 11.8-point plateau bound (§4.15) still caps
   what a real QB run can do to the waiting path — and here it would only make Allen-at-17 look
   marginally better, never Walker-or-Jeanty-at-17 worse.
3. **Continuation after 17 is static VBD** (QB2/TE1, gate 104), common to every arm. It is why
   the sim and the engine can agree on the tie while the engine still lists Chase Brown second by
   1.8 roll points — the engine's lookahead and my pool step are both inside the noise.
4. **Head-to-head n** for the rare names (Lamb 127–133, Henry 51–119, Barkley/Achane/Cook/Allen
   under 90) — reported with their intervals; none of them changes the card.
5. **Doc 94's pick-17 half:** its verdicts survive in direction — Henry first, Hall behind
   Walker (was −$9, now −$14 to −15), TEs out (were −$39/−46, now −$54/−55 on this board), WR
   reach out (Jefferson −$20). What changed is the market: on the 09-03 ADP Walker and Jeanty
   are on the board at 17 in 44% / 29% of drafts (08-23: 25% / 8%), so the tier-2 pick is live
   in two thirds of drafts rather than a third.

## 7. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *The §5 opponent model's depletion by pick 17* — it sets how often Henry/Walker/Jeanty are
   there (8 / 44 / 29%). A faster room (window 22) removes them and makes Lamb the harness's pick
   85% of the time; a slower one (window 1) makes the tie moot. The *ordering* Henry > Walker ≈
   Jeanty > Love ≈ Hall held in every window that could measure it.
2. *The merged-band outcome pool is closer to truth than the banded one at the 24 edge* —
   supported by §4.23(b)'s 1.1-point gradient against the pool's 3.5, and by n=48 per band. If
   the 3.5% step were real, Chase Brown and Lamb would move ahead of Love by $13–43 and the card's
   item 3 would flip. Nothing available before Sept 7 tests it.
3. *Prior-season games at §4.22(e) magnitudes* — carries Hampton's demotion alone.

**Most valuable missing input:** the actual keeper list at the 7:00 PM lock — `gone_ahead` on the
09-03 board already disagrees with §2.1's table by one keeper at pick 32, and one surprise keeper
in the 16–36 band redraws who is on the board at 17. Second: a larger outcome pool (2021, 2023,
2025 seasons) to settle the band step for good.

**Artifacts:** `k5_state.py`, `k5_price.py`, `k5_an.py`, `state17_*.csv`, `early8_*.csv`,
`price17_w8_*.csv`, `price17_w1_*.csv`, `price17_w22_*.csv`, `price17_w8m01_*.csv` — bundled in
`Source\k5_artifacts.zip`. Seeds 250000+s, the same convention as docs 94/138/140.
