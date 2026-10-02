# 430 — claude todo and the online copy built every run

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 25 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 430" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 1129

```
    (CLOCK_URL, 'roster clock'),
    # [doc 430] AND THE OTHER TWO PUBLISHED PAGES, because this bar is the only hub that can point
    # BOTH ways. A browser refuses a file:// link from an https page, so nothing on the web can
    # link back to this PC. The local bar therefore carries everything; the online bar carries
    # only the online set and names the folder in text.
    (POCKET_URL, 'pocket sheet'),
    (TAKES_URL, 'the takes'),
]


```

### `make_online.py`, line 3

```

[doc 430] WHY THIS EXISTS. The published page sat six days stale while every local page was current,
because publishing was a HAND edit somebody did once in a chat and nobody could repeat. ff.bat
cannot publish: it writes files to this PC, and nothing on this PC can push to claude.ai. So the
split is fixed and this script owns the half that can be automated -- producing a publish-ready
file every time the sheet is built, so the only manual step left is the upload itself.

Run by ff.bat. Writes Source\\ONLINE_WEEK_SHEET.html. No network, no ESPN.

THE TRANSFORM, and each line of it is a thing the web copy must do differently:
```

### `ff.bat`, line 76

```
echo --- the copy for the web --- >> "%LOG%"
REM [doc 430] ff.bat CANNOT PUBLISH. Nothing on this PC can push to claude.ai, so the online
REM week sheet was six days stale while every local page was current. This step builds the
REM publish-ready file every run; the upload is the one manual half and Claude does it.
py make_online.py >> "%LOG%" 2>&1
set RC8=%ERRORLEVEL%
if not "%RC8%"=="0" echo *** ONLINE COPY NOT BUILT -- the published page cannot be refreshed >> "%LOG%"

echo. >> "%LOG%"
echo --- the commands page --- >> "%LOG%"
```

### `research\open_threads.py`, line 133

```

    [doc 430] AND THE SAME HOLE EXISTED ON MY SIDE, one level further in. 0.5(e) gave Matt's
    reply-items a home and left MINE with none: a thing I said in a reply that I would do myself
    went into no doc, so the scan above could not see it and no list held it. That is exactly the
    defect 0.5(e) was written to fix, reappearing in the mirror. Measured cost: I told Matt the
    online sheet would refresh every run, did not wire it, and it sat six days until he found it.
    Matt, 25 Sept: "if you do need to wait for me then shouldn't that go on my todo list so
    neither of us drop it?" Both sides now have a file and both render at the top.
    """
    p = os.path.join(src, name)
```

### `claude_todo.txt`, line 4

```
#
# WHY THIS FILE EXISTS (doc 430). Section 0.5(e) sent anything I am waiting on Matt for to
# matt_todo.txt the moment I say it, and left the mirror image with no home: a thing I said I
# would do MYSELF, in a reply, went into no doc, so open_threads.py could not see it and nothing
# held it. It cost six days of a stale published page. Matt found it, not a guard.
#
# THE RULE: if I say I will do something and the turn ends without it done, it goes here BEFORE
# the reply is sent. Not the ledger, not a doc, not a promise in prose.

## OPEN
```

## Where the story is

The full v9.31 entry for this number is in `Source\DIRECTIVE_CHANGELOG.md` under v9.31 (25 Sept), and
the rule it created is §0.5(e) of `00_PROJECT_DIRECTIVE.md`: a thing I say in a reply that I will do
myself goes in `Source\claude_todo.txt` before the reply is sent.
