# 414 — a row with nothing in it is not news

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done 24 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 414" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 734

```
        return ''
    # [doc 414] Belt and braces with build_news.py's own filter: an Active man with no injury
    # is not news, and the page said "Active" in red beside three healthy men before this existed.
    _st, _inj = (r.get('status') or '').strip(), (r.get('injury') or '').strip()
    if _st.lower() in ('active', '') and not _inj and not r.get('return_date'):
        return ''
    bits = [b for b in (_st, _inj) if b]
    _d = (r.get('detail') or '').strip()
    if _d and _d.lower() not in ('not specified', 'unspecified'):
        bits.append(_d.lower())
```

### `check_kit.py`, line 341

```
    'ff.bat': (7756, 'c2212c867ae10e6a'),   # 24 Sept RE-PINNED, doc 422: runs check_sources.py before the vintage check. A guard that is not in this file does not run, and the whole point of that one is that it fires without anyone remembering it. History in _archive and AUDIT_LEDGER.
    'build_news.py': (10029, 'c33b4e434842a785'),   # 24 Sept RE-PINNED, doc 414: an informationless row is filtered at source; 585 of the first 800 were status Active with nothing else. History in _archive and AUDIT_LEDGER.
                                     # step 6 check_vintage.py, then step 7 check_pages.py.
                                     # Doc 374, doc 376
    # doc 374: NEW AND PINNED FROM BIRTH. It fails the run when a page prints a rate this
    # season already refutes, which is the defect that produced four wrong recommendations in
    # twenty-four hours. A guard nothing pins can revert silently (doc 345), and this one is
    # the last thing that should.
    # doc 422: NEW AND PINNED FROM BIRTH. Every error on 24 Sept passed every internal-consistency
    # check because every file agreed; this one tests what an OUTSIDE field MEANS. Its seven
```

### `build_news.py`, line 113

```
            team = (((ath.get('team') or {}).get('abbreviation')) or tm_abbr or '')
            # [doc 414] A ROW WITH NOTHING IN IT IS NOT NEWS. ESPN's feed lists the whole injury
            # REPORT, cleared men included: on the first good run, 585 of 800 rows were status
            # "Active" with no injury, no detail and no return date. Unfiltered, the week sheet
            # printed the word "Active" in red beside Vele, Washington and Pineiro as though it
            # were a diagnosis. An Active man WITH an injury is kept -- he is playing through
            # something and that is worth knowing.
            _status = (e.get('status') or '').strip()
            _has = bool((det.get('type') or '').strip() or (det.get('returnDate') or '').strip())
            if _status.lower() in ('active', '') and not _has:
```
