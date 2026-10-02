# 362 - The flex is a free option, and the slot is just a label

**2026-09-18. Matt's rule, in his words: *"the player placed in my Flex slot should always have the
latest game start time among my active starters... A locked Flex forces me into a 1-to-1 positional
replacement."* He is right, the mechanism is slightly sharper than he stated, and the cost is not
"small" but ZERO.**

---

## 1. WHY IT IS FREE, AND THIS IS DERIVED, NOT MEASURED

**Which of the nine starters sits under which slot LABEL does not change the score.** If Matt has
already decided to start, say, three receivers and two backs, the total is the same whether receiver
C occupies WR2 or FLEX. **The FLEX assignment is a relabelling of a set he has already chosen, so it
cannot cost a point by construction.** `[DERIVED from the scoring rules, not measured]`

That puts it in a different class from every other preference this project has priced. Byes cost up
to 1.2 points (§4.11) and the offensive line is a tiebreak that must never override real margin
(§4.24a). **This one has no margin to override.** It is not a tiebreak. It is free, and free options
get taken.

**THE ONE CONSTRAINT: eligibility.** The rule ranges over the RB, WR and TE he is already starting,
never over all nine. His quarterback, kicker and defence cannot hold the FLEX label whatever time
they play.

---

## 2. THE MECHANISM IS THE TWO-STEP SHUFFLE, NOT THE OPEN SLOT

His stated reason is that an open FLEX lets him *"swap in an RB, WR, or TE."* True, and the more
useful version is one step further on.

**ESPN locks a PLAYER at his own kickoff, and a slot is only frozen because the man in it is.** So
a FLEX holding a Sunday-night or Monday-night body is **a movable asset all afternoon.**

**The case that pays:** his WR2 is a surprise inactive at 11:30 on Sunday and he has no receiver on
the bench. With an early-game player in FLEX, he is stuck. With a late-game receiver in FLEX he
plays it in two moves: **the FLEX receiver slides into WR2, and a bench back or tight end takes the
now-empty FLEX.** A slot carries no kickoff time of its own, so starting a 4:25 player in a slot
vacated by a 1:00 player is legal.

**That is what the rule buys: not a spare seat, but a piece he can still move after the board has
started locking.** A same-position-only swap cannot reach it.

**AND IT IS WORTH NOTHING WITH AN EMPTY BENCH.** The option needs a legal body to bring in. Doc 259
already measured the neighbouring fact on his roster: the best free player is below his worst
startable man at every position, so the wire cannot upgrade a working slot, only fill a broken one.
**The FLEX rule is about covering a break, which is exactly where a replacement-level body is worth
its full value rather than zero.**

---

## 3. WHAT IS NOT ESTABLISHED, AND THE FORM IT WOULD TAKE

**How OFTEN this pays is NOT YET RUN.** The rule is free so it should be adopted regardless, but
nobody should quote a points figure for it until this is measured.

**TESTABLE FORM, stated before running it (§0.5a2): POPULATION, every team-season week in this
league 2022-2025 where a rostered starter was ruled out or inactive AFTER the earliest game of that
week kicked off. OUTCOME, the difference between the best legal lineup available under an open FLEX
and the best legal lineup available under a FLEX already locked by an early starter. BASELINE, zero,
the weeks where the two are identical.** The inputs exist: `form_2026.csv` and the weekly lines
carry who played, and the schedule gives kickoff order. **What is missing is the inactive TIMESTAMP**,
which the weekly files do not carry, so the measurement would have to proxy it with "played zero
snaps while active on the roster." `[NOT YET RUN]`

**BLOCKED, AND THE INPUT IS NAMED (§0.5a4): THIS PROJECT HOLDS NO KICKOFF TIMES.** Checked rather
than assumed: `sched_2026.csv` carries exactly four columns, `week,team,opp,side`. **It knows who
plays whom and nothing about when.** So the rule cannot be applied mechanically today at all, by any
sheet or builder, and Matt can only apply it by eye off the ESPN app.
**What would unblock it:** one column of kickoff datetimes per team-week. nflverse's schedules
release carries `gameday` and `gametime`, and the pull that built `sched_2026.csv` almost certainly
discarded them. **That is one field to add, not a new data source, and it is the first step of any
lineup builder that applies this rule.**

---

## 4. HOW IT SHOULD BE APPLIED

**The rule, as it should be stated in the lineup builder:**

> Among the RB, WR and TE already chosen as starters, the FLEX label goes to the one with the
> LATEST kickoff. Ties go to the player likeliest to be interchangeable, which is the one with the
> most position-eligible bodies behind him on the bench.

**It changes no start-sit decision.** Decide the nine on merit first; the FLEX label is assigned
afterwards, and never used as an argument for starting a different player.

**QUEUED, NOT SHIPPED.** This belongs in `00_START_HERE.md`'s spine and in the directive's §6
doctrine alongside the QB/TE rules. Both are held deliberately: START HERE v4 is the document Fable
is about to test and must not move underneath the test, and the directive is mid-paste under the
one-version-per-day rule adopted in doc 359. **Both edits land after Fable reports.**
