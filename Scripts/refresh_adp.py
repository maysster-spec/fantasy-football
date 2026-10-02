#!/usr/bin/env python3
r"""
refresh_adp.py -- re-freeze the market, without rebuilding the board.

    py refresh_adp.py            show what would change   (default, writes nothing)
    py refresh_adp.py --write    apply it

WHY THIS EXISTS (doc 109). `sept5_check.py` compares `proj_2026` and nothing else, so the
FREEZE/REBUILD verdict is entirely about PROJECTIONS. `adp_pick` -- the market -- rides along as
a silent side effect: FREEZE keeps the old ADP, REBUILD happens to bring a new one. Nobody chose
that, and it is backwards, because MEASURED between the Aug-23 and Aug-30 pulls:

    projections changed on   47 of the top 161
    ADP changed on          160 of the top 161, median 1.43 picks, max 12.77
    only 104 of 161 stayed within 2 slots of their old ADP ORDER

The thing the Sept-5 test watches barely moves. The thing it ignores moves a lot -- and ADP is
what drives `eff_pick`, every survival number, every "take at 104" on the paper sheets, and
`p(next)` on the live board.

WHAT THIS DOES: takes `espn_adp` from the newest good pull, recomputes `gone_ahead` and `eff_pick`
against the current keeper list, and writes them back. **It does not touch projections, VBD or
rank** -- those belong to the FREEZE/REBUILD decision and are not this script's business.
Archives the old board first, re-pins check_kit, and stamps the new vintage so board_audit knows
which pull to check against.
"""
import argparse, datetime as dt, glob, hashlib, os, re, shutil, sys
import pandas as pd

HERE   = os.path.dirname(os.path.abspath(__file__))
KIT    = os.path.join(HERE, 'live_draft')
BOARD  = os.path.join(KIT, 'board_v8_fixed.csv')
SRC    = os.path.normpath(os.path.join(HERE, '..', 'Source'))
ARCH   = os.path.normpath(os.path.join(HERE, '..', '_archive'))
KEEP   = os.path.join(HERE, 'actual_keepers.csv')
STAMP  = os.path.join(KIT, 'adp_vintage.txt')
CHECK  = os.path.join(HERE, 'check_kit.py')


def newest_pull():
    c = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    if not c: sys.exit(f"  no 2026 pull found in {SRC}")
    return c[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--pull', help='use this pull instead of the newest')
    a = ap.parse_args()

    pull = a.pull or newest_pull()
    p = pd.read_csv(pull); p.columns = [c.replace('﻿', '') for c in p.columns]
    if 'espn_adp' not in p.columns: sys.exit(f"  {os.path.basename(pull)} has no espn_adp column")
    b = pd.read_csv(BOARD)
    k = pd.read_csv(KEEP)

    print("=" * 74)
    print(f"  RE-FREEZE THE MARKET from {os.path.basename(pull)}"
          + ("" if a.write else "   (dry run)"))
    print("=" * 74)

    m = b.merge(p[['espn_id', 'espn_adp']], on='espn_id', how='left')
    if m.espn_adp.isna().any():
        miss = m[m.espn_adp.isna()]
        print(f"  !! {len(miss)} board players are not in this pull; they keep their old ADP.")
        for _, r in miss[miss['rank'] <= 161].iterrows():
            print(f"     rank {int(r['rank']):3d}  {r.player}")
    new_adp = m.espn_adp.round(2).fillna(b.adp_pick)

    # keeper depletion, recomputed against the CURRENT keeper list -- the same definition the
    # board builder uses: how many keepers have an ADP ahead of this player.
    # A raw name match found 11 of 12 -- one keeper carries a suffix or punctuation the pull
    # spells differently, and one missing keeper shifts gone_ahead by 1 for everyone behind him.
    # Normalise both sides (ERROR_PATTERNS C1) and REFUSE if it still cannot find all twelve.
    import re as _re, unicodedata as _u
    def _key(n):
        n = _u.normalize('NFKD', str(n)).encode('ascii', 'ignore').decode()
        n = _re.sub(r"[^A-Za-z ]", '', n)
        n = _re.sub(r'(?i)\b(jr|sr|ii|iii|iv|v)\b', '', n)
        return _re.sub(r'\s+', ' ', n).strip().lower()
    want = {_key(x) for x in k.Player}
    p['_k'] = p.Player.map(_key)
    hit = p[p._k.isin(want)]
    kadp = hit.espn_adp.dropna().sort_values().tolist()
    if len(hit) != len(k):
        missing = sorted(want - set(hit._k))
        sys.exit(f"  REFUSING: matched {len(hit)} of {len(k)} keepers in the pull.\n"
                 f"  Unmatched: {missing}\n"
                 f"  One missing keeper moves gone_ahead by 1 for every player behind him, so the\n"
                 f"  eff_pick this would write would be wrong. Fix the name in actual_keepers.csv.")
    gone = new_adp.map(lambda x: sum(1 for v in kadp if v < x))
    eff  = (new_adp - gone).round(2)

    d = pd.DataFrame(dict(player=b.player, rank=b['rank'], old=b.adp_pick, new=new_adp,
                          old_eff=b.eff_pick, new_eff=eff))
    d['move'] = (d.new - d.old).round(2)
    top = d[d['rank'] <= 161]
    print(f"  players compared            {len(d)}")
    print(f"  ADP changed in the top 161  {int((top.move.abs() > 0.005).sum())} of {len(top)}"
          f"   median |move| {top.move.abs().median():.2f}  max {top.move.abs().max():.2f}")
    big = top.reindex(top.move.abs().sort_values(ascending=False).index).head(12)
    print("\n  biggest movers (a negative move means the market now takes him EARLIER):")
    for _, r in big.iterrows():
        print(f"    rank {int(r['rank']):3d}  {r.player:<24} {r.old:6.2f} -> {r.new:6.2f}"
              f"   ({r.move:+6.2f})   your pick moves {r.old_eff:6.1f} -> {r.new_eff:6.1f}")

    if not a.write:
        print("\n  DRY RUN -- nothing written. Re-run with --write.")
        return

    os.makedirs(ARCH, exist_ok=True)
    st = f"{dt.datetime.now():%Y%m%d_%H%M}"
    shutil.copy2(BOARD, os.path.join(ARCH, f"board_v8_fixed_preADP_{st}.csv"))
    b['adp_pick'] = new_adp
    b['gone_ahead'] = gone
    b['eff_pick'] = eff
    b.to_csv(BOARD, index=False)
    open(STAMP, 'w', encoding='utf-8').write(os.path.basename(pull) + "\n")
    print(f"\n  archived the old board to {ARCH}")
    print(f"  wrote {BOARD}")
    print(f"  stamped the vintage in {os.path.basename(STAMP)}")
    repin(BOARD)
    print("\n  NOW, IN THIS ORDER:")
    print("    py board_audit.py            (must still pass)")
    print("    py make_fallback.py          (the paper board's 'goes at' just moved)")
    print("    py depth_map.py              (the sheets read goes_at from the board)")
    print("  The ESPN prerank does NOT need re-injecting: it is ordered by VBD rank, and this")
    print("  script does not touch rank. Only the TIMING numbers moved.")


def repin(pth):
    if not os.path.exists(CHECK): return
    d = open(pth, 'rb').read().replace(b'\r\n', b'\n')
    name = os.path.basename(pth)
    s = open(CHECK, encoding='utf-8').read()
    new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
    s2 = re.sub(r"(    '" + re.escape(name) + r"':\s+)\(\d+, '[0-9a-f]{16}'\),",
                lambda m: m.group(1) + new, s, count=1)
    if s2 != s:
        open(CHECK, 'w', encoding='utf-8', newline='').write(s2)
        print(f"  re-pinned {name}: {new.strip('(),')}")


if __name__ == '__main__':
    main()
