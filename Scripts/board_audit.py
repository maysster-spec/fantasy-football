#!/usr/bin/env python3
r"""
board_audit.py -- does the board say the RIGHT things, and does the engine DO the right
things with them? check_kit.py proves the files are the files. This proves the numbers.

    py board_audit.py

Every check re-derives a value from source and compares. Nothing is taken on trust.
Read-only. Exit 0 = every check passed.
"""
import os, sys, glob
import numpy as np, pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
KIT   = os.path.join(HERE, 'live_draft')
SRC   = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
KDST  = os.path.join(KIT, 'board_v7_kdst_separate.csv')
PRE   = os.path.join(KIT, 'ESPN_prerank_with_ids.csv')
SPINE = os.path.join(SRC, 'code_universe_v5.csv')
# doc 109: the frozen vintage is no longer hard-coded. `refresh_adp.py` stamps which pull the
# board's adp_pick came from, so re-freezing the market on Sept 5 does not turn this check into a
# guaranteed failure -- a gate that always fails is a gate you learn to ignore.
_VSTAMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_draft', 'adp_vintage.txt')
_VINTAGE = (open(_VSTAMP, encoding='utf-8').read().strip()
            if os.path.exists(_VSTAMP) else 'espn_projections_2026_20260823.csv')
ADP   = os.path.join(SRC, _VINTAGE)                        # the pull adp_pick is frozen to
KEEP  = os.path.join(HERE, 'actual_keepers.csv')
OVR   = os.path.join(HERE, 'news_overrides.csv')
REPL  = {'QB':341.603,'RB':168.589,'WR':163.540,'TE':140.295}

R=[]
def chk(name, ok, detail=''):
    R.append((name, bool(ok), detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"   {detail}" if detail else ''))
    return ok

def main():
    print("="*74); print("  BOARD AUDIT -- are the NUMBERS right?"); print("="*74)
    for f in (BOARD, KDST, PRE, SPINE, ADP, KEEP):
        if not os.path.exists(f): sys.exit(f"  missing: {f}")
    b   = pd.read_csv(BOARD)
    kd  = pd.read_csv(KDST)
    pre = pd.read_csv(PRE)
    u   = pd.read_csv(SPINE)
    e   = pd.read_csv(ADP); e.columns=[c.replace('﻿','') for c in e.columns]
    kp  = pd.read_csv(KEEP)

    print("\n--- THE BOARD ---")
    chk("board has 480 rows", len(b)==480, f"{len(b)}")
    chk("espn_id unique", b.espn_id.is_unique)
    chk("only QB/RB/WR/TE", set(b.pos)<= {'QB','RB','WR','TE'}, str(sorted(set(b.pos))))
    dec=['rank','espn_id','player','pos','bye','proj_leaguepts','vbd','adp_pick','eff_pick']
    chk("no blanks in decision columns", not b[dec].isna().any().any(),
        str(b[dec].isna().sum()[lambda x:x>0].to_dict() or 'none'))
    chk("bye weeks plausible (1-18)", b.bye.between(1,18).all())

    # Replacement, re-derived from the pull at FULL precision. The directive quotes these
    # to 3 decimals; the board used the unrounded values. Comparing against the rounded
    # constants makes a correct board look wrong by 4e-04 -- which is what happened the
    # first time this audit ran. Derive, then compare.
    # VBD was built from the 08-23 projections and refresh_adp.py does not touch VBD, so the
    # replacement levels are always checked against that pull, whatever the ADP vintage is now.
    pf = pd.read_csv(os.path.join(SRC, 'espn_projections_2026_20260823.csv'), usecols=['pos','proj_2026'])
    EXACT = {}
    for pos, n in (('RB',30),('WR',30),('QB',12),('TE',12)):
        col = pf[(pf.pos==pos)&pf.proj_2026.notna()].proj_2026.sort_values(ascending=False)
        EXACT[pos] = float(col.iloc[n-1])
    chk("replacement levels reproduce from the pull",
        all(abs(EXACT[p]-REPL[p]) < 0.001 for p in REPL),
        ' · '.join(f"{p}{ {'RB':30,'WR':30,'QB':12,'TE':12}[p] }={EXACT[p]:.6f}" for p in ('RB','WR','QB','TE')))

    want = b.proj_leaguepts - b.pos.map(EXACT)
    chk("VBD = projection - replacement, every row", np.allclose(b.vbd, want, atol=1e-6),
        f"max diff {abs(b.vbd-want).max():.2e} (full precision)")

    # A VBD tie means rank order between those rows is arbitrary. TWO sources are expected
    # and harmless: the four replacement players themselves sit at exactly 0.0 by definition,
    # and every zero-projection body sits at -(replacement) for its position. Anything else
    # would be two real players the board cannot separate -- that is what to look for.
    tied = b[b.vbd.round(6).duplicated(keep=False)]
    inrange = tied[tied['rank'] <= 161]
    # inside the drafted region the ONLY acceptable tie is the four replacement players,
    # who sit at exactly 0.0 because that is what replacement means.
    bad_ties = inrange[inrange.vbd.round(6) != 0.0]
    zeroproj = int((tied.proj_leaguepts.round(6) == 0.0).sum())
    chk("no VBD ties that could misorder a real pick", len(bad_ties) == 0,
        f"{len(tied)} tied rows total: 4 are the replacement players at exactly 0.0, "
        f"{zeroproj} are zero-projection bodies, {len(tied)-4-zeroproj} are real ties "
        f"but all sit outside the top 161"
        if len(bad_ties) == 0 else str(bad_ties[['rank','player','pos','vbd']].values.tolist()))

    # rank must be VBD descending with no gaps
    chk("rank is 1..N with no gaps", list(b['rank'])==list(range(1,len(b)+1)))
    chk("rank orders by VBD descending", b.sort_values('rank').vbd.is_monotonic_decreasing)

    # projections must equal the spine's, not a re-derivation
    m = b.merge(u[['espn_id','proj_leaguepts']], on='espn_id', how='left', suffixes=('','_spine'))
    # doc 97: news_overrides.csv deliberately breaks this equality for suspended/out players.
    # Exclude them here, then assert the override IS present -- so a Sept-5 rebuild that wipes
    # the edit fails LOUDLY instead of silently restoring a +72 VBD ghost at pick 32.
    ov = pd.read_csv(OVR) if os.path.exists(OVR) else pd.DataFrame(columns=['espn_id','player','action'])
    ovid = set(ov.espn_id.astype(int)) if len(ov) else set()
    if ovid:
        m = m[~m.espn_id.astype(int).isin(ovid)]
    chk("projections match the spine exactly", np.allclose(m.proj_leaguepts, m.proj_leaguepts_spine, atol=1e-6),
        f"max diff {abs(m.proj_leaguepts-m.proj_leaguepts_spine).max():.2e}")

    print("\n--- KEEPER DEPLETION (the thing that is easy to get subtly wrong) ---")
    import re as _re
    def norm(s):
        s=_re.sub(r'\s+(Jr\.|Sr\.|II|III|IV|V)$','',str(s).strip(),flags=_re.I)
        return _re.sub(r"[.'’-]",'',s).lower()
    sk=u[u.pos.isin(['QB','RB','WR','TE'])&u.proj_leaguepts.notna()].copy(); sk['nk']=sk.player.map(norm)
    kids=[int(sk[sk.nk==norm(p)].espn_id.iloc[0]) for p in kp.Player if len(sk[sk.nk==norm(p)])==1]
    for _, r in (ov.iterrows() if len(ov) else []):
        eid, act = int(r.espn_id), str(r.action)
        row = b[b.espn_id.astype('Int64')==eid]
        if act == 'remove':
            chk(f"news override applied: {r.player} is off the board", len(row)==0)
        else:
            chk(f"news override applied: {r.player} projection zeroed",
                len(row)==1 and abs(float(row.proj_leaguepts.iloc[0]))<1e-9,
                ('' if (len(row)==1 and abs(float(row.proj_leaguepts.iloc[0]))<1e-9) else
                 (f"proj is still {float(row.proj_leaguepts.iloc[0]):.1f} -- RE-RUN  py apply_news.py --write"
                  if len(row)==1 else 'not on the board at all')))
            if len(row)==1:
                chk(f"news override applied: {r.player} is below every real player",
                    int(row['rank'].iloc[0]) > 400, f"rank {int(row['rank'].iloc[0])} of {len(b)}")

    chk("all 12 keepers resolve in the spine", len(kids)==12, f"{len(kids)}/12")
    chk("no keeper is on the board", not set(kids)&set(b.espn_id.astype(int)))
    adp = e.set_index('espn_id').espn_adp
    kadp = np.sort([float(adp[i]) for i in kids])
    ga = b.adp_pick.map(lambda x:int((kadp<x).sum()))
    chk("gone_ahead = keepers with a lower ADP", (b.gone_ahead==ga).all(),
        f"{int((b.gone_ahead!=ga).sum())} rows differ")
    chk("eff_pick = adp_pick - gone_ahead",
        np.allclose(b.eff_pick, (b.adp_pick-b.gone_ahead).round(2), atol=0.011))
    chk(f"adp_pick matches its stamped vintage ({_VINTAGE[-12:-4]})",
        np.allclose(b.merge(e[['espn_id','espn_adp']],on='espn_id').adp_pick,
                    b.merge(e[['espn_id','espn_adp']],on='espn_id').espn_adp.round(2), atol=0.011))

    print("\n--- STREAMERS AND THE PRERANK ---")
    chk("streamer file is only K and D/ST", set(kd.pos)=={'K','D/ST'}, str(sorted(set(kd.pos))))
    chk("32 of each", (kd.pos=='D/ST').sum()==32 and (kd.pos=='K').sum()==32)
    chk("streamers carry ESPN_ID", 'ESPN_ID' in kd.columns and kd.ESPN_ID.notna().all())
    chk("prerank = board + streamers, exactly",
        set(pre.ESPN_ID)==set(b.espn_id)|set(kd.ESPN_ID), f"{len(pre)} rows")
    kdst_pos = pre[pre.pos.isin(['K','D/ST'])].prerank.min()
    chk("no K or D/ST in the prerank top 250", kdst_pos>250, f"first one at #{kdst_pos}")
    chk("prerank skill order matches board rank",
        [int(x) for x in pre[~pre.pos.isin(['K','D/ST'])].sort_values('prerank').ESPN_ID]
        == [int(x) for x in b.sort_values('rank').espn_id])

    print("\n--- THE ENGINE ---")
    sys.path.insert(0, KIT)
    import code_live_engine as CLE
    eng = CLE.Engine(BOARD, PRE)
    chk("engine indexes every board row by id", len(eng.by_eid)==len(b))
    chk("caps are QB2/RB6/WR6/TE2", CLE.CAPS=={'QB':2,'RB':6,'WR':6,'TE':2}, str(CLE.CAPS))
    chk("MY_PICKS = the 12 skill picks",
        CLE.MY_PICKS==[8,17,32,41,56,65,80,89,104,113,128,137], str(CLE.MY_PICKS))
    chk("D/ST at 152, K at 161", (CLE.DST_PICK,CLE.K_PICK)==(152,161))

    # legal(): must force QB/TE ONLY at zero, and only when picks are running out
    eng.mine=[]
    chk("with no QB/TE and 2 picks left, only QB+TE are legal", eng.legal(2)=={'QB','TE'})
    chk("with no QB/TE and 5 picks left, everything is legal", eng.legal(5)==set(CLE.CAPS))
    qb_i=[i for i in range(len(b)) if eng.pos[i]=='QB'][0]
    te_i=[i for i in range(len(b)) if eng.pos[i]=='TE'][0]
    eng.mine=[qb_i,te_i]
    chk("one QB + one TE held -> no forced pick", eng.legal(1)==set(CLE.CAPS))
    eng.mine=[qb_i]*2
    chk("two QBs held -> QB no longer legal", 'QB' not in eng.legal(9))
    eng.mine=[]

    # set_taken must actually remove players
    ids=[int(x) for x in b.espn_id.head(5)]
    eng.set_taken(ids, [])
    chk("set_taken marks players unavailable", not any(eng.avail[eng.by_eid[i]] for i in ids))
    eng.set_taken([], [])
    chk("set_taken resets", eng.avail.all())

    # recommend(): the contract the render depends on
    recs = eng.recommend(8, rollout_inner=6, top=6)
    chk("recommend returns rows", len(recs)>0, f"{len(recs)}")
    if recs:
        chk("rows sorted by roll descending",
            all(recs[i]['roll']>=recs[i+1]['roll'] for i in range(len(recs)-1)))
        chk("cost is 0 for row 1 and <=0 below",
            recs[0]['cost']==0 and all(r['cost']<=0 for r in recs))
        chk("every recommended player is available",
            all(eng.avail[eng.by_eid[int(b[b.player==r['player']].espn_id.iloc[0])]] for r in recs))
        chk("p(next) is a probability", all(0.0<=r['p_next']<=1.0 for r in recs))

    print("\n" + "="*74)
    bad=[n for n,ok,_ in R if not ok]
    print(f"  {len(R)-len(bad)} of {len(R)} checks passed")
    if bad:
        print("  FAILED:"); [print(f"     - {n}") for n in bad]
        print("\n  DO NOT DRAFT ON THIS BOARD until these are explained.")
    else:
        print("  ALL PASS -- the board's arithmetic and the engine's rules both check out.")
    print("="*74)
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
