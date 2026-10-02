#!/usr/bin/env python3
r"""
make_board_file.py -- THE BUILDER `board_v8_fixed.csv` NEVER HAD.  Doc 150, closing doc 62.

    THIS FILE LIVES IN `Scripts\`, NEVER IN `Scripts\live_draft\`.  doc 151 finding 1: the kit
    folder is an EXACT SET to check_kit.py, so a stray copy of this script (or of its output)
    there reports EXTRA, check_kit exits 1, and `draft_night.bat` aborts at step 1/5 -- at 7:00 PM.

    py make_board_file.py              rebuild from the Aug-23 spine and prove it reproduces
                                       the shipped board exactly. Writes NOTHING. Do this first.
                                       (`--verify` is accepted and means the same thing.)
    py make_board_file.py --write      write Source\board_v8_REBUILT.csv (never over the live one)

WHY THIS EXISTS.  Doc 62 (Aug 28) found that no script anywhere produces `board_v8_fixed.csv` --
the 480-row file the live engine loads.  It was made by ad-hoc code during the Aug-27 red team and
the recipe was never written down.  That was TRUE.  What happened next was not: "it has no builder"
hardened into "it cannot be rebuilt", and that stronger claim went unchallenged for a week and was
told to Matt three times.  Matt: *"I'm still lost as to why the board can't be rebuilt. It was
built after all."*  He was right.  Every step below was recovered by measurement in about ten
minutes, and every one of them reproduces exactly.

THE RECIPE, AND WHAT PROVES EACH STEP (all measured 2026-09-03, not reasoned):

  1. START FROM THE SPINE, SKILL POSITIONS ONLY.
     `code_universe_v5.csv` holds 700 rows; 636 are QB/RB/WR/TE.  The 32 kickers and 32
     defences are not on this board at all -- they live in `board_v7_kdst_separate.csv`,
     which is why 4.8's "draft-day D/ST value is an illusion" never had to be enforced here.

  2. DROP EVERY ROW WITH NO REAL PROJECTION.  `proj_missing == True` on exactly 144 of the
     636.  Not one of them is on the board; not one on-board row has it set.

  3. DROP THE TWELVE KEEPERS.  That leaves 636 - 144 - 12 = 480.  EXACT, not approximately:
     the twelve excluded rows that DO carry a projection are precisely the twelve names in
     `actual_keepers.csv` -- Maye, Javonte Williams, Etienne, Rice, Skattebo, Olave, Pickens,
     Flowers, McMillan, Loveland, Stevenson, Diggs.  This is 2.1(c): the pool is depleted
     from pick 1, so the keepers are not board rows.
     NOTE the selection is NOT a projection cutoff.  Drake Maye is excluded at 373.1 -- higher
     than all but a handful of the board -- and on-board projections run down to 0.0.  Any
     rebuild that ranked by projection and took the top 480 would produce a different board and
     look plausible doing it.

  4. VBD = projection - 4.1's replacement level, by position.  Max error over all 480 rows:
     0.000426.  No hidden term.

  5. rank = descending VBD rank.  480 of 480 agree.

  6. eff_pick = adp_pick - gone_ahead (2.1(e)); `board_audit.py` already re-derives this.
     ADP is whatever the current freeze is -- `adp_vintage.txt` names it -- and `refresh_adp.py`
     owns that column.  THIS SCRIPT DOES NOT TOUCH ADP.

  7. RE-APPLY THE NEWS OVERRIDES LAST.  479 of the 480 projections equal the spine's to 1e-6.
     The one exception is Josh Jacobs at 0.0 against the spine's 241.045 -- `apply_news.py`,
     Commissioner's Exempt List, Aug 30.  A rebuild that skipped this would silently restore a
     suspended player to rank 20, which is doc 101's defect exactly.

WHAT THIS SCRIPT DELIBERATELY DOES NOT DO, AND WHY IT MATTERS MORE THAN WHAT IT DOES:

  **It does not point at a newer projection pull, and you should not make it.**  The mechanics
  of a rebuild are easy -- that is this file.  The reason the board is frozen is not mechanical:
  4.1's replacement levels, 4.2's pick-8 dollars, 4.10's rule ranking and 4.12's noise fit were
  every one of them FITTED AGAINST THIS PROJECTION SET.  Swap the points and each of those
  numbers describes a board that no longer exists, four days before it is used.  That is the
  argument for the freeze, and it survives this script existing.  Post-draft, with time to
  re-fit, this is the file that makes a real refresh possible.
"""
import argparse, os, re, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
KIT  = os.path.join(HERE, 'live_draft')
# doc 151, red-team finding 9.  These were 4.1's PUBLISHED values -- three decimal places -- and
# the comment called them "full precision", which they are not.  The true levels are recoverable
# exactly from the shipped board: `proj - vbd` is a constant per position (min == max over all 480
# rows).  The rounding was the entire 4.26e-4 vbd gap, and because the four offsets differ it
# deterministically re-ordered the four-way tie at ranks 69-72 (Dart/Metcalf/Warren/Andrews, all
# at vbd exactly 0.0).  With the exact values the tolerance drops to 1e-9.
# Recovered to full float precision, not six decimals: `proj - vbd` per position has a
# spread of 5.7e-14 across all 480 rows, i.e. it IS the constant. 4.1 publishes these
# rounded to three places (341.603 / 168.589 / 163.540 / 140.295); these are the values
# the board was actually built with.
REPL = {'QB': 341.602860180, 'RB': 168.588855840,
        'WR': 163.539573570, 'TE': 140.294884170}


def norm(s):
    """The project's canonical normaliser -- COPIED, not reinvented, from board_audit.py:111
    and keeper_swap.py:32.  My first version here stripped punctuation only, so 'Travis Etienne'
    in actual_keepers.csv failed to match 'Travis Etienne Jr.' on the spine, the rebuild came out
    481 rows instead of 480, and Etienne -- another manager's keeper -- would have been sitting on
    the board as available.  That is SS3's identity rule word for word: 10% of this board's names
    carry a suffix, period or apostrophe.  One shared normaliser, or none."""
    s = re.sub(r"\s+(Jr\.|Sr\.|II|III|IV|V)$", '', str(s).strip(), flags=re.I)
    return re.sub(r"[.'\u2019-]", '', s).lower()


def build(spine, keepers, live, news):
    u = pd.read_csv(spine)
    b = pd.read_csv(live)
    # doc 151, finding 8: `isin(REPL)` silently dropped anything else -- an 'FB', a lowercase
    # 'rb', a new position code -- and the only thing standing between that and a quietly short
    # board was the hardcoded 636.
    unknown = sorted(set(u.pos.dropna()) - set(REPL) - {'K', 'D/ST'})
    assert not unknown, f'spine carries positions this builder does not know: {unknown}'
    assert u.espn_id.is_unique, 'spine has duplicate espn_id -- refusing to build'
    sk = u[u.pos.isin(REPL)].copy()
    assert len(sk) == 636, f'spine skill rows: {len(sk)}, expected 636'
    sk = sk[~sk.proj_missing.astype(bool)]
    kp = pd.read_csv(keepers)
    kn = {norm(x) for x in kp.Player}
    hit = sk.player.map(lambda p: norm(p) in kn)
    # LOUD, NOT SILENT.  A keeper that fails to resolve leaves another manager's player on the
    # board as available -- the most expensive silent error this file could make.
    # doc 151, finding 5: my first version compared `hit.sum()` -- a count of matched SPINE ROWS --
    # against 12, so ONE UNRESOLVED KEEPER PLUS ONE DUPLICATE NORMALISING NAME CANCELLED OUT and
    # the assert stayed quiet while Chris Olave sat on the rebuilt board at rank 29. Compare the
    # SETS, and check the roster size separately.
    assert len(kp) == 12, f'actual_keepers.csv has {len(kp)} rows, expected 12'
    matched = set(sk.player[hit].map(norm))
    missing = sorted(p for p in kp.Player if norm(p) not in matched)
    assert not missing, (f'{len(kp)-len(missing)} of 12 keepers resolved against the spine. '
                         f'Unmatched: {", ".join(missing)}')
    sk = sk[~hit]
    out = sk[['espn_id', 'player', 'pos', 'team_c', 'bye', 'proj_leaguepts']].copy()
    # the news overrides, re-applied -- see step 7
    if not os.path.exists(news):
        # doc 151, finding 11b: skipping this silently restores a suspended player to his old rank.
        print(f'  !! {news} not found -- NO news overrides applied. If one is live, this board is')
        print('     wrong in exactly the way doc 101 describes. Do not use it.')
    else:
        nw = pd.read_csv(news)
        # doc 151, finding 3: `col = next(..., None)` then `if col and ...` FAILED OPEN -- with no
        # column containing "action", every row was zeroed whatever it said. Pointing --news at any
        # CSV without that column zeroed the entire board and still printed REPRODUCED.
        col = next((c for c in nw.columns if 'action' in c.lower()), None)
        assert col is not None, (f'{os.path.basename(news)} has no action column '
                                 f'(columns: {list(nw.columns)}) -- refusing to guess')
        for _, r in nw.iterrows():
            if str(r[col]).strip().lower() not in ('out', 'remove'):
                continue
            # doc 151, finding 4: an espn_id that is not on the board matched nothing and the run
            # still printed REPRODUCED, exit 0 -- the one silent failure that survived the whole
            # verification, and precisely the doc-101 class step 7 claims to prevent.
            hit_n = int((out.espn_id == r.espn_id).sum())
            assert hit_n == 1, (f'news override for espn_id {r.espn_id} '
                                f'({r.get("player", "?")}) matched {hit_n} board rows, expected 1. '
                                f'A keeper or a mistyped id -- fix news_overrides.csv.')
            out.loc[out.espn_id == r.espn_id, 'proj_leaguepts'] = 0.0
    out['vbd']  = out.proj_leaguepts - out.pos.map(REPL)
    out['rank'] = out.vbd.rank(ascending=False, method='first').astype(int)
    # ADP is refresh_adp.py's column, and it is re-frozen independently -- carry it across
    out = out.merge(b[['espn_id', 'adp_pick', 'gone_ahead', 'flag', 'bye_clash_pickens']],
                    on='espn_id', how='left')
    out['eff_pick'] = (out.adp_pick - out.gone_ahead).round(2)
    return out.sort_values('rank').reset_index(drop=True), b


def main(argv=None):
    ap = argparse.ArgumentParser()
    # doc 151, finding 2: the docstring and doc 150 both told you to type --verify, and argparse
    # had never heard of it -- so the FIRST command anyone runs exited 2 with no output and read
    # as "the builder is broken". It is the default; accept the word for it.
    ap.add_argument('--verify', action='store_true',
                    help='the default: rebuild and compare, write nothing')
    ap.add_argument('--write', action='store_true',
                    help='additionally write Source\\board_v8_REBUILT.csv (never the live board)')
    ap.add_argument('--spine',   default=os.path.join(SRC, 'code_universe_v5.csv'))
    ap.add_argument('--keepers', default=os.path.join(HERE, 'actual_keepers.csv'))
    ap.add_argument('--live',    default=os.path.join(KIT, 'board_v8_fixed.csv'))
    ap.add_argument('--news',    default=os.path.join(HERE, 'news_overrides.csv'))
    a = ap.parse_args(argv)

    new, old = build(a.spine, a.keepers, a.live, a.news)
    print(f'\n  rebuilt {len(new)} rows from {os.path.basename(a.spine)}')
    bad = 0
    if len(new) != len(old):
        print(f'  ROW COUNT  rebuilt {len(new)} vs shipped {len(old)}'); bad += 1
    else:
        same_ids = set(new.espn_id) == set(old.espn_id)
        print(f"  {'ok   ' if same_ids else 'FAIL '} the same 480 players "
              f"({len(set(new.espn_id) ^ set(old.espn_id))} differences)")
        bad += (not same_ids)
        # doc 151, finding 6: this compared five numeric columns and NOTHING ELSE, so a rebuild
        # carrying "Bijan Rodriguez, ZZZ, bye 1" instead of "Bijan Robinson, ATL, bye 11" printed
        # REPRODUCED and exited 0. `bye` is load-bearing -- 4.11's BYE CHECK reads it.
        for c in ('player', 'pos', 'team_c', 'bye'):
            mm = old[['espn_id', c]].merge(new[['espn_id', c]], on='espn_id',
                                           suffixes=('_old', '_new'))
            n_bad = int((mm[c + '_old'].astype(str) != mm[c + '_new'].astype(str)).sum())
            print(f"  {'ok   ' if not n_bad else 'FAIL '} {c:<16} {n_bad} mismatch(es)")
            bad += bool(n_bad)
        m = old[['espn_id', 'rank', 'proj_leaguepts', 'vbd', 'eff_pick']].merge(
            new[['espn_id', 'rank', 'proj_leaguepts', 'vbd', 'eff_pick']],
            on='espn_id', suffixes=('_old', '_new'))
        # vbd's tolerance is 1e-9 now that REPL carries the exact levels (finding 9). eff_pick's
        # check is CIRCULAR and labelled as such -- see the banner note below.
        for c, tol in (('proj_leaguepts', 1e-6), ('vbd', 1e-9), ('eff_pick', 0.011)):
            d = float(np.abs(m[c + '_old'] - m[c + '_new']).max())
            ok = d <= tol
            bad += (not ok)
            print(f"  {'ok   ' if ok else 'FAIL '} {c:<16} max|diff| = {d:.2e}  (tol {tol:g})")
        # RANK: separate a real disagreement from a tie-break.  Two rows with the SAME vbd carry
        # no information about which comes first -- the shipped board's order among them came from
        # whatever row order the ad-hoc code happened to have, and is not recoverable or worth
        # recovering.  What must reproduce is the order of rows that are NOT tied.
        diff = m[m['rank_old'] != m['rank_new']].merge(
            old[['espn_id', 'vbd']].rename(columns={'vbd': 'v'}), on='espn_id')
        tiedv = set(old.vbd.round(6)[old.vbd.round(6).duplicated(keep=False)])
        ties = diff[diff.v.round(6).isin(tiedv)]
        real = diff[~diff.v.round(6).isin(tiedv)]
        print(f"  {'ok   ' if real.empty else 'FAIL '} rank             "
              f"{len(m) - len(diff)} of {len(m)} identical; {len(ties)} differ ONLY inside a "
              f"vbd tie{'' if ties.empty else f' (deepest rank {int(ties.rank_old.min())}+)'}"
              f"{'' if real.empty else f'; {len(real)} REAL disagreements'}")
        bad += (not real.empty)
    print()
    if bad:
        print(f'  *** {bad} CHECK(S) FAILED -- this is NOT a recovery of the shipped board.')
        print('  *** Do not use it, and do not point it at a newer pull. (doc 62 SS5: do B only')
        print('  *** if it reproduces exactly; otherwise take A and stay frozen.)')
        return 1
    print('  REPRODUCED. Same 480 players, same names/teams/byes, same projections, same VBD,')
    print('  and the same order everywhere the order means anything. The board has a builder.')
    # doc 151, finding 7: the banner used to claim "same eff_pick". It cannot. adp_pick and
    # gone_ahead are COPIED off the live board (refresh_adp.py owns them), so recomputing
    # eff_pick from them and comparing tests the live board's internal consistency and nothing
    # about the rebuild -- setting every spine adp_pick to 999 still gave max|diff| = 0.00.
    print('  NOTE: the eff_pick line above is circular -- ADP is copied from the live board, not')
    print('  rebuilt. It checks that board\'s own consistency. refresh_adp.py owns that column.')
    if a.write:
        p = os.path.join(SRC, 'board_v8_REBUILT.csv')
        new.to_csv(p, index=False)
        print(f'  wrote {p}  -- deliberately NOT over the live board.')
    else:
        print('  Nothing written. --write puts a copy in Source\\ for inspection.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
