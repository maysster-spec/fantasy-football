# 429 — the roster clock is hosted not a file

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 25 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 429" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 1126

```
    ('../COMMANDS.html', 'commands'),
    # [doc 429] The Roster Clock is hosted, not a file on the drive, so it is the one absolute
    # href in this list and `at_root` must not prefix it with Source/.
    (CLOCK_URL, 'roster clock'),
    # [doc 430] AND THE OTHER TWO PUBLISHED PAGES, because this bar is the only hub that can point
    # BOTH ways. A browser refuses a file:// link from an https page, so nothing on the web can
    # link back to this PC. The local bar therefore carries everything; the online bar carries
    # only the online set and names the folder in text.
    (POCKET_URL, 'pocket sheet'),
    (TAKES_URL, 'the takes'),
```
