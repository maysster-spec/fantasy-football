"""Full-league simulator with EMPIRICAL outcome variance.
Objective set: E[points], P(1st), P(top 6), E[payout]. Standings by H2H record and by points."""
import sys, numpy as np, pandas as pd, json, io
sys.path.insert(0,'/tmp/eng')
import engine
from engine import Sim, load, N_TEAMS, N_ROUNDS, TOTAL_PICKS, MY_SLOT, MY_SKILL_PICKS, GP_PROJ
import rules
from rules import RULES, PC

WEEKS=14; NW=WEEKS
OPP_WINDOW=8
PAYOUT={1:525,2:225,3:150,4:85,5:25,6:25}
NEED=np.array([1,2,2,1])
REPL={0:341.7,1:168.0,2:168.5,3:137.7}
REPL_PG={k:v/GP_PROJ*0.80 for k,v in REPL.items()}

KEEP=pd.read_csv(io.StringIO("""slot,player,pos,proj,bye
1,Rashee Rice,WR,222.78,5
8,George Pickens,WR,198.68,14
11,Chris Olave,WR,204.77,8
2,Javonte Williams,RB,240.78,14
6,Zay Flowers,WR,197.89,13
12,Tetairoa McMillan,WR,194.63,5
7,Cam Skattebo,RB,207.88,8
10,Colston Loveland,TE,165.81,10
5,Drake Maye,QB,373.09,11
9,Travis Etienne,RB,223.67,8
3,Rhamondre Stevenson,RB,181.48,11
4,Stefon Diggs,WR,128.44,7"""))

# --- empirical outcome pool: (form, games played), bootstrapped by ADP band ---
E=pd.read_csv('/tmp/var/decomposed.csv')
BANDS=[0,24,48,84,120,180,10**6]
def band_of(adp): return int(np.searchsorted(BANDS, adp, side='right')-1)
POOL={}
for b in range(len(BANDS)-1):
    lo,hi=BANDS[b],BANDS[b+1]
    s=E[(E.adp>lo)&(E.adp<=hi)]
    if len(s)<25: s=E[(E.adp>84)]                    # thin tail -> use the late pool
    POOL[b]=(s.form.values.astype(float), s.gp_a.values.astype(float))

ORDER=[]
for r in range(N_ROUNDS):
    ORDER += list(range(1,N_TEAMS+1) if r%2==0 else range(N_TEAMS,0,-1))

def draft(sim, rule, pref, rng, snyder):
    avail=np.ones(sim.n,bool); rosters={s:[] for s in range(1,N_TEAMS+1)}
    counts={s:{} for s in range(1,N_TEAMS+1)}; allen=False; mine=[]
    for pk in range(1,TOTAL_PICKS+1):
        slot=ORDER[pk-1]
        if slot==MY_SLOT:
            left=sum(1 for p in MY_SKILL_PICKS if p>=pk)
            c=int(rule(sim,avail,mine,counts[slot],pk,left,rng)); mine.append(c)
        else:
            if slot==9 and snyder and not allen and sim.allen>=0 and avail[sim.allen]:
                c=sim.allen
            else:
                left=sum(1 for q in range(pk,TOTAL_PICKS+1) if ORDER[q-1]==slot)
                m=avail & np.isin(sim.pos,list(Sim.opp_legal(counts[slot],left)))
                if not m.any(): m=avail
                cand=np.argsort(np.where(m,pref,np.inf))[:OPP_WINDOW]
                cand=[x for x in cand if m[x]]
                c=int(cand[int(np.argmax(sim.vbd[cand]))]) if cand else int(np.argmin(np.where(m,pref,np.inf)))
        counts[slot][sim.pos[c]]=counts[slot].get(sim.pos[c],0)+1
        rosters[slot].append(c); avail[c]=False
        if c==sim.allen: allen=True
    return rosters

def realise(sim, rosters, rng):
    """per-team weekly starting-lineup points, weeks 1-14, with empirical outcome draws"""
    pts=np.zeros((N_TEAMS,NW))
    for slot in range(1,N_TEAMS+1):
        idx=rosters[slot]
        pc=[PC[sim.pos[i]] for i in idx]; pg0=[sim.proj[i]/GP_PROJ for i in idx]
        by=[sim.bye[i] for i in idx]; adp=[sim.adp_opp[i] for i in idx]
        k=KEEP[KEEP.slot==slot]
        if len(k):
            r=k.iloc[0]; pc.append(PC[r.pos]); pg0.append(r.proj/GP_PROJ); by.append(float(r.bye)); adp.append(30.0)
        n=len(pc); pc=np.array(pc); pg0=np.array(pg0); by=np.array(by)
        form=np.empty(n); gpv=np.empty(n)
        for j,a in enumerate(adp):
            f,g=POOL[band_of(a)]
            t=rng.integers(0,len(f)); form[j]=f[t]; gpv[j]=g[t]
        pg=pg0*form
        # which of the 17 weeks he plays; take the weeks 1-14 slice
        live=np.zeros((n,NW),bool)
        for j in range(n):
            wk=rng.permutation(17)[:int(round(gpv[j]))]
            live[j]=np.isin(np.arange(1,NW+1), wk+1)
            live[j] &= (np.arange(1,NW+1)!=by[j])
        for w in range(NW):
            lv=live[:,w]; used=~lv; s=0.0
            order=np.argsort(-pg)
            for p in range(4):
                kk=NEED[p]; c=0
                for i in order:
                    if c==kk: break
                    if lv[i] and not used[i] and pc[i]==p: s+=pg[i]; used[i]=True; c+=1
                s+=REPL_PG[p]*(kk-c)
            got=False
            for i in order:
                if lv[i] and not used[i] and pc[i] in (1,2,3): s+=pg[i]; got=True; break
            if not got: s+=max(REPL_PG[1],REPL_PG[2],REPL_PG[3])
            pts[slot-1,w]=s
    return pts

def standings(pts, rng):
    tot=pts.sum(1)
    wins=np.zeros(N_TEAMS)
    for w in range(NW):
        opp=rng.permutation(N_TEAMS)
        for a in range(0,N_TEAMS,2):
            i,j=opp[a],opp[a+1]
            if pts[i,w]>pts[j,w]: wins[i]+=1
            else: wins[j]+=1
    key=wins*10000+tot                      # record first, points as tiebreak
    rank_h2h=N_TEAMS-np.argsort(np.argsort(key))
    rank_pts=N_TEAMS-np.argsort(np.argsort(tot))
    return tot, rank_h2h, rank_pts
