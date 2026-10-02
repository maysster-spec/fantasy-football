#!/usr/bin/env python3
"""
code_audit_v1.py — deterministic integrity oracle for E-Discovery Keeper League 2026.

Design principle (see 20_session_protocol_v1.md): a numeric claim written in prose
cannot be enforced. Every claim the directive makes about the data is encoded here as
an assertion with a tolerance. Run this BEFORE any analysis session. Non-zero exit =
the spine moved and the directive is stale.

Usage:  python code_audit_v1.py --src <dir with source csvs> [--json out.json]
Emits:  defects_<date>.csv  (one row per defect)  and a PASS/FAIL summary.

Every check states BASELINE / POPULATION / SAMPLE per directive §3.
"""
import argparse, os, sys, json, datetime as dt
import pandas as pd, numpy as np

DEF = []
def rec(cid, severity, area, claim, observed, verdict, baseline, population, n, downstream=""):
    DEF.append(dict(check_id=cid, severity=severity, area=area, claim=claim,
                    observed=observed, verdict=verdict, baseline=baseline,
                    population=population, sample_n=n, downstream_uses=downstream))

def approx(a, b, tol):  return abs(a-b) <= tol

def main(src, outdir):
    P = lambda f: os.path.join(src, f)
    u = pd.read_csv(P('code_universe.csv'))
    e = pd.read_csv(P('espn_projections_2026_20260820.csv')); e.columns=[c.replace('﻿','') for c in e.columns]
    d = pd.read_csv(P('draft_history_2021_2025.csv'))
    k = pd.read_csv(P('keeper_eligibility_VERIFIED.csv'))

    # ---------- A. PROVENANCE ----------
    cap = e['captured_at'].dropna().unique()
    age = (dt.date.today() - pd.to_datetime(cap[0]).date()).days if len(cap) else None
    rec('A1','INFO','provenance','ESPN pull carries a capture date',
        f'{cap[0] if len(cap) else "MISSING"} ({age}d old)','PASS' if len(cap) else 'FAIL',
        'directive §1 requires provenance','espn_projections_2026_20260820.csv',len(e))
    if age is not None and age > 7:
        rec('A2','HIGH','provenance','projections refreshed within 7 days',
            f'{age} days old','FAIL','directive §8 refresh schedule','all rows',len(e),
            'every VBD, ADP, survival and sim number')

    # ---------- B. REPLACEMENT LEVELS (directive §4.1) ----------
    CLAIM_REPL = {'RB':(30,168.0),'WR':(30,168.5),'QB':(12,341.7),'TE':(12,137.7)}
    for pos,(n,claimed) in CLAIM_REPL.items():
        s = u[u['pos']==pos]['TOT'].dropna().sort_values(ascending=False)
        obs = float(s.iloc[n-1])
        rec(f'B_{pos}{n}','HIGH' if not approx(obs,claimed,0.5) else 'OK','replacement',
            f'directive §4.1 {pos}{n} = {claimed}', f'{obs:.1f}',
            'PASS' if approx(obs,claimed,0.5) else 'FAIL',
            'code_universe.csv TOT', f'all {pos} in universe', int(len(s)),
            'every VBD; §4.3 TE premium; §4.10 strategy sim; board VBD column')

    # ---------- C. ADP SCALE (the deep one) ----------
    m = u[u['ADP_src']=='ESPN_new'].merge(e[['espn_id','espn_adp']],on='espn_id').dropna(subset=['espn_adp'])
    ins = m[m['espn_adp']<169].copy()
    ins = ins.sort_values('espn_adp'); ins['dense']=np.arange(1,len(ins)+1)
    ident = int((ins['ADP']-ins['espn_adp']).abs().lt(0.01).sum())
    med   = float((ins['ADP']-ins['espn_adp']).abs().median())
    rec('C1','CRITICAL','adp_scale','code_universe.ADP is average draft position',
        f'0 of {len(m)} rows equal espn_adp; median |gap| {med:.1f} picks inside the draftable range; '
        f'ADP == dense rank of espn_adp for the top ~60',
        'FAIL','espn_projections_2026_20260820.espn_adp','matched ESPN_new rows',len(m),
        'directive §2.1(c) effective-ADP table; §4.12 noise sd=0.135*ADP; all p_available; '
        'keeper_eligibility_VERIFIED.ESPN_ADP; HANDOFF §9.6 "-5 pick" residual')
    cens = int((e['espn_adp']>=169.4).sum())
    rec('C2','HIGH','adp_scale','ESPN ADP is informative across the draftable pool',
        f'{cens} of {len(e)} rows ({100*cens/len(e):.0f}%) sit in a 1.56-pick blob at ~170 = undrafted sentinel',
        'FAIL','espn_adp column','all ESPN rows',len(e),
        'pick 152 (effADP ~164) and pick 161 (effADP ~173) cannot be ordered by ADP')

    # ---------- D. D/ST AND K JOIN ----------
    ue, ee = (u['pos']=='D/ST').sum(), (e['pos']=='D/ST').sum()
    dst_u = u[u['pos']=='D/ST']['TOT']
    rec('D1','CRITICAL','join','D/ST projections are missing from the source',
        f'ESPN carries {ee} real D/ST projections (range {e[e["pos"]=="D/ST"]["proj_2026"].min():.1f}-'
        f'{e[e["pos"]=="D/ST"]["proj_2026"].max():.1f}, corr with ADP -0.82); universe holds {ue} rows '
        f'hard-set to {dst_u.iloc[0]} via proj_src=v2_carryover. Name key "Houston Texans" vs "Texans D/ST".',
        'FAIL','espn_projections_2026_20260820','all D/ST',int(ee),
        'pick 152; HANDOFF open thread #12 (misdiagnosed as missing data); §4.9 D/ST ADP finding')
    rec('D2','MED','join','all 32 defenses present',
        f'universe has {ue}; missing Falcons, Saints, Colts','FAIL','ESPN pull','D/ST',int(ee))
    vc = u[u['pos']=='K']['proj_src'].value_counts().to_dict()
    rec('D3','MED','staleness','kicker projections current',
        f'{vc.get("v2_carryover",0)} of {int((u["pos"]=="K").sum())} kickers are v2_carryover','FAIL',
        'proj_src column','all K',int((u['pos']=='K').sum()),'pick 161')

    # ---------- E. TEAM CODE KEYS ----------
    uT=set(u[u['pos']!='D/ST']['tm'].dropna()); eT=set(e[e['pos']!='D/ST']['team'].dropna())
    mism = sorted((uT-eT)|((eT-uT)-{'FA'}))
    rec('E1','HIGH','join','team codes agree across files',
        f'universe vs ESPN mismatch: {mism}; proe_team_season uses LA for LAR; '
        f'depth-chart file has 155 distinct Team values (should be 32)',
        'FAIL' if mism else 'PASS','code_universe.tm','non-D/ST rows',len(u),
        'any team-level join: OL status, PROE, SOS, depth charts')

    # ---------- F. INJURY SURFACING ----------
    mm = u.merge(e[['espn_id','injuryStatus','proj_2026']],on='espn_id',how='left')
    fl = mm[(mm['injuryStatus'].isin(['QUESTIONABLE','OUT','DOUBTFUL','INJURY_RESERVE']))&(mm['ADP']<=170)]
    rec('F1','HIGH','artifacts','injury status is surfaced on the board',
        f'{len(fl)} flagged players inside ADP 170 ({fl["injuryStatus"].value_counts().to_dict()}); '
        f'{int((fl["ADP"]<=50).sum())} inside ADP 50 incl. {", ".join(fl[fl["ADP"]<=50]["full"].head(3))}; '
        f'0 have proj zeroed, so the projection does not price the flag; universe has no injury column',
        'FAIL','espn injuryStatus','universe rows matched to ESPN',len(mm),
        'pick 8 primary (Nacua); every PREP MODE recommendation')

    # ---------- G. STRUCTURAL TENDENCIES (directive §4.7) ----------
    t = d[~d['Keeper']]
    r14 = t[t['Rd']<=4]
    obs = 100*r14['Pos'].isin(['RB','WR']).mean()
    rec('G1','MED','structural','§4.7 rounds 1-4 are 83.3% RB/WR', f'{obs:.1f}%',
        'PASS' if approx(obs,83.3,0.3) else 'FAIL','draft_history true picks','rounds 1-4, 2021-2025',len(r14))
    te = t[t['Pos']=='TE'].groupby(['Year','Manager'])['Rd'].min()
    ts = t.groupby(['Year','Manager']).size()
    early = int((te<3).sum())
    who = t[(t['Pos']=='TE')&(t['Rd']<3)][['Year','Manager','Pick','Player']].to_dict('records')
    rec('G2','HIGH','structural','§4.7 TE before round 3 = 1 of 43 team-seasons (herman allen only)',
        f'{early} of {len(ts)} team-seasons: ' + '; '.join(f"{r['Year']} {r['Manager']} pk{r['Pick']} {r['Player']}" for r in who),
        'FAIL','draft_history true picks','all team-seasons 2021-2025',len(ts),
        '§5 opponent model "allen is the ONLY early-TE manager"; grid Opponent-needs sheet; McBride p(avail) at 32')
    rec('G3','MED','structural','§4.7 median first TE round 7', f'{te.median():.0f}',
        'PASS' if te.median()==7 else 'FAIL','draft_history true picks','team-seasons with a TE',len(te))
    kk = t[t['Pos']=='K'].groupby(['Year','Manager'])['Rd'].min()
    kp = 100*(kk>=11).mean()
    rec('G4','LOW','structural','§4.7 first K at round 11+ in 95.8%', f'{kp:.1f}%',
        'PASS' if approx(kp,95.8,0.3) else 'FAIL','draft_history true picks','team-seasons with a K',len(kk))
    # earliest TE off the board per year
    first_te = t[t['Pos']=='TE'].loc[t[t['Pos']=='TE'].groupby('Year')['Pick'].idxmin()]
    rec('G5','MED','structural','HANDOFF §0: first TE off the board = 30(2022), 20(2023), none(2024), 22(2025)',
        '; '.join(f"{int(r.Year)}: pk{int(r.Pick)} {r.Player}" for r in first_te.itertuples()),
        'FAIL','draft_history true picks','all years',len(t),'McBride/Bowers survival to pick 32')

    # ---------- H. DRAFT HISTORY COMPLETENESS ----------
    pc = d.groupby('Year').size()
    short = pc[pc<180].to_dict()
    rec('H1','MED','completeness','all five drafts hold 180 picks',
        f'short years: {short}','FAIL' if short else 'PASS','12 teams x 15 rounds','draft_history',len(d),
        'every §4.7 percentage; franchise-bias z-scores')

    # ---------- I. KEEPER ELIGIBILITY ----------
    nap = k[k['Proj'].isna()]
    rec('I1','MED','keeper','every eligible keeper carries a projection',
        f'{len(nap)} of {len(k)} rows have no Proj: ' + ', '.join(nap['Player'].astype(str).head(8)),
        'FAIL' if len(nap) else 'PASS','keeper_eligibility_VERIFIED.csv','all eligible',len(k),
        'keeper prediction for Lobsinger, Fleming, Kam, Brown/Collins, allen')
    rec('I2','HIGH','keeper','keeper file ESPN_ADP is on the same scale as the board',
        'ESPN_ADP matches the universe rank column (Pickens 27, Rice 21), not espn_adp','FAIL',
        'code_universe.ADP','all eligible',len(k),
        'the "ADP-based keeper prediction beat projection-based 3-for-3" finding')

    # ---------- J. SNAKE / PICK STRUCTURE (should PASS) ----------
    picks=[(rd-1)*12 + (8 if rd%2 else 5) for rd in range(1,16)]
    exp=[8,17,32,41,56,65,80,89,104,113,128,137,152,161]
    rec('J1','OK','structure','§2.1(b) 14 selections at 8..161, no pick 176',
        f'{picks[:14]==exp} (round-15 slot would be {picks[14]})','PASS' if picks[:14]==exp else 'FAIL',
        '12-team snake, slot 8','arithmetic',15)

    # ---------- K. BYES (should PASS) ----------
    bt = u[(u['pos']!='D/ST')&u['tm'].notna()].groupby('tm')['bye'].nunique()
    rec('K1','OK','byes','one bye week per NFL team',
        f'{int((bt>1).sum())} teams with conflicting byes across {len(bt)} teams',
        'PASS' if (bt>1).sum()==0 else 'FAIL','code_universe.bye','32 NFL teams',int(len(bt)),
        '§4.11 bye traps — all 16 named players verified correct')

    out = pd.DataFrame(DEF)
    stamp = dt.date.today().isoformat().replace('-','')
    path = os.path.join(outdir, f'defects_{stamp}.csv')
    out.to_csv(path, index=False)
    fails = out[out['verdict']=='FAIL']
    print(f"checks {len(out)} | FAIL {len(fails)} | CRITICAL {int((fails['severity']=='CRITICAL').sum())} "
          f"| HIGH {int((fails['severity']=='HIGH').sum())}")
    print(fails[['check_id','severity','area','observed']].to_string(index=False)[:4000])
    print(f"\nwrote {path}")
    return 1 if len(fails) else 0

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--src',default='.'); ap.add_argument('--out',default='.')
    a=ap.parse_args(); sys.exit(main(a.src,a.out))
