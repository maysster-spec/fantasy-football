# ESPN payload audit: espn_raw_2026_20260930_2146.json

Scope: 700 player entries; top-level keys are only `players` and `positionAgainstOpponent`. "pull" = Espn_pull_projections.py. "wire" = wire.py, which reads its OWN live kona_player_info/mTeam/mRoster responses (not this file, so a wire read means the same key in a different response). sheet_engine.py never opens this JSON; it reads the pull's CSV (proj_2026, actual_2026). 103 collapsed key paths with counts and read_by are in payload_keys.csv (stat ids, rankings keys and outlook weeks collapsed to <statId>, <rankKey>, <week>).

## player.stats[] combinations (players carrying each)
| seasonId | src | split | period | n | what it is |
|---|---|---|---|---|---|
| 2026 | 0 | 0 | 0 | 700 | 2026 season-to-date actual (id 002026); appliedTotal set |
| 2026 | 1 | 0 | 0 | 599 | 2026 rest-of-season projection (id 102026); appliedTotal set on all 599 |
| 2026 | 0 | 1 | 1 | 6 | week 1 actual, 6 players only |
| 2026 | 0 | 1 | 2 | 609 | week 2 actual; appliedTotal set, nonzero on 358 |
| 2026 | 0 | 1 | 3 | 615 | week 3 actual; appliedTotal set, nonzero on 352 |
| 2026 | 1 | 1 | any | 0 | single-week 2026 projection: ABSENT. No row has scoringPeriodId 4 |
| 2025 | 0 | 0 | 0 | 608 | 2025 season actual (002025) |
| 2025 | 1 | 0 | 0 | 587 | 2025 season projection row (102025) |
| 2025 | 0 | 1 | 6-18 | 115 rows | 2025 weekly actuals; 45 and 55 of them in weeks 17 and 18 |

## Key paths (read? and meaning)
| path | read? | meaning |
|---|---|---|
| player.id, fullName, defaultPositionId, proTeamId | pull, wire | id, name, position (1 QB 2 RB 3 WR 4 TE 5 K 16 D/ST), NFL team |
| player.injuryStatus | pull, wire | ACTIVE 534, QUESTIONABLE 54, INJURY_RESERVE 52, OUT 14, DOUBTFUL 8, DAY_TO_DAY 1, absent 37 |
| player.ownership.percentOwned | pull, wire | roster % across ESPN |
| player.ownership.percentChange, percentStarted, date | wire | the +/- column, start %, time ESPN refreshed them |
| player.ownership.averageDraftPosition | pull (CSV only) | ADP; no page reads it |
| player.draftRanksByRankType.STANDARD/PPR .rank | pull (CSV only) | preseason ranks; no page reads them |
| player.stats[].id, appliedTotal, stats.<statId> | pull (+ sheet_engine via CSV) | picks rows 002026/102026; points; stat lines (only the SCORING-map ids and 210 are interpreted) |
| entry.status, waiverProcessDate | wire | WAIVERS 505 / ONTEAM 195; waiver clear time (epoch ms) |
| entry.onTeamId | wire, no effect | the branch that reads it assigns '' to an already-empty value |
| player.ownership.{activityLevel, auctionValueAverage, auctionValueAverageChange, averageDraftPositionPercentChange, leagueType} | UNREAD | activityLevel is None on all 700 |
| player.draftRanksByRankType.{ELIMINATION, SUPERFLEX, *.auctionValue, published, rankSourceId, rankType, slotId} | UNREAD | other rank types and metadata |
| player.stats[].{appliedAverage, externalId, proTeamId, scoringPeriodId, seasonId, statSourceId, statSplitTypeId} | UNREAD | pull selects rows by the id string instead |
| player.outlooks.outlooksByWeek.<2,3,4>, player.seasonOutlook | UNREAD | news text, see below |
| player.rankings.<0-4>[] {rank, averageRank, rankSourceId, rankType, slotId, published, auctionValue} | UNREAD | expert ranks by source, 571 players |
| player.{active, droppable, eligibleSlots, injured, firstName, lastName, jersey, lastNewsDate, lastVideoDate} | UNREAD | flags, slots, names, dates |
| entry.{id, ratings.0.*, keeperValue, keeperValueFuture, draftAuctionValue, droppedByEliminatedTeam, lineupLocked, rosterLocked, tradeLocked} | UNREAD | ratings.0.totalRating equals 002026 appliedTotal on 700 of 700 |
| positionAgainstOpponent.positionalRatings.<pos>... | UNREAD | top level, see item 8 |

## UNREAD AND POSSIBLY MATERIAL
1. stats[] appliedAverage and stat 210 on the 102026 row: the games the projection covers. Median appliedTotal/appliedAverage is 14.0 (stat 210 = 14.0 on 85 of 102 RBs, 141 of 166 WRs), but ALL 32 D/ST rows show 17.0 (Seahawks D/ST: total 101.7, average 5.98, stat 210 = 17.0). sheet_engine divides every proj_2026 by games left (14), so my reading of the code is that D/ST per-game rates come out about 21% high. Not tested on a page.
2. Weekly actual rows (2026, src 0, split 1, weeks 2 and 3): each player's last two games' league-scored points plus stat lines. 821 QB/RB/WR/TE rows reconcile to the pull's SCORING map, 0 off by more than 1 point.
3. outlooksByWeek.4: this week's news blurb for 312 players (role and injury context).
4. player.droppable: False on 16 players (Gibbs, Chase, Josh Allen, Lamar Jackson, Bijan Robinson...); the league settings observe ESPN's undroppable list.
5. player.injured: True on exactly the 66 players whose injuryStatus is OUT or INJURY_RESERVE, which is the IR-slot-eligible set.
6. player.lastNewsDate (662 players): epoch ms of the newest news item, a recency check on the blurb.
7. player.rankings.<0-4>[]: per-source ranks plus averageRank. Pickens reads about 11-14 under key 0 and 17-19 under key 4; the file does not label the keys, so whether they are periods is not confirmed.
8. positionAgainstOpponent.positionalRatings: positions 1,2,3,4,5,16, 32 opponents each, an average and a rank. wire.py uses last season's pos_allowed_2025.csv instead; this block's season window is not stated in the file.
9. entry.ratings.0.positionalRanking: rank by season-to-date points (Pickens 36); duplicates 002026 data.
10. player.eligibleSlots: lineup slot ids each man can fill (Pickens [3,4,5,23,7,20,21]).

**Weekly projected points in the payload: NO. Read: NO (nothing to read).** The only projection is the 102026 rest-of-season total, read as proj_2026. The pull's request lists only stat sets 002026, 102026, 002025, 102025 (additionalValue), so it never asks for a weekly projection set; I did not test whether ESPN serves one under another id.

## Text fields
outlooksByWeek: week 2 on 306 players (median 541 chars, 262-833), week 3 on 311 (534, 301-988), week 4 on 312 (548, 152-926). seasonOutlook: 337 players (median 686, 109-1026). Only 4 blurbs contain the word "project".

## Spot-checks (actual values)
- George Pickens (id 4426354, WR, proTeamId 6, ONTEAM 9): wk2 7.0, wk3 11.7, 002026 23.0 (avg 7.67), 102026 164.27 (avg 11.73, stat 210 = 14.0), percentOwned 99.28, percentChange 0.0, ACTIVE, droppable True, wk4 outlook 671 chars.
- Ollie Gordon II (id 4711533, RB, proTeamId 15, WAIVERS, waiverProcessDate 1790838000000 = 2026-10-01 07:00Z): wk2 0.7, wk3 13.0, 002026 13.7, 102026 136.34 (avg 9.74), percentOwned 57.43, percentChange 55.78, percentStarted 12.13, wk4 outlook 518 chars.
- Also: Brandon Aubrey (K) 102026 140.6, stat 210 = 14.0; Seahawks D/ST 102026 101.7, stat 210 = 17.0.

Note: both scripts hard-code ESPN session cookies (swid, espn_s2) in source; values not reproduced here.
