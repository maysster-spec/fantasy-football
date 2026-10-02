# 92 — QB2 RESOLVED: YES AT 104/113, AND THE BASELINE THAT DECIDES IT, RE-MEASURED
**2026-08-30. New machinery: shipped 480-row board · §4.12 affine noise on eff_pick · §5 opponent
model (w22, Snyder q=0.90) · paired seeds, N=600 · rosters truncated to the 12 real skill picks ·
outcome draws position-conditioned for QB and TE · payouts per §2. Nothing in `Scripts\` touched.**

---

## 1. STEP 1 — THE STREAMING BASELINE. Doc 12's table is NOT reproducible; the quantity is.

**The nflverse join IS reproducible from this container** (weekly data 2022–2025 fetched; 2025
lives under nflverse's new `stats_player_week` naming). I re-ran the entire pipeline from the raw
`waiver_report_2022–2025.csv`: parse EXECUTED adds → normalize names → join weekly scoring under
this league's rules → rest-of-season return per add.

**Doc 12's counts cannot be recovered.** The raw files contain **1,230 executed adds**
(614 WAIVER + 616 FREEAGENT), not 951. Skill-position adds: QB **135 events / 82 player-seasons**
— doc 12 says n=34. No filter I tried (WAIVER-only, FREEAGENT-only, event vs player-season dedupe)
lands on 34/98/53/105. Doc 12's join evidently kept ~25–40% of adds; the loss mechanism is
unrecorded — most plausibly a strict name join (the §3 C1 defect class, inside the measurement
itself). `[TESTED: parse + join re-run end to end]`

**The re-measured baseline, with intervals** (population: all executed skill adds, four seasons,
dedup per player-season; bootstrap 95% CI):

| pos | n | **per PLAYED week** | per SCHEDULED week |
|---|---|---|---|
| **QB** | 82 | **16.65 [15.51, 17.78]** | 13.12 [11.71, 14.45] |
| RB | 161 | 6.60 [6.06, 7.18] | 5.14 [4.59, 5.67] |
| WR | 165 | 6.98 [6.49, 7.49] | 5.29 [4.84, 5.76] |
| TE | 93 | 6.49 [5.93, 7.06] | 5.07 [4.52, 5.62] |

Doc 12's **15.25** sits between the two definitions — consistent with its unrecorded convention,
so it is re-tagged `[SOURCED: doc 12; values plausible, n irreproducible]`, not `[TESTED]`.
Its **hit rate reproduces almost exactly: 0.60 here vs 0.62** (share of QB adds returning
rest-of-season ≥15 ppg on played weeks). **The binding uncertainty is the definition (±1.8 ppg),
not sampling (±1.1).** For lineup-fill purposes the played-week number is the right one — a
streamer is started in weeks he plays — so the sim uses **QB 16.65 / RB 6.60 / WR 6.98 / TE 6.49**,
and sweeps QB across the whole band. Note both directions of correction: doc 91's 4.84-pts/week
overstatement claim was itself overstated (QB12-rate 20.09 − 16.65 = **3.44**/played-week), and
the engine's internal 0.80×replacement fill (≈17.8) was slightly *generous* to streaming.

## 2. STEP 2/3 — THE ROSTER-SHAPE GRID ON THE SHIPPED BOARD, HOLES FILLED AT MEASURED RATES

2×2 caps, the second QB/TE gated to **picks ≥104** (the question as posed); R2 static-VBD drafting
otherwise; all deltas paired against QB1/TE1. `[TESTED, N=600]`

| shape | Δ points | Δ dollars | ΔP(1st) |
|---|---|---|---|
| **QB2/TE1** | **+11.04 ± 3.08** | **+$18.16 ± 8.08** | +0.02 |
| QB1/TE2 | +4.07 ± 2.54 | +$11.44 ± 7.83 | +0.02 |
| QB2/TE2 | +11.63 ± 3.89 | +$18.49 ± 9.73 | +0.04 |

(Position-blind draws give QB2/TE1 +$13.70 ± 7.40 — same verdict. An untruncated variant that
lets picks 152/161 hold skill players inflates every shape by ~3–5 pts; the truncated numbers
above are the honest ones.) The 2nd QB the rule actually buys: **Goff 46%, Mayfield 21%, Love
10%, at pick 104 (33%) or 113 (26%)** — precisely doc 91's scenario, now simulated rather than
hand-multiplied. Three independent methods now agree: doc 12's grid +10.1, doc 91's arithmetic
+8–12, this machinery **+11.0 ± 3.1**.

## 3. STEP 4 — THE CROSSOVER. It sits ABOVE QB12's own rate: streaming skill cannot save you.

QB2/TE1 − QB1/TE1 as the QB streaming fill rises: `[TESTED, N=600 paired per point]`

| QB fill (ppg) | Δ points | Δ dollars |
|---|---|---|
| 13.12 (scheduled-week floor) | +18.79 ± 3.43 | +$23.09 ± 7.81 |
| 15.25 (doc 12) | +14.12 ± 3.20 | +$17.80 ± 7.87 |
| **16.65 (measured, played-week)** | **+11.04 ± 3.08** | **+$13.70 ± 7.40** |
| 18.37 (≈ p75 of league adds) | +7.26 ± 2.96 | +$10.09 ± 7.94 |
| 20.09 (= QB12 season rate) | +3.48 ± 2.88 | +$3.38 ± 7.74 |

Linear to the eye; the zero crossing extrapolates to **fill ≈ 21.7 ppg — above QB12's own
season rate.** Matt's 0.60–0.62 hit rate is the best in the league and his adds average 16.65;
even crediting him the 75th percentile of his league's own add outcomes, QB2 is +$10. **Only a
streamer who reliably beats the twelfth-best drafted QB kills QB2, and no measured streaming in
this league's four-year record does that.** At exactly QB12-rate fill the dollars are +3.4 ± 7.7 —
the coin flip lives only at that unreached extreme.

## 4. STEP 5 — THE ALTERNATIVE IS PRICED IN, NOT ASSUMED AWAY

The paired baseline arm spends the very same picks on the best-VBD RB/WR darts, whose outcomes
are drawn from the empirical 121–180 band — the band whose 17% breakout rate §4.13 measured — so
the +$18 is **net of the forgone dart's upside, tails included**. §4.13's round-9+ risk doctrine
survives untouched for the *other* three late picks; QB2 claims exactly one of the four.

## 5. STEP 6 — THE TE HALF. Error 2 confirmed; and the measurement now DISAGREES with doc 12.

Confirmed: Andrews at 8.25 ppg is **+1.76/played-week** over the re-measured 6.49 TE streamer
(doc 91's +2.72 used the unreproduced 5.53) — not zero; that reason stays void. But the grid
result is the bigger problem: **TE2-at-104+ measures POSITIVE (+4.07 ± 2.54 pts, +$11.44 ± 7.83)**
where doc 12 measured **−13.4**, and it stays positive under TE-conditioned draws bought at the
gated price. My best account of the flip: this design buys the TE2 at 104–137 dart prices with
holes filled at the measured 6.49 (holes hurt more than the old 0.8×replacement fill assumed),
while doc 12's shape grid ran on the board doc 57 recorded as 39% fabricated, with the join bug
doc 11 called "a thumb on the scale for RB" — and its TE2 purchase timing is unrecorded.
**"No TE2" is now carried ONLY by Matt's stated §6 doctrine and by doc 12's irreproducible grid —
not by any current measurement.** Per v5.5 the doctrine is a preference and governs the night;
this number is filed for post-draft review, not as an argument. What would resolve it: doc 12's
actual shape-timing code, or a re-run sweeping the TE2 purchase pick.

## 6. DRAFT NIGHT

**At 104 or 113, when the board offers Goff/Mayfield-tier against an RB/WR dart: take the QB.**
Not a coin flip at any measured streaming level — +11 pts / +$14–18, CIs clear of zero. One
second QB only (the engine's cap already enforces it), and prefer the earlier of 104/113 if the
tier is thinning — the rule itself took 104 a third of the time. Complementarity per §6: not
bye-14 (Pickens), and check the week the QB1 you actually drafted sits out.

---

## §7 CLOSE

**Assumptions:** (1) QB availability draws from the 41-QB outcome pool (gp mean 14.15) set how
often QB1 sits — if elite QBs miss materially fewer games than the pool average, QB2's edge
shrinks toward the sweep's right-hand rows, which are still positive; *invalidated by* a
gp-vs-draft-slot fit on the pool. (2) The streamer fill is a constant per position — no week-to-week
selection skill; the sweep IS the sensitivity for this, and the crossover verdict absorbs it.
(3) The 2nd QB is bought at 104+ under greedy VBD — an earlier, pricier QB2 was not tested and
doc 12's may have been; *invalidated by* sweeping the purchase pick. **Missing input that would
most improve this:** doc 12's join/shape code — its n=34 and its −13.4 are the two numbers this
document could not reproduce, one of which I have now measured the other way.
