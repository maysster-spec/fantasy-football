#!/usr/bin/env python3
"""MATT'S CLAIM, STATED BEFORE TESTING (SECTION 0.5a2):
holding TWO D/STs and starting the better matchup each week beats holding one, by enough to pay
for the roster spot. POPULATION: all 32 defences on the 2026 schedule. BASELINE: the best SINGLE
defence over the same window. Weekly value = max(A,B) -- you start whichever is better."""
import csv, statistics as st, collections, itertools

gen={r['offence']:float(r['dst_pts_allowed_per_game']) for r in csv.DictReader(open('generosity_2025.csv',encoding='utf-8'))}
mean=st.mean(gen.values()); shr={t: mean+0.325*(v-mean) for t,v in gen.items()}
own=collections.defaultdict(list)
for r in csv.DictReader(open('dst_weekly_2025.csv',encoding='utf-8')): own[r['team']].append(float(r['dst_pts']))
ownm={t:st.mean(v) for t,v in own.items()}; dmean=st.mean(ownm.values())
dshr={t: 0.269*(v-dmean) for t,v in ownm.items()}
sched=collections.defaultdict(dict)
for g in csv.DictReader(open('sched_2026.csv',encoding='utf-8')):
    sched[g['home_team']][int(g['week'])]=g['away_team']; sched[g['away_team']][int(g['week'])]=g['home_team']
TEAMS=sorted(sched)

def wkval(t,w):
    o=sched[t].get(w)
    return None if o is None else shr[o]+dshr[t]      # BYE = None, not zero

def single(t,weeks):
    v=[wkval(t,w) for w in weeks]
    return sum(x for x in v if x is not None), sum(1 for x in v if x is None)

def pair(a,b,weeks):
    tot=0; blank=0
    for w in weeks:
        xs=[x for x in (wkval(a,w), wkval(b,w)) if x is not None]
        if xs: tot+=max(xs)
        else: blank+=1                                 # both on bye
    return tot, blank

for lab,weeks in (('weeks 2-14 (the rest of the regular season)', range(2,15)),
                  ('weeks 15-17 (the playoffs)', range(15,18))):
    n=len(list(weeks))
    sing=sorted(((single(t,weeks)[0], t) for t in TEAMS), reverse=True)
    best_s, best_t = sing[0]
    pairs=sorted(((pair(a,b,weeks)[0], a, b) for a,b in itertools.combinations(TEAMS,2)), reverse=True)
    best_p, pa, pb = pairs[0]
    # the pair you would actually build: best single + its best partner
    withbest=sorted(((pair(best_t,o,weeks)[0], o) for o in TEAMS if o!=best_t), reverse=True)
    print(f"\n  {lab}   ({n} weeks)")
    print(f"    best SINGLE            {best_t:<5}{best_s:>8.2f}   ({best_s/n:.2f} a week)")
    print(f"    best PAIR              {pa}+{pb:<5}{best_p:>7.2f}   ({best_p/n:.2f} a week)")
    print(f"    GAIN from the 2nd spot {'':<5}{best_p-best_s:>8.2f}   ({(best_p-best_s)/n:+.2f} a week)")
    print(f"    best partner FOR {best_t}: {withbest[0][1]} -> {withbest[0][0]:.2f} "
          f"({withbest[0][0]-best_s:+.2f} over {best_t} alone)")
    # and the honest counterweight: how much of the gain is just "two draws from the same urn"?
    med=st.median([p[0] for p in pairs])
    print(f"    median pair {med:.2f}  |  a RANDOM pair beats the best single by "
          f"{med-best_s:+.2f} — so {100*(best_p-med)/(best_p-best_s):.0f}% of the gain is CHOOSING the pair")
