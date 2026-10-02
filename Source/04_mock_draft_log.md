# Mock Draft Log Protocol

**Purpose: make mocks 2, 3 and 4 worth more than mock 1 was.** Board v2.1 is unchanged by the re-paste — same mock, already absorbed.

---

## 1. FIRST, THE QUESTION THAT DETERMINES EVERYTHING

**Does Draft Wizard's Draft Intel model your eleven actual managers, or generic drafters with league-shaped tendencies?**

This decides what a mock can and cannot tell us:

| If Draft Intel encodes **your** managers | If it's generic |
|---|---|
| Mocks test the Snyder-takes-Allen hypothesis | They can't — Draft Wizard doesn't know Snyder |
| Mocks test the TE +15 lag | They can't — the lag *is* your league's deviation from national behavior, so a generic mock reproduces the thing I calibrated away from |
| Availability numbers transfer directly | Availability is national ADP + noise, useful only as an ADP sanity check |

**One clue from mock 1 pointing toward the optimistic answer:** Allen has ADP 20. Under a pure national-ADP model he reaches pick 17 about **93%** of the time. He didn't. That's a 1-in-14 event under the null, in exactly the predicted direction — weak evidence (n=1, p≈0.07), but it's evidence.

If you can tell me which it is, that alone changes how much weight the next three mocks carry.

---

## 2. WHAT TO LOG — six numbers, about a minute

Per mock, from the pick history:

| # | Log this | Why |
|---|---|---|
| 1 | **WRs taken in picks 1–7** | The Taylor mechanism. 3 WRs → he's there 1%; 4 WRs → 88% |
| 2 | **Was Josh Allen gone before pick 17?** Y/N, and at which pick | Snyder hypothesis |
| 3 | **QBs gone by pick 17, and by 32** | League QB pace |
| 4 | **TEs gone by pick 32** — and where Bowers and McBride went | The TE lag. **Highest-value number on this list, see §4** |
| 5 | **RBs gone by pick 17** | RB pace; currently my weakest-supported calibration |
| 6 | **Your five picks and what you passed on** | Sequence check |

**Better still: the raw pick order for picks 1–32.** All six numbers fall out of it, plus everything I haven't thought to ask for. If you can copy/paste or screenshot that, do that instead of tallying.

---

## 3. DECISION THRESHOLDS

Model predictions, so you can read a mock without waiting on me:

| Statistic | National-ADP model | League-calibrated model | Your league, 2024–25 |
|---|---|---|---|
| WRs in picks 1–7 | 3.33 | 3.33 | — |
| RBs gone by 17 | 9.6 | 9.4 | **7.5** |
| QBs gone by 17 | 0.07 | 0.88 | **1.0** |
| QBs gone by 32 | 1.65 | 1.79 | **3.0** |
| TEs gone by 32 | 2.10 | 1.95 | **0.5** |
| P(Allen gone by 17) | 0.07 | 0.88 | — |
| P(Taylor at 8) | 0.29 | 0.29 | — |

**Evidence per mock:** Allen gone before 17 carries a likelihood ratio of **12.4 : 1** for the calibrated model over the national one. **Three mocks with Allen gone every time ≈ 1,900 : 1** — that settles it, conditional on §1.

Note rows 2 and 5: even my calibrated model is slower on QB and faster on RB than your league's actual history. Both gaps are real but rest on two drafts, which is why I didn't shift them. Mocks are the cheapest way to add sample.

---

## 4. WHERE MORE MOCKS WOULD MOST CHANGE THE BOARD

**Brock Bowers at pick 32 — the single most fragile number in v2.1.**

I tried to fit the TE lag four ways against your league's actual TE pace (0 gone by 17 → 0.5 by 32 → 1.5 by 41 → 4.5 by 56):

| Model | TEs by 32 | **Bowers available at 32** | Overall fit |
|---|---|---|---|
| lag +15 *(what the board uses)* | 1.68 | **0.32** | best (SSE 4.1) |
| lag +25 | 0.56 | **0.97** | worse late (SSE 10.7) |
| floor at pick 42 | 0.90 | **0.71** | SSE 7.4 |
| floor at pick 36 | 1.88 | **0.25** | SSE 9.1 |

**No single-parameter model fits the whole curve**, because your league's TE behavior is a step function, not a shift: essentially nothing until round 4, then a burst in rounds 4–5 (12 of 43 team-seasons take their first TE in round 5 exactly).

So Bowers at 32 is **somewhere between 0.25 and 0.97**, and the board's 0.40–0.47 sits at the low end. Every model that matches the pick-32 count specifically puts him *higher* than the board says. The only datapoint pushing the other way is your mock, where he went at 3.06.

**"TEs gone by pick 32" has a small spread (sd ≈ 0.5), so three mocks gives a standard error near 0.3 — enough to separate 0.5 from 1.7 and pick the right model.** That is the highest-leverage number you can bring back.

---

## 5. WHAT MOCKS CANNOT SETTLE

Stating these so you don't spend mocks on them:

- **Whether ESPN's Josh Allen projection is right.** Worth ~25 points of the pick-8 decision, and no mock touches it. Only in-season data would.
- **Who panics during a run.** Draft Wizard bots don't panic the way a room does. Still the largest unmodeled risk.
- **Keeper declarations.** Nine of twelve are still predictions. Only the 7:00 PM lock resolves them, and Snyder's is load-bearing — if he keeps a QB rather than Etienne, the whole Allen line reverses.
- **Pick Predictor survival percentages.** You're right that "% Experts" is a different quantity. If those percentages aren't reachable, my simulated numbers stand with the lower-bound caveat from §1 of the board. Not worth hunting further.

---

## 6. RUNNING TALLY

| Mock | Date | WR top-7 | Allen <17 | QB by 17 / 32 | TE by 32 | RB by 17 | Taylor at 8 |
|---|---|---|---|---|---|---|---|
| 1 | Aug 2026 | **4** | **Y** | — | ≥1 (Bowers 3.06, McBride survived) | — | **Y** |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |

Mock 1's blanks are what I couldn't recover from the summary. Fill the rest and the model updates on all six axes at once.
