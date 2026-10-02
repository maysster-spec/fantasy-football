# 293 · The late pick needs a door: how low-drafted players became starters, 2015-2025

*11 Sept 2026, 2:30 pm ET (stamp corrected by doc 294; it first read 4 pm). In-season red team, catalog item E6 (new). Every result states its population, outcome and
n. Scripts in `Scripts\research\late_picks\` (section 9), run on nflverse files in the folder they run from.*

**Matt, 11 Sept, verbatim:** *"Chubba Hubbard wasn't drafted until the 4th round of the NFL draft but became a
starter. That is a good example because examples can help us understand the underlying indicators that led to that
development of him becoming a starter. Research his example, other lower drafted players that became relevant and
those signals should be easier to parse because petagree no longer drowns out the other signals. difficulty for me
is that I can't easily remember to give you more examples. instead you'll need to research on your own. plus you can
develop your own research plan that is better than my rough idea."*

**The testable forms, stated before any result.** (1) Among players drafted in rounds 4-7 or undrafted, some signals
knowable beforehand separate the ones who became starters from the ones who had the same chance and did not.
(2) Matt's claim, sharpened: those signals read MORE clearly for late picks than for early ones, because a team
gives an early pick the job on his draft slot and a late pick has to earn it. Measured as the interaction between
each signal and pedigree. Direction in both: his.

---

## 0. What changed

1. **The design, first.** A list of success stories shows what the winners had, not what separated them from the
   many late picks who had the same chance and faded. So every test here compares risers with everyone who had the
   same opening. Hubbard is the worked example; the population is the evidence.
2. **Late picks need a door.** Of 404 low-pedigree risers 2015-2025, **38% rose because someone ahead of them was out**
   (hurt, cut, benched, or missing during the stretch), against 22% of 390 early picks. Given the same injury opening,
   late picks rose 10.8% of the time against 20.2%; with nobody hurt, **7.0% against 20.6%**. `[TESTED]`
3. **Three signals name the late pick who takes the job, and they stack.** Among backups in a rotation with nobody
   hurt ahead: **(a) his snap share over his last two games above his position's typical rotation share, (b) his
   points per snap above typical, (c) a light special-teams load.** With all three, **a late pick took the role 36%
   of the time (29 of 81), level with an early pick's 38% (43 of 112, p=0.76)**. With one or none: 8.5% (40 of 472).
   It holds in both eras (2015-2019: 49% against 14%; 2020-2025: 25% against 12%). `[TESTED; signals chosen on this
   population, era split and the absence openings are the checks]`
4. **Matt's sharper claim, that signals read more clearly for late picks, is not supported as stated.** No signal's
   effect is measurably larger for late picks; the interaction terms sit between z -2.0 and +2.3, the only two beyond
   plus or minus 1.4 point in opposite directions, and most lean negative.
   What IS true is the cleaner version: **once the three signals are present, the pedigree gap in winning the job
   disappears.** Pedigree still matters for turning the job into points (all three: 18.5% against 31.2%, p=0.066).
5. **Efficiency is not the door.** Being more efficient than the struggling starter (Hubbard 2023's shape) leaned his
   way and did not resolve: took the role 19.8% against 13.3% (p=0.089). Yards per play did slightly better for late
   picks (20.8% against 13.8%, p=0.047). The team's own usage, and whether it keeps him off the coverage units, say
   more than the efficiency numbers do. `[TESTED]`
6. **Hubbard's own path, from the data:** a rookie who inherited volume when McCaffrey was hurt (2021), a role flip
   from a paid veteran averaging 3.1 yards a carry (2023), a full season as the lead (2024), and then the same thing done
   to him: an undrafted back's two-game cameo took his job (2025). Section 2.

---

## 1. The research plan (and why it is not "collect more examples")

**The flaw in examples:** Hubbard, Jaylen Warren, Tony Pollard and Puka Nacua all had things in common. So did
hundreds of late picks who never started. Traits read off winners are survivorship until they are checked against the
players who had the same chance. **So the unit is the chance, not the player:** every time a late pick got an opening,
did he take it, and what did we know beforehand?

| batch | question | status |
|---|---|---|
| **R1** | how each riser's role opened, by pedigree; which signals separate risers from non-risers after an absence and in a rotation with nobody hurt; the pedigree interaction; the Hubbard file | **DONE today** |
| R2a | the preseason route: 125 late picks were startable from week 1 (Nacua 2023, Kyren Williams 2023, James Robinson 2020). Signals: depth chart, camp news, the money committed to the man ahead | NOT YET RUN. Inputs: nflverse depth charts (weekly, to 2024); OverTheCap contracts (nflverse `contracts` release); our preseason pulls 2022-2026 |
| R2b | the words before the flip: coach quotes and beat reports for every "overtook" or "grew beside" riser, dated, against the same number of non-risers | NOT YET RUN. Joins catalog G1's quote log |
| R2c | does a late pick KEEP the role when the man ahead returns, by pedigree (Dowdle 2025 kept it; directive section 4.27's RB result, split by draft tier) | NOT YET RUN. Data on hand |
| R2d | coaching changes and trades as openers | BLOCKED as run today: `nfldata/games.csv` (head coach per game) is not reachable from this session; nflverse play-by-play carries coach names and is downloadable. Trades: nflverse `trades` |
| R3 | apply the three signals weekly to free players | **LANDED in the Tuesday read's prompt today** (section 8) |

**Top recommendation for the next batch: R2c.** It decides whether a late pick's cameo is worth a claim that lasts, and
it runs on data already downloaded.

---

## 2. Chuba Hubbard, from the data

**Draft:** 2021, round 4, pick 126, Carolina, Oklahoma State (nflverse `draft_picks`).

| season | what happened (Carolina RB snap share, nflverse) | how the role opened | the signals beforehand |
|---|---|---|---|
| 2021 | McCaffrey 89/71% in weeks 1-2, hurt in week 3 (30%); Hubbard 55, 47, 65, 65, 53, 55% in weeks 3-8, 11.3 half-PPR a game on 3.81 yards a carry and -0.12 EPA a carry | the starter hurt in game | a rookie with a 58% special-teams share and poor efficiency: **volume, not talent signals** |
| 2022 | McCaffrey traded after week 6; D'Onta Foreman led most weeks (up to 68%) with Hubbard at 18-69%; Hubbard 4.85 yards a carry against Foreman's 4.59 on half the carries | the man ahead gone | committee, not a flip |
| 2023 | Miles Sanders (paid veteran) led 57-65% in weeks 1-3 on **3.11 yards a carry, -0.34 EPA a carry**; Hubbard 36, 37, 34, then **54, 48%** in weeks 4-5 on 4.40 and +0.02; Sanders out in week 6 (Hubbard 77%, 15.5 points); **Hubbard led every week after Sanders returned**; the points came from week 10 | a failing incumbent, then a one-week cameo | snap share creeping up two weeks before the cameo; a clear efficiency gap; **one of the three signals** (his share, not his points per snap or special-teams load) |
| 2024 | Hubbard 54-97% all season, 14.7 half-PPR a game | already led | none needed |
| 2025 | Rico Dowdle (undrafted) behind him weeks 1-4 on 2.96 yards a carry; Hubbard out weeks 5-6; **Dowdle 7.34 yards a carry and 31.4 points a game in the two games**; Dowdle led weeks 9-12 at 65-82% | the cameo flipped it, against Hubbard | the cameo, not anything before it |

**Dated sources, pages loaded:** CBS Sports, Cody Benjamin, **3 Nov 2023**: Hubbard stays the starter for week 9; Sanders
"averaging just 3.0 yards per carry on the year", with multiple injuries, and Reich said Sanders ran a wrong route in
week 8. NFL.com, Kevin Patra, **undated on the page** (its content places it after week 8 of 2025): Dave Canales, *"We
cannot ignore that Rico has been exceptional in a couple of games, and then in the opportunities he's had over the last
two weeks."* Dowdle had 473 scrimmage yards in the two games Hubbard missed.

**What the example suggested, and what the population then said:** creeping snaps (supported: the strongest signal),
the failing incumbent and the efficiency gap (leaned his way, not resolved), the cameo (directive 4.27 already measures
it for backs; R2c splits it by pedigree).

---

## 3. How 794 risers' roles opened (T1)

**POPULATION:** RB/WR/TE player-seasons 2015-2025 not established last season (6+ games at or above the bar).
**RISER:** the first four straight games played averaging at or above the bar (half-PPR a game: RB 9.92, WR 9.62,
TE 8.25), starting week 2 or later, after averaging under it in any earlier games. **HOW IT OPENED**, at the first game
of the stretch, against the man ahead by snaps (WR: the top three).

| how it opened | rounds 1-3 (390) | rounds 4-7 and undrafted (404) |
|---|---|---|
| already had the most snaps; the points caught up | 57.2% | 41.8% |
| the man ahead out injured beforehand | 6.7% | 12.1% |
| the man ahead hurt during the first game | 2.1% | 5.0% |
| the man ahead cut or traded | 1.0% | 1.7% |
| the man ahead a healthy scratch | 1.0% | 2.0% |
| the man ahead out, no recorded reason | 0.5% | 1.2% |
| the man ahead missed a later game of the four | 10.8% | 16.3% |
| **any absence of the man ahead** | **22.1%** | **38.3%** |
| overtook him while he played | 7.4% | 7.2% |
| scored beside him while still behind in snaps | 13.1% | 12.6% |

Mix, low against high: chi-square p=0.0006. **At running back it is starkest: 90 of 164 late-pick risers (55%) came
through an absence ahead of them, against 35 of 110 early picks (32%)**, and only 20 of the 164 already led.
**Not in this table:** 342 players were startable from week 1 without being established the year before, 125 of them
late picks (Mostert 2023, Kyren Williams 2023, Nacua 2023, Jordan Mason 2024, James Robinson 2020). That route is won in
the preseason and is R2a.

---

## 4. Part A: the man ahead misses a game (T2)

**POPULATION:** the first game a position's snap leader to date missed (RB, TE: the leader; WR: any of the top three),
weeks 3-15, 2015-2025; the candidate is the next man by snaps (number two, or the fourth receiver), not established; one
row per candidate-season, **n=826**. **OUTCOME:** four games at the bar starting that game or the next.

| | risers |
|---|---|
| all | 115 of 826, 13.9% |
| rounds 1-3 / late picks | 20.2% (272) / 10.8% (554) |
| RB early / late | 38.3% (60) / 29.1% (127) |
| TE early / late | 25.4% (59) / 6.2% (128) |
| WR early / late | 11.1% (153) / 5.0% (299) |

**Signals, split at the median inside each position** (a back's EPA a carry and a receiver's EPA a target live on
different scales; the first run pooled them and read efficiency backwards, so every signal is scaled within position):
- **snap share over the last two games:** late picks 15.3% against 7.0% (p=0.002); early 26.3% against 12.5% (p=0.006)
- snap share this season: late 12.2% against 9.7% (p=0.41); early 25.1% against 12.4% (p=0.013)
- share of the backup snaps, RB and TE (the clear path, doc 292): late 21.1% against 14.2% (p=0.19); early 39.7% against
  24.6% (p=0.12)
- EPA a play, this season and last: late 14.7% against 9.6% (p=0.13); early n.s.
- the EPA gap over the leader, the leader's own EPA, a relief game already on record, years in the league, special teams:
  none resolved in either group
**Interaction (signal x late pick, pooled logistic with position):** every term between z -1.4 and +0.8. No signal reads
more clearly for late picks after an absence.

---

## 5. Part B: nobody is hurt, a backup is in the rotation (T3)

**POPULATION:** the first week (4-14) a non-established player's snap share over his last two games sat in the rotation
band (RB 20-49%, TE 25-59%, WR 30-64%) while he was not the leader (WR: not top three) and every leader played the game
before; one row per player-season. **Clean rows** drop the 649 where a leader missed a game in the next four (those are
Part A): **n=1,131**. **OUTCOMES:** (1) rose: four games at the bar starting within the next four; (2) **took the role:
out-snapped the leader in two of the next four games in which the leader played.**

| | rose | took the role |
|---|---|---|
| early picks (344) | 20.6% | 27.3% |
| late picks (787) | 7.0% | 15.1% |

**Late picks, split at the median inside each position** (took the role, then rose):
- snap share over the last two games: took 21.9% against 9.7% (p<0.001); rose 8.2% against 6.0% (p=0.26)
- **points per snap this season:** took 19.2% against 11.6% (p=0.004); rose 10.4% against 4.0% (p=0.001)
- **special-teams share:** took **10.4% above against 22.2% at or below** (p<0.001); rose 4.5% against 10.8% (p=0.001)
- yards per play: took 20.8% against 13.8% (p=0.047); rose n.s.
- the EPA gap over the leader: took 19.8% against 13.3% (p=0.089); rose 11.3% against 7.1% (p=0.18)
- the leader's own EPA a play (a failing starter): took 11.4% when the leader was efficient against 16.9% (p=0.051)
- years in the league: n.s.
**For early picks** the same three signals point the same way; points per snap and yards per play do not separate early
picks who took the role (28.0% against 26.4%; 32.5% against 28.8%).
**Interaction:** extra effect in late picks between z -2.02 (points per snap, on rose) and +2.27 (snap trend, on took);
the rest inside plus or minus 1.4. Mostly null, leaning weaker for late picks on log-odds.

**The three signals together** (last-two-games share above, points per snap above, special-teams share at or below the
position median among rotation backups; medians RB 28% / 0.254 / 18%, TE 36% / 0.055 / 27%, WR 38% / 0.122 / 13%):

| signals | late picks took the role | early picks took the role | late picks rose | early picks rose |
|---|---|---|---|---|
| none | 10/150 = 6.7% | 4/24 = 16.7% | 2/150 = 1.3% | 0/24 |
| one | 30/322 = 9.3% | 12/92 = 13.0% | 20/322 = 6.2% | 10/92 = 10.9% |
| two | 50/234 = 21.4% | 35/116 = 30.2% | 18/234 = 7.7% | 26/116 = 22.4% |
| **all three** | **29/81 = 35.8%** | **43/112 = 38.4%** (p=0.76) | **15/81 = 18.5%** | **35/112 = 31.2%** (p=0.066) |

**Checks, because the three were chosen on these rows:** late picks taking the role with all three, 2015-2019 18 of 37
(49%) against 46 of 322 (14%), p<0.0001; 2020-2025 11 of 44 (25%) against 44 of 384 (11.5%), p=0.017. On Part A's
different event, the two signals it carries (last-two share above, special teams at or below): late picks 5.9% (0),
12.2% (1), 16.5% (both), p=0.042.
By position, late picks rising with all three against fewer: RB 7/27 against 34/260; WR 2/11 against 5/113; TE 6/43
against 1/333.
**Named rows:** Jaylen Warren 2023 week 4 (all three; rose), Tony Pollard 2022 week 4 (all three; rose), Aaron Jones
2018, Chris Carson 2018, Marlon Mack 2018 (all three; rose). **Hubbard 2023 week 4 had one** (share 36% against a 28%
median; points per snap 0.218 against 0.254; special teams 35% against 18%) plus a +0.23 EPA gap, and took the role; his
row is outside the clean set because Sanders missed week 6.

**On the special-teams signal, an inference and flagged as one:** a backup kept off the coverage units is one the staff
is saving for offense. It held in both pedigree groups and both outcomes; its mechanism is not measured here.

---

## 6. Matt's claim, verdict: PARTLY

**Confirmed:** the underlying signals exist inside the late-pick population, they stack, and when all three are present
a late pick wins the job as often as an early pick does. **Not confirmed:** that they read more clearly for late picks
in general; no signal's effect is larger there, and pedigree still shifts the odds of getting a chance (7.0% against
20.6% with nobody hurt) and of turning a job into points. **The better statement of his idea:** pedigree decides how
often a door opens; once a late pick is through it, the team's own usage tells you whether he stays.

---

## 7. Outside research, dated (loaded page)

Quinn A. W. Keefer, *"Do sunk costs affect expert decision making? Evidence from the within-game usage of NFL running
backs"*, **Empirical Economics, 2019 (online 23 Dec 2017)**: compensation, a sunk cost, *"significantly increases the
number of rushing attempts for NFL running backs"* independent of performance, an effect the paper sizes at 174 to 222
prior-season rushing yards. Rookie pay follows draft slot, so this is the mechanism behind section 5's 7.0% against 20.6%.
A second Keefer paper on salary-cap value and playing time (Journal of Sports Economics, 2017) was seen in search results
only and is not relied on.

---

## 8. What changed in the tools

- **Tuesday read (prompt, today):** for every free RB, WR and TE in the rotation band, add points per snap and
  special-teams share (both from `snap_counts_2026.csv` and the weekly stats) and count the three signals against the
  medians above. Context, not a claim rule; measured from week 4, so weeks 1-3 are outside it and the read says so.
- Nothing on either page changed. The page lane is catalog A17, batch 3.

---

## 9. Limitations, named

- **Labels are taken at the first game of the stretch.** Hubbard 2023 reads "already led" because his role flipped in
  weeks 4-6 and the points came in week 10.
- **An in-game injury** is caught only when the man ahead played under 60% of his usual share and missed the next game,
  or missed a later game of the four.
- **Supplemental-draft picks read as undrafted** (Josh Gordon 2018 appears as undrafted). Rare.
- **The join:** 62,336 snap rows by id, 7,066 by normalised name + team + season + position, 532 unjoined (0.8%; 1.5% of
  undrafted players' snaps, 0% of drafted). Advanced stats (yards after contact, broken tackles) exist from 2018 only.
- One row per player-season in each design; team-level clustering is not modelled; the interaction tests are
  underpowered for effects smaller than about a doubling of the odds.
- The three signals were chosen on Part B's late-pick rows. The era split and Part A are the checks, and both hold.

---

## 10. Scripts and inputs

`Scripts\research\late_picks\`, run in this order: `build_weekly.py` (the joined weekly table, 2014-2025) ·
`risers.py` (T1, and the week-1 group) · `openings.py` (T2) · `flips.py` (T3, both outcomes) · `combo.py` (the three
signals, era split, low against high at each count) · `hubbard.py` (section 2). Each prints its results; the tables
above were copied from a single end-to-end run on 11 Sept.
**Inputs, nflverse releases in the folder they run from:** `player_stats_2014..2024.csv`, `stats_player_week_2025.csv`,
`snap_counts_2014..2025.csv`, `roster_weekly_2014..2025.csv`, `injuries_2014..2025.csv`,
`advstats_week_rush_` and `advstats_week_rec_2018..2025.csv`, `draft_picks_all.csv`.

---

## 11. Open threads from this doc

- **R2c:** keep the role after the return, by pedigree. NOT YET RUN, data on hand. **Next.**
- **R2a:** the preseason route (125 late picks startable from week 1). NOT YET RUN; inputs named in section 1.
- **R2b:** the coach's words before a flip, against non-risers. NOT YET RUN; joins G1.
- **R2d:** coaching changes and trades. BLOCKED on `nfldata/games.csv` from this session; play-by-play is the route.
- **The special-teams signal's mechanism.** Observed in both groups; untested.
