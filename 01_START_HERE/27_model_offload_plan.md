# 27 — OFFLOAD PLAN: WHICH MODEL DOES WHAT, AND THE EXACT PACKAGE FOR EACH
**Aug 23, 2026.** Written to your standing constraint: Claude Pro tokens are the scarce
resource. Claude keeps only the work that needs the project's files on disk and the integrity
harness. Everything else moves.

---

## THE HEADLINE IDEA — how to get a measurable breakout hit-rate for free

You cannot score an analyst's **2026** breakout calls yet. You **can** score their **2024 and
2025** calls, because the outcomes are already in this project
(`espn_projections_2026_20260820.csv` carries `proj_2025` and `actual_2025`; the 2025 league
draft is in `draft_history_2021_2025.csv`).

Those old calls are sitting in public YouTube podcast archives, free, outside every paywall.
The August "sleepers and breakouts" episode is the single highest-signal artifact each analyst
produces, and they all make one.

**So the pipeline is:**

1. **Gemini Notebook** ingests the August 2024 and August 2025 breakout episodes for each
   analyst and extracts every named call with a timestamp.
2. **You paste that list back here.** It is small — maybe 200 rows.
3. **Claude scores it** against actuals already on disk and returns a hit rate per analyst,
   with a base rate to compare against.
4. **Only the analysts who clear the base rate** get their 2026 calls loaded onto the board.

That produces exactly what you asked for: a loosely derived but **measured** value, at zero
cost, and it is the only design I can find that scores breakout skill instead of proxying it.

---

## THE STANDARD HEADER — paste at the top of ANY model, every time

This is the guardrail transfer you asked for. Without it they invent patterns.

```
You are working on one specific fantasy football league. Rules that override your defaults:

1. Never state a statistic, ranking or projection that is not in a source I gave you.
   Write [NO SOURCE] instead. Do not fill gaps from memory — your training data is stale.
2. Every claim gets a tag: [SOURCED: file, date] · [TESTED: statistic, n] · [HYPOTHESIS].
3. Every finding must carry three things or it is not a finding: what it was measured
   AGAINST, WHICH population, and the SAMPLE SIZE.
4. A proposal with no falsifier is not a proposal. State the result that would kill it.
5. If n is small, the word is UNDERPOWERED, not "no effect".
6. Do not count in rounds in this league. Count in overall pick numbers.
7. LEAGUE: ESPN, 12 teams, 15 rounds, snake, slot 8. 0.5 PPR. SIX-POINT PASSING TDs.
   Start 1QB 2RB 2WR 1TE 1FLEX 1DST 1K. One keeper per team, charged to round 15, but all
   12 keepers leave the board BEFORE pick 1. My 14 picks: 8, 17, 32, 41, 56, 65, 80, 89,
   104, 113, 128, 137, 152, 161. Playoffs weeks 15-17. First place is 44% of a $1,200 pot.
8. Almost every public ranking assumes full PPR and 4-point passing TDs. Ours does not.
   Say so whenever you use one.
```

---

## THE ASSIGNMENTS

### 1 · Gemini Notebook — **PRIMARY. The breakout hit-rate corpus.**
**Why here:** it ingests YouTube links directly, transcribes them, and answers only from the
sources you add. Roughly 50 sources per notebook, which is enough for 5 analysts × 2 years × 4
episodes. This is the single job no other tool of yours does well.

**Sources to add** — search YouTube for each and take the August episodes from 2024 and 2025:
```
Late-Round Fantasy Football        (JJ Zachariason)   — "sleepers", "breakouts", "draft guide"
The Fantasy Footballers            (Ballers)          — "Breakout Players", "Sleepers", "Busts"
Fantasy Life                       (Dwain McFarland)  — "utilization", "breakouts"
Yahoo Fantasy Forecast             (Matt Harmon)      — "Reception Perception", "breakouts"
Establish The Run                                     — August draft-strategy episodes
The Action Network Fantasy         (Chris Raybon)     — RB #3 on measured multi-year accuracy
```
**Prompt to paste after the standard header:**
```
From the sources in this notebook only, extract every instance where an analyst names a
specific NFL player as a breakout, sleeper, league-winner, or significantly undervalued
relative to his draft price. Ignore general praise. I need an explicit call.

Return a CSV, no prose, these columns exactly:
analyst,show,episode_date,player,position,call_type,conviction,quote,timestamp

call_type   = breakout | sleeper | league-winner | undervalued | bust
conviction  = strong | moderate | passing-mention   (judge from the language used)
quote       = under 20 words, verbatim
episode_date = YYYY-MM-DD

Rules: one row per call. If the same analyst names the same player in two episodes, two rows.
Do not include a player unless a named analyst made the call in one of these sources.
If you cannot find the episode date, write UNKNOWN — do not guess.
```
**Then:** paste the CSV back here. Claude scores it.

---

### 2 · GPT 5.6 Think Deeper — **the breakout metric search**
**Why here:** its stated strength is statistical reasoning over advanced-stat sources, and it
is the model most likely to name a metric this project has not already killed.

**Give it:** the standard header, plus `claude/26_breakout_economics.md` and this list of
**twelve factors already tested and dead** so it does not resell them —
offensive scheme · targets per route run · yards per route run · pass rate over expected ·
NFL draft capital · year-2 experience leap · vacated targets · strength of schedule ·
ranker disagreement · manager positional timing · athleticism · contract year · breakout age ·
BMI · offensive-line quality for running backs · handcuffs · ambiguous backfield ·
elite TPRR with few routes.
**Surviving:** red-zone opportunity stickiness (inside-10 targets r=+0.59, RZ target volume
r=+0.51, RZ target share r=+0.48; **RZ TD rate r=+0.02, noise**) and after-contact ability as
a tiebreaker only.

**Prompt:**
```
Every factor in the DEAD list has been tested against 2024-2025 outcomes and failed either
year-over-year stickiness, out-of-sample gain over prior-year points per game, or survival
after controlling for volume. Do not propose any of them again.

Propose five NEW candidate predictors of a fantasy breakout that are (a) observable before
Labor Day, (b) obtainable free or under $30, and (c) not a restatement of a dead factor.

For each: the metric · the exact URL it comes from · the cost · the statistical gate it must
clear · the specific result that would make you abandon it.
Rank them by expected value per dollar. A proposal with no falsifier does not count.
```

---

### 3 · Gemini 3.1 Pro Deep Think — **the objective-function question**
**Why here:** it is your best reasoning model and this is the hardest open question in the
project, with no data-wrangling attached.

**Give it:** standard header + `claude/21_backtest_2025_holdout.md` + `claude/26_breakout_economics.md`.
**Prompt:**
```
Two results are in tension.

A) The greedy value rule's outcome variance is 14% of a real manager's (sd 76 vs 202 across
   twelve managers, one season) and it lost to exactly the three managers rated best.
B) Total roster surplus over draft cost correlates -0.783 with final seed (p=0.003, n=12),
   and only the two positive-surplus rosters finished first and second.

Payouts: 1st $525, 2nd $225, 3rd $150, 4th $85, 5th/6th $25, of a $1,200 pot. Six of twelve
teams make a three-week single-elimination playoff in weeks 15-17.

Question: what is the correct objective function? Show the mathematics. Specifically, at what
point does added variance stop buying championship equity and start destroying it, given this
payout curve and a six-team bracket? Give me a number I can put in a draft policy, not a
philosophy. State your assumptions and what would falsify your answer.
```

---

### 4 · Gemini Spark — **injury and depth-chart monitoring, Aug 24 → Sep 7**
**Why here:** it is the only thing you have that runs unattended. This replaces a manual
checkpoint and is the highest-value automation before the draft.
**Set up one standing task:**
```
Every morning at 7am through September 7, check for news on these players and report only
CHANGES since yesterday: [paste the 30 names from the board's top 30 by VBD].
Report: player, what changed, source, date. Flag anything that moves a depth chart, a
practice status, or a starting role. No summaries of unchanged situations.
```

---

### 5 · Google Antigravity — **the missing historical inputs**
**Why here:** the multi-year backtest is blocked on one thing only, and this is your code-
execution tool.
**Task:** pull **dated August preseason ADP and projections for 2022, 2023 and 2024** from
`github.com/nflverse/nflverse-data` and `github.com/FantasyFootballAnalytics/ffanalytics`.
Output one CSV per year: `player, team, position, adp, projected_points, source, capture_date`.
**This unblocks:** re-running the manager-level backtest on three more seasons, which is the
falsifier for the entire variance hypothesis.

---

### 6 · Gems — **the draft-night assistant**
Build one Gem pre-loaded with the standard header plus `claude/constants_2026.csv` and
`claude/positional_deadlines_v5.csv`. Its only job on the night is 60-second tiebreaks in the
league's actual scoring. **Test it before Sept 7** with three questions you already know the
answer to.

### 7 · Gemini 3.1 Pro — mock draft scenarios and roster-construction brainstorming.
### 8 · GPT 5.5 Quick — live 60-second tiebreaks as a backup to the Gem.

---

## WHAT STAYS WITH CLAUDE

Only four things, all of which need the files on disk or the assertion harness:

1. Scoring anything another model brings back, against actuals already in the project.
2. The spine rebuild, the integrity harness, and the two artifacts.
3. The Sept 5 refresh and the Sept 7 keeper-lock rebuild.
4. Red-teaming any finding before it changes a draft-day pick.

**Everything else should leave.**
