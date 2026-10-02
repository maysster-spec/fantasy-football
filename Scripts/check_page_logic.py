"""check_page_logic.py -- check the week sheet against the LEAGUE'S RULES, not against the engine.

WHY THIS EXISTS. Doc 425 measured that seven of eight shipped defects come back silently, and gave
the reason in one sentence: every page guard recomputes from the same engine it checks, so the page
and the check move together and agree. The layer that was missing is a check on the PAGE against a
rule that the code did not write. Doc 425 named this file for it. This is the first rule in it.

    P1  A man in the injured-reserve slot is never offered as the drop in THE CALL.
        Doc 436: on 28 Sept THE CALL paired "take Kalif Raymond" with "drop Jonah Coleman, 0.0"
        while Coleman sat in slot 21. A man in the IR slot holds none of the fifteen, so dropping
        him frees no seat and the claim runs as sixteen of fifteen and fails on the roster limit.
    P2  A man in the injured-reserve slot is never the "cheapest thing you own", in the table or in
        the cost line. Same doc, same night: "The cheapest man you own is Jonah Coleman, at 0.0."
    P3  Every man the wire marks "the job is open, see THE CALL" is named in the week sheet's DECISION
        REGION (band 0, from its heading to the bye calendar): in THE CALL, in the picks, in the
        below-the-cut line or in the line that says why he could not be priced. Doc 451: on 29 Sept
        Ollie Gordon II led the wire's IN DOUBT lane with De'Von Achane on injured reserve for the
        season, and the week sheet did not carry his name anywhere. Matt found it, not a guard.
        30 Sept, the first live run: it fired on Kendre Miller, priced at 2.3 and cut by the five-row
        cap, and it did NOT fire on DeeJay Dallas, cut the same way, because his name sat in the seat
        lane's left-off line further down the page. The page-wide search was the weaker guard: it now
        reads band 0 only, and a sheet without the band's anchors fails outright (0.2).
    P4  Every free man among ESPN's ten most-added (the +/- column, at least one full point, read off
        the newest WIRE_<date>.csv and FREE_UNRANKED_<date>.csv) is named in the sheet's crowd table
        with an answer. 30 Sept: the column Matt asked for on 23 Sept (doc 395) had been written to
        the CSV every run and printed nowhere; Jaylen Wright was ESPN's third most-added man and on
        no page. The table is the page's answer to "what do the analysts see that we do not"; this
        check makes sure nobody the crowd is adding goes unanswered.
    P5  THE CALL's "you would drop" never names a man who STARTS by the roster file's own season value
        (top QB, two RB, two WR, one TE, best man left as FLEX, among men valued above zero; slot_id is
        stale between weeks, so it is not used for this). Doc 462: on 1 Oct the page paired "take Pat Bryant" with
        "drop Sam LaPorta", his starting tight end, because the ladder refused every same-position
        drop and walked past two bench receivers. A kicker or defense is exempt (a second one on the
        bench makes the starting label arbitrary). Independent of the engine: it reads the file.
    P6  The long-shot lane (id="tickets", doc 461) names only FREE men (nobody on MY_ROSTER.csv) and
        never a "third string" shape (0 of 249 on both big-hit columns, doc 460); and it sits ABOVE
        the seat list exactly when the standings line's simulated top-six odds are under 30% (doc 469, v9.39;
        the points-for rank off standings_2026.csv is the fallback when no odds are printed). P6b: the odds the
        line prints are the simulator's own number for the files in Source, within a point.
    P10 THE CALL's net is "he is worth" minus the drop's cost with a negative cost counted as zero (doc 416),
        read as plain arithmetic off the three printed numbers. Doc 469: the mutation that adds a negative
        cost to the net survived the harness on the 1 Oct roster, where Pat Bryant is the drop at minus 2.4.
    P7  The waterfall under THE CALL (doc 462): the rank it prints is the standings file's waiver_rank;
        every "CLAIM X" names a man the newest WIRE_<date>.csv marks WAIVERS and every "ADD X now" a
        FREEAGENT; the hedge man it names neither starts by value nor sits in the IR slot.
    P8  A defense or kicker on the "Priority pickups" list is a HOLE fill ("No defense in week 5",
        "No kicker in week 8") and never a season-rate pick ("Outscores your defense in 10 weeks").
        Doc 467: on 1 Oct the list led with "Chiefs D/ST +7.8", a season number for a position the
        wire prices by the week's matchup (4.39); doc 424 had put the weekly rule on THE CALL and the
        drop table and the picks list under them was never covered. The page said it twice in one
        morning and Matt was told to ignore the row; a guard reads the list now. P8b (doc 470): a defense or
        kicker on THE CALL carries "fills the ... hole" in its facts line, since a hole fill is the only way a
        weekly position reaches THE CALL.
    P9  A rate the page marks as ESPN's own projection (data-vintage="proj" in the per-position
        grids) equals that man's rest-of-season projection in the newest espn_projections_2026_*.csv
        divided by the games left, which is 17 less the weeks already played, read off the grid's
        own first week column. Doc 419: the page divided a rest-of-season total by 17 every week and
        every projected rate ran about 11% low; no guard read the number against the file until this
        one, and check_guards.py reported the divisor mutation as a blind spot.

WHAT "PARKED" MEANS HERE. Source\\MY_ROSTER.csv, column slot_id, value 21 (ESPN's IR lineup slot,
directive section 2). The STATUS string is not used: a man can be OUT and not parked, and that man
is a legal drop. The roster file is read directly, never through sheet_engine, so an engine that
forgets who is parked cannot make this check forget with it.

THE JOIN IS NAME AND POSITION, and that is a stated limit, not an oversight. Section 3 says join on
espn_id wherever BOTH sides carry it. THE CALL's drop cell carries a name and a position and no id,
so the page side has no id to join on. The name is normalised the same way for both sides (case,
punctuation, generational suffixes) and the position must agree where the page prints one. A parked
man in the full drop table BELOW THE CALL is not checked: he is meant to be there, marked, because
knowing what he costs is not being asked to cut him (doc 415, doc 436).

    py check_page_logic.py              check Source\\WEEK_SHEET.html, exit 1 if a rule is broken
    py check_page_logic.py --selftest   the negative controls: each defect reproduced must fire,
                                        each legitimate look-alike must stay quiet

A missing page or a missing roster file is a FAILURE, not a skip (0.2: a step that cannot do the
thing it is named after must fail). Standard library only (doc 144). Every path resolves against
this file, never the shell.
"""
import collections
import csv
import glob
import html as _html
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'Source')

IR_SLOT = 21
_SUFFIX = frozenset({'jr', 'sr', 'ii', 'iii', 'iv', 'v'})

TAG = re.compile(r'<[^>]+>')
ROW = re.compile(r'<tr\b[^>]*>(.*?)</tr>', re.S | re.I)
CELL = re.compile(r'<t[hd]\b[^>]*>(.*?)</t[hd]>', re.S | re.I)
TABLE = re.compile(r'<table\b[^>]*>(.*?)</table>', re.S | re.I)
META = re.compile(r'<span class="meta">(.*?)</span>', re.S | re.I)
CALL_ANCHOR = re.compile(r'<h3 class="sub0">The call</h3>', re.I)
CHEAP_ANCHOR = re.compile(r'<th class="corner" scope="col">the cheapest thing you own</th>', re.I)
COST_LINE = re.compile(r'The cheapest man you own is\s*<b>(.*?)</b>', re.S | re.I)


def norm_name(s):
    """Lower case, no punctuation, no generational suffix. Written here rather than imported from
    sheet_engine so that this guard shares no code with the thing it checks."""
    s = _html.unescape(str(s or '')).lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return ' '.join(t for t in s.split() if t not in _SUFFIX)


def parked_men(roster_path):
    """[(norm_name, pos, printed name)] for every row of MY_ROSTER.csv whose slot_id is the IR slot.
    Returns None when the file is absent, which the caller reports as a failure."""
    if not os.path.exists(roster_path):
        return None
    out = []
    with open(roster_path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                slot = int((r.get('slot_id') or '').strip() or -1)
            except ValueError:
                slot = -1
            if slot == IR_SLOT:
                out.append((norm_name(r.get('player')), (r.get('pos') or '').strip().upper(),
                            (r.get('player') or '').strip()))
    return out


def _text(cell_html):
    return ' '.join(_html.unescape(TAG.sub(' ', cell_html)).split())


def _name_and_pos(cell_html):
    """A drop cell is 'Name<span class="meta">POS &middot; ...</span>'. Return (norm name, POS)."""
    meta = META.search(cell_html)
    pos = ''
    if meta:
        pos = _text(meta.group(1)).split('·')[0].strip().upper()
        cell_html = cell_html[:meta.start()] + cell_html[meta.end():]
    return norm_name(_text(cell_html)), pos


def _table_after(text, anchor):
    """The first table that FOLLOWS the anchor (THE CALL's heading precedes its table)."""
    m = anchor.search(text)
    if not m:
        return None
    t = TABLE.search(text, m.end())
    return t.group(1) if t else None


def _table_holding(text, anchor):
    """The table that CONTAINS the anchor (the cheapest-thing header is inside its table)."""
    m = anchor.search(text)
    if not m:
        return None
    for t in TABLE.finditer(text):
        if t.start() <= m.start() < t.end():
            return t.group(1)
    return None


def _hit(name, pos, parked):
    """True when (name, pos) names a parked man. Position must agree where both sides print one."""
    for pn, pp, _printed in parked:
        if pn == name and (not pos or not pp or pos == pp):
            return True
    return False


def scan(text, parked):
    """Return a list of (check, detail). `parked` is parked_men()'s list."""
    bad = []
    if not parked:
        return bad

    # P1 -- THE CALL's "you would drop" column, third cell of every body row.
    call = _table_after(text, CALL_ANCHOR)
    if call is not None:
        for row in ROW.findall(call):
            cells = CELL.findall(row)
            if len(cells) < 3 or 'colspan' in row:
                continue
            take = _text(cells[0])
            if take.lower().startswith('take'):
                continue                                   # the header row
            name, pos = _name_and_pos(cells[2])
            if _hit(name, pos, parked):
                bad.append(('P1 a man in the IR slot offered as the drop in THE CALL',
                            '%s / drop %s' % (take, _text(cells[2]))))

    # P2 -- the cheapest-thing table, first cell of every body row, and the cost line.
    cheap = _table_holding(text, CHEAP_ANCHOR)
    if cheap is not None:
        for row in ROW.findall(cheap):
            cells = CELL.findall(row)
            if len(cells) < 2:
                continue
            name, pos = _name_and_pos(cells[0])
            if name == norm_name('the cheapest thing you own'):
                continue                                   # the header row
            if _hit(name, pos, parked):
                bad.append(('P2 a man in the IR slot listed as the cheapest thing you own',
                            _text(cells[0])))
    for m in COST_LINE.finditer(text):
        name = norm_name(_text(m.group(1)))
        if _hit(name, '', parked):
            bad.append(('P2 a man in the IR slot named as the cheapest man in the cost line',
                        _text(m.group(1))))
    return bad


OPEN_ROW = re.compile(r'<tr\b[^>]*>(?:(?!</tr>).)*?the job is open(?:(?!</tr>).)*?</tr>', re.S | re.I)


REGION_START = re.compile(r'<h2\b[^>]*\bid="s0"', re.I)     # band 0: "Week N -- what to do"
REGION_END = re.compile(r'<h3\b[^>]*\bid="byes"', re.I)      # the bye calendar closes the decision


def decision_region(sheet_text):
    """The HTML of band 0 up to the bye calendar, or None when either anchor is missing."""
    a = REGION_START.search(sheet_text)
    b = REGION_END.search(sheet_text, a.end()) if a else None
    if not a or not b:
        return None
    return sheet_text[a.start():b.start()]


def open_jobs_on_sheet(wire_text, sheet_text):
    """P3: [(check, detail)]. The names the wire marks as open jobs, each looked for in the visible
    text of the sheet's decision region under the same normalisation. Reads two pages and no engine."""
    bad = []
    opens = []
    for row in OPEN_ROW.findall(wire_text):
        cells = CELL.findall(row)
        if cells:
            opens.append(_text(cells[0]))
    if not opens:
        return bad
    region = decision_region(sheet_text)
    if region is None:
        return [('P3 cannot read the decision region: the sheet has no band-0 heading (id="s0") or no '
                 'bye calendar (id="byes") after it', 'the open jobs cannot be checked: ' + ', '.join(opens))]
    plain = norm_name(_text(region))
    for shown in opens:
        name = norm_name(shown)
        if name and name not in plain:
            bad.append(('P3 the wire marks a job as open and the week sheet does not name the man',
                        '%s: not in THE CALL, the picks, the below-the-cut line or the not-priced line'
                        % shown))
    return bad


CROWD_MIN_CHG = 1.0      # the same bar sheet_engine.crowd_table uses; a copy on purpose, this file reads no engine
CROWD_ROWS = 10
CROWD_START = re.compile(r'<h3\b[^>]*\bid="crowd"', re.I)


def most_added(src):
    """[(printed name, +/-)] for the free men ESPN's +/- puts at CROWD_MIN_CHG or more, best first,
    at most CROWD_ROWS, read off the newest WIRE_<date>.csv and FREE_UNRANKED_<date>.csv. None when
    there is no wire file at all."""
    wires = sorted(glob.glob(os.path.join(src, 'WIRE_*.csv')))
    if not wires:
        return None
    files = [wires[-1]] + sorted(glob.glob(os.path.join(src, 'FREE_UNRANKED_*.csv')))[-1:]
    out = []
    for f in files:
        with open(f, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                try:
                    chg = float(r.get('own_chg') or '')
                except ValueError:
                    continue
                if chg >= CROWD_MIN_CHG and (r.get('player') or '').strip():
                    out.append((r['player'].strip(), chg))
    out.sort(key=lambda t: -t[1])
    return out[:CROWD_ROWS]


def crowd_on_sheet(added, sheet_text):
    """P4: [(check, detail)]. Each most-added name must be in the crowd table (from its heading to the
    bye calendar). No table while men qualify is a failure; no qualifying man is quiet."""
    if not added:
        return []
    a = CROWD_START.search(sheet_text)
    b = REGION_END.search(sheet_text, a.end()) if a else None
    if not a or not b:
        return [('P4 the crowd table is missing (id="crowd" to id="byes") while ESPN\'s most-added men exist',
                 ', '.join('%s %+.1f' % t for t in added))]
    plain = norm_name(_text(sheet_text[a.start():b.start()]))
    bad = []
    for shown, chg in added:
        if norm_name(shown) not in plain:
            bad.append(('P4 one of ESPN\'s most-added free men has no answer on the sheet',
                        '%s (%+.1f): not in the crowd table' % (shown, chg)))
    return bad


def check_crowd(src, sheet):
    """P4 for the files on disk. No wire file at all is a failure (0.2)."""
    if not os.path.exists(sheet):
        return [('P0 page was not built', sheet)]
    added = most_added(src)
    if added is None:
        return [('P0 no WIRE_<date>.csv in Source, so the most-added men cannot be known', src)]
    with open(sheet, encoding='utf-8', errors='replace') as fh:
        return crowd_on_sheet(added, fh.read())


def check_open_jobs(wire, sheet):
    """P3 for the two files. A missing page is a failure (0.2)."""
    for p in (wire, sheet):
        if not os.path.exists(p):
            return [('P0 page was not built', p)]
    with open(wire, encoding='utf-8', errors='replace') as fh:
        w = fh.read()
    with open(sheet, encoding='utf-8', errors='replace') as fh:
        t = fh.read()
    return open_jobs_on_sheet(w, t)


STARTS = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1}      # the skill starters; the best man left among RB/WR/TE is the FLEX


def roster_slots(roster_path):
    """{norm_name: slot_id} off MY_ROSTER.csv, or None when the file is absent. slot_id is ESPN's lineup
    slot AT PULL TIME, which is stale between weeks (on 1 Oct Vele sat in the FLEX slot from week 3), so
    P5 and P7 judge a STARTER by value, below, and use the slot only for the IR seat."""
    if not os.path.exists(roster_path):
        return None
    out = {}
    with open(roster_path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                out[norm_name(r.get('player'))] = int((r.get('slot_id') or '').strip() or -1)
            except ValueError:
                out[norm_name(r.get('player'))] = -1
    return out


def roster_starters(roster_path):
    """The set of norm names who START by the roster file's own season value: the top QB, two RB, two WR,
    one TE, and the best man left among RB/WR/TE as the FLEX, counting only men whose value is above
    zero. Men in the IR slot, men with no value and men below replacement are not judged. Independent of
    the engine and of the lineup ESPN happened to hold at pull time. The value is the August board's, so
    a man scoring now on a negative board value (Raymond) is missed, never falsely named: a floor."""
    if not os.path.exists(roster_path):
        return None
    rows = []
    with open(roster_path, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                slot = int((r.get('slot_id') or '').strip() or -1)
                val = float(r.get('value'))
            except (TypeError, ValueError):
                continue
            pos = (r.get('pos') or '').strip().upper()
            # a value at or below zero is BELOW REPLACEMENT on the board: that man is not a starter in
            # the sense that matters here (dropping him costs nothing against the bar), whatever his rank
            # among the men left. On 1 Oct Vele (-64.5) was the second receiver by value because
            # Pickens carries no value on the file and Nacua sat in the IR slot.
            if slot == IR_SLOT or pos not in STARTS or val <= 0:
                continue
            rows.append((pos, val, norm_name(r.get('player'))))
    starters, left = set(), []
    for pos, n in STARTS.items():
        men = sorted((r for r in rows if r[0] == pos), key=lambda r: -r[1])
        starters.update(r[2] for r in men[:n])
        left.extend(r for r in men[n:] if pos in ('RB', 'WR', 'TE'))
    if left:
        starters.add(max(left, key=lambda r: r[1])[2])
    return starters


def starters_in_call(text, starters):
    """P5: [(check, detail)]. A drop cell in THE CALL naming a man who starts by value."""
    bad = []
    call = _table_after(text, CALL_ANCHOR)
    if call is None or not starters:
        return bad
    for row in ROW.findall(call):
        cells = CELL.findall(row)
        if len(cells) < 3 or 'colspan' in row:
            continue
        take = _text(cells[0])
        if take.lower().startswith('take'):
            continue
        name, pos = _name_and_pos(cells[2])
        if name in starters:
            bad.append(('P5 a starter offered as the drop in THE CALL (doc 462: "drop Sam LaPorta")',
                        '%s / drop %s' % (take, _text(cells[2]))))
    return bad


PICKS_START = re.compile(r'<h3 class="sub0">Priority pickups, in order</h3>', re.I)
PICK_BLOCK = re.compile(r'<div class="mv(?: big)?">(.*?)</div>(?=<div class="mv|<h[23]\b|<div class="(?!mv)|$)', re.S | re.I)
PICK_META = re.compile(r'<span class="mmeta">(.*?)</span>', re.S | re.I)
PICK_CTX = re.compile(r'<p class="ctx">(.*?)</p>', re.S | re.I)
WEEKLY = {'D/ST', 'K'}


def weekly_in_picks(text):
    """P8: [(check, detail)]. A defense or kicker on the picks list priced on anything but a hole."""
    bad = []
    m = PICKS_START.search(text)
    if not m:
        return bad
    end = re.search(r'<h[23]\b', text[m.end():])
    body = text[m.end():m.end() + end.start()] if end else text[m.end():]
    for blk in PICK_BLOCK.findall(body):
        meta = PICK_META.search(blk)
        pos = _text(meta.group(1)).split('·')[0].strip().upper() if meta else ''
        if pos not in WEEKLY:
            continue
        ctx = PICK_CTX.search(blk)
        line = _text(ctx.group(1)) if ctx else ''
        if not line.lower().startswith('no '):
            nm = re.search(r'<b class="nm"[^>]*>(.*?)</b>', blk, re.S | re.I)
            bad.append(('P8 a defense or kicker on the picks list priced on a season rate, not a hole '
                        '(doc 467: "Chiefs D/ST +7.8, outscores your defense in 10 weeks")',
                        '%s / %s' % (_text(nm.group(1)) if nm else pos, line[:90])))
    return bad


GRID_TABLE = re.compile(r'<table>(.*?)</table>', re.S | re.I)
GRID_WEEK = re.compile(r'<th scope="col">(\d+)</th>')
GRID_ROW = re.compile(r'<tr>(.*?)</tr>', re.S | re.I)
GRID_NAME = re.compile(r'<span class="pl" title="([^"]*)">.*?<span class="meta">([^<&]*)', re.S | re.I)
GRID_PROJ = re.compile(r'<td class="rate" data-vintage="proj"[^>]*>([\d.]+)</td>', re.I)
PROJ_GAMES = 17


def load_proj(src):
    """{(name, TEAM): proj_2026} off the newest espn_projections_2026_*.csv, or None when there is none."""
    import glob
    pulls = sorted(glob.glob(os.path.join(src, 'espn_projections_2026_*.csv')))
    if not pulls:
        return None
    out = {}
    with open(pulls[-1], newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            nm = (r.get('Player') or r.get('player') or '').strip()
            try:
                out[(nm, (r.get('team') or '').strip().upper())] = float(r.get('proj_2026') or 0)
            except ValueError:
                pass
    return out


def rate_divisor_checks(text, proj):
    """P9: [(check, detail)]. Every projection-only rate on the grids against the file and the games left."""
    bad = []
    if proj is None:
        return [('P9 no espn_projections_2026_*.csv in Source, so no projected rate can be checked', '')]
    for tbl in GRID_TABLE.findall(text):
        hdr = GRID_WEEK.findall(tbl)
        if not hdr:
            continue
        left = PROJ_GAMES - (int(hdr[0]) - 1)
        for row in GRID_ROW.findall(tbl):
            m = GRID_NAME.search(row)
            rc = GRID_PROJ.search(row)
            if not (m and rc):
                continue
            name, tm, rate = _html.unescape(m.group(1)), m.group(2).strip().upper(), float(rc.group(1))
            p = proj.get((name, tm))
            if p is None:
                continue                      # a name the file spells differently is not a divisor error
            want = p / float(left)
            if abs(want - rate) > 0.051:
                bad.append(('P9 a projected rate is not the file\'s rest-of-season total over the games left '
                            '(doc 419: the page divided by 17 every week)',
                            '%s %s prints %.1f, the file says %.1f over %d games = %.1f' % (name, tm, rate, p, left, want)))
    return bad


ODDS_LINE = re.compile(r'<b>(\d{1,3})%</b>\s*to make the top six', re.I)
NUM = re.compile(r'[-+]?\d+(?:\.\d+)?')


def net_checks(text):
    """P10: [(check, detail)]. On every row of THE CALL, net equals "he is worth" minus the drop's cost with a
    negative cost counted as zero (doc 416: a negative cost is not a gain). Plain arithmetic on the three
    printed numbers, so the engine's own netting cannot vouch for itself."""
    bad = []
    call = _table_after(text, CALL_ANCHOR)
    if call is None:
        return bad
    for row in ROW.findall(call):
        cells = CELL.findall(row)
        if len(cells) < 5 or 'colspan' in row:
            continue
        take = _text(cells[0])
        if take.lower().startswith('take'):
            continue
        try:
            worth = float(NUM.search(_text(cells[1])).group(0))
            cost = float(NUM.search(_text(cells[3])).group(0))
            net = float(NUM.search(_text(cells[4])).group(0))
        except (AttributeError, ValueError):
            continue
        want = worth - max(0.0, cost)
        if abs(want - net) > 0.11:
            bad.append(('P10 THE CALL\'s net is not worth minus the drop\'s cost with a negative cost at zero (doc 416)',
                        '%s: worth %+.1f, cost %.1f, net printed %+.1f, arithmetic %+.1f' % (take.split(' ')[0] + ' ' + take.split(' ')[1] if ' ' in take else take, worth, cost, net, want)))
    return bad


def weekly_in_call(text):
    """P8b: [(check, detail)]. A defense or kicker on THE CALL is a hole fill (its facts line says "fills the ...
    hole"), never a season-rate add (doc 424's defect, doc 470's admission of hole fills to THE CALL)."""
    bad = []
    call = _table_after(text, CALL_ANCHOR)
    if call is None:
        return bad
    for row in ROW.findall(call):
        cells = CELL.findall(row)
        if len(cells) < 3 or 'colspan' in row:
            continue
        name, pos = _name_and_pos(cells[0])
        if pos not in WEEKLY:
            continue
        if 'fills the' not in _text(cells[0]).lower():
            bad.append(('P8b a defense or kicker on THE CALL that is not a hole fill (doc 424, doc 470)', _text(cells[0])[:90]))
    return bad


LANE_START = re.compile(r'<h2\b[^>]*\bid="tickets"', re.I)
SEATS_START = re.compile(r'<h2\b[^>]*\bid="seats"', re.I)


def pf_rank_of_mine(src):
    """(rank by points for, teams) off standings_2026.csv, or None. Rebuilt here, not read off the page."""
    p = os.path.join(src, 'standings_2026.csv')
    if not os.path.exists(p):
        return None
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                rows.append(((r.get('mine') or '').strip() == 'yes', float(r.get('points_for'))))
            except (TypeError, ValueError):
                continue
    me = [v for m, v in rows if m]
    if not me:
        return None
    return 1 + sum(1 for _, v in rows if v > me[0]), len(rows)


def lane_checks(text, slots, pf):
    """P6: [(check, detail)]. The long-shot lane's rows and its place against the seat list."""
    bad = []
    a = LANE_START.search(text)
    b = SEATS_START.search(text)
    if not a:
        return bad                                    # no lane built (constants absent): doc 461 prints a box
    end = text.find('<h2', a.end())
    lane = text[a.start():end if end > 0 else len(text)]
    tbl = TABLE.search(lane)
    if tbl:
        for row in ROW.findall(tbl.group(1)):
            cells = CELL.findall(row)
            if len(cells) < 2:
                continue
            name, _ = _name_and_pos(cells[0])
            if name in (slots or {}):
                bad.append(('P6 a man on your own roster is on the long-shot lane', _text(cells[0])))
            if 'third string' in _text(cells[1]).lower():
                bad.append(('P6 a third-string shape on the long-shot lane (0 of 249, doc 460)', _text(cells[0])))
    om = ODDS_LINE.search(text)
    if om and b:
        # [doc 469, v9.39] the trigger is the simulated odds the standings line prints: under 30% the lane leads
        odds = int(om.group(1)) / 100.0
        behind = odds < 0.30
        leads = a.start() < b.start()
        if behind != leads:
            bad.append(('P6 the lane %s the seat list while the page prints %d%% to make the top six'
                        % ('leads' if leads else 'follows', int(om.group(1))), 'doc 464: it leads only under 30%'))
    elif pf and b:
        behind = pf[0] > 6
        leads = a.start() < b.start()
        if behind != leads:
            bad.append(('P6 the lane %s the seat list while the standings file puts you %s of %d in points for'
                        % ('leads' if leads else 'follows', pf[0], pf[1]), 'doc 461: it leads only outside the top six (no odds printed)'))
    return bad


def odds_checks(text, src):
    """P6b: [(check, detail)]. The odds the standings line prints equal the simulator's own number for the
    files in Source (research\\playoff_odds.py, the same seed), within a point. The simulator is a different
    file from the engine; it is the one place the number is computed, so the page cannot drift from it."""
    om = ODDS_LINE.search(text)
    if not om:
        return []
    try:
        rd = os.path.join(HERE, 'research')
        if rd not in sys.path:
            sys.path.insert(0, rd)
        import playoff_odds as _po
        r = _po.live_numbers(src, 5.0)
    except Exception as exc:
        return [('P6b the standings line prints playoff odds the simulator could not reproduce', '%s: %s' % (type(exc).__name__, exc))]
    if not r:
        return [('P6b the standings line prints playoff odds with no schedule_2026.csv in Source', om.group(0))]
    want = round(100 * r['base'][r['me']])
    if abs(want - int(om.group(1))) > 1:
        return [('P6b the standings line prints playoff odds the simulator does not give', 'page %s%%, simulator %d%%' % (om.group(1), want))]
    return []


MATCHUP_COEF = {'RB': 0.10, 'TE': 0.11}   # doc 468: a copy on purpose, this file reads no engine
MATCHUP_MIN_WEEKS = 4
PAGE_WEEK = re.compile(r'Week (\d+) &mdash; what to do', re.I)
ROSTER_START = re.compile(r'<h2\b[^>]*\bid="s5"', re.I)
ROSTER_ROW = re.compile(r'<th scope="row"><span class="pl" title="([^"]*)">[^<]*</span>'
                        r'<span class="meta">(QB|RB|WR|TE|D/ST|K) &middot; ([A-Z]{2,3})', re.I)
MATCHUP_TXT = re.compile(r'matchup vs ([A-Z]{2,3}) (\+|&minus;)(\d+\.\d)', re.I)
ROW_POS = re.compile(r'<span class="meta">(QB|RB|WR|TE|D/ST|K)\b', re.I)


def matchup_terms_file(src, week):
    """The matchup term recomputed from the two files, independently of the engine: {(defense, pos):
    points a week} for every defense with MATCHUP_MIN_WEEKS finished weeks faced before `week`, and
    {team: opponent in `week`}. ({}, {}) when a file is missing or no defense has the record."""
    fp, sp = os.path.join(src, 'form_2026.csv'), os.path.join(src, 'sched_2026.csv')
    if not (os.path.exists(fp) and os.path.exists(sp)):
        return {}, {}
    opp_by = {}
    with open(sp, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                opp_by[(int(r['week']), (r['team'] or '').strip().upper())] = (r['opp'] or '').strip().upper()
            except (KeyError, ValueError):
                continue
    pts, wks = collections.defaultdict(float), collections.defaultdict(set)
    with open(fp, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                w, pos, v = int(r['week']), (r.get('pos') or '').strip(), float(r.get('half_ppr') or 0)
            except (KeyError, ValueError):
                continue
            if w < 1 or w >= week or pos not in MATCHUP_COEF or str(r.get('in_progress') or '0').strip() == '1':
                continue
            d = opp_by.get((w, (r.get('team') or '').strip().upper()))
            if d:
                pts[(d, pos)] += v
                wks[(d, pos)].add(w)
    terms = {}
    for pos in MATCHUP_COEF:
        apg = {d: pts[(d, p)] / len(wks[(d, p)]) for (d, p) in wks if p == pos and len(wks[(d, p)]) >= MATCHUP_MIN_WEEKS}
        if apg:
            mean = sum(apg.values()) / len(apg)
            for d, v in apg.items():
                terms[(d, pos)] = MATCHUP_COEF[pos] * (v - mean)
    return terms, {t: o for (w, t), o in opp_by.items() if w == week}


def matchup_checks(text, src):
    """P11: [(check, detail)]. The matchup number beside a rate (doc 468, finding 4.49): only on RB and TE
    rows; equal to the two files' own arithmetic within 0.06; on every roster RB and TE whose opponent
    this week has the record; and nowhere when no defense has it yet."""
    bad = []
    wm = PAGE_WEEK.search(text)
    if not wm:
        return bad
    week = int(wm.group(1))
    terms, opp = matchup_terms_file(src, week)
    for row in ROW.findall(text):
        mm = MATCHUP_TXT.search(row)
        if not mm:
            continue
        pm = ROW_POS.search(row)
        pos = pm.group(1).upper() if pm else '?'
        d, sign, val = mm.group(1).upper(), mm.group(2), float(mm.group(3))
        shown = val if sign == '+' else -val
        who = _html.unescape(TAG.sub('', row))[:60].strip()
        if pos not in MATCHUP_COEF:
            bad.append(('P11 a matchup number on a row that is not a back or a tight end (doc 468: nothing at receiver)', who))
            continue
        if (d, pos) not in terms:
            bad.append(('P11 a matchup number for a defense without four weeks of record, or with no term built', '%s vs %s' % (who, d)))
            continue
        if abs(terms[(d, pos)] - shown) > 0.06:
            bad.append(('P11 a matchup number the two files do not give', '%s prints %+.1f vs %s, the files say %+.1f' % (who, shown, d, terms[(d, pos)])))
    rs = ROSTER_START.search(text)
    if rs and terms:
        tbl = TABLE.search(text, rs.end())
        if tbl:
            for row in ROW.findall(tbl.group(1)):
                m = ROSTER_ROW.search(row)
                if not m:
                    continue
                name, pos, tm = _html.unescape(m.group(1)), m.group(2).upper(), m.group(3).upper()
                d = opp.get(tm)
                if pos in MATCHUP_COEF and d and (d, pos) in terms and not MATCHUP_TXT.search(row):
                    bad.append(('P11 a roster back or tight end with a priced opponent and no matchup number', '%s %s vs %s' % (name, tm, d)))
    return bad


TOTAL_LINE = re.compile(r'Taking (it|both|all (\d+))(?: this week)? nets\s*<b>([-+]?\d+(?:\.\d+)?)</b>', re.I)
CALL_META = re.compile(r'<span class="meta">(QB|RB|WR|TE|D/ST|K) &middot; ([A-Z]{2,3})', re.I)


def te_leaders_file(src):
    """{team: (leader name, targets)} and {norm_name: targets} for tight ends in the NEWEST finished week on
    form_2026.csv, read here without the engine (doc 457: the man ahead is read off the newest game)."""
    p = os.path.join(src, 'form_2026.csv')
    if not os.path.exists(p):
        return {}, {}
    rows = []
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            try:
                w, t = int(r.get('week') or 0), float(r.get('targets') or 0)
            except ValueError:
                continue
            if w <= 0 or (r.get('pos') or '') != 'TE' or str(r.get('in_progress') or '0').strip() == '1':
                continue
            rows.append((w, (r.get('team') or '').strip().upper(), r.get('player') or '', t))
    if not rows:
        return {}, {}
    newest = max(r[0] for r in rows)
    lead, mine = {}, {}
    for w, tm, nm, t in rows:
        if w != newest:
            continue
        mine[norm_name(nm)] = t
        if tm not in lead or t > lead[tm][1]:
            lead[tm] = (nm, t)
    return lead, mine


def call_rows(text):
    """[(name, pos, team, row html, when text)] for every data row of THE CALL, or []."""
    call = _table_after(text, CALL_ANCHOR)
    if call is None:
        return []
    out = []
    for row in ROW.findall(call):
        cells = CELL.findall(row)
        if len(cells) < 6 or 'colspan' in row or _text(cells[0]).lower().startswith('take'):
            continue
        m = CALL_META.search(cells[0])
        name = _html.unescape(TAG.sub('', cells[0].split('<span', 1)[0])).strip()
        out.append((name, m.group(1).upper() if m else '?', m.group(2).upper() if m else '?', row, _text(cells[5]).strip()))
    return out


def te_leader_checks(text, src):
    """P12: [(check, detail)]. A tight end on THE CALL this week whose team's tight-end target leader in the
    newest finished game is another man with six or more targets and twice his (doc 457: a second tight end
    has never cleared the screen, so he gets no rate). A hole fill for a later week is a calendar claim and
    is not this."""
    bad = []
    lead, mine = te_leaders_file(src)
    if not lead:
        return bad
    for name, pos, tm, row, when in call_rows(text):
        if pos != 'TE' or when.lower() != 'this week' or 'hole' in _text(row).lower():
            continue
        ld = lead.get(tm)
        if not ld or norm_name(ld[0]) == norm_name(name):
            continue
        my = mine.get(norm_name(name)) or 0.0
        if ld[1] >= 6 and ld[1] >= 2 * my:
            bad.append(('P12 a tight end behind his team\'s target leader sits on THE CALL this week (doc 457: a second tight end never cleared the screen)',
                        '%s %s: %s had %.0f targets to his %.0f in the newest game' % (name, tm, ld[0], ld[1], my)))
    return bad


def total_checks(text):
    """P13: [(check, detail)]. The line under THE CALL, "Taking all N nets +X", counts only the rows marked
    "this week" and sums only their nets (doc 457: a row marked for a later week is a calendar claim and is
    not in tonight's total)."""
    bad = []
    rows = call_rows(text)
    tm = TOTAL_LINE.search(text)
    if not rows or not tm:
        return bad
    n_want = 1 if tm.group(1).lower() == 'it' else (2 if tm.group(1).lower() == 'both' else int(tm.group(2)))
    now, later = [], []
    for name, pos, team, row, when in rows:
        cells = CELL.findall(row)
        try:
            net = float(NUM.search(_text(cells[4])).group(0))
        except (AttributeError, ValueError, IndexError):
            continue
        (now if when.lower() == 'this week' else later).append((name, net))
    total = float(tm.group(3))
    if n_want != len(now) or abs(sum(v for _, v in now) - total) > 0.11:
        bad.append(('P13 THE CALL\'s total counts a row marked for a later week, or not every row marked this week (doc 457)',
                    'line says %d rows net %+.1f; this-week rows %d net %+.1f; later rows %s'
                    % (n_want, total, len(now), sum(v for _, v in now), ', '.join(n for n, _ in later) or 'none')))
    return bad


WF_RANK = re.compile(r'You are\s*<b>(\d+) of (\d+)</b>\s*on waivers', re.I)
WF_CLAIM = re.compile(r'<b>(?:CLAIM|Conditionally add) ([^<]+)</b>', re.I)   # doc 469: the card says it ESPN's way
WF_ADD = re.compile(r'<b>ADD ([^<]+?) now</b>', re.I)
WF_HEDGE = re.compile(r'the same drop,\s*<b>([^<]+)</b>', re.I)


def wire_avail(src):
    """{norm_name: avail} off the newest WIRE_<date>.csv and FREE_UNRANKED_<date>.csv, or None."""
    out = {}
    found = False
    for pat in ('WIRE_*.csv', 'FREE_UNRANKED_*.csv'):
        files = sorted(glob.glob(os.path.join(src, pat)))
        if not files:
            continue
        found = True
        with open(files[-1], newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                out[norm_name(r.get('player'))] = (r.get('avail') or '').strip().upper()
    return out if found else None


def my_waiver_rank(src):
    p = os.path.join(src, 'standings_2026.csv')
    if not os.path.exists(p):
        return None
    with open(p, newline='', encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            if (r.get('mine') or '').strip() == 'yes':
                try:
                    return int(float(r.get('waiver_rank')))
                except (TypeError, ValueError):
                    return None
    return None


def waterfall_checks(text, slots, avail, wrank, starters=None):
    """P7: [(check, detail)]. The waterfall's rank, its CLAIM/ADD words and its hedge man (never a
    starter by value, never a man in the IR slot)."""
    bad = []
    i = text.find('How to place them')
    if i < 0:
        return bad
    end = text.find('</details>', i)
    wf = text[i:end if end > 0 else len(text)]
    m = WF_RANK.search(wf)
    if m and wrank is not None and int(m.group(1)) != wrank:
        bad.append(('P7 the waterfall prints a waiver rank the standings file does not hold',
                    'page %s, file %s' % (m.group(1), wrank)))
    for nm in WF_CLAIM.findall(wf):
        if avail is not None and avail.get(norm_name(nm)) == 'FREEAGENT':
            bad.append(('P7 the waterfall says CLAIM for a free agent', nm))
    for nm in WF_ADD.findall(wf):
        if avail is not None and avail.get(norm_name(nm)) == 'WAIVERS':
            bad.append(('P7 the waterfall says ADD for a man on waivers', nm))
    h = WF_HEDGE.search(wf)
    if h:
        _hn = norm_name(h.group(1))
        if (starters and _hn in starters) or (slots is not None and slots.get(_hn) == IR_SLOT):
            bad.append(('P7 the hedge man starts for you, or sits in the IR slot', h.group(1)))
    return bad


def check(sheet, roster_path):
    """[(check, detail)] for one page against one roster file. Missing inputs are failures."""
    if not os.path.exists(sheet):
        return [('P0 page was not built', sheet)]
    parked = parked_men(roster_path)
    if parked is None:
        return [('P0 roster file missing, so who is parked cannot be known', roster_path)]
    with open(sheet, encoding='utf-8', errors='replace') as fh:
        text = fh.read()
    return scan(text, parked) + starters_in_call(text, roster_starters(roster_path)) + net_checks(text)    # P1, P2, P5, P10


# ----------------------------------------------------------------------------- negative controls

# [doc 462] The fixture carries a full set of starters by value, because P5 judges a starter by the
# file's own values: with only two backs on it, both would be "starters" and P1's quiet controls fire.
_ROSTER = ('asof,espn_id,player,pos,team,bye,value,slot_id,status\n'
           '2026-09-29,4702555,Jonah Coleman,RB,DEN,10,-102.9,21,INJURY_RESERVE\n'
           '2026-09-29,4426515,Puka Nacua,WR,LAR,11,131.3,21,OUT\n'
           '2026-09-29,3116389,Samaje Perine,RB,CIN,6,-77.5,20,ACTIVE\n'
           '2026-09-29,4038815,Rico Dowdle,RB,PIT,9,2.8,20,OUT\n'
           '2026-09-29,4890973,Ashton Jeanty,RB,LV,13,79.6,2,ACTIVE\n'
           '2026-09-29,4685702,Quinshon Judkins,RB,CLE,11,41.8,2,ACTIVE\n'
           '2026-09-29,16800,Davante Adams,WR,LAR,11,35.0,4,ACTIVE\n'
           '2026-09-29,4426354,George Pickens,WR,PIT,14,30.0,4,ACTIVE\n'
           '2026-09-29,4373626,Tyler Allgeier,RB,ARI,14,5.0,20,ACTIVE\n')

_CALL = ('<h3 class="sub0">The call</h3><div class="scroll"><table><thead>'
         '<tr><th class="corner" scope="col">take</th><th class="tot" scope="col">he is worth</th>'
         '<th scope="col">you would drop</th><th class="tot" scope="col">that costs</th>'
         '<th class="tot" scope="col">net</th><th scope="col">when</th></tr></thead><tbody>'
         '<tr><th scope="row">Michael Mayer<span class="meta">TE &middot; LV</span></th>'
         '<td class="tot pos">+9.9</td><td>%s</td><td class="tot">0.0</td>'
         '<td class="tot pos">+9.9</td><td class="meta">this week</td></tr>'
         '</tbody></table></div>')

_CHEAP = ('<div class="scroll"><table><thead><tr><th class="corner" scope="col">the cheapest thing '
          'you own</th><th scope="col">what dropping him costs, all 14 weeks</th></tr></thead><tbody>'
          '<tr><th scope="row"><span class="pl" title="%s">%s</span><span class="meta">RB &middot; '
          '%s</span></th><td class="zero">0.0</td></tr></tbody></table></div>')

_FULL = ('<h3 class="sub0">What each of your own men costs to drop</h3><div class="scroll"><table>'
         '<tbody><tr><th scope="row">Jonah Coleman<span class="meta">RB &middot; DEN</span></th>'
         '<td>0.0</td><td>he is in the injured-reserve slot, so dropping him frees no roster seat'
         '</td></tr></tbody></table></div>')


def selftest():
    import tempfile
    fails = []

    def run(html_text, note, want, roster=_ROSTER):
        with tempfile.TemporaryDirectory() as d:
            sheet = os.path.join(d, 'WEEK_SHEET.html')
            ro = os.path.join(d, 'MY_ROSTER.csv')
            with open(sheet, 'w', encoding='utf-8') as fh:
                fh.write(html_text)
            if roster is not None:
                with open(ro, 'w', encoding='utf-8') as fh:
                    fh.write(roster)
            got = check(sheet, ro)
            ok = (len(got) > 0) == want
            print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
            if not ok:
                fails.append((note, got))
            return got

    drop = lambda n, p: '%s<span class="meta">%s</span>' % (n, p)
    print('MUST FIRE -- the defect doc 436 shipped, and the shapes of it')
    run(_CALL % drop('Jonah Coleman', 'RB &middot; <b class="hurt">Injured Reserve</b>'),
        'doc 436: THE CALL drops a man in the IR slot', True)
    run(_CALL % drop('Puka Nacua', 'WR'), 'a second parked man, status OUT, in the drop cell', True)
    run(_CALL % drop('Jonah Coleman', ''), 'the drop cell prints no position at all', True)
    run(_CHEAP % ('Jonah Coleman', 'Jonah Coleman', 'DEN'),
        'doc 436: the cheapest-thing table lists a parked man', True)
    run('<p><b>Every pickup below costs a drop.</b> The cheapest man you own is <b>Jonah Coleman</b>, '
        'at <b>0.0</b></p>', 'doc 436: the cost line names a parked man', True)
    run(_CALL % drop('Jonah Coleman Jr.', 'RB'), 'the same man with a suffix the roster lacks', True)
    run('<p>built</p>', 'the roster file absent: who is parked cannot be known', True, roster=None)
    missing = check(os.path.join(SRC, '__no_such_page__.html'), os.path.join(SRC, 'MY_ROSTER.csv'))
    ok = bool(missing)
    print('  %-4s %-66s fired=%d expected=True' % ('ok' if ok else 'BAD', 'a page that was never built',
                                                   len(missing)))
    if not ok:
        fails.append(('missing page', missing))

    print('MUST STAY QUIET -- the shapes that look like the defect and are correct')
    run(_CALL % drop('Samaje Perine', 'RB'), 'THE CALL drops a bench man (slot 20)', False)
    run(_CALL % drop('Rico Dowdle', 'RB'), 'THE CALL drops a man who is OUT but on the bench', False)
    run(_CALL % drop('Jonah Coleman', 'WR'), 'a parked name at a DIFFERENT position', False)
    run(_CALL % drop('J. Coleman', 'RB'), 'an abbreviated name: a stated limit of the name join, quiet', False)
    run(_CALL % drop('Samaje Perine', 'RB') + _FULL,
        'the parked man in the FULL drop table below, marked, which is where he belongs', False)
    run(_CALL % '&mdash;', 'an add that takes the open seat, no drop named', False)
    run(_CHEAP % ('Samaje Perine', 'Samaje Perine', 'CIN'), 'the cheapest table names a bench man', False)
    run('<p>The cheapest man you own is <b>Samaje Perine</b>, at <b>0.0</b></p>',
        'the cost line names a bench man', False)
    run(_CALL % drop('Jonah Coleman', 'RB'), 'nobody parked at all: the rule has nothing to say', False,
        roster=_ROSTER.replace('-102.9,21,INJURY_RESERVE', '-102.9,20,ACTIVE').replace('131.3,21,OUT', '131.3,4,ACTIVE'))

    print('P3 -- the open job the wire marks must be named on the sheet (doc 451)')
    _WIRE_OPEN = ('<table><tr><th>add him</th><th>tm</th><th>because this man is</th><th>status</th></tr>'
                  '<tr><td class="p">Ollie Gordon II</td><td class="t">MIA</td><td class="n">De\'Von Achane</td>'
                  '<td class="n"><b>Injury Reserve</b> &middot; the job is open, see THE CALL</td><td class="r">261</td></tr>'
                  '<tr><td class="p">Isaiah Davis</td><td class="t">NYJ</td><td class="n">Breece Hall</td>'
                  '<td class="n"><b>Questionable</b></td><td class="r">248</td></tr></table>')
    _WIRE_QUIET = _WIRE_OPEN.replace(' &middot; the job is open, see THE CALL', '')

    def run3(wire_html, sheet_html, note, want):
        got = open_jobs_on_sheet(wire_html, sheet_html)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    def band(inner, after=''):
        return ('<h2 class="bh" id="s0">Week 4 &mdash; what to do</h2>' + inner
                + '<h3 class="sub0" id="byes">Bye weeks</h3>' + after)

    run3(_WIRE_OPEN, band(_CALL % drop('Samaje Perine', 'RB')),
         'doc 451: the wire marks Gordon open, the sheet never names him', True)
    run3(_WIRE_OPEN, band(_CALL % drop('Samaje Perine', 'RB') + '<p class="ctx">Ollie Gordon II is claimed</p>'),
         'the sheet names him: quiet', False)
    run3(_WIRE_OPEN, band('<p class="ctx fine">Open jobs not priced here: <b>Ollie Gordon</b> (MIA)</p>'),
         'named only in the not-priced line, without the suffix: quiet', False)
    run3(_WIRE_OPEN, band('<p class="ctx fine">Open jobs below the cut, priced the same way: <b>Ollie Gordon II</b> (MIA, 2.3 over 1 week)</p>'),
         'named only in the below-the-cut line: quiet', False)
    run3(_WIRE_OPEN, band(_CALL % drop('Samaje Perine', 'RB'),
                          after='<h2 id="seats">The seat list</h2><details><summary>Left off: 1</summary>'
                                '<b>Ollie Gordon II</b> (below the ten-row cap)</details>'),
         '30 Sept: named only in the seat lane\'s left-off line, past the calendar: FIRES', True)
    run3(_WIRE_OPEN, _CALL % drop('Samaje Perine', 'RB') + '<p class="ctx">Ollie Gordon II is claimed</p>',
         'a sheet with no band-0 anchors cannot be checked: FIRES', True)
    run3(_WIRE_QUIET, band(_CALL % drop('Samaje Perine', 'RB')),
         'the lane carries Questionable rows only, no open job: quiet', False)
    run3('<p>no doubt lane at all</p>', band(_CALL % drop('Samaje Perine', 'RB')), 'no lane on the wire: quiet', False)

    print('P4 -- every one of ESPN\'s most-added free men has an answer in the crowd table (30 Sept)')
    _ADDED = [('Ollie Gordon II', 48.4), ('Jaylen Wright', 9.7)]
    _CROWD = ('<h3 class="sub0" id="crowd">The crowd</h3><table class="crowd"><tr><td class="p"><b>Ollie Gordon II</b></td>'
              '<td class="n">THE CALL, row 1</td></tr>%s</table>')

    def run4(added, sheet_html, note, want):
        got = crowd_on_sheet(added, sheet_html)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run4(_ADDED, band(_CROWD % '<tr><td class="p"><b>Jaylen Wright</b></td><td class="n">he holds the MIA job</td></tr>'),
         'both most-added men answered in the table: quiet', False)
    run4(_ADDED, band(_CROWD % ''), '30 Sept: Wright is the third most-added man and not in the table: FIRES', True)
    run4(_ADDED, band(_CROWD % '', after='<p>Jaylen Wright is named down here, past the calendar</p>'),
         'named only past the calendar: FIRES', True)
    run4(_ADDED, band(_CALL % drop('Samaje Perine', 'RB')), 'men qualify and there is no crowd table at all: FIRES', True)
    run4([], band(_CALL % drop('Samaje Perine', 'RB')), 'nobody over the bar this run: quiet', False)

    print('P5 -- THE CALL never drops a starter (doc 462)')
    _R5 = _ROSTER + ('2026-10-01,4430027,Sam LaPorta,TE,DET,6,9.1,6,ACTIVE\n2026-10-01,4569559,Devaughn Vele,WR,NO,8,-64.5,23,ACTIVE\n'
                     '2026-10-01,2973405,Kalif Raymond,WR,CHI,10,-125.2,20,ACTIVE\n')
    run(_CALL % drop('Sam LaPorta', 'TE'), 'doc 462: "take Pat Bryant, drop Sam LaPorta" (the only TE): FIRES', True, roster=_R5)
    run(_CALL % drop('Devaughn Vele', 'WR'), 'Vele, parked in the FLEX slot by a stale lineup, lowest WR by value: quiet', False, roster=_R5)
    run(_CALL % drop('Davante Adams', 'WR'), 'the top receiver by value as the drop: FIRES', True, roster=_R5)
    run(_CALL % drop('Packers D/ST', 'D/ST'), 'a starting defense as the drop: exempt, quiet', False,
        roster=_R5 + '2026-10-01,-16009,Packers D/ST,,,,,16,ACTIVE\n')

    print('P6 -- the long-shot lane: free men, no third string, above the seats only when behind (doc 461)')
    _LANE = ('<h2 id="tickets">The long shots</h2><table><tr><th>the man</th><th>his shape</th></tr>%s</table>'
             '<h2 id="seats">The seat list</h2>')
    _LROW = '<tr><th scope="row"><span class="pl">%s</span><span class="meta">SEA</span></th><td><span class="pl">%s</span></td></tr>'
    _SLOTS = {norm_name('Sam LaPorta'): 6, norm_name('Devaughn Vele'): 20}

    def run6(html_text, slots, pf, note, want):
        got = lane_checks(html_text, slots, pf)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run6(_LANE % (_LROW % ('Emanuel Wilson', 'committee partner')), _SLOTS, (9, 12), 'a free committee partner, behind in points, lane first: quiet', False)
    run6(_LANE % (_LROW % ('Devaughn Vele', 'committee partner')), _SLOTS, (9, 12), 'a man on your own roster on the lane: FIRES', True)
    run6(_LANE % (_LROW % ('Tyler Badie', 'third string or lower')), _SLOTS, (9, 12), 'a third-string shape on the lane: FIRES', True)
    run6(_LANE % (_LROW % ('Emanuel Wilson', 'committee partner')), _SLOTS, (3, 12), 'lane leads while you are 3rd in points: FIRES', True)
    run6('<h2 id="seats">The seat list</h2>' + (_LANE % '').replace('<h2 id="seats">The seat list</h2>', ''), _SLOTS, (3, 12),
         'lane follows the seats while 3rd in points: quiet', False)
    run6('<p>no lane</p>', _SLOTS, (9, 12), 'no lane on the page: nothing to check, quiet', False)
    _ODDS = '<p>where you stand: <b>%d%%</b> to make the top six, simulated on the weeks left</p>'
    run6((_ODDS % 39) + (_LANE % (_LROW % ('Emanuel Wilson', 'committee partner'))), _SLOTS, (9, 12),
         'lane leads at 39% to make the top six, 9th in points: FIRES (doc 469: the odds decide)', True)
    run6((_ODDS % 22) + (_LANE % (_LROW % ('Emanuel Wilson', 'committee partner'))), _SLOTS, (3, 12),
         'lane leads at 22% to make the top six, 3rd in points: quiet (the odds decide)', False)

    print('P7 -- the waterfall says what the files say (doc 462)')
    _WF = ('<details class="leftoff"><summary>How to place them</summary><p>You are <b>%s of 12</b> on waivers this week.</p>'
           '<ol><li><b>CLAIM %s</b>, drop Devaughn Vele</li><li><b>ADD %s now</b>, drop Malik Washington</li></ol>'
           '<p>the same drop, <b>%s</b>, on every claim</p></details>')
    _AV = {norm_name('Emanuel Wilson'): 'WAIVERS', norm_name('Pat Bryant'): 'FREEAGENT'}

    def run7(html_text, note, want, slots=_SLOTS, avail=_AV, wrank=11):
        got = waterfall_checks(html_text, slots, avail, wrank, {norm_name('Sam LaPorta')})
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    _ST = {norm_name('Sam LaPorta')}
    run7(_WF % (11, 'Emanuel Wilson', 'Pat Bryant', 'Devaughn Vele'), 'rank, CLAIM, ADD and hedge all agree with the files: quiet', False)
    run7(_WF % (8, 'Emanuel Wilson', 'Pat Bryant', 'Devaughn Vele'), 'the page prints rank 8 against 11 in the file: FIRES', True)
    run7(_WF % (11, 'Pat Bryant', 'Emanuel Wilson', 'Devaughn Vele'), 'CLAIM on a free agent and ADD on a waiver man: FIRES', True)
    run7(_WF % (11, 'Emanuel Wilson', 'Pat Bryant', 'Sam LaPorta'), 'the hedge man is a starter by value: FIRES', True)
    run7(_WF % (11, 'Emanuel Wilson', 'Pat Bryant', 'Jonah Coleman'), 'the hedge man sits in the IR slot: FIRES', True,
         slots={norm_name('Jonah Coleman'): 21})
    run7('<p>no waterfall</p>', 'no waterfall on the page: quiet', False)
    _CARD = ('<details class="leftoff" open><summary>How to place them</summary><p>You are <b>11 of 12</b> on waivers this week.</p>'
             '<table class="pend"><tr><td>now</td><td><b>Add %s now</b>, LAC WR, a free agent<br>drop Devaughn Vele</td></tr>'
             '<tr><td>1</td><td><b>Conditionally add %s</b>, PHI RB from Waivers<br>Conditionally drop AJ Barner</td></tr></table>'
             '<p>the same drop, <b>Devaughn Vele</b>, on every claim</p></details>')
    run7(_CARD % ('Pat Bryant', 'Emanuel Wilson'), 'the card (doc 469): free agent as Add now, waiver man as Conditionally add: quiet', False)
    run7(_CARD % ('Emanuel Wilson', 'Pat Bryant'), 'the card with the two men swapped: FIRES twice', True)

    print('P10 -- THE CALL\'s net is worth minus the cost, a negative cost at zero (doc 416, doc 469)')
    _NET = ('<h3 class="sub0">The call</h3><div class="scroll"><table><thead><tr><th scope="col">take</th><th scope="col">he is worth</th>'
            '<th scope="col">you would drop</th><th scope="col">that costs</th><th scope="col">net</th><th scope="col">when</th></tr></thead><tbody>'
            '<tr><th scope="row">Tre Harris<span class="meta">WR &middot; LAC</span></th><td class="tot pos">+5.3</td><td>Pat Bryant<span class="meta">WR</span></td>'
            '<td class="tot">%s<span class="meta">below replacement</span></td><td class="tot pos">%s</td><td class="meta">this week</td></tr></tbody></table></div>')

    def run10(html_text, note, want):
        got = net_checks(html_text)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run10(_NET % ('-2.4', '+5.3'), 'a negative cost counted as zero, net equals worth: quiet', False)
    run10(_NET % ('-2.4', '+7.7'), 'the mutated engine: a negative cost added to the net: FIRES', True)
    run10(_NET % ('2.5', '+2.8'), 'a positive cost subtracted: quiet', False)
    run10(_NET % ('2.5', '+5.3'), 'a positive cost ignored: FIRES', True)

    print('P8 -- a defense or kicker on the picks list is a hole fill, never a season rate (doc 467)')
    _PK = ('<h3 class="sub0">Priority pickups, in order</h3>'
           '<div class="mv big"><p class="act"><span class="rank">1</span><b class="nm" title="%s">%s</b>'
           '<span class="mmeta">%s &middot; KC &middot; 40%% rostered</span><span class="pill">7.8<em>points</em></span></p>'
           '<p class="ctx">%s</p></div>'
           '<div class="mv"><p class="act"><span class="rank">2</span><b class="nm" title="Pat Bryant">Pat Bryant</b>'
           '<span class="mmeta">WR &middot; DEN &middot; 3%% rostered</span><span class="pill">6.3<em>points</em></span></p>'
           '<p class="ctx">Outscores your receiver in 6 weeks. Hold him for those weeks.</p></div>'
           '<h3 class="sub0" id="byes">Bye weeks</h3>')

    def run8(html_text, note, want):
        got = weekly_in_picks(html_text)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run8(_PK % ('Chiefs D/ST', 'Chiefs D/ST', 'D/ST', 'Outscores your defense in 10 weeks. Hold him for those weeks.'),
         'the 1 Oct page: Chiefs D/ST on a season rate, first pick: FIRES', True)
    run8(_PK % ('Harrison Mevis', 'Harrison Mevis', 'K', 'No kicker in week 8; he fills it. Hold him for week 8 and let him go.'),
         'a kicker filling a bye hole: quiet', False)
    run8(_PK % ('Tre Harris', 'Tre&#x27; Harris', 'WR', 'Outscores your receiver in 6 weeks. Hold him for those weeks.'),
         'a receiver on a season rate, which is his currency: quiet', False)
    run8('<p>no picks list</p>', 'no picks list on the page: quiet', False)
    _CK = ('<h3 class="sub0">The call</h3><div class="scroll"><table><thead><tr><th scope="col">take</th><th scope="col">he is worth</th>'
           '<th scope="col">you would drop</th><th scope="col">that costs</th><th scope="col">net</th><th scope="col">when</th></tr></thead><tbody>'
           '<tr><th scope="row">Harrison Mevis<span class="meta">K &middot; LAR</span><span class="meta">%s</span></th>'
           '<td class="tot pos">+9.0</td><td>Pat Bryant<span class="meta">WR</span></td><td class="tot">0.0</td><td class="tot pos">+9.0</td>'
           '<td class="meta">week 8</td></tr></tbody></table></div>')

    def run8b(html_text, note, want):
        got = weekly_in_call(html_text)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run8b(_CK % 'fills the kicker hole in week 8, priced on that week alone', 'a kicker on THE CALL as a hole fill: quiet', False)
    run8b(_CK % '9.0 proj, priced at 9.0 a week', 'a kicker on THE CALL on a season rate (doc 424): FIRES', True)

    print('P9 -- a projected rate is the file over the games left (doc 419, doc 467)')
    _GRID = ('<table><thead><tr><th class="corner" scope="col">player</th><th class="rate" scope="col">pts/wk</th>'
             '<th scope="col">4</th><th scope="col">5</th><th class="tot" scope="col">season</th></tr></thead><tbody>'
             '<tr><th scope="row"><span class="pl" title="Chiefs D/ST">Chiefs D/ST</span><span class="meta">KC &middot; bye 5 &middot; </span></th>'
             '<td class="rate" data-vintage="%s" title="x">%s</td><td class="ok">+0.6</td><td class="bye">bye</td><td class="tot">6.5</td></tr>'
             '</tbody></table>')
    _PJ = {('Chiefs D/ST', 'KC'): 91.0}       # 91 over the 14 games left at week 4 is 6.5; over 17 it is 5.4

    def run9(html_text, proj, note, want):
        got = rate_divisor_checks(html_text, proj)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run9(_GRID % ('proj', '6.5'), _PJ, 'the file over the 14 games left at week 4: quiet', False)
    run9(_GRID % ('proj', '5.4'), _PJ, 'the same total over 17 (doc 419): FIRES', True)
    run9(_GRID % ('blend', '5.4'), _PJ, 'a blended rate, which is not the projection: quiet', False)
    run9(_GRID % ('proj', '5.4'), None, 'no projection file in Source: FAILS', True)

    print('P11 -- the matchup number beside the rate is the files\' own arithmetic, RB and TE only (doc 468)')
    import tempfile
    _td = tempfile.mkdtemp()
    with open(os.path.join(_td, 'sched_2026.csv'), 'w', newline='') as fh:
        fh.write('week,team,opp,side\n')
        for w in (1, 2, 3, 4):
            fh.write('%d,AAA,BBB,home\n%d,BBB,AAA,away\n%d,CCC,DDD,home\n%d,DDD,CCC,away\n' % (w, w, w, w))
        fh.write('5,AAA,DDD,home\n5,DDD,AAA,away\n5,BBB,CCC,home\n5,CCC,BBB,away\n')
    with open(os.path.join(_td, 'form_2026.csv'), 'w', newline='') as fh:
        fh.write('week,player,pos,team,half_ppr,in_progress\n')
        for w in (1, 2, 3, 4):
            # BBB allows 20 a week to backs, DDD allows 10, AAA 30 and CCC 0: the league mean is 15
            fh.write('%d,Aback,RB,AAA,20,0\n%d,Bback,RB,BBB,30,0\n%d,Cback,RB,CCC,10,0\n%d,Dback,RB,DDD,0,0\n' % (w, w, w, w))
    # Aback (AAA) plays DDD in week 5: DDD allows 10, mean 15, so 0.10 x (10 - 15) = -0.5
    _RT = ('<h2 id="s0"><span class="n">0</span>Week 5 &mdash; what to do</h2>'
           '<h2 id="s5"><span class="n">5</span>Your roster</h2><div class="scroll"><table><thead><tr><th>player</th></tr></thead><tbody>'
           '<tr><th scope="row"><span class="pl" title="Aback">Aback</span><span class="meta">%s &middot; AAA</span></th>'
           '<td>9.0 blend%s</td><td>7</td></tr></tbody></table></div>')

    def run11(html_text, note, want):
        got = matchup_checks(html_text, _td)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run11(_RT % ('RB', ' <span class="meta">&middot; matchup vs DDD &minus;0.5</span>'), 'a back printing the files\' number: quiet', False)
    run11(_RT % ('RB', ' <span class="meta">&middot; matchup vs DDD +0.5</span>'), 'the sign flipped: FIRES', True)
    run11(_RT % ('WR', ' <span class="meta">&middot; matchup vs DDD &minus;0.5</span>'), 'a receiver with a matchup number: FIRES', True)
    run11(_RT % ('RB', ''), 'a roster back with a priced opponent and no number: FIRES', True)
    shutil.rmtree(_td, ignore_errors=True)

    print('P12 and P13 -- a second tight end is not on THE CALL this week; the total counts this week\'s rows only (doc 457)')
    _td2 = tempfile.mkdtemp()
    with open(os.path.join(_td2, 'form_2026.csv'), 'w', newline='') as fh:
        fh.write('week,player,pos,team,targets,in_progress\n')
        fh.write('3,Brock Bowers,TE,LV,13,0\n3,Michael Mayer,TE,LV,3,0\n3,Mike Gesicki,TE,CIN,9,0\n')
    _CALLT = ('<h3 class="sub0">The call</h3><div class="scroll"><table><thead><tr><th class="corner" scope="col">take</th>'
              '<th class="tot" scope="col">he is worth</th><th scope="col">you would drop</th><th class="tot" scope="col">that costs</th>'
              '<th class="tot" scope="col">net</th><th scope="col">when</th></tr></thead><tbody>%s</tbody></table></div>'
              '<p class="sub">Taking %s nets <b>%s</b>.</p>')
    _R = ('<tr><th scope="row">%s<span class="meta">TE &middot; %s &middot; 9%% rostered</span><span class="meta">%s</span></th>'
          '<td class="tot pos">+%s</td><td>Pat Bryant<span class="meta">WR</span></td><td class="tot">0.0</td>'
          '<td class="tot pos">+%s</td><td class="meta">%s</td></tr>')

    def run12(html_text, note, want):
        got = te_leader_checks(html_text, _td2)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    def run13(html_text, note, want):
        got = total_checks(html_text)
        ok = (len(got) > 0) == want
        print('  %-4s %-66s fired=%d expected=%s' % ('ok' if ok else 'BAD', note, len(got), want))
        if not ok:
            fails.append((note, got))

    run12(_CALLT % (_R % ('Mike Gesicki', 'CIN', '12.9 this season (3 g)', '9.1', '9.1', 'this week'), 'it', '+9.1'),
          'the team\'s own leader on THE CALL: quiet', False)
    run12(_CALLT % (_R % ('Michael Mayer', 'LV', '7.1 this season (3 g)', '4.0', '4.0', 'this week'), 'it', '+4.0'),
          'Mayer behind Bowers 13 to 3, this week (doc 457): FIRES', True)
    run12(_CALLT % (_R % ('Michael Mayer', 'LV', 'fills the tight end hole in week 6', '4.0', '4.0', 'week 5'), 'it', '+4.0'),
          'the same man as a calendar claim for the hole: quiet', False)
    run13(_CALLT % (_R % ('Mike Gesicki', 'CIN', 'x', '9.1', '9.1', 'this week') + _R % ('Michael Mayer', 'LV', 'x', '4.0', '4.0', 'week 5'),
                    'it this week', '+9.1'), 'the total counts the this-week row only: quiet', False)
    run13(_CALLT % (_R % ('Mike Gesicki', 'CIN', 'x', '9.1', '9.1', 'this week') + _R % ('Michael Mayer', 'LV', 'x', '4.0', '4.0', 'week 5'),
                    'both', '+13.1'), 'the total counts the week-5 row (doc 457): FIRES', True)
    shutil.rmtree(_td2, ignore_errors=True)

    n = 29 + 4 + 8 + 8 + 4 + 4 + 4 + 2 + 4 + 5
    if fails:
        print('\nSELFTEST FAILED: %d of %d control(s) behaved wrongly' % (len(fails), n))
        return 1
    print('\nselftest: %d/%d controls behaved as specified' % (n, n))
    return 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    sheet = os.path.join(SRC, 'WEEK_SHEET.html')
    roster = os.path.join(SRC, 'MY_ROSTER.csv')
    print('check_page_logic: the week sheet against the league\'s rules, independent of the engine')
    parked = parked_men(roster)
    if parked:
        print('  in the IR slot today: %s' % ', '.join(p[2] for p in parked))
    else:
        print('  nobody in the IR slot today (or no roster file), so P1 and P2 have nothing to check')
    bad = check(sheet, roster)
    bad += check_open_jobs(os.path.join(SRC, 'THE_WEEKLY_WIRE.html'), sheet)     # P3, doc 451
    added = most_added(SRC)
    if added:
        print('  ESPN\'s most-added free men today: %s' % ', '.join('%s %+.1f' % t for t in added))
    else:
        print('  nobody free has moved a full point on ESPN\'s +/- yet, so P4 has nothing to check')
    bad += check_crowd(SRC, sheet)                                                # P4, 30 Sept
    if os.path.exists(sheet):
        with open(sheet, encoding='utf-8', errors='replace') as fh:
            _text_all = fh.read()
        _slots = roster_slots(roster)
        bad += lane_checks(_text_all, _slots, pf_rank_of_mine(SRC))                 # P6, doc 461
        bad += odds_checks(_text_all, SRC)                                             # P6b, doc 469
        bad += waterfall_checks(_text_all, _slots, wire_avail(SRC), my_waiver_rank(SRC),
                                roster_starters(roster))                               # P7, doc 462
        bad += weekly_in_picks(_text_all)                                              # P8, doc 467
        bad += weekly_in_call(_text_all)                                               # P8b, doc 470
        bad += rate_divisor_checks(_text_all, load_proj(SRC))                          # P9, doc 467
        bad += matchup_checks(_text_all, SRC)                                          # P11, doc 472
        bad += te_leader_checks(_text_all, SRC)                                        # P12, doc 473
        bad += total_checks(_text_all)                                                 # P13, doc 473
    if bad:
        print('  FAIL  %s -- %d' % (os.path.relpath(sheet, ROOT), len(bad)))
        for chk, detail in bad:
            print('          %s' % chk)
            print('                      %s' % detail[:150])
        print('\n%d problem(s). THE PAGE OFFERS A MAN IN THE INJURED-RESERVE SLOT AS A DROP, OR LEAVES AN' % len(bad))
        print('OPEN JOB THE WIRE NAMES OFF THE SHEET, OR LEAVES ONE OF ESPN\'S MOST-ADDED MEN UNANSWERED. A parked')
        print('man holds none of the fifteen (doc 436); an open job is a claim this week (doc 451); the crowd table')
        print('answers every man the crowd is adding. Fix the builder, not the page -- it is rebuilt every run.')
        return 1
    print('  ok    %s' % os.path.relpath(sheet, ROOT))
    print('\nno problems. No man in the IR slot or a starting slot is offered as a drop, every open job the wire marks is on the sheet, every man the crowd is adding has an answer, the long shots are free men in a measured shape, and the waterfall says what the files say.')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
