#!/usr/bin/env python3
"""tail_tickets.py -- which bench ticket, bought at the end of week 4, most often turns into a SEASON-WINNING
stretch? The tail, not the mean. (Matt, 1 Oct: "Just because the average of backups doesn't hit ... doesn't
mean it can't happen and strike big ... I don't feel we are measuring the right thing the right way. The goal
is to take a chance before it is too late.")

THE CLAIM IN TESTABLE FORM: among men a manager could hold on a bench at the end of week 4 (under the position's
startable bar on weeks 1 to 4), the chance of a BIG hit over weeks 5 to 14 differs by the shape of the ticket,
and the backup behind a real job has the fattest tail. Shapes, from the team's own touches per game on weeks 1-4:
  lead back under the bar     the #1 back by touches on his team, 12+ a game, or under 12
  RB committee partner        the #2 back with 8 to 14 touches a game (part of the job already)
  RB handcuff                 the #2 back, under 8 a game, behind a lead at 12+; split by whether the lead's
                              job is top-12 in the league by touches a game
  RB third or lower           the #3 or lower, under 8 a game
  WR young, 3 / 2 / 0-1 of 3  NFL years 1 to 3, the in-season screen's marks on weeks 1-4 (doc 453's builder)
  WR veteran                  year 4+, 2+ targets a game
Outcomes over weeks 5 to 14 (10 weeks, half-PPR): startable weeks (RB 9.92+, WR 9.62+); BIG = 6 or more of the
10; a 150+ point stretch; a 4-week window at 15+ a game (a league-winning month).
nflverse 2021 to 2025 REG; pandas and numpy only. FF_CACHE / FF_SRC as rookie_screen.py. Doc 460.
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rookie_screen as R

W = 4
BAR = {'RB': 9.92, 'WR': 9.62}
ORDER = ['RB lead back under the bar, 12+ a game', 'RB lead back under the bar, under 12 a game',
         'RB committee partner (8-14 a game)', 'RB handcuff, top-12 job', 'RB handcuff, other job',
         'RB third or lower', 'WR young, 3 of 3', 'WR young, 2 of 3', 'WR young, 0 or 1 of 3',
         'WR veteran (year 4+), 2+ targets a game']
KEYS = dict(zip(ORDER, ['lead_12', 'lead_u12', 'committee', 'handcuff_top12', 'handcuff_other', 'third',
                        'wr_3of3', 'wr_2of3', 'wr_01', 'wr_other']))   # the cell names sheet_constants.json carries


def hp(d):
    g = lambda c: pd.to_numeric(d[c], errors='coerce').fillna(0)
    return (0.1 * (g('rushing_yards') + g('receiving_yards')) + 6 * (g('rushing_tds') + g('receiving_tds'))
            + 0.5 * g('receptions') - 2 * (g('rushing_fumbles_lost') + g('receiving_fumbles_lost') + g('sack_fumbles_lost')))


def outcomes(post):
    rows = []
    for (pid, s), g in post.groupby(['player_id', 'season']):
        g = g.sort_values('week')
        pos = g.position.iloc[0]
        pts = g.hppr.values; wk = g.week.values
        best4 = 0.0
        for w0 in range(W + 1, 15 - 3):
            m = (wk >= w0) & (wk < w0 + 4)
            if m.sum() >= 3:
                best4 = max(best4, pts[m].sum() / 4)
        rows.append(dict(player_id=pid, season=s, start_w=int((pts >= BAR[pos]).sum()), pts_post=pts.sum(),
                         g_post=len(g), best4=best4))
    return pd.DataFrame(rows)


def cell(c):
    return (f'n={len(c):>4}  mean pts {c.pts_post.mean():5.1f}  4+ wks {(c.start_w >= 4).mean():5.1%}  '
            f'6+ wks {(c.start_w >= 6).mean():5.1%}  150+ {(c.pts_post >= 150).mean():5.1%}  '
            f'15+ month {(c.best4 >= 15).mean():5.1%}')


def main():
    d = pd.concat([pd.read_csv(R._get(f'stats_player_week_{s}.csv', R.NFLV + f'stats_player/stats_player_week_{s}.csv'),
                               low_memory=False) for s in range(2021, 2026)])
    d = d[(d.season_type == 'REG') & (d.week <= 14) & (d.position.isin(['RB', 'WR']))].copy()
    d['hppr'] = hp(d)
    for c in ('carries', 'targets', 'receiving_yards'):
        d[c] = pd.to_numeric(d[c], errors='coerce').fillna(0)
    d['touch'] = d.carries + d.targets
    pre, post = d[d.week <= W], d[d.week > W]
    out = outcomes(post)
    names = d[['player_id', 'player_display_name']].drop_duplicates('player_id')

    # --- the backs, by their team's touches on weeks 1-4
    rb = pre[pre.position == 'RB'].groupby(['player_id', 'season', 'team']).agg(
        g=('week', 'nunique'), touch=('touch', 'sum'), pts=('hppr', 'sum')).reset_index()
    rb['tpg'] = rb.touch / rb.g; rb['ppg'] = rb.pts / rb.g
    if '--last-game' in sys.argv:
        # [doc 464] THE SHAPE READ OFF THE TEAM'S LAST GAME BEFORE THE CUT instead of the four-week average (4.38's
        # level). TESTED: it does not separate the cells more cleanly (lead 12+ 25.7% a month against 28.1%, committee
        # 13.2% against 13.6%, handcuff top-12 0% four-plus against 5.7%) and only 72% of men land in the same cell under
        # the two readings, so the average stays the shipped reading and this flag is the record of the test.
        tmax = pre.groupby(['season', 'team']).week.max().rename('tw').reset_index()
        lg = pre.merge(tmax, on=['season', 'team'])
        lg = lg[lg.week == lg.tw].groupby(['player_id', 'season', 'team']).touch.sum().rename('lg').reset_index()
        rb = rb.merge(lg, on=['player_id', 'season', 'team'], how='left').fillna({'lg': 0.0})
        rb['tpg'] = rb.lg
        print('(shape read off the team\'s last game before the cut, --last-game)')
    rb['rank'] = rb.groupby(['season', 'team'])['tpg'].rank(ascending=False, method='first')
    lead = rb[rb['rank'] == 1][['season', 'team', 'player_id', 'tpg']].rename(columns={'tpg': 'lead_tpg', 'player_id': 'lead_id'})
    lead['job_rank'] = lead.groupby('season')['lead_tpg'].rank(ascending=False, method='first')
    rb = rb.merge(lead, on=['season', 'team'])
    rb = rb[rb.ppg < BAR['RB']]

    def rb_type(r):
        if r['rank'] == 1:
            return 'RB lead back under the bar, 12+ a game' if r.tpg >= 12 else 'RB lead back under the bar, under 12 a game'
        if r['rank'] == 2 and r.lead_tpg >= 12 and r.tpg < 8:
            return 'RB handcuff, top-12 job' if r.job_rank <= 12 else 'RB handcuff, other job'
        if r['rank'] == 2 and 8 <= r.tpg < 14:
            return 'RB committee partner (8-14 a game)'
        if r['rank'] >= 3 and r.tpg < 8:
            return 'RB third or lower'
        return None
    rb['ticket'] = rb.apply(rb_type, axis=1)
    rb = rb[rb.ticket.notna()]

    # --- the receivers: doc 453's builder at week 4 (young, with the marks), and the veterans
    full = R.load()
    a = R.table(full, W)
    a = a[a.ppg_pre < BAR['WR']].copy()
    a['ticket'] = np.where(a.sig == 3, 'WR young, 3 of 3', np.where(a.sig == 2, 'WR young, 2 of 3', 'WR young, 0 or 1 of 3'))
    vet = pre[pre.position == 'WR'].groupby(['player_id', 'season']).agg(g=('week', 'nunique'), tgt=('targets', 'sum'), pts=('hppr', 'sum')).reset_index()
    vet['ppg'] = vet.pts / vet.g; vet['tpg'] = vet.tgt / vet.g
    vet = vet[(vet.ppg < BAR['WR']) & (vet.tpg >= 2) & (~vet.player_id.isin(full.player_id.unique()))].copy()
    vet['ticket'] = 'WR veteran (year 4+), 2+ targets a game'
    tickets = pd.concat([rb[['player_id', 'season', 'ticket']], a[['player_id', 'season', 'ticket']], vet[['player_id', 'season', 'ticket']]])
    x = tickets.merge(out, on=['player_id', 'season'], how='left')
    x[['start_w', 'pts_post', 'g_post', 'best4']] = x[['start_w', 'pts_post', 'g_post', 'best4']].fillna(0)

    print(f'(a) bench tickets at the end of week {W}, 2021 to 2025, outcomes over weeks 5 to 14 (10 weeks):')
    computed = {}
    for t in ORDER:
        c = x[x.ticket == t]
        if len(c):
            print(f'  {t:<46}{cell(c)}')
            computed[KEYS[t]] = dict(n=int(len(c)), big=round(float((c.start_w >= 6).mean()), 3),
                                     month=round(float((c.best4 >= 15).mean()), 3), four=round(float((c.start_w >= 4).mean()), 3))
    big = x[(x.start_w >= 6) & x.ticket.str.startswith('RB') & ~x.ticket.str.contains('lead')].merge(names, on='player_id')
    print('  the non-lead back tickets that hit 6+ startable weeks: ' + '; '.join(
        f"{r.player_display_name} {int(r.season)} ({r.ticket.split(',')[0].replace('RB ', '')}, {int(r.start_w)} wks, {r.pts_post:.0f} pts)"
        for r in big.sort_values('pts_post', ascending=False).itertuples()))
    bigw = x[(x.start_w >= 6) & (x.ticket == 'WR young, 3 of 3')].merge(names, on='player_id')
    print('  the 3-of-3 receivers that hit 6+: ' + '; '.join(f"{r.player_display_name} {int(r.season)} ({int(r.start_w)} wks, {r.pts_post:.0f})" for r in bigw.itertuples()))

    # --- (b) the handcuff when the starter goes down
    lead_g = post[post.position == 'RB'].groupby(['player_id', 'season']).apply(lambda g: int((g.touch >= 3).sum())).rename('lead_g').reset_index().rename(columns={'player_id': 'lead_id'})
    hc = rb[rb.ticket.str.startswith('RB handcuff')].merge(lead_g, on=['lead_id', 'season'], how='left')
    hc['lead_g'] = hc.lead_g.fillna(0)
    hc = hc.merge(out, on=['player_id', 'season'], how='left').fillna({'start_w': 0, 'pts_post': 0, 'best4': 0})
    print('\n(b) the handcuff, split by whether his lead back played 7+ of weeks 5 to 14 (3+ touches a game):')
    print(f'  {"starter missed 3+ of the 10":<46}{cell(hc[hc.lead_g < 7])}')
    print(f'  {"starter played 7+":<46}{cell(hc[hc.lead_g >= 7])}')
    print(f'  share of handcuffs whose starter missed 3+: {(hc.lead_g < 7).mean():.1%} of {len(hc)}')

    # --- (c) where the league-winning stretches come from
    allpre = pre.groupby(['player_id', 'season']).agg(g=('week', 'nunique'), pts=('hppr', 'sum')).reset_index()
    allpre['ppg'] = allpre.pts / allpre.g
    big_all = out[out.start_w >= 6].merge(d[['player_id', 'position']].drop_duplicates('player_id'), on='player_id')
    big_all = big_all.merge(allpre, on=['player_id', 'season'], how='left').merge(tickets, on=['player_id', 'season'], how='left')

    def state(r):
        if pd.isna(r.g):
            return 'did not play weeks 1-4 (returning man)'
        if r.ppg >= BAR[r.position]:
            return 'already startable on weeks 1-4'
        return r.ticket if isinstance(r.ticket, str) else 'under the bar, no ticket shape'
    big_all['state'] = big_all.apply(state, axis=1)
    print('\n(c) every back and receiver with 6+ startable weeks over weeks 5 to 14, by where he was at the end of week 4:')
    for pos in ('RB', 'WR'):
        c = big_all[big_all.position == pos]
        print(f'  {pos}: n={len(c)}')
        for k, v in c.state.value_counts().items():
            print(f'     {k:<46}{v:>4}  ({v / len(c):.0%})')
    if '--check' in sys.argv:
        # [doc 463] THE CONSTANTS ARE RE-FIT AND GUARDED, the way blend_weight.py --check guards BLEND_W:
        # every cell in sheet_constants.json's tail_tickets block must equal what this run computes.
        import json
        p = os.path.join(R.SRC if hasattr(R, 'SRC') else os.environ.get('FF_SRC', '.'), 'sheet_constants.json')
        held = (json.load(open(p, encoding='utf-8')).get('tail_tickets') or {}).get('cells') or {}
        drift = []
        for k, v in computed.items():
            h = held.get(k) or {}
            for f in ('n', 'big', 'month', 'four'):
                if h.get(f) is None or abs(float(h[f]) - float(v[f])) > (0.5 if f == 'n' else 0.0051):
                    drift.append(f'{k}.{f}: file {h.get(f)} computed {v[f]}')
        if drift:
            print('\nCHECK FAILED: sheet_constants.json tail_tickets drifts from this run:\n  ' + '\n  '.join(drift))
            return 1
        print(f'\ncheck: every tail_tickets cell in sheet_constants.json matches this run ({len(computed)} cells)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
