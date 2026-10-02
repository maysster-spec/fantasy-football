r"""
adp_registry_from_fp.py -- put one season of the ADP registry on the FantasyPros half-PPR archive.
Docs 384 and 385. Standard library plus pandas only; every path is resolved against this file, not the shell.

WHAT IT DOES, for --year Y and --file <a FantasyPros ADP export>:
  1. refuses if the file is not a FantasyPros export (needs Rank, Player (Bye), POS, AVG columns);
  2. refuses if the AVG column is a RANK wearing an ADP's name (values exactly 1..n with no gaps,
     the doc 383 defect) unless --allow-rank is passed;
  2b. refuses the FULL-PPR page (doc 385). The registry is one instrument, the half-PPR archive page,
     and the two pages are told apart by CONTENT, not by the file name: every half-PPR page held
     (2021 to 2025) averages Yahoo, Sleeper and RTSports, and every full-PPR page averages ESPN, CBS
     and Fantrax, which the half-PPR page never carries. A file name containing "ppr" without "half"
     is refused too. --allow-ppr overrides both, and the MANIFEST row then says full-PPR;
  2c. CHECKS THAT AVG IS THE MEAN OF THE SITE COLUMNS, AND SAYS WHICH ONES (doc 435). On every row
     that has an AVG and at least one site value, AVG must sit within 0.05 of the mean of the site
     columns present on that row. Every subset of the non-empty site columns is tested; the subset
     that reproduces AVG on every such row is what the MANIFEST row says AVG is "of", so that text is
     a CHECKED statement and never an echo of the header. A site column that is on the page and NOT
     in the average is named as excluded (2025: Real-Time is on 17 rows and in the average on none of
     them). A year where no subset reproduces AVG FAILS THE BUILD and prints the failing count, unless
     --avg-not-derivable is passed with a reason; the MANIFEST row then says "AVG not derivable from
     the site columns shown" with the counts and the reason. 2021 is that year: 200 of its 495 rows
     carry an AVG and no site value at all, and on the 295 that do, no subset of Yahoo and Sleeper
     comes within 0.05 on more than a sixth of them. Its AVG is FantasyPros' own composite;
  3. archives the current Source\adp_registry\preseason_adp_Y.csv to _archive\ with a stamp;
  4. writes preseason_adp_Y.csv (player,adp,k) with the same name key JOB 4 uses, and copies the raw
     export beside it as FantasyPros_Y_Overall_ADP_Rankings.csv;
  5. rewrites the Y row of MANIFEST.csv;
  6. prints the comparison against the old file: Spearman, and how many men cross ADP 50 and ADP 97,
     which is where the rules cut.
It does NOT edit code_adp_guard.py: its PRESEASON_SOURCES map is a hand edit, and the script prints the
line to paste. Nothing here touches ESPN.

USAGE (from G:\My Drive\_Fantasy\2026\Scripts; a bare file name is looked for in the 2026 folder):
  py research\adp_registry_from_fp.py --year 2025 --file "FantasyPros_2025_Overall_ADP_Rankings_half_point.csv"
  py research\adp_registry_from_fp.py --year 2021 --file "FantasyPros_2021_Overall_ADP_Rankings_half_point.csv" ^
        --avg-not-derivable "FantasyPros' own composite; the export's Yahoo and Sleeper columns do not average to it"
  add --dry-run to see everything and write nothing;
  add --out <folder> to write the registry file, the raw copy and MANIFEST.csv into that folder instead of
      Source\adp_registry (a rebuild you can diff against the live files; the live files are never touched);
  add --exported "22 Sep 2026" when rebuilding from a page exported on a day other than today;
  add --note "..." to carry a provenance note (what the file replaced) onto the MANIFEST row.
  --check-avg alone (no --year) runs check 2c on every FantasyPros_*_Overall_ADP_Rankings.csv in the
      registry folder, writes nothing, and exits 1 if any year fails it without a MANIFEST row that says so.
"""
import argparse
import csv
import os
import re
import shutil
import sys
from datetime import datetime

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))                     # ...\2026
REG = os.path.join(ROOT, 'Source', 'adp_registry')
ARCH = os.path.join(ROOT, '_archive')
MANIFEST = os.path.join(REG, 'MANIFEST.csv')


def norm_name(s):
    """The key JOB 4 (j4_riser_keeper.py) recomputes from `player`; kept identical here."""
    s = str(s).lower().replace('.', '').replace("'", '').replace('-', ' ')
    s = re.sub(r'[^a-z0-9 ]', '', s)
    toks = [t for t in s.split() if t not in ('jr', 'sr', 'ii', 'iii', 'iv', 'v')]
    return ' '.join(toks)


def read_fp(path):
    df = pd.read_csv(path)
    cols = {c.strip(): c for c in df.columns}
    need = ['Rank', 'Player (Bye)', 'POS', 'AVG']
    missing = [c for c in need if c not in cols]
    if missing:
        sys.exit(f'REFUSED: not a FantasyPros ADP export, missing columns {missing}. Columns: {list(df.columns)}')
    df = df.rename(columns={cols[c]: c for c in cols})
    sites = [c for c in df.columns if c not in need]
    # "Christian McCaffrey   SF (9)" -> name; a bare name stays a bare name
    df['player'] = df['Player (Bye)'].astype(str).str.replace(r'\s+[A-Z]{2,3}\s+\(\d+\)\s*$', '', regex=True).str.strip()
    df['adp'] = pd.to_numeric(df['AVG'], errors='coerce')
    df = df.dropna(subset=['adp'])
    return df, sites


PPR_ONLY_SITES = ('ESPN', 'CBS', 'Fantrax', 'NFL')     # on every full-PPR page held, never on a half-PPR one


def scoring_of(path, sites):
    """'half' or 'ppr', from the site columns first and the file name second (doc 385)."""
    if any(x in sites for x in PPR_ONLY_SITES) and 'Yahoo' not in sites:
        return 'ppr'
    name = os.path.basename(path).lower()
    if 'ppr' in name and 'half' not in name:
        return 'ppr'
    return 'half'


def is_rank(series):
    v = sorted(series.astype(float).tolist())
    return v == [float(i) for i in range(1, len(v) + 1)]


AVG_TOL = 0.05      # FantasyPros prints AVG to one decimal, so a true mean sits within 0.05 of it


def check_avg(df, sites, tol=AVG_TOL):
    """Doc 435's guard. Which site columns is AVG the mean of, tested rather than read off the header.

    For every non-empty subset of the site columns that carry at least one value, take the per-row
    mean over the subset's columns PRESENT on that row, and count rows with an AVG and at least one
    such value where |mean - AVG| > tol. Returns a dict:
      ok        True when some subset reproduces AVG on every tested row
      basis     that subset (the largest one, then the one tested on the most rows) or None
      tested    rows the verdict rests on (AVG present and at least one basis-column value)
      fails     rows off by more than tol against the basis; against ALL live sites when none passes
      excluded  live site columns that are on the page and NOT in the basis
      empty     site columns with no value on any row
      no_site   rows with an AVG and no live site value at all (they cannot be tested)
      subsets   {subset: (tested, fails)} for every subset tried, for the printout
    """
    import itertools
    avg = pd.to_numeric(df['AVG'], errors='coerce')
    num = {c: pd.to_numeric(df[c], errors='coerce') for c in sites}
    live = [c for c in sites if num[c].notna().any()]
    empty = [c for c in sites if c not in live]
    any_live = pd.concat([num[c] for c in live], axis=1).notna().any(axis=1) if live else avg.notna() & False
    no_site = int((avg.notna() & ~any_live).sum())
    subsets = {}
    for r in range(1, len(live) + 1):
        for sub in itertools.combinations(live, r):
            m = pd.concat([num[c] for c in sub], axis=1)
            present = m.notna().any(axis=1) & avg.notna()
            diff = (m.mean(axis=1) - avg).abs()
            subsets[sub] = (int(present.sum()), int((diff[present] > tol).sum()))
    passing = [sub for sub, (t, f) in subsets.items() if f == 0 and t > 0]
    out = {'ok': bool(passing), 'basis': None, 'tested': 0, 'fails': 0, 'excluded': [],
           'empty': empty, 'no_site': no_site, 'subsets': subsets, 'live': live}
    if passing:
        basis = max(passing, key=lambda sub: (len(sub), subsets[sub][0]))
        out.update(basis=basis, tested=subsets[basis][0], fails=0,
                   excluded=[c for c in live if c not in basis])
    elif live:
        out.update(tested=subsets[tuple(live)][0], fails=subsets[tuple(live)][1])
    return out


def avg_text(chk, reason=None):
    """The MANIFEST's "AVG of ..." clause, written from check_avg's result and nothing else."""
    if chk['ok']:
        t = (f"AVG of {', '.join(chk['basis'])} (checked: within {AVG_TOL} of their mean on all "
             f"{chk['tested']} rows that carry one of them")
        if chk['excluded']:
            t += (f"; {', '.join(chk['excluded'])} on the page and NOT in the average")
        if chk['empty']:
            t += f"; {', '.join(chk['empty'])} empty that year"
        if chk['no_site']:
            t += f"; {chk['no_site']} rows carry an AVG and no site value"
        return t + ')'
    t = (f"AVG not derivable from the site columns shown ({', '.join(chk['live']) or 'none carry a value'}: "
         f"{chk['fails']} of {chk['tested']} rows with a site value are off by more than {AVG_TOL}"
         f"{'; ' + str(chk['no_site']) + ' rows carry an AVG and no site value at all' if chk['no_site'] else ''}")
    if chk['empty']:
        t += f"; {', '.join(chk['empty'])} empty that year"
    return t + (f'; accepted with --avg-not-derivable: {reason}' if reason else '') + ')'


def print_avg(chk):
    for sub, (t, f) in sorted(chk['subsets'].items(), key=lambda kv: (len(kv[0]), kv[0])):
        mark = 'PASS' if (f == 0 and t > 0) else 'fail'
        print(f"    {mark}  AVG = mean({', '.join(sub)}): {t} rows tested, {f} off by more than {AVG_TOL}")
    if chk['empty']:
        print(f"    (no value on any row: {', '.join(chk['empty'])})")
    if chk['no_site']:
        print(f"    ({chk['no_site']} rows carry an AVG and no site value at all; they cannot be tested)")


def compare(old_path, new):
    if not os.path.exists(old_path):
        return 'no previous file to compare against'
    old = pd.read_csv(old_path)
    old['k'] = old.player.map(norm_name)
    old = old.drop_duplicates('k')
    m = old.merge(new[['k', 'adp']], on='k', suffixes=('_old', '_new'))
    if len(m) < 10:
        return f'only {len(m)} shared names; no comparison'
    rho = m[['adp_old', 'adp_new']].corr(method='spearman').iloc[0, 1]
    d = m.adp_new - m.adp_old
    x50 = int(((m.adp_old < 50) != (m.adp_new < 50)).sum())
    x97 = int(((m.adp_old < 97) != (m.adp_new < 97)).sum())
    return (f'old n={len(old)} new n={len(new)} shared={len(m)} spearman={rho:.3f} '
            f'median diff={d.median():+.1f} cross ADP50={x50} cross ADP97={x97}')


def check_all(reg, manifest):
    """--check-avg: run check 2c on every raw page in the registry folder, write nothing. A year that
    fails is acceptable only if its MANIFEST row already says "AVG not derivable"; otherwise exit 1."""
    import glob
    rows = {}
    if os.path.exists(manifest):
        for r in csv.reader(open(manifest, encoding='utf-8', newline='')):
            if r and r[0].isdigit():
                rows[int(r[0])] = r[-1]
    bad = 0
    pages = sorted(glob.glob(os.path.join(reg, 'FantasyPros_*_Overall_ADP_Rankings.csv')))
    if not pages:
        print(f'  no FantasyPros_*_Overall_ADP_Rankings.csv in {reg}')
        return 1
    for path in pages:
        year = int(re.search(r'FantasyPros_(\d{4})_', os.path.basename(path)).group(1))
        df, sites = read_fp(path)
        chk = check_avg(df, sites)
        print(f'{year}: {len(df)} rows, sites {", ".join(sites)}')
        print_avg(chk)
        said = 'AVG not derivable' in rows.get(year, '')
        if chk['ok']:
            print(f'  ok    {avg_text(chk)}')
            if said:
                print(f'  NOTE  MANIFEST row {year} says not derivable, but it is. Rebuild the row.')
                bad += 1
        elif said:
            print(f'  ok    fails the guard and MANIFEST row {year} says so: {rows[year][:90]}...')
        else:
            print(f'  FAIL  {avg_text(chk)}')
            print(f'        and MANIFEST row {year} does not say so. Rebuild with --avg-not-derivable, or fix the page.')
            bad += 1
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int)
    ap.add_argument('--file', help='the FantasyPros export CSV (relative to this script, or absolute)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--allow-rank', action='store_true', help='accept a file whose AVG is 1..n (a rank); normally refused')
    ap.add_argument('--allow-ppr', action='store_true', help='accept the full-PPR page; normally refused (doc 385)')
    ap.add_argument('--avg-not-derivable', metavar='REASON',
                    help='accept a page whose AVG is not the mean of its site columns (doc 435); the reason goes on the MANIFEST row')
    ap.add_argument('--out', metavar='FOLDER',
                    help='write the registry file, the raw copy and MANIFEST.csv here instead of Source\\adp_registry')
    ap.add_argument('--exported', metavar='TEXT', help='the day the page was exported, for the MANIFEST row (default: today)')
    ap.add_argument('--note', default='', help='a provenance note carried onto the MANIFEST row, e.g. what the file replaced')
    ap.add_argument('--check-avg', action='store_true',
                    help='run the AVG check on every raw page in the registry folder, write nothing, exit 1 on an unrecorded failure')
    a = ap.parse_args()

    reg, arch, manifest = REG, ARCH, MANIFEST
    if a.out:
        # a rebuild into a folder of its own: the live registry is read for the comparison and never written
        reg = os.path.abspath(a.out)
        arch = os.path.join(reg, '_archive')
        manifest = os.path.join(reg, 'MANIFEST.csv')
        os.makedirs(arch, exist_ok=True)
        if not os.path.exists(manifest):
            if os.path.exists(MANIFEST):
                shutil.copyfile(MANIFEST, manifest)
            else:
                with open(manifest, 'w', encoding='utf-8', newline='') as fh:
                    csv.writer(fh).writerow(['season', 'n', 'min', 'max', 'source'])
    if a.check_avg:
        sys.exit(check_all(reg, manifest))
    if a.year is None or not a.file:
        sys.exit('need --year and --file (or --check-avg)')

    # a bare file name is looked for in the 2026 folder (where the exports land), then next to this script
    cands = [a.file] if os.path.isabs(a.file) else [os.path.join(ROOT, a.file), os.path.join(HERE, a.file)]
    src = next((os.path.normpath(c) for c in cands if os.path.exists(c)), None)
    if src is None:
        sys.exit(f'missing input file: {a.file} (looked in {ROOT} and {HERE})')
    for p in (reg, arch):
        if not os.path.isdir(p):
            sys.exit(f'missing folder: {p}')

    df, sites = read_fp(src)
    if is_rank(df.adp) and not a.allow_rank:
        sys.exit(f'REFUSED: AVG is exactly 1..{len(df)} with no gaps. That is a RANK, not an ADP (doc 383). '
                 f'Export the ADP page, not a rankings page.')
    scoring = scoring_of(src, sites)
    if scoring == 'ppr' and not a.allow_ppr:
        sys.exit(f'REFUSED: {os.path.basename(src)} is the FULL-PPR page (sites: {", ".join(sites)}). '
                 f'The registry is the half-PPR page (Yahoo, Sleeper, RTSports), the same instrument as '
                 f'2022 to 2024 (doc 385). Use the half-point export, or pass --allow-ppr on purpose.')
    # check 2c (doc 435): is AVG the mean of the site columns, and of which ones
    chk = check_avg(df, sites)
    print(f'year {a.year}: AVG against the site columns, every subset tried:')
    print_avg(chk)
    if not chk['ok']:
        print(f'  AVG IS NOT DERIVABLE FROM THE SITE COLUMNS SHOWN: {chk["fails"]} of {chk["tested"]} rows with a '
              f'site value are off by more than {AVG_TOL}'
              + (f', and {chk["no_site"]} rows carry an AVG and no site value at all' if chk['no_site'] else '') + '.')
        if a.year == 2021:
            print('  That is the known 2021 case (doc 435): the export shows Yahoo and Sleeper on 295 of 495 rows and '
                  'nothing on 200, and its AVG is FantasyPros\' own composite, not a mean of what is shown.')
        if not a.avg_not_derivable:
            sys.exit(f'FAILED check 2c for {a.year}. The registry row would claim an average the page does not '
                     f'support. If the file is right and the AVG is a composite the export does not show, re-run '
                     f'with  --avg-not-derivable "<why>"  and the MANIFEST row will say so instead.')
        print(f'  accepted on --avg-not-derivable: {a.avg_not_derivable}')
    elif a.avg_not_derivable:
        sys.exit(f'REFUSED: --avg-not-derivable was passed but AVG IS the mean of {", ".join(chk["basis"])} on '
                 f'all {chk["tested"]} rows. Drop the flag; the MANIFEST row must not say otherwise.')
    new = pd.DataFrame({'player': df.player, 'adp': df.adp.round(1)})
    new['k'] = new.player.map(norm_name)
    dupes = new[new.k.duplicated(keep='first')]
    new = new.drop_duplicates('k', keep='first')

    dest = os.path.join(reg, f'preseason_adp_{a.year}.csv')
    raw_dest = os.path.join(reg, f'FantasyPros_{a.year}_Overall_ADP_Rankings.csv')
    live_dest = os.path.join(REG, f'preseason_adp_{a.year}.csv')      # the comparison is against the LIVE file
    # seconds, and never overwrite: on 22 Sept two runs in one minute wrote the same _HHMM name and the
    # second archive copy replaced the first, so the original 2025 file left the drive (doc 385)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    arch_file = os.path.join(arch, f'preseason_adp_{a.year}_replaced_{stamp}.csv')
    n_ = 1
    while os.path.exists(arch_file):
        n_ += 1
        arch_file = os.path.join(arch, f'preseason_adp_{a.year}_replaced_{stamp}_{n_}.csv')
    page = 'half-PPR' if scoring == 'half' else 'FULL-PPR (overridden with --allow-ppr)'
    exported = a.exported or f'{datetime.now():%d %b %Y}'
    source_txt = (f'FantasyPros_{a.year}_Overall_ADP_Rankings.csv :: {avg_text(chk, a.avg_not_derivable)}; '
                  f'FantasyPros {page} archive page, exported {exported}'
                  + (f'; {a.note}' if a.note else '')
                  + ' (adp_registry_from_fp.py, docs 384, 385 and 435)')

    print(f'year {a.year}: {len(df)} export rows, {len(new)} registry rows, adp {new.adp.min():.1f} to {new.adp.max():.1f}, '
          f'sites on the page: {", ".join(sites) if sites else "none named"}')
    if len(dupes):
        print(f'  {len(dupes)} duplicate name keys dropped (first kept): {", ".join(dupes.player.head(5))}')
    print('  against the file it replaces:', compare(live_dest, new))
    print(f'  paste into code_adp_guard.py PRESEASON_SOURCES: {a.year}: "{source_txt}",')
    if a.dry_run:
        print('  dry run: nothing written')
        return

    if os.path.exists(dest):
        shutil.copyfile(dest, arch_file)
        assert open(arch_file, 'rb').read() == open(dest, 'rb').read(), 'archive copy does not match'
        print(f'  archived old registry file to {arch_file}')
    # CRLF on purpose: the drive's registry files were written by pandas on Windows, which uses the
    # platform line ending, so a rebuild on any other machine came out LF and could not be diffed byte
    # for byte against them (found rebuilding all five years off the drive, 29 Sept). On Windows this
    # changes nothing. pandas older than 1.5 spells the argument line_terminator.
    try:
        new.to_csv(dest, index=False, lineterminator='\r\n')
    except TypeError:
        new.to_csv(dest, index=False, line_terminator='\r\n')
    if os.path.normpath(src) != os.path.normpath(raw_dest):
        shutil.copyfile(src, raw_dest)
    rows = list(csv.reader(open(manifest, encoding='utf-8', newline='')))
    hdr, body = rows[0], rows[1:]
    body = [r for r in body if r and r[0] != str(a.year)]
    body.append([str(a.year), str(len(new)), f'{new.adp.min():.1f}', f'{new.adp.max():.1f}', source_txt])
    body.sort(key=lambda r: int(r[0]))
    with open(manifest, 'w', encoding='utf-8', newline='') as fh:
        csv.writer(fh).writerows([hdr] + body)
    # verify by content, not by the write call (directive section 9)
    back = pd.read_csv(dest)
    assert len(back) == len(new) and abs(back.adp.sum() - new.adp.sum()) < 0.05, 'written file does not match'
    print(f'  wrote {dest}, {raw_dest}, MANIFEST row {a.year}'
          + ('' if a.out else '. Now: re-run JOB 4 and the doc 383 batch on it.'))


if __name__ == '__main__':
    main()
