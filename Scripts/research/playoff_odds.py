#!/usr/bin/env python3
"""playoff_odds.py -- his probability of a top-six finish over the weeks left, with and without a big hit (doc 464).

Doc 463 named this as the unit a ticket should be priced in: the objective is dollars against the payout table (0.3),
and the question Matt asked on 1 Oct ("9th in points is not going to cut it ... I need to take this chance now") is
whether a chance taken now gets him into six of twelve. This simulates the rest of the regular season.

THE MODEL, stated so it can be judged: each team's weekly score is drawn Normal(m_i, s), where m_i is the team's
average to date shrunk toward the league average (k prior weeks' worth, default 4) and s is the pooled within-team
weekly spread measured on this league's history. The remaining matchups come from the schedule file. Standings are
wins, then points for (ESPN's default tie-break). Top six make the playoffs. 20,000 draws.

INPUTS: Source\\schedule_2026.csv (wire.py writes it off ESPN's matchup view: week, home, away, home_pts, away_pts) and
Source\\standings_2026.csv (which team is his). The spread s comes from historical_scoreboard_2022_2025.csv.

    py research\\playoff_odds.py                 the live season (needs schedule_2026.csv)
    py research\\playoff_odds.py --lift 5        his mean lifted 5 a week for the weeks left (a big hit in the flex)
    py research\\playoff_odds.py --backtest      2022 to 2025 at the end of week 4: the method against what happened
    py research\\playoff_odds.py --convexity     a ticket against the same expected points spread evenly, by how far behind

BACKTEST (section 1 of doc 464): at the end of week 4 in each of four seasons, the model's P(top six) for every team
against the actual finish, scored by Brier against the naive rule "the current top six make it".
stdlib + numpy + pandas. Paths resolve against this file.
"""
import argparse
import csv
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get('FF_SRC') or os.path.normpath(os.path.join(HERE, '..', '..', 'Source'))
REG_WEEKS = 14
PLAYOFF_TEAMS = 6
K_PRIOR = 4.0
DRAWS = 20000


def pooled_sd(sb):
    """the within-team weekly spread on the league's history, regular season, all seasons pooled"""
    g = sb[sb['Bracket Type'] == 'NONE']
    g = g[~g['Home Team'].astype(str).str.startswith(BYE) & ~g['Away Team'].astype(str).str.startswith(BYE)]
    long = pd.concat([g[['Season', 'Home Team', 'Home Score']].rename(columns={'Home Team': 't', 'Home Score': 's'}),
                      g[['Season', 'Away Team', 'Away Score']].rename(columns={'Away Team': 't', 'Away Score': 's'})])
    resid = long.groupby(['Season', 't']).s.transform(lambda x: x - x.mean())
    n_groups = long.groupby(['Season', 't']).ngroups
    return float(np.sqrt((resid ** 2).sum() / (len(long) - n_groups)))


def simulate(played, remaining, teams, sd, k=K_PRIOR, draws=DRAWS, lift=None, rng=None):
    """played: list of (week, home, away, hp, ap) with scores; remaining: list of (week, home, away).
    teams: list of names. lift: {team: points a week} added to a team's mean for the weeks left.
    Returns {team: P(top six)}."""
    rng = rng or np.random.default_rng(7)
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    wins = np.zeros(n); pf = np.zeros(n); tot = np.zeros(n); cnt = np.zeros(n)
    for w, h, a, hp, ap in played:
        tot[idx[h]] += hp; cnt[idx[h]] += 1; tot[idx[a]] += ap; cnt[idx[a]] += 1
        pf[idx[h]] += hp; pf[idx[a]] += ap
        if hp > ap:
            wins[idx[h]] += 1
        elif ap > hp:
            wins[idx[a]] += 1
        else:
            wins[idx[h]] += 0.5; wins[idx[a]] += 0.5
    league = tot.sum() / max(cnt.sum(), 1)
    mean = (tot + k * league) / (cnt + k)
    if lift:
        for t, v in lift.items():
            mean[idx[t]] += v
    m = len(remaining)
    hi = np.array([idx[h] for _, h, _ in remaining]); ai = np.array([idx[a] for _, _, a in remaining])
    hs = rng.normal(mean[hi], sd, size=(draws, m)); as_ = rng.normal(mean[ai], sd, size=(draws, m))
    W = np.tile(wins, (draws, 1)); P = np.tile(pf, (draws, 1))
    for j in range(m):
        hw = hs[:, j] > as_[:, j]
        W[:, hi[j]] += hw; W[:, ai[j]] += ~hw
        P[:, hi[j]] += hs[:, j]; P[:, ai[j]] += as_[:, j]
    # rank: wins, then points for
    order = np.lexsort((-P, -W), axis=1)
    rank = np.empty_like(order)
    rows = np.arange(draws)[:, None]
    rank[rows, order] = np.arange(n)[None, :]
    made = (rank < PLAYOFF_TEAMS).mean(axis=0)
    return {t: float(made[idx[t]]) for t in teams}


BYE = 'Playoff Bye'      # ESPN's placeholder opponent in the scoreboard export; not a team


def from_scoreboard(sb, season, through_week):
    g = sb[(sb.Season == season) & (sb['Bracket Type'] == 'NONE')]
    g = g[~g['Home Team'].astype(str).str.startswith(BYE) & ~g['Away Team'].astype(str).str.startswith(BYE)]
    teams = sorted(set(g['Home Team']) | set(g['Away Team']))
    played = [(int(r.Week), r['Home Team'], r['Away Team'], float(r['Home Score']), float(r['Away Score']))
              for _, r in g[g.Week <= through_week].iterrows()]
    remaining = [(int(r.Week), r['Home Team'], r['Away Team']) for _, r in g[(g.Week > through_week) & (g.Week <= REG_WEEKS)].iterrows()]
    final = g[g.Week <= REG_WEEKS]
    return teams, played, remaining, final


def actual_top6(final, teams):
    wins = {t: 0.0 for t in teams}; pf = {t: 0.0 for t in teams}
    for _, r in final.iterrows():
        h, a, hp, ap = r['Home Team'], r['Away Team'], float(r['Home Score']), float(r['Away Score'])
        pf[h] += hp; pf[a] += ap
        if hp > ap: wins[h] += 1
        elif ap > hp: wins[a] += 1
        else: wins[h] += 0.5; wins[a] += 0.5
    order = sorted(teams, key=lambda t: (-wins[t], -pf[t]))
    return set(order[:PLAYOFF_TEAMS]), wins, pf


def backtest(sb, through_week=4):
    sd = pooled_sd(sb)
    print(f'pooled within-team weekly spread, 2022 to 2025: {sd:.1f} points')
    briers, naive = [], []
    for season in sorted(sb.Season.unique()):
        teams, played, remaining, final = from_scoreboard(sb, season, through_week)
        if not remaining:
            continue
        p = simulate(played, remaining, teams, sd)
        top6, wins, pf = actual_top6(final, teams)
        now = sorted(teams, key=lambda t: (-sum(1 for w, h, a, hp, ap in played if (h == t and hp > ap) or (a == t and ap > hp)),
                                           -sum(hp if h == t else ap for w, h, a, hp, ap in played if t in (h, a))))[:PLAYOFF_TEAMS]
        b = np.mean([(p[t] - (t in top6)) ** 2 for t in teams])
        nb = np.mean([((t in now) - (t in top6)) ** 2 for t in teams])
        briers.append(b); naive.append(nb)
        hits = sum(1 for t in sorted(teams, key=lambda t: -p[t])[:PLAYOFF_TEAMS] if t in top6)
        print(f'  {season}: Brier {b:.3f} (naive current-top-six {nb:.3f}); the model\'s top six by odds had {hits} of 6 right; '
              + ', '.join(f'{t[:14]} {p[t]:.0%}{"*" if t in top6 else ""}' for t in sorted(teams, key=lambda t: -p[t])))
    print(f'  mean Brier {np.mean(briers):.3f} against naive {np.mean(naive):.3f} (lower is better; 0.25 is a coin flip on each team). '
          f'* marks the teams that made it.')


def convexity(sb, through_week=3, draws=20000):
    """[doc 464] At EQUAL expected points, does a lottery ticket (probability p of +15 a week for six weeks,
    else nothing) raise a team's playoff probability more than the same expected points spread evenly over the
    weeks left, and more so the further behind the team is? The ticket is priced as a probability mixture of
    the spread lift (the simulator has no week-specific lift, so the burst's lumpiness is not modelled; that
    understates the ticket a little). Every team, four seasons, at the end of `through_week`."""
    sd = pooled_sd(sb)
    rows = []
    for season in sorted(sb.Season.unique()):
        teams, played, remaining, final = from_scoreboard(sb, season, through_week)
        if not remaining:
            continue
        n_left = len({w for w, _, _ in remaining})
        base = simulate(played, remaining, teams, sd, draws=draws)
        for t in teams:
            for p in (0.085, 0.19, 0.30):
                ev = p * 15.0 * 6
                steady = simulate(played, remaining, teams, sd, lift={t: ev / n_left}, draws=draws)[t]
                up = simulate(played, remaining, teams, sd, lift={t: 15.0 * 6 / n_left}, draws=draws)[t]
                rows.append(dict(season=season, team=t, base=base[t], p=p, steady=steady, ticket=p * up + (1 - p) * base[t]))
    d = pd.DataFrame(rows)
    d['band'] = pd.cut(d.base, [0, 0.3, 0.6, 1.0], labels=['under 30%', '30 to 60%', 'over 60%'])
    g = d.groupby(['band', 'p'], observed=True).agg(n=('team', 'count'), base=('base', 'mean'), steady=('steady', 'mean'),
                                                     ticket=('ticket', 'mean')).reset_index()
    g['steady_gain'] = (g.steady - g.base) * 100
    g['ticket_gain'] = (g.ticket - g.base) * 100
    print(f'playoff-probability gain in points at the end of week {through_week}, equal expected points, all teams, four seasons:')
    print(g[['band', 'p', 'n', 'base', 'steady_gain', 'ticket_gain']].to_string(index=False, float_format=lambda x: f'{x:.2f}'))
    print('p = the ticket\'s chance of a +15 flex for six weeks (doc 460\'s committee, lead-back and a notional 30% cell).')


def live_numbers(src=None, lift_pts=5.0):
    """[doc 469] The live season as numbers, for the week sheet's standings line: dict(me, base {team: p},
    up (his p with lift_pts a week added), played, remaining, sd), or None when schedule_2026.csv is not
    there. Same inputs and the same seed as live(), so the page and the console print one number."""
    src = src or SRC
    p = os.path.join(src, 'schedule_2026.csv')
    if not os.path.exists(p):
        return None
    sb = pd.read_csv(os.path.join(src, 'historical_scoreboard_2022_2025.csv'))
    sd = pooled_sd(sb)
    sch = pd.read_csv(p)
    st = pd.read_csv(os.path.join(src, 'standings_2026.csv'))
    me = st[st.mine.astype(str).str.strip() == 'yes'].abbrev.iloc[0]
    reg = sch[(sch.playoff.isna() | (sch.playoff.astype(str).str.strip() == '') | (sch.playoff.astype(str) == 'NONE')) & (sch.week <= REG_WEEKS)]
    teams = sorted(set(reg.home) | set(reg.away))
    def scored(r):
        try:
            return (float(r.home_pts) > 0 or float(r.away_pts) > 0)
        except (TypeError, ValueError):
            return False
    played = [(int(r.week), r.home, r.away, float(r.home_pts), float(r.away_pts)) for _, r in reg.iterrows() if scored(r)]
    remaining = [(int(r.week), r.home, r.away) for _, r in reg.iterrows() if not scored(r)]
    base = simulate(played, remaining, teams, sd)
    up = simulate(played, remaining, teams, sd, lift={me: lift_pts})[me] if lift_pts else None
    return dict(me=me, base=base, up=up, lift=lift_pts, played=len(played), remaining=len(remaining), sd=sd, teams=teams)


def live(lift_pts=0.0):
    r = live_numbers(SRC, lift_pts)
    if r is None:
        print('BLOCKED: Source\\schedule_2026.csv is not there yet; wire.py writes it off ESPN on its next run (doc 464).')
        return 2
    base, me = r['base'], r['me']
    print(f"{r['played']} matchups played, {r['remaining']} left; weekly spread {r['sd']:.1f}")
    for t in sorted(r['teams'], key=lambda t: -base[t]):
        print(f'  {t:<8}{base[t]:6.1%}' + ('  <- you' if t == me else ''))
    if lift_pts:
        print(f"\nwith +{lift_pts:.0f} a week for the weeks left: {me} {base[me]:.1%} -> {r['up']:.1%} "
              f"({(r['up'] - base[me]) * 100:+.1f} points of playoff probability)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--backtest', action='store_true')
    ap.add_argument('--week', type=int, default=4)
    ap.add_argument('--lift', type=float, default=0.0)
    ap.add_argument('--convexity', action='store_true')
    a = ap.parse_args()
    if a.convexity:
        sb = pd.read_csv(os.path.join(SRC, 'historical_scoreboard_2022_2025.csv'))
        convexity(sb, a.week if a.week != 4 else 3)
        return 0
    if a.backtest:
        sb = pd.read_csv(os.path.join(SRC, 'historical_scoreboard_2022_2025.csv'))
        backtest(sb, a.week)
        return 0
    return live(a.lift)


if __name__ == '__main__':
    sys.exit(main())
