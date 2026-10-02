"""Competing pick-selection rules. Identical signature; all share the paired opponent noise."""
import numpy as np
from engine import K_NOISE, ADP_CAP, MY_SKILL_PICKS
from fastscore import lineup_value_approx

START_NEED = dict(QB=1, RB=2, WR=2, TE=1)
MY_CAPS    = dict(QB=2, RB=6, WR=6, TE=2)
PC = {'QB':0,'RB':1,'WR':2,'TE':3}

def my_legal(counts, remaining):
    ok = {p for p in MY_CAPS if counts.get(p,0) < MY_CAPS[p]}
    need = [p for p in ('QB','TE') if counts.get(p,0)==0]
    if need and remaining <= len(need): return set(need)
    return ok

def _cand(sim, avail, counts, my_left):
    idx = np.where(avail & np.isin(sim.pos, list(my_legal(counts,my_left))))[0]
    return idx if len(idx) else np.where(avail)[0]

def _arrays(sim, roster, extra=None):
    r = list(roster) + ([extra] if extra is not None else [])
    pc  = [PC[sim.pos[i]] for i in r] + [PC['WR']]
    pg  = [sim.pg[i] for i in r] + [sim.keeper_pg]
    bye = [sim.bye[i] for i in r] + [14.0]
    return pc, pg, bye

def _lv(sim, roster, extra=None):
    pc,pg,bye = _arrays(sim, roster, extra)
    return lineup_value_approx(pc,pg,bye,sim.repl_i)

# R1 -------------------------------------------------- static VBD, unconstrained
def r_static_vbd(sim, avail, roster, counts, pk, left, rng):
    i = np.where(avail)[0]; return i[np.argmax(sim.vbd[i])]

# R2 -------------------------------------------------- static VBD + roster caps
def r_static_legal(sim, avail, roster, counts, pk, left, rng):
    i = _cand(sim, avail, counts, left); return i[np.argmax(sim.vbd[i])]

# R3 -------------------------------------------------- VONA (one-step lookahead)
def r_vona(sim, avail, roster, counts, pk, left, rng, reps=20):
    nxt = next((p for p in MY_SKILL_PICKS if p > pk), None)
    i = _cand(sim, avail, counts, left)
    if nxt is None: return i[np.argmax(sim.proj[i])]
    gap = nxt - pk
    base = {p:0.0 for p in PC}
    a = sim.adp_opp
    for _ in range(reps):
        pref = np.where(avail, a + rng.normal(0,K_NOISE*np.minimum(a,ADP_CAP)), np.inf)
        gone = np.argsort(pref)[:max(gap-1,0)]
        m = avail.copy(); m[gone] = False
        for p in base:
            s = np.where(m & (sim.pos==p))[0]
            base[p] += sim.proj[s].max() if len(s) else 0.0
    v = sim.proj[i] - np.array([base[sim.pos[j]]/reps for j in i])
    return i[np.argmax(v)]

# R4 -------------------------------------------------- need-penalty heuristic
def r_need_penalty(sim, avail, roster, counts, pk, left, rng):
    i = _cand(sim, avail, counts, left)
    f = np.array([1.0 if counts.get(sim.pos[j],0) < START_NEED[sim.pos[j]]
                  else (0.5 if counts.get(sim.pos[j],0)==START_NEED[sim.pos[j]] else 0.25) for j in i])
    return i[np.argmax(sim.vbd[i]*f)]

# R5 -------------------------------------------------- marginal starter (myopic)
def r_marginal(sim, avail, roster, counts, pk, left, rng, top=12):
    i = _cand(sim, avail, counts, left)
    i = i[np.argsort(-sim.vbd[i])][:top]      # V6: shortlist by VBD; the RULE is still myopic
    base = _lv(sim, roster)
    return i[int(np.argmax([_lv(sim, roster, c)-base for c in i]))]

# R6 -------------------------------------------------- rollout (full lookahead)
def _finish(sim, avail, roster, counts, gaps, prank, cand_k=5):
    r=list(roster); c=dict(counts); av=avail.copy()
    n=len(gaps)
    for k,g in gaps:
        av2 = av & (prank > g)
        idx = np.where(av2 & np.isin(sim.pos, list(my_legal(c, n-k))))[0]
        if not len(idx):
            idx = np.where(av2)[0]
            if not len(idx): break
        idx = idx[np.argsort(-sim.vbd[idx])][:cand_k]   # V6: VBD, never raw points
        base=_lv(sim,r)
        best = idx[int(np.argmax([_lv(sim,r,x)-base for x in idx]))]
        r.append(best); c[sim.pos[best]]=c.get(sim.pos[best],0)+1; av[best]=False
    return _lv(sim,r)

def r_rollout(sim, avail, roster, counts, pk, left, rng, top=6, inner=4):
    future=[p for p in MY_SKILL_PICKS if p>pk]
    i=_cand(sim, avail, counts, left)
    i=i[np.argsort(-sim.vbd[i])][:top]
    if not future:
        base=_lv(sim,roster); return i[int(np.argmax([_lv(sim,roster,c)-base for c in i]))]
    gaps=[(k,(p-pk)-(k+1)) for k,p in enumerate(future)]
    sc=np.zeros(len(i)); a=sim.adp_opp
    for _ in range(inner):
        pref=np.where(avail, a+rng.normal(0,K_NOISE*np.minimum(a,ADP_CAP)), np.inf)
        pr=np.empty(sim.n); pr[np.argsort(pref)]=np.arange(sim.n)
        for j,c in enumerate(i):
            av=avail.copy(); av[c]=False
            cc=dict(counts); cc[sim.pos[c]]=cc.get(sim.pos[c],0)+1
            sc[j]+=_finish(sim,av,list(roster)+[c],cc,gaps,pr)
    return i[int(np.argmax(sc))]

# R0 ------------------------------------------------- follow ADP (naive floor)
def r_adp(sim, avail, roster, counts, pk, left, rng):
    i=_cand(sim,avail,counts,left); return i[np.argmin(sim.adp_opp[i])]

RULES={'R0 follow ADP':r_adp,
       'R1 static VBD (no caps)':r_static_vbd,
       'R2 static VBD + caps':r_static_legal,
       'R3 VONA 1-step':r_vona,
       'R4 need-penalty':r_need_penalty,
       'R5 marginal starter':r_marginal,
       'R6 rollout':r_rollout}

# R7 -------------------------------------------------- VONA on MARGINAL value (proposal)
def r_vona_marginal(sim, avail, roster, counts, pk, left, rng, reps=16, top=14):
    """Delta(p) = marginal starting-lineup value of p now
                  - E[marginal value of the best player at p's position at my NEXT pick].
    VONA's baseline, but measured in lineup points rather than raw projection, so roster
    state and the FLEX are priced automatically and no hand-set need penalty is required."""
    nxt = next((p for p in MY_SKILL_PICKS if p > pk), None)
    i = _cand(sim, avail, counts, left)
    base = _lv(sim, roster)
    i = i[np.argsort(-sim.vbd[i])][:top]
    mv = np.array([_lv(sim, roster, c) - base for c in i])
    if nxt is None:
        return i[int(np.argmax(mv))]
    gap = nxt - pk
    fut = {p: 0.0 for p in PC}
    a = sim.adp_opp
    for _ in range(reps):
        pref = np.where(avail, a + rng.normal(0, K_NOISE*a), np.inf)
        gone = np.argsort(pref)[:max(gap-1, 0)]
        m = avail.copy(); m[gone] = False
        for p in fut:
            s = np.where(m & (sim.pos == p))[0]
            if not len(s):
                continue
            s = s[np.argsort(-sim.vbd[s])][:4]
            fut[p] += max(_lv(sim, roster, x) - base for x in s)
    d = mv - np.array([fut[sim.pos[j]]/reps for j in i])
    return i[int(np.argmax(d))]

RULES['R7 VONA on marginal (proposal)'] = r_vona_marginal

def r_rollout_strong(sim, avail, roster, counts, pk, left, rng):
    return r_rollout(sim, avail, roster, counts, pk, left, rng, top=9, inner=10)
RULES['R6b rollout (deeper)']=r_rollout_strong

# ---- V6 REGRESSION HARNESS: the pre-fix inner shortlist, kept only to measure the defect ----
def _finish_buggy(sim, avail, roster, counts, gaps, prank, cand_k=4):
    r=list(roster); c=dict(counts); av=avail.copy(); n=len(gaps)
    for k,g in gaps:
        av2 = av & (prank > g)
        idx = np.where(av2 & np.isin(sim.pos, list(my_legal(c, n-k))))[0]
        if not len(idx):
            idx = np.where(av2)[0]
            if not len(idx): break
        idx = idx[np.argsort(-sim.proj[idx])][:cand_k]        # <-- the defect
        base=_lv(sim,r)
        best = idx[int(np.argmax([_lv(sim,r,x)-base for x in idx]))]
        r.append(best); c[sim.pos[best]]=c.get(sim.pos[best],0)+1; av[best]=False
    return _lv(sim,r)

def r_rollout_buggy(sim, avail, roster, counts, pk, left, rng, top=6, inner=4):
    future=[p for p in MY_SKILL_PICKS if p>pk]
    i=_cand(sim, avail, counts, left); i=i[np.argsort(-sim.vbd[i])][:top]
    if not future:
        base=_lv(sim,roster); return i[int(np.argmax([_lv(sim,roster,c)-base for c in i]))]
    gaps=[(k,(p-pk)-(k+1)) for k,p in enumerate(future)]
    sc=np.zeros(len(i)); a=sim.adp_opp
    for _ in range(inner):
        pref=np.where(avail, a+rng.normal(0,K_NOISE*np.minimum(a,ADP_CAP)), np.inf)
        pr=np.empty(sim.n); pr[np.argsort(pref)]=np.arange(sim.n)
        for j,c in enumerate(i):
            av=avail.copy(); av[c]=False
            cc=dict(counts); cc[sim.pos[c]]=cc.get(sim.pos[c],0)+1
            sc[j]+=_finish_buggy(sim,av,list(roster)+[c],cc,gaps,pr)
    return i[int(np.argmax(sc))]
RULES['R6-buggy rollout (pre-V6-fix)']=r_rollout_buggy
