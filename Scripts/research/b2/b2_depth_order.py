#!/usr/bin/env python3
r"""b2_depth_order.py -- catalog B2: does the usage order name the inheritor better than the
preseason chart does?

THE CLAIM IN ITS TESTABLE FORM, written before the run (0.5a2):
  POPULATION: every team-week 2021-2025, regular season weeks 2-14, where the running back who led
  his team in carries plus targets over the weeks played so far (the usage leader to date) played
  the previous week and has no line this week while his team plays. One event per absence spell:
  its first week only, because from the second week on the usage order already contains the
  inheritor's relief work and the comparison would be rigged.
  OUTCOME: the running back on that team with the most carries plus targets in the absence week.
  PREDICTORS, each naming one man before the week is played:
    chart  -- the official week-1 depth chart (nflverse depth_charts; the 3 Sept snapshot for 2025),
              the top back on it other than the absent man
    usage  -- the second back by carries plus targets over the weeks played so far
    weekly -- the official depth chart as published THAT week (a third arm nobody asked for, and the
              one the wire could actually consume in-season)
  Each arm may step past a man who has no line in the absence week, because the live code already
  steps past a man ESPN lists OUT (doc 296); a no-stepping version is run as a sensitivity.
FALSIFIER, fixed before the run: usage must name the inheritor at least 5 points more often than
  the week-1 chart on the same events, with McNemar p under 0.05. Otherwise the preseason chart
  stays as the wire's source and the usage rebuild is not worth shipping.
PAIRED: the same events are scored under every arm; the test is on the discordant pairs.

Inputs: nflverse stats_player_week_<season>.csv, depth_charts_<season>.csv, games.csv (week dates for
the 2025 snapshots). pandas only.
"""
import json, math, os, sys, urllib.request
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
# On the drive the weekly files already live in Scripts\research\_nflverse_cache\ (2022-2025).
# Anything missing there (2021, the depth charts, the schedule) is fetched once from nflverse and
# kept beside them. A fetch that fails says so and stops; it never runs on a partial set (doc 309).
NFL = os.environ.get('B2_NFLVERSE', os.path.normpath(os.path.join(HERE, '..', '_nflverse_cache')))
OUT = os.environ.get('B2_OUT', HERE)
SEASONS = [2021, 2022, 2023, 2024, 2025]
WEEKS = range(2, 15)
SNAP_2025_PRESEASON = '2025-09-03'          # the day before the 2025 opener
RELEASE = 'https://github.com/nflverse/nflverse-data/releases/download/'


def need(name, release):
    """Path to a cached nflverse file, fetching it if absent. Refuses a tiny (error-page) file."""
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
            sys.exit(f'{name} came back {os.path.getsize(p)} bytes from {url}; not a data file. Stopping.')
    return p


def load_stats(season):
    d = pd.read_csv(need(f'stats_player_week_{season}.csv', 'player_stats'), low_memory=False)
    d = d[(d.season_type == 'REG') & (d.week <= 18)].copy()
    d['touch'] = d.carries.fillna(0) + d.targets.fillna(0)
    return d


def load_chart(season, games):
    """{(team, week): [gsis ids in depth order]} for RB rows, plus (team, 0) = the preseason order."""
    p = need(f'depth_charts_{season}.csv', 'depth_charts')
    d = pd.read_csv(p, low_memory=False)
    out = {}
    if 'depth_team' in d.columns:                                  # 2021-2024 format
        d = d[(d.game_type == 'REG') & (d.depth_position == 'RB') & d.gsis_id.notna()]
        d = d.sort_values(['club_code', 'week', 'depth_team'])
        for (tm, wk), g in d.groupby(['club_code', 'week']):
            ids = list(dict.fromkeys(g.gsis_id.tolist()))
            out[(tm, int(wk))] = ids
        for tm in {k[0] for k in out}:
            first = min(w for (t, w) in out if t == tm)
            out[(tm, 0)] = out[(tm, first)]                         # preseason = the week-1 chart
    else:                                                          # 2025 daily-snapshot format
        d = d[(d.pos_abb == 'RB') & d.gsis_id.notna()].copy()
        d['day'] = d.dt.str[:10]
        days = sorted(d.day.unique())
        wkday = games[(games.season == season) & (games.game_type == 'REG')].groupby('week').gameday.min()
        def snap_before(day):
            prior = [x for x in days if x <= day]
            return prior[-1] if prior else days[0]
        for tm, g in d.groupby('team'):
            byday = {day: gg.sort_values('pos_rank').gsis_id.tolist() for day, gg in g.groupby('day')}
            def order(day):
                s = snap_before(day)
                while s not in byday:
                    i = days.index(s)
                    if i == 0:
                        return []
                    s = days[i - 1]
                return list(dict.fromkeys(byday[s]))
            out[(tm, 0)] = order(SNAP_2025_PRESEASON)
            for wk, gd in wkday.items():
                out[(tm, int(wk))] = order(str(gd)[:10])
    return out


def first_playing(order, absent, played, step=True):
    for pid in order:
        if pid == absent:
            continue
        if not step or pid in played:
            return pid
    return None


def build_events(season, stats, chart, window=None):
    """One row per absence event with the three predictions and the outcome."""
    rb = stats[stats.position == 'RB']
    teams_playing = stats.groupby('week').team.apply(set).to_dict()
    rows = []
    for tm in sorted(rb.team.unique()):
        t = rb[rb.team == tm]
        weekly = {w: g for w, g in t.groupby('week')}
        for w in WEEKS:
            if w not in teams_playing or tm not in teams_playing[w]:
                continue                                           # bye or no data
            prior = t[t.week < w]
            if prior.empty:
                continue
            cum = prior.groupby('player_id').agg(touch=('touch', 'sum'), carries=('carries', 'sum')) \
                       .sort_values(['touch', 'carries'], ascending=False)
            if cum.empty or cum.touch.iloc[0] <= 0:
                continue
            lead = cum.index[0]
            here = weekly.get(w, t.iloc[0:0])
            played_here = set(here.player_id)
            if lead in played_here:
                continue
            # first week of the spell only: he must have had a line the previous week his team played
            prev_weeks = [x for x in range(1, w) if tm in teams_playing.get(x, set())]
            if not prev_weeks or lead not in set(weekly.get(prev_weeks[-1], t.iloc[0:0]).player_id):
                continue
            if here.empty or here.touch.max() <= 0:
                continue
            actual = here.sort_values(['touch', 'carries', 'targets'], ascending=False).player_id.iloc[0]
            # the usage orders
            usage_all = [p for p in cum.index if cum.loc[p, 'touch'] > 0]
            last3 = prior[prior.week >= max(1, w - 3)].groupby('player_id').touch.sum() \
                         .sort_values(ascending=False)
            last3 = [p for p in last3.index if last3[p] > 0]
            last1 = prior[prior.week == prev_weeks[-1]].groupby('player_id').touch.sum() \
                         .sort_values(ascending=False)
            last1 = [p for p in last1.index if last1[p] > 0]
            pre = chart.get((tm, 0), [])
            wkc = chart.get((tm, w), [])
            r = dict(season=season, team=tm, week=w, lead=lead, actual=actual,
                     lead_on_chart_top=int(bool(pre) and pre[0] == lead),
                     lead_share=round(float(cum.touch.iloc[0] / cum.touch.sum()), 3),
                     n_backs_used=int((cum.touch > 0).sum()),
                     chart_has_team=int(bool(pre)), weekly_has_team=int(bool(wkc)))
            for tag, order in (('chart', pre), ('usage', usage_all), ('last3', last3),
                               ('last1', last1), ('weekly', wkc)):
                r[f'pred_{tag}'] = first_playing(order, lead, played_here, step=True)
                r[f'pred_{tag}_nostep'] = first_playing(order, lead, played_here, step=False)
                r[f'hit_{tag}'] = int(r[f'pred_{tag}'] == actual)
                r[f'hit_{tag}_nostep'] = int(r[f'pred_{tag}_nostep'] == actual)
            # the inheritor's share of the backfield that week, so a hit means something
            r['actual_share'] = round(float(here.touch.max() / here.touch.sum()), 3)
            rows.append(r)
    return rows


def mcnemar(a, b):
    """Exact McNemar on paired 0/1 outcomes: p for the discordant split, two-sided."""
    n01 = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    n10 = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    n = n01 + n10
    if n == 0:
        return n01, n10, 1.0
    k = min(n01, n10)
    p = sum(math.comb(n, i) for i in range(0, k + 1)) / (2 ** n)
    return n01, n10, min(1.0, 2 * p)


def report(ev, label, out):
    n = len(ev)
    lines = [f'\n{label}: n={n} events']
    rates = {}
    for tag in ('chart', 'usage', 'last3', 'last1', 'weekly'):
        h = ev[f'hit_{tag}'].mean()
        hn = ev[f'hit_{tag}_nostep'].mean()
        rates[tag] = round(float(h), 4)
        lines.append(f'  {tag:<7} names the inheritor {h:6.1%}   (no stepping: {hn:6.1%})')
    for a, b in (('chart', 'usage'), ('chart', 'weekly'), ('usage', 'weekly'), ('chart', 'last3'),
                 ('usage', 'last3'), ('usage', 'last1')):
        n01, n10, p = mcnemar(ev[f'hit_{a}'].tolist(), ev[f'hit_{b}'].tolist())
        d = (ev[f'hit_{b}'].mean() - ev[f'hit_{a}'].mean()) * 100
        lines.append(f'  {b} minus {a}: {d:+.1f} points; {a} only {n10}, {b} only {n01}; '
                     f'McNemar p={p:.4f}')
    out.extend(lines)
    print('\n'.join(lines))
    return rates


def main():
    games = pd.read_csv(need('games.csv', 'schedules'), low_memory=False)
    allrows = []
    for s in SEASONS:
        stats = load_stats(s)
        chart = load_chart(s, games)
        rows = build_events(s, stats, chart)
        print(f'{s}: {len(rows)} events, teams with a preseason chart '
              f'{len({k[0] for k in chart if k[1] == 0})}')
        allrows.extend(rows)
    ev = pd.DataFrame(allrows)
    # players' names for the reader
    names = {}
    for s in SEASONS:
        d = pd.read_csv(need(f'stats_player_week_{s}.csv', 'player_stats'), low_memory=False,
                        usecols=['player_id', 'player_display_name'])
        names.update(dict(zip(d.player_id, d.player_display_name)))
    for c in ('lead', 'actual', 'pred_chart', 'pred_usage', 'pred_weekly', 'pred_last3', 'pred_last1'):
        ev[c + '_name'] = ev[c].map(names)
    ev.to_csv(os.path.join(OUT, 'B2_events.csv'), index=False)

    out = ['B2 -- usage order against the preseason chart, first week of every lead-back absence',
           'POPULATION: usage leader to date, played last week, no line this week, team played; '
           f'weeks 2-14, 2021-2025. n={len(ev)}']
    print('\n'.join(out))
    ev_c = ev[ev.chart_has_team == 1]
    summary = {'n_all': int(len(ev)), 'n_with_chart': int(len(ev_c))}
    summary['all'] = report(ev_c, 'ALL EVENTS WITH A PRESEASON CHART', out)
    n01, n10, p = mcnemar(ev_c.hit_chart.tolist(), ev_c.hit_usage.tolist())
    gain = (ev_c.hit_usage.mean() - ev_c.hit_chart.mean()) * 100
    verdict = gain >= 5 and p < 0.05
    summary.update(usage_minus_chart_points=round(float(gain), 1), mcnemar_p=round(float(p), 5),
                   falsifier_passed=bool(verdict))
    out.append(f'\nFALSIFIER (usage ahead by 5+ points, McNemar p<0.05): gain {gain:+.1f}, p={p:.4f} -> '
               f'{"USAGE WINS" if verdict else "CHART STAYS"}')
    print(out[-1])
    # by week band, by season, by whether the chart already had the lead on top
    ev_c = ev_c.assign(band=pd.cut(ev_c.week, [1, 4, 9, 14], labels=['wk 2-4', 'wk 5-9', 'wk 10-14']))
    summary['by_band'] = {}
    for b, g in ev_c.groupby('band', observed=True):
        summary['by_band'][str(b)] = report(g, f'BAND {b}', out)
    summary['by_season'] = {}
    for s, g in ev_c.groupby('season'):
        summary['by_season'][int(s)] = report(g, f'SEASON {s}', out)
    summary['lead_was_chart_top'] = {}
    for k, g in ev_c.groupby('lead_on_chart_top'):
        summary['lead_was_chart_top'][int(k)] = report(
            g, 'LEAD WAS THE CHART\'S #1' if k else 'LEAD WAS NOT THE CHART\'S #1', out)
    # how often the two arms name the SAME man, and what happens when they disagree
    same = (ev_c.pred_chart == ev_c.pred_usage)
    dis = ev_c[~same]
    lines = [f'\nAGREEMENT: chart and usage name the same man in {same.mean():.1%} of events '
             f'({same.sum()} of {len(ev_c)}). When they DISAGREE (n={len(dis)}): chart right '
             f'{dis.hit_chart.mean():.1%}, usage right {dis.hit_usage.mean():.1%}, neither '
             f'{((dis.hit_chart == 0) & (dis.hit_usage == 0)).mean():.1%}']
    summary['agree_share'] = round(float(same.mean()), 4)
    summary['disagree'] = {'n': int(len(dis)), 'chart_right': round(float(dis.hit_chart.mean()), 4),
                           'usage_right': round(float(dis.hit_usage.mean()), 4)}
    # the size of the inheritor's job when each arm is right or wrong
    lines.append(f"inheritor's share of the backfield touches that week: median {ev_c.actual_share.median():.0%}")
    out.extend(lines)
    print('\n'.join(lines))
    # week-2 cell on its own, because that is the live situation on 16 Sept
    w2 = ev_c[ev_c.week == 2]
    summary['week2'] = report(w2, 'WEEK 2 ONLY (one game of usage, the live situation this week)', out)
    dis.to_csv(os.path.join(OUT, 'B2_disagreements.csv'), index=False)
    with open(os.path.join(OUT, 'run_b2_20260916.txt'), 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out) + '\n')
    json.dump(summary, open(os.path.join(OUT, 'B2_summary.json'), 'w'), indent=1)
    print('\nwrote B2_events.csv, B2_disagreements.csv, B2_summary.json, run_b2_20260916.txt')


if __name__ == '__main__':
    main()
