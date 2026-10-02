# 283 — LaPorta: the decline already happened, it was not the new skill players, and the risk is the hip

**2026-09-10, week 1.** Matt: *"I want a comfort level with Laporta that he doesn't show signs of
decline, and he's not getting the targets he's expected to get. His rookie year was great, but he's
not likely to repeat since they have more skill players — or so i thought."*

**And first, his other sentence, which is the correct criticism: *"I'm not saying Hockenson is a
great play… I honestly don't know. I don't think you did either."* He is right. I priced the SEAT —
what the spot costs, what a bye fix is worth — and never once asked whether Hockenson is a good
tight end.** That is §0.5(a2) again in its laziest form: I answered a question about roster
arithmetic when he was asking a question about a player.

---

## 0. THE TESTABLE FORMS, STATED BEFORE THE ANSWERS (§0.5a2)

His claim has three separable parts and they resolve differently:
1. **"He's not getting the targets he's expected to get."** → has LaPorta's share of Detroit's
   targets fallen, per game, 2023 → 2024 → 2025? **TESTED. Yes, once, and then flat.**
2. **"They have more skill players."** → did players Detroit ADDED after 2023 take his targets?
   **TESTED. No — the men who took them were already there.**
3. **"Signs of decline."** → is his on-field role shrinking? **TESTED. No. It changed shape.**

---

## 1. THE SHARE — AND THE NUMBER I ALMOST PRINTED WAS WRONG BY HALF

**POPULATION: Sam LaPorta's three NFL seasons. SOURCE: `pff_receiving_2023/2024/2025.csv`, regular
season. BASELINE: Detroit's own team target total in the same season.**

The naive version — his season targets ÷ the team's season targets — gives **20.5% → 15.4% → 8.7%**
and says he has collapsed. **It is wrong, and wrongly in the direction that would have alarmed him:
he played 9 games in 2025 against a 17-game team total.** Normalised per game, which is the only
comparison that means anything:

| season | g | his targets a game | Detroit's targets a game | **his share** |
|---|---|---|---|---|
| 2023 | 17 | 6.94 | 33.8 | **20.5%** |
| 2024 | 16 | 4.88 | 29.8 | **16.3%** |
| 2025 | 9 | 5.00 | 30.5 | **16.4%** |

**The drop is real, it is about a fifth of his rookie role, and it happened in 2024 — two years ago.
It has been flat since, to a tenth of a point.** `[TESTED]` **So "he's not getting the targets he's
expected to get" is true of the rookie-year expectation and false of the current one:** ESPN prices
him at 149.6 league points for 2026, which is the 2024–25 role, not the 2023 one. The market is not
asking him to repeat.

**§0.6, yet again: the population was the first thing wrong.** The games-played denominator is the
same trap as doc 131's 20.7% rushing-yard "bias" and doc 228's missing D/ST.

---

## 2. "MORE SKILL PLAYERS" — RIGHT SHAPE, WRONG NAMES

**Where Detroit's 2025 targets actually went** (`pff_receiving_2025.csv`, 518 team targets):

| | routes | targets | share | yprr |
|---|---|---|---|---|
| Amon-Ra St. Brown | 566 | 162 | 31.3% | 2.48 |
| **Jameson Williams** | 601 | 97 | **18.7%** | 1.86 |
| **Jahmyr Gibbs** | 368 | 92 | **17.8%** | 1.67 |
| Sam LaPorta (9 g) | 244 | 45 | 8.7% | 2.00 |
| Kalif Raymond | 217 | 28 | 5.4% | 1.33 |
| Isaac TeSlaa | 296 | 26 | 5.0% | 0.81 |
| Brock Wright (TE) | 125 | 19 | 3.7% | 0.86 |

**Williams and Gibbs took the share, and both were on the roster in LaPorta's rookie season** —
Williams a 2022 first-round pick, Gibbs a 2023 first. **Nobody arrived and displaced him; two
teammates grew into it.** `[TESTED, by count]`

**Everything Detroit has ADDED at a skill position since 2023** (`nfl_draft_picks.csv`):
**Isaac TeSlaa (2025, round 3)** — 296 routes and a **0.81 yprr**, the worst of any Lion with 200+
routes · **Dominic Lovett (2025, round 7)** · **Kendrick Law (2026, round 5)**. At tight end they
signed **Tyler Conklin** (8 games at LAC, 86 routes, 10 targets, 1.17 yprr).

**And our own measurement says none of those is the archetype that takes a room.** §4.28 / doc 251,
n=364: a **first-round** rookie receiver displaces the incumbent **60.0%** of the time; rounds 2–3
**3.3%**; **round 4 or later 1.4%** (Fisher p=0.000001). **A round-5 receiver is the 1.4% cell.**
So the mechanism he named is a real mechanism and it is not operating here. `[TESTED]`

---

## 3. WHAT IS **NOT** DECLINING — AND THIS IS THE REASSURING HALF

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| routes a game | 29.7 | 28.2 | **27.1** |
| route rate (share of pass plays) | 86.9% | 87.8% | **85.0%** |
| **targets per route run** | 0.234 | 0.173 | **0.184** |
| **yards per route run** | 1.76 | 1.61 | **2.00** |
| average target depth | 7.4 | 7.8 | **5.7** |
| slot rate | 26.9% | 26.0% | **40.4%** |
| inline rate | 45.8% | 51.3% | **40.1%** |

**He is on the field as much as he ever was — 27 routes a game against a rookie-year 29.7, and a
route rate inside three points of it.** What fell was looks per route; what ROSE was yards per
route, to the best figure of his career. **His 2025 role changed shape rather than shrinking: out of
line and into the slot, shorter targets, fewer of them, more yards when they came.** `[TESTED]`

**That is the opposite of the decline pattern.** A tight end losing his job loses ROUTES first —
the snaps go to the blocking body — and LaPorta's went to Brock Wright at a **64% inline rate and
0.86 yprr**, which is a blocker taking blocking snaps, not a receiver taking targets.

---

## 4. THE RISK IS AVAILABILITY, AND IT IS THE BIGGEST ONE THIS PROJECT MEASURES

**Games played: 17 → 16 → 9.** His 2025 ended in November `[SOURCED: Yahoo Sports, 21 Aug 2026 —
back surgery for a herniated disk, 8 games; a second account in the same search records a
hyperextended knee and a week-11 IR designation. The two disagree and I am not picking between
them.]` Then a **hip** injury on **19 Aug 2026** cost him three weeks of camp.

**§4.22 / doc 203: playing ≤12 games the prior season is worth −19.4 points against the price,
p=0.00004, n=735 — the strongest downside signal in this project.** Doc 204 softens it for
established veterans, and LaPorta is entering year 4, which is exactly the band where it still
reads as a warning rather than noise.

**So his instinct to carry a tight end is correct, and for a reason he did not name.** Not "LaPorta
is declining" — "LaPorta misses games." That is the measured version of the hunch.

**AND THE LIVE ANSWER TO THE WEEK HE ASKED ABOUT: he is cleared.** LaPorta returned to practice
8 Sep and **is not on Detroit's first injury report, with no limitations**
`[SOURCED: Heavy.com, 10 Sep 2026]`. **Our own sheet says `QUESTIONABLE` because the pull is from
7 Sep, two days before the report existed** — a staleness the page does not mark, which is its own
`[OPEN]`.

---

## 5. THE WATCH TRIGGER — WHAT TO LOOK AT, WITH A NUMBER

Points are the wrong thing to watch: they are noisy week to week and a touchdown hides a role
change. **Doc 235 measured that the workload is what carries forward (+2.65 a week when it pops).
The inverse is the trigger.**

> **Baseline: 27 routes a game, 0.18 targets per route, 85% route rate.**
> **Two consecutive weeks under ~22 routes a game, OR Conklin/Wright taking inline snaps off him,
> is the signal. One bad box score is not.**

**NOT YET RUN, input named (§0.5a4):** nothing in the ESPN pull carries routes or snaps, so this
cannot be computed from what we fetch. **nflverse publishes weekly snap counts (`offense_snaps`,
`offense_pct`)** — snaps are a fair proxy for routes at tight end — and a small puller would put a
`snaps a game vs his own baseline` line on the weekly sheet for every player Matt owns. **Nothing
to compute until week 1 is played**, so it is queued, not blocked.

---

## OPEN AFTER THIS

- **The weekly snap-share puller**, above. After Sunday.
- **The sheet does not mark how old its injury status is.** It printed `QUESTIONABLE` on a man who
  is cleared, because the pull predates the report by two days. `[OPEN]` — the fix is a stamp on the
  status column, not a faster pull.
- **Whether LaPorta's 2025 slot shift (26% → 40%) holds in 2026** is the thing that decides whether
  the 16.4% share is his floor or his ceiling. 4for4's own stability table (doc 251: slot rate 0.75,
  the most stable receiver trait measured) says the role itself should persist — which would argue
  the 16.4% holds. `NOT YET RUN` as a test on tight ends specifically.
- **Conklin is the body to watch, not the rookie.** A veteran signing with a 42% inline rate is the
  one who can take snaps in week 1; Kendrick Law cannot.
