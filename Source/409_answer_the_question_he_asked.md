# 409 — Answer the question he asked, and the forward rate that died on its own test

*24 Sept 2026. Directive v9.27, new §0.5(a6).*

## PART 1 — THE RULE
Deciding whether to drop Xavier Worthy, Matt said *"I don't see a likely path for him to get more
than WR3 type production."* I answered with Worthy's CURRENT target share, 19.1%, second on Kansas
City. Both true, about different things. **He asked where the player TOPS OUT. I answered where he
IS.** For a drop only the first decides anything.

His instruction: *"Employ that logic always since that is HOW to evaluate each player. Did that
eval contain every consideration for every scenario? Certainly not, but the logic you followed for
that circumstance was good."* **He supplied the limit himself and §0.5(a6) carries it.**

**THE FOUR STEPS:** name which question is on the table, ceiling or floor or present · find the
resource that constrains him and who else draws on it · ask what would have to MOVE for his answer
to be wrong · say which way it leans and say plainly when it cannot be falsified.

It is §4.20's *"buy the job, never the name"* carried from a backfield to a target share, running
on §0.5(a3), his own frame. A share is the cleanest case of that frame in the game: one man's
ceiling is the remainder after everyone ahead of him is fed.

## PART 2 — THE FORWARD RATE, BUILT AND KILLED THE SAME HOUR
`rates()` priced every player at `proj_2026 / 17`. Proposed replacement: `(proj_2026 -
actual_2026) / weeks remaining`, ESPN's own implied rest-of-season rate, needing no games-played
divisor. Built it, tested it on his real pull:

| | measured/g | old | forward |
|---|---|---|---|
| Schultz | 12.8 | 6.38 | **5.53** |
| Tucker | 12.1 | 6.78 | **6.08** |
| Dobbins | 3.6 | 9.37 | **10.14** |
| Dowdle | 4.2 | 7.60 | **8.05** |

**All four moved AWAY from the season.** Subtracting banked points from a sticky season total
penalises whoever has already produced. It is mean reversion wearing a forecast's clothes.
**Reverted, with the numbers in the code so nobody rebuilds it.**

## PART 3 — WHAT SHIPPED INSTEAD
`rates()` rows now carry `actual_2026`, `proj_wk` and a `vintage` tag. The rate is UNCHANGED until
a blend is chosen on evidence. **Rejected divisor, and why:** stat id 210 in `raw_actual_stats`
looks like games played and agreed with independently counted games on only 313 of 375 players,
83.5%. A divisor wrong by 2x on one player in six is worse than none.
