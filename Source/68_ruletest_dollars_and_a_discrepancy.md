# 68 — §4.10 IN DOLLARS, AND THREE DIFFERENT NUMBERS FOR THE SAME COMPARISON

**2026-08-28.** Answers the "does the pick rule matter" question from the Fable tasking prompt,
using files already in `Source\`. No simulation was re-run.

---

## 1. THE DOLLAR ANSWER — it was already computed

`risk_summary_w22.csv`, in `Source\`, carries an `E_payout` column against the §2 table
(`PAYOUT = {1:525, 2:225, 3:150, 4:85, 5:25, 6:25}` — `code_league_sim.py` line 12):

| rule | mean pts | P(1st) | P(top 6) | **E[payout]** |
|---|---|---|---|---|
| static VBD + caps | 1428.95 | 0.1475 | 0.710 | **$144.96** |
| **rollout (current engine)** | 1441.92 | 0.1775 | 0.725 | **$160.15** |
| rollout + upside tilt L=1.0 | 1427.57 | 0.1425 | 0.678 | $138.24 |
| rollout + LATE tilt L=1.5 (rd9+) | 1442.73 | 0.1850 | 0.725 | $162.10 |

**Rollout is worth +$15.19 of expected payout over static VBD + caps** — about 10% on a ~$145
baseline, against a $1,200 pool. **Not nothing, and not the rounding error the §4.13 "spread is
zero" line implies.** So §4.10 does clear the "is it worth auditing" bar.

**Two corollaries that fall straight out of the same table:**
- The **global upside tilt costs −$21.91** ($138.24 vs $160.15). This independently reproduces
  §4.13's stated "$22–41". ✓
- The **round-9+ tilt is worth +$1.95** ($162.10 vs $160.15). §4.13 calls it "free but not
  statistically resolved." **$1.95 is the measurement behind that phrase** — it should be quoted,
  because "free option" reads stronger than two dollars.

**What is NOT established:** the file carries no confidence interval. Read unpaired, P(1st)
0.1775 vs 0.1475 on ~400 sims is ≈1.6 standard errors — **not resolved at 95%**. If the design is
paired the SE is smaller, but the file does not say. **Do not quote +$15.19 as significant.**

---

## 2. THE DISCREPANCY — the directive's headline number is in no file I can find

Directive §4.10 states **rollout +8.6 [+6.5, +10.8]**. Three sources give three answers for what
is described as the same comparison:

| source | rollout vs static VBD + caps |
|---|---|
| **Directive §4.10** | **+8.6 [+6.5, +10.8]** |
| `ruletest_summary_n300.csv` (`vs_R2` column) | **+4.23 [+2.89, +5.58]** |
| `risk_summary_w22.csv` (mean_pts difference) | **+12.97** |

**The other four rows of §4.10's table reproduce exactly**, which is what makes the fifth
suspicious:

| rule | directive | `ruletest_summary_n300.csv` |
|---|---|---|
| Need-penalty | −5.7 | −5.677 ✓ |
| Static VBD, no caps | −8.7 | −8.648 ✓ |
| VONA | −8.8 | −8.781 ✓ |
| Follow ADP | −24.5 | −24.453 ✓ |
| **Rollout** | **+8.6** | **+4.23 ✗** |

Four of five match to two decimals. **Only the headline — the number that justifies shipping the
rollout engine — does not.** Note also that `|−8.648|` is numerically close to `+8.6`, and sits
directly beneath the rollout row in the same table.

**I have NOT established that this is a transcription error.** The two files use different sim
configurations (`risk_summary_w22` runs `OPP_WINDOW=22`; the n300 run may differ), so a legitimate
third number may exist in doc 54 that I did not read. **What is established: the directive quotes
one figure as THE figure, and the shipped results file beside it says something else.**

---

## 3. WHAT THIS CHANGES

1. **§4.10 survives the "does it matter" test.** +$15.19 is worth an audit. Do not skip it.
2. **The audit's first question changed.** It is no longer "is the simulator biased" — it is
   **"which of +8.6, +4.23 and +12.97 is real, and where did +8.6 come from?"** That is a
   ten-minute check against doc 54, not a simulator rebuild.
3. **§4.13's round-9 tilt should carry its dollar figure (+$1.95)** wherever it is described as a
   free option.
4. **Nothing here touches draft night.** The engine ships either way; only the size of its claimed
   edge is in question.

**Assumptions.** (a) `risk_summary_w22.csv` and `ruletest_summary_n300.csv` describe the same
rule pair — they may not, and that alone could explain the gap. (b) `E_payout` in the risk summary
uses the §2 table — confirmed against `code_league_sim.py` line 12. (c) ~400 sims behind the risk
summary; the file does not state N, so the significance arithmetic above is indicative only.
**Most valuable missing input: doc 54's N and CI for the rollout row.**
