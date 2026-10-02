"""
code_live_engine.py -- deterministic pick engine for the live draft.
E-Discovery Keeper League 2026 | Matt Mays (JUG) | slot 8.

RULE (tested, doc 54): score every legal candidate by its MARGINAL starting-lineup
value, minus the marginal value of the best player at that position expected to survive
to my next pick. No hand-set positional penalty -- roster state is priced through the
lineup, which is what the objective actually is.

    Delta(p) = MV(p | roster)  -  E[ MV(best at pos(p) surviving to my next pick) ]
    pick     = argmax Delta

Constants come from the project directive and doc 53.
"""
import os
import numpy as np, pandas as pd

# doc 60: AFFINE noise, refit on all 5 seasons (n=680), weighted RMSE 0.89 picks per band
# against 2.65 for doc 16's fit and 3.06 for the capped-proportional form doc 53 recommended.
#   observed (sorted) sd = 0.1391 x ADP + 6.75   ->  generative sd = 0.111 x ADP + 5.40
# A pure proportional form cannot be right: it goes to ZERO dispersion at the top of the board,
# where the observed sd is 7.5 picks. The floor term is the whole point. This also reconciles
# doc 16's independent fit (0.1255 x rank + 5.31, n=271, this league only) -- two different
# datasets converge on nearly the same line, which is the strongest calibration result here.
K_NOISE   = 0.111     # slope
K_FLOOR   = 5.40      # intercept, in picks
ADP_CAP   = 1e9       # retired: no cap needed once the model has a floor
TE_SHIFT  = 15.0      # directive 4.12 -- league takes TEs ~15 picks later than ADP
GP_PROJ   = 15.32     # doc 42
WEEKS     = list(range(1, 15))
NEED      = {'QB':1, 'RB':2, 'WR':2, 'TE':1}
CAPS      = {'QB':2, 'RB':6, 'WR':6, 'TE':2}
FLEX      = ('RB','WR','TE')
REPL      = {'QB':341.603, 'RB':168.589, 'WR':163.540, 'TE':140.295}
# V5 (doc 57): these are the levels board_v7_2026.csv's own vbd column was built on,
# recovered as proj_leaguepts - vbd. Directive 4.1's 341.7/168.0/168.5/137.7 came from a
# 200-row v2 export and is stale -- WR was 5.0 points too high.
WAIVER    = 0.80
PC        = {'QB':0,'RB':1,'WR':2,'TE':3}
MY_PICKS  = [8,17,32,41,56,65,80,89,104,113,128,137]   # skill picks; 152 D/ST, 161 K
DST_PICK, K_PICK = 152, 161

def snake_picks(slot, teams=12, rounds=14):
    """Overall pick numbers for one slot in a snake draft. Used for mocks, which have
    different sizes and orders than the real league."""
    out=[]
    for r in range(rounds):
        out.append(r*teams + (slot if r%2==0 else teams-slot+1))
    return out

def configure(slot, teams, rounds, dst_round=None, k_round=None):
    """Re-point the module at a different draft shape (an ESPN mock, say)."""
    global MY_PICKS, DST_PICK, K_PICK
    allp = snake_picks(slot, teams, rounds)
    d = allp[dst_round-1] if dst_round and dst_round<=len(allp) else None
    k = allp[k_round-1]   if k_round   and k_round  <=len(allp) else None
    DST_PICK, K_PICK = d, k
    MY_PICKS = [p for p in allp if p not in (d,k)]
    return MY_PICKS

def _lineup_np(pc, pg, bye, repl):
    """THE ORIGINAL. Kept verbatim as the reference the fast path is tested against --
    doc 139. Not called in production; `py -m pytest` has no home here, so the equivalence
    check lives in `bench_lineup.py` and must be re-run if either version is touched."""
    pc=np.asarray(pc); pg=np.asarray(pg,float); bye=np.asarray(bye,float)
    need=[1,2,2,1]; tot=0.0
    for w in WEEKS:
        live=bye!=w; used=~live
        for p in range(4):
            m=live&(pc==p)&~used
            v=np.sort(pg[m])[::-1]; k=need[p]; take=v[:k]
            tot+=take.sum()+repl[p]*(k-len(take))
            if len(take):
                used[np.where(m&(pg>=take[-1]))[0][:k]]=True
        m=live&~used&np.isin(pc,[1,2,3])
        tot+=pg[m].max() if m.any() else max(repl[1],repl[2],repl[3])
    return tot


_NEED = (1, 2, 2, 1)


def _lineup(pc, pg, bye, repl):
    """weeks 1-14 starting-lineup total, byes handled, bench used as the fill.

    doc 139 -- PURE PYTHON ON PURPOSE, and this is a performance fix, not a logic change.
    A roster is 15-16 players; every numpy call in here operated on a 16-element array, where
    the call overhead is 50-100x the arithmetic. This function is the hot spot of the whole
    tool: one on-clock recommendation calls it ~13,000 times through rollout_scores, and it
    was taking 16 SECONDS on Matt's pick. That is why the board lagged the room and the mock
    clock advanced two picks between refreshes -- the poll interval was never the bottleneck.

    Semantics are identical to `_lineup_np` above, deliberately including the tie-break
    detail: the players marked used are the FIRST k in index order whose points clear the
    lowest taken value, which is what np.where(...)[:k] did. bench_lineup.py checks the two
    agree EXACTLY (not approximately) over thousands of real rosters."""
    try:
        pc = pc.tolist(); pg = pg.tolist(); bye = bye.tolist()
    except AttributeError:
        pc = list(pc); pg = list(pg); bye = list(bye)
    n = len(pc)
    rng_n = range(n)
    r0, r1, r2, r3 = repl[0], repl[1], repl[2], repl[3]
    flexrepl = r1
    if r2 > flexrepl: flexrepl = r2
    if r3 > flexrepl: flexrepl = r3
    tot = 0.0
    for w in WEEKS:
        used = [b == w for b in bye]          # start: only the bye-week players are unusable
        for p in range(4):
            k = _NEED[p]
            m = [i for i in rng_n if pc[i] == p and not used[i]]
            if not m:
                tot += repl[p] * k
                continue
            take = sorted((pg[i] for i in m), reverse=True)[:k]
            s = 0.0
            for v in take: s += v
            tot += s + repl[p] * (k - len(take))
            thr = take[-1]; c = 0
            for i in m:                        # ascending, exactly np.where's order
                if pg[i] >= thr:
                    used[i] = True; c += 1
                    if c == k: break
        best = None
        for i in rng_n:
            q = pc[i]
            if not used[i] and (q == 1 or q == 2 or q == 3):
                v = pg[i]
                if best is None or v > best: best = v
        tot += flexrepl if best is None else best
    return tot


class Engine:
    def __init__(self, board_csv, ids_csv, keeper=('George Pickens','WR',198.68,14.0),
                 kdst_csv=None):
        b=pd.read_csv(board_csv)
        b=b[b.pos.isin(list(PC))].reset_index(drop=True)
        if 'espn_id' in b.columns and b.espn_id.notna().all():
            b['ESPN_ID']=b.espn_id.astype('int64')          # board carries its own id: no join
            assert b.ESPN_ID.is_unique, "duplicate espn_id on the board"
            ids=None
        else:
            ids=pd.read_csv(ids_csv)[['player','ESPN_ID']]
            assert ids.player.is_unique, "prerank has duplicate player names -- the id join is ambiguous"
            _n=len(b); b=b.merge(ids,on='player',how='left')
            # ERROR_PATTERNS C1: a name join must never fail silently. An unmatched row loses its
            # id, drops out of by_eid, and stays 'available' all night even after it is drafted.
            assert len(b)==_n, f"id join inflated the board {_n} -> {len(b)} (duplicate name in prerank)"
            _miss=b.loc[b.ESPN_ID.isna(),'player'].tolist()
            assert not _miss, (f"{len(_miss)} board rows have NO ESPN_ID and would stay 'available' "
                               f"for the whole draft: {_miss[:8]}")
            assert b.ESPN_ID.is_unique, "duplicate ESPN_ID on the board -- by_eid would orphan a row"
        self.b=b
        self.name=b.player.values; self.pos=b.pos.values
        self.proj=b.proj_leaguepts.values.astype(float)
        self.vbd=b.vbd.values.astype(float); self.bye=b.bye.values.astype(float)
        self.flag=b.flag.fillna('').values
        self.eid=b.ESPN_ID.values
        self.by_eid={int(e):i for i,e in enumerate(self.eid) if pd.notna(e)}
        adp=b.eff_pick.values.astype(float)
        self.adp=adp; self.adp_opp=adp+np.where(self.pos=='TE',TE_SHIFT,0.0)
        self.pg=self.proj/GP_PROJ
        self.repl={PC[p]:REPL[p]/GP_PROJ*WAIVER for p in REPL}
        self.keeper=keeper
        self.avail=np.ones(len(b),bool)
        self.mine=[]
        self.rng=np.random.default_rng(0)
        self._pm={p:(self.pos==p) for p in PC}
        # doc 59: this was board_csv.replace('board_v7_2026.csv','board_v7_kdst_separate.csv') --
        # a string substitution that silently NO-OPS for any other board filename. Passing
        # board_v8_fixed.csv loaded the SKILL board as the streamer list, so streamers('D/ST')
        # returned [] and picks 152/161 rendered an empty table. Resolve by directory instead,
        # and never swallow the failure: an empty streamer list at 152 costs a starting slot.
        kdst_csv = kdst_csv or os.path.join(os.path.dirname(os.path.abspath(board_csv)),
                                            'board_v7_kdst_separate.csv')
        kd=pd.read_csv(kdst_csv)
        assert set(kd.pos.unique()) <= {'K','D/ST'}, (
            f"{kdst_csv} is not a streamer list -- it holds {sorted(set(kd.pos.unique()))[:5]}")
        # doc 80: this merge used to run UNCONDITIONALLY. Once the streamer file gained its
        # own ESPN_ID column (Aug 29) the merge collided into ESPN_ID_x / ESPN_ID_y, the
        # `'ESPN_ID' in k` test in streamers() went False, and the already-drafted filter
        # stopped running -- a filter that HAD been working via this name join (measured
        # 64/64 matched, 0 disagreements). The Aug-29 "fix" was the regression.
        # Prefer the file's own id (identity rule, s3); name-join only as a legacy fallback.
        if 'ESPN_ID' not in kd.columns:
            kd=kd.merge(pd.read_csv(ids_csv)[['player','ESPN_ID']],on='player',how='left')
        if 'ESPN_ID' not in kd.columns or kd.ESPN_ID.isna().any():
            n=int(kd.ESPN_ID.isna().sum()) if 'ESPN_ID' in kd.columns else len(kd)
            raise SystemExit(
                f"{kdst_csv}: {n} streamer row(s) carry no ESPN_ID. Picks 152/161 would "
                f"recommend already-drafted players with no error. Rebuild the file with ids.")
        # D/ST block ahead of K (pick 152 comes before 161), best-first WITHIN each position
        self.kdst=pd.concat([kd[kd.pos=='D/ST'].sort_values('proj_leaguepts',ascending=False),
                             kd[kd.pos=='K'   ].sort_values('proj_leaguepts',ascending=False)],
                            ignore_index=True)
        for p in ('D/ST','K'):
            assert (self.kdst.pos==p).sum()>=12, f"only {(self.kdst.pos==p).sum()} {p} loaded"

    def streamers(self, pos, taken_ids, n=6):
        """D/ST and K are streamed (§4.8); at picks 152/161 just take the best one left."""
        k=self.kdst
        if not len(k): return []
        k=k[(k.pos==pos)]
        # doc 80: was `if 'ESPN_ID' in k:` -- a silent skip. The one thing this method must
        # do is drop players already off the board; not doing it is never acceptable.
        assert 'ESPN_ID' in k.columns, ("streamer frame lost its ESPN_ID column -- the "
                                        "already-drafted filter cannot run")
        k=k[~k.ESPN_ID.isin([int(x) for x in taken_ids if pd.notna(x)])]
        return [dict(player=r.player, pos=r.pos, team=r.team_c, bye=float(r.bye),
                     proj=round(float(r.proj_leaguepts),1)) for r in k.head(n).itertuples()]

    # ---------------- state ----------------
    def set_taken(self, espn_ids, my_ids):
        self.avail[:]=True
        for e in espn_ids:
            i=self.by_eid.get(int(e))
            if i is not None: self.avail[i]=False
        self.mine=[self.by_eid[int(e)] for e in my_ids if int(e) in self.by_eid]

    @property
    def counts(self):
        c={}
        for i in self.mine: c[self.pos[i]]=c.get(self.pos[i],0)+1
        return c

    def legal(self, picks_left):
        c=self.counts
        ok={p for p in CAPS if c.get(p,0)<CAPS[p]}
        need=[p for p in ('QB','TE') if c.get(p,0)==0]
        if need and picks_left<=len(need): return set(need)
        return ok

    def _cache(self, roster):
        """base arrays for a roster + the keeper, as numpy; one slot left spare"""
        n=len(roster)
        pc=np.empty(n+2,np.int64); pg=np.empty(n+2); by=np.empty(n+2)
        for k,i in enumerate(roster):
            pc[k]=PC[self.pos[i]]; pg[k]=self.pg[i]; by[k]=self.bye[i]
        pc[n]=PC[self.keeper[1]]; pg[n]=self.keeper[2]/GP_PROJ; by[n]=self.keeper[3]
        return pc,pg,by,n+1

    def lv_from(self, cache, extra=None):
        pc,pg,by,m = cache
        if extra is None:
            return _lineup(pc[:m],pg[:m],by[:m],self.repl)
        pc[m]=PC[self.pos[extra]]; pg[m]=self.pg[extra]; by[m]=self.bye[extra]
        return _lineup(pc[:m+1],pg[:m+1],by[:m+1],self.repl)

    def lv(self, extra=None):
        return self.lv_from(self._cache(self.mine), extra)

    # ---------------- survival ----------------
    def survival(self, pick_no, target_pick, reps=400):
        self.rng = self._seed(pick_no)
        """p(each player is still on the board when pick `target_pick` comes up)."""
        gap=target_pick-pick_no
        if gap<=0: return np.ones(len(self.b))
        a=self.adp_opp; out=np.zeros(len(self.b))
        for _ in range(reps):
            pref=np.where(self.avail, a+self.rng.normal(0,(K_NOISE*a + K_FLOOR)), np.inf)
            gone=np.argsort(pref)[:gap-1]
            m=self.avail.copy(); m[gone]=False
            out+=m
        return out/reps

    # ---------------- the rule ----------------
    def _seed(self, pick_no):
        """Deterministic per-state seed: the same board state must always give the same
        recommendation. A single long-lived RNG made successive polls disagree with each
        other (doc 58) -- the board flickered between candidates while Matt watched it."""
        return np.random.default_rng(int(pick_no)*100003 + int((~self.avail).sum())*7919
                                     + len(self.mine))

    def recommend(self, pick_no, top=9, reps=20, rollout_inner=10):
        self.rng = self._seed(pick_no)
        picks_left=sum(1 for p in MY_PICKS if p>=pick_no)
        nxt=next((p for p in MY_PICKS if p>pick_no), None)
        allowed=self.legal(picks_left)
        idx=np.where(self.avail & np.isin(self.pos,list(allowed)))[0]
        if not len(idx): idx=np.where(self.avail)[0]
        idx=idx[np.argsort(-self.vbd[idx])][:top]
        cache=self._cache(self.mine)
        base=self.lv_from(cache)
        mv=np.array([self.lv_from(cache,c)-base for c in idx])
        fut={p:0.0 for p in PC}
        if nxt is not None:
            gap=nxt-pick_no; a=self.adp_opp
            for _ in range(reps):
                pref=np.where(self.avail, a+self.rng.normal(0,(K_NOISE*a + K_FLOOR)), np.inf)
                gone=np.argsort(pref)[:max(gap-1,0)]
                m=self.avail.copy(); m[gone]=False
                for p in fut:
                    s=np.where(m&(self.pos==p))[0]
                    if not len(s): continue
                    s=s[np.argsort(-self.vbd[s])][:4]
                    fut[p]+=max(self.lv_from(cache,x)-base for x in s)
            fut={p:v/reps for p,v in fut.items()}
        surv=self.survival(pick_no, nxt) if nxt else np.ones(len(self.b))
        rows=[]
        for j,i in enumerate(idx):
            p=self.pos[i]
            rows.append(dict(i=int(i), player=self.name[i], pos=p, team=self.b.team_c[i],
                             bye=float(self.bye[i]), vbd=round(float(self.vbd[i]),1),
                             adp=round(float(self.adp[i]),1), flag=self.flag[i],
                             mv=round(float(mv[j]),1),
                             hold=round(float(fut[p]),1),
                             delta=round(float(mv[j]-fut[p]),1),
                             p_next=round(float(surv[i]),2)))
        # RANK BY ROLLOUT (the rule that won the head-to-head); mv/hold/delta stay for the why
        roll=self.rollout_scores(pick_no, idx, inner=rollout_inner)
        best=float(roll.max())
        for j,r in enumerate(rows):
            r['roll']=round(float(roll[j]),1)
            r['cost']=round(float(roll[j]-best),1)     # 0 = the pick; negative = what it costs
        rows.sort(key=lambda r:(-r['roll'], -r['delta']))
        return rows

    # ---------------- ROLLOUT: the tested decision rule (doc 54) ----------------
    def _finish(self, avail, mine, counts, gaps, prank, cand_k=4):
        r=list(mine); c=dict(counts); av=avail.copy(); n=len(gaps)
        for k,g in gaps:
            av2=av&(prank>g)
            ok={p for p in CAPS if c.get(p,0)<CAPS[p]}
            miss=[p for p in ('QB','TE') if c.get(p,0)==0]
            if miss and (n-k)<=len(miss): ok=set(miss)
            idx=np.where(av2&self.posmask(ok))[0]
            if not len(idx):
                idx=np.where(av2)[0]
                if not len(idx): break
            idx=idx[np.argsort(-self.vbd[idx])][:cand_k]   # V6: VBD, never raw points
            cache=self._cache(r)
            best=idx[int(np.argmax([self.lv_from(cache,x) for x in idx]))]
            r.append(best); c[self.pos[best]]=c.get(self.pos[best],0)+1; av[best]=False
        return self.lv_from(self._cache(r))

    def posmask(self, allowed):
        m=np.zeros(len(self.b),bool)
        for p in allowed: m |= self._pm[p]
        return m

    def rollout_scores(self, pick_no, idx, inner=20):
        """expected FINAL starting-lineup value if I take each candidate now and then
        draft greedily against fresh realisations of the opponent model."""
        future=[p for p in MY_PICKS if p>pick_no]
        if not future:
            base=self.lv(); return np.array([self.lv(c)-base for c in idx])
        gaps=[(k,(p-pick_no)-(k+1)) for k,p in enumerate(future)]
        sc=np.zeros(len(idx)); a=self.adp_opp; c0=self.counts
        for _ in range(inner):
            pref=np.where(self.avail, a+self.rng.normal(0,(K_NOISE*a + K_FLOOR)), np.inf)
            pr=np.empty(len(self.b)); pr[np.argsort(pref)]=np.arange(len(self.b))
            for j,c in enumerate(idx):
                av=self.avail.copy(); av[c]=False
                cc=dict(c0); cc[self.pos[c]]=cc.get(self.pos[c],0)+1
                sc[j]+=self._finish(av,list(self.mine)+[c],cc,gaps,pr)
        return sc/inner

    def cliffs(self, pick_no):
        self.rng = self._seed(pick_no)
        """positions whose best-available marginal value falls hardest before my next pick"""
        nxt=next((p for p in MY_PICKS if p>pick_no), None)
        if nxt is None: return []
        base=self.lv(); out=[]
        surv=self.survival(pick_no,nxt)
        for p in PC:
            s=np.where(self.avail&(self.pos==p))[0]
            if not len(s): continue
            s=s[np.argsort(-self.vbd[s])][:8]
            now=max(self.lv(x)-base for x in s)
            exp=sum((self.lv(x)-base)*surv[x] for x in s)/max(sum(surv[x] for x in s),1e-9)
            out.append(dict(pos=p, now=round(now,1), at_next=round(exp,1),
                            drop=round(now-exp,1)))
        out.sort(key=lambda r:-r['drop'])
        return out
