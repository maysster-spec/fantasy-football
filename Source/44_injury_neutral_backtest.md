# 44 — REMOVING INJURY LUCK SHARPENS THE VERDICT: THE RULE IS MEASURABLY WORSE
**Aug 25, 2026.** Matt: *"for a look back you know which players were injured and that should
probably inform you."* He was right. Reproduce: injury-neutral variant of `code_backtest_redteam_v2.py`.

## METHOD
For a backtest, games played (ESPN stat 210) is known after the fact. Using it to *pick* players
would be hindsight cheating. Using it to *decompose* the result is legitimate and is what doc 41's
"3–4 unforecastable picks dominate every year" claim actually needed.

Each player's actual points are converted to **points per game extrapolated to a full 17**, applied
symmetrically to both the manager's real roster and the rule's roster. That holds player quality
constant and strips out who happened to stay healthy. Players with fewer than 4 games are left at
their raw total (the per-game rate is unstable below that).

**POPULATION:** all 12 managers × 2021, 2022, 2024, keepers held constant, K/D-ST deadline pick 121.
**SAMPLE:** n=36 manager-seasons. 2023 excluded (no usable projections); 2025 excluded (the 2026
pull carries `actual_2025` but no per-game stat rows to compute availability from).

## RESULT

| year | as-played | injury-neutral |
|---|---|---|
| 2021 | **+102.3** | **+31.2** |
| 2022 | −55.4 | −47.3 |
| 2024 | −175.6 | −183.9 |
| **pooled (n=36)** | **−42.9** | **−66.6** |

| | 95% CI on mean delta | verdict |
|---|---|---|
| as-played | [−110.1, +19.9] | **includes zero** — no detectable difference |
| **injury-neutral** | **[−117.7, −16.5]** | **EXCLUDES zero** |

## WHAT THIS CHANGES

Doc 41 concluded "no measurable difference between the value rule and real managers." That was
correct **as played** — but it was correct for the wrong reason. Injury noise was wide enough to
swallow a real effect. **With that noise removed, the rule is significantly worse than these
twelve managers**, by roughly 67 points a season.

The change is driven mostly by **2021, where the rule's apparent +102.3 collapses to +31.2** —
i.e. in 2021 the rule's players stayed healthier than the managers' players, and that luck was
being read as skill. 2022 and 2024 barely move, so the effect is not uniform.

Between-year spread also narrows (139.4 → 108.9), consistent with injuries being a genuine noise
source rather than a systematic bias.

**Practical read: the greedy max-VBD rule is not a neutral baseline and should not be treated as
one.** Doc 41's headline should be read as superseded on this point.

## LIMITS
1. Extrapolating a partial season to 17 games assumes the per-game rate would have held. For a
   player who played 5 games at an elite rate this is generous, and the direction of that bias is
   not obviously symmetric between the rule and the managers.
2. **Survivorship:** staying healthy correlates with the traits that produce good seasons, so
   "injury-neutral" does not fully isolate selection skill.
3. n=36 across 3 seasons, one league. The CI excludes zero but is wide (−118 to −17).
4. Season totals, not weekly. A player lost in weeks 15–17 costs a title; this metric cannot see that.
