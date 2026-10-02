# 106 — The dots measure agreement, not value, and I proved it points the wrong way

**Date:** 2026-08-31 · **Matt:** *"So BUY ●●● (3 dots) is the highest buy value?"*

**No — and the question was worth asking, because as built the answer was dangerously close to
yes-looking.**

## THE MEASUREMENT

Dot count against the board, all 212 graded players:

| dots | n | median VBD | median goes-at | best board rank |
|---|---|---|---|---|
| 0 | 131 | −132.7 | 158 | 11 |
| **1** | 53 | **−17.2** | 106 | **1** |
| **2** | 24 | **−37.4** | 127 | 21 |
| **3** | 4 | **−70.5** | 147 | **87** |

Across everyone, dots and VBD correlate **+0.50** — but that is an artifact of the 131 zero-dot
bodies at the bottom of the board. **Among players who carry any dots at all, the relationship
reverses: rho −0.22, p=0.046. More dots goes with a WORSE player.**

The cause is structural, not statistical noise. Every signal feeding the dots is a **late-round
signal by construction**: our panels flag players the market underrates, podcast calls concentrate
on sleepers, and the depth-chart DART only exists for backups. Nobody writes an "analyst is ahead
of ADP" note about Jahmyr Gibbs. So the dots are a *lateness* detector wearing a quality badge.

The four three-dot players make it concrete: **Jonathon Brooks (rank 87), De'Zhaun Stribling (146),
Tyler Allgeier (180), Chris Rodriguez Jr. (202).** Three dots at board rank 202 is a sentence that
should never form on the clock.

## THE FIX

**The dots now render only when the row is already within 3 points of row 1** — that is, only when
the pick is genuinely a tie and his gut is free. Further down the list the word survives (`BUY`,
`CALLS`, `DART`) and the strength does not, at the dimmest tier. A tie-breaker that appears when
there is no tie is not a tie-breaker; it is a suggestion to reach.

`[TESTED]` twelve assertions: dots present at cost 0, absent at cost −11 with the word intact and
the dim class applied.

## AND A REGRESSION I CAUSED AND CAUGHT IN THE SAME MINUTE

My first attempt inserted the `tier` calculation **between** the suppression guard and the
`if buy:` chain, which turned one if/elif into two statements — so `edge = None` for an AVOID
player was immediately overwritten and Kittle, Kraft, Charbonnet, Dell and Love would all have got
a green mark back. Caught by the regression test written an hour earlier for exactly that
property. Rewritten as an explicit `silenced` guard followed by a single chain, so the two cannot
be separated again.

**That is now three times this week that a patch made a working guard stop working** — the D/ST
merge collision, the `draft_night.bat` label, and this. All three were caught by a test that
existed because the guard had been written down as a property rather than as code.

---

**Card updated:** *"Dots are a COUNT of agreement, not a measure of value — more dots goes with a
worse player."*
