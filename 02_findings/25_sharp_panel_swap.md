# 25 — SWAPPING THE EDGE PANEL FOR THE ONE THE DATA ENDORSES
**Aug 23, 2026.** Pulled live from your FantasyPros account via the browser.
`[SOURCED: fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php, captured 2026-08-23]`

## WHAT I DID

Doc 24 established that **RB is the only position where analyst accuracy repeats**
(rho +0.48 / +0.36 / +0.27) and named the persistent rankers. I opened Pick Experts on your
half-PPR board, deselected the default 107-expert consensus, and selected only the ones the
multi-year accuracy data endorses.

**Three of the top five RB rankers were not available.** `Jody Smith (Draft Sharks)`,
`Chris Raybon (The Action Network)` and `Jeff Bell (Footballguys)` do not appear in
FantasyPros' 155-expert 2026 list at all — Draft Sharks and The Action Network syndicate
accuracy history to the contest but not current rankings. **That is a hard ceiling on this
approach and it is worth knowing.**

The five that were available, and what they are:

| expert | multi-year rank |
|---|---|
| Ryan Weisse — Club Fantasy FFL | **RB #2** |
| Kev Wheeler — Wheel Route FF | **RB #4** |
| Nick Zylak — Fantasy Football Advice | **RB #5** |
| Donald Gibson — FantasyPros | **WR #2** |
| Tal Malachovsky — The Fantasy Scout | **WR #3** |

Three of the top five at RB and two of the top three at WR. Applied as a view change only —
**I did not touch "Save My Experts"**, and I reloaded afterwards and confirmed your board is
back to its 107-expert default.

## THE HONEST RESULT: THE SWAP BARELY MOVES ANYTHING

**The new edge correlates +0.897 with the old six-ranker edge** (n=143). The sharp panel's
own rank correlates **+0.945** with ESPN ADP, mean absolute gap 15.8 picks.

Choosing analysts by measured accuracy lands in almost exactly the same place as choosing them
arbitrarily. **This is the monoculture finding again, now with the strongest possible test
attached to it:** you cannot escape the consensus by picking better members of it.

**So the swap buys provenance, not signal.** It is still worth keeping — the column can now be
defended on measured accuracy rather than reputation, and the source file carries full names
plus team, which kills the first-initial collision that produced the Bijan/Brian Robinson error.

### Where the two panels genuinely disagree

| player | ESPN ADP | sharp-5 | old panel |
|---|---|---|---|
| Juwan Johnson, TE NO | 164 | **+44** | +16 |
| T.J. Hockenson, TE MIN | 134 | **−37** | −69 |
| Jake Ferguson, TE DAL | 113 | **−23** | −46 |
| Matthew Golden, WR GB | 107 | **−29** | −9 |

All four are tight ends or a WR — the positions where accuracy does *not* persist. The panels
agree wherever the data says the analysts are actually skilled, and disagree where it says they
are guessing. That is a coherent pattern and mildly reassuring about both.

### Biggest edges on the new panel

**Buy** — Chris Rodriguez Jr. (+63), Tyler Allgeier (+60), Chris Godwin Jr. (+57),
Quentin Johnston (+53, Q), Blake Corum (+45), RJ Harvey (+39). Note most sit deep and carry
heavily negative VBD — the panel likes them *relative to a very late price*, not in absolute terms.

**Fade** — Travis Hunter (−60), Matthew Stafford (−51), Jaxson Dart (−49), T.J. Hockenson (−37),
Kyle Pitts Sr. (−31), Dallas Goedert (−29), Sam LaPorta (−23).

**Also:** Jordyn Tyson, the most-contested player on the board (Smyth 81 vs Pianowski 219), is
now flagged **DOUBTFUL** on the ESPN pull.

## WHAT CHANGED IN THE ARTIFACTS

- **EDGE** on the live board is now the sharp-5 minus ESPN ADP. A small `f` after a number means
  it fell back to the older six-ranker panel (21 players); 150 carry the new one.
- **SPLIT** still comes from the six-ranker Yahoo file, because a five-expert consensus cannot
  measure dispersion. It stays what it was: how contested a player is, not how good.
- The grid's cell legend now reads `E+n`, and the Fade sheet is rebuilt on the new panel.

## LIMITS

- Five experts is a thin consensus. The default is 107. A five-man panel is noisier per player
  even if its members are individually better.
- The accuracy that selected them was measured on **full-season finish order**, and doc 23 showed
  that metric is 97% insensitive to breakouts. **These five are endorsed for getting the ordinary
  ordering right. They are not endorsed as breakout finders, and nothing in this project is.**
- One capture, one day. If it matters on draft night, re-pull on Sep 5.
