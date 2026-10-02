# 227 — The waiver research: the search catalog, what the published material gives, and two measurements it produced

**2026-09-08.** Matt: *"this is what I meant by you researching strategies on waivers. I can't do
this alone and you can fact check my assumptions... I need you to come up with search terms for
current and past results on the web on how to play the waiver wire. both for hot and deep picks."*

**The catalog is §1 — that is the deliverable he asked for, laid out so he can re-order it.** §2 is
the batch I ran off it. §3 is the part that matters: **two measurements the reading produced, one of
which grades code I shipped an hour earlier and one of which changes a rule.**

---

## 1. THE SEARCH CATALOG — every angle, so the gaps are visible

**Marked `[RUN]` where I searched it today, `[OPEN]` where I did not.** `ERROR_PATTERNS` B7 applies
to all of it: state a source's date before using it.

### A. The mechanics of a priority (non-FAAB) wire — the one we actually play `[RUN, thin]`
- *"waiver order reset each week inverse standings does claim move you to bottom"* — **this one paid.
  ESPN's own documentation settled the rule doc 226 was wrong about.**
- *"fantasy football waiver strategy when you have last waiver priority winning team"*
- `[OPEN]` *"rolling waiver priority vs FAAB which rewards skill more"*
- `[OPEN]` *"waiver priority value in points how much is the number one claim worth"*
- `[OPEN]` *"continual rolling list vs reverse standings waiver order strategy differences"*

### B. HOT PICKS — spotting the man everybody will want, one week early `[RUN, partial]`
- *"snap share target share triggers waiver wire predictive early indicator"* — **[RUN]**
- `[OPEN]` *"routes run leading indicator target share breakout fantasy"*
- `[OPEN]` *"red zone touches first week after starter injury workload transfer percentage"*
- `[OPEN]` *"opportunity share carries plus targets threshold RB startable fantasy"*
- `[OPEN]` *"how many games of usage before a breakout is real sample size fantasy"*
- `[OPEN]` *"beat writer practice report predictive value fantasy football"*

### C. DEEP PICKS — the stash, the handcuff, the one-injury-away man `[RUN]`
- *"handcuff running back backup value study percentage finish RB2 when starter injured"* — **[RUN]**
- `[OPEN]` *"contingent value backup running back expected points if starter misses time"*
- `[OPEN]` *"stash injured player IR slot value fantasy football return on roster spot"*
- `[OPEN]` *"how long to hold a stash before dropping him weeks fantasy"*
- `[OPEN]` *"committee backfield early down carries share predicts takeover"*

### D. TIMING `[RUN]`
- *"when to claim waiver wire before or after news breaks fantasy"*
- `[OPEN]` *"speculative add before injury designation value fantasy"*
- `[OPEN]` *"Tuesday vs Wednesday vs Sunday free agent pickup timing"*

### E. HOW MUCH CHURN `[RUN, nothing found]`
- *"roster moves per season correlate with fantasy championship win rate"* — **[RUN, no data anywhere]**
- `[OPEN]` *"transaction count vs finishing position fantasy football study"*
- `[OPEN]` *"is roster churn positive or negative expected value fantasy"*

### F. STREAMING BY MATCHUP `[RUN]`
- *"how much does matchup matter streaming defense opponent quality vs defense quality"* — **[RUN]**
- `[OPEN]` *"streaming quarterback by matchup expected points gain over season"*
- `[OPEN]` *"tight end streaming matchup value data"*
- `[OPEN]` *"kicker streaming dome weather total implied points data"*

### G. BYES, TRADES AND SCHEDULE ARBITRAGE `[OPEN — the whole row]`
- *"bye week trade arbitrage fantasy football sell player with later bye"*
- *"playoff schedule weeks 15 17 strength of schedule streaming plan"*
- *"trading into a league that does not trade how to get offers accepted"*

### H. THE OTHER TWELVE `[OPEN]`
- *"predicting which managers will claim a player waiver competition modelling"*
- *"blocking a claim denying a handcuff to the owner of the starter"*  ← **his idea, and untested anywhere**

### I. QUANTITATIVE / ACADEMIC `[RUN, one hit already in the project]`
- Lee & Liu, *Judgment and Decision Making* 2022, n=188,426 — already in doc 12's survey.
- `[OPEN]` *"fantasy football waiver wire expected value model published"*
- `[OPEN]` *"sports analytics in-season roster acquisition optimisation paper"*

---

## 2. WHAT THE PUBLISHED MATERIAL ACTUALLY GIVES — thin, and worth saying plainly

Sources read today, dates first (`ERROR_PATTERNS` B7):

| source | date | what it gave |
|---|---|---|
| ESPN Fan Support, *Waiver Order Overview* | undated, official | **The rule.** *"once a team successfully makes a waiver claim, they move to the bottom."* Settled doc 223's error |
| Footballguys forum, *Waiver Wire Priority* | 2018-09-11 | four competing mechanisms; **hoarding tested NULL on our data** (doc 226 §3) |
| 4for4, *Waiver Wire & FAAB Strategy* | 2023-08-28 | FAAB-first; nothing for a priority league |
| Football Nation, *Snap Share vs Route Participation* | 2026-08-14, upd 09-01 | **the sequence: routes → target share → box score.** No thresholds, no numbers |
| Draft Sharks, *Best RB Handcuffs* | 2026-08-31 | a 1–10 composite of talent / depth / offence / injury risk. **No historical hit rate at all** |
| The Fantasy Footballers, *Mythbusters: Matchups* | 2021-08-03, upd 2025-08-15 | **the only quantified piece.** Per ranking step: QB offence +0.22 vs defence −0.07 · RB defence 0.13 · WR defence −0.09 · **TE defence ~0** |

**THE HONEST VERDICT ON THE GENRE: almost nobody publishes a hit rate.** Handcuff articles rank
without ever saying how often a handcuff pays. Waiver columns name players, not rules. **Two of six
sources contained a number worth testing, and one of those is a decade-old rule page.** That is why
this project measures its own record instead — and it is also why the catalog above is worth working
through slowly rather than in one sitting.

**One mechanism worth keeping, untested here:** routes run leads target share leads the box score.
**We hold snap counts (2021–2025) but not routes**, so the testable half is snap share. Post-season.

---

## 3. THE TWO MEASUREMENTS THE READING PRODUCED

The Fantasy Footballers piece is per *ranking step*, which is not a unit anything else uses, so it
was re-run on our own data under §2 scoring.

**POPULATION:** all player-weeks 2022–2025 for QB/RB/WR/TE (regular season, players with 8+ scored
weeks that season; QB 10+), and all D/ST team-weeks 2021–2025. **BASELINE:** weekly fantasy points
regressed on the player's OWN season average plus the opponent's points allowed (for a D/ST, the
opponent's points scored). **The distinction that matters: SAME-season opponent quality is
hindsight; PRIOR-season is what a drafter can actually see, and it is what `team_2025.csv` ships.**

### 3a. Matchup, prior season — real at QB, worthless at receiver

| position | n | coefficient | p | swing across a realistic opponent range | spread between the players themselves |
|---|---|---|---|---|---|
| QB | 1,805 | +0.144 | **0.049** | **+1.13 pts/g** | 4.84 |
| RB | 5,387 | +0.071 | **0.007** | +0.56 | 5.18 |
| WR | 8,735 | +0.012 | 0.52 — **null** | +0.09 | 4.29 |
| TE | 4,231 | +0.021 | 0.36 — **null** | +0.15 | 3.07 |

**Same-season is roughly three times bigger at every position** (QB +3.62, RB +1.73, WR +0.51,
TE +0.67). **Two thirds of the apparent matchup effect is information you do not have when you
choose.** `[TESTED]`

> **RULE: never move a receiver or a tight end for a matchup. It is measured at zero.** At
> quarterback it is worth about a point a game — a tiebreak between two streamers, exactly as the
> page claims, and now with the number behind it.

### 3b. AND THE DEFENCE IS THE OTHER WAY ROUND — this is the one that changes behaviour

D/ST weekly points against the opponent OFFENCE, prior season, n=2,174:
**coefficient −0.195, p < 0.00001, swing −2.22 fantasy points** across an opponent range of 17 to
28 points a game.

**The spread between the DEFENCES themselves is 2.06.**

> **So at D/ST the matchup is worth slightly MORE than the difference between the units.** Doc 212's
> headline — *the defence matchup is bigger than the defence* — reproduces on prior-season data,
> which is the version you can act on. `[TESTED]`

**PUT THE TWO TOGETHER, because they point opposite ways and that is the useful part:**

| | matchup swing | player spread | matchup as a share of it |
|---|---|---|---|
| **D/ST** | 2.22 | 2.06 | **108% — chase the matchup** |
| QB | 1.13 | 4.84 | 23% — chase the player |
| RB | 0.56 | 5.18 | 11% |
| WR | 0.09 | 4.29 | 2% — ignore it |
| TE | 0.15 | 3.07 | 5% — ignore it |

**AT DEFENCE, TAKE THE SCHEDULE. AT EVERY OTHER POSITION, TAKE THE PLAYER.**

## 4. WHAT THIS CHANGED IN THE SHIPPED CODE

`wire.py`'s weeks-ahead section was built an hour before this was measured, and it ranked both
quarterbacks and defences by opponent. **The defence half is right and now has a number. The
quarterback half needed its claim shrunk, not removed** — the page said "a tiebreak, never a reason
to start a bad one," which the measurement supports at about a point a game. Wording tightened to
carry the size.

## 5. OPEN

- **Every `[OPEN]` line in §1.** The biggest are row G (bye/trade arbitrage — his idea, entirely
  unsearched) and row H (*denying a handcuff to the man who owns the starter* — his idea, and I
  found nothing published on it at all).
- **Snap share as a leading indicator** — we hold the data, the test is not run.
- The catalog in doc 226 §5 is unchanged and still comes first: trades, standings, drops.
