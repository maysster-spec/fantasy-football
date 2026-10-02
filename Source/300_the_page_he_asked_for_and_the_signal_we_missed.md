# 300 -- the page he asked for, and the signal that would have caught Black

**12 September 2026.** Matt's `Updates_Suggestions.md`, written this morning. Two halves: the week
sheet is rebuilt on his notes, and the thing he was really arguing about turns out to be measurable
in one box score.

---

## 1. What he said, and what changed

> *"Week 1 - the move. This section doesn't make sense. Instead of listing the top takes for that
> week, it list D/ST and other positions to take in later weeks."*

**He is right, and it was the design rather than a slip.** Section 0 sorted every candidate on
SEASON points, so three bye fills for weeks 6, 8 and 11 outranked anything a man could do in week
one, and the page headlined a kicker. Fixed:

| his note | what the page does now |
|---|---|
| the week-1 list is full of later-week fills | **THIS WEEK and THE CALENDAR are separate.** A fill he does not need for a month is a calendar row keyed to the week he should CLAIM, labelled projected, with "these names will move" said out loud |
| *"here are your priority pickups this period in order of value"* | that is the heading, and they are numbered |
| the points should stand out | the number is the headline of each row, and 26px on row one |
| *"Anything that has bearing on what decisions I make deserves prominence"* | the cost of the drop is a bordered box ABOVE the picks, not a line under them |
| the ruled-out block *"reads like you are talking to yourself"*; *"why do I need to know your recommendation was bad before?"* | one sentence, no self-commentary, no instruction to edit a file |
| *"anybody who plays is the whole difference"* ... *"That's not how people write"* | gone. It appeared three times on one page. Every row now carries one written sentence instead of three assembled fragments |
| *"I need an example of this formula in use"* | the box is a worked example built from a live row, never a formula |
| does the team name follow ESPN? | **it does now.** It was hard-coded; `wire.py` reads it from `mRoster`, so renaming the team renames the page |

**Verified:** 44 of 44 red-team controls pass against the production path, the page renders at week 1
and week 6, the retired sentences grep clean, and the calendar was exercised with a planted kicker
and defence because the recorded pool holds neither.

---

## 2. THE PART THAT MATTERS MORE: he was right that we should have caught Black

> *"Other analysts call for Kaelon Black to be a bench stash, but we never heeded those signals and
> we need to learn from that."*

**The seat model on the page prices a backfield seat at what it pays WHEN THE JOB OPENS.** A back
who is already being paid while the starter is healthy is invisible to it by construction. That is
why the page ranks Black third at 1.1 expected points while the news ranks him first.

**THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):** *among teams whose week-1 lead
back PLAYED, the second back's share of the team's week-1 backfield work predicts his weeks 2-14
scoring, and a high share marks a back who becomes startable more often than the ordinary handcuff.*

**POPULATION:** every team-season 2021-2025 whose leading week-1 back played in week 1 (if he did
not, the job was already open, which is doc 294's event), and whose second back also played and
appeared in 4+ of weeks 2-14. **n = 143 team-seasons.**
**PREDICTOR:** the second back's share of his team's week-1 running-back carries plus targets.
**OUTCOME:** his half-PPR points a game over weeks 2-14, and whether that reached the RB
replacement rate of 9.92 `[INHERITED: 4.1's RB30 divided by 17]`.

| RB2's share of week-1 backfield work | n | weeks 2-14 ppg | reached 9.92 |
|---|---|---|---|
| under 20% | 44 | 4.99 | **7%** |
| 20 to 30% | 35 | 5.22 | 11% |
| 30 to 40% | 36 | 8.35 | 39% |
| **40% or more** | **28** | **10.28** | **50%** |

**35% or more against under 35%: +3.89 points a game and +29 points of startable rate. Permutation,
4,000 draws, one-sided: p = 0.0000 on the scoring and p = 0.0003 on the rate.** `[TESTED, n=143]`
The base rate across the whole population is 24% startable at 6.93 a game.

**AND KAELON BLACK IS IN THE TOP BAND.** `[SOURCED: nflverse weekly, 2026 week 1]` San Francisco's
week-1 backfield: McCaffrey 18 carries plus targets, **Black 15 -- 45% of the work**, with McCaffrey
healthy and playing. Only four teams have published a week-1 running-back line so far, so this is an
early read on a partial week, but San Francisco's game is finished and the split is what it is.

**THE HONEST SIZE OF IT: 50% is a coin flip, not a certainty.** The top ten shares include James
Conner, Gibbs, Bijan, Stevenson and Kareem Hunt, and they also include **Carlos Hyde at 3.3 a game,
Gus Edwards at 4.7 and Kenyan Drake at 7.1.** Half of them missed. What the number buys is a
doubling of the base rate off one box score, which is a lot for something that costs nothing to
look at.

**THE SELECTION CAVEAT, because it is real:** this is the RB2 *by week-1 work*, so he got the work
because the coach wanted him to have it. That is not a flaw in the test, it IS the finding: **a
near-even week-1 split usually means the second back is part of the plan rather than a spare body.**
It is a week-1 signal and not a preseason one, and nothing here says it could have been read in
August.

---

## 3. What this does to the page, and what it does not

* **Nothing is rewired today.** The band still ranks by the seat model, and the seat model still
  cannot see a share it has no 2026 usage file for.
* **NOT YET RUN, and it is the wiring job:** feed the weekly share into the seat price, so a backup
  taking a real share of a healthy starter's work is ranked on the band above rather than on the
  generic 46% job-opens figure. The Tuesday read already downloads the file it needs.
* **The Tuesday prompt now carries the band table**, so the next weekly read applies it whether or
  not the page does.

---

## 4. His other three arguments, each with one of the three answers

**(a) The analyst-disagreement population.** His objection: the project measured that disagreement
among rankers predicts finishing WORSE (4.13d, −0.244, p=0.0009) and then dropped the whole
population, *"risking leaving out players who could be included ... Looking at this population could
help identify other key indicators when those player takes worked out to be correct."*
**He has the better of this.** A negative average across a population is not a reason to stop
looking inside it; that is the same mistake 4.27 made before its subgroup was found, and the same
one 4.28 made before draft capital was tried.
**NOT YET RUN, testable form stated:** *within the disagreed-about players only, does any available
trait separate the ones who beat their price from the ones who did not?* Inputs on the drive:
`FantasyPros_ECR_BestWorstStdDev.csv` for the spread, the 1.1 preseason registry for price,
nflverse for the outcome. Queued, not blocked.

**(b) Not every second back inherits, and the reason is body and role.** His examples: a
pass-catching specialist under 200 pounds, short arms, and TreVeyon Henderson kept out by pass
blocking.
**NOT YET RUN. Weight and size are in nflverse rosters and are free; pass-blocking grade is a PFF
field and `pff_rushing_2022-2025.csv` is already on the drive, so this is not blocked either.**
Testable form: *among second backs whose lead back missed time, does weight, or a pass-blocking
grade, separate the ones who took the job from the ones who did not?*

**(c) The size of the pie the lead back held.** *"Historically, CMC has had a large piece of the pie
in that offence."*
**PARTLY MEASURED ALREADY and it is on the page:** `job_ceil` is the projection of the man holding
the job, and McCaffrey's is 302.4, the second largest in the league. What is NOT measured is his
point: whether the backup's return scales with how CONCENTRATED that backfield was, rather than how
large the offence is. **NOT YET RUN**, and the same weekly file answers it.

---

## 5. On the drive

`Scripts\sheet_engine.py` 79,220 · `Scripts\wire.py` 82,751 · `Scripts\check_kit.py` 27,386 ·
`Source\sheet_constants.json` with the measured absence and streamer rates ·
`Scripts\research\wk1\week1_share.py` and its run. Archives for all of them.
