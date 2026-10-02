#!/usr/bin/env python3
r"""j2_bands_2021.py -- JOB 2 item 5: doc 343's P(the job opens) bands with 2021 added, and T5 beside them.

Runs job_opens.study() (doc 343, the script that produced seat.p_opens_by_band) TWICE without
touching it: once on 2022-2025 as the CONTROL, which must reproduce the shipped bands
0.476 / 0.438 / 0.533 / 0.636 on n = 42 / 32 / 30 / 22 exactly; then on 2021-2025. Then, on the
same rows (job_opens_rows.csv, one per team-season), predictor C -- doc 292's T5, the second back's
share of the NON-leader RB snaps in week 1 -- is banded beside doc 300's share so the two
predictors of the ODDS term can be compared on one population.

THE CLAIM IN ITS TESTABLE FORM: adding 2021 keeps the top band (40%+) above the bottom band (<20)
on P(opens), on a larger n. FALSIFIER: if the gradient reverses or the permutation at a 35% split
loses significance on five seasons, the shipped bands rest on four seasons that do not generalise.

INPUTS: research\_nflverse_cache\stats_player_week_2022..2025.csv (already there) plus
stats_player_week_2021.csv and snap_counts_2021..2025.csv, fetched from nflverse into a J2 cache
beside this script if absent. pandas + numpy only.
Run:  py research\j2\j2_bands_2021.py
"""
import contextlib
import importlib
import importlib.util
import io
import os
import re
import sys
import unicodedata
import urllib.request

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
NFL = os.environ.get('J2_NFLVERSE', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
OUT = os.environ.get('J2_OUT', HERE)
WK1 = os.path.normpath(os.path.join(HERE, '..', 'wk1'))
RELEASE = 'https://github.com/nflverse/nflverse-data/releases/download/'
SHIPPED = {'<20': (0.476, 42), '20-30': (0.438, 32), '30-40': (0.533, 30), '40+': (0.636, 22)}


def need(name, release):
    os.makedirs(NFL, exist_ok=True)
    p = os.path.join(NFL, name)
    if not os.path.exists(p) or os.path.getsize(p) < 10000:
        url = RELEASE + release + '/' + name
        print(f'  fetching {name} from nflverse ...')
        try:
            urllib.request.urlretrieve(url, p)
        except Exception as exc:
            sys.exit(f'could not fetch {url}: {type(exc).__name__}: {exc}')
        if os.path.getsize(p) < 10000:
            sys.exit(f'{name} came back {os.path.getsize(p)} bytes; not a data file. Stopping.')
    return p


def norm(s):
    s = unicodedata.normalize('NFKD', str(s or '')).encode('ascii', 'ignore').decode()
    s = s.lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', s)
    return re.sub(r'\s+', ' ', s).strip()


def cache_dir(seasons):
    """A directory holding only the requested seasons' weekly files (links or copies), because
    job_opens.study() globs its CACHE for every stats_player_week_*.csv."""
    d = os.path.join(OUT, f'_cache_{seasons[0]}_{seasons[-1]}_{abs(hash(NFL)) % 100000}')
    os.makedirs(d, exist_ok=True)
    for s in seasons:
        src = need(f'stats_player_week_{s}.csv', 'player_stats')
        dst = os.path.join(d, os.path.basename(src))
        if not os.path.exists(dst):
            try:
                os.symlink(os.path.abspath(src), dst)
            except OSError:
                import shutil
                shutil.copyfile(src, dst)
    return d


def run_job_opens(seasons):
    spec = importlib.util.spec_from_file_location('job_opens', os.path.join(WK1, 'job_opens.py'))
    jo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(jo)                          # fresh module: the seed resets each run
    jo.CACHE = cache_dir(seasons)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = jo.study()
    txt = buf.getvalue()
    rows = pd.read_csv(os.path.join(WK1, 'job_opens_rows.csv'))
    return rc, txt, rows, jo


def main():
    out = []

    def say(*a):
        s = ' '.join(str(x) for x in a); print(s); out.append(s)

    # ---- CONTROL: 2022-2025 must reproduce the shipped constants -----------------------------------
    rc, txt, r4, jo = run_job_opens([2022, 2023, 2024, 2025])
    say('CONTROL -- job_opens.study() on 2022-2025 (the shipped population)')
    say(txt.rstrip())
    ok = True
    for b, (p, n) in SHIPPED.items():
        x = r4[r4.band == b]
        got = (round(float(x.opens.mean()), 3), len(x))
        ok &= got == (p, n)
        say(f'  band {b:<6} shipped {p:.3f} n={n:<3} reproduced {got[0]:.3f} n={got[1]}  {"ok" if got == (p, n) else "MISMATCH"}')
    say(f'  CONTROL {"PASS" if ok else "FAIL"}: the shipped p_opens_by_band reproduce exactly')
    assert ok, 'the shipped bands did not reproduce; stop and look'

    # ---- 2021 added ---------------------------------------------------------------------------------
    rc, txt, r5, jo = run_job_opens([2021, 2022, 2023, 2024, 2025])
    say('\n2021 ADDED -- job_opens.study() on 2021-2025')
    say(txt.rstrip())
    say('\n  P(opens) by band, four seasons against five:')
    say(f"  {'band':<7}{'n4':>4}{'p4':>7}{'n5':>5}{'p5':>7}")
    for b in ('<20', '20-30', '30-40', '40+'):
        x4, x5 = r4[r4.band == b], r5[r5.band == b]
        say(f"  {b:<7}{len(x4):>4}{x4.opens.mean():>7.3f}{len(x5):>5}{x5.opens.mean():>7.3f}")
    say(f'  2021 alone: n={int((r5.season == 2021).sum())}, P(opens) {r5[r5.season == 2021].opens.mean():.3f}')

    # ---- T5 (doc 292) as a second band for the ODDS, on the five-season rows -------------------------
    players = pd.read_csv(need('players.csv', 'players'), low_memory=False, usecols=['gsis_id', 'display_name', 'pfr_id'])
    pfr2gsis = dict(zip(players.pfr_id.dropna(), players.gsis_id[players.pfr_id.notna()]))
    name2gsis = {}
    for g, nm in zip(players.gsis_id, players.display_name):
        name2gsis.setdefault(norm(nm), g)
    names = dict(zip(players.gsis_id, players.display_name))
    # the rows carry names, not ids; rebuild week-1 ids from the stats files the same way study() did
    d = jo.rbs([need(f'stats_player_week_{s}.csv', 'player_stats') for s in (2021, 2022, 2023, 2024, 2025)])
    d = d[d.week == 1]
    t5 = {}
    for s in (2021, 2022, 2023, 2024, 2025):
        sn = pd.read_csv(need(f'snap_counts_{s}.csv', 'snap_counts'), low_memory=False)
        sn = sn[(sn.game_type == 'REG') & (sn.position == 'RB') & (sn.week == 1)]
        snaps = {}
        for r in sn.itertuples(index=False):
            g = pfr2gsis.get(r.pfr_player_id) or name2gsis.get(norm(r.player))
            if g is None:
                continue
            snaps[(r.team, g)] = snaps.get((r.team, g), 0.0) + float(r.offense_snaps or 0)
        for (season, team), g1 in d[d.season == s].groupby(['season', 'team']):
            g1 = g1[g1.work > 0].sort_values(['work', 'player_id'], ascending=[False, True])
            if len(g1) < 2 or g1.work.sum() < 10:
                continue
            lead, two = g1.iloc[0].player_id, g1.iloc[1].player_id
            non = sum(v for (tm, g), v in snaps.items() if tm == team and g != lead)
            mine = snaps.get((team, two))
            if non > 0 and mine is not None and (team, lead) in snaps:
                t5[(int(season), team)] = mine / non
    r5['t5'] = [t5.get((int(a), b)) for a, b in zip(r5.season, r5.team)]
    z = r5[r5.t5.notna()].copy()
    z['bandC'] = z.t5.map(lambda v: '<50' if v < .5 else '50-70' if v < .7 else '70-85' if v < .85 else '85+')
    say(f'\nT5 (doc 292: the second back\'s share of NON-leader week-1 RB snaps) on the same rows: {len(z)} of {len(r5)} joined')
    say(f"  {'band':<7}{'n':>4}{'P(open)':>9}{'startable':>10}{'held AFTER':>11}")
    for b in ('<50', '50-70', '70-85', '85+'):
        x = z[z.bandC == b]
        o = x[x.opens]
        say(f"  {b:<7}{len(x):>4}{x.opens.mean():>9.3f}{x.startable.mean():>10.3f}{(o.held_after.mean() if len(o) else 0):>11.2f}")
    rng = np.random.default_rng(20260918)

    def perm(x, y, cut, n=6000):
        x, y = np.asarray(x, float), np.asarray(y, float)
        hi, lo = y[x >= cut], y[x < cut]
        obs = hi.mean() - lo.mean(); k = len(hi); c = 0
        for _ in range(n):
            p = rng.permutation(y)
            if p[:k].mean() - p[k:].mean() >= obs:
                c += 1
        return obs, (c + 1) / (n + 1), len(hi), len(lo)

    for lab, col, cut in (('doc 300 share at 35%', 'share', .35), ('T5 at 70%', 't5', .70), ('T5 at 85%', 't5', .85)):
        for oc in ('opens', 'startable'):
            o, p, nh, nl = perm(z[col], z[oc], cut)
            say(f'  {lab:<22} {oc:<10} {o:+.3f}  one-sided p={p:.4f}  (n {nh} vs {nl})')
    # do the two bands rank the same men? and P(opens) in the four disagreement cells
    ia = z.band.map({'<20': 0, '20-30': 1, '30-40': 2, '40+': 3}); ic = z.bandC.map({'<50': 0, '50-70': 1, '70-85': 2, '85+': 3})
    z['gap'] = ia - ic
    say(f'  same band index {int((z.gap == 0).sum())}, off by one {int((z.gap.abs() == 1).sum())}, off by two or more {int((z.gap.abs() >= 2).sum())}')
    for lab, sel in (('doc300 high (35%+), T5 low (<70%)', (z.share >= .35) & (z.t5 < .70)),
                     ('doc300 low, T5 high', (z.share < .35) & (z.t5 >= .70)),
                     ('both high', (z.share >= .35) & (z.t5 >= .70)), ('both low', (z.share < .35) & (z.t5 < .70))):
        g = z[sel]
        say(f'    {lab:<34} n={len(g):>3}  P(opens) {g.opens.mean() if len(g) else float("nan"):.3f}  startable {g.startable.mean() if len(g) else float("nan"):.3f}')
    r5.to_csv(os.path.join(OUT, 'J2_job_opens_rows_2021_2025.csv'), index=False)
    # ---- VINTAGE: the drive's cache holds two nflverse releases (2022-2024 at 150 columns, 2025 at 114).
    # The same five seasons on the CURRENT release, when a second cache is given, so the reader can see
    # what the release alone moves.
    alt = os.environ.get('J2_NFLVERSE_ALT')
    if alt and os.path.isdir(alt):
        global NFL
        keep = NFL
        NFL = alt
        try:
            rc, txt, r5b, _ = run_job_opens([2021, 2022, 2023, 2024, 2025])
        finally:
            NFL = keep
        say(f'\nVINTAGE CHECK -- the same five seasons on the current nflverse release ({alt}):')
        say(f"  {'band':<7}{'n drive':>8}{'p drive':>8}{'n cur':>7}{'p cur':>7}")
        for b in ('<20', '20-30', '30-40', '40+'):
            x5, xb = r5[r5.band == b], r5b[r5b.band == b]
            say(f"  {b:<7}{len(x5):>8}{x5.opens.mean():>8.3f}{len(xb):>7}{xb.opens.mean():>7.3f}")
        ncol = {}
        for s_ in (2021, 2022, 2023, 2024, 2025):
            for lab, root in (('drive', keep), ('current', alt)):
                pth = os.path.join(root, f'stats_player_week_{s_}.csv')
                if os.path.exists(pth):
                    ncol[(lab, s_)] = len(open(pth, encoding='utf-8').readline().split(','))
        say('  columns per file: ' + ', '.join(f'{k[0]} {k[1]}: {v}' for k, v in sorted(ncol.items())))
    with open(os.path.join(OUT, 'run_j2_bands_2021.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')
    say(f'\nwrote J2_job_opens_rows_2021_2025.csv and run_j2_bands_2021.txt in {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
