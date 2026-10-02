"""price_dst_k_terms.py: price the two scoring omissions doc 435 found and nobody had measured.

ITEM 1, KICKER. dst_k_supply.py line 56 reads
    pts = g('pat_made') * 1 - g('fg_missed') * 1 - g('pat_missed') * 1
and the league does not score a missed PAT (2026_League_Settings.txt, Kicking block: PAT made +1,
FG missed -1, FG 0-39 +3, 40-49 +4, 50+ +5; nothing for a missed PAT). k12_replacement.py, which
produced the published K12 = 8.26, does NOT deduct it (its week_points has no pat_missed term), so
8.26 and the K1 range are not touched by the defect; only the supply curve in dst_k_supply.py is.

TESTABLE FORM 1. Population: nflverse stats_player_week, season_type REG, position K, weeks 1-14,
seasons 2021-2025, kicker-seasons with 8+ games (k12_replacement.py's own population). For each
kicker-season, points per week WITH the deduction minus points per week WITHOUT it equals
-(missed PATs / games). Report the distribution of that difference, then re-run the three published
numbers (K12 by season total, the K1 range, and dst_k_supply.py's usable-kicker curve) both ways.

ITEM 2, D/ST. dst_weekly_2021_2025.csv (build_dst.py) derives sack, int, fr, saf, dtd and the
points-allowed band from play-by-play and carries no blocked-kick term (+2 each) and no
fumble-lost term (-2 each). Both come from nflverse play-by-play.

TESTABLE FORM 2, the definitions, stated before anything is counted:
  BLKK (+2, credited to the DEFENDING unit = nflverse defteam):
      field_goal_result == 'blocked'  OR  extra_point_result == 'blocked'  OR  punt_blocked == 1.
      On a punt nflverse's defteam is the receiving team, which is the team that blocks it.
  FUML (-2, charged to the unit whose RETURN or DEFENSIVE player fumbled it away):
      fumble_lost == 1 and the fumbling team (fumbled_1_team) is the return/defense side:
        kickoff play  -> posteam   (nflverse marks the RECEIVING team as posteam on kickoffs)
        punt play     -> defteam   (the receiving team)
        any other play-> defteam   (a defender fumbling back an interception or fumble return)
      A fumble lost by the offence on a scrimmage play is the player's, not the unit's, and is not
      charged here. A fumble by the kicking team on its own kick (bad snap) is counted separately
      as a sensitivity line and NOT folded into the term.
  Each term's size is its mean per D/ST-week. The published 5.46 / 6.28 / n=2,576 and 5.99
  (D/ST12, weeks 1-14, ranked by per-game mean, mean of the five seasons; that is the definition
  that reproduces 5.99 exactly from the shipped file) are recomputed with both terms added.

FOUND WHILE JOINING, and reported separately: build_dst.py only writes a row for a team-week in
which the defence recorded at least one sack, interception, recovery, safety or TD, so team-weeks
where the score is the points-allowed band alone are ABSENT from the shipped file (the "acc" dict
is only populated by events). This script rebuilds every team-week from play-by-play the same way,
proves it reproduces the shipped 2,576 rows exactly, and then reports the full set as well.
Two more omissions fell out of the same pass and are priced as asides only: kickoff-return TDs
(td_team == posteam on a kickoff, which build_dst.py's "td_team != posteam" test excludes) and
punt-coverage fumble recoveries (the punting team recovering a muff; build_dst.py requires the
recovering team to be defteam).

Inputs, all beside this file: dst_weekly_2021_2025.csv (copied from Source), stats_player_week_
{2021..2025}.csv (copied from Scripts/research/_nflverse_cache), play_by_play_{season}.csv.gz
(downloaded from nflverse and cached beside this file). Standard library plus pandas and numpy.
"""
import collections
import gzip
import os
import statistics as st
import sys
import urllib.request

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'run_price_dst_k_terms.txt')
SEASONS = (2021, 2022, 2023, 2024, 2025)
PBP_URL = 'https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_{}.csv.gz'
LINES = []


def say(s=''):
    print(s)
    LINES.append(s)


# ----------------------------------------------------------------------------------------------
# ITEM 1: the kicker missed-PAT deduction
# ----------------------------------------------------------------------------------------------
FG = {'fg_made_0_19': 3, 'fg_made_20_29': 3, 'fg_made_30_39': 3,
      'fg_made_40_49': 4, 'fg_made_50_59': 5, 'fg_made_60_': 5}


def load_kickers(wmax):
    rows = []
    for yr in SEASONS:
        _sp = os.path.join(HERE, f'stats_player_week_{yr}.csv')
        if not os.path.exists(_sp):                  # the research cache build_form.py keeps
            _sp = os.path.join(HERE, '_nflverse_cache', f'stats_player_week_{yr}.csv')
        k = pd.read_csv(_sp, low_memory=False)
        k = k[(k['position'] == 'K') & (k['season_type'] == 'REG') & (k['week'].between(1, wmax))].copy()
        g = lambda c: pd.to_numeric(k.get(c, 0), errors='coerce').fillna(0)
        base = g('pat_made') * 1 - g('fg_missed') * 1
        for c, v in FG.items():
            base = base + g(c) * v
        k['pts_league'] = base                      # the league's rules (k12_replacement.py)
        k['pts_deduct'] = base - g('pat_missed')    # dst_k_supply.py line 56
        k['pat_missed'] = g('pat_missed')
        k['fg_blocked'] = g('fg_blocked')
        k['season'] = yr
        k = k.rename(columns={'player_display_name': 'unit'})
        rows.append(k[['season', 'week', 'unit', 'pts_league', 'pts_deduct', 'pat_missed', 'fg_blocked']])
    return pd.concat(rows, ignore_index=True)


def k_replacement(kk, col):
    """k12_replacement.py: weeks 1-14, 8+ games, ranked by season TOTAL, K1 and K12 per season."""
    k1s, k12s, ns = [], [], []
    for yr, s in kk.groupby('season'):
        t = s.groupby('unit')[col].agg(['sum', 'mean', 'size'])
        t = t[t['size'] >= 8].sort_values('sum', ascending=False)
        k1s.append(t.iloc[0]['mean']); k12s.append(t.iloc[11]['mean']); ns.append(len(t))
    return k1s, k12s, ns


def supply_curve(df, bar, col):
    """dst_k_supply.py's curve, verbatim: usable in week W = averages >= bar over W..W+3."""
    out = []
    for w in range(1, 15):
        counts = []
        for yr, s in df.groupby('season'):
            win = s[s['week'].between(w, w + 3)]
            if win.empty:
                continue
            m = win.groupby('unit')[col].mean()
            counts.append(int((m >= bar).sum()))
        if counts:
            out.append((w, np.mean(counts)))
    early = np.mean([c for w, c in out if w <= 5])
    late = np.mean([c for w, c in out if w >= 10])
    return out, early, late


def item1():
    say('=' * 96)
    say('ITEM 1: dst_k_supply.py deducts missed PATs; the league does not score them')
    say('=' * 96)
    say("defect line: dst_k_supply.py line 56:  pts = g('pat_made') * 1 - g('fg_missed') * 1 - g('pat_missed') * 1")
    say("k12_replacement.py week_points() has NO pat_missed term, so 8.26 and the K1 range were computed correctly.")
    say()
    k14 = load_kickers(14)
    # one row per kicker-week (dst_k_supply.py dedups the same way)
    k14 = k14.sort_values('pts_league', ascending=False).groupby(['season', 'week', 'unit'], as_index=False).first()
    ks = k14.groupby(['season', 'unit']).agg(games=('week', 'size'), pm=('pat_missed', 'sum'),
                                             fgb=('fg_blocked', 'sum'),
                                             league=('pts_league', 'mean'), deduct=('pts_deduct', 'mean'))
    ks = ks[ks['games'] >= 8].copy()
    ks['diff'] = ks['deduct'] - ks['league']
    n = len(ks)
    say(f'population: kicker-seasons, REG weeks 1-14, 8+ games, 2021-2025: n = {n} '
        f'({", ".join(str(int(v)) for v in ks.groupby(level=0).size())} by season)')
    say(f'missed PATs per kicker-season: mean {ks["pm"].mean():.2f}, max {int(ks["pm"].max())}; '
        f'{(ks["pm"] == 0).mean() * 100:.0f}% of kicker-seasons missed none')
    say(f'per-week difference (deducting minus league rules): mean {ks["diff"].mean():+.3f}, '
        f'median {ks["diff"].median():+.3f}, worst {ks["diff"].min():+.3f} '
        f'({ks["diff"].idxmin()[1]} {ks["diff"].idxmin()[0]}), '
        f'{(ks["diff"] <= -0.25).sum()} of {n} kicker-seasons move by 0.25 or more')
    say()
    for col, label in (('pts_league', 'league rules (no PAT deduction), as k12_replacement.py'),
                       ('pts_deduct', 'WITH the deduction, as dst_k_supply.py line 56')):
        k1s, k12s, ns = k_replacement(k14, col)
        say(f'  {label}:')
        say(f'    K1 by season  {[round(float(x), 2) for x in k1s]}  range {min(k1s):.2f} to {max(k1s):.2f}')
        say(f'    K12 by season {[round(float(x), 2) for x in k12s]}  REPLACEMENT = {st.mean(k12s):.2f} a week, '
            f'sd {st.pstdev(k12s):.2f}, n={len(k12s)} seasons ({ns} rosterable kickers)')
    say()
    # dst_k_supply.py's curve: weeks 1-17, bar 8.26, window W..W+3
    k17 = load_kickers(17)
    k17 = k17.sort_values('pts_league', ascending=False).groupby(['season', 'week', 'unit'], as_index=False).first()
    say(f'dst_k_supply.py kicker curve (weeks 1-17 rows n = {len(k17)}, bar 8.26, window W to W+3):')
    for col, label in (('pts_deduct', 'as shipped (deducting)'), ('pts_league', 'corrected (league rules)')):
        out, early, late = supply_curve(k17, 8.26, col)
        say(f'  {label:<26} weeks 1-5 {early:.1f} usable ({max(0, early - 12):.1f} free)   '
            f'weeks 10-14 {late:.1f} usable ({max(0, late - 12):.1f} free)   '
            f'week by week {[round(float(c), 1) for w, c in out]}')
    say()
    say(f'aside, NOT ESTABLISHED: nflverse fg_missed EXCLUDES blocked field goals (fg_blocked is a separate '
        f'column); whether ESPN\'s "Total FG Missed" counts a block is not in the settings file. Size if it '
        f'does: {ks["fgb"].sum() / ks["games"].sum():.3f} a week per kicker '
        f'({int(ks["fgb"].sum())} blocks over {int(ks["games"].sum())} kicker-weeks).')
    say()


# ----------------------------------------------------------------------------------------------
# ITEM 2: the D/ST blocked-kick and fumble-lost terms
# ----------------------------------------------------------------------------------------------
BANDS = [(0, 0, 10), (1, 6, 7), (7, 13, 4), (14, 17, 1), (18, 21, 0),
         (22, 27, -1), (28, 34, -4), (35, 45, -7), (46, 999, -10)]


def pa_points(pts):
    for lo, hi, v in BANDS:
        if lo <= pts <= hi:
            return v
    return -10


PBP_COLS = ['season', 'week', 'season_type', 'game_id', 'play_type', 'posteam', 'defteam', 'home_team',
            'away_team', 'total_home_score', 'total_away_score', 'sack', 'interception', 'safety',
            'fumble_lost', 'fumbled_1_team', 'fumble_recovery_1_team', 'touchdown', 'td_team',
            'field_goal_result', 'extra_point_result', 'punt_blocked']


def fetch_pbp(yr):
    path = os.path.join(HERE, f'play_by_play_{yr}.csv.gz')
    if not os.path.exists(path) or os.path.getsize(path) < 1_000_000:
        print(f'downloading {path}')
        urllib.request.urlretrieve(PBP_URL.format(yr), path)
    with gzip.open(path, 'rt', encoding='utf-8', errors='replace') as fh:
        p = pd.read_csv(fh, usecols=PBP_COLS, low_memory=False)
    p = p[p['season_type'] == 'REG'].copy()
    if p.empty:
        raise SystemExit(f'{path}: no REG rows, the download is bad')
    return p


def rebuild(yr, p):
    """Every team-week, build_dst.py's terms reproduced plus the new ones."""
    f = lambda c: pd.to_numeric(p[c], errors='coerce').fillna(0)
    acc = collections.defaultdict(collections.Counter)
    p = p.assign(f_sack=f('sack'), f_int=f('interception'), f_saf=f('safety'), f_fl=f('fumble_lost'),
                 f_td=f('touchdown'), f_pb=f('punt_blocked'))
    for r in p.itertuples(index=False):
        wk = int(r.week)
        d = r.defteam if isinstance(r.defteam, str) else None
        o = r.posteam if isinstance(r.posteam, str) else None
        if d:
            k = (wk, d)
            if r.f_sack: acc[k]['sack'] += 1
            if r.f_int: acc[k]['int'] += 1
            if r.f_saf: acc[k]['saf'] += 1
            if r.f_fl and r.fumble_recovery_1_team == d: acc[k]['fr'] += 1
            # NEW: blocked FG / PAT / punt, credited to defteam
            if r.field_goal_result == 'blocked': acc[k]['blk'] += 1
            if r.extra_point_result == 'blocked': acc[k]['blk'] += 1
            if r.f_pb: acc[k]['blk'] += 1
        if r.f_td:
            tdt = r.td_team if isinstance(r.td_team, str) else None
            if tdt and o and tdt != o:
                acc[(wk, tdt)]['dtd'] += 1
            # aside: a kickoff-return TD by the receiving team (posteam on a kickoff)
            if tdt and o and r.play_type == 'kickoff' and tdt == o:
                acc[(wk, tdt)]['krtd'] += 1
        if r.f_fl and isinstance(r.fumbled_1_team, str):
            ft = r.fumbled_1_team
            if r.play_type == 'kickoff':
                unit = o              # receiving team returns the kickoff
            else:
                unit = d              # punt: receiving team is defteam; scrimmage: the defence
            if ft == unit:
                acc[(wk, ft)]['fuml'] += 1
            elif r.play_type in ('punt', 'kickoff', 'field_goal', 'extra_point'):
                acc[(wk, ft)]['fuml_kick_side'] += 1   # sensitivity only: the kicking unit's own fumble
            # aside: punt-coverage recovery (punting team = posteam recovers the muff)
            if r.play_type == 'punt' and r.fumble_recovery_1_team == o and ft == d:
                acc[(wk, o)]['fr_st'] += 1
    finals, opp = {}, {}
    for r in p[['week', 'home_team', 'away_team', 'total_home_score', 'total_away_score']].itertuples(index=False):
        wk = int(r.week)
        h, a = r.home_team, r.away_team
        if isinstance(h, str) and isinstance(a, str):
            opp[(wk, h)] = a; opp[(wk, a)] = h
            if pd.notna(r.total_home_score) and pd.notna(r.total_away_score):
                finals[(wk, h)] = max(finals.get((wk, h), 0), int(float(r.total_home_score)))
                finals[(wk, a)] = max(finals.get((wk, a), 0), int(float(r.total_away_score)))
    rows = []
    for (wk, team), o in sorted(opp.items()):
        allowed = finals.get((wk, o))
        if allowed is None:
            continue
        c = acc.get((wk, team), collections.Counter())
        base = c['sack'] * 1 + c['int'] * 2 + c['fr'] * 2 + c['saf'] * 4 + c['dtd'] * 6 + pa_points(allowed)
        rows.append({'season': yr, 'week': wk, 'team': team, 'opp': o, 'allowed': allowed,
                     'sack': c['sack'], 'int': c['int'], 'fr': c['fr'], 'saf': c['saf'], 'dtd': c['dtd'],
                     'blk': c['blk'], 'fuml': c['fuml'], 'fuml_kick_side': c['fuml_kick_side'],
                     'krtd': c['krtd'], 'fr_st': c['fr_st'],
                     'had_event': int(bool(c['sack'] or c['int'] or c['fr'] or c['saf'] or c['dtd'])),
                     'pts_base': base, 'pts_adj': base + 2 * c['blk'] - 2 * c['fuml']})
    return pd.DataFrame(rows)


def dst12(df, col, wmax=14, rankby='mean'):
    """Doc 265's D/ST12: weeks 1-14, ranked by per-game mean, mean over the five seasons."""
    vals = []
    for yr, s in df[df['week'] <= wmax].groupby('season'):
        t = s.groupby('team')[col].agg(['sum', 'mean']).sort_values(rankby, ascending=False)
        vals.append(t.iloc[11]['mean'])
    return st.mean(vals), vals


def item2():
    say('=' * 96)
    say('ITEM 2: dst_weekly_2021_2025.csv has no blocked-kick term and no fumble-lost term')
    say('=' * 96)
    say("defect: build_dst.py lines 31-41 count sack, int, fr, saf, dtd only; line 66 sums those plus the band.")
    say("BLKK  = field_goal_result == 'blocked' | extra_point_result == 'blocked' | punt_blocked == 1, +2 to defteam")
    say("FUML  = fumble_lost == 1 by the return/defense side (kickoff: posteam; punt: defteam; else: defteam), -2")
    say()
    _dw = os.path.join(HERE, 'dst_weekly_2021_2025.csv')
    if not os.path.exists(_dw):                      # on the drive it lives in Source\, beside the docs
        _dw = os.path.normpath(os.path.join(HERE, '..', '..', 'Source', 'dst_weekly_2021_2025.csv'))
    shipped = pd.read_csv(_dw)
    full = pd.concat([rebuild(yr, fetch_pbp(yr)) for yr in SEASONS], ignore_index=True)
    full.to_csv(os.path.join(HERE, 'dst_weekly_2021_2025_with_terms.csv'), index=False)
    # 1. prove the rebuild reproduces the shipped object row for row (0.2: test the production object)
    m = shipped.merge(full, on=['season', 'week', 'team'], how='left', suffixes=('', '_re'))
    assert m['pts_base'].notna().all(), 'shipped rows the rebuild could not find'
    mism = int((m['dst_pts'] != m['pts_base']).sum())
    say(f'rebuild check: {len(shipped)} shipped rows, {mism} whose dst_pts differs from the rebuilt base points '
        f'(must be 0), and {len(full)} team-weeks exist in play-by-play, so '
        f'{len(full) - len(shipped)} team-weeks are ABSENT from the shipped file '
        f'(every one has had_event = 0: {int((~full.set_index(["season","week","team"]).index.isin(shipped.set_index(["season","week","team"]).index)).sum())} absent, '
        f'{int(full[~full.set_index(["season","week","team"]).index.isin(shipped.set_index(["season","week","team"]).index)]["had_event"].sum())} of them with an event)')
    if mism:
        say(m[m['dst_pts'] != m['pts_base']][['season', 'week', 'team', 'dst_pts', 'pts_base']].head(20).to_string())
    say()

    def block(df, label):
        n = len(df)
        say(f'--- {label}: n = {n} D/ST-weeks ---')
        say(f'  blocked kicks: {int(df["blk"].sum())} total, {df["blk"].mean():.4f} per D/ST-week, '
            f'= {2 * df["blk"].mean():+.3f} points a week; {(df["blk"] > 0).mean() * 100:.1f}% of weeks have one')
        say(f'  fumbles lost by the unit: {int(df["fuml"].sum())} total, {df["fuml"].mean():.4f} per D/ST-week, '
            f'= {-2 * df["fuml"].mean():+.3f} points a week; {(df["fuml"] > 0).mean() * 100:.1f}% of weeks have one '
            f'(kicking-side own fumbles, not charged: {int(df["fuml_kick_side"].sum())})')
        say(f'  net of both terms: {2 * df["blk"].mean() - 2 * df["fuml"].mean():+.3f} points a week')
        say(f'  week mean / sd  base {df["pts_base"].mean():.2f} / {df["pts_base"].std(ddof=0):.2f}   '
            f'with both terms {df["pts_adj"].mean():.2f} / {df["pts_adj"].std(ddof=0):.2f}')
        for rankby in ('mean', 'sum'):
            b, bv = dst12(df, 'pts_base', rankby=rankby)
            a, av = dst12(df, 'pts_adj', rankby=rankby)
            say(f'  D/ST12 (weeks 1-14, ranked by per-game {rankby}, mean of 5 seasons)  '
                f'base {b:.2f} {[round(float(x), 2) for x in bv]}   with terms {a:.2f} {[round(float(x), 2) for x in av]}')
        d = df.rename(columns={'team': 'unit'})
        for col, bar, label2 in (('pts_base', 5.99, 'base, bar 5.99'),
                                 ('pts_adj', 5.99, 'with terms, bar 5.99'),
                                 ('pts_adj', round(dst12(df, 'pts_adj')[0], 2), 'with terms, its own D/ST12 bar')):
            out, early, late = supply_curve(d[d['week'] <= 17], bar, col)
            say(f'  dst_k_supply.py DEFENSES curve, {label2:<32} weeks 1-5 {early:.1f} usable '
                f'({max(0, early - 12):.1f} free)   weeks 10-14 {late:.1f} usable ({max(0, late - 12):.1f} free)')
        say(f'  asides, outside the two terms: kickoff-return TDs build_dst.py misses: {int(df["krtd"].sum())} '
            f'({6 * df["krtd"].mean():+.3f} a week); punt-coverage recoveries it misses: {int(df["fr_st"].sum())} '
            f'({2 * df["fr_st"].mean():+.3f} a week)')
        say()

    block(full[full.set_index(['season', 'week', 'team']).index.isin(shipped.set_index(['season', 'week', 'team']).index)],
          'ON THE SHIPPED 2,576 ROWS (the published population)')
    block(full, 'ON EVERY TEAM-WEEK IN PLAY-BY-PLAY (adds the event-less weeks build_dst.py drops)')
    absent = full[~full.set_index(['season', 'week', 'team']).index.isin(shipped.set_index(['season', 'week', 'team']).index)]
    say(f'the absent team-weeks: n = {len(absent)}, mean base points {absent["pts_base"].mean():.2f} '
        f'(all are the points-allowed band alone), by season {absent.groupby("season").size().to_dict()}')
    say(f'2022 has {int((full["season"] == 2022).sum())} team-weeks, not 544: BUF at CIN week 17 was cancelled.')
    say()


def main():
    item1()
    item2()
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(LINES) + '\n')
    print(f'wrote {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
