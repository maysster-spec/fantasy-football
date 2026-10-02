#!/usr/bin/env python3
r"""
check_adp_vintage.py -- does the board's ADP actually match the pull it CLAIMS?

    py check_adp_vintage.py

WHY THIS EXISTS (doc 172). On Sept 5 `refresh_adp.py --write` ran: it archived the board to
`_archive\board_v8_fixed_preADP_20260905_1120.csv` and it stamped
`adp_vintage.txt` with `espn_projections_2026_20260905_1040.csv`. But the board's `adp_pick`
still matched the **09-03** pull on 448 of 448 rows, to 0.00.

Nothing caught it. `board_audit.py` reads the stamp, and the stamp was the thing that was wrong,
so the board and its own provenance agreed with each other about a lie. That is s0.2's
"an exit code is not a result" one level up: **the artifact that records what happened is not
evidence that it happened.** The only proof is comparing the numbers themselves.

It exits non-zero on a mismatch so a batch file can branch on it.

Standard library + pandas only; paths resolve against this file (s0.4 v6.8).
"""
import glob, os, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'live_draft')
SRC = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
STAMP = os.path.join(KIT, 'adp_vintage.txt')
TOL = 0.05          # espn_adp is written to 2dp; anything above this is a real difference


def main():
    for p in (BOARD, STAMP):
        if not os.path.exists(p):
            print(f'  missing {p}')
            return 2
    claimed = open(STAMP, encoding='utf-8').read().strip()
    pull = os.path.join(SRC, claimed)
    print('=' * 74)
    print('  ADP VINTAGE CHECK')
    print('=' * 74)
    print(f'  the board claims : {claimed}')
    if not os.path.exists(pull):
        print(f'  !! that pull is not in Source\\ -- cannot verify. FAIL')
        return 2

    b = pd.read_csv(BOARD)
    p = pd.read_csv(pull, usecols=['espn_id', 'espn_adp'])
    m = b[['espn_id', 'player', 'pos', 'rank', 'adp_pick']].merge(p, on='espn_id', how='inner')
    d = (m.adp_pick - m.espn_adp).abs()
    bad = int((d > TOL).sum())
    print(f'  rows comparable  : {len(m)} of {len(b)}   '
          f'({len(b) - len(m)} board players are not in that pull and keep their old ADP)')
    print(f'  rows that DISAGREE with the claim: {bad}   max difference {d.max():.2f}\n')

    if bad == 0:
        print('  PASS -- the board carries the ADP it says it does.')
        return 0

    print('  *** FAIL -- THE BOARD IS NOT FROZEN AGAINST THE PULL IT NAMES. ***')
    print('  Re-run:  py refresh_adp.py        (look)')
    print('           py refresh_adp.py --write')
    print('  then re-run this. If it still fails, the write is not taking and the ADP on the')
    print('  board is whatever the PREVIOUS freeze left -- read the numbers, not the stamp.\n')
    w = m.assign(diff=d).sort_values('diff', ascending=False)
    inside = w[w['rank'] <= 180].head(15)
    print('  worst disagreements inside the printed board (rank <= 180):')
    for _, r in inside.iterrows():
        print('    rank %3d  %-24s %-3s board %6.2f  vs claimed pull %6.2f  (%+6.2f)'
              % (r['rank'], str(r.player)[:24], r.pos, r.adp_pick, r.espn_adp,
                 r.espn_adp - r.adp_pick))
    # what it costs: most rows move a fraction of a pick and do not matter
    big = w[(w['rank'] <= 180) & (w['diff'] > 3)]
    print(f'\n  {int((w["rank"] <= 180).sum())} of these are inside the printed board; '
          f'{len(big)} of them move more than 3 picks.')
    print('  A tenth of a pick is noise. Judge it on that last number, not the first.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
