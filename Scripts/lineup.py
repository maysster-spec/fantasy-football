#!/usr/bin/env python3
r"""
lineup.py -- IS ANYONE IN MY STARTING LINEUP NOT GOING TO PLAY?

    py lineup.py               # check now, print the answer
    py lineup.py --html        # ALSO write the page the scheduler leaves for you
    py lineup.py --check       # just prove the cookies work, pull nothing

WHY THIS EXISTS
    The wire sheet is the Tuesday job. This is the OTHER window: Thursday before the night game
    and Sunday once the inactives are out. It answers one question -- is there a man in my
    starting nine who is not going to be on the field -- and it is the cheapest points in fantasy,
    because a starter left in while he is OUT scores zero and the bench player who would have
    covered him is sitting right there.

WHAT IT FLAGS
    a starter ESPN lists OUT / DOUBTFUL / IR / SUSPENDED   -- red
    a starter whose team is on BYE this week               -- red
    an empty starting slot                                 -- red
    a starter listed QUESTIONABLE                          -- amber, decide it yourself
    and for every red, the healthy bench men at that position

IF IT 401s: your cookies expired. Run `py set_cookies.py` and try again.
"""
import argparse, csv, datetime as dt, json, os, sys

try:
    import requests
except ImportError:
    sys.exit("lineup.py needs `requests`, the same one live_draft.py uses.")

# THE NAV LIVES IN ONE PLACE (doc 372). This page had no way back to the week sheet at all, which
# is what Matt hit on 19 September: "Again, it has no link back to the home page."
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from sheet_engine import page_bar, PAGEBAR_CSS
except ImportError as _exc:
    sys.exit("lineup.py needs sheet_engine.py beside it for the page nav (%s). "
             "Run  py check_kit.py  to see which file is missing." % _exc)
# doc 380: the read-time stamp and the on-open age line, guarded so an older sheet_engine.py
# costs this page its stamp and nothing else.
try:
    from sheet_engine import build_meta as _build_meta, age_line as _age_line
except ImportError:
    _build_meta = _age_line = None

LEAGUE_ID  = 21985
SEASON     = 2026
MY_TEAM_ID = 9                     # JUG
READS = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{lid}"
COOKIES = {
    'swid':    '{A7217088-1F36-4F1F-AE73-67262BF763EF}',
    'espn_s2': '',
}
HEADERS = {'accept': 'application/json', 'x-fantasy-platform': 'espn-fantasy-web',
           'x-fantasy-source': 'kona', 'referer': 'https://fantasy.espn.com/'}

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BYES = os.path.join(SRC, 'byes_2026.csv')
WATCH = os.path.join(SRC, 'watch_list.csv')

# ESPN lineup slots. Anything NOT in these two is a starting slot.
BENCH_SLOTS = {20, 21}          # 20 bench, 21 IR
SLOT_NAME = {0: 'QB', 2: 'RB', 4: 'WR', 6: 'TE', 16: 'D/ST', 17: 'K', 23: 'FLEX',
             20: 'bench', 21: 'IR'}
POS = {1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE', 5: 'K', 16: 'D/ST'}
PRO = {1:'ATL',2:'BUF',3:'CHI',4:'CIN',5:'CLE',6:'DAL',7:'DEN',8:'DET',9:'GB',10:'TEN',
       11:'IND',12:'KC',13:'LV',14:'LAR',15:'MIA',16:'MIN',17:'NE',18:'NO',19:'NYG',
       20:'NYJ',21:'PHI',22:'ARI',23:'PIT',24:'LAC',25:'SF',26:'SEA',27:'TB',28:'WAS',
       29:'CAR',30:'JAX',33:'BAL',34:'HOU'}
BAD  = {'OUT', 'DOUBTFUL', 'INJURY_RESERVE', 'SUSPENSION', 'NOT_ACTIVE'}
WARN = {'QUESTIONABLE'}


def _get(view):
    url = READS.format(season=SEASON, lid=LEAGUE_ID) + '?view=' + view
    r = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=30)
    if r.status_code == 401:
        raise PermissionError('401')
    r.raise_for_status()
    return r.json()


def load_byes():
    """Team -> bye week. Derived once from the board, one row per NFL team."""
    if not os.path.exists(BYES):
        return {}
    out = {}
    with open(BYES, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                out[r['team'].strip()] = int(r['bye'])
            except (KeyError, ValueError):
                continue
    return out



def load_watch():
    """Things that are not injuries and will never show up as an injury status.

    Written because the August sweep graded Puka Nacua HEALTHY on HIGH confidence while a league
    review of an off-field matter was already public. The sweep asked medical questions of medical
    sources and got a clean answer, and the clean answer was the failure. ESPN's status field has
    the same blind spot: a man under review is ACTIVE right up until he is not.

    So this list is kept by hand and printed every time the lineup is checked. A missing file is
    reported, never skipped -- an empty watch box and no watch box must not look the same.
    """
    if not os.path.exists(WATCH):
        return [], 'watch_list.csv is not on the drive, so nothing off-field was checked'
    rows = []
    with open(WATCH, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('status') or '').strip().upper() != 'OPEN':
                continue
            rows.append({k: (r.get(k) or '').strip()
                         for k in ('player', 'team', 'what', 'since', 'last_checked')})
    return rows, ''

def page(verdict, reds, ambers, bench, week, note='', watch=None, watch_note=''):
    def rows(items):
        return ''.join(
            f'<tr><td class="p">{p["name"]}</td><td class="t">{p["slot"]}</td>'
            f'<td class="t">{p["team"]}</td><td class="n">{p["why"]}</td></tr>' for p in items)
    cls = 'bad' if reds else ('warn' if ambers else 'good')
    # doc 380: the stamp is the READ time and the run label (FF_WHO from ff.bat), not "the
    # scheduler", which this page said even when Matt ran it by hand.
    if _build_meta:
        try:
            _meta = _build_meta(src=SRC)          # doc 381: the next kickoff, off sched_2026.csv
        except TypeError:
            _meta = _build_meta()
        _stamp, _attrs, _agel = _meta['text'], _meta['attrs'], (_age_line() if _age_line else '')
        _lock = _meta.get('lock_text') or ''
    else:
        _stamp, _attrs, _agel = dt.datetime.now().strftime('%A %d %B, %H:%M') + ' (run label unknown)', '', ''
        _lock = ''
    body = [f'<div class="wrap">{page_bar(current="LINEUP_CHECK.html")}<h1>Lineup check</h1>',
            f'<div class="sub" id="inputs" {_attrs}>Week {week} &middot; read from ESPN {_stamp}'
            + (f' &middot; next kickoff on file: {_lock}' if _lock else '') + '</div>',
            _agel]
    if note:
        body.append(f'<div class="bad"><b>{note}</b></div>')
    body.append(f'<div class="{cls}"><b>{verdict}</b></div>')
    if watch:
        body.append('<h2>Off the field &mdash; still unresolved</h2>'
                    '<div class="sub">Not injuries: ESPN shows ACTIVE until he does not play. Check the '
                    'news on these before you lock the lineup.</div>'
                    '<table class="w"><tr><th>player</th><th>tm</th><th>what</th>'
                    '<th>since</th></tr>'
                    + ''.join(f'<tr><td class="p">{w["player"]}{" <b>(yours)</b>" if w.get("mine") else ""}</td>'
                              f'<td class="t">{w["team"]}</td><td class="n">{w["what"]}</td>'
                              f'<td class="t">{w["since"]}</td></tr>' for w in watch)
                    + '</table>')
    elif watch_note:
        body.append(f'<div class="bad"><b>Nothing off-field was checked: {watch_note}.</b></div>')
    if reds:
        body.append('<h2>Not playing &mdash; take them out</h2>'
                    '<table class="w"><tr><th>player</th><th>slot</th><th>tm</th><th>why</th></tr>'
                    + rows(reds) + '</table>')
    if ambers:
        body.append('<h2>Questionable &mdash; your call</h2>'
                    '<table class="w"><tr><th>player</th><th>slot</th><th>tm</th><th>why</th></tr>'
                    + rows(ambers) + '</table>')
    if (reds or ambers) and bench:
        body.append('<h2>Healthy on your bench</h2>'
                    '<table class="w"><tr><th>player</th><th>pos</th><th>tm</th><th>status</th></tr>'
                    + rows(bench) + '</table>')
    body.append('</div>')
    css = ("body{margin:0;background:#fcfcfb;color:#1a1a18;font:15px/1.55 Georgia,serif;padding:34px 30px}"
           ".wrap{max-width:760px;margin:0 auto}h1{font:700 27px/1.2 Georgia,serif;margin:0 0 4px}"
           "h2{font:700 12px/1 Georgia,serif;letter-spacing:.13em;text-transform:uppercase;color:#6b6b66;"
           "margin:30px 0 10px;padding-bottom:7px;border-bottom:1px solid #d9d7d2}"
           ".sub{color:#6b6b66;font-size:13px;margin-bottom:18px}"
           ".good,.warn,.bad{border-radius:8px;padding:14px 18px;margin:0 0 18px;font-size:15px}"
           ".good{background:#eef7f1;border:1px solid #b5d8c4;color:#0b6b3a}"
           ".warn{background:#fdf6e7;border:1px solid #e3d3a8;color:#7a5c12}"
           ".bad{background:#fdeceb;border:1px solid #e0b4b0;color:#8a2a22}"
           "table.w{border-collapse:collapse;width:100%;font-size:13.5px}"
           "table.w th{font:700 10px/1 Georgia,serif;letter-spacing:.1em;text-transform:uppercase;"
           "color:#6b6b66;text-align:left;padding:0 8px 6px 0;border-bottom:1px solid #d9d7d2}"
           "table.w td{padding:5px 8px 5px 0;border-bottom:1px solid #efeee9}"
           "td.p{font-weight:700}td.t{color:#6b6b66;font-size:12px}td.n{color:#6b6b66;font-size:12.5px}"
           "@media print{body{padding:0}p.jump.pagebar{display:none}}") + PAGEBAR_CSS
    out = os.path.join(SRC, 'LINEUP_CHECK.html')
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write("<!doctype html><html><head><meta charset='utf-8'><title>Lineup check</title>"
                 "<style>" + css + "</style></head><body>" + ''.join(body) + "</body></html>")
    os.replace(tmp, out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--html', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args(argv)

    try:
        data = _get('mRoster')
    except PermissionError:
        m = 'COOKIES EXPIRED -- ESPN refused. Run  py set_cookies.py  then run this again.'
        if a.html:
            page('CANNOT CHECK YOUR LINEUP', [], [], [], '?', note=m)
        print('\n  ' + m + '\n')
        return 2
    except Exception as exc:
        m = f'COULD NOT REACH ESPN ({type(exc).__name__}). Your lineup was NOT checked.'
        if a.html:
            page('CANNOT CHECK YOUR LINEUP', [], [], [], '?', note=m)
        print('\n  ' + m + '\n')
        return 2

    if a.check:
        print("  cookies OK -- ESPN answered for league %d, season %d." % (LEAGUE_ID, SEASON))
        return 0

    week = data.get('scoringPeriodId') or 0
    byes = load_byes()
    if not byes:
        print(f"  WARNING: {BYES} is missing, so bye weeks were NOT checked.")

    me = None
    for t in data.get('teams', []):
        if t.get('id') == MY_TEAM_ID:
            me = t
    if me is None:
        m = f'Could not find team {MY_TEAM_ID} in the league response. Nothing was checked.'
        if a.html:
            page('CANNOT CHECK YOUR LINEUP', [], [], [], week, note=m)
        print('\n  ' + m + '\n')
        return 2

    reds, ambers, bench, filled = [], [], [], set()
    for e in (me.get('roster') or {}).get('entries', []):
        p = e.get('playerPoolEntry', {}).get('player', {}) or {}
        slot = e.get('lineupSlotId')
        name = p.get('fullName', '?')
        team = PRO.get(p.get('proTeamId'), '?')
        st = (p.get('injuryStatus') or 'ACTIVE').upper()
        pos = POS.get(p.get('defaultPositionId'), '?')
        rec = dict(name=name, slot=SLOT_NAME.get(slot, str(slot)), team=team, why=st.title())
        if slot in BENCH_SLOTS:
            if st not in BAD:
                bench.append(dict(rec, why=st.title(), slot=pos))
            continue
        filled.add(slot)
        if byes.get(team) == week:
            reds.append(dict(rec, why=f'on BYE in week {week}'))
        elif st in BAD:
            reds.append(dict(rec, why=f'ESPN lists him {st.replace("_", " ").title()}'))
        elif st in WARN:
            ambers.append(dict(rec, why='Questionable'))

    if reds:
        verdict = ('One man in your lineup will not play.' if len(reds) == 1
                   else f'{len(reds)} men in your lineup will not play.')
    elif ambers:
        verdict = f'Lineup is legal. {len(ambers)} questionable to decide.'
    else:
        verdict = 'All clear. Everybody in your lineup is expected to play.'

    watch, watch_note = load_watch()
    mine_names = {r['name'] for r in reds + ambers + bench}
    for w in watch:
        w['mine'] = w['player'] in mine_names
    watch.sort(key=lambda w: (not w['mine'], w['player']))

    out = page(verdict, reds, ambers, bench, week, watch=watch, watch_note=watch_note) if a.html else None
    print(f"\n  Week {week}: {verdict}")
    for r in reds:
        print(f"    OUT   {r['name']:<24}{r['slot']:<7}{r['team']:<5}{r['why']}")
    for r in ambers:
        print(f"    ?     {r['name']:<24}{r['slot']:<7}{r['team']:<5}{r['why']}")
    if (reds or ambers) and bench:
        print("  healthy on your bench:")
        for b in bench:
            print(f"    {b['name']:<24}{b['slot']:<7}{b['team']:<5}{b['why']}")
    if watch:
        print("  OFF THE FIELD -- no injury flag will ever show these:")
        for w in watch:
            tag = '  (YOURS)' if w['mine'] else ''
            print(f"    {w['player']:<24}{w['team']:<5}{w['what']}{tag}")
    elif watch_note:
        print(f"  NOTHING OFF-FIELD CHECKED -- {watch_note}.")
    if out:
        print(f"  written: {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
