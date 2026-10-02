# 316 — the masthead name the other rosters and the five row cap

*Written 28 Sept 2026 by doc 435's audit. The work this number stands for was done about 16 Sept 2026.*

> **NO DOCUMENT WAS WRITTEN UNDER THIS NUMBER.** The session that did the work cited "doc 316" in the
> files below and never wrote the doc. This file exists so that the citation resolves and
> `check_citations.py` can see it; **it makes no claim of its own.** Everything below is quoted
> verbatim from the citing files, which are the only record. If a number in a quote below has since
> been retracted, the retraction lives in the directive's DO-NOT-QUOTE table and the findings file,
> not here.

## What the citing files say

### `sheet_engine.py`, line 2892

```
        # a ranking he has to adjudicate, which is the work he pays this page to do.
        # AND THE CAP MUST NOT EAT THE ROW THE PAGE ITSELF SAYS TO CLAIM FIRST (doc 316,
        # RESTORED 18 Sept -- doc 345). Matt, 16 Sept: "Black is no longer on the priority
        # pickups." He was right and the tag fix of the night before did not reach him: Kaelon
        # Black carried 15 carries and targets, the only 56%-contested row on the wire, and he
        # sat BELOW the cut on worth, so `now[:5]` cut him before his own warning could be read.
        # A cap that hides the row the page is shouting about is 0.5(c)5's missing-row defect
        # with a deliberate-looking cause. So: keep five, then re-admit any row below the cut
        # whose contest band says to claim him first. This changes WHAT IS SHOWN, never the
        # ORDER -- 4.32's terms stay as they are, and docs 255-257 are the record of why I do
```

### `wire.py`, line 1411

```
            _abbrev_by_id[t.get('id')] = str(nm).strip()
            # THE MASTHEAD NAME LIVES IN THIS VIEW, NOT IN mRoster (doc 316). The code below
            # reads it off mRoster and a comment there claims the page follows his ESPN team
            # name -- it does not, because ESPN serves teams WITHOUT name/location/nickname in
            # the roster view, so the lookup silently returned '' and the header fell back to
            # "Your team" for a week. Same defect shape as 3's silent-skip rule: a missing field
            # that reads as a legitimate blank. FULL name here, not the abbreviation.
            if t.get('id') == MY_TEAM_ID:
                _full = (t.get('name')
                         or ' '.join(x for x in (t.get('location'), t.get('nickname')) if x)
```

### `wire.py`, line 1457

```
                # ESPN serves it here, so renaming the team renames the page on the next run.
                # mRoster does NOT carry the team name (doc 316) -- this line returned ''
                # every run. mTeam does, and it is read above; this stays only as a fallback.
                my_team_name = (t.get('name') or ' '.join(
                    x for x in (t.get('location'), t.get('nickname')) if x) or '').strip()
                for e in (t.get('roster') or {}).get('entries', []):
                    p = e.get('playerPoolEntry', {}).get('player', {}) or {}
                    mine[str(p.get('id'))] = p.get('fullName', '?')
                    mine_meta[str(p.get('id'))] = (POS.get(p.get('defaultPositionId'), '?'),
                                                   PRO.get(p.get('proTeamId'), '?'))
```

### `wire.py`, line 1471

```

    # ---- FIX 3 (doc 316): the other eleven rosters are FETCHED EVERY RUN AND THROWN AWAY.
    # Matt asked "does anyone else appear to need a TE?" and the only answer available was a
    # bye-week table, because `rosters` above holds all twelve teams and the loop keeps one.
    # 254 called the rival rosters the blocker on a whole lane; they were never blocked, they
    # were discarded. Written out so the question is a lookup from the next run on.
    # NOTE (doc 314) what this does NOT license: positional need does not predict who files on
    # a man. This is for reading the room, not for ordering a claim list.
    try:
        _lr = []
```

### `check_kit.py`, line 109

```
    # never written.
    # doc 316: the masthead name is read
    # from mTeam (mRoster never carried it) and the other eleven rosters are written out
    # instead of discarded. doc 314: load_form() now returns the
    # LAST COMPLETED GAME beside the cumulative row, and `touches` rides onto every free row --
    # the number the rest of the league actually files on. doc 311: the waiver order is READ from
    # ESPN's mTeam view; the page said "you are near the back of the line" as a
    # hard-coded string and priority resets weekly, so it was wrong most weeks.
    # doc 310: the week sheet is no longer
    # behind --html, whose help text named a DIFFERENT page; it builds by default and
```

### `check_kit.py`, line 165

```
    # carrying a multi-week designation, NAMED under the table. C24 covers all of it.
    # doc 345: doc 316's cap
    # exception is back -- the five-row cap on Priority pickups no longer eats a row whose
    # own contest band says to claim him first. It went missing in the 16 Sept 08:05 file
    # and nothing noticed for two days, because nothing pinned it and no control covered
    # it. C23 covers it now and was shown FAILING on the pre-restore code first.
    # doc 343: every seat now carries
    # its OWN odds of the job opening, from that back's share of his backfield in week one
    # -- 0.48 / 0.44 / 0.53 / 0.64 on 126 team-seasons -- so the seat table is ordered by
    # what it is worth rather than by the size of the job, which is all it could do while
```

### `check_kit.py`, line 183

```
    # cost is printed, net of the best free body at his position, so the page stops hiding
    # fourteen of the fifteen numbers it already computes. doc 316: the five-row cap no
    # longer hides a row the page itself flags 'put him first', and a played week is faded.
    # doc 314: the seat lane now
    # joins its own touch count off the free pool, so the man with the biggest workload stops
    # being the one row that says nothing. contest() prints how
    # many rivals file on a man and tells him to claim the contested one FIRST. doc 308: the workload bet lane,
    # the five-row cap, and the screened rows' magnitude is a TOTAL over the hold and
    # no longer says 'a week' (it was overstating by 6.4x). doc 307: the starter's status renders
    # beside the STARTER. doc 305: only a MULTI-WEEK designation is
```
