# Same-team WR pair: hidden cost or not (half-PPR, regular season weeks 1-14, 2021-2025)

**Claim, in testable form.** Matt: "if the team busts that week I'm down two players, and each limits the upside of the other when one has a big game and takes my targets and receptions."
- Population: each team-season's top two WRs by total targets (weeks 1-14), both with a row in at least 8 of those weeks. 160 team-seasons, 148 qualify.
- Unit: pair-weeks where both have a row. Points = 0.1 x (rush + rec yards) + 6 x (rush + rec TDs) + 0.5 x receptions - 2 x (fumbles lost).
- First half = teammates' weekly points correlate POSITIVELY more than two unrelated receivers. Second half = they correlate NEGATIVELY (cannibalise).
- Control: per season-week, the WR2s are randomly re-dealt among the WR1s of other teams, 2,000 draws. The control has identical WR1 and WR2 values, so only the pairing differs.

| metric | all pairs: same team | control | diff [95% CI] | both 10+ ppg: same team | control | diff [95% CI] |
|---|---|---|---|---|---|---|
| pooled weekly r | 0.093 | 0.003 | +0.090 [+0.036, +0.145] | 0.050 | 0.032 | +0.018 [-0.089, +0.122] |
| within-pair r (each pair's own averages removed) | 0.012 | 0.007 | +0.005 [-0.047, +0.060] | 0.030 | 0.037 | -0.008 [-0.119, +0.107] |
| median per-pair r | 0.009 | 0.000 | +0.009 [-0.050, +0.047] | -0.033 | -0.001 | -0.032 [-0.163, +0.090] |
| share of weeks, pair sum >= 30 | 15.6% | 14.8% | +0.8 pts [-1.9, +3.9] | 35.1% | 34.2% | +1.0 pts [-5.5, +7.4] |
| sd of pair sum (pts) | 10.18 | 9.75 | +0.42 [-0.06, +0.92] | 11.16 | 11.06 | +0.10 [-0.77, +0.89] |
| n | 148 pairs, 1,636 pair-weeks | | | 33 pairs, 367 pair-weeks | | |

Notes. n for median per-pair r is 148 pairs (all) and 33 pairs (10+ ppg), each needing 6 or more joint weeks. Its control gives each WR1 a fixed other-team WR2 from the same season. CIs bootstrap the pairs (1,000 resamples) with the control held at its mean (control draw sd for pooled r: 0.024 all, 0.048 at 10+ ppg). Across pairs, the two receivers' season-average points correlate +0.40 (all) and +0.35 (10+ ppg). "Played" means a row exists in the weekly file (20% of WR rows are 0.0 points, so a quiet week still counts); a traded man counts as a separate player-team stint; 2-pt conversions are not scored, per the spec. 2026 not used.

Week to week there is no measurable "busts together" and no measurable "cannibalise": with each pair's own averages removed, teammates sit +0.005 above the cross-team control (CI -0.05 to +0.06), and the median pair is +0.009. The only positive number is the pooled +0.09, and it is a level effect (receivers on the same pass-heavy offence are both good, +0.40 across pairs), not a weekly one, while the upside is the same in practice: 30+ point weeks 15.6% against 14.8% and the spread of the sum 10.2 against 9.8 points, both inside the noise. Among starter-quality pairs there are only 33 pairs, so effects up to about 0.10 in either direction cannot be excluded, but every point estimate there is under 0.05 and the data lean neither way, so the evidence does not support treating a same-team pairing as a cost.
