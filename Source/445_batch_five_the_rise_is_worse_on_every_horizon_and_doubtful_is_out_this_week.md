# 445. BATCH FIVE: THE RISE IS WORSE ON EVERY HORIZON, A DOUBTFUL MAN IS OUT THIS WEEK, A DID-NOT-PRACTICE IS NOT, AND THE FEED QUESTION IS LOGGED

*29 Sept 2026, night. Claude (Cowork), batch five of "complete the to do list... in batches to ensure fidelity": the two
NOT YET RUN measurements left on `claude_todo.txt` after docs 440 to 444. 445 reserved by listing `Source\` at 19:45 ET.
No em dashes.*

---

## 0. WHAT TO DO

1. **The wire's IN DOUBT lane now skips a cover who is himself Doubtful.** On the final injury report of every week from
   2021 to 2025, a Doubtful running back, receiver or tight end played once in 231 (0.4%); an Out man once in 1,435.
   Doubtful is Out for the week, so a Doubtful cover covers nothing this week. The stash lane keeps Doubtful on purpose:
   it is a rest-of-season bet, and a Doubtful man is back sooner (54% still out the next week against 68% for Out).
2. **A did-not-practice with no game designation is NOT a step-past trigger and stays a printed line**: three in four
   play (75%, n=391); at running back it is a coin flip (58%, n=80); a Questionable man who did not practice Friday is
   under one in two (46%, n=310). Nothing on either lane acts on the practice status.
3. **The rise in snaps and targets is worth nothing on eight weeks or the rest of the season either, and the longer the
   horizon the worse the riser looks**: net of the week's levels, minus 6.7 points of startable on four weeks, minus 7.7
   on eight, minus 8.8 on the rest of the season, minus 10.5 on the best four-game stretch inside the next eight; every
   season, every position; the raw gaps shrink to +0.8, +0.1 and +0.3. Finding 4.38's four-week caveat is closed: read
   the level, and "a role that could expand" does not live in the rise.
4. **Whether the report's designation ever leads or lags ESPN's live status is BLOCKED on history and now filling
   forward**: no file holds ESPN's status day by day, so `wire.py` logs the pair every run to `Source\status_pairs_2026.csv`
   (ESPN status beside report status and practice status, one row per seat-lane man per date). The comparison runs when
   the file holds a few weeks.
5. **The v9.35 proposal grows by two index rows**: 4.38 rewritten without numbers to carry the long horizons, 4.42 added
   (the injury report's designation as the this-week signal). `diet_check.py` still passes; the README carries the new
   price (87,461 bytes, 11.7%). Doc 444 carries a banner saying so. Your go-or-no line is unchanged.
6. **Nothing to run.** `wire.py` is re-pinned; the two scripts are in `Scripts\research\wk1\` with their runs.

---

## 1. THE RISE ON A LONGER HORIZON (finding 4.38 addendum)

Testable form, stated before the run: doc 440's TEST 3 population (RB, WR and TE not startable in week w, REG 2021 to
2025, weeks 2 to 16, n=9,999) and predictors (both snap share and targets rose from the previous game, entered beside the
week-w levels); outcomes startable over the next four weeks (2+ rows), eight weeks (4+ rows), the rest of the season (4+
rows), and the best four-game stretch inside the next eight clearing the bar; direction, a rise adds over the levels on the
longer horizons where it did not on four; falsifier, under +3 points net of the levels on every horizon.

| horizon | both rose, net of levels, pooled | RB | WR | TE | raw gap, both rose minus the rest |
|---|---|---|---|---|---|
| next four weeks (n=9,393) | minus 6.7 (se 0.9) | minus 6.2 | minus 7.9 | minus 6.4 | +1.9 |
| next eight weeks (7,308) | minus 7.7 (1.0) | minus 9.2 | minus 7.6 | minus 8.2 | +0.8 |
| rest of the season (7,527) | minus 8.8 (1.0) | minus 11.4 | minus 8.2 | minus 9.1 | +0.1 |
| best four inside the next eight (7,308) | minus 10.5 (1.2) | minus 10.3 | minus 10.9 | minus 10.8 | +0.3 |

By season on eight weeks: minus 7.3 to minus 8.4. The strict rise (10+ snap points and 3+ targets) minus 7.4 to minus
11.2. For scale, the level: startable over the next eight by targets in week w, 0 to 2 targets 9.8%, 3 to 4 17.1%, 5 to
7 24.5%, 8 or more 31.8%. The four-week row reproduces doc 440 to the decimal. Script `rise_horizon.py`, output
`run_rise_horizon.txt`.

## 2. THE INJURY REPORT AS A THIS-WEEK SIGNAL (finding 4.42)

Testable form: every RB, WR and TE row on a week's injury report, REG 2021 to 2025, the week's final report as nflverse
carries it (n=7,464 after five bye rows), joined on gsis_id to snap counts and the weekly stat file; predictor the game
designation crossed with the practice status; outcome played an offensive snap or had a touch that week; the decision it
feeds, whether `next_man_up()` and `in_doubt()` should step past a Doubtful man and whether a did-not-practice with no
designation earns a flag.

| the final report says | played that week | n |
|---|---|---|
| Out | 0.1% | 1,435 |
| Doubtful | 0.4% | 231 (every season 0.0 to 2.3%) |
| Questionable, did not practice | 45.8% | 310 |
| Questionable, limited | 67.2% | 1,232 |
| Questionable, full | 69.4% | 386 |
| no designation, did not practice | 74.9% | 391 (RB 57.5% of 80; WR 79.6%; TE 79.0%) |
| no designation, limited or full | 92 to 93% | 3,444 |

How far a designation reaches: of men Out in week w, 68.0% are still not playing in w+1 and 48.9% in w+2 (n=1,241 and
1,180); of men Doubtful, 53.8% and 33.9% (n=195 and 186). One word, two lanes, two horizons: the IN DOUBT lane is a claim
for this Sunday and treats Doubtful as Out; the stash lane is a bet on the season and keeps him. The change is one set in
`in_doubt()`'s cover filter; the negative control (the same rows with the cover Active) reproduces the old output.

What this cannot test: the report against ESPN's live status. Both are the same official designations and ESPN's is live,
so the practice file can only add the mid-week practice status before Friday's designation exists, and the historical file
holds the final report only. The input that settles it is named and now logged (`log_status_pairs()` in `wire.py`, appended
once per run date, never rewritten; a failure prints one line and takes nothing down). Script `practice_out.py`, output
`run_practice_out.txt`.

## 3. OPEN, BY NAME

- **Matt's:** go or no on v9.35; the two claim-order runs each week; the routes purchase; the ESPN D/ST box score.
- **NOT YET RUN:** the status-pairs comparison, when `status_pairs_2026.csv` holds a few weeks; the 4.34 keeper-riser
  column from week 10; the trim of the other three pages (doc 439); the Wednesday and 6 October runs (doc 439); a second
  diet batch on the v9.12-and-earlier blocks if v9.35 is accepted.
- **BLOCKED on Matt:** the prior Opus research chat.
