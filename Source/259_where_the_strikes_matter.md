# 259 — WHERE THE STRIKES MATTER, ON HIS ACTUAL ROSTER. THE WIRE CANNOT UPGRADE A SINGLE STARTING SLOT HE HAS.

*2026-09-09. Matt: "we really want strong match ups at every position, but not achievable as far as*
*I know, so I need to determine where my strikes matter most, and what players may be available to*
*trade or pick up."*

**He is right that it is not achievable, and the measured reason is better than "there aren't enough**
**good matchups": at three of five positions the matchup is worth almost nothing even when you win it.**

---

## 0. WHAT TO DO — the strike order, biggest first

**[REVISED mid-session on his correction: *"trades are not frequent in my league, and when I get
offers they are most often unbalanced significantly in their favor."* That moves the trade lane
from second to LAST, and it changes what the wire is FOR. See §3.]**

1. **FIX HOLES. 10 to 28 points each, and NO COUNTERPARTY REQUIRED.** Week 11 costs **28.1**,
   week 6 costs **10.7** (doc 233). Nothing else is within a factor of three, and this is the only
   big lever he can pull alone.
2. **STREAM THE D/ST ON THE SCHEDULE.** The one position where matchup beats the player — 108% of
   the spread between the units (doc 227 §3b) — and it needs nobody's agreement.
3. **USE THE WIRE FOR JOB CHANGES, NOT UPGRADES.** Measured in §2: the best free body is BELOW his
   worst startable man at every position. **The wire's value is not who is on it today; it is the
   man who inherits a job in week 4** (§4.27).
4. **PROPOSE trades; do not wait to receive them.** Three league-wide a season means the market is
   not rejecting him — it is barely running. And a man carrying a bye in weeks 5, 8, 9 or 14 is
   **free to him and a real cost to the other guy**, which is the one asymmetry he can offer that
   looks fair on both sides.
5. **HIS WEAKEST STARTING SLOT IS TIGHT END — 10.67 a game — AND IT IS THE ONE POSITION WHERE
   MATCHUP IS MEASURED AT ZERO** (TE 0.15 points of swing). It cannot be streamed better; it can
   only be replaced.
6. **A board artifact to not mistake for a finding: Pickens, Browns D/ST and Pineiro all read 0.00**
   because keepers and K/D-ST are off the 480-row board. His receiver corps is deeper than the
   table shows.

---

## 1. WHERE MATCHUP IS WORTH CHASING — the answer to his question, already measured

Doc 227 §3b, prior-season opponent quality (the version you can act on, not hindsight):

| position | matchup swing | spread between the PLAYERS | matchup as a share |
|---|---|---|---|
| **D/ST** | **2.22** | 2.06 | **108% — chase the matchup** |
| QB | 1.13 | 4.84 | 23% — chase the player |
| RB | 0.56 | 5.18 | 11% |
| TE | 0.15 | 3.07 | 5% — ignore it |
| WR | 0.09 | 4.29 | 2% — ignore it |

> **AT DEFENCE, TAKE THE SCHEDULE. AT EVERY OTHER POSITION, TAKE THE PLAYER.**

**So "strong matchups at every position" is not a thing to fail at — it is a thing worth about a
point a week at QB and nothing at all at receiver and tight end.** The strike that matters is not
a better matchup, it is a better player in a weak slot, or a body in an empty one.

## 2. HIS ROSTER, PER GAME — and the wire against it

**POPULATION: the 15 he drafted plus Hockenson, priced off `board_v8_fixed.csv` (season ÷ 14).
FREE = not taken in our 15-round draft.**

| slot | his man | ppg | **best FREE at that position** | ppg | gap |
|---|---|---|---|---|---|
| QB1 | Hurts | **26.21** | Daniel Jones | 21.87 | −4.3 |
| QB2 | Shough | 21.92 | *(same man)* | 21.87 | **−0.05** |
| RB1 | Jeanty | 17.73 | Samaje Perine | 6.51 | −11.2 |
| RB2 | Judkins | 15.03 | " | 6.51 | −8.5 |
| RB3 | Dowdle | 12.24 | " | 6.51 | −5.7 |
| RB5 | Spears | 9.26 | " | 6.51 | −2.8 |
| WR1 | Nacua | 21.06 | Tank Dell | 8.94 | −12.1 |
| WR3 | Worthy | 10.40 | " | 8.94 | −1.5 |
| **TE1** | **LaPorta** | **10.67** | Hockenson *(now his)* | 8.53 | −2.1 |

**THE READ: there is no upgrade on the wire.** The best free player at every position is below the
worst man Matt would consider starting there. The one exception is quarterback, where Daniel Jones
and Tyler Shough are **0.05 points apart** — which means his QB2 is exactly as good as the wire's
best, i.e. the roster spot Shough occupies is worth almost nothing over a free agent.
**That is a live drop candidate and it had not been surfaced.** `[OPEN — QB2 vs the wire, measured
at 0.05 a game on projections; it needs the §4.17 missed-weeks argument re-run on the live roster
before acting, because projections do not price availability.]`

**AND IT IS DOC 252's THINNING POOL, ON HIS ROSTER, IN WEEK 1.** The free pool is at its DEEPEST
right now and it still cannot beat his bench. By week 9 it holds ten usable players league-wide and
under one startable back.

## 3. THE UPGRADES CANNOT COME FROM A TRADE EITHER — AND THAT IS THE REAL SHAPE OF HIS SEASON

*He corrected this section as it was being written: trades are rare here and the offers he receives
are lopsided against him.*

**Put that beside §2 and the conclusion is uncomfortable and worth saying plainly: his starting nine
is close to FIXED.** The wire cannot upgrade a slot, and the trade market runs at **three deals a
season league-wide** (§2, behavioural not a rule). So the levers that remain are the ones needing no
counterparty: **holes, the defence, and the job change nobody has priced yet.**

**AND THAT REHABILITATES THE WIRE RATHER THAN CONDEMNING IT.** Samaje Perine at 6.51 a game is worth
**nothing** as an upgrade over Dowdle at 12.24 — and worth the **full 10.7** in an empty week-6
tight-end slot. **The same free player is worth zero and worth ten points depending on which
question you ask.** §2's table says he cannot improve a working slot; it says nothing against
filling a broken one, and doc 233 says the broken ones cost 49.6 points a season if ignored.

**ON THE LOPSIDED OFFERS — a claim worth testing, and the input is already on his list.**
`py waivers.py` writes `trade_report_<year>.csv` for the first time (doc 235 §0.8); until it runs,
**every trade claim in this project is unmeasured, including the ones above.** `[NOT YET RUN — needs
his ESPN session, §0.4 item 1. This is the second reason to run it.]`
**The testable form: among the trades this league DID execute, does the proposing side beat the
accepting side on rest-of-season points?** If yes, the answer is not "negotiate harder," it is
**propose more.**

**What he can offer that is genuinely asymmetric, and it is doc 233's table read backwards:**
- **The byes to ASK for: weeks 5, 8, 9 and 14** — they cost him nothing, so a man carrying one is
  cheap to him and expensive to the other guy.
- **The week-11 deal has a deadline of about WEEK 9.**
- **Sell the touchdown pop, keep the workload pop** (+2.65 when the touches jumped, +0.20 when they
  did not). Check carries + targets, never the box score.
- **RB pops carry hardest (+2.36)** — so the back who pops is the worst man to sell and the
  receiver who pops is the best.

**AND THE THING NOTHING HERE HAS TESTED, restated because it is the binding constraint:** §2 records
**three league-wide trades a season observed.** The tool says what to offer; nothing says how to get
it accepted. `[OPEN — doc 227 §1.G]`

## 4. WHAT IS ACTUALLY OPEN ON HIS ROSTER RIGHT NOW

1. **Week 6, 10.7 points, tight end, unfixed** — Hockenson shares Detroit's bye.
2. **Week 11, 28.1 points** — trade window closes about week 9.
3. **D/ST is unpriced on the board**, so the one position where matchup pays is the one he has no
   read on. `dst_weekly_2021_2025.csv` + `team_2025.csv` + the 2026 schedule would build the
   forward slate. **NOT YET RUN** and it is the highest-value build left (doc 258).
4. **Shough at 0.05 over the best free QB** — a bench spot that may be worth more elsewhere.
