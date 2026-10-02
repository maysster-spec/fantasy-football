# 148 — Nine things that would have cost Monday

**2026-09-03, late. T-4 days.** Matt: *"stress test the live board and red team… or other checks
to ensure no other bugs?"*

Answer: yes, and it was the most productive hour of the day. Nine defects that would have shown on
draft night — **five of them mine, shipped this afternoon in doc 147.** Everything below is fixed,
and every fix has been fired against the specific defect that motivated it (§0.2).

> **PROVENANCE CORRECTION, added the same evening — I got this wrong the first time.** The version
> of this doc first written said *"two independent adversarial agents ran in parallel."* **One
> agent ran.** It was given the render diff and it returned §5's five findings, executed. The seven
> bridge and draft-path defects in §1–§3 came from **my own read of `_bridge_picks`, `fetch_picks`,
> `step` and `bridge_server.py`**, not from a second reviewer, and I reported them to Matt as a
> second agent's work. The defects are real and independently demonstrated — every one has a guard
> in §6 that fires against it, and a guard cannot fire against a defect that was not there — but
> **the attribution was invented, which is §3's rule broken in my own write-up.** Say where a
> finding came from, or do not name a source.

---

## 1. THE WORST ONE, AND IT WAS NOT NEW

**An unconnected bridge rendered a confident, complete, entirely correct-looking PICK 1 BOARD.**

`_bridge_picks` returns an empty list — not an error — when the file is missing, when the
extension is not loaded, when the wrong Chrome tab is open, when the listener was never started.
`0 != last(-1)`, so `step()` ran, `pick_no` came out as `len([]) + 1 = 1`, and the page rendered:

```
ON THE CLOCK  1   Cary (DUCK)   round 1        TAKE  Jahmyr Gibbs
```

Every number on it correct, every number on it meaningless. And because the pick count then never
changed, **it rendered once and was never rewritten** — so it never even went stale-looking. The
console said `0 real picks in` a single time, in the same format as a healthy line.

This is the most likely startup failure on the night, and it looked exactly like success.

**FIXED:** an empty feed *before the first real pick* is not a draft state, it is "not connected".
The board holds the amber **Waiting** page and prints, every 20 polls: *"no picks read yet — NOT
rendering a board. Is bridge_server.py running, and is the draft room open in the Chrome that has
the extension loaded?"* Once any pick has arrived the latch is done and the LOST PICKS guard owns
the empty-file case.

---

## 2. THE KEEPER FILTER WAS INERT ON THE ONLY PATH THAT RUNS SEPT 7

`_bridge_picks` stamped **`'keeper': False` on every row, unconditionally.** So doc 58's fix — the
one that stops twelve keeper rows advancing the clock and cost this project a live board that
never fired — could not fire from the bridge. And because `nk` was therefore always 0, the
runbook's *"confirm the first poll line reports the keeper-row count"* was **unsatisfiable**: its
absence was indistinguishable from health.

The 09-02 capture was a keeper-less practice room, which is why nobody saw it.

**FIXED:** rows at `round == 15` or `overall` 169–180 are flagged keeper on the bridge path too
(§2.1b2, verified on the real 2024 and 2025 drafts). `[TESTED]` — 12 keeper rows + 7 real picks
now render the clock at **pick 8**, not pick 20.

---

## 3. SEVEN MORE, ALL EXECUTED, ALL FIXED

| # | what | trigger |
|---|---|---|
| 3 | **The staleness gate read the wrong clock.** It measured `session_started` — when the *listener* booted — so a listener left running since lunchtime made a live feed "stale" and every real pick was discarded, while a file whose listener started a minute ago and then **stopped receiving** was accepted forever. | either direction |
| 4 | **A frozen feed was invisible.** `updated` was returned by `_bridge_picks` and consumed by nothing. Tab closed, `hook.js` detached, socket dropped → a normal board, permanently behind, forever, and the page's own "updated" line is the *render* time, which keeps ticking. | any disconnect |
| 5 | **The LOST PICKS guard released one pick too early.** It held while `len(new) < len(old)`; at **equal** length it accepted the swap. A restarted listener refilled the file to the same count with different picks and the board silently handed every pre-restart player back — at a real 60-pick state it went on to recommend **Gibbs and Bijan as available at pick 120**. | listener restart |
| 6 | **A null pid froze the page and flooded the console.** The `abs(pid) > 100` filter existed only on the ESPN path. From the bridge, `None` raised `TypeError` inside `set_taken`, the loop caught it, deliberately did not advance, and retried the same broken state **every 0.5 s** — four console lines a second — while the browser kept showing the last good board looking healthy. | one malformed row |
| 7 | **`ONCLOCK 9 60000` was captured as "team 9 drafted player 60000".** Five of the eight `PICK_VERBS` were guesses; this one is a team plus a 60-second clock in milliseconds. One phantom pick per message, and the pick counter never recovers — doc 58 with a different cause. | if ESPN emits it |
| 8 | **Auto-promotion was still armed.** It existed because the pick verb was unknown. It is not unknown. Any unknown verb carrying three large numbers plus one in 1–32 could still inject picks, with nothing but a line in the *other* window to say so. Verified: four `NOMINATED` lines promoted `NOMINATED`. | any new verb |
| 9 | **The JSON path never deduped by playerId.** v1.5 fixed exactly this for the line protocol — ESPN re-sends history on every socket reconnect — and left the other path keyed on pick number, so one player under two pick numbers counted twice. Every duplicate is one pick of drift. | socket reconnect |
| 10 | **Past pick 137 it planned for a turn already taken.** `MY_PICKS` ends at 137, so `next(...)` fell through to `MY_PICKS[-1]`: survival came back all-ones, every row read **100% still there**, cliffs came back empty, and the footer said *"your picks done"* while 152 and 161 were still to come. | picks 138–168 |

---

## 4. THE FIX THE RED TEAM PROPOSED WOULD HAVE DELETED THIRTEEN PLAYERS

For #7 the agent proposed *"require a plausible playerId range (5–7 digits)"*. Reasonable. It was
measured against the shipped board before being written:

```
board espn_id: n=480   min=8,439   max=5,220,680
13 ids below 100,000:  8439, 11252, 11394, 12483, 14163, 14880,
                       15818, 15847, 15864, 16002, 16733, 16737, 16800
```

**Four of them sit in the 16,000s — the same magnitude as the `-16001 … -16032` a D/ST rides on.**
A magnitude test cannot separate a clock from a player on this board; it would have silently
deleted thirteen real players from the feed. §0.2 in one line: *report the defect, then measure,
then report the cost.* The red team was right about the defect and wrong about the fix.

**What actually separates them is grammar, not magnitude.** A past-tense verb reports an event
that has happened. `PICK_VERBS` is now `{SELECTED, PICKED, DRAFTED, AUTOPICK}`; `SELECT, PICK,
DRAFT, ONCLOCK` are watched and reported as candidates, never trusted, and `--loose` re-arms them
together with promotion if ESPN changes its wording on the night.

**THE NEGATIVE CONTROL — this is what makes the change safe.** Replaying the real 2026-09-02
capture (1,541 events, the draft that ran live end to end) through both versions:

| | picks | unique pids | duplicates | promotions |
|---|---|---|---|---|
| shipped | **179** | 179 | 0 | 0 |
| patched | **179** | 179 | 0 | 0 |

And the verb census from that log settles it — the four dropped words **never appear at all**:

```
402 SELECTING   400 SELECTED   366 AUTOSUGGEST   172 CLOCK
 75 PONG          7 AUTODRAFT     6 STATE          4 INIT / TOKEN / JOINED
```

---

## 5. FIVE OF THE NINE WERE MINE, FROM THIS AFTERNOON

Doc 147 was a layout pass. It introduced:

1. **A wrong number in the headline.** The waiting panel said the cliff drop was *"between now and
   then"*, and the clause before it binds "then" to Matt's next pick. `Engine.cliffs` uses
   `p > pick_no`, so the drop actually spans now → **the turn after next**. Measured at pick 30:
   the page said *"the RB board drops 23.4 between now and then"* while he is up at 32, and 23.4
   is the decline to **41**. The correct pick number was already being passed in and never used.
2. **A bar whose length meant something different at every pick.** It normalised to the worst row
   on screen, so the bottom row drew a full bar always: full meant 40 points at pick 17 and 4.6 at
   pick 89. Worse, on a flat board nine rows tagged `tie` carried bars from 18% to 82% — the
   graphic contradicting the label beside it. **Now a fixed scale: full = 20 points behind, at
   every pick, all night**, and the legend says so.
3. **Two rows both rendering green "free"** in 6 of the swept states — `cost` is rounded to 1 dp,
   so anything within 0.05 becomes `-0.0`, and `-0.0 == 0` is True — against a legend I had just
   rewritten to promise only one can. Row 1 is the recommendation *by position* now.
4. **Blanking row 1's survival number was only right on the clock.** While waiting, row 1 is the
   player the new hero headlines as "IF THE BOARD HELD, YOU TAKE" — so a 24%-to-last player was
   presented as the plan with his odds deleted from the entire page.
5. **The collapsed legend closed itself three seconds later.** `HOLD_JS` reloads every 3 s and
   suppresses only while the pointer is over `#board`; the `<details>` sits outside that zone. The
   one on-page explanation of the two things I had just changed could not be read at all. Now the
   open state rides in the URL hash (which survives `location.reload()`) **and** an open legend
   holds the reload, under the same 25-second cap as the board.

**None of the five would have raised anything.** All five produce a page that looks right.

---

## 6. WHAT WAS PROVEN AFTERWARDS

**Every guard fired against its own defect — 14 of 14.** Not "the code looks right": each was run
against the exact input that motivated it, including the two escape hatches.

```
G2  feed age measured (2400s) and the PAGE carries the banner      PASS
G3  round-15 rows flagged keeper -> clock reads 8, not 20          PASS
G4  null / 0 / -1 pids dropped; step() survives the feed           PASS
G5  pick 145 plans for 152 and pick 155 for 161, not 137           PASS
G6  equal-length swap HELD, and it says LOST PICKS                 PASS
G7  ONCLOCK + a clock is not a pick; SELECTED still is;
    --loose puts it back                                           PASS
G8  the same player twice via JSON is one pick                     PASS
```

**Every draft state, not six.** All 180 rendered through the production `step()`: no exception, no
state slower than 5 s (51 s for the lot), the fixed 12 + 3 shape everywhere, the clock number on
the page equal to the pick fed in, no `NaN`/`None`/`undefined` leaking into the HTML, well-formed
markup at every state.

**The engine did not move.** Five draft states before and after: identical twelve players, in
identical order, with identical `cost vs #1` strings.

**And the full dress rehearsal ran end to end in the container** — the fake-ESPN harness driving
the *real* board through a changing draft, which §8 records as the one loop nobody had exercised.
168 picks, all fourteen of Matt's turns, the D/ST page at 152, the kicker page at 161, the Draft
complete panel, **exit 0, zero errors**, and `(+12 keeper rows ignored)` on all 161 polls.

---

## 7. THE LESSON WORTH KEEPING

**The agent was told to execute, not to read — and every finding it returned came from execution.**
The two defects that survived my own review this afternoon (the wrong cliff interval, the legend
that closes itself) are invisible in the source and obvious in a screenshot or a run.

Add it to §0.2 as the render-layer form of the rule already there: *a page is an object too.
Build the real one, at more than one state, and look at it.*

**And on offloading (§5 of `00_START_HERE`): the shape that works is one mandate, execution
required, verification required, severity forbidden, editing forbidden. It reports; one place
integrates.** That last rule is what stopped the thirteen-player deletion in §4 from shipping.

**The counter-lesson is in the correction at the top of this doc.** The review earned its keep and
I still mis-stated where half the findings came from. A doc that inflates its own provenance is
the same defect as a magnitude that was never measured — it makes the reader trust the wrong
thing. **Doc 149 is the follow-up, and it starts by sending the SAME agent back at my fixes.**
