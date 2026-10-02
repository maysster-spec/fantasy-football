# Job size vs relief scoring, RB absences 2021-2025 (REG weeks 1-14, nflverse, half-PPR)

**Claim, testable form:** across RB absences, the relief back's half-PPR points a game during the absence (Y) rise with the absent starter's points a game before it (X). A flat 12.1 is wrong if that slope is real and large.

**Population (n = 30 absences, 24 starters):** starter = RB who led his team-season in carries plus targets over weeks 1-14 and averaged 10+ a game when active (160 such starter team-seasons, 70 missed at least one team game). Absence = maximal run of 2+ consecutive team games (bye skipped) with zero opportunities, after 2+ games played. Relief = team RB with the most opportunities in the run. Y = his points per game played in the run. X = starter's points per game played before it (median 6 games). 1 run dropped because the starter was playing for another team (a departure). Mean absence length 2.7 games. Rows: job_slope_absences.csv.

| measure | value |
|---|---|
| Y mean (bootstrap 95%) / median / sd | 11.14 (10.0 to 12.3) / 11.33 / 3.32; flat sheet rate is 12.1 |
| X mean | 12.01 points a game |
| Slope of Y on X (OLS) | -0.076 per point of X, se 0.141, bootstrap 95% [-0.292, +0.197] (5000 resamples of absences) |
| Correlation of Y with X | Pearson -0.102, Spearman -0.097, R2 0.010 |
| X tercile bottom (mean X 7.1) | n=10, mean Y 11.03, median Y 11.46 |
| X tercile middle (mean X 12.2) | n=10, mean Y 11.77, median Y 12.21 |
| X tercile top (mean X 16.8) | n=10, mean Y 10.62, median Y 9.21 |
| Subset with relief back's prior ppg known | n=24, slope on X alone -0.016 (se 0.196, 95% [-0.412, +0.318]) |
| Slope on X controlling for relief back's own prior ppg | +0.078 (se 0.220, 95% [-0.427, +0.516]); prior-ppg coefficient +0.178 (se 0.185, 95% [-0.144, +0.752]); corr(X, prior ppg) -0.45 |
| Check: X as starter's opportunities a game | slope -0.004 (se 0.138, 95% [-0.247, +0.322]) |
| Check: first absence per starter-season only | n=30, slope -0.076 (se 0.141, 95% [-0.285, +0.182]) |
| Check: absences of 3+ games | n=14, slope -0.206 (se 0.169, 95% [-0.466, +0.111]) |
| Check: departures kept (literal spec) | n=31, slope -0.025 (se 0.139, 95% [-0.241, +0.250]) |
| Check: Y per team game instead of per game played | n=30, mean Y 10.75, slope -0.117 (se 0.157, 95% [-0.336, +0.157]) |
| Check: starter = top RB by opportunities per game (4+ games played, 10+) | n=39, slope -0.137 (se 0.206, 95% [-0.492, +0.238]), mean Y 11.90 |

**Face value (fitted line):** a 15-a-game job (260 points a season) gets 10.91 and a 9-a-game job (150 points) gets 11.37, a gap of -0.46 points a game. The 95% interval on the slope allows a gap from -1.8 to +1.2.

It leans against the claim: relief scoring moved -0.08 a game per point of starter job (95% -0.29 to +0.20), which cannot be told apart from zero. The job adds nothing detectable beyond the man: with the relief back's own prior scoring held fixed the job slope is +0.08 (95% -0.43 to +0.52, n=24). At face value the 260-point job gets 10.9 and the 150-point job 11.4 (-0.5 a game, top of the interval +1.2), and the mean relief rate here is 11.1 (10.0 to 12.3), so nothing here supports replacing the flat 12.1 with a job-size rate; with n=30 this caps the slope near +0.20 a point rather than proving it is zero.
