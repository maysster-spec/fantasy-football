# 118 — Two faults in the mock run, and the one that would have cost draft night

**Date:** 2026-09-01. Matt started an ESPN mock, pointed the tool at his real league, and got
`179 real picks in (+1 keeper rows ignored)` followed immediately by Draft complete, then 404 on
every poll after.

---

## 1. WHAT I CAN SAY, AND WHAT I CANNOT

**I reproduced the symptom exactly** with a canned feed of 180 picks, one flagged keeper, marked
`drafted: true` — the tool printed his line character for character. So the shape of what ESPN
served him is not in doubt: **a complete 15-round draft with exactly one keeper row.**

**What that feed IS, I do not know**, and per §0.2 I am not going to reason my way to a cause and
then write a fix aimed at it. Two candidates:
- ESPN serving a **prior season's** completed draft under the 2026 id because the 2026 draft does
  not exist yet.
- A different league entirely.

**One keeper row is the tell, and it argues against both of the obvious stories.** §2.1(b2)
verified **twelve** keeper rows at overall 169–180 on this league's real 2024 and 2025 drafts. A
feed with one does not have this league's shape in any year we have checked.

**`py live_draft.py --probe --league <id>` answers it in one command** and prints only what ESPN
returned: the `seasonId` in the payload, `drafted` / `inProgress`, the pick count, the keeper
count, the draft type and date from settings, and the first and last three picks with player
names resolved off the board. `[VERIFIED by execution against a canned feed and a canned 404]`

---

## 2. THE ESPN MOCK PROBABLY WAS NEVER GOING TO WORK, AND I SHOULD HAVE SAID SO

`--mock` removes keeper depletion and auto-detects the shape. **It does not find a mock.** The
league id still has to be the mock room's own id, and ESPN's mock lobby runs in an ephemeral
league that is very likely not served by `lm-api-reads` at all. **His real league id will never
show a mock, and I let him run that command believing it would.**

**The tested rehearsal path is `py rehearsal.py --realtime`** — doc 96, a local fake feed that
drives the real tool through a changing draft. That is the lane that exists precisely because
ESPN's is not dependable, and it is where an evening should have gone.

---

## 3. THE FIX THAT MATTERS MOST IS NOT THE DIAGNOSIS

The tool saw a complete draft on its **first poll** and rendered **"Draft complete"** — which
reads like a successful run. **That is the dangerous behaviour**, not the odd feed: a tool that
reports success while doing nothing is worse than one that crashes.

Now:
- **A complete draft on the first poll is called out loudly** and no "Draft complete" page is
  written.
- **It does not exit.** The first version of this fix broke out of the loop, and that is the worse
  mistake on Sept 7 — a tool that quits because ESPN served something odd once is a tool that is
  not there at 8:04 PM. It warns, then keeps polling; if the feed flips to a live draft it picks
  it up. Ctrl+C is the way out.
- Gated to `len(picks) > 24`, so a small or partial feed cannot trip it.

`[VERIFIED: the guard fires, prints, and the poller is still alive when the test times out.]`

---

## 4. THE 404 HINT NAMED THE WRONG SUSPECT — it named none at all

404 fell through to the generic branch; only 401/403 mentioned cookies. **For a private league an
expired `swid`/`espn_s2` can return 404 rather than 401**, and his first poll succeeded before the
404s started, which is exactly what an expiring session looks like. The hint now leads with
`py cookie_jar.py`, then the wrong-league-id case, then points at `--probe`.

---

## WHAT MATT SHOULD DO

1. `py live_draft.py --probe --league 1852814276` — one command, tells us what that feed is.
2. If it 404s: `py cookie_jar.py`, then probe again.
3. To rehearse tonight: `py rehearsal.py --realtime`. It does not touch ESPN.

## ASSUMPTIONS

1. **The reproduction matches his feed** because the printed line matches. It matches the *shape*;
   the contents are still unknown until he probes.
2. **ESPN mocks are not readable through this endpoint.** Strongly suspected from how mock lobbies
   work, **not verified** — the probe against a real mock id would settle it.
3. **Warning-and-continuing is safer than exiting.** A judgement about draft night, not a measured
   result.
