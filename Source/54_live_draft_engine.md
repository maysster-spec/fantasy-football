# 54 — WHICH PICK RULE ACTUALLY WINS, AND THE LIVE ENGINE THAT RUNS IT
**Aug 26, 2026.** Matt asked what design applies VOR correctly in a live draft, and whether a
"positional penalty" is needed to stop droughts. Eight candidate rules were raced head-to-head
in a paired simulation rather than argued about. Three of them — including my own proposal and
the published dynamic-VBD method — **lost**.

---

## THE ANSWER, IN ONE LINE

**The board is worth six times more than the pick rule.** Going from following ADP to using
this project's VBD board is **+24.5 points**; going from the simplest sensible VBD rule to the
best rule tested is **+5.6**. Only one rule beat plain constrained VBD: a **Monte-Carlo rollout**.
**No positional penalty is required, and adding one costs 5.7 points.**

---

## PART A — THE TEST

**Objective:** expected starting-lineup points, weeks 1–14, bye- and injury-adjusted (directive
§0). Not roster VBD. **Paired design:** every rule faces the identical opponent-noise draw and
the identical weekly availability draws, so differences are attributable to the rule alone.

**Opponent model:** `eff_pick + N(0, 0.30 × eff_pick)` (doc 53), TE +15, Snyder takes Josh Allen
at q=0.85, roster-legality caps per team. **Board:** `board_v7_2026`, keeper-depleted.
**Me:** slot 8, 12 skill selections at 8…137; D/ST 152 and K 161 excluded from scoring (§4.8).
**Lineup:** 1QB/2RB/2WR/1TE/1FLEX, weeks 1–14, unfillable slots take a waiver-level fill at 80%
of positional replacement. **Availability:** each player each week at p=14.46/17 (doc 42), with
per-game points computed off ESPN's own 15.32-game projection so the discount is not double-counted.

**N = 300 paired simulations.** Reproduce with `code_ruletest_*.py`.

> **RE-VERIFIED, Aug 26 (doc 55 §B1).** The opponent noise model used here over-dispersed picks
> beyond ~84 by 40–70%. Re-run under the corrected `sd = 0.30 × min(ADP, 70)`, N=200, the rollout's
> edge **grows**: R6 **+8.1** [+6.1, +10.2] and R6b **+9.6** [+7.5, +11.6] over static VBD, versus
> +4.2 and +5.6 before. Every conclusion in this document holds, with larger effects.

### Results

| rule | mean | p90 | vs baseline | 95% CI | wins | QB | RB | WR | TE |
|---|---|---|---|---|---|---|---|---|---|
| **R6 rollout** | **1500.2** | 1519.2 | **+4.2** | **[+2.9, +5.6]** | **64%** | 2.00 | 5.92 | 4.08 | 2.00 |
| R2 static VBD + roster caps | 1495.9 | 1517.8 | — (baseline) | — | — | 1.97 | 5.96 | 4.07 | 2.00 |
| R4 need-penalty heuristic | 1490.3 | 1511.8 | **−5.7** | [−7.6, −3.7] | 38% | 1.94 | 5.79 | 4.26 | 2.00 |
| R1 static VBD, no caps | 1487.3 | 1513.6 | **−8.7** | [−10.0, −7.4] | 19% | 2.50 | 6.08 | **1.46** | 3.95 |
| R3 VONA (1-step lookahead) | 1487.2 | 1513.9 | **−8.8** | [−11.0, −6.7] | 30% | 2.00 | 5.69 | 4.72 | 1.59 |
| R0 follow ADP | 1471.5 | 1504.5 | **−24.5** | [−27.4, −21.5] | 17% | 1.82 | 4.86 | 5.60 | 1.72 |
| R5 marginal starter (myopic) | 1411.9 | 1432.7 | **−84.0** | [−86.2, −81.7] | 0% | 2.00 | 5.97 | 4.03 | 2.00 |

Separate run, N=200, same seeds: **R7 (my proposal) −3.6, CI [−5.5, −1.8]** — see A5.
**R6b (deeper rollout: 9 candidates × 10 inner sims) +5.6, CI [+4.1, +7.2]**, and beats the
standard rollout by **+1.5, CI [+0.6, +2.5]**. Depth helps, with diminishing returns.

### A1. The drought is real, and roster caps alone fix it

Matt's worry was correct and it is now measured. **Unconstrained VBD drafts 1.46 WRs** — it
chases the flat top of the TE and QB curves and starts a replacement-level WR2 all season. That
costs **8.7 points**. But the fix is not clever: a hard cap (max 2 QB, 2 TE, 6 RB, 6 WR, and
force QB/TE before the picks run out) recovers all of it. **No dynamic logic needed.**

### A2. VONA — the standard published dynamic-VBD method — LOSES

VONA is the method every fantasy site describes (FantasyPros defines it in their own glossary):
value a player against the best player at his position expected to survive to your next pick.
**Tested here it is 8.8 points worse than plain constrained VBD**, essentially tied with having
no constraints at all.

**Mechanism, from the roster mix:** VONA drafts **4.72 WR and 1.59 TE**. It over-buys positions
with flat value curves, because a flat curve means "the next one is nearly as good" fails to
fire, while a position whose top is steep gets bought early and repeatedly. VONA measures the
*board*, not your *lineup* — it has no idea that your third WR only plays at FLEX. This is
exactly the weakness FantasyPros' own documentation lists ("does not account for team roster
gaps") and it turns out to be fatal, not cosmetic.

### A3. THE HAND-SET POSITIONAL PENALTY LOSES — do not build it

The Gemini blueprint's step 4 asks for a penalty that shrinks a position's VOR once its starter
slots are full. Implemented faithfully (×1.0 → ×0.5 → ×0.25), **it costs 5.7 points, CI
[−7.6, −3.7]**.

It is also another hand-set constant of the exact class this project keeps getting burned by
(`ERROR_PATTERNS` D6/A11). **The correct answer to "how much is a third RB worth?" is not a
tuned multiplier — it is the actual lineup arithmetic**, and the rollout computes it.

### A4. Myopic lineup-marginal drafting is a disaster — this is why replacement level exists

R5 picks whichever player most raises the starting lineup *right now*. With an empty roster that
is a quarterback, so it opens **Josh Allen, then Lamar Jackson**, and finishes **84 points**
behind. Every slot looks equally empty at pick 8. Replacement level is precisely the correction
for this, and removing it is catastrophic. **VBD is not optional.**

### A5. MY OWN PROPOSAL ALSO LOST — reported, not buried

I designed **R7: VONA measured in marginal lineup points instead of raw projection** — VONA's
baseline with R5's lineup awareness, which on paper fixes both of their failure modes and needs
no tuned constant. It was the rule I intended to recommend.

**[TESTED] R7 = −3.6 vs plain constrained VBD, CI [−5.5, −1.8], N=300.** It loses.

**Mechanism:** R7 opens WR 33% of the time and WR-WR 14%, against RB-RB-RB 65% for the rules
that win. The one-step baseline is evaluated against the *current* roster, so at an empty roster
the two WR slots make WR look urgent; by the time the error shows, the round-2/3 RBs are gone.
**Directive §4.10's robust finding — RB in rounds 2 and 3 — is what R7 violates.**

### A6. AN INDEPENDENT REPLICATION OF §4.10

Not sought, but worth recording. §4.10 established on a paired sim (N=300) that "the robust
finding is RB in rounds 2 and 3." This simulator is a different implementation with a different
objective function, a different opponent noise level (0.30, not 0.135) and a different lineup
model — and the two winning rules open **RB-RB-RB in 64–65% of drafts and RB in round 2 or 3 in
essentially all of them.** `[TESTED]` §4.10 replicates.

---

## PART B — CAN FANTASYPROS DO THIS? NO, AND HERE IS THE EXACT REASON

Matt asked whether his own VBD values can drive the FantasyPros Draft Assistant. **They cannot.**
FantasyPros' own support documentation states it directly: *"it is not currently possible to
import projections into our tools."* The only import path is a **ranked list** — an ordering,
with the magnitudes discarded.

That is the whole problem. A rank list can express **R2 and nothing above it**, because every
rule that beat R2 needs cardinal values:

| capability | needs | FantasyPros can express it? |
|---|---|---|
| draft down a fixed list | rank | **yes** |
| know a gap of 40 points from a gap of 2 | values | no |
| price a 3rd RB as a FLEX rather than a starter | values + lineup | no |
| trade off "QB now" against "WR later" | values + survival | no |
| the rollout | values + survival + lineup | no |

**And R2 is a static rule** — a rank list cannot re-order itself as the draft develops, which is
the entire thing Matt asked for. The Draft Assistant will still show its own value math on top;
that math runs on *their* projections, not this league's 6-point-passing-TD scoring.

**Verdict: FantasyPros is a good tool for someone without a model. Matt has a model, and
FantasyPros has no input port for it.** Sync is also Chrome-extension-only and desktop-only.

---

## PART C — THE ENGINE THAT SHIPS

### C1. The rule

For each legal candidate *p*, with my remaining picks *t₁…tₙ*:

```
ROLL(p) = E [ lineup value of my FINAL roster | I take p now,
              then draft greedily by marginal lineup value at t₁…tₙ,
              against a fresh draw of the opponent model ]

pick    = argmax ROLL(p)
```

The expectation is taken over **M independent realisations of the opponent model**
(`pref = eff_pick + N(0, 0.30·eff_pick)`, TE +15). Legality is enforced inside the rollout, so
"must still take a QB and a TE" is priced rather than bolted on.

**Everything Gemini's blueprint asks for falls out of this and none of it is hand-set:**

- *Positional penalty when starters are full* — a third RB simply adds less lineup value, because
  he only reaches the FLEX. **Derived, not tuned.**
- *Availability probability matrix* — the same noise draw produces `p(survive to my next pick)`.
- *Marginal drop-off between position X now and Y now* — the difference in `ROLL`.
- *Bye collisions* — the lineup is scored week by week, so stacking byes lowers `ROLL` directly.

### C2. The two numbers displayed for every candidate

`ROLL` is the decision but it is not readable. Each row also carries the VONA-style decomposition,
which is what makes the recommendation explainable in ten seconds:

```
adds now   MV(p)   = lineup points p adds to my roster today
if I wait  HOLD(p) = expected lineup points from the best player at p's position
                     that survives to my next pick
Δ          MV − HOLD
cost       ROLL(p) − ROLL(best)   -- 0 for the recommendation; how much any
                                     override actually costs, in points
```

**Worked example, pick 41, roster WR-WR-RB:**

| player | pos | adds now | if I wait | Δ | cost vs #1 |
|---|---|---|---|---|---|
| Trey McBride | TE | 66.0 | 40.0 | **+26.0** | **0** |
| Kyren Williams | RB | 68.7 | 46.3 | +22.4 | −3.9 |
| Davante Adams | WR | 19.7 | 8.0 | +11.7 | −21.3 |
| Joe Burrow | QB | **82.5** | **80.9** | +1.6 | −30.4 |

Burrow adds the most raw lineup value of anyone on the board — and is the fourth-best pick,
because a QB nearly as good is expected at 65. **That is exactly the trade Matt described**
("QB is fine as long as enough value is expected at the other positions later"), now with a
number on it. The `cost` column is the override price: taking Adams over McBride costs 21 points.

### C3. How it goes live — no clicking

`live_draft.py` polls ESPN's own draft feed on Matt's machine, using the cookies already working
in `Espn_pull_projections.py` and `espn_draft_injector_Gemini.py`:

```
GET https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2026
    /segments/0/leagues/21985?view=mDraftDetail
    -> draftDetail.picks[] : {overallPickNumber, teamId, playerId, roundId}
```

Every 3 seconds. On any change it re-runs the engine and rewrites `live_board.html`, which
carries a 3-second meta-refresh. **Nothing is clicked and nothing is typed all night.**

Players are matched by **ESPN player id**, not by name — `ESPN_prerank_with_ids.csv` already
carries the mapping for all 544 players, so the C1 name-collision class of defect
(`Travis Etienne` vs `Travis Etienne Jr.`) cannot occur on this path.

**Override is free and needs no interface.** Matt makes whatever pick he wants in the ESPN room;
the next poll sees it, and the engine re-plans the remaining picks around the roster he actually
has. The `cost` column tells him the price beforehand.

**It does not submit picks.** ESPN's write endpoint would allow it. It is not built, deliberately:
an irreversible action taken by software on a 60-second clock, on a night with $525 on the line,
has no acceptable failure mode. The existing prerank injection stays as the safety net — if Matt
times out, ESPN autodrafts his top remaining ranked player.

### C4. Verification done

- **Full-draft integration test**, 3 independent drafts × 168 picks, engine picking for JUG:
  no crash, exactly 14 selections, roster legal every time, no duplicate player.
- **Every render state** exercised — before the draft, on the clock at all 12 skill picks, the
  D/ST slot at 152, the K slot at 161, and after the final pick. All render.
- **Engine latency**: 3.6 s at 8 inner sims, 4.5 s at 10, 12.7 s at 24 — against a 60-second
  clock, and it recomputes during other managers' picks rather than on Matt's.
- **Dry run available**: `py live_draft.py --replay 2025` runs the whole thing against last
  year's finished draft in the same league. **Do this once before Sept 7** — it is the only
  check of the live feed that has not been run, because this session cannot reach ESPN.

---

## WHAT THIS CHANGES

1. **Build the board carefully; do not agonise over the rule.** +24.5 vs +5.6.
2. **Enforce roster caps.** It is the single biggest rule-side effect (8.7) and it needs no model.
3. **Do not implement the positional penalty** — it costs 5.7 points.
4. **Do not implement VONA** — it costs 8.8 points.
5. **Run the rollout, and treat its `cost` column as the price of any gut override.**
6. **FantasyPros is not the answer here** and no amount of configuration makes it one.

## LIMITS

1. **One board.** Every rule is scored against the same ESPN-derived projection. Doc 44 says that
   projection loses to these managers once injury luck is stripped. The ranking of rules is
   probably robust to that; their absolute values are not.
2. **The rollout's inner scorer ignores injuries** (byes only) while the objective includes them,
   which understates the value of depth *inside* the rollout. The +4.2 is therefore a lower bound
   on this design — which is the safe direction.
3. **Opponents are modelled as ADP+noise with roster caps.** Real managers run positional runs,
   react to each other, and reach for their own guys. §4.12's per-manager tendencies are not in
   this simulator.
4. **Season-total projections split evenly over games.** Real weekly variance would raise the
   value of depth and of high-floor players for every rule.
5. **N=300 paired sims, one draft slot, one season.** The CIs reflect only sampling error in the
   simulator, not model error in the board.
6. **The waiver-fill assumption (80% of positional replacement) is unswept.** A more generous
   waiver wire would shrink every gap; a harsher one would widen them.

## §7 CLOSE-OUT

**Top 3 assumptions:**
1. **Starting-lineup points weeks 1–14 is the right objective.** *Invalidated by:* first place
   being 44% of the pot — a rule that raises the ceiling could be worth more than one that raises
   the mean. R6's p90 edge (+1.4) is smaller than its mean edge (+4.2), which is weak evidence
   the rollout is a floor-raiser, not a ceiling-raiser. **Untested and open.**
2. **The opponent model transfers to draft night.** *Invalidated by:* the real draft's residuals
   against ADP. Measurable at the time, not before.
3. **ESPN serves `mDraftDetail` live during the draft, not only after it.** *Invalidated by:* the
   `--replay 2025` dry run failing, or the feed lagging the room. **This is the one load-bearing
   assumption that has not been tested, and it can only be tested from Matt's machine.**

**What would most improve this:** a **second projection source** on the board (unchanged from
doc 45 — it remains the largest gap), and weekly rather than season-total projections, which
would let the objective be computed rather than approximated.
