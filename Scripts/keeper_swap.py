#!/usr/bin/env python3
r"""
keeper_swap.py -- rebuild board_v8_fixed.csv for the ACTUAL keepers at the 7:00 PM lock.
This is also the board's recovered BUILDER (doc 62 closed): run with the predicted keepers
it reproduces the shipped board exactly.

    py keeper_swap.py --check      # rebuild from actual_keepers.csv, DIFF against current board, write nothing
    py keeper_swap.py --write      # archive the old board, then overwrite Scripts\live_draft\board_v8_fixed.csv

7:00 PM drill: edit actual_keepers.csv (12 player names), --check, read the diff, --write, restart live_draft.py.

Provenance (verified 480/480 against the shipped board, doc 70 follow-up):
  pool        = spine skill rows (code_universe_v5.csv) minus the 12 keepers
  adp_pick    = espn_adp from the 08-23 pull  (FROZEN vintage -- matches the shipped board)
  gone_ahead  = count of keeper 08-23 ADPs strictly below the player's adp_pick
  eff_pick    = adp_pick - gone_ahead
  vbd         = spine proj_leaguepts - replacement, DERIVED from the same frozen pull the
                board and board_audit use (not the directive's rounded quotes -- doc 101)
  rank        = vbd descending;  flag = spine injury_status (non-ACTIVE only);  bye_clash = bye==14 -> YES
"""
import argparse, datetime as dt, difflib, hashlib, os, re, shutil, sys
import numpy as np, pandas as pd

HERE   = os.path.dirname(os.path.abspath(__file__))
SRC    = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD  = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
ARCH   = os.path.normpath(os.path.join(HERE, '..', '_archive'))
KFILE  = os.path.join(HERE, 'actual_keepers.csv')
# doc 101: these were the DIRECTIVE's 3-decimal quotes. The shipped board was built with
# full precision, so a keeper-lock rebuild moved every VBD by up to 4.26e-04 -- numerically
# irrelevant, but enough to make board_audit FAIL at 7:05 PM on draft night. A gate that
# cries wolf an hour before the draft is worse than no gate. Derive from the same pull the
# board and the audit both use; fall back to the quoted constants only if that file is gone.
REPL_FALLBACK = {'QB':341.603,'RB':168.589,'WR':163.540,'TE':140.295}

def derive_repl():
    try:
        pf = pd.read_csv(ADP23, usecols=['pos','proj_2026'])
        out = {}
        for pos, n in (('RB',30),('WR',30),('QB',12),('TE',12)):
            col = pf[(pf.pos==pos) & pf.proj_2026.notna()].proj_2026.sort_values(ascending=False)
            out[pos] = float(col.iloc[n-1])
        return out
    except Exception as e:
        print(f"  (could not derive replacement from the pull: {e} -- using the quoted constants)")
        return dict(REPL_FALLBACK)
ADP23  = os.path.join(SRC, 'espn_projections_2026_20260823.csv')
SPINE  = os.path.join(SRC, 'code_universe_v5.csv')
KDST   = os.path.join(HERE, 'live_draft', 'board_v7_kdst_separate.csv')
STAMP  = os.path.join(HERE, 'live_draft', 'adp_vintage.txt')

# doc 164: THE MARKET COLUMN AND THE PROJECTION COLUMN COME FROM DIFFERENT PULLS, AND THIS
# SCRIPT WAS READING ONE FILE FOR BOTH.
#   * proj / replacement MUST stay on the 08-23 pull. doc 101: board_audit compares against
#     the shipped board's own VBD, and re-deriving replacement from a newer pull fails that
#     gate at 7:05 PM on draft night.
#   * adp_pick MUST follow the freeze. `refresh_adp.py` (doc 109) re-froze the market on
#     08-30 and again on 09-03 and stamped `adp_vintage.txt`; this script kept using 08-23,
#     so `--write` at the 7:00 PM lock would have silently rolled the market back 11 days.
#     MEASURED 2026-09-04 against the shipped board: 426 of 480 rows differ, and inside the
#     drafted range Kittle moves 24 slots, Godwin 23, Herbert 22, Aaron Jones and Pollard 20,
#     Hockenson 19. adp_pick drives eff_pick, every survival number and the SS2.1(c) table.
# Read the stamp; fall back to 08-23 only if it is missing, and say which was used.
def _market_pull():
    try:
        name = open(STAMP, encoding='utf-8').read().strip()
        if name:
            p = os.path.join(SRC, name)
            if os.path.exists(p):
                return p, name
            print(f"  !! adp_vintage.txt names {name}, which is not in Source\ -- "
                  f"falling back to the 08-23 pull.")
    except FileNotFoundError:
        print("  !! adp_vintage.txt is missing -- falling back to the 08-23 pull.")
    return ADP23, os.path.basename(ADP23)


def prune_streamers(nonskill, write):
    """doc 164. A kept K or D/ST is removed from board_v8_fixed.csv by construction -- he was
    never on it. He IS on board_v7_kdst_separate.csv, which NOTHING removes him from, and
    `Engine.streamers()` can only filter against players already in the live pick feed. This
    league's keepers do not enter that feed until overall 169-180, AFTER picks 152 and 161.
    So the board would have offered a kept kicker as the best one available, and Matt would
    have found out by having ESPN reject the pick with the clock running.
    2026: Brandon Aubrey (DAL) is the top kicker on the sheet by 10 projected points and is
    the kept player of Window is Always Open."""
    if not nonskill:
        return
    if not os.path.exists(KDST):
        print(f"  !! {KDST} is missing -- cannot check the streamer sheet.")
        return
    k = pd.read_csv(KDST)
    if 'ESPN_ID' not in k.columns:
        print("  !! streamer sheet has no ESPN_ID column -- refusing to prune it by name.")
        return
    ids = {i for _, _, i in nonskill}
    hit = k[k.ESPN_ID.isin(ids)]
    if not len(hit):
        print("  streamer sheet: none of them are on it -- nothing to prune.")
        return
    for _, r in hit.iterrows():
        pk = 152 if r.pos == 'D/ST' else 161
        print(f"  STREAMER SHEET: {r.player} ({r.pos}, {r.team_c}) is KEPT and would still be "
              f"offered at pick {pk}. Removing him.")
    if not write:
        print("  (--check: streamer sheet NOT written. Re-run with --write.)")
        return
    os.makedirs(ARCH, exist_ok=True)
    dst = os.path.join(ARCH, f"board_v7_kdst_separate_ARCHIVED_{dt.datetime.now():%Y%m%d_%H%M}.csv")
    shutil.copy2(KDST, dst)
    out = k[~k.ESPN_ID.isin(ids)]
    for pos in ('K', 'D/ST'):
        n = int((out.pos == pos).sum())
        if n < 12:
            print(f"  !! REFUSING: pruning would leave only {n} {pos} rows; "
                  f"code_live_engine asserts at least 12. Streamer sheet left alone.")
            return
    out.to_csv(KDST, index=False)
    print(f"  archived old streamer sheet -> {dst}")
    print(f"  WROTE {KDST}: {len(out)} rows (was {len(k)})")

def norm(s):
    s=re.sub(r'\s+(Jr\.|Sr\.|II|III|IV|V)$','',str(s).strip(),flags=re.I)
    return re.sub(r"[.'’-]",'',s).lower()



def rebuild_prerank():
    """doc 100 -- FOUND BY FORCING A DIVERGENT KEEPER SET, which is the realistic Sept-7 case.
    This script rewrote the BOARD and never touched ESPN_prerank_with_ids.csv. With keepers
    identical to the predictions that is invisible; with two keepers different, the prerank still
    contained the newly-kept players and was MISSING the two who came back onto the board -- and
    step 4 of draft_night.bat would then have pushed that list to ESPN. board_audit catches it
    ('prerank skill order matches board rank'); this fixes it.

    Skill rows are rebuilt from the new board, in board order. The K / D-ST tail is carried over
    untouched -- keeper logic never touches it (directive 4.9)."""
    pre_path = os.path.join(HERE, 'live_draft', 'ESPN_prerank_with_ids.csv')
    if not os.path.exists(pre_path):
        print("  !! ESPN_prerank_with_ids.csv not found -- prerank NOT rebuilt."); return
    try:
        old = pd.read_csv(pre_path)
        b   = pd.read_csv(BOARD).sort_values('rank')
        tail = old[old.pos.isin(['K', 'D/ST'])].copy()
        skill = pd.DataFrame({
            'prerank': 0,
            'ESPN_ID': b.espn_id.astype('int64').values,
            'player':  b.player.values,
            'pos':     b.pos.values,
            'team_c':  b.team_c.values,
            'bye':     b.bye.values,
            'vbd':     b.vbd.values,
            'adp_pick':b.adp_pick.values,
            'flag':    b.flag.values if 'flag' in b.columns else None,
        })
        out = pd.concat([skill, tail[skill.columns]], ignore_index=True)
        out['prerank'] = range(1, len(out) + 1)
        out.to_csv(pre_path, index=False)
        print(f"  rebuilt prerank: {len(skill)} skill + {len(tail)} K/D-ST = {len(out)} rows")
    except Exception as e:
        print(f"  !! COULD NOT REBUILD THE PRERANK ({e}).")
        print(f"  !! ESPN would be sent a list that does not match the board. Do NOT inject.")


def reapply_news():
    """doc 101 -- REPRODUCED, not reasoned. This function rebuilds the board from the SPINE, so
    it silently reverts every news override: on 2026-08-31 a --write restored Josh Jacobs to
    rank 20 with his full projection, one hour before the draft, while printing "IDENTICAL to
    the current board." The board it compared against is not the board it wrote.

    So the swap now re-applies news_overrides.csv itself. If it cannot, it says so LOUDLY --
    a silent revert at 7:00 PM is exactly the failure this project keeps paying for."""
    try:
        import apply_news
    except Exception as e:
        print("\n  !! COULD NOT RE-APPLY NEWS OVERRIDES (%s)." % e)
        print("  !! The board has been rebuilt from the spine and any suspended or injured")
        print("  !! player is BACK AT FULL VALUE. Run:  py apply_news.py --write")
        return
    print("\n  re-applying news_overrides.csv on top of the rebuilt board...")
    try:
        apply_news.main(['--write'])
    except SystemExit as e:
        if e.code not in (0, None):
            print("  !! apply_news refused (%s). RUN IT YOURSELF before drafting." % e.code)
    except Exception as e:
        print("  !! apply_news FAILED (%s). RUN IT YOURSELF before drafting." % e)


def main():
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--check',action='store_true'); g.add_argument('--write',action='store_true')
    a=ap.parse_args()

    u=pd.read_csv(SPINE)
    MKT, mkt_name = _market_pull()
    e=pd.read_csv(ADP23); e.columns=[c.replace('﻿','') for c in e.columns]
    if MKT != ADP23:
        # refresh_adp.py wrote `new_adp = m.espn_adp.fillna(b.adp_pick)` -- it OVERWROTE the
        # board where the newer pull had a value and LEFT the old one where it did not. The
        # newer pull is smaller (it drops players ESPN has stopped listing), so coalescing in
        # that order is what reproduces the shipped board. Doing it any other way makes this
        # builder disagree with the file it is supposed to rebuild.
        n=pd.read_csv(MKT); n.columns=[c.replace('﻿','') for c in n.columns]
        fresh=n.set_index('espn_id').espn_adp
        e['espn_adp']=e.espn_id.map(fresh).combine_first(e.espn_adp)
        print(f"  market column (adp_pick): {mkt_name}, "
              f"{int(e.espn_id.isin(fresh.dropna().index).sum())} rows refreshed, "
              f"rest held at {os.path.basename(ADP23)}")
    else:
        print(f"  market column (adp_pick) from: {mkt_name}")
    k=pd.read_csv(KFILE)
    if 'Player' not in k.columns: sys.exit("actual_keepers.csv needs a 'Player' column")
    want=[str(x).strip() for x in k.Player.dropna()]
    if len(want)!=12: sys.exit(f"REFUSING: {len(want)} keepers listed; a locked draft has exactly 12.")
    if len(set(map(norm,want)))!=12: sys.exit("REFUSING: duplicate keeper names in the file.")

    sk=u[u.pos.isin(['QB','RB','WR','TE']) & u.proj_leaguepts.notna()].copy()
    sk['nk']=sk.player.map(norm)
    # doc 90: a K or D/ST keeper is no longer hypothetical. Matt's rule is that a manager who
    # misses the deadline must keep SOMETHING once the draft is paused -- and the rational
    # choice for them is their worst player, which can be a kicker or a defence. Those are not
    # on the skill spine, so the old code exited "matched 0 spine rows" and the 7:00 PM
    # sequence stopped dead. They need no board surgery: they were never ON board_v8_fixed.csv,
    # so removing them is a no-op. Recognise them, count them toward the 12, and carry on.
    allpos=u.copy(); allpos['nk']=allpos.player.map(norm)
    ids, nonskill = [], []
    for w in want:
        hit=sk[sk.nk==norm(w)]
        if len(hit)==1: ids.append(int(hit.espn_id.iloc[0])); continue
        other=allpos[(allpos.nk==norm(w)) & (~allpos.pos.isin(['QB','RB','WR','TE']))]
        if len(other)>=1:
            nonskill.append((w, other.pos.iloc[0], int(other.espn_id.iloc[0])))
            continue
        sugg=difflib.get_close_matches(w, sk.player.tolist(), n=3, cutoff=0.6)
        sys.exit(f"REFUSING: keeper '{w}' matched {len(hit)} spine rows. Closest names: {sugg}. "
                 f"Fix the name in actual_keepers.csv (copy it exactly from the suggestion).")
    if nonskill:
        print(f"  NOTE: {len(nonskill)} keeper(s) are K or D/ST and are not on the skill board:")
        for w,ps,_ in nonskill:
            print(f"     {w} ({ps}) -- nothing to remove; he was never on board_v8_fixed.csv")
        print("  They still count toward the 12. The board below is built from the rest.")
        prune_streamers(nonskill, a.write)
    kset=set(ids)

    adp=e.set_index('espn_id').espn_adp
    missing=[i for i in ids if i not in adp.index or pd.isna(adp[i])]
    if missing: sys.exit(f"REFUSING: no ADP in {mkt_name} for keeper espn_id(s) {missing}.")
    kadp=np.sort([float(adp[i]) for i in ids])

    pool=sk[~sk.espn_id.isin(kset)].copy()
    pool=pool.merge(e[['espn_id','espn_adp']],on='espn_id',how='left')
    if pool.espn_adp.isna().any():
        bad=pool[pool.espn_adp.isna()].player.tolist(); sys.exit(f"REFUSING: no ADP in {mkt_name} for {bad[:5]}")
    b=pd.DataFrame({
        'espn_id':pool.espn_id.astype(int),'player':pool.player,'pos':pool.pos,'team_c':pool.team_c,
        'bye':pool.bye,'proj_leaguepts':pool.proj_leaguepts,
        'vbd':pool.proj_leaguepts-pool.pos.map(derive_repl()),'adp_pick':pool.espn_adp.round(2)})
    b['gone_ahead']=b.adp_pick.map(lambda x:int((kadp<x).sum()))
    b['eff_pick']=(b.adp_pick-b.gone_ahead).round(2)
    b['flag']=pool.injury_status.where(pool.injury_status.ne('ACTIVE'))
    b['bye_clash_pickens']=np.where(b.bye==14.0,'YES',None)
    b=b.sort_values('vbd',ascending=False).reset_index(drop=True)
    b.insert(0,'rank',np.arange(1,len(b)+1))
    b=b[['rank','espn_id','player','pos','team_c','bye','proj_leaguepts','vbd','adp_pick',
         'gone_ahead','eff_pick','flag','bye_clash_pickens']]

    old=pd.read_csv(BOARD)
    gone_p=sorted(set(old.espn_id)-set(b.espn_id)); new_p=sorted(set(b.espn_id)-set(old.espn_id))
    nm=u.set_index('espn_id').player
    print(f"rebuilt board: {len(b)} rows (current board {len(old)})")
    print(f"  players REMOVED (newly kept): {[nm.get(i,i) for i in gone_p] or 'none'}")
    print(f"  players RE-ADDED (no longer kept): {[nm.get(i,i) for i in new_p] or 'none'}")
    m=old.merge(b,on='espn_id',suffixes=('_o','_n'))
    ch=int((m.eff_pick_o!=m.eff_pick_n).sum())
    print(f"  eff_pick changed on {ch} of {len(m)} shared rows")
    same=(len(old)==len(b)) and not gone_p and not new_p and ch==0
    if same: print("  IDENTICAL to the current board -- keepers match the build.")

    if a.write:
        os.makedirs(ARCH,exist_ok=True)
        dst=os.path.join(ARCH,f"board_v8_fixed_ARCHIVED_{dt.datetime.now():%Y%m%d_%H%M}.csv")
        shutil.copy2(BOARD,dst); b.to_csv(BOARD,index=False)
        by=os.path.getsize(BOARD); sha=hashlib.sha256(open(BOARD,'rb').read()).hexdigest()[:16]
        print(f"  archived old board -> {dst}")
        print(f"  WROTE {BOARD}: {by:,} bytes  sha {sha}")
        rebuild_prerank()
        reapply_news()
        print(f"  NOTE: check_kit.py will now flag the board as changed -- expected after keeper lock.")
        print(f"  Restart live_draft.py so it loads the new board.")
if __name__=='__main__': main()
