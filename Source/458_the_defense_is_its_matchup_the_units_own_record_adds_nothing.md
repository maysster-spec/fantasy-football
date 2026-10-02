# 458. THE DEFENSE IS ITS MATCHUP: THE UNIT'S OWN RECORD ADDS NOTHING BESIDE THE LINE

*1 Oct 2026, 01:40 ET. Claude (Cowork). Matt, 1 Oct 01:15, on Packers over Bears: "GB currently ranks at the 30th D/ST
... Chicago is ranked 8th, no negative weeks ... Are you sure about that? ... What is the counter argument?" 458 reserved
by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Keep the Bears claim if you like; the measured cost of feel over the line is about 1.7 points this week and about the
   same next week.** Your claims are yours (section 0.4). What the numbers say: in your exact shape (a top-12 unit facing
   an opponent total 2 to 3 points higher than a bottom-ten unit's, 364 pairs over five seasons) the better matchup scores
   5.9 a week and the better unit 4.2, and the matchup wins 60% of the pairs.
2. **What 17.5 and 20.0 are:** the opponent's implied points from the pregame line, total over two minus the spread over
   two. Tampa is expected to score about 17.5 at home to Green Bay; the Jets about 20 at Chicago. Fewer expected points
   for the offence across from your defense means fewer points allowed, more sacks and more turnovers in the game script.
   That one number is worth about three D/ST points a week over picking at random (finding 4.39), and it is on the wire page
   every Wednesday.
3. **The counter-argument, tested, and it dies: a defense's own season-to-date scoring carries nothing beside the
   matchup.** On 2,238 unit-weeks (2021 to 2025, two or more prior games, a line on file): in a regression of this week's
   D/ST points on both, the unit's own average is minus 0.02 points per standard deviation (se 0.14) and the opponent's
   implied total minus 2.12 (se 0.14). As a pick rule among all 32 units, "highest own average" is +1.0 over random (t 1.2)
   against the line's +4.1 (t 5.7); the line beats it by 3.05 a week, 41 weeks to 24. Rank, sacks a week and interceptions
   are all inside "own average", and own average adds nothing. The wire's rule stands, and now it has a tested rival.
4. **Nothing to run.** The script is `Scripts\research\own_quality_dst.py` beside `vegas_streams.py` (doc 441), whose
   loaders it reuses; its output is `run_own_quality_dst.txt`.

---

## 1. THE MEASUREMENT

**The claim in testable form, Matt's:** picking the defense with the higher own season-to-date average beats picking the
one facing the lower opponent implied total, and the own average carries weight beside the line.

| what | number |
|---|---|
| Spearman with this week's D/ST points, n=2,238 | own season-to-date average +0.10; opponent implied total minus 0.33 |
| regression, points per one sd of each | own average minus 0.02 (se 0.14); opponent implied total minus 2.12 (se 0.14) |
| pick rule, all 32 units, 75 season-weeks | line +4.08 over random (t 5.7); own average +1.03 (t 1.2); line minus own +3.05 (se 1.17), 41-24-10 |
| pick rule, the streamable pool (rank 13 to 32) | line +3.16 (t 4.4); own average +1.04 (t 1.4); line minus own +2.13 (se 1.02), 41-26-8 |
| head to head, top-12 unit facing a total 2+ points higher than a rank-23-or-worse unit's, n=1,536 pairs | good unit 3.64, worse unit with the better matchup 6.58; the matchup wins 65% |
| the same at a gap of 2 to 3 points (Bears 20.0 against Packers 17.5 is 2.5) | n=364: 4.19 against 5.90, the matchup wins 60% |
| at 3 to 5 points; at 5 or more | 3.88 against 6.61 (64%); 3.06 against 6.96 (69%) |

Population: every D/ST team-week 2021 to 2025, regular season weeks 1 to 17, with two or more prior games and a pregame
line (nflverse games.csv, `vegas_streams.py`'s sign checks), D/ST points under this league's rules from the 2,718-row file
of doc 441. "Rank" is by prior-weeks average within the season, the same instrument ESPN's ranking approximates.

What this does not say: that the Bears are a bad unit, or that Green Bay will have a good day. It says that over five
seasons the unit's record told you nothing the opponent's expected score had not already told you, and that the feel of
"sacks every week, three interceptions" is the kind of thing that does not carry forward week to week once the matchup is
known. Finding 4.47 at v9.38.

## 2. THE FINER POINT (added 02:05, Matt: "where do these really bad defenses land on that spectrum? ... is there a finer
point to be made without too much noise to catch the signal?")

**Testable form:** within the softest matchups, D/ST points fall with the unit's own rank (a bad unit wastes a soft
matchup); and taking the better unit when two matchups are close beats the plain rule. `own_quality_dst2.py`.

Mean D/ST points by the unit's own tier (rows, season-to-date rank) and the opponent's implied total (columns), with the
share of 10-point weeks and of weeks at or below zero in brackets, n=2,238:

| own tier | 17.5 or less | 17.5 to 20 | 20 to 22.5 | 22.5 to 25 | over 25 |
|---|---|---|---|---|---|
| top 8 | 8.7 (38% / 7%) n=133 | 6.7 (28% / 12%) n=117 | 5.1 (19% / 23%) n=161 | 4.4 (19% / 26%) n=134 | 2.9 (12% / 40%) n=73 |
| 9 to 16 | 8.1 (36% / 8%) n=66 | 6.8 (33% / 18%) n=132 | 5.8 (28% / 22%) n=137 | 3.1 (14% / 31%) n=140 | 2.3 (6% / 37%) n=134 |
| 17 to 24 | 8.7 (39% / 7%) n=56 | 6.8 (26% / 16%) n=102 | 6.8 (35% / 15%) n=135 | 3.5 (15% / 29%) n=124 | 2.2 (10% / 39%) n=174 |
| 25 to 32 | 7.4 (37% / 21%) n=19 | 7.6 (36% / 13%) n=47 | 5.8 (26% / 17%) n=96 | 3.5 (17% / 36%) n=105 | 1.8 (9% / 43%) n=153 |

Read down any column and the tiers are flat; read across any row and the points fall by about six from the softest
band to the hardest. Within the soft matchups (opponent total 19 or less, n=487) the tiers score 8.2, 7.6, 7.9 and 7.8,
Spearman of own average with points +0.05, and the interaction term in the regression is +0.01 (se 0.13): a bad unit does
not waste a soft matchup and a good unit does not rescue a hard one. The one place the intuition shows is the bust rate
of the worst tier in the softest band, 21% at or below zero against 7% to 8% for the others, on 19 weeks (four busts):
too thin to act on, and the mean there is still 7.4.

As a pick rule, 75 season-weeks, against the plain lowest-total rule: the better unit among totals within 1.5 points
of the lowest, +0.18 a week (se 0.59), 20 wins, 14 losses, 41 ties; within 3.0 points, minus 0.31 (se 0.70); the lowest
total but never a unit ranked 25 to 32, +0.13 (se 0.20), 4 wins, 1 loss, 70 ties. **So the finer point, honestly: when
two matchups are within about a point and a half, taking the better unit costs nothing and is not measured to help;
beyond that, the matchup, and the Bears against the Packers were 2.5 apart.** The wire's rule stands as written.

## 3. OPEN, BY NAME

- **Matt's:** unchanged from doc 457.
- **Mine, tomorrow:** v9.38 now carries 4.44 to 4.47; the rest as doc 457.
