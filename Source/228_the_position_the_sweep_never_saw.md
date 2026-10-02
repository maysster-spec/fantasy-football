# 228 — D/ST and K were excluded from every waiver measurement in this project. He was right, and one of his two claims survives.

**2026-09-08.** Matt: *"I thought I even had luck with kicker when matchup is also factored. I
thought this is what allowed me to pickup players early though you didn't find evidence for it.
I'm not certain you considered other meaningful factors and circumstances. I know it's true for
defense and ST, but concerning you didn't pick that up with your sweep."*

**He is right about the sweep, and the reason is worse than an oversight in the analysis — the data
was never in it.**

---

## 1. THE DEFECT — 27% OF ALL WAIVER ACTIVITY, NEVER MEASURED

Doc 205 states its population as *"982 executed adds, 2022–2025, **D/ST excluded**."* Docs 224, 225
and 226 inherited that population without restating the exclusion, and my scoring function made it
permanent: `REPL = {'QB','RB','WR','TE'}` and `if pos not in REPL: continue`. **A defence has no row
in nflverse's player-week table, so every D/ST add fell out silently.**

**In 2024 alone, 174 of 649 waiver adds were defences.** Across 2022–2025 there are **248 executed
D/ST adds** and **126 kicker adds**. §4.16 already recorded that D/ST is the most-streamed position
in this league at 5.17 adds per team-season. **So the single most-churned position was the one the
sweep could not see, and every sentence this project has written about "waivers" means "waivers at
the four skill positions."**

**This is `ERROR_PATTERNS` A-class:** the exclusion was stated once, correctly, in the doc that made
it — and then it became invisible because nothing downstream repeated it. **His instinct that
"other meaningful factors and circumstances" were missing was not a hunch about the model. It was a
correct read that the population was wrong.**

## 2. D/ST STREAMING — MEASURED FOR THE FIRST TIME, AND IT WORKS

**POPULATION: 248 executed D/ST waiver adds, 2022–2025, this league, mapped from the transaction
nickname to the team code. BASELINE — state it every time: the added defence's fantasy points in
the week of the add, against the MEDIAN defence that week.** The median is the right comparator
because streaming is a within-week choice: the alternative is not "nothing," it is any other
defence.

| | n | beat the median defence | points over the median |
|---|---|---|---|
| **whole league, week of the add** | 227 | **55.9%** | **+1.92 per start** |
| whole league, the week after | 222 | 45.9% | +0.67 |

**Streaming a defence is a real, positive act in this league: about two points a start over taking
whoever.** `[TESTED]` Nothing in this project has said that before, in either direction.

### 2a. AND THE MATCHUP IS WHAT DRIVES IT — his claim, confirmed

Regressing how far each add beat the median on **the opponent's PRIOR-season points scored** (the
forecastable version, not hindsight):

> **−0.267 points per point the opponent scored last year · se 0.105 · p = 0.011 · n = 227.**
> **Across the realistic opponent range that is a 3.0-point swing.** `[TESTED]`

**This is measured on real adds by real managers in this league**, and it is a second, independent
confirmation of doc 227's team-week result (−0.195, p<0.00001) and of doc 212's headline. **The
matchup is the whole of the skill at D/ST.**

### 2b. HIS TIMING SHOWS UP HERE — AND ONLY HERE

| | week OF the add | the week AFTER |
|---|---|---|
| **Matt** (n=28) | 50.0% · +0.89 | **57.1% · +1.62** |
| the other eleven (n=199 / 194) | 56.8% · +2.07 | 44.3% · +0.53 |

**The field's adds are good in the week they add and bad the week after; his are the other way
round.** That is precisely the shape of a manager buying a defence a week before he needs it — his
claim, in the population where he said it was true.

**n = 28. Nothing here is resolved and I am not going to pretend otherwise.** But it is the first
time his pattern has appeared at all, and it appeared the moment the right population was used.
**Doc 226's "being early does not work" was measured on skill positions only and must not be quoted
against this.**

## 3. KICKER — NOT SUPPORTED, AND THIS IS THE HALF THAT DIES

Kicker adds were resolvable after all: nflverse gives a kicker's team per season, and `k_weekly`
gives that team's kicking points per week. **123 of 126 adds mapped.**

| | n | beat the median kicker | points over the median |
|---|---|---|---|
| whole league | 123 | **45.5%** | +0.60 |
| Matt | 7 | 57.1% | +1.71 |

**And matchup does not drive it: −0.030 per point the opponent allowed last year, p = 0.83, swing
−0.23.** `[TESTED — NULL]`

**So of his two claims, the defence one is confirmed and the kicker one is not.** His own kicker
record is seven adds, which is not a record. **Do not carry a kicker matchup rule.**

## 4. WHAT THIS CHANGES

1. **Every waiver finding in docs 205, 224, 225 and 226 must be read as "at QB, RB, WR and TE."**
   Not retracted — rescoped. The sentence "the wire produces startable bodies regularly and
   league-winners almost never" is true of skill positions and says nothing about defences.
2. **The D/ST half of `wire.py`'s weeks-ahead section is now confirmed twice** — on team-weeks and
   on this league's own adds. Its instruction stands: at defence take the schedule.
3. **The kicker gets no matchup line anywhere.** It was never on the page; it does not go on now.
4. **`waiver_hits.pkl` and the scoring path that built it are skill-only by construction.** Anything
   built on them inherits that. Say so at the top of the next thing that uses them.

## 5. HIS STANDING REQUEST, NOT YET BUILT

*"we need to look at teams and player trends as the season goes on at every position."*

**Nothing in this project tracks in-season trend.** Everything is preseason or full-season. The
computable version is doc 227 §1 row B — rolling snap share, target share and touches, week over
week, with the change flagged rather than the level. **We hold snap counts 2021–2025 and weekly
usage; we do not hold routes run.** That is the next build, and it is the thing that would let the
Tuesday sheet say *"this man's snap share went 34% → 58% → 71%"* instead of only *"here is what he
is worth."* Not started.

## 6. OPEN

- The 28-add timing pattern needs more seasons or a different league to resolve. It cannot be
  settled here.
- Kicker: measured null on matchup, but **nothing tested weather, dome, or the team total**, which
  is what a kicker streamer would actually claim. Named so it is not read as a closed file.
- Doc 226 §5's catalog is still first: trades, standings, drops.
