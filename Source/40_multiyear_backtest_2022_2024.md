# 40 — THE 2022/2024 FALSIFIER RAN. THE VALUE RULE DID NOT SURVIVE IT.
**Aug 25, 2026.** Reproduce with `code_backtest_multiyear.py` on `espn_projections_{2022,2024}_20260824.csv`
and `draft_history_2021_2025.csv`.

> **CORRECTION, same day, after inspecting the raw ESPN payloads.** The first version of this
> doc guessed that the broken `proj_2023` column was "likely the same class of
> season/statSourceId mismatch as the actuals bug" and therefore fixable by re-running the
> pull. **That guess was wrong and is withdrawn.** The parser is correct; ESPN does not serve
> 2023 preseason projections. Proof and full diagnosis in the next section and in
> `GEMINI_FIX_BRIEF_espn_pull.md`. Everything else in this doc is unchanged — the backtest
> never used 2023.

> **SUPERSEDED IN PART BY `claude/41_redteam_of_doc40.md` (Aug 25, red team on Opus).**
> The headline below — "the rule beat only 2 of 24 manager-seasons" — **does not survive.**
> The greedy policy used here drafts kickers and defenses at median pick 75, five rounds earlier
> than the league ever does and in direct violation of §4.8. Correcting only that recovers
> **+105.6 points per manager-season**, moves the count to 8 of 24, and flips Lobsinger 2022 from
> −242.0 to **+11.9**. Pooled with 2025 on identical code the rule beats **18 of 36** with a
> bootstrap 95% CI of **[−89.5, +62.3] — including zero**. Read doc 41 before quoting any number
> on this page. The 2023 quarantine and the pick-by-pick sections below remain valid.

## THE ANSWER, IN ONE LINE

Doc 21's own pre-registered falsifier was: *"re-run the manager-level backtest on 2022, 2023 and 2024. If the
rule beats Lobsinger and Taylor in two of those three years, this is 2025 noise and I withdraw it."* **2023 cannot be run
at all (ESPN-side data gap, below) — only 2022 and 2024 could. In both, the rule loses to Lobsinger AND
Taylor. It also loses to almost everyone else: 2 of 24 manager-seasons total.** That is a much more severe and
different failure than 2025's (beat 9 of 12, lost only to the top 3). The floor-raiser hypothesis does not
survive intact, but neither is it cleanly refuted — see "what this does and doesn't mean" below.

---

## 2023 IS QUARANTINED — AND IT IS NOT RECOVERABLE BY FIXING THE SCRIPT

**[TESTED, against `espn_raw_2023_20260824.json` directly, not against the CSV.]**

`proj_2023` is `0.0` for **575 of 700** rows, including the entire top of the board —
McCaffrey (ADP 2.07), Tyreek Hill (2.89), Chase, Kelce, Ekeler, Hurts. The cause is now
established and it is **ESPN-side, not a defect in the pull script**:

1. **Every player has exactly one 2023 season-projection row** (`seasonId=2023, statSourceId=1,
   statSplitTypeId=0`): 699 of 700 have exactly one, none have more. So the parser never faced
   an ambiguous choice and there is no richer row it failed to find.
2. **Those rows are empty.** 435 contain a single stat key — `"210"`, games played, e.g.
   `{"210": 14.17647059}`. 140 contain zero keys. Only 124 contain a real projection.
   Stat 210 is not a scoring stat, so `appliedTotal` is legitimately `0.0`.
3. **Complete stat list ESPN returns for McCaffrey in the 2023 payload:**
   `002023` actual, 50 keys, 357.8 (good) · `102023` projection, **1 key, 0.0** ·
   two weekly `statSplitTypeId=1` rows. That is all of it.
4. **It reproduces across two independent network calls.** 2023 is fetched twice by this
   pipeline — as its own season, and as the prior season inside the 2024 run. Both return
   empty projections. **2022 is also fetched twice and returns good projections both times.**

| season | as own-year | as prior-year |
|---|---|---|
| 2022 | 539 real | 468 real |
| **2023** | **124 real** | **91 real** |
| 2024 | 530 real | — |

Same code, same filter, same session — so this is not data decay with age (2022 is older and
works) and not a code-path difference. **BASELINE:** the raw JSON payload's own stat entries.
**POPULATION:** all 700 rows of `espn_raw_2023_20260824.json`. **SAMPLE:** n=700, 699 projection
rows examined.

**What is still good in the 2023 file, and should not be discarded:** `actual_2023` (verified —
Josh Allen 448.8, McCaffrey 357.8, Hurts 401.5), `espn_adp` (a genuine 2023 board — McCaffrey
2.07, Hill 2.89, Pollard 8.74; 224 uncensored), `rank_std` / `rank_ppr` (ESPN preseason draft
ranks, 700 populated), `pct_owned`. **Only `proj_2023` is quarantined.**

**Checked and rejected as a substitute source:** `FantasyPros_Draft_Accuracy_2023.csv` is an
analyst leaderboard (246 rows of expert-vs-position accuracy ranks), not player-level
projections. It cannot fill this column.

**Consequence for the 3-year test:** a VBD-based rule cannot be run on 2023 without projected
points. A **rank-based** variant could be, using the intact `rank_std`/`espn_adp` — but that is
a *different rule* (what looks valuable vs what is valuable, directive §0), and its results are
not poolable with the 2022/2024 VBD numbers without saying so. Offered as an option, not done.

---

## THE 2022/2024 RESULT

Same methodology as doc 21's RT3 (`code_backtest_redteam.py`): each manager's real keeper is held constant,
each manager's "rule" roster is built greedily by max-VBD-subject-to-roster-need against the **ground-truth
availability pool** (every player actually taken later in that year's real draft — no modelled survival,
so this isolates the value rule itself). Scoring: season-total optimal starting lineup, 1QB 2RB 2WR 1TE 1FLEX
1D/ST 1K. **POPULATION:** all 12 managers, true (non-keeper) picks, 2022 and 2024. **SAMPLE:** n=24
manager-seasons (12 × 2 years).

| | mean delta (rule − actual) | sd | rule beat actual |
|---|---|---|---|
| **2022** | −233.5 | 175.7 | 1 of 12 |
| **2024** | −208.8 | 189.6 | 1 of 12 |
| **combined** | **−221.1** | **179.2** | **2 of 24** |
| *2025 (doc 21, for contrast)* | *+43.1* | *~150* | *9 of 12* |

**Lobsinger and R Taylor specifically** (doc 21's named falsifier targets, the opponent model's top-rated
managers): rule lost to both, in both years.

| year | manager | actual | rule | delta |
|---|---|---|---|---|
| 2022 | Lobsinger | 1702.7 | 1460.7 | −242.0 |
| 2022 | R Taylor | 1735.4 | 1481.5 | −253.9 |
| 2024 | Lobsinger | 1938.7 | 1479.4 | **−459.3** |
| 2024 | R Taylor | 1720.8 | 1603.9 | −116.9 |

The only two manager-seasons where the rule won: **Fleming 2022 (+42.7)** — the opponent model's *weakest*
manager — and **Rychlicki 2024 (+207.3)** — rated "trending up," not elite. The rule did not selectively lose
to strong managers and beat weak ones; it lost broadly, weak and strong alike.

Variance comparison (the other half of the 2025 "floor-raiser" story) does **not** replicate cleanly either:
2022 has the rule *more* variable than actual (sd 136.0 vs 104.1) — opposite of 2025's low-variance property.
2024 has it lower (sd 78.9 vs 167.5) — consistent with 2025. Mixed, n=2, not a stable pattern either way.

Full table: `backtest_2022_2024_all_managers.csv`.

---

## WHY, PICK BY PICK (RT2-STYLE CONCENTRATION CHECK, MATT'S OWN ROSTER)

**2024, Matt Mays: actual 1972.3, rule 1514.2, delta −458.1.** Rule benefited from two picks Matt could not
have known would bust (Jonathon Brooks 6.0 actual, Ty Chandler 25.4 actual — rule got Montgomery/Conner
instead, +199.6 and +204.9 favoring rule) but lost far more to breakouts nobody's preseason number saw coming:
**Jayden Daniels** (`proj 286.1` → `actual 404.3`, rule took Brian Robinson Jr. instead, **−254.5**), **Drake
London** (rule got a Pacheco bust, −179.9), **Terry McLaurin** (rule got a stale D/ST, −166.8), **Ja'Marr
Chase** at 9 (rule took Jonathan Taylor, a defensible value call given `proj`, −103.8). Raw pick-level sum is
only −100.4 — the −458.1 lineup number comes from how those specific swaps land relative to starting thresholds,
not from one dominant outlier the way 2025's three injuries were. **This is a different mechanism than 2025,
not a mirror of it**: 2025's edge was concentrated in three unforeseeable injuries; 2024's Matt-specific loss is
concentrated in unforeseeable **breakouts**, spread across four picks rather than three.

**2022, Matt Mays: actual 1683.8, rule 1601.9, delta −81.9.** Smaller and more balanced: rule gained from Josh
Allen at 18 (+144.8) and Aaron Rodgers's still-solid 2022 at 66 (+243.8), lost from A.J. Brown outperforming a
Dobbins bust at 42 (−177.9). Top-3-by-magnitude picks account for essentially all of the raw delta here too
(104% — the rest nets to ~zero), same concentration pattern doc 21's RT2 found in 2025.

---

## WHAT THIS DOES AND DOESN'T MEAN

**Does not mean:** "the value rule is bad and should be abandoned." Every year examined (2025, 2022, 2024) shows
the result dominated by 3-4 picks whose outcomes a preseason projection structurally cannot see — injuries in
2025, breakouts in 2024, a mix in 2022. That is a property of one-season variance at n=12-14 picks, not
necessarily a property of the rule's decision logic.

**Does mean, at minimum:** the specific 2025 claim *"the rule loses only to the best managers while beating
everyone else, because it's a floor-raiser"* does not generalize. In 2022 and 2024 it lost broadly, including
to below-median managers, and its variance was not reliably lower than real outcomes. Whatever the rule is
doing, "quietly buys a safe floor" is not a description that holds across three years.

**Still true and unchanged by this:** doc 21's RT4 power calculation — smallest detectable per-pick effect at
14 paired picks and this outcome variance is roughly ±67-90 points. **n=2 additional years is still
underpowered for a general verdict**, per A1 discipline. Direction (rule loses) is now consistent across 2/2
testable years plus mixed-but-net-positive in 2025's own year, but "consistent in 2 of 2" is not the "2 of 3"
the falsifier was designed around — 2023 never got to vote, and now cannot on a VBD basis.

**What would most improve this, revised:** the 3-year VBD test is **blocked, not pending** — ESPN
does not hold the input. The realistic upgrades, in order:
1. **Add 2021 and 2025 to the VBD test.** 2025 already ran in doc 21 under slightly different
   framing; re-running it inside `code_backtest_multiyear.py` would make 2022/2024/2025 directly
   comparable on identical code — three years, same estimator. 2021 needs a 2021 pull, which by
   the evidence above may or may not carry projections; one probe answers it.
2. **Run a rank-based variant across all available years including 2023**, clearly labelled as a
   different rule, to see whether the "rule loses broadly" result is specific to VBD or general to
   greedy best-available drafting.
3. Weekly rather than season-total scoring, which is the actual objective function.

---

## LIMITS — same four as doc 21, plus one new one

1. Season totals, not weekly. No bye or injury-week granularity, no weekly lineup optimum — same as doc 21.
2. `NEED` is the same simplified greedy policy as doc 21, not `draft_sim_2026.py`.
3. Each manager's rule-roster is simulated independently against real go-forward availability; it does not
   model 12 rule-drafters competing for the same players in the same simulated draft. Same simplification as
   doc 21 — carried forward, not introduced here.
4. 2022 and 2024 draft histories are each 178 picks, not 180 (H1, already logged) — Wilson Kam is short 2 picks
   in both years, which affects his row's totals for both policies roughly proportionally.
5. **New:** join rate 175/178 (2022) and 176/178 (2024) — small numbers of un-matched historical names (Cam
   Akers, DJ Moore, Gabe Davis in 2022; Chig Okonkwo, DJ Moore in 2024) despite the alias table. Not large
   enough to plausibly flip the direction of the headline result, but noted per C1 join discipline.
6. **New:** the pull script writes `0.0` rather than null when ESPN returns an empty projection row.
   In 2022 and 2024 this affects 151 and 157 rows, but they sit at median ADP 169.9 and only 3 and 7
   fall inside ADP 170 — so the 2022/2024 results are not materially exposed to it. Full defect list
   in `GEMINI_FIX_BRIEF_espn_pull.md`.
