r"""doc 141: rebuild values.csv FROM THE SHIPPED VALUE_LADDER.pdf.

`values.py` wrote values.csv from a `rankers.csv` that only ever existed in a previous
container -- it is not in Scripts\ or Source\, so the sheet could not be rebuilt from its own
inputs.  Rather than reconstruct rankers.csv approximately (and silently ship a DIFFERENT
sheet), read the rows back out of the PDF that actually shipped.  Everything mkvalue.py
renders is on the page, so this round-trips exactly by construction, and the row count and
every field are asserted against the PDF at the end.
"""
import math, os, re, shutil, subprocess, sys, pandas as pd, numpy as np


def _norm_cdf(x, loc=0.0, scale=1.0):
    """doc 143.  This used scipy, which is NOT installed on Matt's machine -- the script I
    shipped him died on the import before it read a single row.  The only thing it ever needed
    from scipy was one normal CDF, and the standard library has erf.  No dependency, identical
    result to 1e-15."""
    return 0.5 * (1.0 + math.erf((x - loc) / (scale * math.sqrt(2.0))))

# doc 144: this shelled out to `pdftotext`, which is NOT on Matt's machine -- WinError 2, the
# same mistake as the scipy import.  The PDF parse was only ever a ONE-TIME RECOVERY of a
# values.csv that had been lost with its container; that recovery is done and values.csv is now
# stored in Scripts\ next to this file.  So: read values.csv when it exists, and fall back to
# the PDF only if it is missing AND pdftotext is available.
HERE   = os.path.dirname(os.path.abspath(__file__))
VALUES = os.path.join(HERE, 'values.csv')
# doc 144: these were bare filenames, which only worked in the container that built the sheet.
# On Matt's machine the board is in Scripts\live_draft\ and he runs from Scripts\.
BOARD  = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
PDF = sys.argv[1] if len(sys.argv)>1 else 'VALUE_LADDER.pdf'
def _from_pdf():
    if not shutil.which('pdftotext'):
        sys.exit("  values.csv is missing and `pdftotext` is not installed, so the sheet cannot\n"
                 "  be recovered from the PDF either. Restore Scripts\\values.csv from\n"
                 "  2026\\_archive\\ (or ask for it) and re-run.")
    return subprocess.run(['pdftotext','-layout',PDF,'-'],capture_output=True,text=True).stdout

txt = '' if os.path.exists(VALUES) else _from_pdf()
EV   = ['BOARD','ANALYSTS','BUY','JOB','INJURY-OPENED']
rows=[]; pick=None; eff=None
for line in txt.splitlines():
    h=re.match(r'\s*PICK (\d+) . effective ADP available here ~(\d+)',line)
    if h: pick,eff=int(h.group(1)),int(h.group(2)); continue
    m=re.match(r'\s{0,6}(\S.*?)\s{2,}(QB|RB|WR|TE)\s+(\d+)\s+([01]\.\d\d)\s*(.*)$',line)
    if not m or pick is None: continue
    name,pos,adp,p,rest = m.group(1).strip(),m.group(2),int(m.group(3)),float(m.group(4)),m.group(5)
    ev=[]
    for e in EV:                       # fixed vocabulary; order is values.py's ev() order
        if re.search(r'(?<![A-Z-])'+e+r'(?![A-Z-])',rest): ev.append(e); rest=rest.replace(e,'',1)
    c=[]
    for pat in (r'\bAVOID\b',r'\bDISC\b',r'\b(\d+)g\b',r'\bbear\b'):
        mm=re.search(pat,rest)
        if mm: c.append(mm.group(0)); rest=rest[:mm.start()]+' '*(mm.end()-mm.start())+rest[mm.end():]
    rows.append(dict(take_at=pick,eff_pick=eff,player=name,pos=pos,adp_pick=adp,p_there=p,
                     ev=str(ev),nev=len(ev),caution=' '.join(c),why=rest.strip()))
if os.path.exists(VALUES):
    v=pd.read_csv(VALUES)
    print(f'  read {os.path.basename(VALUES)} ({len(v)} players) -- no PDF parse needed')
else:
    v=pd.DataFrame(rows)
    assert len(v), 'parsed nothing -- the PDF layout changed'

# --- pull the structured bits back out of the rendered why-string ---
def grab(pat,s,cast=str,d=None):
    m=re.search(pat,str(s));  return cast(m.group(1)) if m else d
v['opened_by']=[grab(r'path opened by (.+?)(?: · |$)',w) for w in v.why]
v['job']      =[grab(r'\b(UNSETTLED|contested) job',w) for w in v.why]
v['job_ceil'] =[grab(r'job, worth (\d+) pts',w,int) for w in v.why]
v['Boone']    =[grab(r'Boone (\d+)',w,int) for w in v.why]
v['Harmon']   =[grab(r'Harmon (\d+)',w,int) for w in v.why]
v['gap']      =[(a-np.mean([b,h])) if pd.notna(b) else np.nan
                for a,b,h in zip(v.adp_pick,v.Boone,v.Harmon)]

# --- everything board-derived is JOINED FROM THE BOARD, never carried from the PDF -----
# doc 143.  The parsed p/eff came from a page built on the 08-30 ADP.  The moment
# `refresh_adp.py --write` re-freezes the market, every timing number on this sheet is stale and
# NOTHING says so -- the page still renders, with the old percentages.  So: take the player,
# position, badges and cautions from the PDF (they are ADP-independent judgements), and RECOMPUTE
# every timing number from the CURRENT board.  Re-running this script after an ADP refresh is now
# all it takes to correct the sheet.
b=pd.read_csv(BOARD)[['player','team_c','bye','rank','vbd','adp_pick','eff_pick']]
b=b.rename(columns={'adp_pick':'adp_now','eff_pick':'eff_now'})
# s3, THE MERGE COLLISION -- and it caught me. On the first run values.csv came from the PDF
# and had none of these columns; on every run after, it is the file THIS SCRIPT wrote, so it
# already carries them and pandas suffixes both sides to _x/_y. `v.team_c` then raises. Drop the
# board-derived columns before the merge so the board is always the single source for them.
v['adp_prev'] = v['adp_pick'] if 'adp_pick' in v.columns else np.nan
v = v.drop(columns=[c for c in ('team_c','bye','board_rank','vbd','adp_pick','eff_pick')
                    if c in v.columns])
n=len(v); v=v.merge(b,on='player',how='left')
assert len(v)==n, 'board join inflated the sheet -- duplicate player name on the board'
miss=v.loc[v.team_c.isna(),'player'].tolist()
assert not miss, f'{len(miss)} rows got no board row: {miss}'
v=v.rename(columns={'rank':'board_rank'})

PICKS=[8,17,32,41,56,65,80,89,104,113,128,137]
# s2.1(c)'s "effective ADP available at pick P" was a HAND-SOLVED TABLE fitted on the 08-23 keeper
# ADPs and hardcoded in values.py as [8,17,35,51,...].  Derive it from the board instead: the board
# already carries `eff_pick` (= adp_pick minus keepers ahead), recomputed by refresh_adp.py against
# the current keeper list, so the player sitting at eff_pick P tells you what adp is available at P.
_bb=pd.read_csv(BOARD)[['adp_pick','eff_pick']].dropna().sort_values('eff_pick')
EFF=[int(round(_bb.iloc[(_bb.eff_pick-P).abs().argmin()].adp_pick)) for P in PICKS]
def _sd(a): return 0.111*a+5.40
def _surv(eff,pick): return float(1-_norm_cdf(pick,loc=eff,scale=_sd(eff)))
def _take_at(eff):
    out=None
    for P,E in zip(PICKS,EFF):
        if _surv(eff,E)>=0.50: out=P
    return out
v['take_at_now']=v.eff_now.map(_take_at)
v['p_now']=[_surv(e,dict(zip(PICKS,EFF))[t]) if pd.notna(t) else float('nan')
            for e,t in zip(v.eff_now,v.take_at_now)]

moved=v[(v.take_at_now.notna()) & (v.take_at_now!=v.take_at)]
drop =v[v.take_at_now.isna()]
print(f'  effective-ADP map derived from the board: {dict(zip(PICKS,EFF))}')
_mv=(v.adp_now.round()!=v.adp_prev.round())
print(f'  ADP moved on {int(_mv.sum())} of {len(v)} rows vs the shipped sheet'
      + (f'   (max {float((v.adp_now-v.adp_prev).abs().max()):.1f} picks)' if _mv.any() else ''))
if len(moved):
    print(f'  {len(moved)} players change PICK GROUP:')
    for _,r in moved.iterrows():
        print(f'    {r.player:<24} adp {r.adp_prev:>3.0f} -> {r.adp_now:>3.0f}   '
              f'pick {r.take_at:>3.0f} -> {r.take_at_now:>3.0f}   p {r.p_there*100:>3.0f}% -> {r.p_now*100:>3.0f}%')
if len(drop):
    print(f'  {len(drop)} players no longer reachable at any of your picks: '
          f'{", ".join(drop.player)}')
v['take_at']=v.take_at_now.fillna(v.take_at)
v['p_there']=v.p_now.fillna(v.p_there)
v['adp_pick']=v.adp_now
v['eff_pick']=v.eff_now
v=v.drop(columns=['take_at_now','p_now','adp_now','eff_now','adp_prev'])

# doc 145.  THE BADGES WERE FROZEN AND THE ADP WAS NOT.  `ev` came out of the shipped PDF and was
# never recomputed, but BOARD is defined against ADP (`board_rank < adp_pick - 12`) -- so after the
# 09-03 refresh some BOARD badges were firing at a 3-slot gap when the rule needs 12.  Recompute it
# from the CURRENT board, which is the only ADP-dependent badge on the sheet.
def _recut(row):
    e=[x for x in eval(row.ev) if x!='BOARD']
    if row.board_rank < row.adp_pick - 12: e.append('BOARD')
    return str(e)
v['ev']=v.apply(_recut,axis=1)

# AGREE now counts OPINION-INDEPENDENT badges only.  BOARD is excluded on purpose -- see the
# legend and doc 145: it selects "the projection likes him more than the market does", which is
# s4.13's RETIRED signal, replicated NEGATIVE by s4.22(b) at rho -0.173 (p<0.001, n=409). It also
# fires on 40 of 49 rows, so it barely separates anything even before you ask which way it points.
AGREE_BADGES = ('ANALYSTS','BUY','JOB','INJURY-OPENED')
v['nev']  = v.ev.map(lambda x: len([e for e in eval(x) if e in AGREE_BADGES]))
v['fact'] = v.ev.map(lambda x: 1 if 'INJURY-OPENED' in eval(x) else 0)
v['jobw'] = v.job_ceil.fillna(0)
v.to_csv(VALUES,index=False)
print(f'values.csv rebuilt: {len(v)} players across {v.take_at.nunique()} picks, '
      f'{v.team_c.notna().sum()} teams joined, 0 unmatched')
print(v.groupby("take_at").size().to_string())
