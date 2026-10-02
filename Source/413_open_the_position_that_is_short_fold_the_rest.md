# 413 — open the position that is short fold the rest

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 24 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 413" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 1800

```
    # candidates: the best few at each position, priced
    # [doc 413] OPEN THE POSITION THAT IS SHORT, FOLD THE REST. Doc 369 catalogued this and it
    # was never worked: six positions x six men x thirteen week columns is 36 rows of a grid,
    # printed above the bar that explains what its numbers mean, and most weeks he needs ONE
    # position. A position opens when the best free man there actually beats your bar (season
    # total over 0.05) or when you have an empty slot ahead at that position; everything else is
    # one click away, not gone. Matt, 24 Sept: "it's too cluttered for me to figure it out."
    cand_html = ''
    _short = {}
    for p in POS:
```

### `build_news.py`, line 53

```

# [doc 413] THE FIRST LIVE RUN RETURNED 403 ON BOTH ENDPOINTS AND THE HEADERS WERE WHY.
# A custom User-Agent ("fantasy week sheet; personal use") is exactly what ESPN's edge rejects,
# and the container this was written in reaches the same URL fine, so the failure could only
# appear on Matt's machine. `wire.py` has talked to ESPN from that machine for weeks and sends
# NO User-Agent at all, but it does send a referer and an explicit accept -- so the proven shape
# is copied here rather than invented. Three profiles are tried in order and the LAST error is
# reported with the status code, so one run settles it instead of costing a round trip each time.
HEADER_PROFILES = [
    {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
```
