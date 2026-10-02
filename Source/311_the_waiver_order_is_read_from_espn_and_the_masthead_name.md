# 311 — the waiver order is read from espn and the masthead name

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done about 15 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 311" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `wire.py`, line 1313

```
                 f'Check these by eye:<br><br>{shown}{more}</div>')
    # doc 311: the real number, or an honest silence. NEVER the old hard-coded "near the back".
    if waiver_rank and waiver_n:
        _wa = waiver_ahead or []
        if _wa:
            _wl = (f' <b>This week you are {waiver_rank} of {waiver_n}, and the '
                   f'{len(_wa)} team{"s" if len(_wa) != 1 else ""} who pick before you '
                   f'{"are" if len(_wa) != 1 else "is"} {_esc(", ".join(_wa))}.</b>')
        else:
            _wl = f' <b>This week you are first of {waiver_n}. Nobody picks before you.</b>'
```

### `wire.py`, line 1391

```

    # --- THE WAIVER ORDER, READ FROM ESPN RATHER THAN ASSERTED (doc 311) --------------------
    # The page has been saying "you are near the back of the line" as a HARD-CODED STRING since
    # it was written. Priority resets every week to inverse standings (section 2), so a fixed
    # sentence is wrong most weeks by construction, and it is the one number 4.32 term 4 needs:
    # you cannot count the teams AHEAD of him without knowing where he stands. Doc 254 logged it
    # [OPEN] on 9 Sept and nothing read it.
    # It is FETCHED, never assumed: if ESPN does not serve the field, the page says the order is
    # unknown rather than printing a number or repeating the old sentence (0.2).
    waiver_order, my_waiver_rank, ahead_of_me = [], None, []
```

### `check_kit.py`, line 113

```
    # LAST COMPLETED GAME beside the cumulative row, and `touches` rides onto every free row --
    # the number the rest of the league actually files on. doc 311: the waiver order is READ from
    # ESPN's mTeam view; the page said "you are near the back of the line" as a
    # hard-coded string and priority resets weekly, so it was wrong most weeks.
    # doc 310: the week sheet is no longer
    # behind --html, whose help text named a DIFFERENT page; it builds by default and
    # --no-sheet opts out. doc 308: wire.py now reads
    # Source\form_2026.csv and tags the week-1 workload screen (2 of 3 = 38%
    # startable against a 13.9% base). Before this NOTHING on either page had seen
    # a snap of 2026 football. doc 307: RE-PINNED twice. the team AND THE BYE come from the
```
