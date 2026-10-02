r"""j4_band_loo.py -- doc 385. The band split and the leave-one-season-out check on a J4_rows file.
Reproduces doc 384's band row exactly on J4_rows_main_halfppr3.csv (+51.0 [18.5, 73.4], n=100), which is the
control. Usage: py j4_band_loo.py J4_rows_main_halfppr5.csv   (pandas + numpy only)."""
import numpy as np, pandas as pd, sys
def ols(X, y):
    X = np.asarray(X, float); y = np.asarray(y, float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ b; n, p = X.shape
    s2 = (r @ r) / max(n - p, 1); cov = s2 * np.linalg.pinv(X.T @ X); return b, np.sqrt(np.diag(cov)), r
def gap_one(d):
    q1, q2 = d.riser.quantile([1/3, 2/3]); hi = (d.riser >= q2).astype(float); lo = (d.riser <= q1).astype(float)
    X = np.column_stack([np.ones(len(d)), hi, lo, np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE]); b,_,_ = ols(X, d.vbd14_N1); return b[1]-b[2]
def band(df, lo, hi, seed=20260921, B=2000):
    d = df[(df.adp >= lo) & (df.adp < hi)].reset_index(drop=True)
    X = np.column_stack([np.ones(len(d)), np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE, d.riser*10])
    b, se, _ = ols(X, d.vbd14_N1)
    q1, q2 = d.riser.quantile([1/3, 2/3])
    rng = np.random.default_rng(seed); bs=[]
    for _ in range(B):
        s = d.iloc[rng.choice(len(d), len(d), replace=True)]
        try: bs.append(gap_one(s))
        except Exception: pass
    return dict(n=len(d), riser10=b[5], riser10_se=se[5], logadp=b[1], logadp_se=se[1], gap=gap_one(d),
                ci=(np.percentile(bs,2.5), np.percentile(bs,97.5)),
                st_top=d[d.riser>=q2].startable_N1.mean(), st_bot=d[d.riser<=q1].startable_N1.mean(),
                vbd_top=d[d.riser>=q2].vbd14_N1.mean(), vbd_bot=d[d.riser<=q1].vbd14_N1.mean())
def youth(df, lo, hi):
    d = df[(df.adp >= lo) & (df.adp < hi)].dropna(subset=['exp_N'])
    X = np.column_stack([np.ones(len(d)), np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE, d.riser*10, d.young, d.riser*10*d.young])
    b, se, _ = ols(X, d.vbd14_N1); return b[7], se[7], len(d)
def report(path, label):
    df = pd.read_csv(path)
    if 'adp' not in df: df = df.rename(columns={'adp_N':'adp'})
    for p in ('RB','WR','TE'):
        if f'pos_{p}' not in df: df[f'pos_{p}'] = (df.pos==p).astype(float)
    a = band(df, 50, 97); z = band(df, 97, 1e9)
    yb = youth(df, 50, 97); yp = youth(df, 0, 1e9)
    print(f"{label}: n={len(df)} by season {df.season_N.value_counts().sort_index().to_dict()}")
    print(f"  BAND 50-96 n={a['n']} gap {a['gap']:+.1f} [{a['ci'][0]:.1f}, {a['ci'][1]:.1f}]  riser/10 {a['riser10']:+.1f} (se {a['riser10_se']:.1f})  logADP {a['logadp']:+.1f} (se {a['logadp_se']:.0f})  startable {100*a['st_top']:.0f}% vs {100*a['st_bot']:.0f}%  VBD14 top {a['vbd_top']:+.1f} bottom {a['vbd_bot']:+.1f}")
    print(f"  9+   97+   n={z['n']} gap {z['gap']:+.1f} [{z['ci'][0]:.1f}, {z['ci'][1]:.1f}]  riser/10 {z['riser10']:+.1f} (se {z['riser10_se']:.1f})")
    print(f"  youth x riser: pooled {yp[0]:+.1f} (se {yp[1]:.1f}) n={yp[2]}; band {yb[0]:+.1f} (se {yb[1]:.1f}) n={yb[2]}")
    return a, z, yp, yb
def loo(path):
    df = pd.read_csv(path).rename(columns={'adp_N': 'adp'})
    for p in ('RB', 'WR', 'TE'):
        df[f'pos_{p}'] = (df.pos == p).astype(float)
    for s_ in sorted(df.season_N.unique()):
        a = band(df[df.season_N != s_], 50, 97)
        d = df[(df.season_N == s_) & (df.adp >= 50) & (df.adp < 97)]
        X = np.column_stack([np.ones(len(d)), np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE, d.riser * 10])
        b, se, _ = ols(X, d.vbd14_N1)
        print(f"  without {s_}: n={a['n']} gap {a['gap']:+.1f} [{a['ci'][0]:.1f}, {a['ci'][1]:.1f}] per ten {a['riser10']:+.1f} (se {a['riser10_se']:.1f})"
              f"   |   {s_} alone: n={len(d)} per ten {b[5]:+.1f} (se {se[5]:.1f})")
    d = df[(df.adp >= 50) & (df.adp < 97)]
    S = pd.get_dummies(d.season_N, drop_first=True).astype(float).values
    X = np.column_stack([np.ones(len(d)), np.log(d.adp), d.pos_RB, d.pos_WR, d.pos_TE, S, d.riser * 10])
    b, se, _ = ols(X, d.vbd14_N1)
    print(f"  band slope with season fixed effects: {b[-1]:+.1f} (se {se[-1]:.1f})")


if __name__ == '__main__':
    for p in sys.argv[1:]:
        report(p, p)
        loo(p)
