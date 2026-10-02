# 119 — It was never the cookies. What the 404 IS, I still cannot say.

> **[CORRECTED 2026-09-01, after Matt pointed out the timeline.] The version below concluded**
> **"the mock room was torn down." That does not fit and I should not have written it.**
> He ran the probe and `cookie_jar` **after the mock had already ended**, at my request — so
> those 404s say nothing about why the tool 404ed **during** the mock, seconds after a
> successful first read. The cookie finding stands. The cause of the original failure does not,
> and is now unrecoverable: that league will not answer. See doc 120.

**Date:** 2026-09-01. Three commands in sequence answered it, and the second one is the evidence.

---

## THE CHAIN

| command | result | what it proves |
|---|---|---|
| `--probe --league 1852814276` | **HTTP 404** | that id will not resolve |
| `py cookie_jar.py` | **HTTP 200, 12 teams — "ALREADY FINE"** | **the cookies work** |
| `--probe --league 1852814276` | **HTTP 404 again** | nothing to do with cookies |

**`cookie_jar` tests league 21985** (`set_cookies.py`, `TEST_URL`) — same host, same season, same
two cookies. It got a 200. **`1852814276` got a 404 with those identical cookies.**
That is not an authentication failure. **That league does not exist.**

**21985 is the E-Discovery league.** It is `LEAGUE_ID` in `live_draft.py` and the default for
`--league`. **1852814276 was the ESPN mock room** — which is exactly what a mock room looks like
over its life: it answers while you are in it (at 23:30 it returned the JUG team name and a pick
feed) and 404s the moment ESPN reclaims it.

**Why that feed was already 180 picks deep with one keeper row is now unanswerable** — the league
is gone and nothing can be re-read from it. It also no longer matters. A mock id is disposable and
does not belong in a command.

---

## THE FIX: THE PROBE NOW ANSWERS THIS INSTEAD OF LISTING SUSPECTS

The old 404 branch offered two theories in likelihood order and made Matt spend a cookie refresh
on the wrong one. **The tool could just settle it, and now does:** on any 404 it immediately re-runs
the same request against the known-good `LEAGUE_ID` with the same cookies, same host, same season.

- **known league 200 →** *"YOUR COOKIES ARE FINE. League X does not exist for this season any more,"*
  plus what a torn-down mock room looks like, plus `py live_draft.py` with no `--league`.
- **both fail →** *"this is NOT about which league"* → `py cookie_jar.py`.

`[VERIFIED by execution against a server that 200s for 21985 and 404s for everything else.]`

**This is the §0.2 pattern in miniature.** The first version reported a defect and *reasoned* about
its cause. The second version measures it. A diagnostic that lists suspects makes the human do the
experiment; a diagnostic that runs the experiment costs one extra HTTP call.

---

## AND THE CTRL+C TRACEBACK

`time.sleep(a.interval)` sat **inside** the `except` handler, so Ctrl+C during a retry raised on top
of an already-handled exception and printed *"During handling of the above exception, another
exception occurred"* over eight lines of traceback. Harmless, and exactly the wrong thing to be
reading at 8:04 PM — it buries the message that matters. Ctrl+C there now prints
`stopped. Nothing was written to ESPN.` and returns.

---

## FOR DRAFT NIGHT

**Do not pass `--league`.** It defaults to 21985. The only reason it was ever typed was to chase a
mock, and chasing an ESPN mock with this tool does not work — the room is ephemeral and unreadable
once it closes.

**`py rehearsal.py --realtime` is the rehearsal.** Local fake feed, real tool, a draft that actually
changes pick by pick. That lane exists because ESPN's does not hold still.

## ASSUMPTIONS

1. **21985 is the right league.** Corroborated three ways: it is `LEAGUE_ID`, `set_cookies` uses it
   as the health check, and it just returned 12 teams.
2. **1852814276 was the mock room.** Strongly implied — it served his team name and a draft feed at
   23:30 and 404s now — but unverifiable, because it is gone.
