# 139 — The board was the bottleneck, not the feed

**2026-09-03 · Matt's four post-mock reports, all four closed · T-4 days**

> **NUMBERING — this shipped as 138 and was renumbered within the hour.** Fable's
> `138_keeper_value_does_not_persist.md` landed on Drive at 00:25 while this was being written,
> and both files claimed 138. Fable's has priority (it was written first and is already
> referenced by `k3_artifacts.zip`). Every `doc 138` reference in `live_draft.py`,
> `code_live_engine.py`, `bridge_server.py`, `bench_lineup.py` and `check_kit.py` was rewritten
> to `doc 139` and the affected hashes re-pinned. **This is the naming rule failing in a new
> place:** it covers one FILE having two versions, and says nothing about two files claiming one
> NUMBER. Two agents writing to the same numbered series with no reservation step will collide
> again. **Check `Source\` for the next free number before writing, not after.**

---

## The do-this list

1. **Nothing.** The kit on your machine is already updated and `check_kit.py` re-pinned.
2. When you next run the bridge, the board should be visibly quicker. If it is not, say so —
   the numbers below say what to expect.
3. Read §5 before Sept 7: **pick 32 is a genuine tie** and the engine will not break it for you.

---

## What Matt reported after the 2026-09-02 bridge mock

> "Everything seemed to work. Maybe speed of the mock messed it up but the draft clock
> couldn't keep up and would increment by two. Players coming off the board was also delayed."
> "Something i've noticed before it that the draft board changes how many rows are displayed.
> That can be distracting."

Plus one line in his log:

```
[20:00:14] 0 real picks in
```

Four complaints. They turned out to be **three different defects and one correct behaviour
that looks like a defect**, and the biggest one was in a place nobody had looked.

---

## 1. `0 real picks in` — the comment and the code disagreed

`live_draft.py --bridge` reads `bridge_picks.json`. The reader returned `None` when the file
could not be parsed, and the caller did this:

```python
got = _bridge_picks()
if got[0] is None:              # unreadable this instant -- treat as "no change"
    return [], False, {}        # <-- returns EMPTY, which is not "no change"
```

An empty pick list is not a no-op. `step()` calls `eng.set_taken([])`, which hands **every
drafted player back to the engine as available**. For one poll the board would have
recommended players who were already gone.

**Why the file was unreadable:** `bridge_server.py` wrote it with a plain `open(PICKS,'w')`,
which truncates the file to zero bytes and leaves it that way for the whole `json.dump`. A
poll landing in that window read a half-written file. At a 3-second interval it took most of
a draft to hit; it hit once.

**Two fixes, in the right order.**

- `bridge_server.py` now writes a sibling `.tmp` and `os.replace()`s it. The rename is atomic
  on Windows and POSIX, so a reader sees the old complete file or the new complete file. This
  *removes* the window rather than coping with it.
- `live_draft.py` keeps the **last complete read** and returns that when a read fails. It also
  refuses a read that goes **backwards** — a draft only ever gains picks, so a shorter file is
  a reset or a restarted listener, and holding the larger set is always safer than handing
  drafted players back.

**Negative control** (§0.2 — a guard that has never executed is not a guard). Old code, on a
deliberately half-written file:

```
OLD code, good file  -> 9 picks
OLD code, mid-write  -> 0 picks   <-- this is the [20:00:14] line
```

New code, driven by a writer that truncates on purpose *and* resets to zero mid-draft:

```
[00:29:15] 14 real picks in
  !! bridge file went BACKWARDS (14 -> 0 picks). Holding the larger set.
[00:29:17] 15 real picks in
```

Monotone throughout. Both branches observed firing.

---

## 2. The clock incrementing by two — **the poll interval was never the problem**

The obvious read was "3-second poll against a fast mock." That is wrong, and it is worth
being explicit about how wrong, because it is exactly the shape of error §0.2 exists to catch:
a plausible cause, asserted, never measured.

Profiled the on-clock render:

```
16032275 function calls in 27.618 seconds
   13293 calls  _lineup()   <-- 27.0s of it
  186103 calls  np.isin()   <-- 10.0s of that
```

**`_lineup` is the whole tool.** One on-clock recommendation calls it ~13,000 times through
`rollout_scores`. It computes a 14-week starting-lineup total for a roster of **15 players** —
and it did that with numpy, where every call carried 50–100× more overhead than arithmetic on
a 15-element array. Measured cost: **16–20 seconds per on-clock render, ~4 seconds per waiting
render.** The board was not lagging because it polled slowly. It was lagging because it spent
four seconds thinking between every pick and sixteen on Matt's.

Rewrote `_lineup` in **pure Python**. No logic change — deliberately including the tie-break
detail that the players marked used are the first *k* in index order clearing the lowest taken
value, which is what `np.where(...)[:k]` did.

**Equivalence, tested the way §0.2 v5.5 requires — against the object production builds, not
an equivalent one.** `bench_lineup.py` wraps `Engine.lv_from` so every call the real engine
makes runs through both implementations and asserts they agree **exactly**, then runs the real
`recommend()` calls at seven draft states:

```
18,728 calls, 0 mismatches.  EXACT AGREEMENT.
```

Speed, same file:

```
pick 8, on the clock     1.92s   was  17.93s    9.4x faster   same order: True
pick 17, on the clock    1.68s   was  16.01s    9.5x faster   same order: True
waiting (mid draft)      0.43s   was   3.66s    8.5x faster   same order: True
```

The poll interval was dropped to **0.5s in bridge mode** as well (it reads a local file;
politeness is not a consideration), and the every-40-polls ESPN evidence snapshot is now
skipped in bridge mode — an 8-second network timeout inside the poll loop is the worst thing
that can happen to board latency, and in bridge mode ESPN is not the source anyway.

**Incidental find:** that snapshot's `polls` counter **was never incremented**. The block has
never once run. Fixed — §0.2 again.

---

## 3. The row count — two causes, one of them not the tier lines

Matt assumed the dashed tier dividers. They were half of it. The other half was worse:

```python
recs = eng.recommend(ref, rollout_inner=(24 if on_clock else 8),
                     top=(10 if on_clock else 8))
```

**The board dropped two rows every time it was not his pick and grew them back on his turn.**
That is the movement he was seeing, and it was in the code the whole time.

Fixed by construction rather than with a CSS `min-height`, so there is no pixel estimate to
get wrong: **exactly 12 player rows** (padded if the candidate list runs short) and **exactly
3 tier rows** (the biggest breaks; invisible spacers hold the remaining slots). Capping the
dividers at three is also an improvement on its own — a board with eight dashed lines
communicates nothing.

Verified across 73 draft states from pick 1 to pick 150:

```
distinct board shapes seen (pr rows, tier rows, pad rows): [(12, 3, 0)]
PASS
```

`top` is now 12 in both modes. It costs nothing at the new speed and the padding never fires.

---

## 4. `KeyboardInterrupt` traceback

Ctrl+C is the documented way to stop the tool and it printed a traceback — twelve lines of red
on the screen he is running the draft from. A traceback means *something broke*; nothing broke.
Wrapped at the entry point. It now prints `stopped. Nothing was written to ESPN.`

---

## 5. THE FINDING THAT MATTERS MORE THAN ANY OF THE ABOVE

`rollout_inner` is a Monte-Carlo sample count. It was set to 24 when a run cost 16 seconds —
i.e. it was set by what was affordable, not by what was needed. With a 10× speedup it became
cheap to ask whether 24 was enough. **It was not, at one specific pick.**

Ten runs per pick under ten different seeds:

| pick | inner | same #1 | distinct winners | margin over #2 |
|---|---|---|---|---|
| **8** | 24 | **10/10** (St. Brown) | 1 | 19.96 ± 0.55 |
| 8 | 60 | 10/10 | 1 | 20.21 ± 0.20 |
| 8 | 150 | 10/10 | 1 | 20.20 ± 0.13 |
| **32** | 24 | **7/10** (Egbuka) | **3** | **0.31 ± 0.35** |
| 32 | 60 | 9/10 | 2 | 0.15 ± 0.07 |
| 32 | 150 | 10/10 | 1 | 0.15 ± 0.07 |
| **56** | 24 | **10/10** (Burden) | 1 | 2.77 ± 0.18 |

Three things fall out of that table.

**(a) Pick 8 is closed, again, from a direction nobody tried.** Ten seeds, three sample sizes,
one answer: **Amon-Ra St. Brown, by 20 points.** §4.2 reached "best board player at 8" through
a paired dollar simulation against Josh Allen. This is an unrelated route to the same player,
and the margin is the largest on the board by an order of magnitude.

**(b) `inner` was quietly overstating every margin.** The winner is the max of twelve noisy
estimates, so it is biased upward: pick 32's margin *shrinks* 0.31 → 0.15 as samples rise, and
pick 8's *grows* 19.96 → 20.20. The headline number Matt reads was inflated at the small end,
which is precisely where he needs it honest. **On-clock `inner` is now 60** — 4.0s against
1.7s, still 4× faster than what he lived with on 2026-09-02.

**(c) PICK 32 IS A COIN FLIP AND MORE COMPUTE WILL NOT FIX IT.** The margin **converges to
0.15 points**. Raising `inner` from 24 to 150 does not find a winner; it makes the engine
*consistent about there not being one*. This is the longest-gap turn in Matt's draft (§2.1:
"17→32 is the longest gap"), it is where three keepers have already gone, and the engine has
**no opinion**. Pick 8 the engine decides. **Pick 32 he decides** — on §4.18's keeper option,
the analyst takes, the `12g` badge, the unsettled-backfield flag. The board's own "a coin
flip" tag is not hedging there; it is the correct answer.

---

## 6. The 3 QB / 3 TE mock roster

Matt's mock ended 4 WR / 2 RB / 3 QB / 3 TE, which breaks both his §6 doctrine and the
engine's `CAPS = {'QB':2, 'TE':2}`. **It was ESPN's autodraft.** The live tool has no write
path to ESPN — it renders a page, nothing more.

Confirmed the second half by driving the engine through **200 full drafts** against the
calibrated opponent model: **zero cap violations**. Roster shapes:

```
  94  {'QB':2, 'RB':5, 'TE':2, 'WR':3}
  70  {'QB':2, 'RB':6, 'TE':2, 'WR':2}
  31  {'QB':2, 'RB':4, 'TE':2, 'WR':4}
   5  {'QB':2, 'RB':3, 'TE':2, 'WR':5}
```

The caps hold. **But look at the first column: QB 2 and TE 2 in 200 of 200.** The engine treats
the cap as a target, and §6 treats the second QB/TE as *conditional* — "taken only after
landing on the wrong end of a drought." That gap is measured separately below.

---

## 7. `check_kit.py` had never seen the bridge

Every part of the draft-night pick source was invisible to the checker:

- `live_draft.py` was pinned at 80,868 bytes against an 86,022-byte file.
- `bridge_server.py` was listed under `Scripts\` but lives in `Scripts\live_draft\` — reported
  MISSING in one place and EXTRA in the other, for one file.
- `bridge_picks.json`, `bridge_raw.jsonl` and `espn_bridge\` all read as EXTRA, so the kit
  folder reported FAIL on its newest and most important contents.
- **The Chrome extension was not checked at all.** A stale `hook.js` is invisible: it connects,
  prints nothing, and simply never forwards a pick.

All five extension files are now pinned, `espn_bridge\` is its own canonical entry, the bridge's
runtime files are declared, and the three changed scripts are re-pinned. Dry-run on a
reconstructed tree: `PASS: canonical tree matches the manifest`.

---

## What is on disk now

| file | was | is |
|---|---|---|
| `Scripts\live_draft\live_draft.py` | 86,022 | **92,132** |
| `Scripts\live_draft\code_live_engine.py` | 16,576 | **19,135** |
| `Scripts\live_draft\bridge_server.py` | 19,993 | **20,850** |
| `Scripts\live_draft\bench_lineup.py` | — | **3,815** (new) |
| `Scripts\check_kit.py` | 15,009 | **17,621** |

Rollback: `_archive\live_draft_kit_pre138_20260903.zip` holds all four pre-change files. They
restore **as a set** — `live_draft.py` and `code_live_engine.py` changed together.

---

## Assumptions, and what would invalidate them

1. **`_lineup` is bit-identical.** 18,728 production-generated calls agree exactly and the row
   ORDER is unchanged at every tested state. Invalidated by: any board row carrying a NaN
   projection, which the numpy version sorts last and Python does not order at all. Nothing on
   the shipped board has one; a REBUILD on Sept 5 could introduce one. `bench_lineup.py` would
   catch it — **re-run it after any board rebuild.**
2. **The atomic write closes the empty-read window.** Invalidated by Google Drive's sync client
   holding a lock on `bridge_picks.json` at the instant of `os.replace`. The last-good cache
   covers that case anyway, which is why both fixes shipped.
3. **Pick 32's tie is real, not a modelling artifact.** It rests on §4.12's noise model and this
   board. A REBUILD verdict on Sept 5 changes the board and the tie may resolve — **re-run the
   seed check if the board changes.**

**The missing input that would most improve this:** a second live bridge run, at real draft
pace rather than mock pace, with `bridge_raw.jsonl` from a room that is NOT autodrafting. Every
frame captured so far came from an autodraft, which fires every ~1.5s and may batch `SELECTED`
differently from a room of twelve humans on a 60-second clock.

---

## 8. ADDENDUM — the QB2 question, asked of the shipped engine

§6 above left one thing open: the engine reaches QB2/TE2 in 200 of 200 drafts, while §6
doctrine treats the second QB/TE as conditional. So I asked the engine directly, at the two
picks where §4.18's draft-night rule actually lives.

24 opponent realisations each at **pick 104** and **pick 113**, `inner=24`, `top=12`, Matt
seeded with a realistic 1 QB / 2 RB / 3 WR / 1 TE roster:

| pick | engine's #1 row | if it says QB, margin over best RB/WR | if it says RB/WR/TE, best QB trails by |
|---|---|---|---|
| **104** | RB 15 · QB 5 · TE 4 | **0.64** (0.10 – 1.70) | **0.80** |
| **113** | RB 13 · TE 7 · QB 4 | **0.93** (0.20 – 2.20) | **1.10** |

**Every number in that table is inside the board's own "a coin flip" band (< 1.5 points), in
both directions.** The engine does not prefer the QB and it does not prefer the back. It has
no opinion, and it says so in the only units it has.

**This independently replicates §4.18 from a completely different direction.** §4.18 reached
"neither dominates, so the tiebreak is the PLAYER, not the position" by pricing QB2's 2026
edge (+5 to +11, §4.17/§4.17b) against the RB dart's keeper option (≈ +8 in 2027, from four
keeper transitions). Those are seasonal, historical, dollar-denominated arguments. This is the
shipped rollout, in points, on tonight's board. **Two unrelated methods, same verdict.**

Practical consequence for Sept 7: **at 104 and 113 the board will not decide QB2 for you and
is not supposed to.** §4.18's rule is the rule — *take the second QB only if the tier is Goff
or better AND no RB with a plausible 2027 role is on the board.* The QBs the engine names at
those picks are Purdy, Nix, Mahomes and Goff, so the "Goff or better" clause is live and doing
real work.

The names above are the engine's, not a recommendation — the room on the night decides who is
actually there.

---

## 9. THE BLIND SPOT — why §8's tie and doc 138's re-pricing are the same result

§8 left a tension I did not want to paper over. The shipped rollout says QB2-vs-RB at 104/113 is
a tie (margins 0.64 / 0.93, both inside "coin flip"). Docs 92 and 111 say QB2 is worth **+5 to
+11 points**. Those cannot both be describing the same quantity, so I went and looked at what
the rollout is able to see.

**`_lineup()` models exactly one kind of absence: the bye week.** There is no injury model —
every player plays all 14 non-bye weeks. So in the entire rollout, across all ~13,000
evaluations, **a backup QB can enter the starting lineup in exactly one week of the season:
QB1's bye.** Measured directly, on a plausible pick-104 roster (QB1 = Bo Nix, bye 10):

| second QB | bye | lineup value it adds |
|---|---|---|
| Brock Purdy | 8 | **+4.77** |
| Dak Prescott | 14 | +4.75 |
| Patrick Mahomes | 5 | +4.61 |
| Jaxson Dart | 8 | +4.46 |
| best RB available (Warren) | 9 | +2.20 |
| best WR available | 11 | **+0.00** |

and the decisive cut:

```
QB2 sharing QB1's bye  : mean added +0.00  (n=2)
QB2 on a different bye : mean added +2.49  (n=16)
```

**Two things fall out, and one of them is a gift to Matt.**

**(a) The rollout can price at most ONE of QB2's weeks, against 2.98 measured.** Doc 111 measured
that a drafted starting QB is missing **2.98 weeks a season** (n=48 team-seasons), worth 1.8–2.6
ppg each over a waiver replacement. The rollout sees the bye and nothing else — **the other two
weeks, roughly +3.6 to +5.2 points, are invisible to the ordering by construction.** Set that
against the 0.64–1.10 margin §8 measured in the RB's favour and the sign flips. **The board and
doc 111 were never in conflict; the board is blind in a direction I can now name and size.**

This does **not** apply to TE2. `_lineup`'s FLEX takes the best remaining RB/WR/TE every week, so
a second TE has a lineup path in all 14 weeks and the rollout prices it fully. §6's "TE is a
different question and must not be answered by analogy to QB" is right, and this is the
mechanical reason why.

**(b) A second QB on QB1's bye week is worth LITERALLY ZERO.** Not "worse" — zero, to two
decimal places, because he never starts. §6 records Matt's same-bye trap as a **preference**:
*"A same-bye second QB/TE is the specific trap — it doubles the hole instead of covering it."*
That was never measured. It is now, from the engine's own arithmetic, and it is not a preference
— it is arithmetic. **[Confirms a stated preference by measurement; the doctrine's reason was
correct.]**

### How this composes with doc 138

Fable's doc 138 (`138_keeper_value_does_not_persist.md`, same night) re-priced the other side of
the same decision: **the RB dart's keeper option is ≈ +0.7 [−2.0, +3.1], not the +8.5 §4.18
assumed** — a kept RB returns +6.7 VBD14, not +81, and NFL-wide a hit from preseason ADP 97+
returns **−3.9** the following year.

Put the three measurements together, all made independently and on different machinery:

| the 104/113 decision | source | value |
|---|---|---|
| what the rollout can see | this doc, §8 | **tie** — 0.64 / 0.93, coin flip |
| what the rollout CANNOT see (QB1's ~2 non-bye missed weeks) | this doc, §9 + doc 111 | **+3.6 to +5.2 to the QB** |
| the RB dart's 2027 keeper option | doc 138 | **+0.7**, was assumed +8.5 |

**§4.18's rule was built on the +8 keeper option cancelling QB2's +11. The +8 is gone, and the
board's own tie turns out to be a tie only because it cannot see two thirds of QB2's value.**
Both corrections push the same way. Fable's revised rule — *at 104 or 113, if a QB of Goff's
tier or better is on the board, take the QB2* — is what the engine would also say if it could
see missed weeks.

**Caveat, and it matters:** these are one measurement per side. Doc 138's own §5 lists n=18 kept
RBs and n=21 late NFL hits and labels every positional cut UNDERPOWERED. §9(a)'s +3.6 to +5.2 is
arithmetic on doc 111's 2.98 weeks, not a paired simulation. **The direction is now supported
from three unrelated angles; the size is not.** Do not quote a single number for it on the night
— quote the rule.

### What NOT to do about it

The obvious move is to teach `_lineup` an absence model so the rollout stops being blind. **Do
not do that before Sept 7.** §4.10's whole rule ranking, §4.2's pick-8 dollars and §4.12's noise
calibration were all fitted against this objective; changing what the objective measures four
days out invalidates the measurements that make the tool worth running. **Log it, use the §4.18
rule as the patch, revisit in the post-draft review.**
