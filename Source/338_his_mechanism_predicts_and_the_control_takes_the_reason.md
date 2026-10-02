# 338 HIS MECHANISM PREDICTS, AND THE CONTROL TAKES THE REASON

**2026-09-17, overnight.** Matt, holding the Browns D/ST: *"the bucks def is expected to do well
against CLE because they suck. Then here i am putting out the defense that's expected to have the
worse offense of the week, lol. I don't like it and want out."* Then, an hour later, the positive
version: *"Bears may be a sneaky pick too if their offense continues to blow teams away those teams
get forced into more mistakes, turnovers, pick 6."*

**Two mechanisms, one variable, tested separately. The first predicts and loses its reason to a
control. The second is null and underpowered. Neither had ever been looked at here.**

---

## 1. WHAT NOTHING IN THIS PROJECT HAD MEASURED

Section 4.33 measures the OPPONENT: matchup swing at D/ST is 2.22 against a 2.06 spread between the
units, 108%, the only position where the schedule beats the player. Doc 212 adds the four-week
horizon. Doc 264 fixed the scoring scale. **Not one of them looks at the team the defence plays
FOR.** `Scripts\research\build_dst.py` builds `dst_week1_2026.csv` from opponent generosity alone.

## 2. TEST ONE, AND THE FORM WAS WRITTEN FIRST (section 0.5a2)

**CLAIM:** a defence whose own offence is bad scores worse.
**UNIT: team-season**, because both predictors are team-season constants (section 4.24c's
clustering trap, fourth occurrence).
**OUTCOME:** that D/ST's mean fantasy points per week, weeks 1 to 14, under section 2's bands, from
`dst_weekly_2021_2025.csv`.
**PREDICTORS, both preseason-knowable:** the team's prior-season points per game, and the mean
prior-season points per game of its weeks 1-14 opponents.
**POPULATION: 2022-2025, n=128 team-seasons, 1,580 team-weeks.** 2021 has no prior season on file.

| term | coefficient | se | t |
|---|---|---|---|
| **own offence, prior ppg** | **+0.0979** | 0.0450 | **+2.18** |
| opponent slate, prior ppg | −0.1419 | 0.1682 | −0.84 |

**rho(own offence, D/ST points per week) = +0.181, permutation p = 0.0367, n=128.** `[TESTED]`
**And in his own framing: a defence whose own offence was the worse of the two in that game scores
4.89 a week against 6.10 for the better one. A gap of 1.21 points, permutation p = 0.0007,
n=1,580.** Quartiles of own offence: 4.87 / 5.42 / 5.91 / 5.80.

**THE SEASON SLATE IS NULL AND THAT DOES NOT CONTRADICT SECTION 4.33.** Own offence varies by
4.08 points a game across teams; the 14-week opponent slate varies by 1.09. **Matchup is a WEEK
property and own offence is a SEASON property.** They are not competing, and a season-level test
cannot see a week-level effect.

## 3. THE CONTROL THAT TAKES THE MECHANISM AWAY

**Stated before running: a team with a good offence is usually a good TEAM, so own-offence may be
standing in for a good defence.** Control = the team's prior-season points ALLOWED per game.

| model | own offence | prior points allowed |
|---|---|---|
| own offence alone | +0.0914, t **+2.06** | |
| **+ prior points allowed** | +0.0480, t **+1.04** | **−0.1837, t −2.71** |
| + prior D/ST points per week | +0.0442, t +0.92 | −0.1570, t −1.36 |

**THE PREDICTION SURVIVES AND THE MECHANISM DOES NOT.** What forecasts a defence is how good that
defence already was. `[TESTED]`

**AND IT LETS CLEVELAND OFF.** Their 2025 offence was **29th of 32** at 16.4 a game, which is what
Matt saw. **Their defence was 17th of 32** at 22.3 allowed. Corrected weeks 2-4, free teams plus
his: KC 18.5, NO 17.8, CHI 17.4, **CLE 17.2**, LA 16.9, GB 16.5, SF 15.9. **Kansas City leads
because its defence was 7th in points allowed, which `build_dst.py` cannot see, and that is also
why ESPN had KC fifth while our file had it 25th of 32.** Matt's opening instinct on Kansas City
was better than our number.

## 4. TEST TWO: THE BEARS MECHANISM, SPLIT OUT BECAUSE TEST ONE WOULD HAVE HIDDEN IT

Total D/ST points are mostly the points-allowed band, so a turnover effect could be invisible
inside it. **OUTCOME SPLIT IN TWO:** takeaways (sack + 2×int + 2×fumble + 4×safety + 6×TD) and the
band. Same population, same control.

| outcome | own offence alone | own offence given prior PA |
|---|---|---|
| **takeaways** (mean 5.97/wk, sd 1.30) | +0.0436, t +1.55 | +0.0261, t +0.88 |
| points-allowed band (mean −0.50/wk, sd 1.16) | +0.0478, t +1.92 | +0.0220, t +0.85 |

**NULL, and the SPLIT is the finding: the effect on takeaways and the effect on the band are the
same size.** If leads were forcing mistakes, the takeaway half should carry more of it. It carries
exactly half, which is what an undifferentiated team-quality effect looks like. `[TESTED, null]`

**FAILED POWER AS MUCH AS PREDICTION (section 4.24b).** His effect, at the size the point estimate
suggests, is about +0.18 a week per sd of offence; the smallest this design could see is about
+0.23. **Report null, underpowered, AND what would resolve it: more seasons, or a within-team
specification that uses a club's own offensive swings rather than cross-sectional differences.**

## 5. A FALSIFIER I FIXED IN ADVANCE AND THEN FAILED

**Stated first: if the own-offence term is what our projection is missing, adding it should move our
numbers TOWARD ESPN's week-2 projections.** Result: r = +0.125 to **+0.148**, n=10. Nothing.
**So this does NOT explain the ESPN disagreement and nothing here is validated by ESPN's agreement.**
Reported because it was fixed in advance (section 0.2).

## 6. THE DEFECT THIS EXPOSES IN THE PAGE

`wire.py`'s defence block ranks the hold candidates **by opponent slate alone**. Its own advice is
right: *"hold one defence through a soft run rather than chasing weekly."* **Its ranking key is
incomplete, and it is incomplete on the variable that varies most.** Slate sd across teams over a
14-week run is 1.09 points a game; the defence's own prior points allowed is the term that survives
every control at t = −2.71.

**NOT YET RUN, with the form and the control written down:** add a prior-season points-allowed term
to `dst_runs()` at the measured **β = −0.1837 per point allowed per game**, print the defence's own
prior rank beside the slate, and plant a control that inverts two teams' prior defensive quality and
asserts the printed order flips. **Do NOT ship it before the control fires** (section 0.2: a guard
that has never been executed is not a guard). **And haircut it in the prose: defensive quality
persists year to year at only +0.204 (section 4.22a), so the correction is real and weak.**

## 7. STILL BLOCKED, SAME INPUT AS DOC 336

Everything above is prior-season. **Nothing here has seen a 2026 snap.** The missing input is
`play_by_play_2026.csv.gz` from nflverse; `Scripts\research\_nflverse_cache\` holds 2022 through
2025 and no 2026 file. `build_dst.py` and `dst_all.py` both run against it unchanged.

## 8. THE RECORD

Section 0.5(a4)'s count moves. **Matt: confirmed or partly confirmed 13, null 8, underpowered his
way 2.** Test one is a partial confirmation, the prediction without the reason. Test two is a null
that is honestly underpowered. **He proposed two mechanisms on one variable in one evening and one
of them found something nothing in this project had looked for.**
