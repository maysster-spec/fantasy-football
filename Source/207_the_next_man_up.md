# 207 — The next man up: real, large, and not a team trait you can draft

*2026-09-06. Matt: **"is it true that some teams perform better with backup RBs coming off the bench
due to injury. I'm thinking SF as an example. maybe bench is wrong word instead the next man up."***

---

## 0. ACTIONABLE FIRST

1. **The phenomenon is real and it is enormous.** When a team's lead back is out, the next man
   scores **12.0** half-PPR points — against **6.1** for the same role in weeks the lead back plays.
   **Inheriting a backfield roughly doubles a back.**
2. **"Some teams" is supported: between-team differences beat chance (F=1.62, p=0.029).**
3. **But it does NOT persist year to year — r=+0.153, p=0.51.** Which team was good at it last
   season tells you nothing about this one. **Not draftable.**
4. **SF is the wrong example, on the largest sample in the league.** 22 lead-back-out weeks,
   **10.3 points — below the 12.0 league mean.** The Shanahan-system reputation does not show up
   in the outcome.
5. **What this reinforces is §4.20: buy the JOB, never the name — and never the system either.**

---

## 1. WHAT WOULD HAVE TO BE TRUE (§0.5(a2))

**POPULATION:** every team-week 2021–2025 in which the season's RB1 (most offensive snaps) played
**under 25%** of snaps — 353 of 2,703 team-weeks, **13.1%**.
**OUTCOME:** the best OTHER back's half-PPR points that week.
**BASELINE:** the same measure in weeks the RB1 did play.
**AND THE TEST THAT DECIDES IT:** persistence. A team effect that does not carry from one season to
the next cannot be drafted on, however real it is within a season.

## 2. RESULTS

**The takeover premium — the headline number:**

| | mean next-man points |
|---|---|
| lead back OUT (n=353) | **12.01** |
| lead back playing (n=2,350) | **6.09** |

**By team, 2021–2025, teams with 6+ such weeks:**

| top | | | bottom | |
|---|---|---|---|---|
| NE | 17.13 (n=10) | | WAS | 10.48 (n=14) |
| CHI | 16.86 (n=11) | | **SF** | **10.03 (n=22)** |
| CAR | 16.18 (n=13) | | NYJ | 9.83 (n=7) |
| MIN | 14.68 (n=10) | | DET | 9.79 (n=8) |
| SEA | 14.12 (n=16) | | HOU | 8.99 (n=19) |
| TB | 13.81 (n=7) | | NO | 7.79 (n=20) |

**Between-team ANOVA: F=1.62, p=0.029.** Real spread.

**PERSISTENCE — and this is the one that decides it.** Team mean in season *t* against season
*t+1*, teams with at least 3 out-weeks in both: **n=21 pairs, r=+0.153, p=0.509** (Spearman +0.173,
p=0.452). **Nothing.** The within-window spread is who happened to have a good backup, not a
reproducible property of the offense.

## 3. SF, EVERY WEEK, BECAUSE HE NAMED IT

22 lead-back-out weeks, more than any other team, mean **10.3**:
2021 Sermon 10.4 / 8.9 / 6.0 and Hasty 2.5 / 2.1 / 4.4 · 2022 Mitchell 4.1, Wilson 11.3 / 12.1 /
13.4 / 2.5, Coleman 20.2 · 2023 Mitchell 13.7 · 2024 Guerendo 17.7 / 25.8 / 9.5 / 11.9, Taylor
3.0 / 12.6, and three McCaffrey weeks.

**METHOD NOTE:** in 2024 the season's snap leader was Jordan Mason, so a barely-playing McCaffrey
registers as the "next man" in weeks 10–12. That is the definition working as written, not a
defect, and dropping those three rows does not move SF off the bottom half.

## 4. WHERE IT TOUCHES THE 2026 BOARD — AND THE CIRCULARITY

**NE tops the table at 17.13 — and that is largely TreVeyon Henderson's own 2025 takeover**
(29.8 and 27.5 in weeks 10 and 11, two of the eight biggest next-man weeks in five years).
**So NE's rank is not independent evidence about NE's system for 2026; it is Henderson's 2025
restated.** Do not read the team number as a reason to buy the player who produced it.

**What survives and is already shipped:** §4.13c's observation that 8 of 15 late ratio-booms were
backs who inherited a backfield now has its magnitude — **the inheritance is worth about +6 points a
week**. That is the whole case for `depth_map.py`'s **UNSETTLED / job worth** flag, and none of it
depends on which team the job is on.

---

*Reproduce: nflverse snap counts 2021–2025 (`position == RB`, `game_type == REG`) joined to weekly
scoring under §2 on a suffix-stripped name key; RB1 = most offensive snaps that team-season;
out-week = RB1 offense_pct < 0.25; outcome = max points among that team's other backs.*
