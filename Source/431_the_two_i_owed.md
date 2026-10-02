# 431 — The two I owed, run. A starting QB's misses pile up late; the defense pool does not thin at all

> **BANNER, 28 Sept 2026 (doc 435), reproduced cold.** The missed-weeks curve reproduces from `qb2_window.py` (6.2% / 29.9% / 44.6%, n=160; the levels depend on the definition of "missed", which here is "not the team's top-scoring QB that week"). **The 96% does NOT stand: it divides the weeks-10-to-17 missed weeks (2.57) by the weeks-1-to-14 total (2.67). Against the full season (3.89) the share is 66%, and 67% under a plain did-not-play definition.** "Flips the verdict" is withdrawn: a week-10 QB2 covers about two thirds of a season's exposure for 8 of 17 roster-weeks, a mild positive, not nearly free. The defence and kicker supply numbers stand (13.5 / 13.6 and 15.4 / 14.2 are raw usable counts; the "minus 12" floor is stated separately). Note: `dst_k_supply.py` deducts missed PATs, which §2 does not score, and `dst_weekly_2021_2025.csv` carries no blocked-kick or fumble-lost term.

*25 Sept 2026. Matt: "when are you going to run those two open items?" They were on `claude_todo.txt`
within the hour of that file existing, which is the point of the file, and it is not an answer to
his question. Both are below.*

---

## 1. A QUARTERBACK'S MISSED WEEKS ARE NOT SPREAD EVENLY, SO PRO-RATING WOULD HAVE BEEN WRONG

**§4.17b prices QB2 at +5 to +11 on a FULL-SEASON hold, from a drafted starter missing 2.98 weeks.**
I flagged pro-rating that to "held from week W" as arithmetic nobody had measured. It is valid only
if the misses are uniform. **They are not.**

**POPULATION:** every team-season 2021-2025, n=160. The STARTER is the quarterback with the most
week 1-3 production; a week counts MISSED when he is not his team's top-scoring QB. Measured 2.42
missed weeks over weeks 1-14, against §4.17b's 2.98 on a different definition — close enough to
treat the two as the same phenomenon.

| week | 1 | 4 | 7 | 10 | 12 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|
| **not his team's starter** | 6.2% | 12.5% | 25.7% | 25.7% | 27.0% | **29.9%** | 36.5% | 41.2% | **44.6%** |

**It rises monotonically and it does not flatten.** By the championship week nearly half of week-1
starters are gone.

| a QB2 held | missed weeks it covers | share of the full weeks 1-14 exposure |
|---|---|---|
| weeks 1-14 (all season) | 2.67 | 100% |
| **weeks 10-17** | **2.57** | **96%** |
| weeks 12-17 | 2.07 | 78% |
| weeks 15-17 (playoffs only) | 1.22 | 46% |

**THE ANSWER: buy the second quarterback in WEEK 10 and you get 96% of a full season's insurance
for 8 weeks of roster cost instead of 17.** `[TESTED]` Naive pro-rating would have said 8/14, so
57%, and it would have talked him out of a move that is nearly free.

**AND IT FLIPS THE VERDICT.** §4.17b's +5 to +11 against a bench spot doc 267 priced at about +7
was a coin flip. At 96% of the value for roughly half the roster cost it stops being one. **The
+3.3 bench-spot figure for a part-season hold is MY pro-rating of doc 267's number and is NOT
measured; the 96% is.**

---

## 2. THE DEFENSE POOL DOES NOT THIN. AT ALL.

**Doc 252 built the supply curve for RB/WR/TE/QB and excluded defenses and kickers in its own words,
because it needed weekly D/ST scoring under our rules and §2 did not carry it. §2 has carried it
since v9.3 and doc 265 measured D/ST12 at 5.99; doc 423 measured K12 at 8.26. The blocker named when
it was skipped was gone and nobody went back.**

**METHOD, and it differs from doc 252 on purpose.** Doc 252 rebuilt who was rostered week by week
from the draft plus every executed add and drop. There are only 32 defenses and a 12-team league
rosters 12, so the count clearing the bar nearly is the story. A unit is USABLE in week W if it
averages the replacement rate over weeks W to W+3, which is doc 252's own definition. **"Free and
usable" here is `usable minus 12`, the WORST CASE, assuming every rostered one is a good one. The
real supply is higher. State it as a floor.**

| | weeks 1-5 | weeks 10-14 | shape |
|---|---|---|---|
| **DEFENSES** clearing 5.99 | **13.5** | **13.6** | **flat** |
| free and usable, worst case | 1.5 | 1.6 | flat |
| **KICKERS** clearing 8.26 | 15.4 | 14.2 | mild fall |
| free and usable, worst case | 3.4 | 2.2 | mild fall |

`[TESTED, 2021-2025 REG]` **Neither behaves like running back, which goes 3.5 usable free to 0.8.**

**WHAT IT SETTLES, and it is Matt's own sentence.** His words in doc 267: *"Good defenses will be
out there for pick up but the sacrifice is holding two spots on the roster."* **He is right, and
this is the first time it has been measured.** So the supply side gives no reason to buy the second
defense early, which is what doc 267 concluded from the cost side alone: the pair returns +0.79 a
week and costs a bench spot every week, so hold it from week 9. **Two independent arguments, same
answer.**

## ASSUMPTIONS

1. "Not his team's top-scoring QB" is a proxy for not starting. It will miscount a blowout where the
   backup outscores a starter who played three quarters. That error is small and does not trend
   across the season, which is the axis the finding rests on.
2. The D/ST and K "free" counts are a floor by construction. A reconstruction of who was actually
   rostered, the way doc 252 did it for the skill positions, would raise them. Not run.
3. The kicker scoring uses our bands (0-39 = 3, 40-49 = 4, 50+ = 5, PAT 1, miss -1) against
   nflverse's made-field-goal buckets.
