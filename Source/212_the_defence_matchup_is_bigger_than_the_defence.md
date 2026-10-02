# 212 — the D/ST matchup is bigger than the D/ST, and Matt had to ask twice

**2026-09-07, 14:30 ET, T−5.5h.** Matt: *"This is a big deal. Having a bad match up week 1 can
easily decide win/lose… I'm surprised you haven't called this out yet."*

**He is right on both counts.** I offered to test this twice and did not run it, which is the
§0.5 failure in its plainest form — he should never have to ask for the red team. Run now.

---

## 1 — THE HEADLINE: THE OPPONENT MATTERS MORE THAN THE DEFENCE

**POPULATION: 2,718 team-weeks, 2021–2025 regular season. OUTCOME: D/ST fantasy points scored
under THIS LEAGUE'S OWN RULES**, rebuilt from nflverse play-by-play — sack 1 · INT 2 · fumble
recovery 2 · safety 4 · defensive or return TD 6 · the nine points-allowed bands from
`2026_League_Settings.txt`. **BASELINE: 5.10 points a week, sd 6.56.** `[TESTED]`

Two-way fit, within season, on who the defence IS and who it PLAYS:

| what | share of the variance in one week |
|---|---|
| **the opponent's identity** | **15.6%** |
| the defence's own identity | 9.4% |
| both together | 24.4% |
| **week-to-week randomness** | **75.6%** |

**Who they play carries two thirds again as much as who they are.** And the board ranks defences
on a season-long projection, which is the 9.4% — it has no schedule in it at all. Matt's instinct
was right and the board could not have told him.

Swing, best to worst: **opponent 8.2 points a week, defence 6.6.**

---

## 2 — BUT WEEK 1 ALONE IS THE WRONG HORIZON, AND THIS CORRECTS ME

This morning I reasoned that the drafted D/ST is a one-week asset, so take the best Week 1
matchup. **The arithmetic says that is the small half of the question.**

| horizon | best-to-worst spread across the 32 defences |
|---|---|
| **Week 1 only** | **3.56 points** |
| **Weeks 1–4** | **11.72 points** |

One week is barely half a standard deviation — inside the noise. **Four weeks is three times the
signal, and it is also the answer to what Matt actually asked for: not being forced onto the wire
in week 2.** Draft the soft OPENING STRETCH, not the soft opener.

Persistence, measured over four transitions (n=128 each), and used to shrink 2025 form before
projecting: **defence quality r=+0.269 · an offence's generosity to opposing D/STs r=+0.325.**
Both weak — which is why the projection below is a tilt, not a forecast.

---

## 3 — WHAT IS ACTUALLY AVAILABLE AT PICK 152

The best four-week defences are **not draftable at 152**: Seattle **25.83** goes at ESPN 108.6,
Pittsburgh 23.81 at 116.2, Houston 22.75 at 87.3. Crossed against the board's own prices:

| D/ST | ESPN adp | Week 1 | weeks 1–4 |
|---|---|---|---|
| ~~Seahawks~~ | ~~108.6~~ | 5.58 | **25.83** — gone long before 152 |
| **Jaguars** | **167.9** | **7.10** *(vs CLE)* | **23.87** |
| ~~Steelers~~ | ~~116.2~~ | 5.73 | 23.81 — gone |
| **Bears** | 169.2 | 5.69 | 23.15 |
| **Buccaneers** | 169.8 | 5.88 | 22.97 |
| **Chargers** | 164.1 | 5.94 | 22.04 |
| **Packers** | 168.4 | 6.17 | 21.83 |
| worst on the board | | | **NYJ 14.11 · CIN 15.28 · WAS 15.69** |

**JACKSONVILLE IS THE PICK AT 152.** It is first on the four-week number *and* first on Week 1
among everything that reaches him, and it is priced 16 picks past his turn. Backups in order:
**Chicago · Tampa Bay · Chargers · Green Bay.** The gap from Jacksonville to the worst on the
board is **9.8 points over the first four weeks** — the largest thing available at a pick this
project had written off as free.
*Caveat kept: §4.9 measured ESPN's D/ST prices as the least reliable on the board, so treat 167.9
as "should be there", not "will be there".*

---

## 4 — KICKERS: HE IS RIGHT THAT THEY SCORE, AND WRONG THAT THE MATCHUP HELPS

Same build, same rules — PAT 1 · FG missed −1 · 0–39 = 3 · 40–49 = 4 · 50+ = 5. **n=2,683
team-weeks. BASELINE 8.02 a week, sd 4.59.**

**A kicker outscores a defence by three points a week with two thirds of the variance, and
35.3% of kicker weeks are double digits.** Matt's read is correct and the position is quietly
the steadier of the two.

**But it is far less forecastable:**

| what | share of one kicker week |
|---|---|
| his own offence | 7.9% |
| the opponent | 7.3% |
| both | 15.3% |
| **randomness** | **84.7%** |

**Week-1 spread across 32 kickers: 1.64 points. Weeks 1–4: 6.26.** Opponent persistence is
r=+0.121 — barely there.

**SO: do not shop a kicker by matchup.** Best four-week slates are Houston (Fairbairn) 35.99,
Seattle (Myers) 35.15, Dallas (Aubrey) 34.17, Chicago 33.80, Chargers (Dicker) 33.57 — and every
one of those is priced inside 161 anyway. **At 161 take whatever the board offers; if two are
level, prefer the better offence.** A point and a half a week is not worth a second of the clock.

---

## 5 — WHAT THIS DOES AND DOES NOT CHANGE

**It does not contradict §4.8.** That finding is about drafting a defence EARLY — the +105.6
points a manager-season is the cost of spending a real pick on one. This is about *which* one to
take at a pick that is already spent, which is free.

**And streaming still governs from week 2 on** — 11 or 12 of 12 teams stream every season, and
his own waiver record (doc 205) shows a claim beats a free-agent add at every position. Drafting
the four-week slate is what buys him the option to *not* stream in week 2, which is what he asked
for.

**NOT MODELLED, and say so:** home field · 2026 roster and coaching turnover (this is 2025 form
shrunk toward the mean) · weather · any in-season injury. The whole model explains 24% of a D/ST
week and 15% of a kicker week. **Treat the four-week ordering as a tilt worth about 0.8 points a
week at D/ST and 0.4 at kicker — real, small, and free.**

Reproduce: `dst_weekly_2021_2025.csv`, `k_weekly_2021_2025.csv`, `dst_week1_2026.csv`,
`k_week1_2026.csv`. Schedule verified against nfl.com weeks 1–4, two independent sources,
64 games, every team once.
