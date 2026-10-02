# 120 — What I actually know about the mock failure, and what I invented

**Date:** 2026-09-01. Matt: *"you asked me to run those commands AFTER it ended... Nothing yet
explains why the live draft crashed."* He is right, and doc 119 overreached.

---

## 1. THE RETRACTION

Doc 119 concluded that `1852814276` was a mock room ESPN had **torn down**, and that the tear-down
explained the 404s. **The timeline does not support it.** Every 404 I used as evidence was
collected *after* the mock had finished — because I asked him to collect it then. It says nothing
about the failure during the mock.

**What the tool actually did, in order, at 23:30:**
1. `23:30:31` — read the league. **Succeeded.** Printed `team 9 = JUG "The Poetry of Junkyard Juggers"`.
2. `23:30:32` — read `mDraftDetail`. **Succeeded.** 179 real picks + 1 keeper row.
3. Rendered **Draft complete** — a nearly empty page.
4. Every poll after that: **404.**

**A successful read followed immediately by unbroken 404s, on the same URL with the same cookies,
seconds apart.** That is not a tear-down and it is not an expired session. **I do not know what
it is.** Candidates I can neither confirm nor eliminate: ESPN rate-limiting a repeated poll by
returning 404 rather than 429; the mock room ending its draft phase and the id ceasing to resolve;
a routing quirk on `lm-api-reads`. **The league no longer answers, so none of this is recoverable.**

**This is `ERROR_PATTERNS` again and I walked into it inside a document that quotes the rule:
§0.2 says reproduce the failure before writing the fix. I could not reproduce it, so I explained
it instead.** The cookie finding was real and measured. The story I wrapped around it was not.

---

## 2. ONE MORE CLUE, WHICH THE PROBE COULD NOT SEE

**The "Draft complete" page was empty** — no roster. If those 180 picks were a completed draft
that team 9 took part in, that page would list fifteen players. **It listed none**, while `mTeam`
in the same payload said team 9 is JUG.

So the feed had teams that own picks *and* a team 9 that owns none of them. The probe printed pick
counts and keeper counts but never said **whose** picks they were, which is the one thing that
would have separated "a draft I am in" from "a draft I am not in."

**Fixed. `--probe` now prints the teams that own picks, the count per team, and explicitly whether
your team owns any** — with `<-- ZERO. This feed is not a draft you are in.` when it owns none.
`[VERIFIED by execution.]`

---

## 3. THE QUESTION THAT ACTUALLY MATTERS NOW

Not "what was in a league that no longer exists." **It is: what does the REAL league return today?**

If `21985`'s 2026 `draftDetail` already holds a completed draft, that is a Sept 7 emergency and we
need seven days of warning, not seven minutes. If it holds zero picks, the tool is fine and the
whole episode was about an id that was never ours.

```
py live_draft.py --probe
```

No `--league`. It defaults to 21985. **That is the only thing worth running from this.**

---

## 4. WHAT SURVIVES FROM DOCS 118 AND 119

- **The cookies are fine.** Measured: 21985 answers 200 with them.
- **A complete draft on the first poll no longer renders "Draft complete"** and no longer ends the
  run. That guard is the real value from this whole episode, and it is independent of the cause.
- **404 now self-diagnoses** against the known-good league instead of listing suspects.
- **Ctrl+C exits cleanly.**
- **Chasing an ESPN mock with this tool is unproven and should not be attempted again before
  Sept 7.** `py rehearsal.py --realtime` is the tested lane.

## ASSUMPTIONS

1. **The screenshot is the completion page from that run.** Matt says "as the draft first started,
   not sure of the actual second mark," so its exact position in the sequence is his recollection.
2. **The empty roster means team 9 owned no picks in that feed.** Consistent with the render code,
   not independently verified against that payload — which no longer exists.
