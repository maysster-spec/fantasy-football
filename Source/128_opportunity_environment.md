# 128 — "Opportunity environment": measured, and it is the small half

*2026-09-01. Answers Matt's question: players entering an environment with more expected
targets — 2-WR sets, faster pace, no-huddle, better coaching; and the RB version, RPO,
dump-offs, pass-catching role. Should it be a flag? Should Gemini research it?*

**Verdict up front: the team-environment half is real and worth about +2 points a season
with perfect foresight. The role half is worth 12× more and is already flagged. Do not
build the environment flag. Retarget the research at the role.**

---

## 0. What was measured, and against what

Sources: ESPN preseason projection pulls for 2022 and 2024 (`raw_stats` / `raw_actual_stats`,
stat id `0` = pass attempts, `58` = targets, `53` = receptions — all verified against nflverse,
r = 1.000, mean absolute difference 0.0 on 292 matched 2024 receivers), plus nflverse weekly
regular-season logs 2022–2025.

**The 2023 projection pull is unusable for this** — only 5 of 103 QB rows carry non-zero
projected pass attempts. Dropped. That leaves two seasons of ESPN projections, and it is the
binding limit on everything below.

---

## 1. Where does a receiver's target count actually come from?  `[TESTED, n=221]`

Clean decomposition, nflverse only, no ESPN proxy. Year-over-year change in a WR/TE's targets,
split into *his team threw more* and *he took a bigger slice*. Population: WR/TE with ≥50
targets and ≥12 games in **both** years, three transitions (2022→23, 23→24, 24→25).

| component | variance | share of total | sd |
|---|---|---|---|
| Var(log target change) | 0.1601 | 100% | **40.0%** |
| **team pass volume** | 0.0119 | **7.5%** | 10.9% |
| **his own target share** | 0.1495 | **93.4%** | 38.7% |
| 2·cov | −0.0014 | −0.9% | — |

corr(team volume change, his target change) = **+0.257**.
corr(his share change, his target change) = **+0.962**.

Same test on RBs (n=113, ≥100 touches and ≥12 games both years): **team volume 5.7%, his own
share 95.9%**, corr(share, target change) **+0.971**.

And the role half is partly *knowable*: RB usage is sticky year over year — **targets per game
r = +0.620, carries per game r = +0.633** on the same 113 pairs. So the big term is not only
big, it is the forecastable one.

**A team's passing volume moves ±11% a year. A player's slice of it moves ±39%.** The
environment is the small term in the product, on both sides of the ball.

## 2. Upper bound: what if you called the environment perfectly?  `[TESTED, n=228]`

Regress a player's fantasy-point beat (actual − ESPN projection) on his team's pass-volume
**surprise** (actual team attempts − ESPN's projection). This is an oracle: it uses the
realised change, not a forecast, so it is a ceiling on any research that tries to forecast it.

| population | n | r | p | effect per **+50** team pass attempts | sd of player beat |
|---|---|---|---|---|---|
| WR/TE | 239 | +0.112 | 0.084 | **+2.1 pts** [−0.3, +4.4] | 47 |
| WR only | 177 | +0.166 | 0.027 | **+3.3 pts** [+0.4, +6.2] | 48 |
| TE only | 62 | −0.060 | 0.645 | −0.9 pts [−4.6, +2.9] | 42 |
| **RB** | 86 | **−0.228** | **0.035** | **−5.4 pts** [−10.3, −0.5] | 60 |

+50 attempts is a **large** environment change — about +9%, the size of a genuine coordinator
or QB change. Perfect foreknowledge of it buys a WR about **two to three points over a
fourteen-week season**, roughly 0.2 points a week, against a 47-point spread in outcomes.

**The RB row points the opposite way from the premise.** More team passing was *worse* for RB
fantasy points, significantly so. Mechanically this is game script and the attempt substitution
— a team that throws more runs less — and it says the "dump-offs and RPO lift the back"
intuition does not survive contact with the team-volume version of the measurement. n=86, one
sample, so treat it as a warning against the premise rather than a finding to act on.

## 3. Nobody forecasts team pass volume — including ESPN  `[TESTED, n=62 team-seasons]`

ESPN's starter-QB projected attempts vs actual team attempts: **r = +0.231** pooled;
**+0.345** in 2022, **−0.035** in 2024. Summing all a team's QBs instead of the starter:
+0.348 / −0.024. Negative control — last year's actual team attempts as the forecast for 2024:
**r = +0.315**, which beats ESPN.

So the dimension genuinely is *unpriced*. It is unpriced because it is close to unforecastable,
not because the market is asleep. `ERROR_PATTERNS` A8's lesson applies: unpriced and predictive
are different claims.

## 4. The one concrete artifact: vacated target share — and it fails its test

Computed for all 32 teams: 2025 targets whose owner is not on that team's 2026 roster.
League median **28.9%**, sd 13.5.

Highest: **MIA 56.4% · WAS 52.5% · PIT 46.3% · GB 37.8% · NE 37.4% · PHI 37.2% · NO 35.6% ·
NYG 35.0%.**  Lowest: **LA 0.0% · DEN 0.7% · CIN 7.1% · DAL 7.2% · SEA 9.3%.**

**IDENTITY-RULE NOTE (§3).** The first build of this table name-joined nflverse to the ESPN
board and reported **8 false departures out of 15** players with ≥35 targets — Kyle Pitts Sr.,
Michael Pittman Jr., Travis Etienne Jr., Aaron Jones Sr., David Sills V, Tre' Harris, Oronde
Gadsden, Joshua Palmer. It inflated ATL from 31.9% to 54.6% and LAC to 50.5%. Suffix- and
nickname-normalised join fixes it; **8 players remain unmatched to any 2026 team** and the
shipped script prints them every run for eyeballing — Marquise Brown, Ertz, Jayden Higgins,
JuJu Smith-Schuster, Cedric Tillman, Hopkins, Lockett, Jerome Ford. **Exactly the defect §3
warns about, caught by auditing the join instead of trusting a clean-looking output.**

**THE TEST — does it predict?** 2024 only (the one season with a usable prior-year target base
and an ESPN projection). Returning WR/TE/RB with ≥40 projected points, n=138 on 32 teams:

| level | n | r | p | effect per +10% vacated |
|---|---|---|---|---|
| player-level | 138 players | +0.040 | 0.64 | +1.38 pts |
| **team-clustered** | **32 teams** | **+0.125** | **0.50** | **+1.84 pts [−3.38, +7.05]** |

**Not resolved, not shippable.** Vacated share is a team constant, so the honest n is 32, not
138 — the identical correction that killed PROE in `ERROR_PATTERNS` A5 (ΔOOS R² = +0.00206,
CI [−0.00200, +0.00559]). One season cannot resolve an effect this size. `[HYPOTHESIS]`

## 5. Two independent measurements now say the same thing

§4.20 measured the team RB "pie" — sum of a team's top three RB projections — at **IQR 317–355,
±6% across 32 teams**, and concluded there is no big-vs-small backfield axis, only uncertainty
about *who holds the job*. This doc measures the passing side and gets **sd of ESPN's 2026
team-volume repricing = 7.4%**, and team volume at 7.5% of target variance.

**Rushing side and passing side, measured separately, agree: the team environment barely varies;
the job does.** That is the same conclusion §4.20 reached from the other direction, and it is
why `depth_map.py`'s UNSETTLED / contested / LEAD BACK plus `job worth` is already the flag Matt
is asking for — it just isn't named after the environment.

## 6. What ESPN has already repriced for 2026 (descriptive; no edge in it)

Projected 2026 team pass attempts, all QBs, vs 2025 actual. **sd of the change: 38 attempts,
7.4%.**

More: **MIN +92 (+19%) · WAS +73 (+16%) · BAL +64 (+15%) · GB +62 (+13%) · NYJ +58 · LV +54.**
Less: **DAL −49 · ARI −44 · CIN −43 · DEN −26 · CHI −24 · NO −23.**

These are *inside* the projection and therefore inside VBD. A player on a team ESPN has already
moved up carries no edge from that move. The only exploitable version is a discrete, dated
change the 08-30 pull did not absorb — which is a news question, not a modelling one, and is
what the Sept 5 refresh already covers.

## 7. Decision

1. **No environment flag.** Measured ceiling +2 points with perfect foresight, against QB2 at
   +5 to +11 (§4.17b) and the RB dart's keeper option at +8 (§4.18). It would add a column to
   the board that cannot move a pick.
2. **The flag already exists** and is pointed at the 93% half: `depth_map.py`'s UNSETTLED /
   `job worth`, §4.20.
3. **Retarget the Gemini task** from "which offenses will throw more" to "who wins the specific
   open job" on the teams where a job is actually open. The vacated table in §4 is a *targeting
   list* for that research even though it fails as a predictor — it says where to look, not what
   to conclude.

## Assumptions, and what would break them

1. **Two seasons of usable ESPN projections.** 2023's pull is empty and 2021/2025 were never
   pulled. Everything in §2 and §4 rests on 2022 and 2024. A third season could move the oracle
   bound, though it would have to move a long way to matter.
2. **Team pass attempts stands in for "opportunity environment."** Pace, no-huddle rate and
   personnel groupings are not measured here — they are correlated with volume but not identical
   to it. A separate channel could carry more than 7.5%; nothing in this project can test that,
   and PROE, the one such variable that *was* tested, failed (A5).
3. **The RB negative result is game script, not a law.** n=83, one direction, one sample.

**Most valuable missing input:** a preseason ESPN projection pull for 2023 and 2025. Two more
seasons would take the oracle test from n=228 to ~450 and the vacated test from 32 teams to ~96
— enough to resolve §4 either way.


---

## 8. Reproducing it

`Scripts\env_study.py` — every number above, one command.

```
py env_study.py                 rerun all five sections
py env_study.py --vacated       just the 2026 vacated-target table + join audit
py env_study.py --team-volume   just ESPN's 2026 repricing vs 2025 actual
```

It needs nflverse weekly player stats for 2022–2025 in `Source\nfl\w<year>.csv`
(`stats_player_week_<year>.csv` from the nflverse-data `player_stats` release, renamed).
It writes `Source\vacated_targets_2026.csv` and nothing else. Run end to end on 2026-09-01;
the output in this doc is that run.
