#!/usr/bin/env python3
r"""
redteam_controls.py -- the negative controls behind the in-season pages (doc 291, catalog A16).

WHY IT EXISTS. A guard shown firing on one input and trusted on the rest is not a guard. On 11 Sept
the team-code assert had been shown firing on ARZ while Washington fell off both pages through a
join it never saw. This file breaks ONE input at a time, rebuilds both pages against a RECORDED
player pool (no ESPN call, no cookies), and checks what the pages say. Every control here was run
against the pre-291 code first and failed there, so a pass means something.

WHAT IT NEEDS, and nothing else is read:
  Scripts\wire.py, Scripts\sheet_engine.py, Scripts\depth_map.csv,
  Scripts\live_draft\board_v8_fixed.csv, Scripts\live_draft\player_context.csv,
  the eleven Source inputs in PAGE_INPUTS below, and the two frozen files beside this script:
  WIRE_20260910.csv (the free pool on 10 Sept) and MY_ROSTER_20260911.csv (his roster on 11 Sept).

RUN:   py research\redteam\redteam_controls.py                 (the tree this file sits in)
       py research\redteam\redteam_controls.py --root "D:\copy\2026"   (another tree, e.g. old code)
Writes nothing into the real tree: every control runs in a temporary folder that is deleted after.
Stdlib only. Exit 0 only when every check passes.
Added 11 Sept, doc 292: C16, the off-board free players file (FREE_UNRANKED_<date>.csv), with a
planted undrafted back the board has never rated (MOCK_EXTRA), and a player sent with no ownership
number, off the board and on it (MOCK_NO_OWN). The 291 code died on the second: a latent crash of the
whole run. Those two checks run last, because a dead child process stops the harness.
Added 12 Sept, doc 296: C17, the man who inherits must be a man who is PLAYING -- with
Jordan James (OUT in ESPN's own 11 Sept pool) planted at SF, where the shipped code named
him and the fixed code names Kaelon Black and says whom it stepped over.
"""
import csv, html, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PULL = 'espn_projections_2026_20260907_1258.csv'
PAGE_INPUTS = ['byes_2026.csv', 'cards_2026.csv', PULL, 'form_2026.csv', 'inherit_2026.csv',
               'pedigree_2026.csv', 'pos_allowed_2025.csv', 'redzone_te_2025.csv', 'sched_2026.csv',
               'sheet_constants.json', 'team_2025.csv', 'team_shape_2025.csv']
# form_2026.csv JOINED PAGE_INPUTS ON 16 SEPT (doc 321) and it is the point of C21. Until then the
# harness ran with no form file at all, so every check passed on a page whose workload lane was
# switched off -- which is exactly how the `touches` column could vanish out of wire.py and out of
# WIRE_20260915.csv without one control failing. A control tree that omits an input cannot see a
# defect in the code that reads it.
SCRIPT_INPUTS = ['wire.py', 'sheet_engine.py', 'depth_map.csv',
                 os.path.join('live_draft', 'board_v8_fixed.csv'),
                 os.path.join('live_draft', 'player_context.csv')]
CARD = 'Omar Cooper Jr. WR · NYJ · the screen'          # how a card's header reads on the sheet


# ---------------------------------------------------------------------------------------------
# THE MOCK: wire.main() against a recorded pool. Runs in a child process: --mock <tree>
# ---------------------------------------------------------------------------------------------
def mock(root):
    scripts, src = os.path.join(root, 'Scripts'), os.path.join(root, 'Source')
    sys.path.insert(0, scripts)
    os.chdir(scripts)
    import wire
    posid = {'QB': 1, 'RB': 2, 'WR': 3, 'TE': 4, 'K': 5, 'D/ST': 16}
    proid = {v: k for k, v in wire.PRO.items()}
    proid.setdefault('WAS', 28); proid.setdefault('WSH', 28); proid.setdefault('LA', 14)
    status = {'4428209': 'INJURY_RESERVE', '4430834': 'QUESTIONABLE'}   # Pearsall IR, McMillan Q
    status.update(json.loads(os.environ.get('MOCK_STATUS', '{}')))
    drop = set(filter(None, os.environ.get('MOCK_DROP', '').split(',')))
    no_own = set(filter(None, os.environ.get('MOCK_NO_OWN', '').split(',')))   # ids sent with no ownership number
    with open(os.path.join(src, 'MY_ROSTER.csv'), encoding='utf-8-sig') as fh:
        mine = {r['espn_id']: r['player'] for r in csv.DictReader(fh)}
    with open(os.path.join(src, PULL), encoding='utf-8-sig') as fh:
        pull = {str(r['espn_id']).strip(): r for r in csv.DictReader(fh)}

    def entry(pid, name, pos, team, owned=0.0, st='ACTIVE'):
        return {'player': {'id': int(pid), 'fullName': name, 'defaultPositionId': posid.get(pos, 0),
                           'proTeamId': proid.get((team or '').upper(), 0), 'injuryStatus': st,
                           'ownership': {'percentOwned': float(owned or 0)}}}
    players, seen = [], set()
    with open(os.path.join(src, 'WIRE_20260910.csv'), encoding='utf-8-sig') as fh:
        for r in csv.DictReader(fh):
            pid = r['espn_id'].strip()
            seen.add(pid)
            if pid not in drop:
                players.append(entry(pid, r['player'], r['pos'], r['team'], r['owned_pct'],
                                     status.get(pid, 'ACTIVE')))
                if pid in no_own:
                    players[-1]['player']['ownership'] = {'percentOwned': None}
    # a player the board has never rated, planted on request (C16): [id, name, pos, team, owned, status]
    for pid, name, pos, team, owned, st in json.loads(os.environ.get('MOCK_EXTRA', '[]')):
        players.append(entry(str(pid), name, pos, team, owned, st))
        if owned is None:                        # ESPN sending no ownership number at all
            players[-1]['player']['ownership'] = {'percentOwned': None}
        seen.add(str(pid))
    # the recorded pool has no kickers or defences, so every one he does not own is treated as free:
    # the generous direction for any "would it have shown" question about K and D/ST
    for pid, r in pull.items():
        if r.get('pos') in ('K', 'D/ST') and pid not in mine and pid not in seen:
            players.append(entry(pid, r.get('player') or r.get('Player'), r['pos'], r.get('team')))
    roster = [{'playerPoolEntry': {'player': {
        'id': int(pid), 'fullName': nm, 'injuryStatus': 'ACTIVE',
        'defaultPositionId': posid.get(pull.get(pid, {}).get('pos'), 0),
        'proTeamId': proid.get((pull.get(pid, {}).get('team') or '').upper(), 0)}}}
        for pid, nm in mine.items()]

    def fake_get(view, xfilter=None):
        if view == 'kona_player_info':
            return {'players': players}
        if view == 'mRoster':
            return {'scoringPeriodId': int(os.environ.get('MOCK_WEEK', '2')),
                    'teams': [{'id': wire.MY_TEAM_ID, 'roster': {'entries': roster}}]}
        raise RuntimeError('unexpected view ' + view)
    wire._get = fake_get
    wire.fetch_schedule = lambda: None
    rc = wire.main(['--html'])
    print('HARNESS FINISHED exit', rc, '| pool', len(players))
    return 0


def page_text(path):
    if not os.path.exists(path):
        return None
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'(?s)<style.*?</style>', ' ', s)
    s = re.sub(r'<(br|/p|/div|/h[1-6]|/li|/tr|/table|/article|h[1-6][^>]*)>', '\n', s)
    s = re.sub(r'</t[dh]>', ' | ', s)
    s = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    return '\n'.join(l for l in (re.sub(r'\s+', ' ', x).strip() for x in s.split('\n')) if l)


# ---------------------------------------------------------------------------------------------
# THE CONTROLS
# ---------------------------------------------------------------------------------------------
def page_section(txt, heading, ends):
    """The plain text of ONE section of a page: from `heading` to whichever of `ends` comes first.
    Returns '' when the heading is missing OR when no end marker is found -- an UNBOUNDED section is
    the whole rest of the page, and the first version of this returned exactly that, so C23 passed
    against the very code it was written to fail (Kaelon Black sits in the seat table further down).
    A helper that cannot bound its own section must report nothing, never everything."""
    if not txt:
        return ''
    i = txt.find(heading)
    if i < 0:
        return ''
    cuts = [txt.find(e, i + len(heading)) for e in ends]
    cuts = [c for c in cuts if c > 0]
    return txt[i:min(cuts)] if cuts else ''


def ranked_names(sec):
    """The pickup rows in the order the page prints them. Each row opens with its rank number and
    then the name, so the numbers are the only reliable separator once the tags are gone."""
    out = []
    for m in re.finditer(r'(?:^|\s)(\d{1,2})\s+([A-Z][^\d]{2,40}?)\s+(?:QB|RB|WR|TE|K|D/ST)\b', sec or ''):
        out.append(m.group(2).strip())
    return out


def rewrite_csv(path, fn):
    with open(path, newline='', encoding='utf-8-sig') as fh:
        rdr = csv.DictReader(fh)
        cols, rows = rdr.fieldnames, list(rdr)
    rows = fn(rows)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def recode(col, old, new, pred=None):
    def fn(rows):
        n = 0
        for r in rows:
            if r[col] == old and (pred is None or pred(r)):
                r[col] = new
                n += 1
        assert n, f'no {col}={old} rows to recode'
        return rows
    return fn


def build_tree(root, dst):
    for rel in SCRIPT_INPUTS:
        os.makedirs(os.path.dirname(os.path.join(dst, 'Scripts', rel)), exist_ok=True)
        shutil.copy2(os.path.join(root, 'Scripts', rel), os.path.join(dst, 'Scripts', rel))
    os.makedirs(os.path.join(dst, 'Source'), exist_ok=True)
    for name in PAGE_INPUTS:
        shutil.copy2(os.path.join(root, 'Source', name), os.path.join(dst, 'Source', name))
    shutil.copy2(os.path.join(HERE, 'WIRE_20260910.csv'), os.path.join(dst, 'Source', 'WIRE_20260910.csv'))
    shutil.copy2(os.path.join(HERE, 'MY_ROSTER_20260911.csv'), os.path.join(dst, 'Source', 'MY_ROSTER.csv'))


def main(argv):
    root = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
    if '--root' in argv:
        root = os.path.abspath(argv[argv.index('--root') + 1])
    work = tempfile.mkdtemp(prefix='redteam_')
    results = []

    def run(name, mutate=None, env=None):
        d = os.path.join(work, name)
        build_tree(root, d)
        if mutate:
            mutate(os.path.join(d, 'Source'))
        e = dict(os.environ)
        e.update(env or {})
        cp = subprocess.run([sys.executable, os.path.abspath(__file__), '--mock', d],
                            capture_output=True, text=True, env=e, encoding='utf-8', errors='replace')
        con = (cp.stdout or '') + (cp.stderr or '')
        if 'HARNESS FINISHED' not in con:        # an exit code is not a result
            raise SystemExit(f'HARNESS DID NOT FINISH on control {name}:\n' + con[-1500:])
        return dict(con=con, ws=page_text(os.path.join(d, 'Source', 'WEEK_SHEET.html')),
                    ww=page_text(os.path.join(d, 'Source', 'THE_WEEKLY_WIRE.html')), dir=d)

    def check(ctl, label, ok, detail=''):
        results.append((ctl, label, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}] {ctl}: {label}" + (f"  -- {str(detail)[:300]}" if detail and not ok else ''))

    try:
        b = run('c0_base')
        check('C0', 'sheet written', b['ws'] is not None, b['con'][-400:])
        check('C0', 'no team-code problem on the wire page', b['ww'] and 'match no team' not in b['ww'])
        check('C0', 'Pearsall (on IR) not on the sheet', b['ws'] and 'Pearsall' not in b['ws'])
        check('C0', "Cooper's card on the sheet", b['ws'] and CARD in b['ws'])

        r = run('c1_byes_bad', lambda s: rewrite_csv(os.path.join(s, 'byes_2026.csv'), recode('team', 'WAS', 'XXX')))
        check('C1', 'byes code that resolves to nothing: sheet refused', r['ws'] is None)
        check('C1', 'console names XXX', "unknown ['XXX']" in r['con'], r['con'][:600])
        check('C1', 'wire page says the sheet was not rebuilt', r['ww'] and 'week sheet was not rebuilt' in r['ww'])
        r = run('c1b_byes_alias')
        check('C1b', 'byes spelled WAS still resolve (alias)', r['ws'] is not None)
        r = run('c1c_pull_bad', lambda s: rewrite_csv(os.path.join(s, PULL), recode(
            'team', 'WSH', 'XXX', pred=lambda row: 'Commanders' in (row.get('player') or row.get('Player') or ''))))
        check('C1c', 'one pull row with a bad code: sheet refused', r['ws'] is None)
        check('C1c', 'console names XXX (1 players)', 'XXX (1 players)' in r['con'], r['con'][:600])

        for tag, fname, col in (('C2', 'team_2025.csv', 'team'), ('C3', 'sched_2026.csv', 'opp'),
                                ('C4', 'pos_allowed_2025.csv', 'team')):
            r = run(tag.lower(), lambda s, f=fname, c=col: rewrite_csv(os.path.join(s, f), recode(c, 'ARI', 'XXX')))
            check(tag, f'{fname}: wire page names XXX', r['ww'] and re.search(re.escape(fname) + r'.{0,60}XXX', r['ww']))
            check(tag, f'{fname}: console prints the problem', 'XXX' in r['con'])
        r = run('c5', lambda s: rewrite_csv(os.path.join(s, 'team_shape_2025.csv'), recode('team', 'ARZ', 'XXX')))
        check('C5', 'team_shape guard fires and shows on the wire page', r['ww'] and 'team_shape_2025.csv resolved' in r['ww'])

        r = run('c6', env={'MOCK_STATUS': json.dumps({'4428209': 'ACTIVE'})})
        check('C6', 'Pearsall shown when ESPN lists him active', r['ws'] and 'Pearsall' in r['ws'])

        def blank_bryant(s):
            def fn(rows):
                hit = [row for row in rows if str(row['espn_id']).strip() == '4600981']
                assert len(hit) == 1
                hit[0]['proj_2026'] = ''
                return rows
            rewrite_csv(os.path.join(s, PULL), fn)
        r = run('c7', blank_bryant)
        check('C7', 'Bryant (active, no projection) named in the missing-row box',
              r['ws'] and re.search(r'NOT priced above.{0,400}Pat Bryant', r['ws'], re.S))
        r = run('c7b', blank_bryant, env={'MOCK_STATUS': json.dumps({'4600981': 'OUT'})})
        check('C7b', 'Bryant (OUT, no projection) left to ESPN',
              r['ws'] and not re.search(r'NOT priced above.{0,400}Pat Bryant', r['ws'], re.S))

        r = run('c8', env={'MOCK_DROP': '4723820'})
        check('C8', "a claimed carded player's card is off the sheet", r['ws'] is not None and CARD not in r['ws'])
        check('C8', 'the console names him', 'Cooper' in r['con'])

        def blank_card_id(s):
            def fn(rows):
                hit = [row for row in rows if row['player'] == 'Omar Cooper Jr.']
                assert len(hit) == 1
                hit[0]['espn_id'] = ''
                hit[0]['tm'] = ' nyj'
                return rows
            rewrite_csv(os.path.join(s, 'cards_2026.csv'), fn)
        r = run('c9', blank_card_id)
        check('C9', 'a card with a blank id and a messy team code still shows', r['ws'] and CARD in r['ws'])

        runs = re.findall(r'^    (\S.*?D/ST)\s+\S+\s+wks \S+\s+(.*?)who score', b['con'], re.M)
        order = [(n.strip(), 'bye' in o) for n, o in runs]
        check('C10', 'the defence run renders (week read from the roster payload)', len(order) >= 3)
        first = next((i for i, (_, hb) in enumerate(order) if hb), None)
        check('C10', 'no run without a bye sits below a run with one', first is None or all(hb for _, hb in order[first:]))
        check('C11', 'a single tight-end bye reads as one pickup, not a trade',
              b['ww'] and 'one empty TE slot' in b['ww'] and 'The trade that is sitting there' not in b['ww'])
        r = run('c12', env={'MOCK_WEEK': '7'})
        check('C12', 'week 11 (three starters, two positions) keeps the trade headline',
              r['ww'] and 'The trade that is sitting there' in r['ww'] and 'Week 11 is 4 weeks away' in r['ww'])

        pat = r'Mike Washington Jr\. RB · LV · priced as the handcuff to ([^|]+?) \| ([\d.]+)'
        base_w = re.search(pat, b['ws'] or '')
        check('C13', 'Washington priced as the handcuff', base_w is not None)
        r = run('c13', lambda s: rewrite_csv(os.path.join(s, 'inherit_2026.csv'),
                                            recode('holds_the_job', 'Ashton Jeanty', 'Ashton Jeanty Jr.')))
        m = re.search(pat, r['ws'] or '')
        check('C13', "holder spelled 'Ashton Jeanty Jr.': same handcuff price", m and base_w and m.group(2) == base_w.group(2))
        r = run('c14', lambda s: rewrite_csv(os.path.join(s, 'inherit_2026.csv'), recode('next_man_id', '4686658', '4686659')))
        m = re.search(pat, r['ws'] or '')
        check('C14', 'wrong next_man_id: same handcuff price', m and base_w and m.group(2) == base_w.group(2))
        check('C14', 'console names the id that matches nobody', '4686659' in r['con'])
        r = run('c15', lambda s: rewrite_csv(os.path.join(s, 'cards_2026.csv'), recode('espn_id', '4723820', '4723821')))
        check('C15', 'a card with a wrong id still shows', r['ws'] and CARD in r['ws'])
        check('C15', 'console names the id mismatch', '4723821' in r['con'])

        # C17 (doc 296): THE MAN WHO INHERITS MUST BE A MAN WHO IS PLAYING.
        # The live 11 Sept page named Jordan James as the back who would inherit McCaffrey's
        # 303-point job. ESPN's own pool had him OUT and he did not play in week 1; Kaelon Black,
        # one row deeper and ACTIVE, led the team in carries. Plant the same status and check the
        # page steps over him, names the healthy man, and SAYS why.
        def stash_block(txt):
            """Only the stash table. 'not in the whole page' is the wrong test: a man can appear
            legitimately in the free pool, and that is how a loose grep token closed a row it
            should not have (AUDIT_LEDGER row 13)."""
            if not txt:
                return ''
            i = txt.find('One injury away')
            if i < 0:
                return ''
            j = txt.find('In doubt', i)
            return txt[i:j if j > i else i + 2500]

        r = run('c17', env={'MOCK_STATUS': json.dumps({'4685397': 'OUT'})})
        blk = stash_block(r['ww'])
        check('C17', 'the stash block exists at all', bool(blk), (r['ww'] or '')[:300])
        # AND THE TEST ITSELF HAS TO BE TIGHT. The first version of this check was
        # "'Jordan James' not in blk" and it failed on the fixed code, because the fix PRINTS his
        # name in the reason. Read the first cell of each row, never the block. Same defect as
        # AUDIT_LEDGER row 13, on the same day, in the opposite direction.
        stash_names = [ln.split('|')[0].strip() for ln in blk.splitlines() if '|' in ln]
        check('C17', 'a back ESPN lists OUT is not named as the man who inherits',
              'Jordan James' not in stash_names, stash_names[:6])
        check('C17', 'the healthy man one row deeper is named instead', 'Kaelon Black' in blk, blk[:400])
        check('C17', 'and the page says whom it stepped over, and why',
              'ahead of him Jordan James (out)' in (r['ww'] or ''), blk[:400])
        # the same fix in the other lane: a cover who is himself OUT covers nothing
        check('C17', 'the base run still names somebody at SF', 'SF' in stash_block(b['ww']))

        # -----------------------------------------------------------------------------------
        # C18 / C19 (doc 320): THE USAGE ORDER NAMES THE INHERITOR, AND ONLY FROM WEEK THREE.
        # Doc 320 measured the cumulative carries-plus-targets order naming the man who actually
        # inherits 72.1% of the time against the preseason chart's 62.2% (n=111, McNemar p=0.043),
        # and the week-2 cell is a TIE on n=8. So the switch has two halves and both are tested:
        # it must fire at two completed weeks and must NOT fire at one.
        # THE FIXTURE IS INDIANAPOLIS, whose chart reads Taylor / Giddens / McGowan and whose job
        # is worth 291, high enough that the row is on the page. Planted usage puts McGowan second
        # and Giddens last, so the CHART names Giddens as the man who inherits and the USAGE ORDER
        # names McGowan. One name is the whole difference between the two arms.
        # NOTE doc 320's own draft control said "assert next_man_up() names the depth-3 man". It
        # cannot: a man who LEADS his team in touches becomes depth 1, and next_man_up filters to
        # depth >= 2. The object it measures is the INHERITOR, so the fixture makes him second.
        FORM_COLS = ['week', 'name_key', 'player', 'pos', 'team', 'snap_pct', 'targets', 'carries',
                     'tgt_share', 'car_share', 'touches', 'half_ppr', 'in_progress']
        IND = {'Jonathan Taylor': 25, 'DJ Giddens': 2, 'Seth McGowan': 14}

        def plant_form(weeks, override, last=None):
            """Rewrite the tree's real form_2026.csv to hold `weeks` completed weeks, with the
            named players' CUMULATIVE touches forced. The real file is the base, not a synthetic
            one: a planted file holding four rows would switch off every other lane on the page
            and the run would no longer be the object production builds (0.2, doc 80)."""
            def fn(src):
                path = os.path.join(src, 'form_2026.csv')
                with open(path, newline='', encoding='utf-8-sig') as fh:
                    rows = [r for r in csv.DictReader(fh)]
                cum = [r for r in rows if str(r.get('week')).strip() == '0']
                one = [r for r in rows if str(r.get('week')).strip() == '1']
                out = []
                for r in cum:
                    r = dict(r)
                    if r.get('player') in override:
                        r['touches'] = str(override[r['player']])
                    out.append(r)
                for w in range(1, weeks + 1):
                    for r in one:
                        r = dict(r)
                        r['week'] = str(w)
                        r['in_progress'] = '0'
                        if last and r.get('player') in last and w == weeks:
                            r['touches'] = str(last[r['player']])   # his LAST completed game only
                        out.append(r)
                with open(path, 'w', newline='', encoding='utf-8') as fh:
                    wr = csv.DictWriter(fh, fieldnames=FORM_COLS, lineterminator='\n',
                                        extrasaction='ignore')
                    wr.writeheader()
                    wr.writerows(out)
            return fn

        def inheritor(txt, tm):
            """The name in the stash row for one NFL team -- never a grep of the whole page."""
            for ln in stash_block(txt).splitlines():
                cells = [c.strip() for c in ln.split('|')]
                if len(cells) > 1 and tm in cells[1:3]:
                    return cells[0]
            return ''

        r = run('c19_one_week', plant_form(1, IND))
        check('C19', 'ONE completed week: the chart order stands and Giddens is the man who inherits',
              inheritor(r['ww'], 'IND') == 'DJ Giddens', stash_block(r['ww'])[:400])
        check('C19', 'and nothing announces a re-rank', 'depth re-ranked on usage' not in r['con'])
        r = run('c18_two_weeks', plant_form(2, IND))
        check('C18', 'TWO completed weeks: the usage order names McGowan instead',
              inheritor(r['ww'], 'IND') == 'Seth McGowan', stash_block(r['ww'])[:400])
        check('C18', 'the console says the re-rank ran and how many rows moved',
              'depth re-ranked on usage' in r['con'],
              [l for l in r['con'].splitlines() if 'depth' in l][:4])
        check('C18', 'the man ahead is still printed, not blanked by a team with no usage rows',
              (r['ww'] or '').count('behind') >= (b['ww'] or '').count('behind') - 2)

        # C20 (doc 319): THE WEEK-6 TIGHT-END FILL PRINTS BOTH WAYS.
        # The page's own price for a bye-week fill charges the empty slot at ZERO, which is what
        # put four tight ends within 0.6 of each other at 6.1 to 6.7 and made the choice among them
        # look like a decision. Against the man he would actually claim instead they are 1.2 to 2.0.
        # Structural, not a number: the sentence must carry the second figure on any certain fill
        # that exists only because a slot is empty.
        import re as _re
        # BOTH NUMBERS OUT OF ONE SENTENCE. The first version of this check asserted the second
        # figure was under 6, which is doc 319's TIGHT END and nothing else -- the first such row
        # on the base page is a DEFENCE at 19.6 and the control failed on correct output. A
        # hard-coded expectation from the example that motivated the change is not a test of it.
        both = _re.search(r'the whole of his ([0-9.]+)\. Against the ordinary [\w ]+ you could '
                          r'claim instead he is worth ([0-9.]+)', b['ws'] or '')
        check('C20', 'a bye-week fill prints what he is worth against a waiver body, not only against nobody',
              bool(both), 'no both-ways sentence on the base page')
        check('C20', 'and the second number is below the headline it qualifies, on the same row',
              bool(both) and float(both.group(2)) < float(both.group(1)), both.group(0) if both else '')

        # C21 (doc 321): THE WORKLOAD COLUMN MUST REACH BOTH ARTIFACTS.
        # THE DEFECT THIS IS BUILT ON, and it shipped: wire.py 101,831 bytes, run at 03:11 on
        # 16 Sept, wrote a WIRE_20260915.csv with NO touches column and a WEEK_SHEET.html with the
        # word "contested" on it zero times. Doc 314's whole finding was switched off and nothing
        # said so, because contest() returns two empty strings on a missing workload -- by design,
        # since a missing number must never print as "nobody wants him". A silent degrade needs an
        # external check, and this is it. Run against that file, both checks below FAIL.
        import glob as _glob
        hits = sorted(_glob.glob(os.path.join(b['dir'], 'Source', 'WIRE_2*.csv')))
        wrows = []
        if hits:
            with open(hits[-1], newline='', encoding='utf-8-sig') as fh:
                wrows = list(csv.DictReader(fh))
        check('C21', 'the wire file carries a touches column at all',
              bool(wrows) and 'touches' in wrows[0], list(wrows[0]) if wrows else None)
        check('C21', 'and it is filled on at least 20 rows (a column of blanks is the same defect)',
              sum(1 for r in wrows if (r.get('touches') or '').strip()) >= 20,
              sum(1 for r in wrows if (r.get('touches') or '').strip()))
        check('C21', 'the sheet prints a contested band on at least one pickup',
              'contested' in (b['ws'] or ''), (b['ws'] or '')[:200])
        # AND IT MUST BE THE LAST GAME, NOT THE SEASON. Doc 314's band was fitted on targets plus
        # carries in ONE game; read off the cumulative row instead it would price a man on six
        # weeks of work and put him two bands too high. Planted: Devaughn Vele at 40 touches for
        # the season and 3 in his last completed game. The column must say 3.
        # (The long sentence under the row is NOT asserted here: it renders only for the top two
        # rows or a contested man, by design -- doc 315 -- so its absence is not a defect.)
        r = run('c21_last_game', plant_form(2, {'Devaughn Vele': 40}, last={'Devaughn Vele': 3}))
        hits = sorted(_glob.glob(os.path.join(r['dir'], 'Source', 'WIRE_2*.csv')))
        vrow = {}
        if hits:
            with open(hits[-1], newline='', encoding='utf-8-sig') as fh:
                vrow = next((x for x in csv.DictReader(fh) if x['player'] == 'Devaughn Vele'), {})
        check('C21', 'the workload on the wire is his LAST COMPLETED GAME, not the season total',
              vrow.get('touches') == '3', vrow)
        check('C21', 'and the week it came from is recorded beside it',
              vrow.get('last_game_week') == '2', vrow)

        # C23 (doc 316, RESTORED 18 Sept -- doc 345): THE FIVE-ROW CAP MUST NOT EAT THE ROW THE
        # PAGE ITSELF SAYS TO CLAIM FIRST. The claim, stated before the run: on the recorded pool a
        # free man whose contest band prints "Put him first" (10+ carries and targets in his last
        # game) ranks BELOW fifth on worth, so `now[:5]` drops him while his own warning says he is
        # the one claim that has to spend the priority. Kaelon Black is that man in this tree -- 15
        # carries and targets, 56% contested, twelfth on worth at 1.5 -- and he is the player Matt
        # named on 16 Sept. THE NEGATIVE CONTROL WAS RUN FIRST: against the shipping code of
        # 17 Sept (sheet_engine.py pin e951cbd7dbceae3c, which reads `now[:5]` with no exception)
        # the first two of these three FAIL and the third passes, which is the signature of a cap
        # that hides rather than reorders.
        sec = page_section(b['ws'], 'Priority pickups, in order',
                           ('On the calendar', 'The bar', 'Every free body, priced'))
        check('C23', 'the section was found at all', bool(sec), (b['ws'] or '')[:200])
        check('C23', 'a man the page says to claim first is ON the priority list',
              sec and 'Kaelon Black' in sec, (sec or '')[:400])
        check('C23', 'and his claim-first sentence is printed, not just his row',
              sec and 'Put him first' in sec, (sec or '')[:400])
        check('C23', 'the re-admit did not promote him: he is not in the first five',
              sec and 'Kaelon Black' not in ranked_names(sec)[:5], ranked_names(sec or '')[:6])

        # C24 (doc 349): A SEAT YOU CANNOT CLAIM, OR A MAN WHO IS NOT PLAYING, IS NOT A SEAT.
        # The claim, stated before the run: the seat table said in its own words "these men have
        # never been rostered" while printing a man rostered in this league AND, at the very top,
        # a man on INJURY RESERVE. Both were Matt's catches. So: a seat man planted on IR must
        # leave the table and be NAMED with his reason, and a seat man absent from the free pool
        # must do the same. NEGATIVE CONTROL RUN FIRST against the 18 Sept shipping sheet_engine
        # (pin 78a1c4d945c95f49), where both fail because no such filter exists.
        # The heading is 'THE SEAT LIST' since doc 350 -- Matt asked for one name he and the
        # page both use out loud. This control FAILED on the rename before the marker moved,
        # which is the anchor doing its job; leave it anchored to the heading.
        SEATS = ('THE SEAT LIST', 'On the calendar', 'The bar', 'Every free body, priced')
        sec = page_section(b['ws'], SEATS[0], SEATS[1:])
        check('C24', 'the seat block renders at the top, with the pickups',
              bool(sec) and 'Priority pickups' in (b['ws'] or '')[:(b['ws'] or '').find(SEATS[0]) + 1],
              (b['ws'] or '')[:200])
        check('C24', 'a man rostered in this league is left off the seats and NAMED',
              sec and 'Left off, and why' in sec and 'Jaydon Blue' in sec.split('Left off, and why')[-1],
              (sec or '')[-300:])
        check('C24', 'each seat says what he actually does, not just how much',
              sec and ('run &middot;' in (b['ws'] or '') or ' run ' in sec)
              and any(w in sec for w in ('runs it', 'catches it', 'does both', 'barely used')),
              (sec or '')[:400])
        r = run('c24_ir', env={'MOCK_STATUS': json.dumps({'4429013': 'INJURY_RESERVE'})})
        sec2 = page_section(r['ws'], SEATS[0], SEATS[1:])
        head2 = (sec2 or '').split('Left off, and why')[0]
        check('C24', 'a seat man on injury reserve is not a seat row', sec2 and 'Tank Bigsby' not in head2,
              head2[:300])
        check('C24', 'and the page says who it left off and why',
              sec2 and 'Tank Bigsby' in (sec2 or '').split('Left off, and why')[-1]
              and 'injury reserve' in (sec2 or '').split('Left off, and why')[-1],
              (sec2 or '')[-300:])

        # C16 (doc 292): a free skill player off the board must reach a file the weekly read can use
        def free_file(d):
            import glob
            hits = sorted(glob.glob(os.path.join(d, 'Source', 'FREE_UNRANKED_*.csv')))
            if not hits:
                return None
            with open(hits[-1], newline='', encoding='utf-8-sig') as fh:
                return list(csv.DictReader(fh))
        fb = free_file(b['dir'])
        check('C16', 'base run writes FREE_UNRANKED_<date>.csv (header, nobody off the board in the recorded pool)',
              fb is not None and len(fb) == 0, fb)
        plant = [['9990001', 'Test Undrafted', 'RB', 'SEA', 0.1, 'ACTIVE']]
        r = run('c16', env={'MOCK_EXTRA': json.dumps(plant)})
        fr = free_file(r['dir']) or []
        hit = [x for x in fr if x.get('espn_id') == '9990001']
        check('C16', 'a planted off-board free back is in the file with position, team and ownership',
              len(hit) == 1 and hit[0]['pos'] == 'RB' and hit[0]['team'] == 'SEA' and hit[0]['owned_pct'] == '0.1', fr)
        check('C16', 'the sheet still finds the newest WIRE file (no glob collision)', r['ws'] and CARD in r['ws'])
        check('C16', 'the wire page still names him in the not-on-our-board list',
              r['ww'] and 'Test Undrafted' in r['ww'])
        # last, because on code without the guard the child process dies and the harness stops here
        r = run('c16b', env={'MOCK_EXTRA': json.dumps([['9990002', 'Test Unowned', 'WR', 'NYJ', None, 'ACTIVE']])})
        fr = free_file(r['dir']) or []
        hit = [x for x in fr if x.get('espn_id') == '9990002']
        check('C16', 'an off-board player with no ownership number is written at 0.0 and the run finishes',
              len(hit) == 1 and hit[0]['owned_pct'] == '0.0', fr)
        r = run('c16c', env={'MOCK_NO_OWN': '4723820'})
        check('C16', 'a board player with no ownership number: both pages still build',
              r['ws'] is not None and r['ww'] is not None and CARD in r['ws'])
    finally:
        shutil.rmtree(work, ignore_errors=True)
    bad = [x for x in results if not x[2]]
    print(f"\n  {len(results) - len(bad)} of {len(results)} checks pass")
    return 0 if not bad else 1


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--mock':
        sys.exit(mock(os.path.abspath(sys.argv[2])))
    sys.exit(main(sys.argv[1:]))
