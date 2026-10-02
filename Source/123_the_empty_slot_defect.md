# 123 — THE WORST BUG IN THIS PROJECT. It was mine, it was reproducible, and it would have ended draft night before pick 1.

**Date:** 2026-09-01. Found because Matt refused to accept "we don't know" and ran it a third time.

---

## 1. WHAT HE DID THAT CRACKED IT

He ran the same command against a **different** mock room — `1286108548` instead of `1852814276` —
**while the room was live**, with no 404 at all. And it returned:

```
[00:11:20] 179 real picks in  (+1 keeper rows ignored)
```

**Identical counts. Different league. A mock that had not made a single pick.**

Two different rooms cannot coincidentally hold the same completed draft. **The moment the numbers
repeated, it stopped being a story about ESPN and became a bug in my code.** Everything I wrote in
docs 118–122 was chasing an external cause for something that was mine.

---

## 2. THE DEFECT, EXACTLY

**ESPN pre-creates the ENTIRE pick grid the moment a draft room opens** — 180 rows, one per
(round, team), each with a real `overallPickNumber`, a real `teamId`, and an **empty `playerId`**.
They are slots. Nothing has been picked.

`fetch_picks` filtered them like this:

```python
out = [p for p in out if p['pid'] and p['overall']]
```

**ESPN's empty-slot sentinel is a small negative number, and in Python `-1` is truthy.**
So every unfilled slot passed the filter. Then, in `step()`:

```
real = 179  ->  pick_no = 180  ->  if pick_no > 168: render_done()
```

**"Draft complete", instantly, with an empty roster — because no player was ever actually taken.**
That is precisely what his screenshots show: the amber *Waiting for ESPN* page for a fraction of a
second, then a completion page with nothing on it.

**IT WOULD HAVE DONE THE SAME THING AT 8:00 PM ON SEPT 7.** The room opens, ESPN lays out the grid,
the tool reads 180 picks and declares the draft over before Cary makes pick 1.02. Every recommendation
for the entire night, gone, and the printed board would have been the whole evening.

---

## 3. IT IS DOC 58 AGAIN, AND I HAD MY HANDS ON THIS EXACT LINE

Doc 58 fixed the *other half* of this filter: ESPN carries the 12 keepers inside `draftDetail.picks`
and counting them put the clock 12 picks ahead. **I fixed the keeper half and never asked what else
in that array is not a selection.** §3 says *"when a finding invalidates a metric, enumerate every
downstream use."* The finding was "rows in this array are not all picks." I enumerated one.

**And the same defect was live in a second place:** `fetch_keepers.from_draft()` matched on
`pk.get('keeper')` alone, so an empty slot flagged keeper would have come back as a keeper with no
player in it — at 7:00 PM on lock night. Fixed with the same rule.

---

## 4. WHY THE REHEARSAL LANE NEVER CAUGHT IT — the part that matters most

`rehearsal.py` served **only picks that had happened.** Real ESPN serves the whole grid from the
start. **The harness was kinder than reality, so it tested a shape that does not exist.**

This is doc 80's lesson word for word — *"a test must exercise the object PRODUCTION builds, not an
equivalent one"* — and the harness I built to prevent draft-night surprises had the same flaw as
the D/ST test that doc 80 caught. **A UAT lane that never fails is not evidence.**

`rehearsal.py` now emits the empty slots too. Re-run against the fixed tool:

```
feed carries 180 pick rows; 168 are EMPTY SLOTS (playerId [-1]) and are not selections. 12 real picks.
[04:21:22] 0 real picks in  (+12 keeper rows ignored)
[04:21:31] 1 real picks in  (+12 keeper rows ignored)
[04:21:39] 2 real picks in  (+12 keeper rows ignored)
```

**Zero at the start, counting up.** Before the fix, that same feed said 180 and quit.
`[VERIFIED by execution.]`

---

## 5. THE FIX, AND THE TRAP INSIDE THE FIX

**Negative is NOT the test.** Directive §8 records that all 32 defenses ride the wire as
`-16000 - proTeamId`. A naive `playerId > 0` filter would have deleted **every D/ST pick** — a
second bug hiding inside the fix for the first.

The rule is `abs(playerId) > 100`: keeps every real player (5–7 digits) and every defense
(~−16000), and cannot keep a `0` / `-1` / `None` sentinel. Tested against a feed carrying a real
player, a D/ST at −16016, and 177 empty slots of both sentinel shapes — 3 real picks out, the D/ST
among them.

Three more things now stand between this and a repeat:
- **It prints what it dropped**, once per run: `180 pick rows; 177 are EMPTY SLOTS (playerId [-1, 0])`.
  Silent filtering is how this survived.
- **`render_done` refuses to draw with zero players selected** and says so — a guard on the exact
  branch the bug came out of.
- **The raw payload is kept** (doc 122), so the next anomaly is evidence instead of archaeology.

---

## 6. WHAT MATT SHOULD ACTUALLY TAKE FROM THIS

**He found it, and he found it by not accepting my answer.** I wrote three documents explaining a
404 that was incidental, while the real defect sat in a line I had edited myself and never
re-examined. The reproduction he ran — same command, different room, watch the numbers — is the
experiment I should have asked for two documents earlier.

## ASSUMPTIONS

1. **`abs(pid) > 100` cleanly separates slots from selections.** Verified against the mock's
   observed sentinels and the D/ST id range; a third sentinel shape would need the payload, which
   is now being kept.
2. **The 404s on `1852814276` were a separate, incidental problem.** The new mock room did not 404
   at all, so the two failures are not the same failure. What the 404 was remains unknown and no
   longer matters.
