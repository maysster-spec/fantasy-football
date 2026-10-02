r"""Shared pieces for doc 293's batch R1 scripts: the weekly table, bars, established set, window starts, features."""
import os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))   # outputs and common.py live beside this file
import pandas as pd

BAR = {'RB': 9.92, 'WR': 9.62, 'TE': 8.25}
LINE = {'RB': 0.50, 'WR': 0.65, 'TE': 0.60}

def load():
    w = pd.read_pickle(os.path.join(HERE, 'weekly.pkl'))
    w['key'] = np.where(w.gsis_id.notna(), w.gsis_id, 'pfr:' + w.pfr_player_id)
    w['bar'] = w.position.map(BAR)
    w['line'] = w.position.map(LINE)
    w['plays'] = np.where(w.position == 'RB', w.carries, w.targets)
    w['epa'] = np.where(w.position == 'RB', w.rushing_epa, w.receiving_epa)
    w['yds'] = np.where(w.position == 'RB', w.rushing_yards, w.receiving_yards)
    return w

def established(w):
    ps = w.groupby(['key', 'season']).agg(g=('week', 'nunique'), ppg=('half', 'mean'), bar=('bar', 'last')).reset_index()
    ok = (ps.g >= 6) & (ps.ppg >= ps.bar)
    return set(zip(ps.key[ok], ps.season[ok] + 1))

def window_starts(w):
    """(key, season) -> set of weeks where four straight games played start and average at or above the bar."""
    out = {}
    for (key, season), g in w.sort_values('week').groupby(['key', 'season']):
        h, wk, bar = g.half.values, g.week.values, g.bar.values
        s = set()
        for i in range(len(g) - 3):
            if h[i:i + 4].mean() >= bar[i]:
                s.add(int(wk[i]))
        out[(key, season)] = (s, list(wk))
    return out

def logistic(X, y):
    """IRLS; returns beta, se. X includes a constant column."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    b = np.zeros(X.shape[1])
    for _ in range(100):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        W = p * (1 - p) + 1e-9
        H = X.T @ (X * W[:, None]) + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.abs(step).max() < 1e-8:
            break
    se = np.sqrt(np.diag(np.linalg.inv(H)))
    return b, se
