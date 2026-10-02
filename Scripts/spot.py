r"""spot.py -- THE SPOT-CHECK CARD. One command, one player, every number we hold on him.

    py spot.py "Josh Palmer"
    py spot.py "Mike Washington"            suffixes, periods and case do not matter
    py spot.py "Washington"                 a surname alone lists the men who carry it and stops
    py spot.py "Josh Allen" --team BUF      when two men share a name
    py spot.py --id 4686658                 by ESPN id, no name match at all

WHY THIS EXISTS (claude_todo, doc 433). check_inputs.py answers "is every file we hold read by
something"; it cannot answer "did the page see THIS man's numbers". All six of the 25 Sept defects
were found by a human looking at one player, and there was no command for that. This is it: it
prints every row every Source file holds for one man, says which file and what vintage each number
carries, and closes with the columns that exist for him and are rendered on neither page.

WHAT IT READS, in this order, and a missing file is NAMED, never skipped:
    Source\MY_ROSTER.csv, Source\LEAGUE_ROSTERS.csv, Source\STATUS_LOG.csv     who owns him, slot, status
    the newest Source\WIRE_<date>.csv (and FREE_UNRANKED_<date>.csv)            the wire row, every column
    Source\form_2026.csv                                                       week 0 cumulative, then each week
    Source\depth_daily.csv and Scripts\depth_map.csv                           his slot and the men around him
    Source\practice_2026.csv                                                   the practice report
    Source\inherit_2026.csv                                                    if he holds a job or is next man
    Source\pedigree_2026.csv                                                   draft capital and last season
    the newest Source\espn_projections_2026_<stamp>.csv                        the projection row
    Source\snaps_2026.csv                                                      his snaps by week
    Source\news_2026.csv, Source\redzone_te_2025.csv                           news and last season's red zone

HOW A NAME IS MATCHED. sheet_engine.norm_name() when it is beside this script (case, periods,
apostrophes, hyphens and Jr/Sr/II/III stripped), else the same rule in a local copy. Exact match
first; then a first-name prefix ("Josh" for "Joshua") on the same team and position, which is
LABELLED, because the pages' own join is exact and a row matched only by prefix is a row the page
did not see. Two different men left standing is an error that lists them and stops.

HOW "NOT PRINTED ON ANY PAGE" IS DECIDED. A column counts as reaching a page when its name appears
as a quoted string literal in Scripts\sheet_engine.py or Scripts\wire.py. That is a grep, not a
render check: a name the writer lists in its own fieldnames counts as used, so the closing list is
a FLOOR on what the pages ignore, not the whole of it. It says so on the card.

Standard library only. No network. Writes nothing.
"""
import argparse
import csv
import datetime as dt
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'Source')
sys.path.insert(0, HERE)

try:
    from sheet_engine import norm_name as _norm, team_key as _tk
    NORM_SOURCE = 'sheet_engine.norm_name'
except Exception:                                   # a card must still print without the engine
    _SUFFIX = frozenset({'jr', 'sr', 'ii', 'iii', 'iv', 'v'})

    def _norm(s):
        s = str(s or '').lower().replace('’', "'")
        s = re.sub(r"[.']", '', s).replace('-', ' ')
        return ' '.join(t for t in s.split() if t not in _SUFFIX)

    def _tk(t):
        return str(t or '').strip().upper()
    NORM_SOURCE = 'a local copy of norm_name (sheet_engine.py not importable from here)'


def squash(s):
    """One key for both spellings of a name key: sheet_engine's 'kenneth walker' and build_form's
    'kennethwalker' squash to the same thing."""
    return re.sub(r'[^a-z]', '', _norm(s))


def toks(s):
    return _norm(s).split()


def prefix_match(query, name):
    """'josh palmer' matches 'joshua palmer': same token count, every query token a prefix."""
    q, n = toks(query), toks(name)
    return len(q) == len(n) and all(b.startswith(a) for a, b in zip(q, n))


SLOT = {0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE', 16: 'D/ST', 17: 'K', 20: 'bench', 21: 'IR', 23: 'FLEX'}
# columns that name or date a row rather than measure it; the closing section leaves them out
IDENTITY = {'espn_id', 'player', 'name_key', 'gsis_id', 'pos', 'team', 'tm', 'nfl', 'team_id', 'week',
            'as_of', 'asof', 'captured_at', 'read_at', 'run', 'own_asof', 'reported', 'source', 'slot_id',
            'next_man_id', 'holds_the_job', 'next_man', 'in_progress'}
MISSING = []            # every file that should be there and is not, named at the end too


# ----------------------------------------------------------------------------- files
def rel(p):
    return os.path.relpath(p, ROOT).replace('/', '\\')


def stamp(p):
    return dt.datetime.fromtimestamp(os.path.getmtime(p)).strftime('%Y-%m-%d %H:%M')


def read_csv(p, label=None):
    """Rows of a CSV, or None when the file is absent (and it is recorded as MISSING)."""
    if not os.path.exists(p):
        MISSING.append(rel(p) if not label else f'{label} ({rel(p)})')
        return None
    with open(p, newline='', encoding='utf-8-sig', errors='replace') as fh:
        return [{(k or '').strip(): (v or '').strip() for k, v in r.items()} for r in csv.DictReader(fh)]


def newest(pattern, label):
    """The newest file by the date in its NAME (WIRE_20260929.csv, espn_projections_2026_20260924_0740.csv),
    the same rule sheet_engine and build_inherit use to find the newest wire."""
    hits = sorted(glob.glob(os.path.join(SRC, pattern)))
    if not hits:
        MISSING.append(f'{label} (no Source\\{pattern})')
        return None
    return hits[-1]


# ----------------------------------------------------------------------------- printing
def H(title):
    print(f'\n== {title}')


def where(p, extra=''):
    print(f'   {rel(p)}  (file modified {stamp(p)}{"; " + extra if extra else ""})')


def blank(v):
    return v in (None, '')


def kv(row, cols=None, indent='   '):
    cols = cols or list(row.keys())
    w = max(len(c) for c in cols) if cols else 0
    for c in cols:
        v = row.get(c, '')
        print(f'{indent}{c:<{w}}  {v if not blank(v) else "(blank)"}')


def table(rows, cols, indent='   '):
    if not rows:
        return
    w = {c: max(len(c), *(len(str(r.get(c, ''))) for r in rows)) for c in cols}
    print(indent + '  '.join(f'{c:<{w[c]}}' for c in cols))
    for r in rows:
        print(indent + '  '.join(f'{str(r.get(c, "")):<{w[c]}}' for c in cols))


def note(msg):
    print(f'   NOTE: {msg}')


# ----------------------------------------------------------------------------- identity
class Man:
    def __init__(self):
        self.id = None
        self.names = set()          # every spelling met across the files
        self.pos = None
        self.team = None
        self.seen = []              # (file, spelling) pairs, for the WHO line

    def key(self):
        return self.id or ('name', squash(sorted(self.names)[0]), self.team, self.pos)

    def label(self):
        n = sorted(self.names, key=len)[-1]
        return f'{n} ({self.pos or "?"}, {self.team or "?"}, espn_id {self.id or "none"})'


def universe():
    """Every (name, pos, team, espn_id) any file carries, from the files that carry an id or a
    team, so a query can be resolved before any row is printed."""
    people = []

    def add(file, name, pos, team, pid):
        if name:
            people.append((file, name.strip(), (pos or '').strip().upper(), _tk(team),
                           (str(pid).strip() if not blank(pid) else None)))

    for fn, cols in (('MY_ROSTER.csv', ('player', 'pos', 'team', 'espn_id')),
                     ('LEAGUE_ROSTERS.csv', ('player', 'pos', 'nfl', 'espn_id')),
                     ('depth_daily.csv', ('player', 'pos', 'team', 'espn_id')),
                     ('pedigree_2026.csv', ('player', 'pos', None, 'espn_id')),
                     ('news_2026.csv', ('player', 'pos', 'team', 'espn_id')),
                     ('form_2026.csv', ('player', 'pos', 'team', None)),
                     ('snaps_2026.csv', ('player', 'pos', 'team', None)),
                     ('practice_2026.csv', ('player', 'pos', 'team', None))):
        p = os.path.join(SRC, fn)
        if os.path.exists(p):
            for r in read_csv(p):
                add(fn, r.get(cols[0]), r.get(cols[1]), r.get(cols[2]) if cols[2] else '',
                    r.get(cols[3]) if cols[3] else None)
    for pat, cols in (('WIRE_*.csv', ('player', 'pos', 'team', 'espn_id')),
                      ('FREE_UNRANKED_*.csv', ('player', 'pos', 'team', 'espn_id')),
                      ('espn_projections_2026_*.csv', ('Player', 'pos', 'team', 'espn_id'))):
        hits = sorted(glob.glob(os.path.join(SRC, pat)))
        if hits:
            for r in read_csv(hits[-1]):
                add(os.path.basename(hits[-1]), r.get(cols[0]), r.get(cols[1]), r.get(cols[2]), r.get(cols[3]))
    dm = os.path.join(HERE, 'depth_map.csv')
    if os.path.exists(dm):
        for r in read_csv(dm):
            add('depth_map.csv', r.get('player'), r.get('pos'), r.get('tm'), r.get('espn_id'))
    inh = os.path.join(SRC, 'inherit_2026.csv')
    if os.path.exists(inh):
        for r in read_csv(inh):
            add('inherit_2026.csv', r.get('next_man'), 'RB', r.get('team'), r.get('next_man_id'))
            add('inherit_2026.csv', r.get('holds_the_job'), 'RB', r.get('team'), None)
    return people


def resolve(query, pid, team, pos):
    """The one man the query names, or a list of candidates and None."""
    people = universe()
    if pid:
        hits = [p for p in people if p[4] == str(pid)]
        how = f'espn_id {pid}'
    else:
        exact = [p for p in people if squash(p[1]) == squash(query)]
        # the prefix hits ride along even when an exact hit exists, because the same man is
        # "Josh Palmer" in the nflverse files and "Joshua Palmer" in ESPN's; the grouping below
        # only merges them when team and position agree, and anything else lists as a second man
        pref = [p for p in people if p not in exact and prefix_match(query, p[1])]
        hits = exact + pref
        how = 'exact name' if exact else f'first-name prefix ("{query}" is not spelled that way in any file)'
        if exact and pref:
            how += ' plus a first-name prefix on the same team and position'
        if not hits:
            last = toks(query)[-1] if toks(query) else ''
            hits = [p for p in people if toks(p[1]) and toks(p[1])[-1] == last]
            how = 'surname only'
    if team:
        hits = [p for p in hits if p[3] == _tk(team)]
    if pos:
        hits = [p for p in hits if p[2] == pos.upper()]
    # group the hits into men: by id when there is one, else by (squashed name, team, pos), and
    # an id-less hit joins an id-bearing man on the same squashed-or-prefix name, team and position
    men = {}
    for file, name, ps, tm, i in sorted(hits, key=lambda h: (h[4] is None, h[0])):
        m = None
        if i:
            m = men.get(i)
        else:
            for cand in men.values():
                same = any(squash(n) == squash(name) or prefix_match(name, n) or prefix_match(n, name)
                           for n in cand.names)
                if same and (not tm or not cand.team or tm == cand.team) and (not ps or not cand.pos or ps == cand.pos):
                    m = cand
                    break
        if m is None:
            m = Man()
            m.id = i
            men[i or ('name', squash(name), tm, ps)] = m
        m.names.add(name)
        m.pos = m.pos or ps
        m.team = m.team or tm
        m.seen.append((file, name))
    return list(men.values()), how


# ----------------------------------------------------------------------------- lookups
def by_id_or_name(rows, man, idcol, namecol, teamcol=None, poscol=None):
    """Rows for this man. By id when both sides carry one; else exact squashed name (plus team when
    the file carries one); else first-name prefix on the same team and position, which is reported
    as such because the pages' own join would NOT have found it. Returns (rows, how)."""
    if rows is None:
        return [], 'file missing'
    if idcol and man.id:
        got = [r for r in rows if r.get(idcol, '') == man.id]
        if got:
            return got, 'espn_id'
    keys = {squash(n) for n in man.names}
    got = [r for r in rows if squash(r.get(namecol, '')) in keys
           and (not teamcol or not man.team or blank(r.get(teamcol)) or _tk(r.get(teamcol)) == man.team)]
    if got:
        return got, 'exact name' + (' + team' if teamcol else '')
    got = [r for r in rows if any(prefix_match(r.get(namecol, ''), n) or prefix_match(n, r.get(namecol, ''))
                                  for n in man.names)
           and (not teamcol or not man.team or _tk(r.get(teamcol)) == man.team)
           and (not poscol or not man.pos or (r.get(poscol) or '').upper() == man.pos)]
    if got:
        return got, ('FIRST-NAME PREFIX ONLY, spelled "%s" in this file: the page joins on the exact '
                     'name, so it did NOT see these rows' % got[0].get(namecol, ''))
    return [], 'no row'


def held(section, cols, row_or_rows, register):
    """Record the non-blank columns this man has in a file, for the closing section."""
    rows = row_or_rows if isinstance(row_or_rows, list) else [row_or_rows]
    have = [c for c in cols if any(not blank(r.get(c)) for r in rows)]
    if have:
        register.setdefault(section, set()).update(have)


# ----------------------------------------------------------------------------- the card
def card(man, how):
    reg = {}    # file -> columns held for him
    print(f'SPOT CARD  {man.label()}')
    print(f'   matched by {how}; name rule: {NORM_SOURCE}')
    print('   spellings met: ' + '; '.join(f'"{n}" in {f}' for f, n in sorted(set(man.seen))))

    # 1. roster and status --------------------------------------------------------------
    H('ROSTER AND STATUS')
    p = os.path.join(SRC, 'MY_ROSTER.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'team')
        where(p, f'asof column {rows[0].get("asof", "?") if rows else "?"}')
        if got:
            r = got[0]
            try:
                slot = SLOT.get(int(r.get('slot_id')), r.get('slot_id'))
            except (TypeError, ValueError):
                slot = r.get('slot_id')
            print(f'   ON YOUR ROSTER: slot {r.get("slot_id")} ({slot}), status {r.get("status")}, '
                  f'value {r.get("value") or "(blank)"}, bye {r.get("bye") or "(blank)"}   [matched by {h}]')
            kv(r)
            held('MY_ROSTER.csv', list(r.keys()), r, reg)
        else:
            print('   not on your roster')
    p = os.path.join(SRC, 'LEAGUE_ROSTERS.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'nfl')
        where(p)
        if got:
            r = got[0]
            print(f'   OWNED by team {r.get("team")} (team_id {r.get("team_id")}), status {r.get("status")}   [matched by {h}]')
            kv(r)
            held('LEAGUE_ROSTERS.csv', list(r.keys()), r, reg)
        else:
            print('   on no roster in the league: a free agent (or on waivers)')
    p = os.path.join(SRC, 'STATUS_LOG.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player')
        where(p, f'{len(rows)} rows, newest read_at {rows[-1].get("read_at") if rows else "?"}')
        if got:
            print(f'   {len(got)} reads of his slot and status; the last five   [matched by {h}]')
            table(got[-5:], ['read_at', 'run', 'slot_id', 'status'])
            held('STATUS_LOG.csv', list(got[0].keys()), got, reg)
        else:
            print('   never on your roster during a logged read')

    # 2. the wire row ---------------------------------------------------------------------
    H('THE WIRE ROW (every column)')
    p = newest('WIRE_*.csv', 'the wire')
    wire_row = None
    if p:
        rows = read_csv(p)
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'team')
        m = re.search(r'(\d{8})', os.path.basename(p))
        where(p, f'date in the name {m.group(1) if m else "?"}; own_asof column is ESPN\'s read time')
        if got:
            wire_row = got[0]
            print(f'   [matched by {h}]')
            kv(wire_row)
            held(os.path.basename(p), list(wire_row.keys()), wire_row, reg)
        else:
            print('   not on the wire (rostered, or the board never priced him)')
    p = newest('FREE_UNRANKED_*.csv', 'the unranked free list')
    if p:
        rows = read_csv(p)
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'team')
        where(p)
        if got:
            print(f'   FREE AND OFF THE BOARD   [matched by {h}]')
            kv(got[0])
            held(os.path.basename(p), list(got[0].keys()), got[0], reg)
        else:
            print('   not on it')

    # 3. form -----------------------------------------------------------------------------
    H('FORM (form_2026.csv: week 0 is the season to date, then each week)')
    p = os.path.join(SRC, 'form_2026.csv')
    rows = read_csv(p)
    form_rows = []
    if rows is not None:
        got, h = by_id_or_name(rows, man, None, 'player', 'team', 'pos')
        wk = [int(r['week']) for r in rows if (r.get('week') or '').isdigit()]
        where(p, f'data through week {max(wk) if wk else "?"}')
        if got:
            form_rows = sorted(got, key=lambda r: int(r.get('week') or 0))
            print(f'   [matched by {h}]')
            cols = [c for c in form_rows[0].keys() if c not in ('name_key', 'player', 'pos', 'team')]
            table(form_rows, cols)
            if any((r.get('in_progress') or '') == '1' for r in form_rows):
                note('a row carries in_progress 1: that game had not finished when the file was built')
            held('form_2026.csv', list(form_rows[0].keys()), form_rows, reg)
            # THE JOIN MISS. wire.py carries the form onto the wire row by norm_name(player), so a man
            # spelled one way by ESPN and another by nflverse has a form row here and blank workload
            # columns there. That is a number we hold that the page did not use, which is the whole
            # point of this card, so it is called out, not left for the reader to notice.
            if wire_row is not None and all(blank(wire_row.get(c)) for c in ('snap_pct', 'tgt_share', 'xfp', 'wopr')):
                sp_w, sp_f = wire_row.get('player', ''), form_rows[0].get('player', '')
                why = (f'the wire spells him "{sp_w}" and this file "{sp_f}", and the join is on the exact name'
                       if squash(sp_w) != squash(sp_f) else 'the spellings agree, so look at the join key (name, pos, team)')
                note(f'THE WIRE ROW ABOVE HAS BLANK WORKLOAD COLUMNS WHILE THIS FILE HOLDS {len(form_rows)} ROWS '
                     f'FOR HIM: the page\'s form join missed him ({why}). The screen never saw these numbers.')
        else:
            print('   no rows (he has not played a snap this season, or the file spells him another way)')

    # 4. depth chart ----------------------------------------------------------------------
    H('DEPTH CHART')
    p = os.path.join(SRC, 'depth_daily.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'team', 'pos')
        where(p, f'as_of column {rows[0].get("as_of") if rows else "?"}')
        if got:
            r = got[0]
            print(f'   {r.get("team")} {r.get("pos")} depth {r.get("depth")}   [matched by {h}]')
            around = sorted((x for x in rows if x.get('team') == r.get('team') and x.get('pos') == r.get('pos')),
                            key=lambda x: int(x.get('depth') or 99))
            for x in around:
                mark = '  <-- him' if x is r else ''
                print(f'      {x.get("depth")}. {x.get("player")}{mark}')
            held('depth_daily.csv', list(r.keys()), r, reg)
        else:
            print('   not on the daily chart')
    p = os.path.join(HERE, 'depth_map.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'tm', 'pos')
        where(p, 'the frozen preseason job map, built before week 1')
        if got:
            print(f'   [matched by {h}]')
            kv(got[0])
            held('depth_map.csv', list(got[0].keys()), got[0], reg)
        else:
            print('   no row')

    # 5. practice -------------------------------------------------------------------------
    H('PRACTICE REPORT')
    p = os.path.join(SRC, 'practice_2026.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, None, 'player', 'team')
        wk = [int(r['week']) for r in rows if (r.get('week') or '').isdigit()]
        where(p, f'week {max(wk) if wk else "?"}; days_old is the report\'s age at build')
        if got:
            print(f'   [matched by {h}]')
            table(got, ['week', 'pos', 'report_status', 'practice_status', 'practice_injury', 'days_old'])
            if any((r.get('pos') or '').upper() != (man.pos or '') for r in got):
                note('a row carries a different position: check it is the same man')
            held('practice_2026.csv', list(got[0].keys()), got, reg)
        else:
            print('   not on the report (no injury listed)')

    # 6. inherit --------------------------------------------------------------------------
    H('THE SEAT (inherit_2026.csv)')
    p = os.path.join(SRC, 'inherit_2026.csv')
    rows = read_csv(p)
    if rows is not None:
        where(p)
        keys = {squash(n) for n in man.names}
        nxt = [r for r in rows if (man.id and r.get('next_man_id') == man.id) or squash(r.get('next_man')) in keys]
        hold = [r for r in rows if squash(r.get('holds_the_job')) in keys]
        for r in nxt:
            print(f'   NEXT MAN behind {r.get("holds_the_job")} ({r.get("team")})')
            kv(r)
            held('inherit_2026.csv', list(r.keys()), r, reg)
        for r in hold:
            print(f'   HOLDS THE JOB at {r.get("team")}; next man {r.get("next_man")}')
            kv(r)
            held('inherit_2026.csv', list(r.keys()), r, reg)
        if not nxt and not hold:
            print('   not a job holder or a next man on the file')

    # 7. pedigree -------------------------------------------------------------------------
    H('PEDIGREE (draft capital and last season)')
    p = os.path.join(SRC, 'pedigree_2026.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', None, 'pos')
        where(p, 'g25/tgt25/ypt25/tpg25/ppg25 are 2025 season totals and rates')
        if got:
            print(f'   [matched by {h}]')
            kv(got[0])
            held('pedigree_2026.csv', list(got[0].keys()), got[0], reg)
        else:
            print('   no row')

    # 8. projection -----------------------------------------------------------------------
    H('PROJECTION (newest ESPN pull)')
    p = newest('espn_projections_2026_*.csv', 'the ESPN projection pull')
    if p:
        rows = read_csv(p)
        got, h = by_id_or_name(rows, man, 'espn_id', 'Player', 'team')
        where(p, f'captured_at column {rows[0].get("captured_at") if rows else "?"}; proj_2026 is the REST of the season from that date, actual_2026 the season to date')
        if got:
            r = got[0]
            print(f'   [matched by {h}]')
            kv(r, [c for c in r.keys() if c not in ('raw_stats', 'raw_actual_stats')])
            for c in ('raw_stats', 'raw_actual_stats'):
                if c in r:
                    v = r[c]
                    print(f'   {c}: {v[:400] + " ..." if len(v) > 400 else v}')
            held(os.path.basename(p), list(r.keys()), r, reg)
        else:
            print('   no row: ESPN did not project him in this pull (the pull is the most-owned 700)')

    # 9. snaps ----------------------------------------------------------------------------
    H('SNAPS BY WEEK (snaps_2026.csv)')
    p = os.path.join(SRC, 'snaps_2026.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, None, 'player', 'team', 'pos')
        wk = [int(r['week']) for r in rows if (r.get('week') or '').isdigit()]
        where(p, f'data through week {max(wk) if wk else "?"}')
        if got:
            print(f'   [matched by {h}]')
            table(sorted(got, key=lambda r: int(r.get('week') or 0)), ['week', 'snaps', 'team_plays', 'snap_pct'])
            held('snaps_2026.csv', list(got[0].keys()), got, reg)
        else:
            print('   no rows')

    # 10. news and red zone ---------------------------------------------------------------
    H('NEWS (news_2026.csv)')
    p = os.path.join(SRC, 'news_2026.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player', 'team')
        where(p)
        if got:
            print(f'   [matched by {h}]')
            for r in got:
                kv(r)
            held('news_2026.csv', list(got[0].keys()), got, reg)
        else:
            print('   no item')
    H('RED ZONE LAST SEASON (redzone_te_2025.csv: tight ends only; display only, it moves nothing)')
    p = os.path.join(SRC, 'redzone_te_2025.csv')
    rows = read_csv(p)
    if rows is not None:
        got, h = by_id_or_name(rows, man, 'espn_id', 'player')
        where(p, '2025 season')
        if got:
            print(f'   [matched by {h}]')
            kv(got[0])
            held('redzone_te_2025.csv', list(got[0].keys()), got[0], reg)
        else:
            print('   no row' + ('' if man.pos == 'TE' else ' (not a tight end)'))

    # 11. held but not printed ------------------------------------------------------------
    H('HELD BUT NOT PRINTED ON ANY PAGE')
    pages = {}
    for fn in ('sheet_engine.py', 'wire.py'):
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            pages[fn] = open(p, encoding='utf-8', errors='replace').read()
        else:
            MISSING.append(f'Scripts\\{fn} (needed to decide what the pages print)')
    if not pages:
        print('   CANNOT DECIDE: neither sheet_engine.py nor wire.py is beside this script')
    else:
        print('   decided by grepping ' + ' and '.join(f'Scripts\\{f}' for f in pages)
              + ' for the column name as a quoted string literal.')
        print('   A name the writer uses in its own fieldnames counts as used, so this is a floor on what the')
        print('   pages ignore, not the whole of it. Identity and stamp columns (ids, names, team, week, dates)')
        print('   are not numbers and are left out.')
        blob = '\n'.join(pages.values())
        any_out = False
        for section, cols in reg.items():
            un = sorted(c for c in cols if c.lower() not in IDENTITY
                        and not re.search(r"['\"]" + re.escape(c) + r"['\"]", blob))
            if un:
                any_out = True
                print(f'   {section:<40} {", ".join(un)}')
        if not any_out:
            print('   nothing: every number he has a value in is named somewhere in the two page scripts')

    if MISSING:
        H('FILES THAT SHOULD BE THERE AND ARE NOT')
        for m in MISSING:
            print(f'   MISSING: {m}')


def main(argv=None):
    ap = argparse.ArgumentParser(description='every number we hold on one player, by file and vintage')
    ap.add_argument('name', nargs='?', help='the player, any spelling; suffixes and periods do not matter')
    ap.add_argument('--id', help='ESPN id instead of a name')
    ap.add_argument('--team', help='NFL team code, to split two men with one name')
    ap.add_argument('--pos', help='position, to split two men with one name')
    a = ap.parse_args(argv)
    if not a.name and not a.id:
        ap.error('give a name or --id')
    men, how = resolve(a.name or '', a.id, a.team, a.pos)
    if not men:
        print(f'NO MATCH for "{a.name or a.id}" in any Source file (tried exact, first-name prefix, surname).')
        if MISSING:
            print('files not found while looking: ' + '; '.join(MISSING))
        return 2
    if len(men) > 1:
        print(f'AMBIGUOUS: "{a.name or a.id}" matches {len(men)} men (by {how}). Say which with --team or --pos or --id:')
        for m in sorted(men, key=lambda m: m.label()):
            print(f'   {m.label()}')
        return 2
    card(men[0], how)
    return 0


if __name__ == '__main__':
    sys.exit(main())
