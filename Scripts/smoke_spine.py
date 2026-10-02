#!/usr/bin/env python3
"""
smoke_spine.py - run the PATCHED code_rebuild_spine_v5.py in a throwaway scratch
folder and DIFF its output against the shipped code_universe_v5.csv.

It never writes to Source\. It refuses to run if scratch resolves anywhere inside
Source\, because the whole point is that the smoke test cannot cause the desync
the spine's own gate exists to prevent.

  py smoke_spine.py

Inputs it needs, copied into scratch\src\ :
  code_universe.csv                       <- NOT in Source\ (Drive: "files(02)", 126,086 B)
  espn_projections_2026_20260820.csv      <- in Source\
"""
import os, shutil, subprocess, sys, hashlib, tempfile

SCRIPTS = r'G:\My Drive\_Fantasy\2026\Scripts'
SOURCE  = r'G:\My Drive\_Fantasy\2026\Source'
SPINE   = os.path.join(SCRIPTS, 'code_rebuild_spine_v5.py')
SHIPPED = os.path.join(SOURCE, 'code_universe_v5.csv')
NEEDED  = ['code_universe.csv', 'espn_projections_2026_20260820.csv']

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(65536), b''): h.update(b)
    return h.hexdigest()[:16]

scratch = os.path.join(tempfile.gettempdir(), 'spine_smoke')
if os.path.normcase(os.path.abspath(scratch)).startswith(os.path.normcase(os.path.abspath(SOURCE))):
    sys.exit('REFUSING: scratch resolves inside Source\\ -- that is the desync this test exists to avoid.')

shutil.rmtree(scratch, ignore_errors=True)
os.makedirs(os.path.join(scratch, 'src')); os.makedirs(os.path.join(scratch, 'out'))
shutil.copy(SPINE, scratch)

missing = []
for n in NEEDED:
    for cand in (os.path.join(SOURCE, n), os.path.join(os.getcwd(), n)):
        if os.path.exists(cand):
            shutil.copy(cand, os.path.join(scratch, 'src', n)); break
    else:
        missing.append(n)
if missing:
    sys.exit(f"MISSING INPUT: {', '.join(missing)}\n"
             f"  Put a copy beside this script or in Source\\, then re-run.\n"
             f"  code_universe.csv is NOT in Source\\ -- Drive folder \"files(02)\", 126,086 bytes.")

print(f'scratch: {scratch}')
r = subprocess.run([sys.executable, 'code_rebuild_spine_v5.py'], cwd=scratch,
                   capture_output=True, text=True)
print(r.stdout[-2000:]);  print(r.stderr[-1000:], file=sys.stderr)
if r.returncode != 0:
    sys.exit(f'spine exited {r.returncode} -- see output above. Nothing was written to Source\\.')

new = os.path.join(scratch, 'out', 'code_universe_v5.csv')
print(f'\nshipped {SHIPPED}\n        {os.path.getsize(SHIPPED):,} B  {sha(SHIPPED)}')
print(f'rebuilt {new}\n        {os.path.getsize(new):,} B  {sha(new)}')

try:
    import pandas as pd
    a, b = pd.read_csv(SHIPPED), pd.read_csv(new)
    print(f'\nrows {len(a)} -> {len(b)}')
    common = [c for c in a.columns if c in b.columns]
    print(f'columns only in shipped: {sorted(set(a.columns)-set(b.columns))}')
    print(f'columns only in rebuilt: {sorted(set(b.columns)-set(a.columns))}')
    m = a[common].merge(b[common], on='espn_id', suffixes=('_old','_new'))
    for c in ('proj_leaguepts','vbd','adp_pick'):
        if f'{c}_old' in m:
            d = (m[f'{c}_old'].fillna(-9e9) - m[f'{c}_new'].fillna(-9e9)).abs()
            print(f'  {c:16s} rows differing: {int((d>1e-9).sum())} of {len(m)}')
    print('\nEXPECTED: vbd differs ONLY on K and D/ST rows (now null by design, doc 61 D2).')
except ImportError:
    print('(pandas not available -- byte/hash comparison above is the result)')
print('\nSource\\ was not written to.')
