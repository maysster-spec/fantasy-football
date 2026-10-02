# 292 · No gate where a rank will do: the risers, the clear path and the metrics

*11 Sept 2026, 1:30 pm ET. In-season red team. Catalog items: A9 (extended), A17 (new), B11 (new), E4
(extended), E5 (new). Every result states its population, outcome and n. Scripts are in `Scripts\research\`
(section 8) and read nflverse files from the folder they run in.*

**Matt, 11 Sept, verbatim:** *"I do think broken tackles, yards after contact, win rate, yards after catch,
separation, and other performance metrics mater when determining potential value that likely lies outside of
ESPN projections. The scenario again is circumstances change before ESPN catches up. Plus, we may wish to stash
players anyway that are behind higher value running backs with teams that have a clear path to the next man up
soaking up enough of that volume to be fantasy relevant for my roster. I'm sure you can put better words and
logic on that point. however. plus, other scenarios apply that are worth considering for stash and potential
value. Yes, petagree matters too, but even undrafted free agent pick ups nfl teams get can begin to earn enough
targets to be fantasy relevant. this is rare I understand but I provided that example to underscore that it is
possible and no sense in ruling it out. We don't want rules that create blind spots"*

**The testable forms, stated before any result.** (1) Undrafted and late-round players make up a real share of
mid-season risers, so a pedigree gate discards hits. (2) Once a team is using a player, his draft tier adds little
to whether the role turns into startable points. (3) A backup who already takes most of the backup work absorbs
most of the job when the starter sits, and scores. (4) Efficiency metrics add to usage in naming who converts.
Direction in all four: his.

---

## 0. What changed

1. **Undrafted players are rare per player and common among risers.** 2019-2025: 60 of 355 mid-season risers were
   undrafted, more than came from the first round (44). A rounds 1-3 gate discards 53% of risers. `[TESTED]`
2. **Once the team is using him, pedigree mostly stops sorting.** At his first starter-level snap week after already
   playing 35%+ of snaps: undrafted 17.8%, drafted 22.2% (p=0.37). **The exception is the emergency spike:** from
   under 35% of snaps, undrafted 5.5% against drafted 14.8% (p=0.031). `[TESTED, seven seasons]`
3. **The clear path is real and can be read before the injury:** the backup's share of his team's backup RB snaps.
   85%+ of them: 65% scored like a starter in the first game the lead back missed. Under 70%: 29%. n=154,
   p=0.002, and the direction replicates on the earlier seasons alone. `[TESTED]`
4. **Most performance metrics do not repeat at a backup's volume**, so they cannot carry much signal where he wants
   them. RB yards after contact per carry is the exception. Added on top of usage, two of sixteen cells lean his way
   in two independent periods, and none clears the multiple-comparison bar. `[UNDERPOWERED]`
5. **Separation and win rate exist only for players who already have volume.** They cannot see the backup before
   his jump. `[BLOCKED for that population, inputs named in section 4]`
6. **The page code hides risers behind six gates** (section 1). Fix direction: each gate becomes a ranking term,
   plus one pedigree-blind usage lane (A17). **One piece shipped today** so the Tuesday read can see free players the
   board never rated: `Source\FREE_UNRANKED_<date>.csv`. Building its control found a latent crash in the live
   `wire.py` (a player with no ownership number would have stopped every page); fixed with it (section 6).

---

## 1. The gates in the page code (A17), counted on the 10 Sept inputs

| where | the gate | what it hides | count on 10 Sept |
|---|---|---|---|
| `wire.py` pool fetch: `limit 400`, sorted by ownership | only the 400 most-owned free players exist | a riser owned 0.0% | 28 board rows at 0.0% sat inside the 400, so the cut falls inside the zero-owned block and the rest of that block is dropped in ESPN's order. How many: unknown without the live pool (A13) |
| `wire.py` lanes 1-3 and `WIRE_<date>.csv` | priced only if on the draft board | every free player the board never rated | 71 free skill players, named on the page only, first 30 shown |
| `wire.py` lane 3, `build_pedigree.py` | receivers only; drafted since 2021; three of three needs NFL round 3 or earlier | every RB and TE riser; every undrafted player, by construction | 14 screened players on the whole board, owned or free (9 three-of-three, 5 first-round rookies). Receivers drafted in rounds 1-3 were 72 of 355 risers 2019-2025 (20%) |
| `wire.py` lane 2, `depth_map.csv`, `build_inherit.py` | RBs only; the number two on the 8 Aug depth chart; one man per team | receiver and tight-end inheritance; a number two who lost the job since August; a committee | 111 RB rows, one next man for each of 32 teams; `free` is read from the board-only WIRE file, so a free backup off the board would read as rostered (latent: all 32 next men are on the board today) |
| `sheet_engine.py` `rates()` | priced only with a positive 7 Sept ESPN projection | call-ups, players returning from injury, anyone ESPN zeroed | 199 skill rows in the 7 Sept pull at or below zero: WR 71, TE 51, RB 41, QB 36 (A3, doc 277) |
| `sheet_engine.py`, the bet | two archetypes: three of three, first-round rookie | every other potential shape | n/a |

Display cuts, not exclusions: `SHOW_PER_POS = 8` on the console and eight rows a position on the page. The CSV holds
every priced row.

---

## 2. Risers by draft tier (T1, T3)

**T1. POPULATION:** RB/WR/TE player-seasons not established last season (6+ games at or above the position's
per-game bar: RB 9.92, WR 9.62, TE 8.25 half-PPR, derived from section 4.1 of the directive divided by 17) and under
the bar in weeks 1-4. **OUTCOME:** a riser is four straight games played in weeks 5-17 averaging at or above the
bar. **TIER:** nflverse `draft_picks`; undrafted when no draft row exists.

| tier | 2022-2025 risers / population | rate | share of risers | 2019-2025 risers / population | rate | share of risers |
|---|---|---|---|---|---|---|
| round 1 | 26 / 94 | 27.7% | 13.4% | 44 / 155 | 28.4% | 12.4% |
| rounds 2-3 | 73 / 338 | 21.6% | 37.6% | 122 / 536 | 22.8% | 34.4% |
| rounds 4-7 | 69 / 548 | 12.6% | 35.6% | 129 / 939 | 13.7% | 36.3% |
| undrafted | 26 / 460 | 5.7% | 13.4% | 60 / 873 | 6.9% | 16.9% |

A rounds 1-3 gate discards 49% of risers on 2022-2025 and 53% on 2019-2025. **Pedigree sorts the rate by a factor
of four and does not come close to deciding who rises.** By position 2019-2025: RB 122 risers, WR 148, TE 85.
53 of the 60 undrafted risers had at least one NFL season behind them; 7 were rookies (Zonovan Knight, Rashid
Shaheed, Keaton Mitchell and Jalen Coker among them). Among players in years 0-2 only, undrafted was 26 of 195
risers (13.3%).

**T3. What could be seen in the two games before the four-game stretch began** (2022-2025, the 194 risers): his snap
share at the starter line (RB 50%, WR 65%, TE 60%) in one of them 54%; the bar in one of them 24%; either 62%;
neither, or no game, 38%. First-round risers showed the snap line first 85% of the time (22 of 26); undrafted
risers 42% (11 of 26). **About four risers in ten give no usage or scoring sign two games out, whatever lane looks.**

---

## 3. The usage lane, priced (T4, T2)

**T4. POPULATION:** NFL-wide player-weeks, weeks 3-13, RB/WR/TE not established last season and not already scoring
at the bar that season. **OUTCOME:** his next four games played (two or more) average at or above the bar. The
decision rows are one per player-season, at the first week the flag fires. Tier joins on the PFR id, which
`draft_picks` carries for about 100% of picks since 2010 (the first version joined on the gsis id and gave the same
tables on 2022-2025).

**2019-2025, seven seasons, 77 season-weeks:**

| what the week showed | names a week, NFL-wide | first flags | converted |
|---|---|---|---|
| snap line AND the bar | 14.3 | 623 | **26.0%** |
| snap line, under the bar | 32.3 | 898 | **16.0%** |
| the bar, under the snap line | 9.5 | 543 | 13.6% |
| neither | 150.4 | (all player-weeks) | 3.8% |

| first flag, by tier | round 1 | rounds 2-3 | rounds 4-7 | undrafted |
|---|---|---|---|---|
| snap line AND the bar | 36.1% (83) | 28.3% (219) | 23.3% (219) | 18.6% (102) |
| snap line, under the bar | 21.7% (115) | 20.5% (283) | 12.8% (320) | 11.1% (180) |
| **first snap-line week, already 35%+ of snaps before** | 29.5% (112) | 24.2% (264) | 16.6% (247) | **17.8% (107)** |
| **first snap-line week, a spike from under 35%** | 13.3% (15) | 13.3% (60) | 15.6% (128) | **5.5% (91)** |

Undrafted against drafted: already in the rotation **17.8% vs 22.2%, p=0.37**; the spike **5.5% vs 14.8%, p=0.031**.
Snap line and the bar, undrafted against rounds 2-7: 18.6% vs 25.8%, p=0.16.

**The replication record, kept because the first cut overstated.** On 2022-2025 alone the undrafted spike was 1 of
46 against 16.8% (p=0.013), and T2's stricter jump gave 0 of 49 (p=0.0002). On the independent 2019-2021 seasons the
spike was 4 of 45 against 12.7% (p=0.59). Pooled, the direction holds and the rate is about a third of the drafted
rate, not zero. The rotation result moved the other way: 19.1% vs 20.2% on 2022-2025, 16.7% vs 25.1% on 2019-2021.
**Quote the seven-season numbers only.**

**T2. The jump, a stricter object.** POPULATION: the first game in weeks 2-14 at the starter line after averaging under
35% in one or more earlier games that season, excluding a snap starter last season (the first definition counted Allen
Lazard's 2022 return from injury as a jump). OUTCOME as T4. 2019-2025, n=349, 15.2% converted.
- **It is a running-back event.** Drafted backs 31-39% (rounds 2-3: 38.7% of 31; rounds 4-7: 31.2% of 64); receivers
  5-13%; tight ends under 8%. Logistic, position in: RB +1.40, z 3.70.
- **A shock adds nothing measurable:** the position's snap leader sat out the jump game 17.6% vs 13.8%, p=0.35.
- Scoring the bar in the jump game 24.0% vs 10.3%, p=0.001, but z 0.96 once position and tier are in: backs do both.

**What this is not:** whether the lane names a player before a rival in this league adds him. That is E4, and needs
this league's add log against the week of the flag. NOT YET RUN.

---

## 4. The performance metrics (B11)

**Preseason form: already TESTED, NULL (doc 190, 6 Sept).** Prior-season yards per carry, EPA per carry, YAC per
catch, yards per target, EPA per target and aDOT against beating the preseason ADP price: n=699, nothing under p=0.30,
five of six the wrong way. **The directive's section 4.6 still calls after-contact ability "underweighted"; that
downgrade never reached it** (`AUDIT_LEDGER.md` row 19).

**In-season form (T6).** nflverse PFR advanced stats, weekly, 2019-2025.

**(a) Does the number repeat?** Odd weeks against even weeks of the same season, r (player-seasons):

| position, volume per half | efficiency | volume, the benchmark |
|---|---|---|
| RB, 10-30 carries (237) | yards after contact a carry **+0.55** · broken tackles a touch +0.21 | carries a game +0.65 |
| RB, 30-60 carries (181) | +0.68 · +0.32 | +0.61 |
| RB, 60+ carries (277) | +0.79 · +0.57 | +0.74 |
| WR, 5-15 catches (461) | YAC a catch +0.32 · broken tackles a catch +0.15 · yards a target +0.14 | targets a game +0.59 |
| WR, 15-30 catches (371) | +0.43 · +0.29 · +0.23 | +0.54 |
| WR, 30+ catches (225) | +0.46 · +0.39 · +0.17 | +0.58 |
| TE, 5-15 catches (274) | +0.18 · +0.21 · +0.13 | +0.60 |
| TE, 15-30 catches (168) | +0.37 · +0.27 · +0.20 | +0.62 |

**At a backup's volume only RB yards after contact a carry repeats about as well as volume does.** Inside one season
that can be the line and the role as much as the legs; it is still the object that matters for the rest of that
season on that team.

**(b) Does it add to usage?** At the first snap-line week (866 player-seasons; 694 above a volume floor of 15 carries
or 5 catches to date), split at the position median, inside "scored the bar that week" and not: sixteen splits, ten
lean his way. Two lean his way in both independent periods:
- a receiver with above-median broken tackles who also scored: 2019-2021 **34.8% vs 17.2%** (n=52); 2022-2025
  **31.8% vs 11.9%** (n=64); pooled p=0.020;
- a tight end with above-median yards a target who also scored: **40.0% vs 12.5%** (n=18); **40.0% vs 7.7%** (n=33);
  pooled p=0.025.
**Neither clears 0.05 / 16 = 0.003.** RB yards after contact did not replicate (2022-2025 60.0% vs 31.6%; 2019-2021
35.0% vs 35.0%). `[UNDERPOWERED: two cells worth re-testing on 2026]`

**(c) BLOCKED for the population he means, inputs named.**
- **Separation:** NGS publishes a weekly line only for receivers with volume, a median of 68 a week in 2025 (56 to
  80, checked 11 Sept on `ngs_receiving.csv.gz`). A backup before his jump has none.
- **Win rate:** ESPN Analytics' receiver scores (Open, Catch, YAC, Overall; `espnanalytics.com/receivers`, undated
  page, read 11 Sept 2026) are season-level with a minimum of 22 targets for WR/TE and 15 for RB in 2025 (30 and 20 in
  earlier seasons), and no export. PFF's route grades need a subscription export the drive does not hold.
- **The structural point:** a metric that needs volume before it exists cannot flag the man who has none yet, which
  is exactly the man a stash or an early claim is about.

---

## 5. The stash in better words (A9), and the other shapes (E5)

**A stash is a bet on a job, not a player. It pays when four numbers line up, against what the roster spot would
otherwise earn:**
1. **How big the job is:** what the lead back's work scores (`job_pays` in `inherit_2026.csv`).
2. **How likely the job opens in the weeks that matter:** the starter's fragility (A1 and B4 re-test the flat 0.46).
3. **How much of the job he inherits: the clear path.** Measured below, readable before the injury.
4. **Whether he produces with it:** usage and points in the first game (section 3), pedigree as a tiebreak.
Against: the seat's alternative use (doc 240's method; the sheet's seat price).

**T5. POPULATION:** every team-season 2019-2025 where the RB snap leader to date (two or more games) missed a game
in weeks 3-15; the first game of each absence only. **PREDICTOR:** the number-two back's share of all non-leader RB
snaps to date. **OUTCOME:** his half-PPR points that game at or above 9.92, his share of the room's RB snaps, and
whether he led the room.

| his share of the backup snaps before | n | his share of the room that game | led the room | median points | at the bar |
|---|---|---|---|---|---|
| under 50% | 28 | 22% | 32% | 3.7 | 25.0% |
| 50-70% | 57 | 50% | 65% | 6.5 | 31.6% |
| 70-85% | 35 | 56% | 74% | 9.1 | 45.7% |
| **85%+** | **34** | **71%** | **88%** | **15.5** | **64.7%** |

70%+ against under: **55.1% vs 29.4%, p=0.0017**; rho with his points +0.39, with his room share +0.41 (both
p<0.0001). The earlier seasons alone (2019-2021, n=80) point the same way: 48.6% vs 28.9%, p=0.10; rho +0.51 with room
share. The outcome is one game; the whole absence is NOT YET RUN.
**So the logic, in one sentence:** hold the back who already takes most of the backup work behind a big job whose
holder is fragile, and treat a backup who shares that work as half the bet he looks like.

**The other stash shapes, with their status:**

| shape | status |
|---|---|
| the handcuff with a clear path | TESTED here (T5) |
| a committee back already at 35%+ who reaches the snap line | TESTED here (T4): 17-30% by tier |
| a first-round rookie receiver behind a veteran | section 4.28 of the directive, 9 of 15; under re-check (B7) |
| a young receiver with three signals | section 4.30; under re-check (B6, F2) |
| a veteran arrival squeezing the room below him | NOT YET RUN (F1) |
| an absence that opens an alignment, not a rank | NOT YET RUN (F3) |
| a coach cutting a role after a fumble or drops | NOT YET RUN (G2) |
| **a quarterback change moving the target tree** | **NOT YET RUN, new (E5).** nflverse play-by-play: the new passer's prior target shares by alignment and depth |
| **a trade or release that opens a job without an injury** | **NOT YET RUN, new (E5).** T5's clear-path measure on events found in weekly rosters |
| **a hurt starter parked on IR until he returns** | **NOT YET RUN, new (E5).** Return-to-role rate after four or more weeks out: nflverse injuries plus snaps. A12 covers the seat |
| a defence held for a schedule | measured (doc 258, directive section 4.33) |
| a tight end for the December draw | OPEN (C4) |

---

## 6. What shipped today, and why ahead of batch 1's second half

**One file, because this week is the one that binds.** Claims filed after week 1 settle Thursday 17 Sept: the first
waiver run with any usage in it, and the week the league's own claims have paid best so far (directive section 4.31,
under re-check as catalog B3).
Before today a free player off the board with a week-1 role reached the Tuesday read only as one of 30 names.

- `wire.py` now writes **`Source\FREE_UNRANKED_<date>.csv`**: asof, espn_id, player, pos, team, owned_pct, status,
  for every free skill player the board never rated. A header with no rows means nobody. The write is guarded and
  cannot stop the wire. The name cannot match `WIRE_*.csv`, which `sheet_engine.py` and `build_inherit.py` glob for.
  Nothing on either page changed.
- **A latent crash, found while building the control and fixed:** a player sent by ESPN with no ownership number
  killed the whole run in the live code (`round(None)` on the ownership read; no page would have been written). Not
  seen in a live run; both reads now default to 0.0. **`wire.py` 79,387 bytes; `check_kit.py` re-pinned.**
- **Negative controls C16** in `research\redteam\redteam_controls.py`: a planted undrafted back the board never rated,
  and a player with no ownership number off the board and on it. **39 of 39 on the new code.** On the live 291 code
  the three file checks fail and the harness dies on the board player with no ownership number (35 passed before it);
  the pre-291 code passed 11 before the same crash. The two checks that pass everywhere (no `WIRE_*` glob collision,
  the page still names the planted back) guard against regressions.
- **The Tuesday read's prompt gains the usage lane and the clear-path check** (section 7). Pedigree ranks there and
  never filters.

**Not shipped, and why:** the lane on the page itself, because stacking a page change on batch 1's unverified rebuild
would blur which change broke what; the 400 cut (A13), because it cannot be tested from the cloud without ESPN.

---

## 7. The step added to the Tuesday read

> **2b. THE USAGE LANE (doc 292): nobody is filtered on pedigree.** Download nflverse `snap_counts_2026.csv` and
> `roster_weekly_2026.csv` (github.com/nflverse/nflverse-data releases `snap_counts` and `weekly_rosters`); state the
> latest week in each before using it, and say BLOCKED in one line if the download fails. For every RB, WR and TE
> whose offensive snap share in the latest week reached the starter line (RB 50%, WR 65%, TE 60%), join `pfr_id` to
> `espn_id` through the roster file and keep the ones free in this league: in `WIRE_<today>.csv` or
> `FREE_UNRANKED_<today>.csv`, not on `MY_ROSTER.csv`. For each: snap share that week and his average before it (under
> 35% = a spike, 35%+ = already in the rotation; in week 1 there is no before, so say so); his half-PPR points that
> week against RB 9.92, WR 9.62, TE 8.25; NFL draft round or undrafted. Rank snaps-and-points first, then rotation
> players at the snap line, then spikes, and weight backs above receivers. Context from 2019-2025, weeks 3-13, never a
> claim rule: snaps and points became a startable four games 26% of the time, snaps alone 16%, an undrafted spike 5.5%
> against 14.8% drafted, and an undrafted player already in the rotation 17.8% against 22.2%. Rates were measured from
> week 3 on; a week-1 or week-2 flag sits outside them. **The clear path:** for Mike Washington Jr. and for every free
> `next_man` in `inherit_2026.csv`, his share of his team's backup RB snaps so far (85%+ of them scored like a starter
> in 65% of first games the lead back missed; under 70%, 29%). One game of snaps is thin; say so.

---

## 8. Scripts and inputs

In `Scripts\research\`, each taking `--years 2019,2020,...` (default 2022-2025): `emergence_by_tier.py` (T1) ·
`emergence_lead.py` (T3, 2022-2025) · `usage_jump_by_tier.py` (T2; `--strict` is the definition quoted) ·
`lane_precision.py` (T4) · `clear_path.py` (T5) · `efficiency_check.py` (T6).
**Inputs, nflverse releases in the folder they run from, nothing else read:** `player_stats_2018..2024.csv` and
`stats_player_week_2025.csv` · `roster_weekly_2018..2025.csv` · `snap_counts_2018..2025.csv` ·
`advstats_week_rush_2019..2025.csv` and `advstats_week_rec_2019..2025.csv` · `draft_picks_all.csv` (release
`draft_picks`, file `draft_picks.csv`). Snap rows join to the stats by `pfr_id` through the weekly rosters at 89-91%;
the unjoined rows are dropped and each script prints the count on its first line.

---

## 9. Open threads from this doc

- **E4:** does the lane name the beneficiary before a rival in this league adds him (this league's add log against the
  flag week). NOT YET RUN.
- **T5 over the whole absence**, not only its first game. NOT YET RUN.
- **B11's two cells** (receiver broken tackles, tight-end yards a target, both conditional on scoring): re-test on
  2026 at season's end.
- **E5's three new shapes:** quarterback change, trade or release, IR return. NOT YET RUN.
- **A17's page lane:** after batch 1's rebuilt pages verify.
- **`AUDIT_LEDGER.md` row 19:** section 4.6 of the directive. Lands in the one directive pass after the catalog.
