# 463. THE CONTROLS FOR A MORNING OF CHANGES, AND THE CLAIM THAT LANDS BY RANK

*1 Oct 2026, 09:45 ET. Claude (Cowork). Matt, 1 Oct 09:05: "We covered a lot of ground this morning. Do we have
controls in place to be sure the updates are set? ... anything more you can run on the claude todo list? ... any new
metrics come to mind?" 463 reserved by listing `Source\`. No em dashes.*

---

## 0. WHAT TO DO

1. **Paste directive v9.38 into the project's custom instructions** (on your list). Findings 4.44 to 4.48, the open-job
   rule, the tail posture rule, the crowd check line, the IR-cap line. Nothing retracted.
2. **Nothing else to run.** Tomorrow's 07:30 run carries the waterfall's measured rank term and runs the three new
   checks; every RESULT term should still read 0.
3. **Your question, answered honestly: this morning's changes now have controls; until this doc two of the three did
   not.** Section 1 says which guard reads which change, and what no guard reads.
4. **A number changed on the page: at your rank, a contested claim lands 24% of the time, measured, not "nothing."**
   Section 2. From ranks 1 to 4 it is 53%, from 5 to 8 36%, from 9 to 12 24% (at 11 itself, 13% on 55 claims). An
   uncontested claim lands 74 to 85% from every rank. The waterfall prints the band's number now.
5. **Four metrics that came out of the morning, each with its status** (section 3): the claim-by-rank curve (TESTED,
   above); a playoff-odds simulation that would price a ticket in the unit you actually care about (BLOCKED on the
   league schedule, which `wire.py` can read off the next run); the tail on the latest game's level rather than the
   four-week average (NOT YET RUN); whether ESPN's +/- predicts contention in this league (accruing, mid-October).

---

## 1. THE CONTROLS, CHANGE BY CHANGE

| the change | the guard that reads it | shown to fire on |
|---|---|---|
| the long-shot lane (doc 461) | `check_page_logic.py` P6: only free men on it, no third-string shape, above the seat list exactly when the standings file puts you outside the top six; and `check_plain.py` (it fired once on a draft note with a sample size) | six controls: a rostered man, a third-string row, the lane leading while 3rd in points |
| the tail cells in `sheet_constants.json` | `tail_tickets.py --check` re-fits all ten cells from the nflverse files and fails on any drift (5 seconds) | a cell set to 0.20 against a computed 0.136 |
| the waterfall (doc 462) | P7: the rank it prints is the standings file's; CLAIM and ADD agree with the wire's own `avail`; the hedge man neither starts by value nor sits in the IR slot | a wrong rank, a CLAIM on a free agent, a starter as the hedge, a parked man as the hedge |
| the by-rank term (this doc) | `claim_rank.py --check` re-fits the three bands from the waiver reports and the scoreboard file and fails on drift | a band set to 0.30 against a computed 0.238 |
| the same-position drop (doc 462) | P5: THE CALL never names a man who starts by the roster file's own value (top QB, two RB, two WR, one TE, best remaining as FLEX, among men valued above zero); the mutation harness's own-position mutation re-aimed at the new predicate | the real 08:04 page ("drop Sam LaPorta") fires P5; the mutation is NO EFFECT on today's roster, where the cheapest men are bench receivers either way, and needs the fixture roster (catalog A5) |
| every edited file | `check_kit.py` pins (size and hash, CRLF-normalised) | stale pins fail the run |
| the directive, findings, changelog | `check_citations.py` (every `§4.x` and `doc N` cited resolves) and `audit_directive.py` (4.14's numbers) | run clean on the v9.38 set |

**What has no guard, said plainly:** the lane's cell assignment on the page (the shape words beside a man) is the
engine's own reading of the form file; no independent check recomputes a man's rank on his team. P6 checks the lane's
membership and place, not its arithmetic. The fixture roster (A5) is what would let the harness prove the own-position
mutation, and it stays on the list. The P5 starter set is the August board's value, so a man scoring now on a negative
board value (Raymond) is missed, never falsely named: a floor, labelled as one in the file.

## 2. THE CLAIM THAT LANDS BY RANK

**The claim in testable form:** in this league, the share of claims on a contested man that land falls with the
claimant's waiver rank that week, and the share on an uncontested man does not. POPULATION: every WAIVER-type claim
that reached a decision (EXECUTED or FAILED_*) in `waiver_report_2022..2025`, weeks 2 to 14, matched to the standings
rebuilt from `historical_scoreboard_2022_2025.csv` after the previous week (inverse order: fewest wins, then fewest
points for), 875 claims, 455 of them contested (two or more teams on the same man that week; claim-weighted, so not
doc 396's run-weighted 28.6%). Two team names in the reports never match a scoreboard row and their claims are left out.
`Scripts\research\claim_rank.py`; the scoreboard file is on the drive now beside the reports.

| the claimant's rank | contested claims | landed | uncontested claims | landed |
|---|---|---|---|---|
| 1 to 4 | 105 | 53.3% | 88 | 73.9% |
| 5 to 8 | 169 | 35.5% | 143 | 85.3% |
| 9 to 12 | 181 | 23.8% | 189 | 74.1% |

By exact rank the contested column is noisy at 30 to 55 claims a rank (rank 9 reads 47%, rank 12 27%), so the page
uses the band. The uncontested failures are the no-drop and limit failures of doc 435, not priority. TESTED, the
direction holds, and the waterfall's "priced at nothing" floor is replaced by the band's rate; `claims.by_rank_band` in
`sheet_constants.json`.

## 3. NEW METRICS, WITH THEIR STATUS

1. **A claim's landing rate by rank.** TESTED, section 2, on the page.
2. **Playoff odds as the unit for a ticket.** The objective is dollars against the payout table (0.3), and the
   question he asked is whether a chance taken now gets him into six of twelve. The metric: his probability of a top-six
   finish, simulated over the ten weeks left from each team's scoring to date and the league's history, with and
   without a big hit (a +15 month in the flex). BLOCKED, input named: the league's remaining schedule, which no file
   holds; `wire.py` can write it off ESPN's matchup view on the next run, and the simulation follows.
3. **The tail on the latest level.** 4.38 says the level of the newest game beats the average; the lane prints both
   (Allgeier 10.7 a game, 6 last game) and the cells are fit on the average. NOT YET RUN: refit the ten cells on the
   last game's touches and see whether the handcuff and committee cells separate more cleanly.
4. **Whether ESPN's +/- predicts contention in this league.** The wire records `own_chg` every run since 23 Sept and
   the claim log pairs his order with the outcome every Thursday; by mid-October there are enough runs to test whether
   a man at +4 is the man two teams file on. Accruing (doc 396's open line).
5. **Seat-weeks per startable week on his own bench**, the efficiency of a roster spot: how many bench weeks each man
   cost against the startable weeks he returned, this season, so the Perine-for-Barner kind of swap is judged on what
   the seat produced and not on the names. NOT YET RUN; the inputs exist (MY_ROSTER by run, the form file).

## 4. WHAT CHANGED

`check_page_logic.py`: P5, P6, P7 and `roster_starters()`; 45 controls. `sheet_engine.py`: the waterfall's contested
term reads `claims.by_rank_band`. `sheet_constants.json`: `claims.by_rank_band`; the judgement floor removed.
`research\claim_rank.py` (new, pinned, `--check`); `research\wk1\tail_tickets.py` (`--check`); `check_kit.py` pins.
`Source\historical_scoreboard_2022_2025.csv` placed beside the waiver reports. Directive v9.38, the findings file (4.44 to
4.48), the changelog, `00_START_HERE.md` version 22.

## 5. OPEN, BY NAME

- Mine: the fixture roster for the mutation harness (A5); the schedule off the matchup view and the playoff-odds
  simulation; the tail on the latest level; seat-weeks per startable week; the catalog's remaining batch (A2, A3, A6,
  B3); the payload wiring (the week blurb, `droppable`, `injured`, `rankings`).
- Matt's: the v9.38 paste; Sunday's flex and the Nacua move; the week-5 tight end; the routes purchase; the D/ST box
  score; the Opus chat and the podcasts.
