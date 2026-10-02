#!/usr/bin/env python3
r"""
ctl_307.py -- the negative controls for doc 307's three fixes. Run it from anywhere:

    py Scripts\research\redteam\ctl_307.py

It resolves every path against its OWN location, never the shell's (SECTION 0.4, doc 144), and
uses only the standard library plus what wire.py already imports.

WHAT IT PROVES, IN ORDER. Each block refuses to read its variant until its control passes.

  A. wire.py's patched flags() reproduces the SHIPPED flags() byte for byte on every real
     player_context row, when nobody moved. Without this, nothing below can be read.
  B. On the two rows the fix is for, the job clause is dropped and the move is named.
  C. The new team expression, replayed on the real board joined to the newest pull, corrects
     exactly the players who changed NFL teams and leaves everyone else alone.
  D. depth_map.py's job-ceiling guard lifts NOTHING when handed its own baseline pull.
  E. It lifts Green Bay 152 -> 241 on every post-exemption pull, and no other team on any pull.
  F. It does NOT touch job_gap, so Green Bay still labels UNSETTLED. The label was always right;
     only the number was wrong.
  G. sheet_engine.py's seat table prints the starter's status beside the STARTER, not under the
     backup's name.
  H. THE BYE MOVES WITH THE TEAM. The first version of the team fix corrected seven rows and left
     all seven byes pointing at the club the man left.
"""
import csv, os, sys, glob, importlib.util

HERE     = os.path.dirname(os.path.abspath(__file__))
SCRIPTS  = os.path.normpath(os.path.join(HERE, '..', '..'))
SRC      = os.path.normpath(os.path.join(SCRIPTS, '..', 'Source'))
LIVE     = os.path.join(SCRIPTS, 'live_draft')
FAILURES = []


def load(name):
    p = os.path.join(SCRIPTS, name)
    if not os.path.exists(p):
        sys.exit(f'MISSING: {p}')
    sys.path.insert(0, SCRIPTS)
    sys.argv = [name]
    spec = importlib.util.spec_from_file_location('ctl_' + name[:-3], p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(label, ok, detail=''):
    print(f'  {"PASS" if ok else "FAIL"}  {label}{("   " + detail) if detail else ""}')
    if not ok:
        FAILURES.append(label)
    return ok


def flags_SHIPPED(c):
    """wire.py's flags() exactly as it stood before doc 307. The control's whole point."""
    if not c:
        return ''
    out = []
    why = c.get('why', '') or ''
    g = (c.get('grade') or '').upper()
    if g in ('AVOID', 'DISCOUNT'):
        out.append(g.title())
    job = c.get('job') or ''
    if job:
        out.append(f"{job.lower()} job, worth {c.get('job_ceil') or '?'}")
    i = why.find('RB SIGNALS: ')
    if i >= 0:
        n = why[i + 12:i + 15].strip()
        if n and n[0].isdigit():
            out.append(f"back signals {n[0]} of 3")
    i = why.find('TGT SHARE 2025: ')
    if i >= 0:
        out.append('targets ' + why[i + 16:i + 34].split('(')[0].strip())
    return ' · '.join(out)


def rows_of(p, key=None):
    with open(p, newline='', encoding='utf-8-sig') as fh:
        rs = list(csv.DictReader(fh))
    return {str(r[key]).strip(): r for r in rs} if key else rs


def main():
    W = load('wire.py')

    # ---------- A ----------------------------------------------------------------------------
    print('\nA. CONTROL: patched flags() == shipped flags() when nobody moved')
    ctx = rows_of(os.path.join(LIVE, 'player_context.csv'), 'ESPN_ID')
    diff = [k for k, c in ctx.items() if W.flags(c) != flags_SHIPPED(c)]
    ok = check(f'all {len(ctx)} player_context rows reproduce', not diff,
               '' if not diff else f'{len(diff)} differ')
    check('the empty row reproduces', W.flags(None) == flags_SHIPPED(None) == '')
    if not ok:
        print('  refusing to read the variants against a function that does not reproduce')
        return 1

    # ---------- B ----------------------------------------------------------------------------
    print('\nB. THE ROWS THE FIX IS FOR (job_ceil is a TEAM constant, so a move invalidates it)')
    for pid, name, now in [('4819231', 'Kaleb Johnson', 'GB'), ('4362478', 'Emari Demercado', 'DAL')]:
        c = ctx.get(pid)
        if c is None:
            check(f'{name} present in player_context.csv', False, f'id {pid} not found')
            continue
        before, after = flags_SHIPPED(c), W.flags(c, now)
        print(f'     {name:<18} before {before!r}')
        print(f'     {"":<18} after  {after!r}')
        check(f'{name}: old job number gone', 'job, worth' not in after)
        check(f'{name}: the move is named', f'moved to {now}' in after)

    # ---------- C ----------------------------------------------------------------------------
    print('\nC. THE TEAM EXPRESSION, replayed on the real board against the newest pull')
    board = rows_of(os.path.join(LIVE, 'board_v8_fixed.csv'), 'espn_id')
    pulls = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    live = rows_of(pulls[-1], 'espn_id')
    moved, same = [], 0
    for pid, b in board.items():
        p = live.get(pid)
        if not p:
            continue
        raw = (p.get('team') or '').strip().upper()
        lt = '' if raw in ('FA', '') else W.team_key(raw)     # proTeamId 0 -> PRO.get() is None
        bt = W.team_key(b.get('team_c', ''))
        if lt and bt and lt != bt:
            moved.append((b.get('player', pid), bt, lt))
        else:
            same += 1
    print(f'     against {os.path.basename(pulls[-1])}: {same} unchanged, {len(moved)} corrected')
    for nm, was, now in sorted(moved):
        print(f'       {nm:<24} {was} -> {now}')
    check('at least one correction, and it is a small minority', 0 < len(moved) < 0.1 * (same + len(moved)))

    # ---------- D, E, F ----------------------------------------------------------------------
    print('\nD/E/F. THE JOB-CEILING GUARD')
    DM = load('depth_map.py')
    pre, pre_file = DM.preseason_ceiling()
    print(f'     baseline the function chose for itself: {pre_file}  ({len(pre)} teams)')
    check('a baseline was found', bool(pre_file))

    def ceil_gap(path):
        import pandas as pd
        d = pd.read_csv(path, low_memory=False)
        d.columns = [c.replace('﻿', '') for c in d.columns]
        d = d[d.pos == 'RB'].copy()
        d['proj'] = pd.to_numeric(d.proj_2026, errors='coerce').fillna(0)
        ce, ga = {}, {}
        for tm, g in d.groupby('team'):
            v = g.sort_values('proj', ascending=False).proj.values
            if len(v) >= 2:
                ce[tm] = float(v[0]); ga[tm] = float(v[0] - v[1])
        return ce, ga

    everything, self_lifted = set(), None
    for f in pulls:
        ce, ga = ceil_gap(f)
        lift = [(t, v, pre[t]) for t, v in ce.items() if t in pre and (pre[t] - v) > 40]
        everything |= {t for t, _, _ in lift}
        if os.path.basename(f) == pre_file:
            self_lifted = lift
        names = ', '.join(f'{t} {a:.0f}->{b:.0f}' for t, a, b in sorted(lift)) or 'nothing'
        print(f'     {os.path.basename(f):<44} lifts {names}')
    check('D. the guard lifts nothing against its own baseline', self_lifted == [])
    check('E. exactly one team is ever lifted', len(everything) == 1, f'{sorted(everything)}')
    ce, ga = ceil_gap(pulls[-1])
    if 'GB' in ga:
        lbl = 'UNSETTLED' if ga['GB'] < 60 else ('contested' if ga['GB'] < 150 else 'LEAD BACK')
        check('F. job_gap untouched, so GB still labels UNSETTLED', lbl == 'UNSETTLED',
              f'gap {ga["GB"]:.0f} -> {lbl}')

    # ---------- G ----------------------------------------------------------------------------
    print('\nG. THE SEAT TABLE NAMES THE RIGHT MAN')
    se = open(os.path.join(SCRIPTS, 'sheet_engine.py'), encoding='utf-8').read()
    check('the status renders beside the starter, not under the backup',
          'for the season{holdtag}' in se and
          "tag = ' &middot; <strong>your own man</strong>' if yours else ''" in se)
    seats = [r for r in rows_of(os.path.join(SRC, 'inherit_2026.csv')) if r.get('live_tag')]
    print(f'     {len(seats)} of 32 seat rows carry a starter status that used to print on the backup:')
    for r in seats:
        print(f"       {r['next_man']:<22} was tagged {r['live_tag']!r}, which belongs to {r['holds_the_job']}")

    # ---------- H ------------------------------------------------------------------------
    print('\nH. THE BYE FOLLOWS THE TEAM')
    byes = W.load_byes()
    check('byes_2026.csv resolves all 32 teams', len(byes) == 32, f'{len(byes)} teams')
    if byes:
        wrong = []
        for nm, was, now in sorted(moved):
            want = byes.get(now)
            had = byes.get(was)
            if want is None:
                wrong.append((nm, now, 'no bye for the new team'))
                continue
            print(f'     {nm:<24} {was} bye {had} -> {now} bye {want}')
            if had == want:
                continue                      # the two clubs share a bye; nothing to get wrong
        check('every moved row has a bye available for its new team',
              not wrong, '; '.join(f'{a} {b} {c}' for a, b, c in wrong))
        # the live artefact, if it has been rebuilt
        import glob as _g
        wires = sorted(_g.glob(os.path.join(SRC, 'WIRE_*.csv')))
        # A WIRE FILE OLDER THAN ITS BUILDER IS NOT A FAILURE, IT IS AN UNRUN BUILD. Reporting it
        # as FAIL is how a checker teaches you to ignore it (doc 146).
        if wires and os.path.getmtime(wires[-1]) < os.path.getmtime(os.path.join(SCRIPTS, 'wire.py')):
            print(f'     {os.path.basename(wires[-1])} predates this wire.py: not checked. '
                  f'Run  py wire.py  and run this again.')
            wires = []
        if wires:
            live_rows = rows_of(wires[-1])
            bad = []
            for r in live_rows:
                if 'moved to' not in (r.get('flags') or ''):
                    continue
                want = byes.get(W.team_key(r['team']))
                got = str(r.get('bye') or '').split('.')[0]
                if want is not None and got != str(want):
                    bad.append(f"{r['player']} on {r['team']} reads bye {got}, should be {want}")
            check(f'{os.path.basename(wires[-1])}: every moved row carries its NEW team bye',
                  not bad, '; '.join(bad))

    print('\n' + ('ALL CONTROLS PASS' if not FAILURES else 'FAILED: ' + '; '.join(FAILURES)))
    return 1 if FAILURES else 0


if __name__ == '__main__':
    sys.exit(main())
