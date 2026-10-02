# 424 — one predicate both sides

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 24 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 424" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 45

```

    [doc 424] ONE PREDICATE, BOTH SIDES. Doc 422 introduced WEEKLY_VALUE and applied it only to the
    replacement lookup, so the drop table was protected and the ADD table was not -- and the page
    offered a defense at a net of MINUS 4.3 that same night. Every consumer of this property calls
    this function, so a position cannot be weekly for one table and seasonal for the other.
    """
    return pos not in WEEKLY_VALUE
FLEXABLE = ('RB', 'WR', 'TE')
WEEKS = list(range(1, 15))
SEASON_WEEKS = list(range(1, 15))     # the fourteen scoring weeks, fixed
```

### `sheet_engine.py`, line 2940

```
        # rows is worse than four scattered tables, because it looks decided (0.1(f2)).
        # [doc 424] AND THE SAME PROPERTY MUST GOVERN THE ADD SIDE. Doc 422 put WEEKLY_VALUE on
        # the DROP lookup and stopped there, so the page could still OFFER a defense on a season
        # rate -- and it did, the same night: "take Jets D/ST +1.5, drop Tre Tucker 5.8, net -4.3".
        # Matt: "it still has me picking up Jets D/ST and that doesn't compute." He is right twice
        # over, and his own line about this is the lesson: "the guard has to be designed correctly
        # because those have been faulty too."
        # A HALF-APPLIED PROPERTY IS WORSE THAN NO PROPERTY, because the half that is covered makes
        # the whole thing look handled. One predicate, used by both sides, so they cannot diverge.
        _seen_pos, _picked = set(), []
```

### `sheet_engine.py`, line 3014

```
                         + '</span>')
            # [doc 424] A ROW THAT LOSES POINTS IS NOT A RECOMMENDATION. The Jets row printed
            # "+1.5 worth, 5.8 to drop, net -4.3" under the heading WHAT TO DO. The caption has
            # always said to read down until the net stops being positive, which puts the work on
            # the reader and assumes he is reading a list rather than being told. He was right to
            # call it: "that doesn't compute". The table stops at the last row that GAINS, and
            # says how many were held back rather than silently truncating (0.5(c)5).
            if _net <= 0.05:
                _skipped += 1
                continue
```

### `check_kit.py`, line 142

```
    # FAILED on the rename before the marker moved, which is the anchor working.
    'sheet_engine.py': (205458, 'f951ff9140158127'),   # 24 Sept RE-PINNED, doc 424: season_priced() is ONE predicate used by the add side and the drop side, because doc 422 applied WEEKLY_VALUE to the drop lookup only and the page then offered Jets D/ST at a net of MINUS 4.3. And THE CALL now stops at the last row that gains, saying how many it held back. Both controls run. History in _archive and AUDIT_LEDGER.
                                                       # for five pages, section anchors. Doc 372   # 18 Sept 13:50 RE-PINNED: TODO_CMDS
    # gained `done "<some words>"`, so it shows on the to-do page AND on COMMANDS.html from the
    # one list. Before that, 18 Sept 13:15 RE-PINNED: THE SEAT
    # FILTER RAN ON THE WRONG POPULATION. Its availability/rostered test sat inside
    # `if not yours`, so any row whose man ahead is on Matt's own roster skipped it -- Dylan
    # Sampson led the list on INJURY RESERVE for a day because he is behind Judkins. The test
    # now runs on every row; `yours` only picks the alternative bar. Doc 354. Before that,
    # 18 Sept 13:00 RE-PINNED: the masthead
```
