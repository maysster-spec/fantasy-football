# 257 — HE IS RIGHT AGAIN, AND MY DEMOTION WAS THE SAME REFUSAL IN NEW CLOTHES

*2026-09-09. Matt: "the calculation matters but you need all considerations to make that*
*calculation."*

**Doc 255 enshrined his rule. Doc 256 demoted it to a tiebreak. Both were wrong in the same way —**
**I kept ruling on the VERDICT instead of filling in the TERMS.**

---

## 0. WHAT TO DO

1. **DOC 256's DEMOTION IS WITHDRAWN.** "A tiebreak, never a number" was me declining to do
   arithmetic because one input was noisy. **That is "it isn't measurable" wearing a different
   suit, and §0.5(a4) says it is not one of the three answers.**
2. **The claim ordering is an EXPECTED-VALUE CALCULATION. Status: NOT YET RUN, six terms, five of
   which we already hold numbers for.** Listed in §2.
3. **The queued v9.1 edit is rewritten a second time** — it now names the terms rather than ruling
   on the rule's standing.
4. **A term neither of us had: LOSING A CLAIM IS NOT LOSING THE PLAYER.** Two runs a week plus free
   agency means going second on a man costs a delay, not the man. That shrinks the whole ordering
   question and it was missing from doc 255 and doc 256 alike.

---

## 1. THE PROOF THAT HE IS RIGHT IS IN HIS OWN OBJECTIONS

He argued against doc 255 with two things: *"my real need is WR"* and *"that RB may be a bye-week
fill-in."* **Both of those are INPUTS to the calculation, not arguments against having one.** He was
not saying the arithmetic is wrong; he was saying it was missing rows. I read it as "stand down"
and stood down.

## 2. THE TERMS — and what we actually hold for each

For each player on the list, what going FIRST is worth:

| # | term | status |
|---|---|---|
| 1 | **what he adds to the nine Matt actually starts this week** | **HAVE IT** — `_lineup()`, pure Python and fast since doc 139 |
| 2 | **the next-best body at that position** — his own bench, then the free pool | **HAVE IT** — doc 252 rebuilt the free pool week by week |
| 3 | **the weeks he is actually needed** — byes are deterministic, not a guess | **HAVE IT** — `byes_2026.csv` |
| 4 | **P(a team AHEAD of him also files)** | **NOT YET RUN** (doc 254), and **BOUNDED**: doc 224's 56% uncontested / 16% contested is the empirical envelope |
| 5 | **what happens if he loses — run 2, then free agency** | **NEW. Never included by either of us.** See §3 |
| 6 | **the drop** — what leaves the roster to make room | **HAVE THE METHOD** — doc 240 prices a bench spot against its best alternative use |

**Five of six are already computable. The one that is not has a measured range, so the calculation
runs today as an interval rather than a point.** That is a very different answer from "tiebreak."

## 3. THE MISSING TERM, AND IT CUTS AGAINST BOTH MY VERSIONS

**Doc 255 priced going second as LOSING the player. It is not.** There are two waiver runs a week
(his fact, doc 255 §1), and after a run clears, an unclaimed man is a free agent. So the cost of
putting the receiver first is not *"lose the back"* — it is *"maybe get the back three days later,
or not at all if somebody ahead took him in run 1."*

**That is a smaller number than either doc assumed, and it explains why his instinct — need first —
is right more often than doc 255 implied and for a better reason than doc 256 gave.** Not "the
probability is unknowable." **The DOWNSIDE is small, because the player usually comes back around.**

## 4. THE PATTERN, NAMED FOR THE THIRD TIME TODAY

Promote → demote → both wrong. **The common defect is that I answered "how much should this rule
count?" when the question was "what goes into the number?"** §0.5(a4) exists precisely to stop the
second kind of dodge: for anything he proposes I owe **TESTED**, **NOT YET RUN with the form
written**, or **BLOCKED with the input named** — and "treat it as a tiebreak" is none of those. It
is a verdict issued instead of a measurement.

## 5. QUEUED FOR v9.1, THIRD AND FINAL FORM

1. **§4.31 scope** (doc 253): the week-1 penalty applies to speculative claims for a season asset,
   **not** to filling an empty starting slot, where the alternative is zero.
2. **Claim ordering:** it is an expected-value calculation over the six terms in §2, **not** a
   ranking rule and **not** a tiebreak. Five terms are in hand; the sixth is bounded by doc 224.
   **Losing a claim delays a player, it rarely removes him** — two runs a week, then free agency.
   State the two-runs mechanic wherever priority is discussed.
