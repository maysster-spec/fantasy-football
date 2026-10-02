"""vegas_streams.py: do Vegas lines improve the three STREAMING picks (D/ST, K, QB)
over the season-average opponent generosity the pages use today?  (doc 437 section 6 item 6)

POPULATION, stated here and not inherited (section 0.6):
    nflverse games.csv, seasons 2021-2025, game_type REG, weeks 1-17 (week 18 dropped on purpose:
    the task scopes weeks 1-17; the league's own season ends at 14 and playoffs run 15-17).
    Every one of the 1,359 REG games 2021-2025 carries spread_line, total_line and both moneylines.
    Sign convention, checked two ways in check_sign_convention():
        nflreadr data dictionary: "spread_line: A positive number means the home team was favored by
        that many points ... lines up with the result column"; result = home_score minus away_score.
        Inspection: when home_moneyline < away_moneyline (home favoured) spread_line > 0 in 99.5% of
        games; corr(spread_line, result) = +0.46.
    Implied team total: implied_team = total_line/2 + spread_team/2, where spread_team is the team's
    own expected margin (spread_line for the home side, minus spread_line for the away side).
    So a 10-point home favourite in a 52.5 game is implied 31.25, the dog 21.25; the two sum to the total.
    The file carries ONE line per game; the dictionary does not say opening or closing.  Treated as the
    pregame line and called that throughout.  Whether it is the close is NOT ESTABLISHED.

    D/ST points: Source\\dst_weekly_2021_2025.csv as rebuilt by doc 440/441, column dst_pts (base band+sack+int+fr+saf
    +TD PLUS the blocked-kick +2 and fumble-lost -2 terms), ALL 2,718 team-weeks in play-by-play.
    NOT the shipped Source\\dst_weekly_2021_2025.csv, which is missing 142 event-less team-weeks.
    QB and K points: nflverse stats_player_week_{season}.csv scored under THIS league's rules:
        QB  0.04/pass yd, 6/pass TD, -2/INT, 0.1/rush yd, 6/rush TD, -2/fumble lost, +2 any 2-pt.
        K   PAT 1, FG 0-39 = 3, 40-49 = 4, 50+ = 5, FG missed -1 (no missed-PAT deduction).
    A QB game = a row with 10+ attempts (mop-up men out), as doc 435's audit used.

STREAMABLE, ex ante, prior weeks only.  The RANK is taken among everyone with a season-to-date average
as of that week (bye teams included), because the top 12 are rostered whether or not they play; the
POOL is the streamable men who play this week:
    D/ST: rank 13-32 among the 32 units by season-to-date mean pts_adj over weeks before this one,
          needing 2+ prior games; pool = those playing this week.
    K:    rank 13-32 among kickers with 2+ prior games AND a game in one of the two prior weeks (so a
          replaced kicker drops out of the ranking); pool = those kicking this week.
    QB:   rank 13-24 among QBs with 3+ prior games of 10+ attempts AND a game in one of the two prior
          weeks (a benched or hurt man does not hold a rank); pool = those with 10+ attempts this week
          (that condition is applied to every rule alike, so the comparison BETWEEN rules is fair,
          though the pool mean itself is a touch generous to all of them).

PICK RULES, each week, within the pool (ties split by averaging the tied men):
    line rule:     D/ST lowest opponent implied total; QB and K highest own-team implied total.
    season rule:   D/ST lowest opponent season-to-date points scored (what a season-average page knows),
                   and as a sensitivity the opponent's season-to-date D/ST points ALLOWED to defences;
                   QB softest matchup = opponent's season-to-date QB points allowed per game, prior weeks
                   only (doc 427's rule as doc 435 re-ran it ex ante);
                   K the opponent's season-to-date K points allowed (a sensitivity; no page rule exists).
    both:          rank-sum of the line rule and the season rule (lowest sum wins).
    random:        the pool mean, which is the expected value of a uniform draw.
    The reported se of each mean is over season-weeks; the paired difference's se is over the same weeks.

FALSIFIERS (set before running): a rule is worth wiring if it beats random by 1.0 a week with se under
0.5; the line replaces the season rule only if it beats it by 0.5 a week.

    py vegas_streams.py          writes run_vegas_streams.txt beside this file

Standard library plus pandas and numpy; paths resolve against this file, never the shell.
"""
import os
import sys
import urllib.request

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
GAMES_URL = 'https://github.com/nflverse/nflverse-data/releases/download/schedules/games.csv'
GAMES_CSV = os.path.join(HERE, 'games.csv')
# On the drive: Scripts\research\vegas_streams.py, so Source is ..\..\Source and the weekly stats are the research cache.
# dst_weekly_2021_2025.csv is the doc 440/441 rebuild: all 2,718 team-weeks with blk and fuml, dst_pts the full score.
DST_CSV = os.path.normpath(os.path.join(HERE, '..', '..', 'Source', 'dst_weekly_2021_2025.csv'))
STATS_DIR = os.path.join(HERE, '_nflverse_cache')
OUT = os.path.join(HERE, 'run_vegas_streams.txt')
SEASONS = (2021, 2022, 2023, 2024, 2025)
WEEKS = (1, 17)
WIRE_GAIN, WIRE_SE, REPLACE_GAIN = 1.0, 0.5, 0.5

LINES = []


def say(s=''):
    LINES.append(s)
    print(s)


# ------------------------------------------------------------------ games and lines
def load_games():
    if not os.path.exists(GAMES_CSV):
        urllib.request.urlretrieve(GAMES_URL, GAMES_CSV)
    g = pd.read_csv(GAMES_CSV, low_memory=False)
    g = g[(g.season.isin(SEASONS)) & (g.game_type == 'REG') & (g.week.between(*WEEKS))].copy()
    need = ['spread_line', 'total_line', 'home_moneyline', 'away_moneyline', 'home_score', 'away_score']
    miss = g[need].isna().sum()
    assert miss.sum() == 0, f'missing line fields:\n{miss}'
    return g


def check_sign_convention(g):
    say('SIGN CONVENTION (games.csv, 2021-2025 REG weeks 1-17, n=%d games)' % len(g))
    res_ok = ((g.home_score - g.away_score) == g.result).mean()
    home_fav = g.home_moneyline < g.away_moneyline
    share_pos = (g.loc[home_fav, 'spread_line'] > 0).mean()
    say('  result == home minus away in %.1f%% of games; when the home moneyline is shorter the spread_line '
        'is positive in %.1f%%; corr(spread_line, result) = %+.3f'
        % (100 * res_ok, 100 * share_pos, g.spread_line.corr(g.result)))
    say('  => spread_line = home minus away expected margin, positive = home favoured (matches the nflreadr '
        'dictionary text: "a positive number means the home team was favored").')
    say('  implied_team = total_line/2 + spread_team/2, spread_team = the side\'s own expected margin')
    ex = g[(g.season == 2021) & (g.week == 1)].head(3)
    for _, r in ex.iterrows():
        hi = r.total_line / 2 + r.spread_line / 2
        ai = r.total_line / 2 - r.spread_line / 2
        say('     %d wk%d %s at %s: spread %+.1f total %.1f -> implied home %.2f away %.2f (sum %.1f); '
            'actual %d-%d' % (r.season, r.week, r.away_team, r.home_team, r.spread_line, r.total_line,
                              hi, ai, hi + ai, r.home_score, r.away_score))
    assert abs(share_pos - 1) < 0.02 and res_ok > 0.999


def team_games(g):
    """Two rows per game: the team's own line, implied total, opponent implied total, scores."""
    h = pd.DataFrame({'season': g.season, 'week': g.week, 'team': g.home_team, 'opp': g.away_team,
                      'home': 1, 'spread_team': g.spread_line, 'total_line': g.total_line,
                      'pts_for': g.home_score, 'pts_against': g.away_score,
                      'moneyline': g.home_moneyline})
    a = pd.DataFrame({'season': g.season, 'week': g.week, 'team': g.away_team, 'opp': g.home_team,
                      'home': 0, 'spread_team': -g.spread_line, 'total_line': g.total_line,
                      'pts_for': g.away_score, 'pts_against': g.home_score,
                      'moneyline': g.away_moneyline})
    t = pd.concat([h, a], ignore_index=True)
    t['implied_team'] = t.total_line / 2 + t.spread_team / 2
    t['implied_opp'] = t.total_line / 2 - t.spread_team / 2
    # the implied totals must sum to the total and the favourite must carry the larger one
    assert np.allclose(t.implied_team + t.implied_opp, t.total_line)
    fav = t[t.spread_team > 0]
    assert (fav.implied_team > fav.implied_opp).all()
    r_for = t.implied_team.corr(t.pts_for)
    say('  implied_team vs actual points scored, all team-games n=%d: Pearson %+.3f; implied_opp vs points '
        'allowed %+.3f (a positive check that the formula points the right way)'
        % (len(t), r_for, t.implied_opp.corr(t.pts_against)))
    return t


def prior_mean(df, keys, col):
    """Season-to-date mean of col over PRIOR weeks (shifted expanding mean) and the prior game count."""
    df = df.sort_values(keys + ['week']).copy()
    grp = df.groupby(keys)[col]
    df[col + '_prior'] = grp.transform(lambda s: s.shift().expanding().mean())
    df['n_prior'] = grp.cumcount()
    return df


def rank_as_of(df, idcol, min_prior, recent=None):
    """For every season-week w, rank every id by its mean pts over weeks < w (n_prior games needed);
    recent=k keeps only ids whose last game was within the k prior weeks.  Returns one row per
    (season, week, id) with pts_prior, n_prior, rank (1 = best)."""
    out = []
    for season, d in df.groupby('season'):
        for w in range(WEEKS[0] + 1, WEEKS[1] + 1):
            pri = d[d.week < w].groupby(idcol).agg(pts_prior=('pts', 'mean'), n_prior=('pts', 'size'),
                                                     last=('week', 'max')).reset_index()
            pri = pri[pri.n_prior >= min_prior]
            if recent is not None:
                pri = pri[pri['last'] >= w - recent]
            pri['rank'] = pri.pts_prior.rank(ascending=False, method='min')
            pri['season'] = season
            pri['week'] = w
            out.append(pri.drop(columns=['last']))
    return pd.concat(out, ignore_index=True)


# ------------------------------------------------------------------ pick-rule machinery
def spearman(x, y):
    x, y = pd.Series(x), pd.Series(y)
    m = x.notna() & y.notna()
    return x[m].rank().corr(y[m].rank()), int(m.sum())


def pick_value(pool, col, lowest):
    """Points of the man the rule picks; ties averaged."""
    v = pool[col]
    target = v.min() if lowest else v.max()
    return pool.loc[v == target, 'pts'].mean()


def run_rules(pool_df, rules, label, pool_min=3):
    """pool_df: one row per candidate-week with columns season, week, pts and each rule's column.
    rules: dict name -> (column, lowest_bool).  Returns the per-week frame."""
    rows = []
    for (season, week), pool in pool_df.groupby(['season', 'week']):
        if len(pool) < pool_min:
            continue
        row = {'season': season, 'week': week, 'n_pool': len(pool), 'random': pool.pts.mean()}
        for name, (col, lowest) in rules.items():
            p = pool.dropna(subset=[col])
            row[name] = pick_value(p, col, lowest) if len(p) else np.nan
        rows.append(row)
    w = pd.DataFrame(rows)
    say('%s: n=%d season-weeks, pool %.1f men a week, seasons %s'
        % (label, len(w), w.n_pool.mean(), sorted(w.season.unique())))
    return w


def se(x):
    x = pd.Series(x).dropna()
    return x.std(ddof=1) / np.sqrt(len(x))


def report_rules(w, order, base_name):
    say('  %-34s %7s %6s %9s %6s' % ('rule', 'mean', 'se', 'vs random', 'se'))
    for name in order:
        d = w[name] - w['random']
        say('  %-34s %7.2f %6.2f %+9.2f %6.2f' % (name, w[name].mean(), se(w[name]), d.mean(), se(d)))
    say('  %-34s %7.2f %6.2f' % ('random (pool mean)', w['random'].mean(), se(w['random'])))
    if base_name:
        d = w[order[0]] - w[base_name]
        wins = (w[order[0]] > w[base_name]).sum()
        loss = (w[order[0]] < w[base_name]).sum()
        tie = len(w) - wins - loss
        say('  line rule minus %s: %+.2f a week, se %.2f; line wins %d, loses %d, same pick or tie %d '
            '(%.0f%% of decided weeks)' % (base_name, d.mean(), se(d), wins, loss, tie,
                                           100 * wins / max(1, wins + loss)))
    by = w.groupby('season')[order + ['random']].mean().round(2)
    say('  by season:')
    for s, r in by.iterrows():
        say('    %d  ' % s + '  '.join('%s %.2f' % (k, r[k]) for k in order + ['random']))


def verdict(w, line, season_rule, sd_pick=None):
    """Two readings of the wire bar.  LITERAL: gain >= 1.0 and se < 0.5.  The se of a pick's mean over
    n weeks cannot fall below sd(pick)/sqrt(n) whatever the rule does, so the literal bar is reported
    against that floor.  T-READING: gain >= 1.0 and gain >= 2 se (the interval clears zero by two se),
    which is what 'se under half the gain' means once the gain is bigger than 1.0."""
    g_line = w[line] - w['random']
    g_seas = w[season_rule] - w['random']
    d = w[line] - w[season_rule]
    n = len(w)
    if sd_pick is None:                      # the sd of the line pick's weekly points, the floor's input
        sd_pick = float(w[line].std(ddof=1))
    floor = sd_pick / np.sqrt(n)
    lit = lambda g: g.mean() >= WIRE_GAIN and se(g) < WIRE_SE
    tr = lambda g: g.mean() >= WIRE_GAIN and g.mean() >= 2 * se(g)
    repl = d.mean() >= REPLACE_GAIN
    say('  FALSIFIER: wire needs +%.1f over random with se < %.1f (literal) or gain >= 2 se (t-reading); '
        'replace needs +%.1f over the season rule.  se floor at n=%d with a pick sd of %.1f is %.2f, so the '
        'literal se bar is %s at this n.' % (WIRE_GAIN, WIRE_SE, REPLACE_GAIN, n, sd_pick, floor,
                                             'attainable' if floor < WIRE_SE else 'UNATTAINABLE by any rule'))
    say('    line over random        %+.2f (se %.2f, t %+.1f) -> literal %s, t-reading %s'
        % (g_line.mean(), se(g_line), g_line.mean() / se(g_line), 'PASS' if lit(g_line) else 'fail',
           'PASS' if tr(g_line) else 'fail'))
    say('    season rule over random %+.2f (se %.2f, t %+.1f) -> literal %s, t-reading %s'
        % (g_seas.mean(), se(g_seas), g_seas.mean() / se(g_seas), 'PASS' if lit(g_seas) else 'fail',
           'PASS' if tr(g_seas) else 'fail'))
    say('    line over season rule   %+.2f (se %.2f, t %+.1f) -> %s'
        % (d.mean(), se(d), d.mean() / se(d), 'PASS' if repl else 'fail'))
    if tr(g_line) and repl:
        v = 'WIRE THE LINE (t-reading; literal se bar %s)' % ('met' if lit(g_line) else 'not met')
    elif tr(g_seas):
        v = 'KEEP THE SEASON AVERAGE (the season rule clears random on the t-reading and the line does not beat it by %.1f)' % REPLACE_GAIN
    elif tr(g_line):
        v = 'WIRE THE LINE as the only rule that clears random (t-reading), with no season rule to replace'
    else:
        v = 'NEITHER clears random'
    say('  VERDICT: ' + v)
    return v


# ------------------------------------------------------------------ T1 D/ST
def t1_dst(tg):
    say()
    say('=' * 100)
    say('T1  D/ST.  Testable form: among streamable defences (rank 13-32 by season-to-date mean, 2+ prior')
    say('    games, playing this week), the unit facing the LOWEST opponent implied total scores more D/ST')
    say('    points than the unit facing the lowest opponent season-to-date points scored, and than random.')
    say('    Points = dst_pts from Source/dst_weekly_2021_2025.csv as rebuilt by doc 441 (all 2,718 team-weeks, blocked')
    say('    kicks and fumbles lost included), NOT the shipped Source file that drops 142 event-less weeks.')
    say('=' * 100)
    d = pd.read_csv(DST_CSV)
    d = d[d.season.isin(SEASONS) & d.week.between(*WEEKS)].copy()
    d = d.rename(columns={'dst_pts': 'pts'})[['season', 'week', 'team', 'opp', 'pts']]   # dst_pts == pts_adj on the rebuilt file
    say('  D/ST-weeks after the week filter: n=%d (%d per season: %s)'
        % (len(d), d.groupby('season').size().iloc[0], d.groupby('season').size().tolist()))
    # season-to-date own average (prior weeks) and rank among the 32
    d = prior_mean(d, ['season', 'team'], 'pts')
    # opponent offence: season-to-date points scored (prior weeks), from games.csv
    off = prior_mean(tg[['season', 'week', 'team', 'pts_for']].copy(), ['season', 'team'], 'pts_for')
    off = off.rename(columns={'team': 'opp', 'pts_for_prior': 'opp_pts_scored_prior'})[
        ['season', 'week', 'opp', 'opp_pts_scored_prior']]
    # opponent offence: season-to-date D/ST points ALLOWED to defences (prior weeks)
    allowed = d[['season', 'week', 'opp', 'pts']].rename(columns={'pts': 'dst_allowed'})
    allowed = prior_mean(allowed, ['season', 'opp'], 'dst_allowed')[
        ['season', 'week', 'opp', 'dst_allowed_prior']].rename(columns={'dst_allowed_prior': 'opp_dst_allowed_prior'})
    x = d.merge(tg[['season', 'week', 'team', 'implied_opp', 'implied_team', 'spread_team', 'total_line']],
                on=['season', 'week', 'team'], how='inner')
    assert len(x) == len(d), 'every D/ST-week must find its line'
    x = x.merge(off, on=['season', 'week', 'opp'], how='left').merge(allowed, on=['season', 'week', 'opp'], how='left')
    # Spearman, all D/ST-weeks with a line
    r1, n1 = spearman(x.implied_opp, x.pts)
    r2, n2 = spearman(x.spread_team, x.pts)
    r3, n3 = spearman(x.total_line, x.pts)
    say('  Spearman with D/ST points, ALL D/ST-weeks n=%d: opponent implied total %+.3f; own spread (positive = '
        'the defence\'s team favoured) %+.3f; game total %+.3f' % (n1, r1, r2, r3))
    r4, n4 = spearman(x.opp_pts_scored_prior, x.pts)
    r5, n5 = spearman(x.opp_dst_allowed_prior, x.pts)
    say('  Spearman with D/ST points, weeks with a prior: opponent season-to-date points scored %+.3f (n=%d); '
        'opponent season-to-date D/ST points allowed %+.3f (n=%d)' % (r4, n4, r5, n5))
    # streamable pool
    x['rank'] = x.groupby(['season', 'week'])['pts_prior'].rank(ascending=False, method='min')
    pool = x[(x.n_prior >= 2) & (x['rank'] >= 13)].copy()
    say('  streamable pool: rank 13-32 by prior-weeks mean, 2+ prior games -> %d candidate-weeks, weeks %d-%d'
        % (len(pool), pool.week.min(), pool.week.max()))
    rp1, np1 = spearman(pool.implied_opp, pool.pts)
    rp2, np2 = spearman(pool.spread_team, pool.pts)
    say('  Spearman inside the pool n=%d: opponent implied total %+.3f; own spread %+.3f' % (np1, rp1, rp2))
    rules = {'line: lowest opp implied total': ('implied_opp', True),
             'season: lowest opp pts scored': ('opp_pts_scored_prior', True),
             'season-b: lowest opp D/ST allowed': ('opp_dst_allowed_prior', True),
             'spread: most favoured defence': ('spread_team', False)}
    w = run_rules(pool, rules, '  pick rules')
    order = list(rules)
    report_rules(w, order, 'season: lowest opp pts scored')
    d2 = w[order[0]] - w['season-b: lowest opp D/ST allowed']
    say('  line rule minus season-b (D/ST allowed): %+.2f a week, se %.2f' % (d2.mean(), se(d2)))
    say('  week-by-week, line over season rule (wins-losses-ties):')
    wk = []
    for week, s in w.groupby('week'):
        a, b = s['line: lowest opp implied total'], s['season: lowest opp pts scored']
        wk.append('w%d %d-%d-%d' % (week, (a > b).sum(), (a < b).sum(), (a == b).sum()))
    say('    ' + '  '.join(wk))
    return verdict(w, 'line: lowest opp implied total', 'season: lowest opp pts scored')


# ------------------------------------------------------------------ QB and K weekly loading
def qb_score(d):
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    return (g('passing_yards') * 0.04 + g('passing_tds') * 6 - g('passing_interceptions') * 2
            + g('rushing_yards') * 0.1 + g('rushing_tds') * 6
            - (g('sack_fumbles_lost') + g('rushing_fumbles_lost') + g('receiving_fumbles_lost')) * 2
            + (g('passing_2pt_conversions') + g('rushing_2pt_conversions') + g('receiving_2pt_conversions')) * 2)


def k_score(d):
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    return (g('pat_made') * 1.0
            + (g('fg_made_0_19') + g('fg_made_20_29') + g('fg_made_30_39')) * 3.0
            + g('fg_made_40_49') * 4.0
            + (g('fg_made_50_59') + g('fg_made_60_')) * 5.0
            - g('fg_missed') * 1.0)


def load_weekly(pos):
    out = []
    for yr in SEASONS:
        p = os.path.join(STATS_DIR, f'stats_player_week_{yr}.csv')
        if not os.path.exists(p):
            raise SystemExit('missing ' + p)
        d = pd.read_csv(p, low_memory=False)
        d = d[(d.position == pos) & (d.season_type == 'REG') & (d.week.between(*WEEKS))].copy()
        d['season'] = yr
        d['pts'] = qb_score(d) if pos == 'QB' else k_score(d)
        d['attempts'] = pd.to_numeric(d.get('attempts', 0), errors='coerce').fillna(0)
        out.append(d[['season', 'week', 'player_id', 'player_display_name', 'team', 'opponent_team', 'attempts', 'pts']])
    return pd.concat(out, ignore_index=True).rename(columns={'opponent_team': 'opp'})


# ------------------------------------------------------------------ T2 QB
def t2_qb(tg):
    say()
    say('=' * 100)
    say('T2  QB.  Testable form: among streamable QBs (rank 13-24 by season-to-date mean, 3+ prior games of')
    say('    10+ attempts, playing this week), the man with the HIGHEST own-team implied total scores more than')
    say('    the man with the softest matchup by opponent season-to-date QB points allowed (doc 427 ex ante),')
    say('    and than random; and the rank-sum of both beats either alone.')
    say('=' * 100)
    q = load_weekly('QB')
    allq = q.copy()
    q = q[q.attempts >= 10].copy()
    say('  QB games (10+ attempts) weeks 1-17: n=%d; QB-team-weeks with two such men: %d'
        % (len(q), (q.groupby(['season', 'week', 'team']).size() > 1).sum()))
    q = prior_mean(q, ['season', 'player_id'], 'pts')
    # opponent generosity: ALL QB points allowed by the defence per game, prior weeks (doc 435's definition)
    al = allq.groupby(['season', 'week', 'opp'], as_index=False).pts.sum().rename(columns={'pts': 'qb_allowed'})
    al = prior_mean(al, ['season', 'opp'], 'qb_allowed')[['season', 'week', 'opp', 'qb_allowed_prior']]
    x = q.merge(tg[['season', 'week', 'team', 'implied_team', 'implied_opp', 'spread_team', 'total_line']],
                on=['season', 'week', 'team'], how='inner')
    assert len(x) == len(q), 'every QB game must find its line'
    x = x.merge(al, on=['season', 'week', 'opp'], how='left')
    r1, n1 = spearman(x.implied_team, x.pts)
    r2, n2 = spearman(x.qb_allowed_prior, x.pts)
    r3, n3 = spearman(x.total_line, x.pts)
    say('  Spearman with QB points, all QB games: own implied total %+.3f (n=%d); opponent season-to-date QB '
        'points allowed %+.3f (n=%d); game total %+.3f' % (r1, n1, r2, n2, r3))
    x['rank'] = x[x.n_prior >= 3].groupby(['season', 'week'])['pts_prior'].rank(ascending=False, method='min')
    pool = x[(x.n_prior >= 3) & x['rank'].between(13, 24)].copy()
    say('  streamable pool: rank 13-24 among QBs with 3+ prior games -> %d candidate-weeks, weeks %d-%d, '
        'season-to-date mean of the pool %.2f' % (len(pool), pool.week.min(), pool.week.max(), pool.pts_prior.mean()))
    rp1, _ = spearman(pool.implied_team, pool.pts)
    rp2, _ = spearman(pool.qb_allowed_prior, pool.pts)
    say('  Spearman inside the pool n=%d: own implied total %+.3f; opponent QB points allowed %+.3f; the two '
        'signals with each other %+.3f' % (len(pool), rp1, rp2, spearman(pool.implied_team, pool.qb_allowed_prior)[0]))
    # rank-sum column: rank descending on each (1 = best), sum
    pool['rs'] = (pool.groupby(['season', 'week'])['implied_team'].rank(ascending=False)
                  + pool.groupby(['season', 'week'])['qb_allowed_prior'].rank(ascending=False))
    rules = {'line: highest own implied total': ('implied_team', False),
             'season: softest matchup (doc 427)': ('qb_allowed_prior', False),
             'both: rank-sum of the two': ('rs', True),
             'total: highest game total': ('total_line', False)}
    w = run_rules(pool, rules, '  pick rules')
    order = list(rules)
    report_rules(w, order, 'season: softest matchup (doc 427)')
    for a in ('line: highest own implied total', 'season: softest matchup (doc 427)'):
        d = w['both: rank-sum of the two'] - w[a]
        say('  both minus [%s]: %+.2f a week, se %.2f' % (a, d.mean(), se(d)))
    # reconciliation against doc 427 / 435: full-season tier 13-24 (8+ games), prior-week generosity, weeks 2-17
    say('  reconciliation, doc 435 definitions (tier by FULL-season ppg rank 13-24 with 8+ games, an in-sample '
        'tier; generosity prior weeks only; pools of 2+):')
    tot = x.groupby(['season', 'player_id']).agg(g=('pts', 'size'), ppg=('pts', 'mean')).reset_index()
    tot = tot[tot.g >= 8]
    tot['r'] = tot.groupby('season').ppg.rank(ascending=False, method='first')
    ids = tot[tot.r.between(13, 24)][['season', 'player_id']]
    p2 = x.merge(ids, on=['season', 'player_id']).dropna(subset=['qb_allowed_prior'])
    p2['rs'] = (p2.groupby(['season', 'week'])['implied_team'].rank(ascending=False)
                + p2.groupby(['season', 'week'])['qb_allowed_prior'].rank(ascending=False))
    w2 = run_rules(p2, rules, '    doc-435-style pool', pool_min=2)
    report_rules(w2, order, 'season: softest matchup (doc 427)')
    return verdict(w, 'line: highest own implied total', 'season: softest matchup (doc 427)')


# ------------------------------------------------------------------ T3 K
def t3_k(tg):
    say()
    say('=' * 100)
    say('T3  K.  Testable form: among streamable kickers (rank 13-32 by season-to-date mean, 2+ prior games,')
    say('    kicking this week), the man with the HIGHEST own-team implied total scores more than random.')
    say('    No page rule exists for kickers; the opponent\'s season-to-date K points allowed is run as the')
    say('    season-average stand-in so the replace test has something to bite on.')
    say('=' * 100)
    k = load_weekly('K')
    # one kicker per team-week: the man with the most PAT+FG attempts is the team's kicker that week
    k = k.sort_values('pts', ascending=False).drop_duplicates(['season', 'week', 'team'])
    say('  kicker-weeks (one per team-week, the higher scorer where two kicked) weeks 1-17: n=%d' % len(k))
    k = prior_mean(k, ['season', 'player_id'], 'pts')
    al = k.groupby(['season', 'week', 'opp'], as_index=False).pts.sum().rename(columns={'pts': 'k_allowed'})
    al = prior_mean(al, ['season', 'opp'], 'k_allowed')[['season', 'week', 'opp', 'k_allowed_prior']]
    x = k.merge(tg[['season', 'week', 'team', 'implied_team', 'implied_opp', 'spread_team', 'total_line']],
                on=['season', 'week', 'team'], how='inner')
    say('  kicker-weeks with a line: n=%d (%d dropped: no nflverse opponent or team mismatch)' % (len(x), len(k) - len(x)))
    x = x.merge(al, on=['season', 'week', 'opp'], how='left')
    r1, n1 = spearman(x.implied_team, x.pts)
    r2, n2 = spearman(x.total_line, x.pts)
    r3, n3 = spearman(x.spread_team, x.pts)
    r4, n4 = spearman(x.k_allowed_prior, x.pts)
    say('  Spearman with K points, all kicker-weeks n=%d: own implied total %+.3f; game total %+.3f; own spread '
        '%+.3f; opponent season-to-date K points allowed %+.3f (n=%d)' % (n1, r1, r2, r3, r4, n4))
    x['rank'] = x[x.n_prior >= 2].groupby(['season', 'week'])['pts_prior'].rank(ascending=False, method='min')
    pool = x[(x.n_prior >= 2) & (x['rank'] >= 13)].copy()
    say('  streamable pool: rank 13-32 among kickers with 2+ prior games -> %d candidate-weeks, weeks %d-%d'
        % (len(pool), pool.week.min(), pool.week.max()))
    rp1, _ = spearman(pool.implied_team, pool.pts)
    say('  Spearman inside the pool n=%d: own implied total %+.3f' % (len(pool), rp1))
    pool['rs'] = (pool.groupby(['season', 'week'])['implied_team'].rank(ascending=False)
                  + pool.groupby(['season', 'week'])['k_allowed_prior'].rank(ascending=False))
    rules = {'line: highest own implied total': ('implied_team', False),
             'season: most K pts allowed': ('k_allowed_prior', False),
             'both: rank-sum of the two': ('rs', True),
             'total: highest game total': ('total_line', False)}
    w = run_rules(pool, rules, '  pick rules')
    order = list(rules)
    report_rules(w, order, 'season: most K pts allowed')
    return verdict(w, 'line: highest own implied total', 'season: most K pts allowed')


def main():
    say('vegas_streams.py: do pregame lines beat the season-average matchup on the three streaming picks?')
    say('games.csv cached at %s; D/ST from %s' % (GAMES_CSV, DST_CSV))
    g = load_games()
    check_sign_convention(g)
    tg = team_games(g)
    v1 = t1_dst(tg)
    v2 = t2_qb(tg)
    v3 = t3_k(tg)
    say()
    say('VERDICTS   D/ST: %s   |   QB: %s   |   K: %s' % (v1, v2, v3))
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(LINES) + '\n')
    print('\nwrote', OUT)


if __name__ == '__main__':
    main()
