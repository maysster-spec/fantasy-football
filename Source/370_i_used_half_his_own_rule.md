# 370. I TOLD HIM TO CANCEL THE COLEMAN CLAIM USING HALF OF HIS OWN RULE AND A BASE RATE I CALLED A FORECAST

*19 September 2026, early hours ET. A reversal, in full, because the recommendation went out first and
the argument against it was his. Doc 369 is the previous number. Population note (0.6): every roster
and depth figure below is from `MY_ROSTER.csv` and `Scripts\depth_map.csv` as they stood on the
Friday 18 Sept 08:57 build, and every injury designation is from nfl.com's official Week 2 report,
loaded 19 Sept.*

---

## 0. WHAT TO DO

1. **The Coleman claim stands. Nothing to do.** Matt placed it; I argued against it; the argument was
   bad in four separate places and they are enumerated in section 1.
2. **THE KICKER DROP CHANGED AND THIS IS THE ACTIONABLE PART: drop EDDY PINEIRO, not Demercado.**
   Doc 368 said Demercado. That was wrong twice over and section 3 says why. `matt_todo.txt` is
   corrected.
3. **A number that must not be quoted again: "Schultz is worth 11.1."** It is the base rate for
   anything clearing the week-1 workload screen, not a forecast of Dalton Schultz. Section 2.
4. **BLOCKED, with the missing input named: Matt's Lions mechanism cannot be tested on the data here.**
   Section 4 says exactly what is missing and where it comes from.
5. Nothing to run beyond `.\ff.bat`, which doc 369 already put on the list.

---

## 1. THE FOUR THINGS WRONG WITH MY RECOMMENDATION

**(a) I APPLIED HALF OF §6's SPEARS RULE.** The rule, which came out of Matt's own correction on
9 September, reads: *"A BENCH RUNNING BACK EARNS HIS SPOT BY THE JOB HE WOULD INHERIT AND THE
FRAGILITY OF THE MAN AHEAD OF HIM, NEVER BY HIS OWN PROJECTION."* I priced the job, 164 on
`depth_map.csv`, called it smaller than Spears' 171, and stopped. **The clause I did not read is the
one that decides this case.** Spears failed the rule on both halves at once: a 171 job AND Tony
Pollard, who had played 33 of 34 games across two seasons. Coleman sits behind a chart where the
second man is currently hurt and the lead back has a long injury history. **Same job size, opposite
fragility, and the rule's own wording puts fragility on equal footing with the job.** Using half a
rule to kill an idea is worse than not having the rule.

**(b) DOBBINS IS THE PROFILE §4.22 IS ABOUT.** Prior-season availability predicting future absence is
the largest downside signal this project has measured, across all positions and five seasons, and it
is one of the mechanisms in Matt's confirmed column. **A fragile lead back makes the next man up worth
more.** I cited the handcuff as a confirmed mechanism in an earlier session, at +7.30, and then argued
against a handcuff-shaped bet without mentioning it.

**(c) I COMPARED A POPULATION AVERAGE WITH A PLAYER-SPECIFIC READ.** This is 0.6's failure exactly.
`WEEK_SHEET.html` prints **Dalton Schultz 11.1 expected** and **Michael Mayer 11.1 expected**, with
word-for-word identical reasoning and an identical 38%. **Two different players cannot have identical
expectations; it is the screen's base rate printed once per man who clears it**, 29.3 if it fires
times 38%. §4.30 says this in terms: the composite *"is a screen on young non-startable receivers,
never a forecast."* So "Schultz is worth 11.1 and Coleman is worth little" set a population average
against a depth-chart read and presented them as the same currency. **The 11.1 must not be quoted as a
Schultz number again.**

**(d) HIS OWN LIST ALREADY RULED OUT THE THING I RECOMMENDED.** `matt_todo.txt` carries, from an
earlier session: *"week 5, the TE for week 6, AND THE WHOLE ARGUMENT IS WORTH 1.3 POINTS, ONCE...
Do not pick a name now. IN WEEK 5, take whoever leads on FOUR WEEKS OF THIS SEASON'S targets."*
I recommended picking a name now. **I had read that file in this same session.** The milestone check
in §0.5(d) covers a question whose answer is already in the directive; nothing covers a
recommendation that contradicts his own to-do list, and this is the second failure tonight that a
cross-check against his trackers would have caught.

**AND THE STANDING INSTRUCTION POINTS THE OTHER WAY TOO.** `matt_todo.txt` under STANDING:
*"Swing more often. Taylor took 89 waiver swings to your 23 over four years at a WORSE hit rate...
a claim costs only the drop. That is the cheapest point available to you."* He swung. I said stop.

---

## 2. WHAT SURVIVES, AND IT IS SMALL

**The week-10 pile-up is real.** Coleman's bye is 10. So is J.K. Dobbins'. So is Jalen Hurts'. The
shipped sheet already prints week 10 with an **empty quarterback slot**, so that week is the worst on
the board before anything is added to it.

**But it is contingent and I led with it as though it were not.** It costs nothing unless Coleman is
worth starting by week 10, which is the same event that would make the claim a success. **A cost that
only arrives if the bet wins is not an argument against the bet.** It is a note for week 9.

**Matt's read on the claim window is his, and it is not what §4.31 measures.** §4.31 found the waiver
hit rate flat across the season and week 1 the worst week, and the sheet prints 40% / 29% / 40% by
window. That is about the RATE of a hit. Matt's claim is about the supply of unsettled jobs in
September, which is a different quantity and is not measured here. **NOT YET RUN**, testable form:
*of the backs who took over a job during a season, what share of those takeovers began in weeks 1 to
4, against the share of the season those weeks represent*, 2022 to 2025. That is answerable from
`form_2025.csv` plus the PFF files and it is queued.

---

## 3. THE KICKER: TWO ERRORS, AND ONE OF THEM WOULD HAVE BROKEN HIS CLAIM

Doc 368 said drop Demercado, add Boswell, keep Pineiro on the bench. Matt: *"why would i drop
Demercado for a new kicker and then roster two kickers? Eddy is that good?"*

**HE IS NOT.** The 8.4 I was protecting is the season-long gap between Pineiro and the best free
kicker, and it assumes he is your kicker for thirteen more weeks and that you never stream one again.
§4.8 says K value is not realizable and nearly everyone streams. **A second kicker is a wasted seat
and the number I used to justify it was answering a different question.**

**THE SECOND ERROR IS WORSE BECAUSE IT WAS MECHANICAL.** Matt placed a waiver claim for Coleman with
**Demercado as the drop**. Had he taken doc 368's advice and dropped Demercado for a kicker on
Saturday, **the claim would have had no drop attached when it processed.** I recommended an action
that would have broken a pending move I did not know about, which is a fair thing not to know, and
then the fix is trivially available anyway: **the drop is Pineiro.** Kickers are excluded from keeper
eligibility entirely, so it costs nothing in 2027 either.

**The 1:00 constraint from doc 368 is untouched and is the part that still matters.** Pineiro plays
at 4:25, his inactive posts at 2:55, and all six free kickers on the sheet kick off at 1:00. The
decision has to be made before 1:00 whichever man is dropped.

**Matt's IR idea was right in principle and I should have raised it before he did.** Moving a rostered
player to IR frees a seat, which is the only add that costs no drop. It fails on eligibility rather
than on logic: ESPN wants an IR or Out designation and a one-week illness will not produce one.
**BLOCKED on the exact rule: `2026_League_Settings.txt` lines 24 to 44 give "Injured Reserve (IR):
3 Slots | N/A" and never list which statuses qualify.** Only the ESPN league page shows that, which
is a §0.4 category-four file. Tried: the settings export, grepped for injur/IR/reserve/slot.

---

## 4. THE RED-ZONE HALF IS TESTED AND IT GOES AGAINST HIM. THE TRAILING HALF IS BLOCKED.

Matt, refining it himself: *"The Lions will be working from behind and can't make the safe plays...
Laporta is skilled and will get the ball, and especially near the goal line. He's a big target that's
hard to match up against in the red zone."* Two claims, and they separate cleanly.

**LAPORTA'S THURSDAY IS CONFIRMED:** six of seven targets, 52 yards, a touchdown, in a 41 to 31 loss.
RotoWire, updated 17 September 22:34, loaded.

**THE RED-ZONE CLAIM IS TESTABLE TODAY AND IT IS §4.5's TERRITORY**, which holds that red-zone VOLUME
is sticky and red-zone TD RATE is noise. So the question is volume, not touchdowns.
Population: `04_source_data\RedZone_Receiving_2024.csv` and `_2025.csv`, every pass catcher with a
red-zone target, position joined from `Source\pff_receiving_*.csv`, 93 tight ends matched in 2024 and
100 in 2025.

| Sam LaPorta, inside the 10 | 2024 | 2025 |
|---|---|---|
| targets | 9 | 3 |
| games played | 16 of 17 | **9 of 17** |
| targets per game | **0.56** | **0.33** |
| share of Detroit's, raw season | 22.0% | 7.1% |
| share of the chances he was present for, estimated | **~23%** | **~13.5%** |
| rank among tight ends by inside-10 targets | **8th of 93** | 42nd of 100 |

**THE FIRST READ WAS WRONG AND I NEARLY SHIPPED IT.** Taken raw, 22.0% to 7.1% looks like his
goal-line role collapsed. **He played nine games.** Detroit accrued red-zone targets in the eight he
missed, so the season share punishes him for being absent. Adjusted for the chances he was actually
present for, the fall is about 23% to 13.5%, and per game it is 0.56 to 0.33, **a fall of 41% rather
than of two thirds.** This is the same population error as §2 of this doc, caught this time only
because the game count was checked before the conclusion was written.

**WHAT SURVIVES THE CORRECTION, AND IT IS STILL AGAINST HIM.** A 41% fall in per-game red-zone volume
is real, and the mechanism is visible in the same table: **Amon-Ra St. Brown went from 36.6% of
Detroit's inside-10 targets to 50.0%.** Half of everything inside the ten goes to one man, and it is
not LaPorta. **Matt's physical read is sound and was clearly true in 2024, when LaPorta was the 8th
most targeted tight end inside the ten in the league. The trend since is down, and the binding
constraint is not coverage matchups, it is St. Brown.**

**AND THE PART THAT DOES SUPPORT HIM:** overall targets per game are flat, 4.9 then 5.0, so the role
is not shrinking, only the goal-line share is. His inline rate fell 51.3 to 40.1, meaning less
traditional in-line work and more split out, which is consistent with a receiver-shaped usage rather
than a goal-line-shaped one. **ASSUMPTION STATED: the adjusted share treats team red-zone targets as
evenly spread across 17 games. They are not exactly, so that column is an estimate and the per-game
row, which needs no such assumption, is the stronger of the two.**

**THE WATCH ITEM, in the form §4.5 says is the reliable one:** inside-10 targets per game, not
touchdowns. Two or three games at or above 0.56 says the 2024 role is back. Touchdowns off that
volume are noise and must not be read as the signal.

### 4b. THE TRAILING HALF IS BLOCKED, AND HERE IS EXACTLY WHAT IS MISSING

**The testable form, stated before the test per §0.5(a2):** *for a team whose defence allowed
above-median points in a season, was its starting tight end's targets per game higher than for a team
below the median, same season, 2022 to 2025?*

**BLOCKED, one input, named.** The tight-end half is in hand: `Source\pff_receiving_2022..2025.csv`
carry `position`, `team_name`, `targets` and `player_game_count`. **What is missing is NFL points
allowed by team by season.**

**Tried, and this is the part worth recording:** `04_source_data\historical_scoreboard_2022_2025.csv`
looked like the answer by its name. It is not. It is **the JUG league's own fantasy scoreboard**,
412 rows of `Season, Week, Home Team, Home Score, Away Team, Away Score`, where the teams are
Bloodied Castaways and ChatCTE. **A file named "scoreboard" in a fantasy project is the fantasy
scoreboard**, and trusting the filename would have produced a confident answer about nothing. Checked
by reading its columns.

**WHERE IT COMES FROM:** nflverse game results, the same source `Scripts\research\wk1\build_form.py`
already pulls for `form_2026.csv`. The unblock is a small addition to that script writing points
allowed per team-season. **Mine to write, queued behind the page batches.**

---

## 5. THE FORMULA HE ASKED FOR ALREADY EXISTS, AND IT IS WHY A TIGHT END IS NOT A FLEX BET

Matt: *"maybe there is a formula where it makes sense and the player is good enough and in a good
position like Schultz that i can also use as a flex."*

**HE IS RIGHT ON ELIGIBILITY AND IT IS WORTH SAYING SO PLAINLY:** `2026_League_Settings.txt` line 39,
`Flex (RB/WR/TE) : 1 Starter`. A tight end can occupy the flex here.

**HE IS WRONG ON STARTABILITY, AND THE SHEET'S OWN BAR SAYS SO.** Schultz projects **6.1 a week**.
The flex is filled by the best remaining runner or receiver, so the bar he must clear is the
**RB/WR bar of 11.7**, not the TE bar. At 6.1 he never enters the lineup as a flex, in any week.

**BUT THE FORMULA HE IS REACHING FOR IS REAL AND IT IS THIS: a hit is worth what it clears YOUR bar
by, and your bars are not equal.**

| position | Matt's bar | a 12.7-a-game hit clears it by |
|---|---|---|
| TE | **8.8** | **+3.9 a week** |
| RB | 11.7 | +1.0 a week |
| WR | 11.7 | +1.0 a week |

**That single table explains the whole shape of the sheet's ticket list**, and it is why the same
12.7-a-game hit prices at 29.3 for a tight end and 8.7 for a receiver. **It is not a claim that
Schultz is better than Coleman. It is a claim about which of Matt's slots is thin**, and the thin
one is tight end, because he has one of those and four receivers.

**SO THE TWO BETS DO NOT COMPETE AND SHOULD NOT BE RANKED AGAINST EACH OTHER.** Coleman is a bet on a
job opening. A tight-end screen is a bet on the cheapest slot Matt owns. They want different seats,
and the sequencing in section 0 of the reply is what matters, not a ranking.

---

## 6. THE PATTERN IN BOTH OF TONIGHT'S ERRORS

The kicker error and the Coleman error are the same shape. **In each case I took one number off the
shipped week sheet, 8.4 for Pineiro and 11.1 for Schultz, and used it as though it answered the
question in front of me.** Neither did. The 8.4 answers *what does dropping him cost over a season
where you never stream*, and the 11.1 answers *what does a man clearing this screen return on
average*. Both are correct numbers on the page and neither is the number the decision needed.

**§0.6 already says restate the population in every doc that uses an inherited dataset. The page is an
inherited dataset too, and it is the one I read fastest and question least.** The rule that would have
caught both: **before quoting a figure off a generated page, say in one line what population it is an
average over and whether the decision is about that population.** If a second player prints the
identical number, it is a base rate.
