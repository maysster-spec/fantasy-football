#!/usr/bin/env python3
r"""homer_bias.py -- doc 152. Generalises buf_bias.py from ONE team to every manager x every team.

Matt: "Beyond the Bills homers we already discussed, what about the other known teams in my
league? Herman Allen is a Commanders fan. Others like myself are Panthers homies."

METHOD, identical to buf_bias.py so the Bills number reproduces as a control:
  reach = preseason ADP - actual pick.  POSITIVE = took him EARLIER than the market.
  Preseason ADP only, from the sanctioned registry (SS1.1). True selections only, keepers
  excluded (SS4.7). A manager's own picks are the comparison group -- a manager who reaches on
  everybody is not a homer, he is just aggressive.

THE THING THAT WILL KILL MOST OF THIS, STATED BEFORE THE NUMBERS (SS4.21/SS4.24's lesson, three
times over): 12 managers x 32 teams is ~384 tests. At p<0.05 you expect ~19 hits BY CHANCE.
So the p-values below are reported WITH a Benjamini-Hochberg false-discovery correction, and a
raw p under 0.05 that does not survive it is noise wearing a number.
"""
import re, sys, warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from scipy import stats as st

S = '/mnt/user-data/uploads/2026/Source/'
SUF = r'\b(jr|sr|ii|iii|iv|v)\b'
NICK = {'joshua':'josh','mitchell':'mitch','christopher':'chris','nathaniel':'nate',
        'benjamin':'ben','michael':'mike','zachary':'zach','matthew':'matt'}
def norm(s):
    s = str(s).lower().replace('.',' ').replace("'",'').replace('-',' ')
    s = re.sub(SUF,'',s); s = re.sub(r'[^a-z ]','',s); p = s.split()
    if p: p[0] = NICK.get(p[0], p[0])
    return ''.join(p)

d = pd.read_csv(S+'draft_history_2021_2025.csv')
d = d[d.Keeper != True].copy()
d['k'] = d.Player.map(norm)
d['NFL'] = d.NFL.astype(str).str.upper().str.strip()
d['NFL'] = d.NFL.replace({'WSH':'WAS','JAC':'JAX','LVR':'LV','OAK':'LV','SD':'LAC','STL':'LA','LAR':'LA'})
adp = {}
for y in range(2021, 2026):
    a = pd.read_csv(S+f'adp_registry/preseason_adp_{y}.csv'); a['k'] = a.player.map(norm)
    adp[y] = dict(zip(a.k, a.adp))
d['adp'] = [adp.get(y,{}).get(k, np.nan) for y, k in zip(d.Year, d.k)]
d = d[d.adp.notna()]
print(f"  {len(d)} true selections 2021-2025 with a preseason ADP, {d.Manager.nunique()} managers, "
      f"{d.NFL.nunique()} NFL teams\n")

MIN_N = 4
rows = []
for mgr, g in d.groupby('Manager'):
    if len(g) < 20: continue
    for tm, tg in g.groupby('NFL'):
        if len(tg) < MIN_N: continue
        oth = g[g.NFL != tm]
        t, p = st.ttest_ind(tg.reach if False else (tg.adp-tg.Pick), (oth.adp-oth.Pick), equal_var=False)
        rows.append(dict(manager=mgr, team=tm, n=len(tg),
                         team_reach=(tg.adp-tg.Pick).mean(), other=(oth.adp-oth.Pick).mean(),
                         diff=(tg.adp-tg.Pick).mean()-(oth.adp-oth.Pick).mean(), p=p))
r = pd.DataFrame(rows).sort_values('diff', ascending=False)
# Benjamini-Hochberg
r = r.sort_values('p').reset_index(drop=True)
m = len(r); r['bh'] = r.p * m / (r.index+1)
r['bh'] = r.bh[::-1].cummin()[::-1].clip(upper=1.0)
r = r.sort_values('diff', ascending=False)

print(f"  {m} manager-team pairs with n>={MIN_N}. At p<0.05 you would expect {m*0.05:.0f} by chance.")
print(f"  Surviving a Benjamini-Hochberg correction: {int((r.bh<0.05).sum())}\n")
print(f"  {'manager':<24}{'tm':<5}{'n':>3} {'team reach':>11} {'his other':>10} {'diff':>8} {'p':>8} {'BH':>7}")
print('  '+'-'*78)
for _, x in r.head(12).iterrows():
    print(f"  {x.manager[:23]:<24}{x.team:<5}{int(x.n):>3} {x.team_reach:>11.1f} {x.other:>10.1f} "
          f"{x['diff']:>+8.1f} {x.p:>8.3f} {x.bh:>7.3f}{'  <-- survives' if x.bh<0.05 else ''}")

print("\n  ── THE THREE TEAMS MATT NAMED, whatever their rank above ──")
NAMED = {'BUF':'Snyder (the one already in SS5)', 'WAS':'herman allen', 'CAR':'Matt himself'}
for tm, who in NAMED.items():
    sub = r[r.team == tm]
    print(f"\n  {tm}  ({who})")
    if sub.empty:
        n_tot = int((d.NFL == tm).sum())
        print(f"    no manager drafted {MIN_N}+ {tm} players in five years "
              f"({n_tot} {tm} picks league-wide). Not testable.")
        continue
    for _, x in sub.sort_values('diff', ascending=False).iterrows():
        print(f"    {x.manager[:26]:<28}n={int(x.n):<3} reach {x.team_reach:+6.1f} vs his own "
              f"{x.other:+6.1f}  diff {x['diff']:+6.1f}  p={x.p:.3f}  BH={x.bh:.3f}")
r.to_csv('/home/claude/work/hb/homer_bias.csv', index=False)
print(f"\n  wrote homer_bias.csv ({m} rows)")
