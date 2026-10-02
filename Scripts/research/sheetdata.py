#!/usr/bin/env python3
"""Builds one JSON for the weekly sheet: the roster, the week grid, the candidate table with BOTH
market value and measured potential, the bye-cover plan, and the defence marriage."""
import json, csv, collections, statistics as st, numpy as np
exec(open('moves.py').read().split('# ---- every (add, drop) pair')[0]
     .replace("('Tyjae Spears','RB',9),", ""))

owned = {r['player']: float(r['owned_pct'])
         for r in csv.DictReader(open('/mnt/user-data/uploads/2026/Source/WIRE_20260910.csv',
                                      encoding='utf-8-sig'))}
SLOTNAMES = ['QB','RB','RB','WR','WR','TE','FLEX','D/ST','K']

def lineup(players, w):
    avail=collections.defaultdict(list)
    for p in players:
        if p['bye']!=w: avail[p['pos']].append(p)
    for k in avail: avail[k].sort(key=lambda x:-x['wk'])
    used=collections.Counter(); slots=[]
    for label in ['QB','RB','RB','WR','WR','TE']:
        pool=avail.get(label,[]); i=used[label]
        slots.append((label, pool[i]['name'] if i<len(pool) else None,
                      pool[i]['wk'] if i<len(pool) else 0.0)); used[label]+=1
    bestp=None
    for pos in ('RB','WR','TE'):
        pool=avail.get(pos,[]); i=used[pos]
        if i<len(pool) and (bestp is None or pool[i]['wk']>bestp['wk']): bestp=pool[i]
    slots.append(('FLEX', bestp['name'] if bestp else None, bestp['wk'] if bestp else 0.0))
    for label in ['D/ST','K']:
        pool=avail.get(label,[]); i=used[label]
        slots.append((label, pool[i]['name'] if i<len(pool) else None,
                      pool[i]['wk'] if i<len(pool) else 0.0)); used[label]+=1
    return slots

weeks=[]
for w in range(1,15):
    sl=lineup(roster,w)
    weeks.append(dict(week=w, total=round(sum(x[2] for x in sl),1),
                      off=[p['name'] for p in roster if p['bye']==w],
                      empty=[lab for lab,nm,_ in sl if nm is None],
                      slots=[[lab, nm or '', round(v,1)] for lab,nm,v in sl]))

def gain(cand):
    return round(season(roster+[cand])-base, 2)
def gain_weeks(cand):
    return {w: round(week_points(roster+[cand],w)-week_points(roster,w),1)
            for w in range(1,15) if week_points(roster+[cand],w)-week_points(roster,w) > 0.05}

D3=np.load('/home/claude/dst/dist_3of3.npy'); DR=np.load('/home/claude/dst/dist_rook1.npy')
def potential(cand, dist):
    g=[season(roster+[dict(cand, wk=float(x))])-base for x in dist]
    return round(float(np.mean(g)),2), round(float(np.percentile(g,90)),1), round(float((np.array(g)>0.5).mean()),3)

PICK = [
 ('Brenton Strange','TE','JAX',None), ('Pat Freiermuth','TE','PIT',None),
 ('Dalton Schultz','TE','HOU',None),  ('Gunnar Helm','TE','TEN',None),
 ('Chris Boswell','K','PIT',None),    ('Trey Smack','K','GB',None),
 ('Will Reichard','K','MIN',None),
 ('Daniel Jones','QB','IND',None),    ('Baker Mayfield','QB','TB',None),
 ('Omar Cooper Jr.','WR','NYJ','rook'), ('Ricky Pearsall','WR','SF','3of3'),
 ('Pat Bryant','WR','DEN','3of3'),    ('Jalen McMillan','WR','TB','3of3'),
 ('Tre Tucker','WR','LV',None),       ('Jerry Jeudy','WR','CLE',None),
 ('Tank Dell','WR','HOU',None),
 ('Samaje Perine','RB','CIN',None),   ('Brian Robinson Jr.','RB','ATL',None),
 ('Tyjae Spears','RB','TEN',None),
]
byname={f['name']: f for f in free}
cands=[]
for nm,pos,tm,screen in PICK:
    f=byname.get(nm)
    if not f: print("  MISSING from the priced pool:", nm); continue
    c=dict(name=nm,pos=pos,tm=f['tm'],bye=f['bye'],wk=f['wk'])
    row=dict(name=nm,pos=pos,tm=f['tm'],bye=f['bye'],
             market_wk=round(f['wk'],2), owned=owned.get(nm),
             market_gain=gain(c), weeks=gain_weeks(c), screen=screen)
    if screen:
        m,p90,pnz = potential(c, DR if screen=='rook' else D3)
        row.update(pot_gain=m, pot_p90=p90, pot_hit=pnz)
    cands.append(row)

# ---- the defence marriage --------------------------------------------------------------------
gen={r['offence']:float(r['dst_pts_allowed_per_game']) for r in csv.DictReader(open('/home/claude/dst/generosity_2025.csv',encoding='utf-8'))}
mean=st.mean(gen.values()); shr={t: mean+0.325*(v-mean) for t,v in gen.items()}
ownd=collections.defaultdict(list)
for r in csv.DictReader(open('/home/claude/dst/dst_weekly_2025.csv',encoding='utf-8')): ownd[r['team']].append(float(r['dst_pts']))
ownm={t:st.mean(v) for t,v in ownd.items()}; dmean=st.mean(ownm.values())
dshr={t: 0.269*(v-dmean) for t,v in ownm.items()}
sched=collections.defaultdict(dict)
for g in csv.DictReader(open('/home/claude/dst/sched_2026.csv',encoding='utf-8')):
    sched[g['home_team']][int(g['week'])]=g['away_team']; sched[g['away_team']][int(g['week'])]=g['home_team']
def wv(t,w):
    o=sched[t].get(w); return None if o is None else round(shr[o]+dshr[t],2)
PARTNERS=['CHI','BUF','SF','KC','CAR','DAL','IND']
dst={'CLE':{w:wv('CLE',w) for w in range(2,18)},
     'opp':{t:{w:sched[t].get(w) for w in range(2,18)} for t in ['CLE']+PARTNERS}}
for t in PARTNERS: dst[t]={w:wv(t,w) for w in range(2,18)}
tot={}
for t in PARTNERS:
    for lab,rng in (('w2_14',range(2,15)),('w9_14',range(9,15)),('w15_17',range(15,18))):
        solo=sum(x for x in (wv('CLE',w) for w in rng) if x is not None)
        pair=sum(max([x for x in (wv('CLE',w), wv(t,w)) if x is not None] or [0]) for w in rng)
        tot.setdefault(t,{})[lab]=round(pair-solo,2)
json.dump(dict(roster=[{k:(round(v,2) if isinstance(v,float) else v) for k,v in p.items()} for p in roster],
               base=round(base,1), weeks=weeks, cands=cands,
               dst=dst, dst_gain=tot, partners=PARTNERS), open('sheet.json','w'), indent=1)
print(f"  roster {len(roster)}  weeks {len(weeks)}  candidates {len(cands)}  partners {len(PARTNERS)}")
print("  empty slots:", [(w['week'],w['empty']) for w in weeks if w['empty']])
for c in cands:
    if c.get('pot_gain') is not None:
        print(f"    {c['name']:<20} market {c['market_gain']:+6.2f}   potential {c['pot_gain']:+6.2f}  p90 {c['pot_p90']:+5.1f}")
print("  defence pair gains:", {t:tot[t]['w9_14'] for t in PARTNERS})
