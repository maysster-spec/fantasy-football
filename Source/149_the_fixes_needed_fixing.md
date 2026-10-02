# 149 — The fixes needed fixing

**2026-09-03, late. T-4 days.** Matt, one line: *"if you made changes, have it run the code test
again."*

He is right and it is the obvious next move that I did not make on my own. **Doc 148 accepted five
findings and wrote fourteen edits in about an hour, and those edits were then completely
unreviewed** — written under time pressure, by the same person who wrote the defects they were
fixing. So the same agent that found them was sent back at them, with the before and after files
and its own five findings to check off.

**It returned six more. Two of them are worse than what they replaced.**

---

## 1. THE ONE THAT MATTERS: MY FIX COULD FREEZE THE BOARD

Doc 148 finding 5 was that the collapsed legend closed itself three seconds later. My fix held the
page reload while the legend was open, sharing the `held` counter with the existing board-hover
branch. **`mouseleave` on the board resets `held` to 0** — so moving the mouse on and off the
table, which is the ordinary motion of reading a glossary that sits directly under it, renewed the
hold every time. Simulated over two minutes of the shipped interval body:

| state | reloads in 120 s |
|---|---|
| baseline, legend shut | 37 |
| mouse parked on the board (the pre-existing 25 s cap) | 4 |
| **legend open, mouse crossing the board every 8 s** | **0** |

**Zero.** The 25-second cap exists, in a comment I read and did not connect, *"so a mouse left on
the table can never freeze the night's most important screen"* — and I defeated it. On a
60-second clock a frozen board is worse than no board, because it still looks like a board.

**And the second half of the fix was untestable.** `history.replaceState` with a URL argument from
a `file://` document is refused by Chrome, and I had wrapped it in `catch(e){}`, so **both
outcomes were silent**: either it worked and the legend re-opened on every load (holding the
reload indefinitely, above), or it threw and the persistence never existed at all. There was no
configuration in which the shipped behaviour was the intended one.

**FIXED — the board must never stop refreshing, so there is no hold at all.** The open state
survives via `location.hash`, which is a plain fragment navigation allowed on every origin
including `file://`, and `location.reload()` carries it. The page keeps its three-second rhythm
underneath. Reading the legend costs a reflow; it cannot cost the board.

---

## 2. THE FEED-STALL BANNER WAS INERT IN EXACTLY ITS OWN SCENARIO

Doc 148 finding 2 added a red banner for a bridge that has stopped receiving. It renders through
`step()`, and `step()` is called from `if len(picks) != last:`.

**A stalled feed is by definition one whose pick count stops changing.** Executed: 20 picks arrive,
then 30 polls at a frozen count with the age climbing from 10 to 39 minutes —

```
pages rendered: {'BOARD': 20, 'WAITING': 1}     any page carrying the banner: False
```

It appeared only in the run where a **new pick arrived** — i.e. only where the feed was
demonstrably alive. A warning that fires only when it is wrong. **FIXED:** the page is now
re-rendered on the transition into a stall and on the way out, so the banner reaches the screen
the moment the condition it describes becomes true. The threshold also moved 90 s → **180 s**: 90
seconds is inside one ESPN pick clock, so a manager letting it run out would have tripped it.

---

## 3. FOUR MORE

**My keeper fix invented keepers in every mock.** Doc 148 finding 9 was right that round-15 /
overall-169–180 rows are keepers *in this league*. Applied unconditionally it flagged **10 rows in
a 10×16 mock, 12 in a 12×16, 26 in a 14×15, 8 in an 8×15** — and `pick_no` counts non-keeper rows,
so the clock ran that many picks BEHIND the room for the rest of the run. The pre-fix code was
*right* about mocks and wrong about the real draft; mine reversed it. `--mock` now turns the row
detection off with the depletion, and says so.

**My "past pick 137" fix did not fix what its own comment claimed.** It changed `ref`, and
`Engine.recommend` and `Engine.cliffs` derive their own next-turn from `MY_PICKS` independently —
which still ends at 137. Executed at picks 138 / 145 / 153 / 160: **`cliffs` still empty, every row
still `100% still there`, footer still "your picks done"**, all three named symptoms intact across
~22 picks. Widening `MY_PICKS` is not a four-days-out change — it feeds the survival maths and
§4.12's calibration. **What is safely fixable is what the page SAYS:** the remaining-turns list now
includes 152 and 161, so the hero names the next turn instead of `-` and the footer stops claiming
you are done. The rest is recorded here as unfixed rather than left as a comment that lies.

**The stale-file message named a clock it no longer reads.** The check moved to `updated`; the
message still said *"a listener that started 9.0 hours ago"* — printed while the listener had
started that second — and offered the remedy for the old failure, not the new one it now detects.

**Two smaller ones:** the `_SAW_PICKS` latch guarded only the *start*, so on the ESPN path an empty
feed mid-draft still reached `step()` and rendered doc 148's pick-1 page displaced to mid-draft
(the bridge path was already covered by the subset guard); and the runbook's *"confirm the first
poll line reports the keeper-row count"* could stop printing entirely behind the new waiting latch
— so the count is now stated once, out loud, the first time any picks are read, **including when
it is zero**.

---

## 4. WHAT THE SECOND PASS ALSO CONFIRMED

Not everything was broken. Executed, on the shipped file: the cliff interval now matches
`Engine.cliffs` at three separate waiting states (`nxt` = 41 / 65 / 113, internal `nxt` identical);
`cmax` is gone with no orphan reference and a full bar means 20 points at every pick; two rows can
no longer both read `free`; `on_clock` is in scope so the waiting board shows row 1's survival
again; the pid filter drops `None`/`'abc'`/`0`/`-1` and keeps a D/ST at `-16011`; `#gloss` being
absent on the streamer, done and waiting pages is handled; and the fixed 12 + 3 + 8 shape held
across 27 real states plus the adversarial set with no exception anywhere.

One disclosed consequence of the fixed bar scale: at the steep turns it **saturates** — pick 8 has
7 rows at 100% (spanning −20 to −28.4). Within that block the bar stops discriminating. That is the
price of a constant meaning and it is the right trade; the numbers are still there to read.

---

## 5. THE FULL BATTERY, RE-RUN AFTER THE SECOND ROUND

- **21 of 21 guards fire** against their own defects, including the six added tonight — the stalled
  feed rendering its banner, `--mock` not inventing keepers, the real league still finding them,
  the legend hold being gone, the hash not using `replaceState`, and a warning containing markup
  being escaped.
- **All 180 draft states** through the production path: 52 s, no exception, shape 12 + 3
  everywhere, clock equal to the pick fed in, no `NaN`/`None` leaking, well-formed markup.
- **The engine did not move**, again: identical twelve players, identical order, identical
  `cost vs #1` strings at five states.
- **The full dress rehearsal, end to end, exit 0** — 168 picks, all fourteen turns, D/ST at 152,
  kicker at 161, Draft complete. And the new line prints where the runbook needs it:
  `KEEPER ROWS IN THE FEED: 12  (12 expected for this league)`.

---

## 6. THE LESSON, AND IT IS NOT A NEW ONE

**A fix is a change, and a change is unreviewed code.** Doc 148 ran a red team, accepted its
findings, wrote fourteen edits and shipped — and two of those edits were worse than the defects
they replaced, one of them capable of freezing the draft board. **The review has to run again after
the fixes, and Matt is the one who said so.** It cost one message and it caught a freeze.

Put it next to §0.2's existing rule that a diagnosis is a claim: **a remedy is a claim too.** The
fix for a measured defect is not measured merely because the defect was.
