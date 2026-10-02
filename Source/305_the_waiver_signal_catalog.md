# 305 -- the waiver signal catalog, weighted, and the two blockers that are already dead

**13 September 2026, Sunday night, week 1 complete.** Matt asked for three things: the week-by-week
waiver timing restated, a catalog of every signal we have with weights on it, and a red team of that
catalog. Plus his podcast idea, which he says he has forgotten my answer to. **The answer he forgot
is that the project half-built it a month ago and then declared it blocked on a file I am holding
right now.**

---

## 1. THE TIMING, AND HIS RECOLLECTION IS BACKWARDS IN THE HALF THAT MATTERS

He wrote: *"what I recall is that weeks one and two provide the most valuable waiver wire pickups.
And I believe you mentioned some Weeks later in the season."*

**WEEK 1 IS THE WORST WEEK OF THE YEAR. WEEK 2 IS THE BEST. AND THERE ARE NO SPECIAL WEEKS LATER.**
§4.31, doc 252. **POPULATION, restated because it is inherited (0.6): every executed add in this
league 2022-2025 that matched a QB/RB/WR/TE weekly line, n=718 in weeks 1-14. That is 58% of the
1,230 executed adds; 248 of them are D/ST and are NOT in this table.** BASELINE: points per game
from the add week onward reaching the position's replacement rate. Outcome B removes the
shrinking-window confound by scoring only the next four weeks.

| add week | n | rest of season | **next four weeks** |
|---|---|---|---|
| **1** | 32 | 12.5% | **9.4%** |
| **2** | 52 | 26.9% | **34.6%** |
| 3 | 52 | 17.3% | 15.4% |
| 4 | 50 | 24.0% | 26.0% |
| 5-8 | 247 | 19.8% | 25.1% |
| 9-14 | 285 | 22.1% | 21.4% |

**The rate is FLAT: rho(week, hit) = +0.003, p=0.926 on the four-week outcome. Weeks 2-4 against
9-14 is 22.7% against 22.1%, p=0.905.** The single real result is week 1 at **9.4% against week 2's
34.6%, Fisher p=0.010**. Why: a week-1 claim bets on a depth chart nobody has tested; a week-2 claim
bets on a snap count.

**THE OPERATIONAL FACT, AND IT IS TONIGHT'S HEADLINE: the claim he files now processes as a WEEK-2
ADD. He is sitting on the best measured week of the season, once.**

**AND THE THING THAT DOES CHANGE ACROSS THE SEASON IS THE POOL, NOT THE RATE.** Same doc:
free-and-usable players fall from 13.8 / 16.8 / 15.5 in weeks 1 / 2 / 5 to 10.0 / 10.0 / 9.8 in
weeks 9 / 11 / 12. **Free STARTABLE running backs go 3.5 in week 2 to 0.8 in weeks 7 and 9. In half
the league-weeks after week 6 there was not one startable back on the wire.** But the ceiling does
not fall: the best free player is worth 22-26 a game in nearly every week. **There are fewer of
them; they are not worse.** So the hit rate is flat and the barrel still thins, and both are true.

---

## 2. THE CATALOG, TIERED BY WHAT THE MEASUREMENT WILL BEAR

Ranked by effect size against reliability. **Every row carries its own population, because a signal
quoted without one is how this project got doc 228.**

### TIER 1 -- act on these

| signal | number | population | what it cannot do |
|---|---|---|---|
| **Week-1 backfield share** (docs 300, 303) | claimable RB2 at 35%+ of week-1 RB work: **64% startable**, n=114, **p=0.0008**. Spearman(share, ppg) **+0.464** | team-seasons 2021-2025, both backs played wk1, RB2 in 4+ of wks 2-14, restricted to backs who were NOT startable the prior season | **The payoff IS the takeover.** Where the man ahead stayed the lead back the top band is 27% and not separated (p=0.256). It MULTIPLIES the job-opens term, never replaces it |
| **The receiver composite, 3 of 3** (§4.30, doc 248) | **39.4% against an 11.4% base**, p=0.0000. Two signals is 7.1%, so it is a factor of five, not a sum | WR seasons 2021-2024, years 1-3, not startable, 4+ games, played 4+ again next season. n=33 in the cell | It is a **next-season** screen. The shipping constants warn on its face not to put it on the weekly sheet |
| **First-round rookie receiver displacement** (§4.28, doc 251) | **60% displace the incumbent**, against 7.4% for everyone else. Fisher **p=0.000001**. 40% startable in year one | first-year challengers paired with a 60+-target incumbent still on the roster, n=364 | n=15 in the numerator. The size is not in doubt, the precision is |
| **Prior-season availability, the `12g` badge** (§4.22, doc 203) | played 12 or fewer games last season = **-19.4 points**, se 4.7, **p=0.00004**. All positions | n=735 player-seasons 2021-2025, controls for season, position and log(ADP) | **Close to noise on an established veteran** (doc 204): among players with three prior seasons the coefficient is +0.63, p=0.59. It is a warning on the young and unproven |
| **Claim in week 2, not week 1** (§4.31) | 34.6% against 9.4%, Fisher p=0.010 | above | Does not govern filling an EMPTY starting slot, where the alternative is zero |

### TIER 2 -- screen with these, do not lead with them

| signal | number | the catch |
|---|---|---|
| **The workload pop, not the points** (doc 235) | the workload is the thing that predicts, not the box score | it is why week 2 beats week 1 at all |
| **Wally Pipp, conditional** (§4.27, doc 244) | a back who PRODUCES in relief keeps **+12.4 pp** of the job; one who does not loses **-4.1**. Difference +16.6, p=0.006, n=40 | the unconditional average is null and +9.8 must not be quoted. And a **short** absence is more dangerous to the starter than a long one, p=0.108, suggestive only |
| **Position refill rate** (doc 12, n irreproducible per §4.17) | QB **62%** / 16.65 ppg · TE 42% / 5.53 · WR 31% / 6.54 · **RB 22%** / 5.43 | the single most decision-relevant table here, and it says **RB is the position the wire cannot fix.** Three of the four numbers are inherited from a doc the project has already declared irreproducible |
| **Buy the job, never the name** (§4.20, doc 141) | the UNSETTLED flag says the job is unresolved and worth N points. It has **no opinion on who wins it**: incumbent minus challenger +8.2, p=0.604 | the variance is the story, not the mean |
| **The 2nd receiver squeeze** (docs 299, 302, 303) | with the arrival out of the denominator: 2nd receiver **-0.031, p=0.078** | `[SUGGESTIVE]`. It was p=0.011 on four seasons and the fifth moved it. Do not write it as a finding |

### TIER 3 -- tiebreak only, never over real margin

- **D/ST matchup** (§4.33): at defence the matchup is **108%** of the spread between the units, so
  chase the schedule. At QB it is 23%, at RB 11%, at TE 5%, at **WR 2%**. Everywhere but defence,
  take the player.
- **The tight end's weeks 15-17 draw** (§4.26b): +3.39 per sd, p=0.031, n=70. One live cell out of
  ten tests, and doc 10 disagrees with it. `[OPEN]`
- **Kicker, from about week 6** (doc 272): the hot three beat three at random off the same list by
  **+1.29 a week**; at week 8 the same test is +0.23 and the interval covers zero.
- **Byes** (§4.11): worth at most 1.2 points, ever. Never moves a pick with margin behind it.

### TIER 4 -- DEAD. Stop looking here, and stop letting an analyst sell them back to us

- **"The market is sleeping on him"** (ADP rank minus projection rank): rho **-0.079**, the worst
  signal ever tested here, and its coldest quintile broke out MORE often.
- **Analyst disagreement**: controlling for ADP level it predicts finishing **WORSE, -0.244,
  p=0.0009.** The players the experts argue about do not outperform.
- **Speed.** Backwards three separate times on three different objects. A forty under 4.43 measured
  **-7.7** on the composite.
- **Weight.** +2.3, p=0.80, and PlayerProfiler calls it *"the most positive indicator of future NFL
  success."*
- **Opportunity environment / team pass volume**: 7.5% of the variance, and close to unforecastable.
- **Vacated target share, on the MEAN**: null. The TAIL is real and is a different claim.
- **Offensive line**: null for backs, underpowered for quarterbacks.
- **Year-two bounce-back**: null, and the discount unwinds after one healthy season.

---

## 3. RED TEAM OF MY OWN CATALOG

1. **Almost everything above was measured on a SEASON outcome, and a waiver claim is a WEEK
   decision.** Doc 253 already caught me misapplying §4.31 within an hour of writing it. The 64%
   and the 39.4% are "did he become a season asset", not "should I claim him Tuesday". **Treat
   tier 1 as a screen on who is worth a roster spot, and the lineup arithmetic as what decides the
   claim.**
2. **The decisive cells are small.** n=33 on the composite, n=15 on the rookie rate, n=40 on Wally
   Pipp, n=14 in the claimable top band. None of these are stable to a season.
3. **Three of the four refill rates come from doc 12, which §4.17 re-tagged `[SOURCED, n
   irreproducible]`.** Only the QB number was re-derived. That table is doing more work in my
   reasoning than its provenance supports.
4. **Nothing in this project computes a ceiling** (§4.13d), so every "upside" call is a human
   judgement on a near-tie with no metric behind it. Say so rather than dressing it.
5. **The catalog is a list, not a model.** He asked how to STACK them and the honest answer is that
   only one stack has ever been measured: §4.30's 0 / 5.0 / 7.1 / 39.4. Everywhere else the
   interaction is null with a wide interval, and doc 191's one significant interaction is
   **NEGATIVE** (target share by availability at RB, -36.0, p=0.031). **Do not assume additivity
   and do not assume compounding. Measure the cell.**

---

## 4. THE TWO BLOCKERS THAT ARE ALREADY DEAD, INCLUDING HIS PODCAST IDEA

**HIS PODCAST QUESTION, ANSWERED: the project built the corpus and then stopped one file short.**
`Source\analyst_calls_joined.csv` holds **180 dated analyst calls** transcribed from podcasts, and
doc 30 lists the shows, including the FantasyPros 2024 and 2025 episodes in matching format. Doc 35
states the falsifier in terms:

> *"the corpus contains dated 2024 and 2025 calls. Scoring those against actuals already in the
> project would convert this from agreement to measured hit rate. **It is currently blocked on 2024
> player-level actuals, which the project does not have.**"*

**I am holding `stats_player_week_2024.csv` right now: 18,130 rows, 18 weeks, 1,997 players.** The
blocker is false and has been since nflverse's `stats_player` release was found. **So the direct
test Matt is describing -- which analyst calls actually hit -- is NOT YET RUN, not blocked.**

**Two honest caveats before anyone gets excited.** Doc 35 records that **episode dates are absent by
design and not recoverable from the transcripts**, which matters because an undated call cannot be
scored against what was knowable when it was made. For a preseason sleeper episode the date is
roughly known and the outcome is the season, so those are scoreable; an in-season waiver take is
not, without the date. And doc 35's own warning stands: transcription noise is material and 30 name
aliases were mapped by hand.

**The second dead blocker:** §4.30's slot rate and targets per route run were listed as blocked on
PFF fields. `pff_receiving_2022-2025.csv` have been on the drive since 10 Sept.

**Still genuinely blocked, input named:** Breakout Age and College Dominator Rating need a college
receiving table nflverse does not carry. `draft_picks.csv` holds a `cfb_player_id`, so the join key
exists and LevelUpFantasy and PFF both publish the data.

---

## 5. WHAT THE PAGE STILL CANNOT SEE

* The week-1 backfield share is not in the seat price. `AUDIT_LEDGER` row 29. It put the measured
  name third tonight.
* No injury and no expected duration on any row. `injuries_2026.csv` is now on the drive and covers
  12 of the 59 non-active men on the wire, so it is a partial join and must say so.
* `build_pedigree.py` still screens the BOARD, not the free pool. Ledger row 26. That is how Jayden
  Higgins was invisible.
* No NFL round or overall pick on the board, so a first-round rookie receiver reads as a blob row.

## 6. OPEN THREADS FROM THIS DOC

* **NOT YET RUN:** the analyst hit-rate test. 180 calls against 2021-2025 actuals, scored on the
  preseason subset where the year is known. The blocker doc 35 named is gone.
* **NOT YET RUN:** the concentration test Matt asked for -- for starters drafted rounds 1-4,
  2021-2025, the manager's actual lineup loss in the weeks that player missed, QB and TE against
  RB and WR.
* **NOT YET RUN:** slot rate and targets per route run added to the composite, from the PFF files.
* **NOT YET RUN:** every table in docs 302 and 303 on the full 32-team week-1 slate.
