# 138 — Does a kept player's value persist? No. The RB dart's keeper option is ≈ +0.7, not +8.

**2026-09-03 · Fable · answers `FABLE_TASKING_PROMPT_3_keeper_persistence.txt` · extends §4.18**

Inputs: `draft_history_2021_2025.csv` (894 rows, `Keeper` flag; 12 keepers every season; 46 of the 48
keepers 2022–25 are verifiably round-5+ picks the year before — the other two, Hubbard and
Conner 2024, fall in the two rows the 2023 file is missing), nflverse weekly
2021–2025 (REG, weeks 1–14, §2 scoring: 6-pt pass TD, 0.5 PPR, −2 INT/fumble, 2-pt = 2, return
TD 6), and the sanctioned ADP registry through `code_adp_guard.load_preseason_adp()` — **no
historical `espn_adp` was touched (§1.1).** Joins: normalized name + position → nflverse
`player_id`, then ids everywhere; 755 of 765 QB/RB/WR/TE draft rows matched, the 10 misses are
name variants of non-keepers (Gabe Davis, Robbie Chosen, Will Fuller, Josh Palmer, Chig Okonkwo,
Marquise Brown ×2, Bernhardt, Travis Hunter) and touch nothing below.

**BASELINE, stated once for every number:** value = **VBD14** = a player's weeks-1–14 points minus
the **same season's** 30th RB / 30th WR / 12th QB / 12th TE weeks-1–14 total (§4.1's cutoffs, on
actuals). Not §4.1's 2026 projection levels — those are 17-game projections and cannot be laid
over 2021–25 actuals without a scale assumption. Scale check: on this measure an **RB5–RB10
finisher averages +81.4** (n=30, 2021–25), so §4.18's "+85" anchor translates almost exactly.
A season with no games = 0 points = −replacement, not missing. `[TESTED]`

---

## 0. The card

1. **The RB dart's keeper option is worth ≈ +0.7 points [−2.0, +3.1], not +8.** A kept RB
   returns **+6.7 VBD14 [−20.1, +31.4]** in the season he is kept (n=18, this league,
   2022–25), against the +81 §4.18 assumed. 10.0% × 6.7 = 0.7.
2. **§4.18's draft-night rule at 104/113 resolves toward the QB.** The +8 that made QB2 (+5 to
   +11, docs 92/111) and the RB dart "nearly cancel" does not exist; the gap is now roughly
   **+4 to +10 points in QB2's favour**, each side measured once. New wording in §4.
3. **This is not a league quirk — late hits do not persist anywhere.** NFL-wide, on the
   registry market: an RB who hit from preseason ADP 97+ returned **−3.9 VBD14 [−26.4,
   +20.4]** the next year (n=21); the same-size hit from ADP 1–48 returned **+44** (n=32).
   The market knew which hits were talent and which were circumstance.
4. **Every positional cut here is under n=30 and is labelled UNDERPOWERED.** What carries the
   conclusion is that two populations, the early-ADP benchmark, three hit thresholds and the
   per-game decomposition all land on the same side of a falsifier fixed in advance.

---

## 1. The falsifier, fixed before anything was computed

§4.18 prices the option at 10.0% × +85 = +8.5. The rule it feeds says QB2 (+5 to +11) and the
RB option "nearly cancel — take the better player." Written down before the first number:

- **Option < +4** (E[VBD14 | kept RB] < +40, i.e. less than half the anchor) → the option is
  worth *less* than §4.18 says and the rule resolves toward QB2.
- **Option > +11** (E[VBD14] > +110) → worth *more*, resolves toward the RB.
- **A CI spanning both bounds** → the sample cannot resolve it; the rule stands unchanged.

Result: **+6.7 [−20.1, +31.4].** The whole interval sits below +40. The falsifier fires the
first way. `[TESTED, n=18]`

## 2. The 48 keepers, 2022–2025

| pos | n | mean VBD14 **before** | mean VBD14 **kept season** | Δ (95% CI) | still > 0 next yr |
|---|---|---|---|---|---|
| RB | 18 | +21.9 | **+6.7** | −15.2 [−45.9, +15.4] | 61% |
| WR | 15 | +9.3 | **−0.8** | −10.1 [−27.4, +5.4] | 67% |
| QB | 9 | +29.6 | **−55.7** | −85.3 [−161.7, −8.4] | 33% |
| TE | 6 | +21.3 | **+5.4** | −15.9 [−42.3, +14.8] | 33% |
| **all** | **48** | **+19.3** | **−7.5** | **−26.8 [−48.6, −6.7]** | 54% |

Every cut UNDERPOWERED except the pooled row. The retention *ratio* the prompt asked for is
reported as Δ instead: with prior means this close to zero the ratio's bootstrap is unbounded
(RB: 0.31 [−1.8, +2.7]) and says nothing.

Two things the table hides:
- **Managers do not keep last year's VBD; they keep names.** 7 of 18 kept RBs had *negative*
  VBD14 the year before (Cook, Mattison, Elliott, Conner '24, Taylor '24, Javonte '24, Ekeler).
  The "hit" population §4.18 imagines (RB5–10, +81) is not who gets kept. Kept RBs finished a
  median **RB25** in their keeper season; two finished top-10 (Kamara, Montgomery — both
  round-6/7 picks, not darts).
- **The late-round subset is where the option lives, and it is worse.** Kept RBs drafted in
  round 9 or later the year before: n=7, **+31.3 → −2.5** (Fournette +104→+45, Walker +33→+18,
  Stevenson +65→+8, Robinson +43→+13, Mattison −51→−8, Elliott −15→−75, Irving +40→−18).
  UNDERPOWERED; direction matches every other cut.
- Matt's own four (2022–25): Chase +69→+39, Mattison −51→−8, LaPorta +50→−4, Daniels +50→−131.
  n=4, colour only.

## 3. Survivorship — the two controls the prompt required

**(a) Same-league matched control.** Round-5+ draftees who hit (VBD14 > 0) and were **not**
kept, the 3 nearest by prior VBD to each kept hit, same position:

| pos | kept hits: prior → kept season | matched non-kept: prior → next season |
|---|---|---|
| RB (n=10) | +55.7 → **+12.4** | +53.9 → **−20.0** |
| WR (n=10) | +34.8 → +12.1 | +32.1 → −3.4 |
| TE (n=3) | +50.8 → +42.2 | +50.3 → −2.5 |
| QB (n=7) | +42.5 → −59.2 | +36.1 → −28.9 |

Managers' selection carries real information at RB/WR/TE — the kept player beats a look-alike
who was not kept by ~+30. **Selection is not the problem. The level is:** the *favourable* side
of the comparison is +12, not +81. `[TESTED, UNDERPOWERED]`

**(b) NFL-wide, on the sanctioned preseason market.** Every player-season 2021–24 with a
registry ADP, hit = VBD14 > 0 that year, outcome = VBD14 the next year:

| RB, preseason ADP band | n | hit size (VBD14) | **next season** | 95% CI | still > 0 | per-game VBD | games |
|---|---|---|---|---|---|---|---|
| 1–48 (rounds 1–4) | 60 | +67.0 | **+47.5** | [+29.0, +65.7] | 78% | +5.4 → +4.5 | 11.9 → 11.4 |
| 49–96 (rounds 5–8) | 30 | +46.7 | **−8.1** | [−27.0, +10.8] | 43% | +3.3 → +0.2 | 12.3 → 10.3 |
| **97+ (rounds 9+)** | **21** | +35.0 | **−3.9** | [−26.4, +20.4] | 38% | **+2.8 → +0.3** | 12.3 → 10.9 |

Matched on hit size (20 ≤ VBD14 ≤ 80): **early 47.6 → +44.2 (n=32); mid 42.5 → −10.0 (n=21);
late 42.3 → −23.1 [−51.9, +9.7] (n=10).** Threshold sensitivity for the late band: hits ≥ 0 →
−1.7 (n=23); ≥ 20 → −23.1 (n=12); ≥ 40 → −14.1 (n=7). Same sign at WR (late 20.8 → −13.6,
n=23), QB (34.5 → −42.7, n=11) and TE (16.6 → −13.2, n=20). `[TESTED; late cuts UNDERPOWERED]`

**Read of the mechanism:** the collapse is per-game, not injury — late hits' VBD per game falls
from +2.8 to +0.3 while games fall only 12.3 → 10.9; early hits keep 84% of their per-game
value. **Regression to the mean is the null, and the early band shows plain regression
(0.71 retention). The late band does not regress toward the mean — it regresses through
replacement.** A late hit is, on average, a role that existed for one year.

The names, so this can be checked: the 21 late RB hits' next seasons run Mostert −66, Jamaal
Williams −92, Gus Edwards −75, Pierce −54, Moss −45, Ford −41, Perine −41, Warren −40, Tracy
−30, Irving −18, Hubbard '24 −12, Dobbins 0, Charbonnet 0, Dillon +1, Robinson +13, Conner +20,
Dowdle +58, Hubbard '23 +67, Achane +83, Kyren +93, Pollard +97. Five real assets in 21; mean
−3.9. **The option is a lottery on a lottery, and its mean is zero.**

## 4. Re-pricing §4.18

| | §4.18 said | measured |
|---|---|---|
| P(round-9–12 RB becomes a keeper) | 10.0% (n=50) | unchanged — not re-measured here |
| E[VBD in the keeper season] | ~+85 (RB5–10 on the 2026 board) | **+6.7 [−20.1, +31.4]** kept RBs (n=18); **−2.5** late-round kept (n=7); **−3.9** NFL late-ADP hits (n=21) |
| **RB dart's keeper option** | **≈ +8.5** | **≈ +0.7 [−2.0, +3.1]** |
| QB dart's keeper option | 16.7% × ~+3 ≈ +0.5 | kept QBs **−55.7** (n=9), NFL late QB hits −42.7 (n=11) → **≤ 0** |
| QB2's 2026 edge (docs 92/111) | +5 to +11 | not re-measured; taken as is |

Two corrections that only make the option smaller and are not priced above: Matt keeps **one**
player, so the dart's option is its value *over his next-best eligible keeper*, not over
replacement; and a kept player's 2027 points are a year further off than QB2's 2026 points.

**DRAFT-NIGHT RULE, revised (replaces §4.18's last paragraph):** at 104 or 113, if a QB of
Goff's tier or better is on the board, **take the QB2.** The RB dart's keeper case was worth
+8 on an assumed number and measures ≈ +1 on real seasons; QB2's +5 to +11 no longer has an
offset. Take the RB only when no such QB is there, or when the RB is the better *2026* player
by the board's own VBD — the 2027 story is not a tiebreaker anymore. `[TESTED, one measurement
per side, see §5]`

**A wider reading, for post-draft only:** across all 48 keepers this league has kept, the
keeper-season return averages **−7.5 VBD14 [−25.7, +10.1]** (median +7.8; +3.6 [−11.8, +19.0]
excluding the QBs). **The keeper slot, as this league uses it, returns about replacement level.**
§6's "every round-5+ pick is a keeper audition" is priced by this — it is worth auditioning,
but not paying for. Not for the card; filed.

## 5. What I could not check, and the limits that stand

1. **n.** 18 kept RBs, 7 late-round, 21 NFL late hits, 10 size-matched. Every positional
   number is UNDERPOWERED by the prompt's own rule. The conclusion rests on *direction agreeing
   across independent cuts against a pre-fixed threshold*, not on any one interval.
2. **Two populations, one scoring input.** The league keepers and the NFL registry pool are
   different selections, but both are scored on the same nflverse × §2 pipeline and the same
   VBD14 definition. That is two measurements, not three, and they share an input.
3. **The registry is heterogeneous** (2021 ADP#, 2022 FP ADP, 2023 Underdog best-ball, 2024 a
   consensus *rank* proxy, 2025 nine-site). "ADP 97+" means slightly different things by year.
   It is still the only market §1.1 allows, and the early/late split is coarse enough to survive it.
4. **P(kept) was not re-measured.** The 10.0% is §4.18's own figure; if it is also optimistic
   the option is smaller still, not larger.
5. **The QB keeper collapse is injury-heavy** (Burrow ×2, Daniels, Dak, Cousins, Stroud — 5 of 9
   missed 4+ of 14 weeks). Four seasons cannot tell "QBs get hurt" from "this league had a bad
   run." It does not matter for the rule: both keeper options round to zero either way.
6. **Not tested:** whether Matt's own selection beats the league's (n=4), whether a kept player's
   value persists into a *third* year, and the alternative-keeper displacement in §4.

## 6. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *VBD14 against same-season rank cutoffs is the right value scale* → if the option should be
   priced in 2027 draft-capital terms (what the kept player would cost to re-draft) rather than
   realised points, a kept RB25 is still a round-6 pick's worth — re-run with the registry as the
   outcome; direction cannot flip, size might.
2. *2021–25 is representative* → one more season with two Kyren/Achane-class late hits among
   ~6 would lift the late-band mean toward +15; it would not reach +40.
3. *P(kept)=10.0% stands* → if Matt's own hit-and-keep rate on RB darts is materially higher
   than the league's, the option scales with it — but he would need ~5× the league rate to
   recover +4.

**Most valuable missing input:** 2026 realised values, in five months — one more transition
adds ~12 keepers and ~6 late RB hits. Nothing available before Sept 7 moves this.

**Artifacts:** `k3_build.py`, `k3_keepers.py`, `k3_control.py`, `vbd_seasons.csv` (2,710
player-seasons), `keepers_valued.csv`, `league_pool.csv`, `nfl_pool.csv` — bundled in
`Source\k3_artifacts.zip`.
