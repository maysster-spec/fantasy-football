# 121 — "How do we know the cookies were good for that room?" We do, and not from cookie_jar.

**Date:** 2026-09-01. Matt asked the question that catches the weak link in both prior docs.

---

## 1. THE ANSWER — and cookie_jar is NOT the evidence

`cookie_jar` proves the cookies work **for league 21985, after the mock was over.** That is the
wrong league at the wrong time and I leaned on it as though it were the proof.

**The real proof is in his own console output, from during the mock:**

```
[23:30:31] league 1852814276 season 2026 team 9
  team 9 = JUG  "The Poetry of Junkyard Juggers"   <- IS THIS YOU?
[23:30:32] 179 real picks in  (+1 keeper rows ignored)
```

Two authenticated reads against **1852814276**, one second apart, and the first one **came back
with his own team's name.** ESPN does not hand a private league's team names to an unauthenticated
caller. **So the cookies were unquestionably good for that league at 23:30:32** — and every 404
came *after* that.

The chain that actually eliminates cookies:
1. **23:30:31–32** — two successful authenticated reads on `1852814276`. Cookies good, that league, that moment.
2. **23:30:33 onward** — 404 on the same URL.
3. **Later** — `cookie_jar` reports the cookies **stored in the scripts** still work. `set_cookies`
   writes the same values into all four scripts including `live_draft.py`, so these are the same
   cookies, unrotated.

**Same credentials, working before and after, failing throughout the middle.** Cookies are ruled
out — but by his console log, not by `cookie_jar`.

---

## 2. THE DISTINCTION I HAD COLLAPSED, AND IT MATTERS

**A valid cookie and access to a given league are two different things, and ESPN returns 404 for
both.** A session can be perfectly valid while the account is not authorised for a particular
league — and being removed from a mock room the instant its draft ends would look exactly like
that: a 404 that has nothing to do with cookie validity.

So the honest statement is narrower than what I wrote:

| I said (doc 119) | what is actually supported |
|---|---|
| "the mock room was torn down" | unsupported — invented to fill the gap |
| "that league does not exist any more" | **unknown.** 404 means ESPN will not serve it to you |
| "your cookies are fine" | **true**, and provable — but from the 23:30 log |

**The probe was repeating the same overclaim** — it printed *"League X does not exist for season Y
any more."* It cannot know that. It now says the cookies are **valid**, that a stale session is
therefore not the cause, and **explicitly that it cannot tell whether you are authorised for the
other league**, because 404 covers both. `[VERIFIED by execution.]`

---

## 3. WHY THIS KEEPS HAPPENING TO ME IN THIS PROJECT

Three documents in a row now: a real measurement, then a causal story bolted onto it that the
measurement does not carry. Doc 57 sized a defect at 78 points and it measured 0.26. Doc 91
declared a quantity unmeasured that had been measured. This one turned "the cookies are valid"
into "the league is gone."

**The tell is the same every time: the moment the sentence stops describing an observation and
starts describing a mechanism.** "21985 returns 200" is an observation. "The room was torn down"
is a mechanism, and nothing in this project ever saw a room being torn down.

## ASSUMPTIONS

1. **ESPN will not return a private league's team names unauthenticated.** Standard for this API
   and consistent with everything this project has seen, but not tested here deliberately.
2. **`set_cookies` really does write identical values to all four scripts** — that is what it is
   for, and doc 86 verified it.
