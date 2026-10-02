# 145 — The badge I called "the only measured one" is the one measured to point backwards

**2026-09-03 · Matt: "examine the strategy… make sure you have a well considered and justified
approach that you have sent through the red team" · T-4 days**

---

## The do-this list

1. **Re-run `py parse_ladder.py` then `py mkvalue.py`.** The ladder's order changed and one badge
   changed meaning.
2. **New: `after_pull.bat`.** Runs the seven post-pull steps in the one order that is correct, and
   **stops** if the board audit fails. Use it instead of the sequences I have been typing at you.
3. Nothing else.

---

## 1. He asked me to justify the ordering. It does not survive the asking.

The sheet sorted by **AGREE** — how many of five badges fired. I defended that twice. Here is what
the five badges actually are, read out of `values.py`, and how often each fires on the 49 rows:

| badge | what it tests | fires | what this project has measured about it |
|---|---|---|---|
| **BOARD** | `board_rank < adp_pick − 12` | **40/49** | **§4.13 retired it (rho −0.079). §4.22(b) replicated it NEGATIVE: rho −0.173, p<0.001, n=409** |
| ANALYSTS | Boone + Harmon rankings 25+ ahead of ADP | 25/49 | §4.13d: the panel is one opinion measured six times (pairwise r 0.81); disagreement predicts finishing **worse** (−0.244) |
| BUY | the analyst **commentary** sweep called him up | 30/49 | unmeasured |
| JOB | open backfield, job worth ≥ 150 | 25/49 | §4.20's flag. Doc 141: it does **not** predict who wins (n=19, p=0.60) |
| INJURY-OPENED | a teammate at his position is OUT / PUP / exempt | 7/49 | **a fact, not a forecast** |

**BOARD fires when our projection likes a player more than the market does.** That is precisely
"the market is sleeping on him" — the signal §4.13 tested against 324 player-seasons and
**retired**, and that §4.22(b) then re-measured on a different market at **rho −0.173, p<0.001,
n=409**, concluding *"when the market and the projection disagree, the market is the one that is
right."*

**The sheet's own warning box said: "Every signal here except BOARD is unpriced and unmeasured."
That is exactly backwards.** BOARD is the one that IS measured, and it points the wrong way. I
wrote that line and repeated it to Matt as recently as this afternoon.

**And it barely discriminates:** 40 of 49 rows carry it. Sorting a 49-row sheet on a count that
includes a near-universal, measured-negative flag is not a ranking of anything.

**One more thing, found while checking:** the badges were parsed out of the shipped PDF and frozen,
but **BOARD is defined against ADP** — so after the 09-03 refresh some BOARD badges were firing at
a **3-slot** gap when the rule requires 12. The sheet was not even self-consistent. BOARD is now
recomputed from the live board every run.

**Careful about what this does NOT say.** It does not say those players are bad. The outcome
measured is *beats his own projection*, so a BOARD player who slightly underperforms a high
projection can still be a good pick — §4.13b's ratio-vs-absolute distinction applies. What dies is
the **bargain reading**: BOARD is not a reason to take him.

## 2. The order, and why it is not by value

Matt asked for "the player with the most potential / board value first." **That is what the draft
board is for, and if this sheet sorted by value it would be a strictly worse copy of it.** The
ladder's only contribution is *where several independent things point at the same name*; sort it by
VBD and that contribution disappears.

So the order is now **facts, then agreement, then size, then opinion:**

1. **INJURY-OPENED** — the only badge reporting something that has already happened.
2. **AGREE** — now the **four non-BOARD badges** only.
3. **job worth** — how big the open job is, the nearest thing to a ceiling number this project has
   (§4.20, §4.13d). It breaks ties and never leads, because it only exists for RBs and would
   otherwise push every WR to the bottom of every block.
4. the analyst gap.

**And the sheet now says plainly that this is a reading order, not a ranking** — every row inside a
PICK block is reachable at the same pick, so their relative order carries no claim.

**BOARD is greyed out**, kept visible because the disagreement is worth seeing, excluded from AGREE,
and its legend now names it as the retired signal instead of endorsing it.

**Two badge definitions were also just wrong on the sheet.** `BUY` was described as "both analyst
panels ahead of ADP" — that is ANALYSTS' definition. `BUY` is `player_context.buy`, the analyst
**commentary** sweep, and it is independent of the injury grade (a BUY can carry AVOID: 1 does).
Corrected to "a different source from ANALYSTS, not the same thing said twice."

## 3. The runner Matt was right to ask for

> *"I've been asked to run several things lately in a certain order that didn't have batch files."*

Correct, and worse than he knew — **the two sources disagreed with each other.**
`refresh_adp.py`'s footer says `make_fallback` then `depth_map`. COMMANDS.html says `depth_map`
then `make_fallback`. **COMMANDS.html is right, and it matters:** `depth_map.py` *writes* the job
labels into `player_context.csv` (it printed "stamped job labels into player_context.csv (86 rows
carry one)"), and `make_fallback.py` *reads* that file at line 56. Run them the other way and the
paper board is built from yesterday's labels, silently.

`after_pull.bat` now runs all seven in the correct order, **gates on `board_audit.py`** (39/39 or it
stops and runs nothing downstream), and deliberately does **not** run `make_board.py` (slow) or
`make_prerank.py` (writes to ESPN — never automatic, and `refresh_adp` does not touch rank anyway).

---

## 4. Close (§7)

**Top 3 assumptions → what would invalidate each**
1. *BOARD implements §4.13's retired signal.* Read from `values.py`: `board_rank < adp_pick − 12`,
   where `board_rank` is the VBD (projection) rank and `adp_pick` is the market. Invalidated only
   if §4.22(b)'s outcome variable is not what "beats projection" means there — it is.
2. *Facts should outrank opinions in a research reading order.* This is a judgement, not a
   measurement, and I am labelling it as one. What it rests on is that four of the five badges have
   no positive measured record and one has a negative one, so ranking by their count is unsupported.
3. *`depth_map` must precede `make_fallback`.* Verified by reading both files, not inferred.

**The missing input that would most improve this:** a measured record for `JOB` and `BUY`. Doc 141
tested the incumbent/challenger half of JOB and got a null; nobody has tested whether the *presence*
of an open job predicts anything at all, or whether the commentary sweep's BUY calls have a record.
Until then the AGREE count is four unmeasured things, honestly labelled — which is better than five
with a negative one hidden inside, but it is not evidence.
