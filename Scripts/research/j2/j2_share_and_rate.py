#!/usr/bin/env python3
r"""j2_share_and_rate.py -- JOB 2: the inheritor's share, and whether the relief RATE and WEEKS vary with it.

THE CLAIM IN ITS TESTABLE FORM (REDTEAM_TASKING_PROMPT.md section B, JOB 2 as amended 17 Sept):
  across 2021 to 2025 backfield absences, (1) the usage order's predicted inheritor captures a
  larger share of the vacated carries plus targets than the chart's does, and (2) the relief
  SCORING rate varies with that predicted share.
FALSIFIER, fixed before the run: if the scoring rate is flat across predicted share -- Spearman
  rho with p >= 0.05 AND the 35%-split permutation p >= 0.05, on the page's own predictor (A below)
  -- then the seat lane is right to apply one number (12.13) and JOB 2 closes as a null on its
  second half, whatever the first half shows. The first half is null if the paired mean
  difference in share (usage minus chart) is <= 0 or its one-sided sign-flip p >= 0.05.

POPULATION (0.6, restated): doc 320's events -- every team-week 2021-2025, regular season weeks
  2-14, where the running back who led his team in carries plus targets over the weeks played so
  far played the previous week and has no line this week while his team plays; ONE event per
  absence spell, its first week. Built by the same function b2_depth_order.build_events(), so the
  rows are doc 320's rows. The SPELL is then the run of consecutive team-played weeks from that
  week in which the leader has no line, CAPPED AT WEEK 14 -- the sheet's horizon and the currency
  every seat is priced in. Weeks 15-18 are a sensitivity, not the finding.
THE MEN: chart = the top back on the week-1 depth chart other than the absent man; usage = the
  second back by carries plus targets to date. Each may step past a man with no line in the first
  absence week (the live code steps past a man ESPN lists OUT, doc 296).
OUTCOMES, per man over the spell:
  share  = his carries plus targets in the spell weeks / the team's RB carries plus targets in the
           spell weeks (the pie that is actually redistributed while the leader is out)
  rate   = his half-PPR per game over the spell weeks in which he had a line (the seat's 12.13)
  weeks  = the spell weeks in which he had a line (the seat's 3.02)
PREDICTORS, for the usage man (the page's man since doc 320), each knowable BEFORE the absence:
  A  wk1_share: his share of the team's week-1 RB carries plus targets, the LEADER IN the
     denominator -- doc 300's measure and the column inherit_2026.csv carries (wk1_share).
     Blank, never zero, when he has no week-1 line.
  B  share to date: the same ratio over weeks 1 to w-1.
  C  T5 at week 1: his week-1 offensive snaps / all RB snaps that week EXCLUDING the leader's --
     doc 292's measure, leader OUT of the denominator, so a clean two-man room reads 100%.
  D  T5 to date: the same over weeks 1 to w-1.
  A and B are banded <20 / 20-30 / 30-40 / 40+ (doc 343's bands); C and D at <50 / 50-70 / 70-85 /
  85+ (doc 292's). A and C are run as INDEPENDENT bands on the same rows and every man on whom
  they disagree by two bands or more is listed, on the history and on the live 2026 seat rows.
TESTS: Spearman rho with a permutation p (6,000 draws); band means; the one-sided permutation at a
  35% split (A, B) or a 70% split (C, D), as job_opens.py and doc 292 did, so the numbers compare.
  One seed, one draw of the permutation labels reused across every outcome.
INPUTS: nflverse stats_player_week_2021..2025.csv, depth_charts_2021..2025.csv, games.csv,
  snap_counts_2021..2025.csv (fetched beside the cache if absent), players.csv (pfr id -> gsis
  id for the snap join; a miss falls back to name + team + season, and every miss is printed).
  For the live flags: Source\inherit_2026.csv, research\wk1\stats_player_week_2026.csv and
  snap_counts_2026.csv. pandas + numpy only (0.4).
Run:  py research\j2\j2_share_and_rate.py        (J2_NFLVERSE, J2_OUT, J2_SRC override the paths)
"""
import csv
import importlib.util
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
SRC = os.environ.get('J2_SRC', os.path.normpath(os.path.join(HERE, '..', '..', '..', 'Source')))
WK1 = os.path.normpath(os.path.join(HERE, '..', 'wk1'))
os.environ['B2_NFLVERSE'] = NFL
SEASONS = [2021, 2022, 2023, 2024, 2025]
HORIZON = 14
SEED = 20260918
NPERM = 6000
RELEASE = 'https://github.com/nflverse/nflverse-data/releases/download/'

# ---- doc 320's event builder, imported from its own file so the rows are the same rows ---------
_spec = importlib.util.spec_from_file_location('b2', os.path.join(HERE, '..', 'b2', 'b2_depth_order.py'))
b2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(b2)


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


BANDS4 = ('<20', '20-30', '30-40', '40+')
BANDS5 = ('<50', '50-70', '70-85', '85+')


def load_snaps(season, players):
    """{(team, week, gsis_id): offensive snaps} for RB rows; the join is pfr id -> gsis id via
    players.csv, then name + team as the fallback. Misses are counted and printed, never silent."""
    d = pd.read_csv(need(f'snap_counts_{season}.csv', 'snap_counts'), low_memory=False)
    d = d[(d.game_type == 'REG') & (d.position == 'RB')].copy()
    pfr2gsis = dict(zip(players.pfr_id.dropna(), players.gsis_id[players.pfr_id.notna()]))
    name2gsis = {}
    for g, nm in zip(players.gsis_id, players.display_name):
        name2gsis.setdefault(norm(nm), g)
    out, miss = {}, []
    for r in d.itertuples(index=False):
        g = pfr2gsis.get(r.pfr_player_id) or name2gsis.get(norm(r.player))
        if g is None:
            miss.append((r.player, r.team, int(r.week)))
            continue
        out[(r.team, int(r.week), g)] = out.get((r.team, int(r.week), g), 0) + float(r.offense_snaps or 0)
    if miss:
        print(f'  snap rows with no id in {season}: {len(miss)} of {len(d)} -- e.g. {miss[:4]}')
    return out


def spell_weeks(t, teams_playing, lead, w):
    """Consecutive team-played weeks from w, within the horizon, in which the leader has no line."""
    out = []
    for x in range(w, HORIZON + 1):
        if x not in teams_playing or t not in teams_playing[x]:
            continue                                 # bye: the spell continues past it
        if x in lead:
            break
        out.append(x)
    return out


def rank(a):
    a = np.asarray(a, dtype=float)
    order = a.argsort()
    r = np.empty(len(a)); r[order] = np.arange(1, len(a) + 1)
    # average ranks on ties
    vals, inv, cnt = np.unique(a, return_inverse=True, return_counts=True)
    sums = np.zeros(len(vals)); np.add.at(sums, inv, r)
    return sums[inv] / cnt[inv]


def spearman(x, y, rng, n=NPERM):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx, ry = rank(x), rank(y)
    obs = np.corrcoef(rx, ry)[0, 1]
    c = 0
    for _ in range(n):
        if abs(np.corrcoef(rx, rng.permutation(ry))[0, 1]) >= abs(obs):
            c += 1
    return obs, (c + 1) / (n + 1)


def split_perm(x, y, cut, rng, n=NPERM):
    """One-sided: mean(y | x >= cut) - mean(y | x < cut), permutation on the labels."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    hi, lo = y[x >= cut], y[x < cut]
    if len(hi) < 3 or len(lo) < 3:
        return None
    obs = hi.mean() - lo.mean()
    k, c = len(hi), 0
    for _ in range(n):
        p = rng.permutation(y)
        if p[:k].mean() - p[k:].mean() >= obs:
            c += 1
    return obs, (c + 1) / (n + 1), len(hi), len(lo)


def signflip(d, rng, n=10000):
    d = np.asarray(d, float)
    obs = d.mean()
    c1 = c2 = 0
    for _ in range(n):
        s = (d * rng.choice([-1, 1], size=len(d))).mean()
        if s >= obs:
            c1 += 1
        if abs(s) >= abs(obs):
            c2 += 1
    return obs, (c1 + 1) / (n + 1), (c2 + 1) / (n + 1)


def main():
    rng = np.random.default_rng(SEED)
    games = pd.read_csv(need('games.csv', 'schedules'), low_memory=False)
    players = pd.read_csv(need('players.csv', 'players'), low_memory=False, usecols=['gsis_id', 'display_name', 'pfr_id'])
    names = dict(zip(players.gsis_id, players.display_name))
    rows = []
    for s in SEASONS:
        stats = b2.load_stats(s)
        chart = b2.load_chart(s, games)
        events = b2.build_events(s, stats, chart)
        snaps = load_snaps(s, players)
        rb = stats[stats.position == 'RB'].copy()
        rb['half'] = rb.fantasy_points.fillna(0) + 0.5 * rb.receptions.fillna(0)
        teams_playing = stats.groupby('week').team.apply(set).to_dict()
        for e in events:
            tm, w, lead = e['team'], e['week'], e['lead']
            t = rb[rb.team == tm]
            lead_wks = set(t[t.player_id == lead].week)
            spell = spell_weeks(tm, teams_playing, lead_wks, w)
            spell18 = [x for x in range(w, 19) if (x in teams_playing and tm in teams_playing[x])]
            s18 = []
            for x in spell18:
                if x in lead_wks:
                    break
                s18.append(x)
            pie = t[t.week.isin(spell)]
            pie_tot = float(pie.touch.sum())
            pre = t[t.week < w]
            pre_tot = float(pre.touch.sum())
            pre_wks = sorted(set(pre.week))
            r = dict(season=s, team=tm, week=w, lead=lead, lead_name=names.get(lead, lead),
                     spell_weeks=len(spell), spell_weeks_18=len(s18), spell_first=w,
                     pie_touch=pie_tot, pie_per_week=(pie_tot / len(spell) if spell else 0.0),
                     pre_pie_per_week=(pre_tot / len(pre_wks) if pre_wks else 0.0),
                     lead_share_pre=e['lead_share'], actual=e['actual'], actual_name=names.get(e['actual']),
                     actual_share_first=e['actual_share'], same_man=int(e['pred_chart'] == e['pred_usage']),
                     chart_has_team=e['chart_has_team'])
            # week-1 and to-date shares for every RB on the team, leader in the denominator
            w1 = t[t.week == 1]
            w1_tot = float(w1.touch.sum())
            w1_share = {p: float(g.touch.sum()) / w1_tot for p, g in w1.groupby('player_id')} if w1_tot > 0 else {}
            td_share = {p: float(g.touch.sum()) / pre_tot for p, g in pre.groupby('player_id')} if pre_tot > 0 else {}
            # T5: non-leader snap share, week 1 and to date
            def t5(weeks):
                tot = 0.0; per = {}
                for (tt, ww, g), v in snaps.items():
                    if tt == tm and ww in weeks and g != lead:
                        tot += v; per[g] = per.get(g, 0.0) + v
                return {g: v / tot for g, v in per.items()} if tot > 0 else {}
            t5_w1 = t5({1})
            t5_td = t5(set(pre_wks))
            for tag in ('chart', 'usage'):
                m = e[f'pred_{tag}']
                r[f'{tag}_man'] = m
                r[f'{tag}_name'] = names.get(m)
                if m is None or not spell:
                    for k in ('share', 'rate', 'weeks', 'share_first'):
                        r[f'{tag}_{k}'] = None
                    continue
                mine = pie[pie.player_id == m]
                r[f'{tag}_share'] = (float(mine.touch.sum()) / pie_tot) if pie_tot > 0 else None
                r[f'{tag}_weeks'] = int(len(mine))
                r[f'{tag}_rate'] = (float(mine.half.sum()) / len(mine)) if len(mine) else None
                fm = t[(t.week == w) & (t.player_id == m)]
                wk_tot = float(t[t.week == w].touch.sum())
                r[f'{tag}_share_first'] = (float(fm.touch.sum()) / wk_tot) if wk_tot > 0 else None
                r[f'{tag}_wk1_share'] = w1_share.get(m)              # A: blank when no week-1 line
                r[f'{tag}_td_share'] = td_share.get(m)               # B
                r[f'{tag}_t5_w1'] = t5_w1.get(m)                     # C
                r[f'{tag}_t5_td'] = t5_td.get(m)                     # D
            rows.append(r)
    ev = pd.DataFrame(rows)
    ev.to_csv(os.path.join(OUT, 'J2_events.csv'), index=False)
    lines = []

    def say(*a):
        s = ' '.join(str(x) for x in a)
        print(s); lines.append(s)

    say(f'JOB 2 -- events {len(ev)} (doc 320 construction), {sorted(ev.season.unique().tolist())}, '
        f'spells capped at week {HORIZON}; with a preseason chart {int(ev.chart_has_team.sum())}')
    say(f'  spell length within the horizon: mean {ev.spell_weeks.mean():.2f}, median {ev.spell_weeks.median():.0f}; '
        f'through week 18: mean {ev.spell_weeks_18.mean():.2f}')
    say(f'  the pie while the leader is out is {ev.pie_per_week.mean():.1f} RB carries+targets a week against '
        f'{ev.pre_pie_per_week.mean():.1f} before the absence ({ev.pie_per_week.mean() / ev.pre_pie_per_week.mean():.0%})')

    # ---- FIRST HALF: share of the vacated work, usage against chart, paired ------------------------
    both = ev[ev.chart_share.notna() & ev.usage_share.notna() & (ev.chart_has_team == 1)].copy()
    d = (both.usage_share - both.chart_share).values
    obs, p1, p2 = signflip(d, rng)
    say(f'\nFIRST HALF -- share of the spell pie captured, paired on {len(both)} events with a chart')
    say(f'  chart man {both.chart_share.mean():.3f}   usage man {both.usage_share.mean():.3f}   '
        f'usage minus chart {obs:+.3f}  one-sided sign-flip p={p1:.4f} (two-sided {p2:.4f})')
    dis = both[both.same_man == 0]
    if len(dis):
        o2, q1, q2 = signflip((dis.usage_share - dis.chart_share).values, rng)
        say(f'  the two arms name the same man on {int(both.same_man.sum())} of {len(both)}; on the {len(dis)} where they '
            f'DISAGREE: chart {dis.chart_share.mean():.3f}, usage {dis.usage_share.mean():.3f}, diff {o2:+.3f}, '
            f'one-sided p={q1:.4f}')
    for b, g in both.groupby(pd.cut(both.week, [1, 4, 9, 14], labels=['wk 2-4', 'wk 5-9', 'wk 10-14']), observed=True):
        say(f'    {b}: n={len(g)} chart {g.chart_share.mean():.3f} usage {g.usage_share.mean():.3f} '
            f'diff {(g.usage_share - g.chart_share).mean():+.3f}')
    say(f'  rate over the spell: chart man {both.chart_rate.mean():.2f} a game, usage man {both.usage_rate.mean():.2f}; '
        f'weeks with a line: chart {both.chart_weeks.mean():.2f}, usage {both.usage_weeks.mean():.2f}')
    first_half = obs > 0 and p1 < 0.05
    say(f'  FALSIFIER (usage share > chart share, one-sided p<0.05): {"PASSES -- usage captures more" if first_half else "NULL"}')

    # ---- SECOND HALF: the RATE and the WEEKS against the predicted share ---------------------------
    u = ev[ev.usage_man.notna() & (ev.spell_weeks > 0)].copy()
    say(f'\nSECOND HALF -- the usage man (the page\'s man): {len(u)} events; relief rate on the men who played '
        f'{u.usage_rate.mean():.2f} a game (n={int(u.usage_rate.notna().sum())}; the constant is 12.13), '
        f'weeks with a line {u.usage_weeks.mean():.2f} (constant 3.02), share of the pie {u.usage_share.mean():.3f}')
    # a man with no line in the whole spell scores nothing: rate is None; weeks 0. The RATE test runs on
    # men who played (that is what 12.13 is); the WEEKS test runs on everybody.
    results = {}
    for tag, col, bands, bandf, cut in (('A wk1 share (doc 300, the page column)', 'usage_wk1_share', BANDS4, band4, .35),
                                        ('B share to date', 'usage_td_share', BANDS4, band4, .35),
                                        ('C T5 at week 1 (doc 292, non-leader snaps)', 'usage_t5_w1', BANDS5, band5, .70),
                                        ('D T5 to date', 'usage_t5_td', BANDS5, band5, .70)):
        z = u[u[col].notna()].copy()
        z['band'] = z[col].map(bandf)
        say(f'\n  PREDICTOR {tag}: n={len(z)} with the predictor ({len(u) - len(z)} blank)')
        say(f"  {'band':<7}{'n':>4}{'rate':>7}{'n_rate':>7}{'weeks':>7}{'share':>7}{'startable':>10}")
        for b in bands:
            g = z[z.band == b]
            if not len(g):
                continue
            gr = g[g.usage_rate.notna()]
            say(f"  {b:<7}{len(g):>4}{gr.usage_rate.mean() if len(gr) else float('nan'):>7.2f}{len(gr):>7}"
                f"{g.usage_weeks.mean():>7.2f}{g.usage_share.mean():>7.3f}"
                f"{(gr.usage_rate >= 9.92).mean() if len(gr) else float('nan'):>10.3f}")
        res = {}
        for oc, ocol, sub in (('rate', 'usage_rate', z[z.usage_rate.notna()]), ('weeks', 'usage_weeks', z),
                              ('share', 'usage_share', z)):
            rho, pr = spearman(sub[col], sub[ocol], rng)
            sp = split_perm(sub[col], sub[ocol], cut, rng)
            res[oc] = dict(n=len(sub), rho=round(float(rho), 3), rho_p=round(float(pr), 4),
                           split=None if sp is None else dict(diff=round(float(sp[0]), 3), p=round(float(sp[1]), 4),
                                                             n_hi=sp[2], n_lo=sp[3]))
            sptxt = 'n/a' if sp is None else f'{sp[0]:+.2f} p={sp[1]:.4f} (n {sp[2]} vs {sp[3]})'
            say(f'    {oc:<6} rho {rho:+.3f} p={pr:.4f}   split at {cut:.0%}: {sptxt}')
        results[tag] = res
    A = results['A wk1 share (doc 300, the page column)']
    flat = A['rate']['rho_p'] >= 0.05 and (A['rate']['split'] is None or A['rate']['split']['p'] >= 0.05)
    say(f'\n  FALSIFIER on the RATE against predictor A (rho p and 35%-split p both >= 0.05 = flat): '
        f'{"FLAT -- the seat lane is right to apply one rate; second half NULL" if flat else "NOT FLAT -- the rate varies with the share"}')
    wflat = A['weeks']['rho_p'] >= 0.05 and (A['weeks']['split'] is None or A['weeks']['split']['p'] >= 0.05)
    say(f'  and on the WEEKS: {"flat" if wflat else "NOT flat"} (rho {A["weeks"]["rho"]:+.3f} p={A["weeks"]["rho_p"]:.4f})')

    # ---- A against C: two bands, one man; where do they disagree? ------------------------------------
    z = u[u.usage_wk1_share.notna() & u.usage_t5_w1.notna()].copy()
    z['bandA'] = z.usage_wk1_share.map(band4); z['bandC'] = z.usage_t5_w1.map(band5)
    ia = z.bandA.map({b: i for i, b in enumerate(BANDS4)}); ic = z.bandC.map({b: i for i, b in enumerate(BANDS5)})
    z['band_gap'] = (ia - ic)
    rho_ac, p_ac = spearman(z.usage_wk1_share, z.usage_t5_w1, rng)
    say(f'\nA AGAINST C on the same {len(z)} men: rho {rho_ac:+.3f} (p={p_ac:.4f}); '
        f'same band index {int((z.band_gap == 0).sum())}, off by one {int((z.band_gap.abs() == 1).sum())}, '
        f'off by two or more {int((z.band_gap.abs() >= 2).sum())}')
    far = z[z.band_gap.abs() >= 2].sort_values('band_gap')
    for r in far.itertuples():
        say(f'    {r.season} {r.team} wk{r.week} {r.usage_name:<22} A {r.usage_wk1_share:.2f} ({r.bandA})  '
            f'C {r.usage_t5_w1:.2f} ({r.bandC})  -> rate {r.usage_rate if r.usage_rate is None else round(r.usage_rate, 1)}, '
            f'weeks {r.usage_weeks}, share {r.usage_share:.2f}')
    # which band is right where they disagree: mean rate by (A high, C low) and (A low, C high)
    for lab, sel in (('A high (30%+), C low (<70%)', (z.usage_wk1_share >= .30) & (z.usage_t5_w1 < .70)),
                     ('A low (<30%), C high (70%+)', (z.usage_wk1_share < .30) & (z.usage_t5_w1 >= .70)),
                     ('both high', (z.usage_wk1_share >= .30) & (z.usage_t5_w1 >= .70)),
                     ('both low', (z.usage_wk1_share < .30) & (z.usage_t5_w1 < .70))):
        g = z[sel]; gr = g[g.usage_rate.notna()]
        say(f'    {lab:<30} n={len(g):>3}  rate {gr.usage_rate.mean() if len(gr) else float("nan"):.2f}  '
            f'weeks {g.usage_weeks.mean() if len(g) else float("nan"):.2f}  share {g.usage_share.mean() if len(g) else float("nan"):.3f}')
    z.to_csv(os.path.join(OUT, 'J2_A_vs_C.csv'), index=False)

    # ---- the live 2026 seat rows: A (the page's column) and C side by side ------------------------
    live_flags = live_2026(players, names, say)

    with open(os.path.join(OUT, 'run_j2_share_and_rate.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    import json
    json.dump(dict(n_events=int(len(ev)), n_paired=int(len(both)), first_half=dict(diff=round(float(obs), 4), p_one=round(float(p1), 4),
                   p_two=round(float(p2), 4), passes=bool(first_half)), rate_mean=round(float(u.usage_rate.mean()), 2),
                   weeks_mean=round(float(u.usage_weeks.mean()), 2), share_mean=round(float(u.usage_share.mean()), 3),
                   predictors=results, rate_flat_on_A=bool(flat), weeks_flat_on_A=bool(wflat),
                   A_vs_C=dict(n=int(len(z)), rho=round(float(rho_ac), 3), p=round(float(p_ac), 4),
                               off_two_or_more=int((z.band_gap.abs() >= 2).sum())),
                   live_2026=live_flags, seed=SEED, horizon=HORIZON),
              open(os.path.join(OUT, 'J2_share_summary.json'), 'w'), indent=1)
    say(f'\nwrote J2_events.csv, J2_A_vs_C.csv, J2_live_bands_2026.csv, J2_share_summary.json, run_j2_share_and_rate.txt in {OUT}')
    return 0


def live_2026(players, names, say):
    """The 2026 seat rows with predictor A (the page's wk1_share) and predictor C (T5 week 1) side by side."""
    ip = os.path.join(SRC, 'inherit_2026.csv')
    sp = os.path.join(WK1, 'stats_player_week_2026.csv')
    np_ = os.path.join(WK1, 'snap_counts_2026.csv')
    for p in (ip, sp, np_):
        if not os.path.exists(p):
            say(f'\nLIVE 2026: MISSING INPUT {p} -- the live flags are not run')
            return None
    d = pd.read_csv(sp, low_memory=False)
    d = d[(d.season_type == 'REG') & (d.position == 'RB') & (d.week == 1)].copy()
    d['touch'] = d.carries.fillna(0) + d.targets.fillna(0)
    sn = pd.read_csv(np_, low_memory=False)
    sn = sn[(sn.position == 'RB') & (sn.week == 1)].copy()
    rows = list(csv.DictReader(open(ip, encoding='utf-8-sig')))
    out = []
    # ESPN's club codes against nflverse's: the seat file carries ESPN's (ARZ, LAR, WSH, JAC).
    TEAM = {'ARZ': 'ARI', 'LAR': 'LA', 'WSH': 'WAS', 'JAC': 'JAX'}
    say(f'\nLIVE 2026 SEAT ROWS -- the page\'s A (wk1_share) against C (T5, non-leader week-1 snaps), {len(rows)} rows')
    say(f"  {'next man':<22}{'team':<5}{'A':>6}{'bandA':>7}{'C':>6}{'bandC':>7}  holds the job / note")
    for r in rows:
        tm = TEAM.get(r['team'], r['team'])
        tt = d[d.team == tm]
        tot = float(tt.touch.sum())
        a_mine = None
        for x in tt.itertuples():
            if norm(x.player_display_name) == norm(r['next_man']) and tot > 0:
                a_mine = float(x.touch) / tot
        # A IS THE PAGE'S OWN COLUMN (share_2026() writes it, joined on the name alone); the team-aware
        # recomputation sits beside it and a disagreement is printed, because a name-only join can take
        # a man's share from ANOTHER club's backfield (section 3's identity rule).
        page_a = r.get('wk1_share')
        page_a = float(page_a) if str(page_a or '').strip() else None
        a = page_a
        ss = sn[sn.team == tm]
        lead_norm = norm(r['holds_the_job'])
        lead_rows = ss[ss.player.map(norm) == lead_norm]
        non = ss[ss.player.map(norm) != lead_norm]
        c = None
        ntot = float(non.offense_snaps.sum())
        me = non[non.player.map(norm) == norm(r['next_man'])]
        # T5 needs the leader ON the field that week: with him absent the "non-leader" pool is the whole
        # room and the number is not doc 292's quantity, so it is left blank (a miss is no information).
        if ntot > 0 and len(me) and len(lead_rows):
            c = float(me.offense_snaps.sum()) / ntot
        lead_snaps = lead_rows.offense_snaps.sum() if len(lead_rows) else 0
        note = ''
        if page_a is not None and a_mine is None:
            note = f'PAGE SAYS {page_a:.3f} BUT HE HAS NO WEEK-1 LINE FOR {tm}: name-only join'
        elif page_a is not None and a_mine is not None and abs(page_a - a_mine) > 0.006:
            note = f'PAGE SAYS {page_a:.3f}, team-aware {a_mine:.3f}'
        elif page_a is None and a_mine is not None:
            note = f'page blank, team-aware {a_mine:.3f}'
        if len(ss) and not len(lead_rows):
            note += ' (leader had no week-1 snaps: C blank)'
        ba = band4(a) if a is not None else '-'
        bc = band5(c) if c is not None else '-'
        gap = ''
        if a is not None and c is not None:
            gi = BANDS4.index(ba) - BANDS5.index(bc)
            gap = ' <-- DISAGREE' if abs(gi) >= 2 else ''
        say(f"  {r['next_man']:<22}{tm:<5}{('-' if a is None else f'{a:.2f}'):>6}{ba:>7}{('-' if c is None else f'{c:.2f}'):>6}{bc:>7}  "
            f"{r['holds_the_job']} {r.get('free', '')} {note}{gap}")
        out.append(dict(next_man=r['next_man'], team=tm, holds_the_job=r['holds_the_job'], free=r.get('free'),
                        A_wk1_share_page=page_a, A_team_aware=None if a_mine is None else round(a_mine, 3), bandA=ba,
                        C_t5_wk1=None if c is None else round(c, 3), bandC=bc, disagree=bool(gap),
                        leader_wk1_snaps=int(lead_snaps)))
    pd.DataFrame(out).to_csv(os.path.join(OUT, 'J2_live_bands_2026.csv'), index=False)
    return out


if __name__ == '__main__':
    sys.exit(main())
