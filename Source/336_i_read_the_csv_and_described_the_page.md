# 336 I READ THE CSV AND DESCRIBED THE PAGE

**2026-09-17, overnight.** Matt asked whether we score defences and said Kansas City and San
Francisco looked like good week 2 plays. Three things came out of it: a defect of mine that the
project has a named rule against, a stale number I quoted as current, and a measured disagreement
between our defence projection and ESPN's that nothing here can settle.

---

## 1. THE DEFECT, AND IT IS SECTION 0.5(c)5 EXACTLY

I ran `grep` for D/ST rows in `WIRE_20260916.csv`, found none, and told Matt **"there is not one
defence on the wire page."**

**`THE_WEEKLY_WIRE.html` has a whole defence section.** It is headed *"The defence to HOLD, not the
defence to start this week"*, it ranks ten teams over the weeks 2 to 5 run, it marks Matt's Browns
`(yours)` at second of ten, and it carries two measured findings I did not have in my head.
`wire.py` line 1475 drops K and D/ST from the row table on purpose, and line 1609 reads them back
out of the pool for that section, with the comment *"D/ST are not on the board by design."*

**The rule this broke is already written down.** Section 0.5(c)5: *"After any build that produces a
printed or rendered artifact, verify that the rows which must be on it ARE on it, by name, against
the decision they serve, not by row count."* I verified a row count, in a different file, and
reported it as a property of the page. **The CSV and the page are two artifacts and only one of
them is what Matt reads.**

**STANDING CORRECTION: never describe the page from the CSV. Open the page.**

## 2. WHAT THE PAGE ALREADY SAID, WHICH IS MORE THAN I DID

- **Chasing the best week is worth about a point. Not being forced into the worst one is worth
  more.** Across every defence-week of the last four seasons, a hard draw scores below zero more
  than a quarter of the time and under two points 37% of the time; an easy draw does that 9% and
  17% of the time. **So hold one defence through a soft run rather than chasing weekly.**
- **Four in every ten waiver claims Matt filed in each of the last two seasons were for a defence**,
  13 one year and 12 the next, against about three for the average manager in this league. Only the
  first winning claim each run comes at his real priority. **This is the clearest single leak in his
  waiver record and it is on the page he already has.**
- **Week 6 is already flagged and already priced.** *"Sam LaPorta, T.J. Hockenson are off together.
  That is one empty TE slot, and a one-week pickup fills it. No trade is needed for a single hole."*
  Cost 9 points. Week 11 is the real one at 23 points, with Nacua, Judkins and Adams all off.

**I told Matt the tooling had missed the week-6 tight end pair and then recommended a claim to fix
it. The tooling had caught it four weeks out and told him not to spend on it.** That reversal is in
the same night's chat and the page was right both times.

## 3. THE STALE NUMBER

I gave Matt week-2 defence ranks from `Source\dst_week1_2026.csv`. **That file is built by
`Scripts\research\build_dst.py` from `play_by_play_2025.csv.gz` and nothing else**, scored under
section 2's own points-allowed bands, then inverted to each offence's generosity. It was written
11 September. **It contains no 2026 football at all.**

Matt's objection was "Miami didn't look so hot", which is precisely the information the file cannot
hold. **Quoting it without its capture date is the section 1.1 discipline applied to the wrong
kind of file, and B7's "state every source's date before use" covers it.**

## 4. THE DISAGREEMENT, MEASURED

ESPN's in-league week 2 D/ST projections against ours, for the ten ESPN displayed:

| team | opp | ESPN | ours | our rank | status |
|---|---|---|---|---|---|
| TB | vs CLE | 7.9 | 6.34 | 6 | rostered, FLEM |
| SEA | @ARI | 7.4 | 6.90 | 4 | rostered, Boo |
| SF | vs MIA | 7.2 | 5.27 | 14 | claimable |
| PHI | @TEN | 7.1 | 7.05 | 2 | rostered, POT |
| KC | vs IND | 6.9 | 4.26 | 25 | claimable |
| BAL | vs NO | 6.9 | 5.81 | 9 | rostered |
| LAC | vs LV | 6.7 | 7.14 | 1 | rostered, Tets |
| NE | vs PIT | 6.6 | 5.36 | 12 | rostered, DUCK |
| CHI | vs MIN | 6.4 | 6.53 | 5 | claimable |
| GB | @NYJ | 6.3 | 5.92 | 7 | claimable |
| CLE | @TB | not shown | 5.52 | 11 | **his** |

**Pearson r = +0.125, n=10.** The two measures of the same quantity are close to unrelated. On the
four claimable teams the orders are reversed at the top: ESPN says SF, KC, CHI, GB and ours says
CHI, GB, SF, KC. `[TESTED, n=10, descriptive]`

**AND NOBODY HAS EVER CHECKED WHETHER ESPN'S D/ST PROJECTIONS ARE ON OUR SCALE.** Section 4.23(c)
verified the board reconciles to section 2 scoring at r=0.9914, but that check sets
`SCORING_CHECK_POS = {QB, RB, WR, TE}` and **excludes K and D/ST in terms**, because they score off
a different component set. Doc 264 established separately that our points-allowed bands span 20
points against ESPN's default 10, so a scale difference is live and unmeasured.

## 5. BLOCKED, WITH THE EXACT MISSING INPUT (section 0.5a4)

**To settle section 4 I need each defence's ACTUAL week 1 2026 score computed under section 2's
bands.** That needs one of:
1. `play_by_play_2026.csv.gz` from nflverse. **`Scripts\research\_nflverse_cache\` holds 2022
   through 2025 and no 2026 file.** `build_dst.py` and `dst_all.py` both run unchanged against it.
2. Or a 2026 ESPN pull carrying D/ST actual stat lines, which needs Matt's session (section 0.4
   item 1).

**Route 1 is mine to do and needs no login. It is on the open list, not waiting on him.**
Until then, neither projection is defensible over the other and I should quote neither as a rank.

## 6. WHAT THE DECISION WAS, AND WHY IT SURVIVES NOT KNOWING

**Start the Browns, spend no claim on a defence.** Taking ESPN's numbers at face value, SF over CLE
is about 1.7 points for one week. The page's own measurement puts the value of chasing the best week
at roughly a point, the cost is a priority turn already committed to a receiver, and defence claims
are the leak in section 2 above. **A recommendation that holds under both projections is worth more
than picking the projection I prefer.**

Tampa is not a choice regardless: FLEM owns it. And its 7.9 is high **because it plays Cleveland**,
which is a statement about Cleveland's offence and carries nothing about the Browns defence facing
Tampa's. Matt called it a trap on instinct and the instinct was pointed at the right game.
