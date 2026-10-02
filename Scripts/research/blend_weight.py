"""blend_weight.py -- measures BLEND_W, the table sheet_engine.rates() uses. Writes nothing.

THE QUESTION. Standing in week W of a season, you want a man's points per game for the REST of it.
You hold two numbers: what he has averaged so far this season, and a preseason forecast. How much
weight goes on THIS season? sheet_engine.rates() used 0% for its whole life -- every "he is worth"
number on THE CALL was computed from a preseason rate, so Dalton Schultz showed +13.1 off 6.06 a
week while actually measuring 12.8.

The blend was deferred twice because I would not invent the weight (directive 0.2: a severity
estimate is a claim and must be measured, not reasoned). This file is the measurement.

THE DESIGN.
    population  nflverse weekly, 2021-2025, season_type REG, positions RB/WR/TE
    scoring     half-PPR, (fantasy_points + fantasy_points_ppr) / 2 -- this league is 0.5 PPR
    unit        one player-season with a prior season, kept if he has >= 1 game each side of W
    outcome     ppg over weeks W..14 (the fantasy regular season, section 2)
    features    ppg over weeks 1..W-1  ("now"), and ppg over the PRIOR season ("prior")
    fit         ordinary least squares, outcome ~ now + prior, no intercept beyond the mean;
                the reported weight is the normalised coefficient on `now`
    n           846 to 1,254 player-seasons per week

STABILITY. Re-fitted under 18 population definitions (minimum games each side 1, 2 or 3, outcome
window ending week 14 or 17): every week's weight moves by at most 0.07 and the shape, the ordering
and the crossover are identical in all 18. The first version of this table was fitted INLINE, from
a population nobody wrote down, and none of those 18 reproduced it -- that is doc 399's failure and
it is why this file exists instead of a comment claiming a number.

THE CAVEAT, and it bounds the number rather than decorating it. The PRIOR here is last season's
ppg, not ESPN's in-season projection. ESPN's projection is the better prior -- it knows about
injuries, depth-chart moves and rookies, which last season's ppg does not. A better prior earns
more weight, so THE MEASURED WEIGHT ON THIS SEASON IS AN UPPER BOUND. It is not shaded down in
production, because shading it would be exactly the guess this measurement exists to avoid.

RB/WR/TE ONLY. form_2026.csv does not score passing or kicking (doc 375), so QB, K and D/ST get
no measured rate to blend and stay on the projection. rates() labels them `proj` in `vintage`.

    py blend_weight.py           print the table
    py blend_weight.py --check   print it AND diff it against sheet_engine.BLEND_W; exit 1 on drift

Standard library plus pandas/numpy (doc 144).
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))          # doc 144: resolve against the script
CACHE = os.path.join(HERE, '_nflverse_cache')
SEASONS = (2021, 2022, 2023, 2024, 2025)
POS = ('RB', 'WR', 'TE')
LAST_WEEK = 14                                             # this league's regular season (section 2)
MIN_GAMES = 1


def load():
    frames = []
    for yr in SEASONS:
        p = os.path.join(CACHE, f'stats_player_week_{yr}.csv')
        if not os.path.exists(p):
            print(f'  missing {p} -- run the nflverse cache builder first')
            raise SystemExit(2)
        d = pd.read_csv(p, low_memory=False)
        d = d[(d.get('season_type') == 'REG') & (d['position'].isin(POS))].copy()
        # half-PPR: nflverse ships standard and full-PPR, and the average of the two IS 0.5 PPR
        d['hppr'] = (d['fantasy_points'] + d['fantasy_points_ppr']) / 2.0
        frames.append(d[['player_id', 'season', 'week', 'position', 'hppr']])
    return pd.concat(frames, ignore_index=True)


def prior_ppg(df):
    """ppg over the whole of each player's PRIOR season, keyed (player_id, season)."""
    tot = df.groupby(['player_id', 'season'])['hppr'].agg(['sum', 'count'])
    tot['ppg'] = tot['sum'] / tot['count']
    out = {}
    for (pid, yr), row in tot.iterrows():
        out[(pid, yr + 1)] = row['ppg']
    return out


def weight_at(df, prior, week):
    rows = []
    for (pid, yr), g in df.groupby(['player_id', 'season']):
        before = g[g['week'] < week]['hppr']
        after = g[(g['week'] >= week) & (g['week'] <= LAST_WEEK)]['hppr']
        if len(before) < MIN_GAMES or len(after) < MIN_GAMES:
            continue
        pr = prior.get((pid, yr))
        if pr is None:
            continue
        rows.append((before.mean(), pr, after.mean()))
    if len(rows) < 50:
        return None
    a = np.array(rows, dtype=float)
    now, pri, out = a[:, 0], a[:, 1], a[:, 2]
    X = np.column_stack([now, pri, np.ones(len(a))])
    beta, *_ = np.linalg.lstsq(X, out, rcond=None)
    b_now, b_pri = float(beta[0]), float(beta[1])
    share = b_now / (b_now + b_pri) if (b_now + b_pri) else float('nan')
    share = min(max(share, 0.0), 1.0)
    rmse = lambda p: float(np.sqrt(np.mean((out - p) ** 2)))
    e_now, e_pri = rmse(now), rmse(pri)
    e_bl = rmse(share * now + (1 - share) * pri)
    best_single = min(e_now, e_pri)
    return {'n': len(a), 'w': share, 'rmse_now': e_now, 'rmse_prior': e_pri,
            'rmse_blend': e_bl, 'gain': (best_single - e_bl) / best_single}


def main():
    df = load()
    prior = prior_ppg(df)
    print(f'population: nflverse 2021-2025 REG, {"/".join(POS)}, half-PPR; '
          f'>= {MIN_GAMES} games each side; outcome is ppg over weeks W..{LAST_WEEK}')
    print(f'{"wk":>4} {"n":>6} {"now":>6} {"prior":>6} {"blend":>6} {"gain":>6}   weight on THIS season')
    table = {}
    for w in range(2, LAST_WEEK + 1):
        r = weight_at(df, prior, w)
        if not r:
            continue
        table[w] = round(r['w'], 2)
        print(f'{w:>4} {r["n"]:>6} {r["rmse_now"]:>6.2f} {r["rmse_prior"]:>6.2f} '
              f'{r["rmse_blend"]:>6.2f} {r["gain"]*100:>5.0f}% {r["w"]*100:>18.0f}%')

    print('\nBLEND_W = ' + repr(table))

    if '--check' in sys.argv:
        sys.path.insert(0, os.path.join(HERE, '..'))
        import sheet_engine
        live = sheet_engine.BLEND_W
        drift = {w: (live.get(w), table.get(w)) for w in sorted(set(live) | set(table))
                 if live.get(w) != table.get(w)}
        if drift:
            print('\nDRIFT between this measurement and sheet_engine.BLEND_W:')
            for w, (a, b) in drift.items():
                print(f'   week {w}: production {a}, measured {b}')
            return 1
        print('\nsheet_engine.BLEND_W matches this measurement exactly.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
