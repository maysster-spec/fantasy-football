#!/usr/bin/env python3
r"""j3_product.py -- JOB 3 TASK B: do the ODDS (week-one work share) and the RATE (T5) multiply?

THE CLAIM IN ITS TESTABLE FORM, pre-registered in FABLE_JOB3_seat_lane.md (18 Sept), restated before
the run:
  For a seat, expected relief points = P(inherits | week-one share band) x relief ppg (| T5 band), and
  the two inputs are independent enough inside the seat population that the product is a fair estimate
  rather than a double count.
RUN ORDER, as fixed: (1) rho between the week-one work share and T5 inside the seat population, with p
  and n, before anything else; (2) the cross of share bands (<20 / 20-30 / 30-40 / 40+) against T5
  QUARTILES, with cell counts, the observed inheritance rate and the observed relief ppg -- a cell
  under n=8 is printed with its n and no conclusion; (3) every seat scored three ways -- odds alone,
  rate alone, odds x rate -- and each ranked against the seat's ACTUALLY REALISED relief points (zero
  for a seat that never opened), Spearman rho for all three.
KILL CONDITION: if odds x rate does not beat the better single instrument by at least 0.05 of rho, the
  page keeps ranking by odds alone and prints the rate as a separate column.

POPULATION (0.6, restated): doc 343's seat rows with 2021 added (doc 348 section 5, n=157): every NFL
  team-season 2021-2025 whose week-one RB usage leader and second back both played in week one with
  combined RB carries plus targets of 10 or more; one row per team-season, the SEAT is the second
  back. Rebuilt here by job_opens.py's own reader (rbs()) on the same cache files, and the shares are
  asserted equal to J2_job_opens_rows_2021_2025.csv before anything is scored.
  OPENS: the leader misses a team-played week in weeks 2-14. REALISED RELIEF POINTS: the seat's
  half-PPR over the leader's absence weeks in 2-14 (zero if it never opened); REALISED RELIEF PPG:
  the same over the absence weeks in which he had a line (blank if none).
  T5: the seat's week-one offensive snaps over all RB snaps that week EXCLUDING the leader's (doc 292),
  blank when the leader has no week-one snap row or the join misses. BREADTH and TARGET RATIO
  (Task A's definitions) on the seat's weeks before the first absence (weeks 1-14 if it never opened).
THE INSTRUMENTS (the page's, both in-sample on these seasons): odds = seat.p_opens_by_band, five
  seasons (doc 348): <20 0.510 / 20-30 0.474 / 30-40 0.564 / 40+ 0.621; rate = doc 348 section 3's
  relief ppg by week-one T5 band, measured on doc 320's 114 events: <50 8.91 / 50-70 12.55 /
  70-85 14.69 / 85+ 12.98. A second rate, the in-sample T5-quartile mean of realised relief ppg on
  these seats, is scored beside it and labelled in-sample.
INPUTS: research\_nflverse_cache\stats_player_week_2021..2025.csv, snap_counts_2021..2025.csv,
  players.csv (fetched if absent). pandas + numpy only (0.4).
Run:  py research\j3\j3_product.py        (J3_NFLVERSE and J3_OUT override the paths)
"""
import importlib.util
import json
import os
import re
import sys
import unicodedata
import urllib.request

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
NFL = os.environ.get('J3_NFLVERSE', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
OUT = os.environ.get('J3_OUT', HERE)
WK1 = os.path.normpath(os.path.join(HERE, '..', 'wk1'))
J2 = os.path.normpath(os.path.join(HERE, '..', 'j2'))
RELEASE = 'https://github.com/nflverse/nflverse-data/releases/download/'
SEASONS = [2021, 2022, 2023, 2024, 2025]
WEEKS = range(2, 15)
SEED = 20260918
NPERM = 6000
ODDS = {'<20': 0.510, '20-30': 0.474, '30-40': 0.564, '40+': 0.621}          # doc 348 section 5
RATE_T5 = {'<50': 8.91, '50-70': 12.55, '70-85': 14.69, '85+': 12.98}      # doc 348 section 3, predictor C


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


def band4(s):
    return '<20' if s < .20 else '20-30' if s < .30 else '30-40' if s < .40 else '40+'


def band5(s):
    return '<50' if s < .50 else '50-70' if s < .70 else '70-85' if s < .85 else '85+'


def rank(a):
    a = np.asarray(a, dtype=float)
    order = a.argsort()
    r = np.empty(len(a)); r[order] = np.arange(1, len(a) + 1)
    vals, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(vals)); np.add.at(sums, inv, r)
    return sums[inv] / cnt[inv]


def spearman(x, y, rng, n=NPERM):
    rx, ry = rank(x), rank(y)
    obs = float(np.corrcoef(rx, ry)[0, 1])
    c = 0
    for _ in range(n):
        if abs(np.corrcoef(rx, rng.permutation(ry))[0, 1]) >= abs(obs):
            c += 1
    return obs, (c + 1) / (n + 1)


def main():
    rng = np.random.default_rng(SEED)
    spec = importlib.util.spec_from_file_location('job_opens', os.path.join(WK1, 'job_opens.py'))
    jo = importlib.util.module_from_spec(spec); spec.loader.exec_module(jo)
    paths = [need(f'stats_player_week_{s}.csv', 'player_stats') for s in SEASONS]
    d = jo.rbs(paths)
    # carries and targets are needed raw for breadth; rbs() keeps them
    played = set(zip(d.season, d.team, d.week))
    players = pd.read_csv(need('players.csv', 'players'), low_memory=False, usecols=['gsis_id', 'display_name', 'pfr_id'])
    pfr2gsis = dict(zip(players.pfr_id.dropna(), players.gsis_id[players.pfr_id.notna()]))
    name2gsis = {}
    for g, nm in zip(players.gsis_id, players.display_name):
        name2gsis.setdefault(norm(nm), g)
    snaps = {}
    for s in SEASONS:
        sn = pd.read_csv(need(f'snap_counts_{s}.csv', 'snap_counts'), low_memory=False)
        sn = sn[(sn.game_type == 'REG') & (sn.position == 'RB') & (sn.week == 1)]
        for r in sn.itertuples(index=False):
            g = pfr2gsis.get(r.pfr_player_id) or name2gsis.get(norm(r.player))
            if g is None:
                continue
            snaps[(s, r.team, g)] = snaps.get((s, r.team, g), 0.0) + float(r.offense_snaps or 0)
    rows = []
    for (season, team), g1 in d[d.week == 1].groupby(['season', 'team']):
        g1 = g1[g1.work > 0].sort_values(['work', 'player_id'], ascending=[False, True])
        if len(g1) < 2:
            continue
        lead, two = g1.iloc[0], g1.iloc[1]
        tot = float(g1.work.sum())
        if tot < 10:
            continue
        later = d[(d.season == season) & (d.team == team) & (d.week.isin(WEEKS))]
        wks = sorted(w for w in WEEKS if (season, team, w) in played)
        if not wks:
            continue
        lead_wk = set(later[later.player_id == lead.player_id].week)
        missed = [w for w in wks if w not in lead_wk]
        first = missed[0] if missed else None
        tl = later[later.player_id == two.player_id]
        rel = tl[tl.week.isin(missed)]
        relief_pts = float(rel.half.sum()) if missed else 0.0
        relief_ppg = (float(rel.half.sum()) / len(rel)) if len(rel) else None
        # breadth on the seat's weeks before the first absence (all of 1-14 if it never opened)
        allw = d[(d.season == season) & (d.team == team) & (d.player_id == two.player_id)]
        pre = allw[allw.week < (first if first is not None else 15)]
        c_, t_ = float(pre.carries.sum()), float(pre.targets.sum())
        work = c_ + t_
        tr = (t_ / work) if work > 0 else None
        breadth = (1 - abs(tr - 0.5) * 2) if tr is not None else None
        non = sum(v for (ss, tm, g), v in snaps.items() if ss == season and tm == team and g != lead.player_id)
        mine = snaps.get((season, team, two.player_id))
        t5 = (mine / non) if (non > 0 and mine is not None and (season, team, lead.player_id) in snaps) else None
        rows.append(dict(season=int(season), team=team, lead=lead.player_display_name, name=two.player_display_name,
                         wk1_share=float(two.work) / tot, opens=first is not None, first_absence=first,
                         absence_weeks=len(missed), relief_weeks_with_line=int(len(rel)),
                         realised_relief_ppg=relief_ppg, realised_relief_points=relief_pts,
                         pre_carries=c_, pre_targets=t_, breadth=breadth, target_ratio=tr, t5=t5))
    r = pd.DataFrame(rows)
    r['share_band'] = r.wk1_share.map(band4)
    lines = []

    def say(*a):
        s_ = ' '.join(str(x) for x in a); print(s_); lines.append(s_)

    # ---- CONTROL: the population must be doc 348's 157 rows with the same shares -------------------
    ref = pd.read_csv(os.path.join(J2, 'J2_job_opens_rows_2021_2025.csv'))
    m = r.merge(ref[['season', 'team', 'share', 'opens']], on=['season', 'team'], how='outer', suffixes=('', '_ref'), indicator=True)
    both = m[m._merge == 'both']
    say(f'TASK B -- seats rebuilt: {len(r)} (doc 348 had {len(ref)}); matched {len(both)}; '
        f'largest share gap {float((both.wk1_share - both.share).abs().max()):.4f}; opens agree on {int((both.opens == both.opens_ref).sum())} of {len(both)}')
    assert len(r) == len(ref) == len(both) and float((both.wk1_share - both.share).abs().max()) < 1e-6 \
        and int((both.opens == both.opens_ref).sum()) == len(both), 'the seat population did not reproduce; stop and look'
    say(f'  opened {int(r.opens.sum())} of {len(r)} ({r.opens.mean():.3f}); realised relief points, all seats, mean {r.realised_relief_points.mean():.1f}, '
        f'median {r.realised_relief_points.median():.1f}; among opened seats with a line (n={int(r.realised_relief_ppg.notna().sum())}) ppg {r.realised_relief_ppg.mean():.2f}')
    z = r[r.t5.notna()].copy()
    say(f'  T5 joined on {len(z)} of {len(r)} (blank: {", ".join(f"{a.season} {a.team} {a.name}" for a in r[r.t5.isna()].itertuples())})')

    # ---- STEP 1: are the two instruments the same thing? ----------------------------------------------
    rho, p = spearman(z.wk1_share.values, z.t5.values, rng)
    say(f'\nSTEP 1 -- rho(week-one work share, T5) inside the seat population: rho {rho:+.3f}, p={p:.4f}, n={len(z)}')
    say(f'  Pearson {float(np.corrcoef(z.wk1_share, z.t5)[0, 1]):+.3f}; share of variance shared {float(np.corrcoef(z.wk1_share, z.t5)[0, 1]) ** 2:.3f}')

    # ---- STEP 2: the cross -------------------------------------------------------------------------
    qs = z.t5.quantile([.25, .5, .75]).values
    def t5q(v):
        return 'Q1' if v < qs[0] else 'Q2' if v < qs[1] else 'Q3' if v < qs[2] else 'Q4'
    z['t5_quartile'] = z.t5.map(t5q)
    say(f'\nSTEP 2 -- share bands x T5 quartiles (quartile cuts {qs[0]:.3f} / {qs[1]:.3f} / {qs[2]:.3f}; T5 is 1.00 on {int((z.t5 >= 0.999).sum())} rows, so the top quartiles tie)')
    say(f"  {'band':<7}{'T5 q':<6}{'n':>4}{'P(open)':>9}{'relief ppg':>12}{'n ppg':>6}{'relief pts':>12}")
    cells = {}
    for b in ('<20', '20-30', '30-40', '40+'):
        for q in ('Q1', 'Q2', 'Q3', 'Q4'):
            g = z[(z.share_band == b) & (z.t5_quartile == q)]
            gp = g[g.realised_relief_ppg.notna()]
            cells[f'{b}|{q}'] = dict(n=int(len(g)), p_open=(round(float(g.opens.mean()), 3) if len(g) else None),
                                     relief_ppg=(round(float(gp.realised_relief_ppg.mean()), 2) if len(gp) else None),
                                     relief_pts=(round(float(g.realised_relief_points.mean()), 1) if len(g) else None))
            note = '  (n<8, no conclusion)' if 0 < len(g) < 8 else ''
            say(f"  {b:<7}{q:<6}{len(g):>4}{(g.opens.mean() if len(g) else float('nan')):>9.3f}"
                f"{(gp.realised_relief_ppg.mean() if len(gp) else float('nan')):>12.2f}{len(gp):>6}{(g.realised_relief_points.mean() if len(g) else float('nan')):>12.1f}{note}")
    say('  margins by T5 quartile:')
    for q in ('Q1', 'Q2', 'Q3', 'Q4'):
        g = z[z.t5_quartile == q]; gp = g[g.realised_relief_ppg.notna()]
        say(f"    {q}  n={len(g):>3}  T5 {g.t5.min():.2f}-{g.t5.max():.2f}  P(open) {g.opens.mean():.3f}  relief ppg {gp.realised_relief_ppg.mean():.2f} (n={len(gp)})  relief pts {g.realised_relief_points.mean():.1f}")
    say('  margins by share band:')
    for b in ('<20', '20-30', '30-40', '40+'):
        g = z[z.share_band == b]; gp = g[g.realised_relief_ppg.notna()]
        say(f"    {b:<6} n={len(g):>3}  P(open) {g.opens.mean():.3f}  relief ppg {gp.realised_relief_ppg.mean():.2f} (n={len(gp)})  relief pts {g.realised_relief_points.mean():.1f}")

    # ---- STEP 3: three scores against realised relief points ----------------------------------------
    z['t5_band'] = z.t5.map(band5)
    z['score_odds'] = z.share_band.map(ODDS)
    z['score_rate'] = z.t5_band.map(RATE_T5)
    z['score_product'] = z.score_odds * z.score_rate
    # the in-sample variant: the rate by T5 quartile from these seats' own realised ppg
    qmean = z[z.realised_relief_ppg.notna()].groupby('t5_quartile').realised_relief_ppg.mean().to_dict()
    z['score_rate_insample'] = z.t5_quartile.map(qmean)
    z['score_product_insample'] = z.score_odds * z.score_rate_insample
    y = z.realised_relief_points.values
    say(f'\nSTEP 3 -- Spearman rho of each score against REALISED relief points (zero when the seat never opened), n={len(z)}')
    res = {}
    for col, lab in (('score_odds', 'odds alone (doc 348 bands)'), ('score_rate', 'rate alone (doc 348 T5 bands, measured on the 114 events)'),
                     ('score_product', 'odds x rate'), ('score_rate_insample', 'rate alone, IN-SAMPLE quartile means'),
                     ('score_product_insample', 'odds x rate, in-sample rate')):
        rho_, p_ = spearman(z[col].values, y, rng)
        res[col] = dict(rho=round(rho_, 4), p=round(p_, 4))
        say(f'  {lab:<58} rho {rho_:+.3f}  p={p_:.4f}')
    # among opened seats only, against realised ppg (a secondary view: what the rate half is for)
    zo = z[z.realised_relief_ppg.notna()]
    say(f'  among the {len(zo)} opened seats with a line, against realised relief PPG:')
    for col, lab in (('score_odds', 'odds alone'), ('score_rate', 'rate alone'), ('score_product', 'odds x rate')):
        rho_, p_ = spearman(zo[col].values, zo.realised_relief_ppg.values, rng)
        res[col + '_opened_ppg'] = dict(rho=round(rho_, 4), p=round(p_, 4))
        say(f'    {lab:<20} rho {rho_:+.3f}  p={p_:.4f}')
    # bootstrap the gap between the product and the better half
    best_half = max(res['score_odds']['rho'], res['score_rate']['rho'])
    gap = res['score_product']['rho'] - best_half
    boots = []
    idx = np.arange(len(z))
    for _ in range(2000):
        bi = rng.choice(idx, size=len(idx), replace=True)
        yy = y[bi]
        ro = float(np.corrcoef(rank(z.score_odds.values[bi]), rank(yy))[0, 1])
        rr = float(np.corrcoef(rank(z.score_rate.values[bi]), rank(yy))[0, 1])
        rp = float(np.corrcoef(rank(z.score_product.values[bi]), rank(yy))[0, 1])
        boots.append(rp - max(ro, rr))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    say(f'\n  product minus the better half: {gap:+.3f} (bootstrap 95% [{lo:+.3f}, {hi:+.3f}], 2,000 draws)')
    verdict = 'THE PRODUCT EARNS ITS PLACE' if gap >= 0.05 else 'DECORATION: rank by odds alone, print the rate as its own column'
    say(f'  KILL CONDITION (product beats the better single instrument by >= 0.05 rho): {verdict}')

    # ---- the deliverable CSV: every seat ---------------------------------------------------------------
    out = r.merge(z[['season', 'team', 't5_quartile', 't5_band', 'score_odds', 'score_rate', 'score_product',
                     'score_rate_insample', 'score_product_insample']], on=['season', 'team'], how='left')
    out = out[['season', 'team', 'lead', 'name', 'wk1_share', 'share_band', 't5', 't5_quartile', 't5_band', 'breadth', 'target_ratio',
               'pre_carries', 'pre_targets', 'opens', 'first_absence', 'absence_weeks', 'relief_weeks_with_line',
               'realised_relief_ppg', 'realised_relief_points', 'score_odds', 'score_rate', 'score_product',
               'score_rate_insample', 'score_product_insample']]
    out = out.sort_values(['season', 'team'])
    out.to_csv(os.path.join(OUT, 'J3_seats_2021_2025.csv'), index=False, float_format='%.4f')
    with open(os.path.join(OUT, 'run_j3_product.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    json.dump(dict(n_seats=int(len(r)), n_with_t5=int(len(z)), step1=dict(rho=round(rho, 4), p=round(p, 4), n=int(len(z))),
                   quartile_cuts=[round(float(q), 4) for q in qs], cells=cells, step3=res, gap=round(float(gap), 4),
                   gap_ci=[round(float(lo), 4), round(float(hi), 4)], verdict=verdict, odds=ODDS, rate_t5=RATE_T5,
                   rate_insample={k: round(float(v), 2) for k, v in qmean.items()}, seed=SEED),
              open(os.path.join(OUT, 'J3_product_summary.json'), 'w'), indent=1)
    say(f'\nwrote J3_seats_2021_2025.csv, J3_product_summary.json, run_j3_product.txt in {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
