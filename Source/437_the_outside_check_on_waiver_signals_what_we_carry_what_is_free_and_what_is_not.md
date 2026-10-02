# 437. THE OUTSIDE CHECK ON WAIVER SIGNALS: WHAT PUBLISHED PRACTICE USES, WHAT WE CARRY, WHAT IS FREE, AND WHAT IS NOT

*29 Sept 2026, Fable. Matt: "can i get help from you to research other potential metrics that pertain to fantasy
football... this lack of ADOT indicates the research wasn't complete. The goal is to capture the signals we need to
get the edge over other teams in the league when evaluating player pick ups from the waiver wire." This is §0.5(c)6,
the outside batch, which doc 435 left open. Every source below says whether it was LOADED as page text or seen only
as a search SNIPPET, and its date (ERROR_PATTERNS B7). Every free path was probed by fetching the actual file on
29 Sept, not assumed. Number reserved by listing Source\ and the store (436 was the newest).*

---

## 1. DO THIS

1. **The research was not the gap. The wiring was.** Docs 227 (8 Sept), 248 (9 Sept), 263 (9 Sept) and 305 (14 Sept)
   all named air-yards share, aDOT, routes, targets per route run and slot rate; finding 4.35 (22 Sept) called
   air-yards share "the missing half of the screen". Four catalogs, one to-do item, zero columns. The cause is the
   one doc 430 named: until 25 Sept nothing held a thing I said I would do. Section 6 below is the wiring list, on
   `claude_todo.txt`, with the order.
2. **Two signals wired today, both free and live for 2026.** Air yards, aDOT, air-yards share and WOPR (this
   morning, doc 435 addendum) and **expected fantasy points under our scoring, with points over expected**
   (`xfp`, `xtd`, `fp_oe`, `xfp_g`), from ffverse's ffopportunity model. Both are in `form_2026.csv` and on every
   wire row. Neither is on a page yet and neither is in the screen's signal count: that needs the tests in section 6.
3. **The one signal published practice leans on that we cannot get free and live is routes run** (route
   participation, TPRR, YPRR). NFL Next Gen's route model is not public; FTN's participation data reaches nflverse
   only after each season (2024 and 2025 are up, 2026 will not be until February); PFF and Fantasy Points Data sell
   it. **Do not buy yet.** The historical files let me test whether pass-play participation beats snap share for
   OUR claim population; if it does by a margin worth money, that is the moment to price a subscription.
4. **Read the "role paid less than it should" column with care.** In three games Pickens is 14 points under his
   expected line, Malik Washington 11 under, Jeanty 17 under; Tucker is 8 over, Adams 13 over. Published practice
   (Sharp Football, June 2026) treats that as regression fuel and says case by case; our own doc 193 measured the
   draft-era version null because the market prices it. On the wire it is a screen for a man whose usage is real
   and whose points are not, which is the exact lane 4.30 and 4.35 fish in. Test before trusting: section 6, item 1.
5. **Nothing for you to run.** The form file on the drive carries every column above through week 3.

---

## 2. WHAT PUBLISHED PRACTICE USES, AND THE EVIDENCE BEHIND EACH

| signal | who says so, date, how read | what they claim |
|---|---|---|
| snap share, route participation, target share as a sequence | Football Nation, "Snap Share vs Route Participation", 14 Aug 2026, updated 1 Sept 2026, LOADED | "snap share tells you presence, route participation tells you access, and target share tells you whether the quarterback used that access." Route data from "the NFL's Next Gen Stats route-recognition model". No thresholds, no numbers |
| targets per route run | Fantasy Footballers, TPRR 2026 Season Preview, 8 Sept 2026, LOADED | "TPRR does not predict the future. It is a backward-looking stat"; 30%+ elite, 25 to 30 excellent, 20 to 25 fantasy-relevant, under 20 "requires deeper investigation"; source of routes not named |
| expected fantasy points and points over expected | Sharp Football Analysis, "Expected Fantasy Points Explained", 25 June 2026, LOADED | priced by "location, down, distance, air yards, etc." against league-average outcomes; "it can undersell elite players"; use "on a player-by-player basis". No correlation numbers published. ESPN's 2025 xFP leaderboards and Fantasy Points' Everything Report: SNIPPETS only |
| the model behind the free xFP file | ffverse ffopportunity README, LOADED (undated) | "xgboost and tidymodels trained on public nflverse data from 2006-2020", weekly automated releases in csv; **no validation numbers published**, which is why item 1 in section 6 exists |
| WOPR | Action Network, LOADED, undated; formula credited to Josh Hermsmeyer | 1.5 x target share + 0.7 x air-yards share; "there isn't a direct correlation between WOPR and fantasy success". Our own 4.35 measured it: top fifth spikes 10% against 4% |
| high-leverage RB touches | Footballguys, "High-Leverage Opportunities, Running Backs, Week 3", 22 Sept 2026, LOADED to the paywall | "Targets and goal-line carries are the lifeblood of quality fantasy production for the running back position"; source not named |
| a public waiver tool's inputs | seampm/waiverwire on GitHub, 2026, LOADED | target share, rush share, touch trends, snap share, from nflverse pbp and snap counts. Nothing we do not carry |
| high-value touches, goal-line index | RotoBaller 2026, EdgeLine 2026 | SNIPPETS only, not loaded; named so nobody re-suggests them as verified |

The pattern across all of it: **opportunity first (snaps, routes, targets, air yards, red-zone touches), then an
expected-points translation of that opportunity, then efficiency only as a tiebreak.** That is the order 4.5, 4.6,
4.30 and 4.35 already put things in. The two pieces we were missing were the air-yards half of opportunity and the
expected-points translation. Routes we cannot have live.

---

## 3. THE CATALOG: EVERY SIGNAL AGAINST WHAT WE CARRY AND WHAT IS FREE

"Free for 2026" means the file was fetched on 29 Sept and its header read; "no" means I looked and it is not there.

### Opportunity, the leading indicators

| signal | free for 2026, where | carried? | verdict |
|---|---|---|---|
| snap share | nflverse `snap_counts`, four times a day | yes, `form_2026.csv` | keep |
| snap count and team plays | same feed; `snaps_2026.py` | container only, not scheduled | freshness read only (doc 434 measured share beats count); on Matt's Monday line |
| targets, target share | nflverse `stats_player` nightly | yes | keep |
| air yards, aDOT, air-yards share, WOPR | same feed, `receiving_air_yards` | **yes since 29 Sept** | threshold test open (section 6, item 2); aDOT alone was null on doc 248's 45-row test, so it is a descriptor until measured |
| expected fantasy points, points over expected | ffverse `ep_weekly_2026.csv`, nightly, one night behind on Monday games | **yes since 29 Sept**: `xfp`, `xtd`, `fp_oe`, `xfp_g` | backtest open (section 6, item 1). Their scoring is full PPR and 4-point passing TD; converted to ours. `fp_oe` blank at QB because `half_ppr` scores no passing (doc 375, now closed) |
| RB opportunity share, carries plus targets over the team's | derivable from columns we hold | not as one number | derive when the seat lane reads it; trivial |
| red-zone and goal-line usage: carries inside the 10 and 5, targets inside the 20, end-zone targets | nflverse `pbp` 2026, nightly, `yardline_100` and `air_yards` | **no**: we hold 2024 and 2025 season files only | wire from pbp (section 6, item 3). 4.5: red-zone volume is sticky; doc 193: the draft market already prices it, so on the wire it is a role read, not an edge on its own |
| route participation, routes run, TPRR, YPRR | **none live**. NGS route model not public; FTN participation via nflverse for 2023 to 2025 only, after each season; PFF and Fantasy Points Data are paid | no | historical test on 2023 to 2025 participation (section 6, item 5); buy nothing until it is run |
| daily depth chart, timestamped | nflverse `depth_charts` 2026, daily 07:00 UTC, 55 MB | **no**: `depth_map.csv` is the 8 Aug chart | replace the source (section 6, item 4); the seat lane's "man ahead" reads a chart seven weeks old |
| practice status Wed to Fri (DNP, limited, full) | nflverse `injuries` 2026, daily 07:00 UTC, `practice_status` | partly: the ESPN feed carries game status, not practice | the Wednesday-night signal for the man ahead (section 6, item 4) |
| Vegas spread and total, implied team total | nflverse `schedules` `games.csv`, every 5 minutes, `spread_line`, `total_line`, lines for future weeks | **no**: `sched_2026.csv` has no lines | the standard streaming instrument for D/ST, K and QB, and doc 421's "a season rate is not a matchup" answer (section 6, item 6) |
| team pass rate, plays, PROE in season | nflverse `stats_team_week` 2026 | no: preseason `proe_team_season.csv` only | low: 4.21 measured environment as the small half |
| rostered %, rostered change, ESPN projection | the ESPN pull | yes (doc 395 for the change) | keep |

### Efficiency, tiebreaks only (4.6: "already priced by ESPN; after-contact is a tiebreak")

| signal | free for 2026, where | carried? | verdict |
|---|---|---|---|
| YAC over expected, separation, cushion, share of intended air yards | nflverse `nextgen_stats` `ngs_receiving.csv.gz`, nightly; **qualifying receivers only, about 70 men a week** | no | low: most free men do not qualify; doc 248's 45-row separation and aDOT tests were null or suggestive |
| rush yards over expected, share of carries against 8+ in the box | `ngs_rushing.csv.gz` | no | low, same reason |
| drops, broken tackles, yards after contact | nflverse `pfr_advstats` weekly 2026 | no | low, 4.6 |
| catchable, contested, screen, play-action per target | nflverse `ftn_charting` 2026 joined to pbp | no | low; a per-target context we have never needed |

### Market

| signal | free | carried? | verdict |
|---|---|---|---|
| FantasyPros weekly rest-of-season ECR | free page | no | low: a second opinion on the projection, not a signal about the man |

---

## 4. WHY THE RESEARCH LOOKED COMPLETE AND WAS NOT

Each catalog measured the signal it could reach with the data on hand and filed the rest as NOT YET RUN or BLOCKED.
Three things then happened. The nflverse feed we already pulled carried `receiving_air_yards` and nobody read the
header past `targets` and `carries`. The free expected-points file lives on ffverse's releases, not nflverse's, and
the two 404 probes in doc 435's time (`nflverse-data/.../ff_opportunity/...`) would have said "not free" had I
stopped there; the file is at `ffverse/ffopportunity/releases/download/latest-data/ep_weekly_2026.csv`. And the
routes question was answered "PFF, blocked" (doc 248), then "in Downloads" (doc 263, last season's files), and never
"not live for this season, here is the historical test". The fix for the class is in section 6: every open signal
carries its file, its URL and its testable form, not a category.

---

## 5. WHAT SHIPPED TODAY, AND HOW IT WAS CHECKED

`research\wk1\build_form.py` fetches three files now: the weekly stats, the snap counts, and ffverse's expected
points. The join to the expected-points file is the same key as the snap join (normalised name, position, team) and
hit 920 of 929 skill rows; the nine misses are fullbacks the two feeds label differently and one two-way player.
The twelve week-3 rows with no expected line were all Chicago and Philadelphia, the Monday game the model had not
processed yet; those are blank, never zero, and `xfp_g` says how many games the sum covers. Every column that
existed before today is byte-identical to the midday build on all 4,774 rows. `wire.py` carries the three new
columns onto every row it writes; `check_kit.py` is re-pinned. Doc 375's open question, whether `build_form`
should carry a league-scored column, is closed: `xfp` is league-scored; `half_ppr` stays rushing and receiving.

---

## 6. THE WIRING LIST, IN ORDER (all mine, all on `claude_todo.txt`)

1. **The expected-points backtest.** Population: claimable RB/WR/TE player-weeks 2021 to 2025 (doc 389's
   definition, extended to backs), with ffverse's `ep_weekly_2021..2025.csv`. Outcome: startable in the next four
   weeks. Test: does `xfp` over the last two games predict it better than actual points over the same games, and
   does adding it as a fourth signal raise the three-signal screen's hit rate? Falsifier fixed now: under +2
   points of spike rate over the three-signal count, it stays a display column and never enters the sort.
2. **The air-yards threshold** (from doc 435): the WOPR cut that marks the top fifth on doc 389's population, and
   whether it lifts the screen as a fourth signal.
3. **Red-zone usage from pbp**: carries inside the 10 and 5, targets inside the 20, end-zone targets, per week and
   cumulative, into `form_2026.csv`. Test on 2021 to 2025 pbp: does red-zone share add to job worth in the seat
   lane, net of snap share?
4. **Daily depth chart and practice status** from nflverse, replacing the 8 Aug chart behind the seat lane and
   adding Wednesday-to-Friday practice status for the man ahead.
5. **Routes, historically**: from the 2023 to 2025 participation files, pass-play participation per receiver-week;
   test it against snap share on the claim population. If it beats snap share by more than the air-yards half did,
   price the paid feed then, with the number in hand.
6. **Vegas lines** from `games.csv` into the D/ST, K and QB streaming lanes: opponent implied total against
   season points allowed, 2021 to 2025 (the file carries historical lines).
7. RB opportunity share as one column; team pass rate and plays; the efficiency tiebreaks. Low.

---

## 7. SOURCES, WITH HOW EACH WAS READ

LOADED as page text: nflreadr data schedule (nflverse update cadences, undated); nflreadr `load_participation`
reference (FTN participation after each season, page updated 2023-12-19); Football Nation, 14 Aug 2026, updated
1 Sept 2026; Fantasy Footballers TPRR preview, 8 Sept 2026; Sharp Football Analysis, 25 June 2026; Footballguys,
22 Sept 2026 (paywalled past the introduction); Action Network WOPR definition (undated); ffverse ffopportunity
README (undated); seampm/waiverwire README (2026). FETCHED as files on 29 Sept: nflverse `pbp`, `stats_team`,
`snap_counts`, `injuries`, `depth_charts`, `schedules`, `pfr_advstats`, `ftn_charting`, `nextgen_stats`,
`pbp_participation` 2024 and 2025 (no 2026), `weekly_rosters`; ffverse `ep_weekly_2021` to `2026`. SNIPPETS only:
ESPN xFP leaderboards 2025, Fantasy Points Everything Report 2025, PFF YPRR pieces, RotoBaller high-value touches
2026, EdgeLine goal-line index 2026, NovaPredict opportunity leaderboards.
