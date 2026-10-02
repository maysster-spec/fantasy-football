"""
Data-integrity harness. Runs BEFORE any analysis. Every check raises, not warns.
Exists because three separate silent-join failures reached conclusions:
  1. Travis Hunter dropped (trailing "CB")
  2. 405 rows from 357 ("J. Williams" collision)
  3. 37 players dropped (ESPN injury flags "Q"/"O" glued to surname)
"""
import numpy as np, pandas as pd, sys, re

FAILURES = []
def check(name, ok, detail=""):
    (print(f"  PASS  {name}") if ok else FAILURES.append(f"{name}: {detail}"))
    if not ok: print(f"  FAIL  {name}  --  {detail}")

def assert_join(left, right, merged, label):
    """A merge must not create or destroy rows."""
    check(f"[{label}] row count preserved", len(merged) == len(left),
          f"in {len(left)} -> out {len(merged)}")

def assert_no_silent_drop(source_df, result_keys, keycol, label, allow=0):
    lost = source_df[~source_df[keycol].isin(set(result_keys))]
    check(f"[{label}] no silent drops", len(lost) <= allow,
          f"{len(lost)} lost, e.g. {list(lost[keycol].head(6))}")
    return lost

# F1 replacement levels. These are SPINE-SPECIFIC and must be updated whenever the
# projection source changes -- that is the point of the assertion, not a nuisance.
#   v2 (200-row undated ESPN export + linear ramp): RB30 168.0 WR30 168.5 QB12 341.7 TE12 137.7
#   v4 (espn_projections_2026_20260820.csv, 700 rows, dated, self-verifying):
REPLACEMENT_V4 = {'RB': (30, 168.589), 'WR': (30, 163.540), 'QB': (12, 341.603), 'TE': (12, 140.295)}
REPLACEMENT_V2 = {'RB': (30, 168.0), 'WR': (30, 168.5), 'QB': (12, 341.7), 'TE': (12, 137.7)}


def assert_replacement(u, truth=REPLACEMENT_V4, tol=0.5):
    """Universe must reproduce F1's verified replacement levels."""
    for p,(n,v) in truth.items():
        # doc 59: np.sort puts NaN LAST, so [::-1] puts it FIRST and s[n-1] read a NaN.
        # The guard itself violated V2 ("replacement pools exclude nulls, zeros, synthetic").
        col = u.loc[(u['pos']==p) & u['proj_leaguepts'].notna() & (u['proj_leaguepts']>0)]
        if 'synthetic' in u.columns: col = col[~col['synthetic'].astype(bool)]
        s = np.sort(col['proj_leaguepts'].values)[::-1]
        got = s[n-1] if len(s) >= n else np.nan
        check(f"replacement {p}#{n}", abs(got-v) <= tol, f"got {got:.1f} expected {v:.1f}")

# H2 (doc 59): the old gate was D/ST>=20 and K>=20. C3's surviving count was 29, so the
# threshold passed the exact defect it was written for. Both pools are exactly 32 NFL teams.
def assert_coverage(u, mincount={'QB':60,'RB':70,'WR':120,'TE':60,'K':32,'D/ST':32}):
    for p,m in mincount.items():
        c = (u['pos']==p).sum()
        check(f"coverage {p}", c >= m, f"only {c} (expect >= {m})")

def assert_unique(df, col, label):
    d = df[col].duplicated().sum()
    check(f"[{label}] unique {col}", d == 0, f"{d} duplicates")

def assert_no_nulls(df, cols, label):
    for c in cols:
        n = df[c].isna().sum()
        check(f"[{label}] {c} non-null", n == 0, f"{n} nulls")

def report():
    if FAILURES:
        print("\n" + "="*60); print("INTEGRITY FAILURES — ANALYSIS MUST NOT PROCEED:")
        for f in FAILURES: print("  * " + f)
        print("="*60); sys.exit(1)
    print("\n  ALL INTEGRITY CHECKS PASSED\n")
    return True   # doc 59: returned None, so the caller's exit code contradicted the message

# ---------------------------------------------------------------- name keys --
def norm_name(s):
    """Canonical name key. Two files may spell the same player differently
    ('Travis Etienne' vs 'Travis Etienne Jr.'). Six join failures in this project
    trace to comparing raw name strings across sources."""
    s = str(s).lower()
    s = re.sub(r"\b(jr|sr|ii|iii|iv|v)\b\.?", "", s)
    return re.sub(r"[^a-z]", "", s)

def assert_names_match(left_names, right_names, label, allow=0):
    """Set-compare two name columns on the NORMALISED key, not the raw string."""
    L = {norm_name(x) for x in left_names}
    R = {norm_name(x) for x in right_names}
    miss = sorted(L - R)
    check(f"[{label}] every name resolves", len(miss) <= allow, f"unmatched: {miss[:8]}")
    return miss

def assert_xwalk_unique(x, idcol='gsis_id', label='xwalk'):
    """The canonical crosswalk carries alias rows (one id, two spellings). That is
    expected; two DIFFERENT players sharing an id is not."""
    d = x.dropna(subset=[idcol])
    bad = [i for i, g in d.groupby(idcol) if g['pos2'].nunique() > 1]
    alias = int(d[idcol].duplicated().sum())
    check(f"[{label}] no cross-position {idcol} collisions", not bad, f"{bad[:5]}")
    print(f"  NOTE  [{label}] {alias} alias row(s) share a {idcol} (same player, two spellings)")
    return bad

def assert_keepers_removed(u, keepers, namecol='player'):
    """H1 (doc 59): this was INVERTED -- it passed the broken universe and failed the correctly
    depleted pool. A keeper that LEAKS into the pool is the defect; a keeper that is absent is
    the correct state."""
    pool = {norm_name(v) for v in u[namecol].dropna()}
    leaked = sorted(k for k in keepers if norm_name(k) in pool)
    if leaked:
        FAILURES.append(f"[keepers] {len(leaked)} keeper(s) STILL IN THE POOL: {leaked}")
    else:
        print(f"PASS  [keepers] all {len(keepers)} removed from the pool")
    return not leaked


# ---------------------------------------------------------------------------
# doc 59 (H-chunk): this module had ZERO importers and report() had ZERO callers.
# Its docstring claimed "runs BEFORE any analysis; every check raises, not warns".
# Neither clause was true. It is now runnable:  py code_integrity.py
# ---------------------------------------------------------------------------
def run_all(spine_csv='code_universe_v5.csv', board_csv='board_v8_fixed.csv',
            keepers_csv='predicted_keepers_v5.csv', prerank_csv='ESPN_prerank_with_ids.csv'):
    import pandas as _pd, os as _os
    FAILURES.clear()
    u = _pd.read_csv(spine_csv)
    assert_replacement(u)
    assert_coverage(u)
    if _os.path.exists(board_csv) and _os.path.exists(keepers_csv):
        b  = _pd.read_csv(board_csv)
        kp = _pd.read_csv(keepers_csv)
        # the BOARD must be keeper-free -- the spine legitimately contains them
        assert_keepers_removed(b, list(kp['Player']), namecol='player')
        check("board no null vbd", b['vbd'].notna().all(), f"{b['vbd'].isna().sum()} nulls")
        check("board no K/DST",  not b['pos'].isin(['K','D/ST']).any(), "streamers on the skill board")
        if 'espn_id' in b.columns:
            assert_unique(b, 'espn_id', 'board')
            assert_no_nulls(b, ['espn_id'], 'board')
    if _os.path.exists(prerank_csv):
        p = _pd.read_csv(prerank_csv)
        assert_unique(p, 'ESPN_ID', 'prerank')
        assert_no_nulls(p, ['ESPN_ID'], 'prerank')
        check("prerank order == prerank col", list(p['prerank']) == list(range(1, len(p)+1)),
              "row order is not the ranking")
        for _p in ('K','D/ST'):
            check(f"prerank has all 32 {_p}", (p['pos']==_p).sum()==32,
                  f"only {(p['pos']==_p).sum()}")
    return report()


if __name__ == '__main__':
    import sys as _sys
    _sys.exit(0 if run_all() else 1)
