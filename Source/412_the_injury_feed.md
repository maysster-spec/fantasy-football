# 412 — The injury feed, which is doc 408's missing input

*24 Sept 2026. `Scripts\build_news.py`, new. ff.bat step 0.*

## THE SOURCE
**ESPN's PUBLIC injuries endpoint**, `site.api.espn.com/apis/site/v2/sports/football/nfl/injuries`.
No cookies, no auth, so nothing here touches `wire.py`'s session. Per entry it carries: `status`,
`date`, and a `details` object with `type` (Achilles, Knee), `location`, `detail` (Surgery) and
**`returnDate`**. That last field is the thing doc 408 says was missing.

**Rejected: the general news endpoint.** `/news` returned 15 articles, and with `limit=50` they
were from 30 August. Thin and stale for a 15-man roster.

## THE JOIN IS AN ID (§3)
The injuries feed carries **no athlete id field**. Every athlete's `links` href contains one
(`/nfl/player/_/id/4428718/...`) and that number **is the fantasy `espn_id`** — verified against the
24 Sept pull: Marvin Harrison Jr is 4432708 on both sides. Where no id can be extracted the row
falls back to **name + position + team**, which is §3's stated fallback, and a `source` column says
which key it used. **Never a bare name join.**

## IT REFUSES RATHER THAN RETURNING A THIN FILE
The league-wide endpoint has been observed returning **one team**. Below 20 teams `build_news.py`
falls back to the per-team endpoints and, failing that, **exits 2 and writes nothing**. A news file
covering part of the league is worse than none: the sheet would print nothing beside a man who is
actually hurt. `ff.bat` prints `*** NEWS FEED DID NOT REFRESH` on a non-zero. **Doc 146: an exit
code is not a result, so the file is re-read and its row count checked after writing.**

## WHERE IT LANDS ON THE PAGE
**In the drop-cost table, beside every man, which is where the Dowdle recommendation was made:**

> Rico Dowdle · RB · bye 9 · the seat behind Jaylen Warren · **Questionable, Knee, back 09-28** · 7.6 · 4.1

## TESTED WITHOUT TOUCHING THE NETWORK
The parser was run against fixtures built from the live payload's exact shape: id extracted from
href, graceful fallback when `links` is empty, dates clipped, `details` carried. **Negative control
run first:** a one-team payload returns exit 2 and writes nothing.

## A TRAP, THE SECOND TODAY
The render kwarg was first named `news`. `render()` already rebinds `news` twice internally (lines
~1580 and ~2190, both to strings), so by the drop table it was a string and unpacked as *"too many
values to unpack (expected 3)"*. Renamed `news_lookup`. **Same collision as `season` in doc 410,
six hours apart. Grep before naming a parameter in `render()`.**

## [NOT YET RUN]
The first live run is its own verification: I could not confirm through a summarising fetch whether
the league-wide endpoint returns all 32 teams. `ff.bat` answers it in the log on the next run.
