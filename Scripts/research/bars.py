"""The hidden variable made visible: for each position and week, the rate a NEW player must beat
to change the starting nine. gain = sum over weeks of max(0, his rate - the bar). That is the whole
calculation, and with this grid Matt can do it for anybody without me."""
import json, collections
exec(open('moves.py').read().split('# ---- every (add, drop) pair')[0]
     .replace("('Tyjae Spears','RB',9),", ""))
POS=['QB','RB','WR','TE','D/ST','K']
bar={}
for pos in POS:
    bar[pos]={}
    for w in range(1,15):
        lo,hi=0.0,45.0
        for _ in range(45):
            mid=(lo+hi)/2
            c=dict(name='X',pos=pos,tm='',bye=0,wk=mid)
            if week_points(roster+[c],w) > week_points(roster,w)+0.0005: hi=mid
            else: lo=mid
        bar[pos][w]=round(hi,1)
print(f"  {'pos':<6}" + "".join(f"{w:>6}" for w in range(1,15)))
for pos in POS:
    print(f"  {pos:<6}" + "".join(f"{bar[pos][w]:>6.1f}" for w in range(1,15)))
d=json.load(open('sheet.json')); d['bar']=bar
# per-candidate weekly arithmetic
for c in d['cands']:
    by=int(float(c['bye'])); r=c['market_wk']; pos=c['pos']
    wk={}
    for w in range(1,15):
        if w==by: wk[w]='bye'
        else:
            g=round(max(0.0, r-bar[pos][w]),1)
            wk[w]= g if g>0.049 else 0
    c['calc']=wk; c['calc_total']=round(sum(v for v in wk.values() if isinstance(v,(int,float))),2)
json.dump(d, open('sheet.json','w'), indent=1)
print()
for c in d['cands'][:8]:
    print(f"  {c['name']:<20}{c['market_wk']:>6.1f}  season {c['calc_total']:+6.2f}  (engine said {c['market_gain']:+6.2f})")
