#!/usr/bin/env python3
r"""
apply_news.py -- push real-world news into the board and the ESPN prerank.

    py apply_news.py            show what would change  (default, writes nothing)
    py apply_news.py --write    apply it, archive the originals, re-pin check_kit

WHY THIS EXISTS (doc 97)
    DRAFT_DAY_GUIDE has carried this gap in writing since it was written: "a late injury has no
    automated catch." On Aug 30 the NFL put Josh Jacobs on the Commissioner's Exempt List. He is
    board rank 20, VBD +72.5, and his effective pick is 32.42 -- which is Matt's pick 32 almost
    exactly. Nothing in the system would have moved him, and the engine would have recommended
    him on the clock.

    The board is BUILT from ESPN's projections. ESPN may or may not re-forecast a suspended
    player before Sept 7 (the Aug-29 drift check found 0 of 700 projections changed in 8 hours),
    so waiting for the pull to fix it is a hope, not a plan. This applies the correction on top,
    from a file you can read and reverse.

THE OVERRIDE FILE   Scripts\news_overrides.csv
    espn_id,player,action,dated,note
    action = out     projection -> 0. VBD becomes -replacement, so he sinks to the bottom of the
                     board and the bottom of the prerank's skill block, but the row SURVIVES --
                     a late flyer is still possible and still priced honestly.
           = remove  drop the row entirely. Use only when a player is off an NFL roster.

    ADP is deliberately NOT touched. A suspended player still costs the field a pick if someone
    reaches on him, and keeper depletion (gone_ahead / eff_pick) is about keepers, not injuries.
    The Sept 5 pull re-derives ADP from ESPN on its own.

RE-RUN THIS AFTER EVERY BOARD REBUILD. A REBUILD verdict on Sept 5 regenerates the board from
the pull and will wipe these edits. `board_audit.py` now fails loudly if an override in this
file is not present on the board, so a wiped edit cannot go unnoticed.
"""
import argparse, csv, datetime as dt, hashlib, os, re, shutil, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
KIT   = os.path.join(HERE, 'live_draft')
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
PRE   = os.path.join(KIT, 'ESPN_prerank_with_ids.csv')
OVR   = os.path.join(HERE, 'news_overrides.csv')
CHECK = os.path.join(HERE, 'check_kit.py')
ARCH  = os.path.normpath(os.path.join(HERE, '..', '_archive'))


def load_overrides():
    if not os.path.exists(OVR):
        sys.exit(f"  no override file at {OVR} -- nothing to do.")
    o = pd.read_csv(OVR)
    need = {'espn_id', 'player', 'action'}
    if not need <= set(o.columns):
        sys.exit(f"  {os.path.basename(OVR)} must have columns {sorted(need)}; it has {list(o.columns)}")
    bad = set(o.action) - {'out', 'remove'}
    if bad:
        sys.exit(f"  unknown action(s) {sorted(bad)} -- only 'out' and 'remove' are understood.")
    return o


def replacement_from(b):
    """Derive replacement per position from the board itself: vbd = proj - repl, so
    repl = proj - vbd. Every row of a position must agree, or the board is already broken.
    Deriving beats hard-coding -- doc 94's first two 'failures' were hard-coded constants."""
    repl = {}
    for pos, g in b.groupby('pos'):
        r = (g.proj_leaguepts - g.vbd)
        if r.max() - r.min() > 1e-6:
            sys.exit(f"  board is inconsistent at {pos}: proj-vbd spans {r.min()}..{r.max()}")
        repl[pos] = float(r.iloc[0])
    return repl


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='actually apply it')
    a = ap.parse_args(argv)

    o = load_overrides()
    b = pd.read_csv(BOARD)
    p = pd.read_csv(PRE)
    repl = replacement_from(b)
    print("=" * 74)
    print(f"  APPLY NEWS -- {len(o)} override(s) from {os.path.basename(OVR)}")
    print("=" * 74)

    changed = 0
    for _, r in o.iterrows():
        eid = int(r.espn_id)
        hit = b.espn_id.astype('Int64') == eid
        if not hit.any():
            print(f"  !! {r.player} (id {eid}) is NOT on the board. Override ignored -- check the id.")
            continue
        row = b[hit].iloc[0]
        if r.action == 'remove':
            print(f"  REMOVE  {row.player:<22} {row.pos}  rank {int(row['rank']):>3}  "
                  f"vbd {row.vbd:+.1f}  ->  off the board entirely")
            b = b[~hit]
            p = p[p.ESPN_ID.astype('Int64') != eid]
        else:
            new_vbd = 0.0 - repl[row.pos]
            print(f"  OUT     {row.player:<22} {row.pos}  rank {int(row['rank']):>3}  "
                  f"proj {row.proj_leaguepts:.1f} -> 0.0   vbd {row.vbd:+.1f} -> {new_vbd:+.1f}")
            b.loc[hit, 'proj_leaguepts'] = 0.0
            b.loc[hit, 'vbd'] = new_vbd
            p.loc[p.ESPN_ID.astype('Int64') == eid, 'vbd'] = new_vbd
        changed += 1
        if isinstance(r.get('note'), str):
            print(f"          {r['note'][:96]}")

    if not changed:
        print("\n  nothing applied."); return 0

    # Re-sort and renumber both files exactly the way the builder does: board by VBD desc,
    # prerank by the board's order with the K/D-ST tail left where it is.
    b = b.sort_values('vbd', ascending=False, kind='mergesort').reset_index(drop=True)
    b['rank'] = range(1, len(b) + 1)

    skill = p[~p.pos.isin(['K', 'D/ST'])].copy()
    tail  = p[p.pos.isin(['K', 'D/ST'])].copy()
    order = {int(e): i for i, e in enumerate(b.espn_id.astype(int))}
    skill['_o'] = skill.ESPN_ID.astype(int).map(order)
    skill = skill.sort_values('_o', kind='mergesort').drop(columns='_o')
    p = pd.concat([skill, tail], ignore_index=True)
    p['prerank'] = range(1, len(p) + 1)

    moved = [(int(r.espn_id), r.player) for _, r in o.iterrows()]
    for eid, nm in moved:
        w = b.index[b.espn_id.astype('Int64') == eid]
        if len(w):
            print(f"\n  {nm}: board rank -> {int(b.loc[w[0], 'rank'])} of {len(b)}   "
                  f"prerank -> {int(p.loc[p.ESPN_ID.astype('Int64') == eid, 'prerank'].iloc[0])} of {len(p)}")

    if not a.write:
        print("\n  DRY RUN -- nothing written. Re-run with --write to apply.")
        return 0

    os.makedirs(ARCH, exist_ok=True)
    stamp = f"{dt.datetime.now():%Y%m%d_%H%M}"
    for src in (BOARD, PRE):
        root, ext = os.path.splitext(os.path.basename(src))
        shutil.copy2(src, os.path.join(ARCH, f"{root}_{stamp}{ext}"))
    print(f"\n  originals archived to {ARCH} with suffix _{stamp}")

    b.to_csv(BOARD, index=False)
    p.to_csv(PRE, index=False)
    print(f"  wrote {BOARD}")
    print(f"  wrote {PRE}")

    repin(BOARD); repin(PRE)
    print("\n  DONE. Now do BOTH of these, in this order:")
    print("    py board_audit.py                     (must still be 37+ of 37)")
    print("    py espn_draft_injector_Gemini.py      (ESPN is still holding the OLD prerank)")
    print("    py verify_prerank.py")
    return 0


def norm(pth):
    return open(pth, 'rb').read().replace(b'\r\n', b'\n')


def repin(pth):
    """check_kit pins these files by hash; a deliberate edit must move the pin with it, or the
    next run cries STALE about a change we made on purpose and the warning stops meaning anything."""
    if not os.path.exists(CHECK):
        print(f"  (check_kit.py not found -- re-pin {os.path.basename(pth)} by hand)"); return
    d = norm(pth)
    name = os.path.basename(pth)
    s = open(CHECK, encoding='utf-8').read()
    pat = re.compile(r"(    '" + re.escape(name) + r"':\s+)\(\d+, '[0-9a-f]{16}'\),")
    if not pat.search(s):
        print(f"  (no pin for {name} in check_kit.py -- nothing to update)"); return
    new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
    open(CHECK, 'w', encoding='utf-8', newline='').write(pat.sub(lambda m: m.group(1) + new, s, count=1))
    print(f"  re-pinned {name}: {new.strip('(),')}")


if __name__ == '__main__':
    sys.exit(main() or 0)
