# 389. THE SPIKE WEEK CANNOT BE CALLED: 4% BECOMES 10%, TUCKER WAS 67TH PERCENTILE, AND OUR SCREEN IS ORDERED ON THE WEAK HALF OF THE SIGNAL

> **BANNER, 28 Sept 2026 (doc 435), reproduced cold from the nflverse cache (n=8,671 against 8,651 here, immaterial).** Base 4.3%, top fifth by WOPR 10.2%, targets 9.6% all reproduce. **The cross table in section 2 is mislabelled: its four cells match TARGETS x WOPR to within two rows and 0.4 points on every cell, not targets x air-yards share. On the true targets x air-yards cross: both 10.8% (n=969), air-yards only 7.3% (n=762), targets only 8.0% (n=762), neither 2.4%.** So "targets alone 6.7%, barely better than the pool" is really "targets but not WOPR"; targets alone is nearly double the pool, and the both-cell gain over targets-only is about 2.8 points (se about 1.1), not 4.1. Finding 4.35's "weak half" line is weakened, not killed; the screen ordering stands.

*22 Sept 2026, 16:40 ET. Claude (Cowork), on Matt at 16:05: "I'm not getting Tucker but I wish there was a way we
could have predicted the break out for him. We need more news and signals for these players is my guess." Doc 388 is
the previous number; 389 reserved by listing `Source\` at 16:07. No em dashes.*

---

## 0. WHAT TO DO

1. **The answer to your question is a number, and it is low: about one spike in ten.** Among receivers and tight ends
   you could have claimed, the next week is an 18-point game **4.3%** of the time. The best fifth by opportunity
   share gets to **10.1%**. Nothing gets past that.
2. **Tucker would not have been named.** After week 1 he sat at the **67th percentile** of that pool on opportunity
   share, 65th on targets, 72nd on air-yards share. The top fifth caught 2 of the 7 spikes that happened in week 2,
   and he was not one of them.
3. **Your "more signals" half is half right, and the useful half is one we already download and never print:
   air-yards share.** Top fifth on targets AND air-yards share spikes **10.8%**; **targets alone 6.7%**, which is
   barely better than the pool. The wire page screens on targets, snaps and touches, so it is ordered on the weak half.
   **Mine to fix, ledger row 165.**
4. **Your "more news" half is blocked by the clock, not by the data.** The nflverse injuries feed (practice and game
   status, 50 KB a season) is downloadable today, but the first reports for a week land Wednesday, after the Tuesday
   waiver run. It can inform a Sunday lineup or a Thursday add. It cannot inform a Tuesday claim.
5. **Paste v9.14 when convenient.** New finding §4.35 carries the ceiling so nobody hunts it again. On your list, no rush.
6. Nothing to run.

---

## 1. THE TEST, STATED BEFORE IT RAN

**POPULATION:** WR and TE player-weeks, regular season 2021 to 2025, who were **not startable in week w** on §4.13b's
bar (WR 9.62, TE 8.25 a game), had at least one target in w, and played in w+1. That is the pool a claim comes from:
**8,651 player-weeks, WR 5,699, TE 2,952.**
**PREDICTORS**, all measured in week w and all already inside the nflverse weekly file `build_form.py` downloads every
Tuesday: targets, target share, air-yards share, and WOPR (1.5 x target share + 0.7 x air-yards share, nflverse's own
column).
**OUTCOME:** a **spike** in w+1, 18.0 or more on this league's scoring, which is what Tucker's week 2 was (20.4).
Secondary: startable in w+1 on the same bar.
**FALSIFIER:** if the top fifth is no better than the pool, or no better than the top fifth by targets alone, then the
share adds nothing and the page's screen is already as good as it gets.
**Script and full output:** `Scripts\research\wk1\wopr_spike.py`, `run_wopr_spike.txt`.

---

## 2. WHAT IT SAYS

**Base rates in the pool: spike 4.3%, startable 21.2%, 5.50 points.**

| week-w signal, top fifth | spike next week | startable next week | points next week |
|---|---|---|---|
| WOPR | **10.1%** | 38.4% | 8.73 |
| targets | 9.6% | 37.0% | 8.46 |
| air-yards share | 9.2% | 35.0% | 8.18 |
| bottom fifth by WOPR | 0.8% | 7.7% | 2.78 |

**WOPR beats raw targets by half a point of spike rate, which is nothing** (about one standard error is 0.7 on each).
**The ordering gain is in the cross, and that is the part worth building:**

| week-w profile | n | spike next week | startable next week |
|---|---|---|---|
| top fifth on targets AND air-yards share | 1,220 | **10.8%** | 39.8% |
| air-yards share only | 511 | 8.4% | 35.0% |
| **targets only** | 511 | **6.7%** | 30.1% |
| neither | 6,409 | 2.6% | 15.8% |

**A man who clears a workload screen on targets alone is barely better than the pool he came out of.** Our wire flag
reads *"workload 2 of 3 (targets 8 · 84% of snaps)"*, and air-yards share is not in it.

---

## 3. THE LIVE WEEK, AND THE ABSENCE DISCOUNT

**2026 week 1 into week 2, same definitions: 122 claimable men, 7 spikes (5.7%). The top fifth by week-1 WOPR caught
2 of the 7.**

| who spiked | week-1 targets | week-1 WOPR | his percentile | week 1 | week 2 |
|---|---|---|---|---|---|
| DeVonta Smith | 6 | 0.655 | 95th | 6.8 | 22.7 |
| Davante Adams (yours) | 6 | 0.534 | 89th | 4.1 | 35.5 |
| Dalton Schultz | 8 | 0.381 | 71st | 5.5 | 20.0 |
| **Tre Tucker** | **4** | **0.362** | **67th** | **3.7** | **20.4** |
| Ja'Marr Chase | 4 | 0.282 | 56th | 2.2 | 23.0 |
| Rashod Bateman | 1 | 0.122 | 32nd | 0.0 | 18.3 |
| Jake Ferguson | 2 | 0.114 | 29th | 1.6 | 18.3 |

**What his day actually was:** 5 catches for 119 yards and a touchdown on 7 targets, with **50.5% of Las Vegas' air
yards**, against 22.1% in week 1. That is the shape of a role change, and week 3 is where it shows up or does not.
**Four of the seven came from the bottom two thirds of the ranking, which is the whole finding in one line.**

**THE ABSENCE DISCOUNT (second test, same script).** Inside the top fifth, when the team's alpha (highest target share
over the prior three weeks, at least 20%) was **out** in week w, the next week spiked **5.0%** (n=160) against **6.7%**
when the alpha played (n=1,172); startable 25.0% against 30.7%. **Direction is yours and it is about one standard
error: underpowered, and it must not be quoted as a rule.** (The rates are lower than section 2's because this pool
needs three prior weeks and a 20% alpha, so weeks 1 to 3 drop out.)

---

## 4. OPEN, BY NAME

- **Matt's:** the two claims for the 24 Sept run (doc 388); Nacua's practice report; paste v9.14 when convenient; the
  Tuesday task prompt paste (doc 387 §6).
- **Mine:** ledger row 165 (air-yards share and WOPR through `build_form.py` onto the wire row, and the list ordered on
  the cross); rows 162, 163, 164; the LA and NYG week-2 snap shares; the doc 383 batch on the five-year registry.
- **NOT YET RUN, with the form written down:** does the injuries feed, read Thursday rather than Tuesday, beat the
  Tuesday claim it would replace? Population: free WR and TE in weeks 4 to 14; predictor: a teammate at 20% target
  share or more carrying OUT or DOUBTFUL on the Thursday report; outcome: the same spike bar.
