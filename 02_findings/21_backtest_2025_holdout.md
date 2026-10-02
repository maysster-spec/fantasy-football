# 21 — THE 2025 HOLDOUT BACKTEST
**Aug 22, 2026.** `HANDOFF_v2` §6: *"the strongest available self-red-team and it has never
been done."* It has now been done. Reproduce with `code_backtest_2025.py` then
`code_backtest_redteam.py`.

## THE ANSWER, IN ONE LINE

**The value rule is not measurably better than your own drafting.** It "won" 2025 by 277.5
points, **99% of which came from three injuries it could not have foreseen.** Across the
other eleven picks it gained **+7.3 points total.**

---

## DESIGN

You drafted slot 11 in 2025: picks 11, 14, 35, 38, 59, 62, 83, 86, 107, 110, 131, 134, 155,
158, keeper Jayden Daniels at 179 held constant for every policy.

The availability pool at each pick is **every player actually taken later in the real 2025
draft.** That is ground-truth availability, not modelled availability — it removes the
survival model from the test entirely, so what is being measured is the **value rule alone**.

Preseason information only (ESPN `proj_2025`). Outcome: `actual_2025`. Scoring: season-total
starting lineup, 1QB 2RB 2WR 1TE 1FLEX 1DST 1K.

## HEADLINE NUMBERS

| policy | starting-lineup points |
|---|---|
| **ACTUAL — what you drafted** | **1566.8** |
| BAV — max VBD, no constraints | 1806.2 |
| **NEED — max VBD subject to roster need** | **1844.3** |
| ORACLE — hindsight ceiling | 2280.7 |

Rule beat you on 8 of 14 picks. Total raw delta +517.0. **Then the red team ran.**

---

## WHY THE HEADLINE IS WRONG

**RT1 — is `proj_2025` really preseason, or contaminated?** *(the `top_400` failure, B1)*
Correlation with the 2025 finish: **0.845** across all skill players, **0.672** restricted to
players projected 100+. The restricted figure is the honest one and it sits in the normal
preseason band. Only two players projected 150+ finished under 40. **Clean — no leakage.**

**RT2 — where does the win actually come from?** *(A10: print the members)*

| pick | you | pts | rule | pts | delta |
|---|---|---|---|---|---|
| 11 | Malik Nabers | 48.1 | Derrick Henry | 272.0 | **+223.9** |
| 110 | Braelon Allen | 14.3 | Courtland Sutton | 182.7 | **+168.4** |
| 158 | Rashod Bateman | 45.9 | DeVonta Smith | 163.3 | **+117.4** |
| — | *the other eleven picks* | | | | **+7.3** |

**Top three picks = +509.7 of +517.0. Ninety-nine percent.** All three are players whose
seasons ended. Nothing in a preseason projection sees that.

**RT3 — bootstrap.** Mean pick-level delta **+36.9**, sd 89.5, **95% CI [−6.2, +80.4]. Includes
zero.** Median delta **+6.6**. Excluding the three injuries: mean **+0.7**, CI **[−30.5, +32.6]**.

**RT4 — power.** *(A1: say what the test could have detected)* With 14 paired picks at sd 89.5,
the smallest detectable mean effect at 80% power is **±67 points per pick.** Anything smaller
is invisible here. **The correct word is underpowered, not null.**

---

## THE FINDING THAT DID SURVIVE, AND IT MATTERS MORE

Running the same rule for **all twelve managers** on their real 2025 slots:

| | mean | sd | range |
|---|---|---|---|
| what managers actually scored | 1686 | **202** | 1498 – 2133 |
| what the rule would have scored | 1788 | **76** | 1634 – 1936 |

**The rule's outcome variance is 14% of a real manager's.** It beat 9 of 12 — and lost to
exactly the three the opponent model already names as the best: **Lobsinger −196.3 (reigning
champion), R Taylor −182.0 ("best manager, never worse than 5th"), Rychlicki −41.1 ("trending
up").**

*Honest caveat:* `corr(actual, delta) = −0.929` is mechanical — delta is defined as
`rule − actual`, so it must fall as actual rises. That is the A8 floor/ceiling trap and this
result is partly inside it. The part that is **not** mechanical is the variance itself:
**sd 76 against sd 202 is a property of the rule's own output**, measured across twelve
independent draft positions, and no definitional artifact produces it.

### Why this is the important number

Your objective function is under review precisely because first place is **44% of a $1,200
pot** and your losses are entirely in weeks 15–17. A rule that compresses outcomes into a
300-point band is **buying a floor and selling a ceiling.** You finished 2nd, 4th, 3rd and 6th
in points and have no title. **A floor is not your problem.**

This also sits against the sim's own conclusion that variance-seeking is punished
(ceiling +15 costs −$62.67, t=−4.97). Those two now disagree, and the disagreement is
worth more than either result alone:

- The **sim** says take less variance. It was calibrated on simulated opponents who never
  optimise a lineup, and it gives you 33–44% title odds, which is not a real regime.
- The **holdout** says the value rule already removes most of the variance for free, and the
  three managers who beat it did so by *not* following it.

`[HYPOTHESIS]` — **the greedy value rule may be a floor-raiser being deployed by someone who
needs a ceiling-raiser.** Falsifier: re-run the manager-level backtest on 2022, 2023 and 2024.
If the rule beats Lobsinger and Taylor in two of those three years, this is 2025 noise and I
withdraw it. **All four inputs are already in the project** — `draft_history_2021_2025.csv`
carries every year; what is missing is preseason projections for 2022–2024, which is exactly
the FantasyPros historical export already at the top of the to-do list. **That export just
became the highest-value item on the list, for a reason nobody had before today.**

## LIMITS — read these before quoting any number above

1. One season. Fourteen paired picks. Twelve managers.
2. Season totals, not weekly — no bye adjustment, no injury-week adjustment, no weekly
   lineup optimum. The real objective is weekly starting-lineup points.
3. The pool is restricted to players someone actually drafted (173 of 180 picks joined; seven
   2025 draftees are gone from the 2026 ESPN file and were dropped).
4. `NEED` is a simplified greedy policy, not `draft_sim_2026.py`. It tests the *value rule*,
   not the shipped simulator.
5. The rule got ESPN's projection for every player. You did not necessarily use ESPN's.
