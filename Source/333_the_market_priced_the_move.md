# 333. The market priced the move

*17 Sept 2026, 02:40 UTC. Matt: "Pickens switched teams and then he was easy pickens. It's like we
tried not to find a keeper, lol. I should have done the research I said I would do." The joke names
a real mechanism, so it got tested. It is null and it leans the other way, and the reason his own
case worked is not the one the joke implies.*

---

## 1. WHAT CHANGED

1. **TESTED, and it does not hold: a team change before the season he was drafted made a player
   LESS likely to become a keeper, not more. 3.3% against 8.5%.** `[TESTED, n=272, NULL,
   UNDERPOWERED: Fisher p=0.263]`
2. **Pickens is one of only two changed-team keepers in five years.** The other is Ezekiel Elliott.
3. **AND THE MARKET PRICED HIS MOVE, WHICH IS THE PART THAT MATTERS.** He went **round 5 pick 52 in
   2024 and round 5 pick 59 in 2025**. Seven picks. **The trade did not make him cheap. He cost the
   same and the season that followed was the payoff.**
4. **The first run of this test missed him**, because `draft_history_2021_2025.csv` stops at 2025 and
   the 2025-to-2026 transition is where his own case lives. Caught by checking his example against
   my own result and not finding it.
5. **The research he is apologising for is mine.** Section 0.4, and the specific item is already in
   the directive under his name.

---

## 2. THE CLAIM, STATED BEFORE THE TEST (0.5a2)

His words: *"Pickens switched teams and then he was easy pickens."* The mechanism inside the joke:
**a new team resets a player's price and unlocks a role, so a team change is a keeper signal.**

**POPULATION: every round-5-or-later selection in this league where the player appears in the
PREVIOUS year's draft too, so a team change is determinable from the draft history itself. n=272
after excluding the kicker and the defence (section 4.9's rule). BASELINE: became a keeper the
following year. PREDICTOR: his NFL team in year N differs from his NFL team in year N-1.**

| | n | became a keeper |
|---|---|---|
| **changed NFL team** | 60 | **2 = 3.3%** |
| same team | 212 | 18 = 8.5% |

**Fisher two-sided p = 0.263.** Expected hits among the 60 if the base rate held: 5.1. Observed 2.
**NULL, direction AGAINST his framing, and UNDERPOWERED: the 95% interval on 2 of 60 runs to about
11.5% and contains the base rate, so this cannot rule out a real effect either.** Section 4.24(b):
it failed POWER, not PREDICTION.

**The two who changed and were kept: George Pickens (PIT to DAL, round 5, 2025 to 2026) and
Ezekiel Elliott (free agent to NE, round 11, 2023 to 2024).**

**THE SELECTION LIMIT, NAMED:** the population requires the player to be drafted by this league in
two consecutive years, which is itself a filter on being worth drafting twice. A player who changed
teams and vanished from the league's boards is not counted. `[OPEN]` the unfiltered version needs
season-by-season team from the ESPN pulls rather than the draft history.

---

## 3. THE PART THAT DID HOLD, AND IT IS NOT THE TEAM CHANGE

| season | manager | round | pick | team |
|---|---|---|---|---|
| 2024 | Brown/Collins | 5 | **52** | PIT |
| 2025 | **Matt** | 5 | **59** | **DAL** |

**Seven picks apart, across the trade.** The move happened in May 2025, months before the draft, so
by the time the board was set **the market had already repriced him and the price had not moved.**

So the sentence "switched teams and then he was easy pickens" is half right in a way worth keeping:
**he was gettable, but not because he was cheap. He was the same price he had been.** What made him
a keeper was the season he then played, which nobody had on the board in August.

**That is section 4.22(b) a second time, from a new angle: when the market and the projection
disagree, the market is the one that is right.** The market did not discount him for the move. It
was correct not to.

**AND HIS OWN CASE IS NOT EVEN CONSISTENT WITH THE MECHANISM.** Pickens has been a keeper twice:
in 2023 off a round-9 pick with **no team change at all** (doc 331), and in 2026 after one. One
case each way, from the same player.

---

## 4. THE RESEARCH HE IS APOLOGISING FOR IS MINE, AND IT IS WRITTEN DOWN UNDER HIS NAME

Section 4.25b carries this, and has since 6 September:

> **STILL UNTESTED, and he named it: age conditional on a SITUATION CHANGE, new team, new role,
> new QB (his Randy Moss case). Section 4.21 measured the environment but never age times
> environment change. Post-draft; it needs the 2023 and 2025 preseason pulls.**

**That is the same family of idea, it is recorded as HIS, it was labelled post-draft, and it sat
there.** Section 0.4 puts reading, arithmetic and every form of verification on me. **The crude
version above took about four minutes on files already on his drive and needed nothing from him.**

**And "it's like we tried not to find a keeper" is closer to literal than he meant it.** Docs 329
and 331 measured exactly that: three numbered rules choose the audition band and every one of them
is a price or a round, against one unnumbered bullet about an ascending role. **He did not fail to
do research. The instrument was pointed away from the question.**

---

## 5. WHAT THIS DOES NOT SAY

- It does **not** say a team change is bad. n=60, p=0.263, and the interval contains the base rate.
- It does **not** retire the situation-change idea. **JOB 4's riser variable is the better-specified
  version of the same instinct** and it is still queued.
- It does **not** say the Pickens pick was luck. He paid market price for a player who then produced;
  that is what the keeper rule pays out for, which is doc 331's point.

---

## 6. OPEN

- **The unfiltered team-change test**, using season-by-season team from the ESPN pulls instead of
  requiring two consecutive drafts. `[NOT YET RUN]`, inputs named, and it would roughly triple n.
- **Section 4.25b's situation-change item**, still `[NOT YET RUN]` in its full form (age times
  environment change). The crude keeper version is now done and null.
- Carried: JOB 3, JOB 4, ledger rows 29 and 42, the section 4.25b wording, catalog B4.
