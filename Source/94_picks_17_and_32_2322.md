# 94 — Picks 17 and 32, measured in dollars on the shipped board

**2026-08-31 · Fable · answers `FABLE_TASKING_PROMPT_2_picks_17_32.txt` · supersedes doc 09 §5 for both picks**

Machinery: the /tmp/eng harness — shipped `board_v8_fixed.csv` (480 rows, all 12 predicted
keepers verified absent; Trevor ≠ Travis Etienne checked), §4.12 affine noise on `eff_pick`,
§5 opponent model (best-VBD-in-window, OPP_WINDOW=8 primary / 22 sensitivity), Snyder q=0.90,
doc 92's measured streaming fills (QB 16.65 · RB 6.60 · WR 6.98 · TE 6.49 per played week),
v5 replacement, payout per §2. **N=1500 paired seeds** (common random numbers: same opponent
noise, same Snyder draw, same player outcomes across arms), sensitivities N=600.

Arms are **policies**, not certainties: "take X at pick P *if he is on the board*, else the
engine's best legal pick (QB2/TE1 shape, gate 104)." Policy deltas are the decision-relevant
number; conditional-on-available deltas are also given where they differ. All deltas are paired
against the control (engine free at every pick). Per §5, no absolute win probabilities anywhere.

---

## 0. The card

1. **Pick 17: take the best player on the board, which in practice means the top RB.** The
   engine's free choice already IS the answer — forcing Henry when available is *identical to
   control in every one of 1500 seeds* (Δ = exactly 0.00; he is the board's top VBD at 17
   whenever he survives). No deviation from board order survives measurement.
2. **Pick 32: coin flip, exactly as doc 09 said — but now on machinery that can be trusted.**
   Hall/Jacobs-if-they-slip, Bowers, McBride, Judkins, Adams, Kyren are all within ±$1.5
   (policy) of the engine, CIs overlapping zero. **Two names are now clearly out: Burrow
   −$13.30 [−22.4, −3.3] and Warren −$14.00 [−22.2, −5.9].**
3. **The 17→32 pair prices as two independent picks.** Matt's pick-17 choice moves the
   pick-32 availability of every tracked name by ≤ 2.5 percentage points (table §4). The
   prompt's hypothetical — "−2 alone but +6 through its effect on 32" — does not exist on
   this board.
4. **Bye collisions are worth 0.0–1.2 points, ever** (§5). Tiebreaker at an exact tie;
   never worth passing a better player.

---

## 1. The pick-8 conditioning arm (step 1)

Conditioned on **doc 70's closed answer: best non-QB board player at 8.**

- Under OPP_WINDOW=22 the arm takes **St. Brown 600/600** — doc 70's "120/120" reproduces
  exactly. `[TESTED, N=600, w22]`
- Under the primary w8 model it is **St. Brown 79.1%**, and the remainder is a *strictly
  better* player who slipped (Taylor 7.0%, McCaffrey 5.7%, Nacua 2.9%, JSN 2.5%, Chase 1.2%,
  Bijan 0.9%, Gibbs 0.6%) — the rule takes him. Same policy, different window; nothing
  downstream inherits an error. `[TESTED, N=1500, w8]`

---

## 2. Pick 17 (step 2) — the slate

Paired vs control, N=1500, w8. "avail" = P(on the board at 17) under the model
(§7 rule: simulated survival has run low against every checkable observation — treat as
lower bounds; §4.15 applies, these come from the full opponent model, not dispersion alone).

| arm (policy) | avail | Δ pts | Δ $ | 95% CI ($) | conditional-on-available |
|---|---|---|---|---|---|
| **Henry** | 0.14 | **0.00** | **0.00** | [0, 0] | identical to control — engine already takes him |
| Jeanty | 0.08 | +0.1 | +1.2 | [−0.4, +2.9] | +1.6 pts, +$14.6 [−5.1, +36.3] — n=124, unresolved |
| Walker | 0.25 | +0.1 | −0.2 | [−2.3, +1.7] | +0.5 pts — co-optimal with board order |
| Allen | 0.026 | −0.5 | −0.5 | [−1.8, +0.7] | **−17.7 pts [−40.6, +3.1]**, n=39 |
| Hall | 0.65 | −4.9 | −6.0 | [−10.9, −1.3] | −7.6 pts, −$9.2 [−16.6, −2.0] |
| bestWR | 1.00 | −5.5 | −8.5 | [−16.8, −0.1] | (Lamb/Jefferson when slipped, else London) |
| Jacobs | 0.99 | −15.9 | −23.7 | [−32.0, −15.7] | ≈ policy |
| Hampton | 1.00 | −17.8 | −21.3 | [−29.7, −13.4] | ≈ policy |
| **Bowers** | 1.00 | **−30.9** | **−39.3** | [−48.6, −29.5] | ≈ policy |
| **McBride** | 1.00 | **−30.8** | **−46.1** | [−56.0, −36.3] | ≈ policy |

What "best board player at 17" actually is, over 1500 drafts: Hall 35% · Walker 20% ·
Lamb 15% · Henry 14% · Barkley 7% · Jeanty 5% · Allen 1.4% · Cook 1.4%. The engine takes
Hall at 17 in a third of drafts — *taking* Hall is often right; *forcing* him over a
surviving Henry/Walker/Lamb is what costs the −$9.2.

**Doc 09 confirm-or-kill:**
- Henry +0 baseline → **CONFIRMED in the strongest form** (force-Henry ≡ control, 1500/1500).
- Walker −5.3 → now **0.0**: co-optimal. Hampton −2.9 → **−21**. Jacobs −6.7 → **−24**.
  Hall −15.9 → **−9.2** (conditional). Magnitudes were board artifacts; order mostly survives.
- Bowers −26.5 / McBride −26.8 → **CONFIRMED and slightly worse in dollars** (−$39 / −$46).
- **Allen "+5.3 if he survives" → KILLED.** Survival to 17 is 0.026 (matches §4.2's ≈0.03),
  and *even conditional on surviving*, taking him measures −17.7 pts (CI touches +3.1;
  n=39). The pick-17 Allen question has the same answer as the pick-8 one: no.

## 3. Pick 32 (step 3) — corrected depletion (3 keepers gone, eff ≈ 35)

Conditioned on best-board at 8 and 17. Paired vs control, N=1500, w8.

| arm (policy) | avail at 32 | Δ pts | Δ $ | 95% CI ($) | conditional Δ$ |
|---|---|---|---|---|---|
| Bowers | 0.24 | −0.4 | +0.2 | [−1.6, +1.8] | +0.7 [−6.7, +7.7] |
| McBride | 0.17 | −0.0 | +0.0 | [−1.8, +1.9] | +0.1 [−10.4, +10.1] |
| Jacobs | 0.09 | 0.00 | 0.00 | [0, 0] | engine already takes him on sight |
| Hall | 0.02 | 0.00 | 0.00 | [0, 0] | engine already takes him on sight |
| Adams | 0.35 | −0.7 | −0.1 | [−3.6, +3.4] | −0.2 |
| Kyren | 0.19 | −0.5 | −1.0 | [−3.7, +1.6] | −5.2 [−19.4, +8.3] |
| Judkins | 0.55 | −1.5 | −1.3 | [−5.5, +2.7] | −2.4 |
| Lamar | 0.50 | −1.4 | −3.8 | [−10.8, +3.2] | −7.6 [−21.5, +6.4] |
| **Burrow** | 0.99 | **−9.8** | **−13.3** | [−22.4, −3.3] | ≈ policy |
| **Warren** | 0.99 | **−12.9** | **−14.0** | [−22.2, −5.9] | ≈ policy |

**FLAT.** Doc 09 called pick 32 "a ±4 coin flip, call it on roster fit and bye" — that
verdict **survives** re-measurement on the corrected depletion, the real board, the affine
noise, and in dollars. The ordering *inside* the flat cluster scrambled (Kyren +3.8 → −1.0,
Bowers −2.0 → +0.2), which is what flat means. The engine's own behavior at 32: Judkins 23% ·
Bowers 21% · Adams 14% · McBride 13% · Kyren 11% · Jacobs 9% (= every time he's there) ·
Hall 2% (same). A TE **as the TE1** at 32 is fine (engine's own choice in a third of drafts);
this does not touch the §6 TE2 doctrine.
- Doc 09's only clear negatives → **CONFIRMED and amplified: Burrow −$13.3, Warren −$14.0.**
  The WR30 correction and depletion fix did NOT flip the RB-vs-TE cluster — the headline the
  prompt anticipated ("WR replacement correction alone flips it") did not materialize.

## 4. The pair (step 4) — there is no pair

P(name available at Matt's pick 32) by pick-17 choice — the full cascade:

| pick-17 arm | Bowers | McBride | Judkins | Adams | Kyren | Jacobs |
|---|---|---|---|---|---|---|
| control | .238 | .173 | .553 | .345 | .193 | .089 |
| any RB (Henry/Hall/Walker/Jeanty) | .238–.239 | .173–.174 | .553–.555 | .345 | .193 | .089 |
| Bowers | .000 | .182 | .563 | .369 | .200 | .093 |
| McBride | .244 | .000 | .563 | .360 | .198 | .091 |

Fourteen opponent picks sit between 17 and 32; removing one player at 17 washes out to
≤ 2.5 points of availability anywhere. **Price the picks independently.**

**"TE at 17 as survival insurance" — killed three ways:**
1. Base model (w8): Bowers still on the board at 32 in 24% of drafts, and taking him there
   is free (+$0.7 conditional). Reaching at 17 costs −$39 to buy insurance he doesn't need.
2. herman allen sensitivity: slot 5 re-modeled to value TEs at raw ADP (no +15 shift — his
   picks are 20 and 29). Bowers-at-32 falls to 3.2%, McBride to 5.8% — and **Bowers-at-17
   still measures −24.5 pts [−30.7, −18.2]** (N=600). When the TE truly won't come back, the
   engine simply takes Judkins/Adams at 32 and buys the TE1 later; reaching still loses.
3. w22 sensitivity: TE survival to 32 ≈ 0; Bowers-at-17 = −13.6 pts, McBride −14.9. Negative
   under every opponent model tried. `[TESTED, all three]`

## 5. Bye collisions (step 5) — measured, small

Scoring-side counterfactual on control rosters: same draft, same outcomes, one player's bye
moved to the roster's emptiest week 5–12. The de-stack gain IS the collision cost.
N=1500 drafts, natural incidence. Points, not dollars — payout deltas are noise (±$5) at
this effect size.

| collision | incidence | cost (pts) | 95% CI |
|---|---|---|---|
| **Lamb + Pickens, both WR, week 14** | 15% of drafts | **1.16** | [+0.68, +1.62] |
| pick-17 bye-13 RB + Bowers (wk 13) | 12% | 0.45 | [+0.08, +0.84] |
| second bye-13 body vs first (p17 side) | 28% | ~0.1–0.3 | overlaps 0 |
| McBride + Pickens (TE+WR, wk 14) | 13% | **0.02** | [−0.36, +0.43] |
| moving a lone bye (control) | — | −0.35 to +0.15 | overlaps 0 |

The **largest measured collision in the draft is ~1.2 points** — Lamb-at-17 stacking Pickens,
same position, same week — and even that is under half a VBD tier. The week-13 RB+TE stack
§4.11 worries about costs ~0.5–0.8. Cross-position stacks (McBride+Pickens) cost **nothing**:
the TE fill and the WR bench cover independently. **Rule: byes break exact ties only.** At 17,
Lamb vs Hall/Jeanty within ~1 VBD → take the RB; that is the only live case found.

## 6. What I could NOT check (step 6)

1. **Per-manager behavior beyond Snyder.** One pref model + window for all 11 opponents;
   herman allen's TE timing was bracketed by sensitivity, not fitted (2 observed early-TE
   picks can't fit a parameter). QB-timing tendencies (§5 table) are not in the model at all.
2. **OPP_WINDOW.** w8 vs w22 moves every survival number hugely (Henry-at-17: 14% vs 0.2%).
   Directions and the card's decisions are stable across both; the *availability* numbers
   are model quantities. Treat p(avail) as lower bounds per §7, and don't quote them as odds.
3. **Streaming fills flatter rostered depth** (doc 93's caveat, inherited here): no
   week-to-week matchup selection for the streamer. Biases *against* the TE-at-17 arms
   slightly... in both directions across arms; it cannot rescue a −$39.
4. **Dollar CIs on ±$1-scale questions.** The payout table is lumpy; nothing inside the
   pick-32 cluster can be separated in dollars at any feasible N. That IS the "flat" verdict.
5. **Predicted keepers, not actual.** All runs use the 12 predicted keepers. Keeper lock is
   Sep 7, 7:00 PM; a surprise keeper (e.g., an unexpected RB kept) changes depletion and the
   32 slate. Re-run is `keeper_swap.py` + this harness if the lock surprises.
6. Doc 09's point estimates were confirmed/killed against **its own** stated numbers; its
   machinery (v4 noise, 39%-fabricated board) was not resurrected to decompose *which* input
   moved each number. Not worth the tokens — every input changed at once.

## 7. Close (§7)

**Top 3 assumptions → what would invalidate each:**
1. *Opponents draft best-VBD-in-window off eff_pick with affine noise* → a real draft where
   several managers chase needs early (3 QBs inside 30 picks) would break the survival
   tables; the pick-17 VBD ordering itself would survive.
2. *The 12 predicted keepers* → keeper lock Sep 7 7:00 PM. Any surprise keeper in the
   eff 8–45 band invalidates §2–§4 availability numbers (not the TE/Burrow/Warren verdicts).
3. *ESPN's projections are the outcome mean* (shared by board and scoring; §5's reason to
   ban absolute probabilities) → nothing at these picks hinges on a single projection, but
   Henry-vs-field at 17 does lean on his +95.4; a real injury downgrade before Sep 7 (news
   pass, Sep 5) reorders the top of the 17 slate.

**Most valuable missing input:** the actual keeper list at lock (free on Sep 7) — nothing
else moves these two picks. Second: any real per-manager draft tendencies for slots 1–7
(they pick 9 of the 14 slots between Matt's turns at 17→32... they ARE the survival model).

**Run artifacts:** `/tmp/out/task2_*.csv` (p17, p32, pairs, byecf, w22, allente),
`/tmp/eng/task2.py`, analysis `/tmp/eng/t2an.py`. Seeds 250000+s, N=1500 primary.
