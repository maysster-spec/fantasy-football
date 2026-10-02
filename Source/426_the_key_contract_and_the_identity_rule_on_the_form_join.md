# 426 — the key contract and the identity rule on the form join

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 24 to 25 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 426" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 2117

```
        _free_by[norm_name(_fr.get('name'))] = _fr
    # [doc 426] THE KEY CONTRACT, ASSERTED ONCE, BECAUSE A .get() THAT MISSES IS SILENT.
    # The seat guard below was shipped reading `team`; free rows spell it `tm` (wire.py builds each
    # one as `dict(rate[pid])`), so every lookup returned None, the comparison was never true, and
    # the filter did not fire a single time. It was "verified" against the WIRE CSV, which does
    # spell it `team` -- same logic, different object, which is doc 80 exactly. Nothing about that
    # failure was visible: no error, no empty table, just a rule that quietly was not a rule.
    # Section 3's own words: never gate a mandatory step on a key being present. Assert.
    if freerows:
        _need = ('name', 'pos', 'tm', 'wk', 'bye')
```

### `sheet_engine.py`, line 2194

```
                continue
            # [doc 426] AND THE SAME QUESTION ABOUT THE OTHER MAN: IS THE BACKUP STILL ON THE
            # TEAM? doc 411 checked whether the STARTER had gone and nobody checked whether the
            # SEAT had. Emari Demercado moved to Dallas; inherit_2026.csv still had him behind
            # Kenneth Walker III on Kansas City, so the page printed "Demercado KC bye 5" -- the
            # team and the bye of the man he no longer backs up -- gave him 51% of a 248.9 job he
            # cannot inherit, and promoted the 4.5 that fell out of it to a claim on THE CALL.
            # The live team was in the wire row this loop already holds. A seat is an option on a
            # job; a man on another roster holds no option on it.
            # `freerows` is a COPY OF THE rates() DICT (wire.py: f = dict(rate[pid])), and that
```

### `sheet_engine.py`, line 3438

```
    _season = season_ppg(src) if week else {}
    # [doc 426] SECTION 3's IDENTITY RULE, APPLIED TO THE ONE JOIN THAT SKIPPED IT. form_2026
    # spells him 'Kyle Pitts' and the projection pull spells him 'Kyle Pitts Sr.', so the raw
    # dict lookup below missed and he fell back to a PRESEASON projection with no error and a
    # vintage of 'proj' that looked deliberate. Nine men, all suffix or apostrophe: Pitts
    # printed 7.89 against a correct 5.41 and was the page's top cover for the week-6 TE bye.
    # norm_name has existed for exactly this since doc 58 and this call site never used it.
    _season_n = {norm_name(k): v for k, v in (_season or {}).items()}
    _left = proj_games(week)          # doc 419: proj_2026 is a REST-OF-SEASON total
    if week and _left < PROJ_GAMES:
```
