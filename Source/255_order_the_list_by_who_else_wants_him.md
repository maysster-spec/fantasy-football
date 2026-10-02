# 255 — THE CLAIM LIST IS ORDERED BY WHO ELSE WANTS HIM, NOT BY WHO IS BEST. AND THERE ARE TWO WAIVER RUNS A WEEK.

> **BANNER, 28 Sept 2026 (doc 435).** The title and point 2 below say there are TWO WAIVER RUNS A WEEK. **Retracted at v9.21 and measured dead at v9.26 (doc 405): the run is Thursday 03:00 to 06:00, one per week, and a winning claim spends his priority for the rest of that week.** Point 1, rank the contested man first, stands as a dominance argument only (doc 401). Kept as a dated record.

*2026-09-09. Matt: "are you forgetting that there are two waiver periods each week? I am penalized*
*for the second period if I claimed a waiver the first period." And: "say I want two claims, one*
*running back and one wide receiver. If I'm ahead of Russell in waivers and no one else likely wants*
*the wide receiver that I do, then what I do is prioritize the running back over the wide receiver."*

**Both right. The second one is a REAL IMPROVEMENT on the rule the directive currently carries, and**
**I answered a different question in my last reply.**

---

## 0. WHAT TO DO

1. **A RULE CHANGED — order the claim list by CONTESTEDNESS × value, not by value.** Doc 226 says
   *"rank the list by value, never by convenience."* **That is now too coarse.** The priority is only
   worth spending on a player somebody else will take. Put the contested man first even when the
   uncontested one is worth more — you get the uncontested one anyway.
2. **The two-run week is his fact, not mine to argue.** He is penalized in run 2 if he won in run 1.
   The settings file records *"Waiver Period: 2 Days"* — that is the LENGTH of a period, not the
   COUNT of runs. **The count comes from the operator and nothing in this project measured it.**
3. **What I got wrong last reply:** I answered *"claim now or wait for free agency."* He asked
   *"which of my own claims goes first."* Different decision, and his is the one that recurs weekly.
4. **Two directive edits are now queued** — this rule, plus §4.31's scope sentence from doc 253.
   Both fold into one paste; no third version tonight.

---

## 1. THE MECHANIC, STATED CORRECTLY

Three facts, and they only make sense together:

- **ACROSS weeks the order resets to inverse standings** (settings file, doc 250). Winning a claim
  last week does not push him back this week.
- **WITHIN a run, the first claim that clears spends his position** — ESPN Fan Support, *Waiver
  Order Overview*: *"once a team successfully makes a waiver claim, they move to the bottom of the
  waiver priority list."* (doc 226, and it corrected doc 223's error.)
- **AND THERE ARE TWO RUNS A WEEK, so the penalty lands inside the same week.** Win in run 1, sit
  at the back for run 2. **That is the part I kept describing as "within one week" without saying
  it costs him a second, separate opportunity.** His words in doc 226 said it plainly nine months
  of sessions ago: *"waiver order on the second waive/round is bad for me because i usually take
  waivers 1st waive."*

**So the resource is not "a claim." It is ONE turn at his real priority, twice a week.**

## 2. HIS RULE, AND WHY IT BEATS THE ONE ON FILE

Doc 226 ends: *"Rank the list by value, never by convenience."* **Correct as far as it goes and it
ignores the other eleven teams.**

**HIS VERSION:** the priority changes the outcome **only for a player somebody ahead of him would
otherwise take.** An uncontested player is his whether he claims first, second, or picks him up as
a free agent after the run. So the first slot belongs to the man he would LOSE.

Written as the thing to compute, for each player on the list:

> **spend priority where `P(a team still ahead of you when this claim processes also wants him)`
> × `(his value to you − the next-best body at that position)` is largest.**

**His crude example is exactly this and it is right:** RB contested, WR wanted by nobody → claim
the RB first, take the WR second or off the wire later, end up with both. Ranking by value alone
would put the WR first if the WR graded higher, and he would end up with the WR only.

**AND THE REFINEMENT THAT MAKES IT OPERATIONAL: "contested" is not enough — it has to be contested
by somebody AHEAD OF HIM.** He is 5th of 12 this week (doc 238); only Lobsinger, R. Taylor,
Rychlicki and Snyder can take a name before him. A player four teams behind him also want is a
player he still gets, so he does not belong in the first slot either.

## 3. WHY THIS IS WORTH BUILDING AND NOT JUST WRITING DOWN

Doc 254 established that the rival-competition model is **NOT YET RUN**, feasible, and now
unblocked. **This doc is what that model is FOR.** It does not need to predict who wins a contested
claim — doc 224 already measures that at 16% for him. **It needs one number per player: is anybody
ahead of me going to file on this man?** That is a smaller, easier target than "who gets him," and
it is the whole of the ordering decision.

**Falsifier, fixed now:** if the contestedness estimate cannot beat "put the scarcest position
first," the model is noise and the honest fallback is his own gut, which produced this rule
unprompted.

## 4. WHAT WENT WRONG IN MY LAST REPLY (§0.5(a2) again)

He described a **within-list ordering problem**. I answered a **claim-versus-wait problem**. Both
sit under "waiver strategy," which is exactly how the object slides. **The tell I ignored: he wrote
"prioritize the running back OVER the wide receiver" — the word is comparative, between two things
he is already claiming.** Nothing in that sentence is about whether to claim.

## 5. QUEUED FOR THE NEXT DIRECTIVE VERSION (v9.1)

1. **§4.31 scope sentence** (doc 253): the week-1 penalty applies to speculative claims for a season
   asset, **not** to filling an empty starting slot, where the alternative is zero.
2. **The ordering rule above**, replacing doc 226's "rank by value" — and the **two-runs-a-week**
   mechanic stated explicitly wherever priority is discussed, because "the order resets weekly" is
   true and by itself reads as "there is no cost," which is wrong twice a week.
