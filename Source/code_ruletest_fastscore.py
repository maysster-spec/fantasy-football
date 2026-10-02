import numpy as np
from engine import WEEKS, P_WEEK
NEED = np.array([1,2,2,1])          # QB RB WR TE
NW = len(WEEKS)                     # 14

def lineup_value_approx(pos_codes, pg, bye, repl):
    """14 x (best legal lineup), minus the bye-week cost of each starter.
    Exact when no two starters share a bye; a close upper bound otherwise.
    Fast surrogate used INSIDE the rollout only -- the objective uses score_mc."""
    pos_codes=np.asarray(pos_codes); pg=np.asarray(pg,float); bye=np.asarray(bye,float)
    starters=[]; bench_by_pos={p:[] for p in range(4)}
    for p in range(4):
        idx=np.where(pos_codes==p)[0]
        idx=idx[np.argsort(-pg[idx])]
        starters += list(idx[:NEED[p]])
        bench_by_pos[p]=list(idx[NEED[p]:])
    flexpool=[i for p in (1,2,3) for i in bench_by_pos[p]]
    if flexpool:
        f=max(flexpool,key=lambda i:pg[i]); starters.append(f)
        bench_by_pos[pos_codes[f]].remove(f)
        flex_next=[i for p in (1,2,3) for i in bench_by_pos[p]]
        flex_repl=max([pg[i] for i in flex_next],default=max(repl[1],repl[2],repl[3]))
        flex_idx=f
    else:
        flex_repl=max(repl[1],repl[2],repl[3]); flex_idx=None
    base=NW*sum(pg[i] for i in starters)
    if flex_idx is None: base+=NW*flex_repl
    pen=0.0
    for i in starters:
        b=bye[i]
        if not (1<=b<=NW): continue
        p=int(pos_codes[i])
        if i==flex_idx: fill=flex_repl
        else:
            fill=pg[bench_by_pos[p][0]] if bench_by_pos[p] else repl[p]
        pen += max(pg[i]-fill,0.0)
    return base-pen

def score_mc(pos_codes, pg, bye, repl, rng, reps=60):
    """the OBJECTIVE: expected starting-lineup pts wks 1-14 with per-week availability."""
    pos_codes=np.asarray(pos_codes); pg=np.asarray(pg,float); bye=np.asarray(bye,float)
    n=len(pg); order=np.argsort(-pg); tot=0.0
    for _ in range(reps):
        alive=rng.random((NW,n))<P_WEEK
        for wi,w in enumerate(WEEKS):
            live=alive[wi]&(bye!=w)
            used=np.zeros(n,bool); s=0.0
            for p in range(4):
                k=NEED[p]; c=0
                for i in order:
                    if c==k: break
                    if live[i] and not used[i] and pos_codes[i]==p:
                        s+=pg[i]; used[i]=True; c+=1
                s+=repl[p]*(k-c)
            got=False
            for i in order:
                if live[i] and not used[i] and pos_codes[i] in (1,2,3):
                    s+=pg[i]; got=True; break
            if not got: s+=max(repl[1],repl[2],repl[3])
            tot+=s
    return tot/reps
