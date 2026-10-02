# 235 — "Wait for a bench guy to pop, then trade him": half right, and the half that matters is the workload

**2026-09-08, evening.** Matt: *"sometimes I'll wait for players on my bench to pop before I
approach a trade."*

**THE TESTABLE FORM, stated before the run (§0.5(a2)) — and it is only ONE of the two claims in
his sentence:** *among skill players who already have a role, does a single big week predict the
next three weeks ABOVE that player's own pre-spike baseline, compared with a matched player who
had an ordinary week?* If the answer is no, the pop is a pricing window and selling into it is
free. **If the answer is yes, selling into a pop gives away real improvement, and the instinct is
backwards.** The second claim — that a league-mate will PAY more right after a pop — is about the
market, not the player, and it is **not tested here** (§4). If that second one is what he meant,
one word re-aims this.

---

## 0. ACTIONABLE

1. **A pop DOES carry forward. +1.73 points a week** over the next three, against a matched flat
   week (95% CI +1.24 to +2.22). **So on average, selling into a pop sells a real improvement.**
2. **But essentially all of it is WORKLOAD.** A pop where his touches also jumped carries
   **+2.65**; a pop where the touches were flat carries **+0.20**.
3. **THE RULE THAT COMES OUT OF THIS: sell the touchdown pop, keep the workload pop.** A 2-TD week
   on flat volume carries **+0.38** — that is the selling window. Two big box scores can look
   identical and be worth 2.5 points a week apart.
4. **Check carries + targets, not the points.** That one column is the whole test.
5. **RB pops carry hardest (+2.36 over flat), TE +1.37, WR +1.21.** So the back who pops is the
   worst one to sell and the receiver who pops is the best.
6. **ROSTER-SPECIFIC: do not run this play on Mike Washington Jr.** His pop only happens if Jeanty
   is out, which is a workload pop by construction and the exact week Matt needs him.
7. **The waiting has a deadline: the week-11 bye trade must be done by about week 9.** A trade made
   in week 11 fixes nothing.
8. **`py waivers.py` is what answers the untested half** — it writes `trade_report_<year>.csv` for
   the first time. Already on his list; this is a second reason.

---

## 1. THE MEASUREMENT

**POPULATION:** every RB/WR/TE player-week, 2022–2025 regular season, weeks 1–14 (nflverse
`stats_player_week`, fetched 2026-09-08), restricted to players who **already had a role** — at
least three prior games that season and a trailing average of 4.0+ points. **3,613 player-weeks,
370 distinct players.**
**SCORING:** §2's rules for skill positions — 0.1/yd, 6-pt TD, 0.5 PPR, −2 fumble lost, 2-pt = 2.
**BASELINE — state it every time: the player's OWN mean over his prior games that season.**
**OUTCOME:** mean of his next three games minus that baseline.
**CONTROL:** the same quantity for player-weeks that came in **within 3 points of baseline** — an
ordinary week. Comparing forward against the PRE-spike baseline, and against a matched control,
is what keeps this from being plain regression to the mean (§4.23's trap: selecting on a high week
guarantees a fall if you measure it against the high week).
**Confidence intervals bootstrapped 4,000× resampling PLAYERS, not player-weeks** (`ERROR_PATTERNS`
A5 — the same player contributes many rows).

| group | n | baseline | **next 3 weeks minus baseline** |
|---|---|---|---|
| **POPPED** — week ≥ baseline+10 and ≥15 pts | 278 | 9.83 | **+1.84** |
| **FLAT** — week within 3 of baseline | 1,285 | 8.61 | **+0.12** |
| | | **difference** | **+1.73, CI [+1.24, +2.22]** `[TESTED]` |

**So the naive form of the instinct is wrong: a pop is not noise.** The man who pops is a
genuinely better player over the following month, by about a point and three quarters a week.

## 2. AND IT SPLITS CLEANLY ON ONE COLUMN

Within the popped group, by whether **touches (carries + targets)** also jumped:

| the pop was… | n | **next 3 weeks minus baseline** |
|---|---|---|
| **workload jumped too** (+4 touches or more) | 143 | **+2.65** |
| **workload flat or down** (+1 or less) | 63 | **+0.20** |
| | **difference** | **+2.45, CI [+1.38, +3.51]** `[TESTED]` |
| **2+ TDs on flat workload** | 41 | **+0.38** |

**This is §4.5 showing up in-season.** That finding measured volume as sticky (red-zone target
volume r=+0.51, red-zone target share r=+0.48) and **red-zone TD rate as noise (r=+0.02)**. The
same split governs a single week: the volume half of a pop persists, the efficiency half does not.
**The pop is not the signal. The touch count inside the pop is the signal.**

## 3. BY POSITION

| pos | popped | flat | difference |
|---|---|---|---|
| **RB** | +2.54 (n=116) | +0.19 | **+2.36** |
| TE | +1.63 (n=47) | +0.26 | +1.37 |
| **WR** | +1.23 (n=115) | +0.02 | **+1.21** |

Directionally consistent with §4.19's asymmetry — the back who takes over keeps taking over, and
the wire cannot replace him. **A popped back is the worst asset on the roster to sell; a popped
receiver is the best.**

## 4. THE HALF THIS DOES NOT TOUCH — AND IT IS THE HALF HE ACTUALLY ASKED ABOUT

His sentence contains a claim about the **market**: that a league-mate will offer more for a man
who just scored 22 than for the same man a week earlier. **Nothing here tests that**, and it is the
claim that decides whether the strategy pays. If the premium a rival pays exceeds the +1.7 of real
improvement being handed over, waiting wins; if not, it loses.

**It is now measurable and was not before.** `waivers.py` was rewritten this morning and writes
`trade_report_<year>.csv` — **every trade in this league's four-season history, which had been
pulled and thrown away every time** (doc 233 / doc 226). Until that file exists, this is
`[HYPOTHESIS]`, and his read on how this league's managers behave has been right nearly every time
it has been checked (`ERROR_PATTERNS` F4), so the prior is with him.

**One thing that is already known and cuts against the waiting, from the directive rather than
from a fresh measurement:** §2 records **about 3 trades league-wide per season**, behavioural not
rule-imposed — and that number itself has never been read out of the feed. **In a market that
clears three times a year, "wait for the right moment" may mean waiting past the moment the trade
was supposed to fix.** His own week-11 hole is the case: the trade has to land by roughly week 9.

## 5. OPEN

- The market half of §4 — needs `trade_report_*.csv`, then: do accepted trades cluster in the week
  after one side's player posted a spike?
- Whether the +1.73 is bigger for players **off** a roster's starting lineup specifically (his
  actual population is bench men, and this test did not condition on that — a bench player has a
  lower baseline by selection, and the test floor was 4.0 points).
- Two seasons of the four are the same seasons §4.5 was fitted on; this is not an independent
  replication of that finding, it is the same relationship measured on a different object.
