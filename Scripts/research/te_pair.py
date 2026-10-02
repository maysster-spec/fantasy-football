"""The pair test at TIGHT END, the same shape doc 267 ran for defences and doc 428 for quarterbacks.
CLAIM: hold two tight ends so a hard week for one is an easy week for the other.
TESTABLE FORM: does starting whichever of {TE1, TE2} faces the softer defence beat always starting TE1?

EX ANTE (the default): for a game in week w, a defence's TE generosity is the mean of the points
scored against it by the opposing team's top TE over weeks 1 to w-1 ONLY, which is what a manager
could see on the Wednesday before the game. The game being scored never enters its own matchup term.

--in-sample reproduces the ORIGINAL behaviour as a control: one generosity per defence per season,
the mean over weeks 1 to 14, applied to every scored week. For the weeks 2-14 window that mean
INCLUDES the game being scored (lookahead); for the weeks 15-17 window it did not, and that window
was already ex ante on weeks 1-14. Doc 435 caught the lookahead cold on 28 Sept 2026: the first
version of this file said "leave-one-out" in this docstring and did the in-sample mean in the code.

TIERS, unchanged in both modes: weeks 1-14 points a game among TEs with 8+ games in weeks 1-14;
elite = ranks 1-6, mid = ranks 7-12, streamable = ranks 13-24. For the weeks 2-14 window that is
hindsight on WHO is elite, the same assumption doc 428 makes for quarterbacks (its assumption 1).
This file fixes the generosity term only; the tier assumption is stated, not removed.

Population: nflverse REG 2021-2025, the team's top TE each week, scored under this league's rules
(0.5 PPR: 0.5 a catch, 0.1 a yard, 6 a TD, -2 a lost fumble, 2 for a two-point conversion).
Inputs: _nflverse_cache/stats_player_week_{2021..2025}.csv, resolved against this file's own folder
unless --cache is given.

Usage:  py te_pair.py                 (ex ante, the number to quote)
        py te_pair.py --in-sample     (the control; reproduces the retracted rows)
        py te_pair.py --selftest      (negative control on the generosity term; exits 0 on PASS)
        py te_pair.py --cache PATH    (point at another nflverse cache folder)
"""
import argparse, itertools, os, sys
import pandas as pd, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(description='TE pair test, ex ante by default')
ap.add_argument('--in-sample', action='store_true',
                help='control: one weeks-1-14 generosity per defence per season (the original, lookahead in 2-14)')
ap.add_argument('--cache', default=os.path.join(HERE, '_nflverse_cache'),
                help='folder holding stats_player_week_{year}.csv')
ap.add_argument('--selftest', action='store_true',
                help='negative control: a perturbed scored game must move the in-sample term and not the ex-ante one')
args = ap.parse_args()
MODE = 'IN-SAMPLE (control: weeks 1-14 season mean, includes the scored game in the 2-14 window)' \
       if args.in_sample else 'EX ANTE (weeks 1 to w-1 only, what a manager sees on Wednesday)'

def score(d):
    g = lambda c: pd.to_numeric(d.get(c, 0), errors='coerce').fillna(0)
    return (g('receptions')*0.5 + g('receiving_yards')*0.1 + g('receiving_tds')*6
            + g('rushing_yards')*0.1 + g('rushing_tds')*6
            - (g('receiving_fumbles_lost')+g('rushing_fumbles_lost'))*2
            + (g('receiving_2pt_conversions')+g('rushing_2pt_conversions'))*2)

rows=[]
for yr in range(2021, 2026):
    f = os.path.join(args.cache, f'stats_player_week_{yr}.csv')
    if not os.path.exists(f):
        sys.exit(f'BLOCKED: missing input {f}')
    d = pd.read_csv(f, low_memory=False)
    d = d[(d['position']=='TE') & (d['season_type']=='REG') & (d['week'].between(1,17))].copy()
    d['pts']=score(d); d['season']=yr
    rows.append(d[['season','week','player_display_name','team','opponent_team','pts']])
t = pd.concat(rows, ignore_index=True)
t = t.sort_values('pts',ascending=False).groupby(['season','week','team'],as_index=False).first()
print(f'MODE: {MODE}')
print(f'cache: {args.cache}')
print(f'TE starts (team top TE), 2021-2025 REG wk1-17: n={len(t)}')

def generosity(s, reg, w, in_sample=None):
    """Centred generosity per defence for a game in week w of season frame s.
    in-sample: the weeks-1-14 mean (reg), the same Series for every w.
    ex ante  : the mean over weeks 1..w-1 only."""
    if in_sample is None: in_sample = args.in_sample
    base = reg if in_sample else s[s['week'] < w]
    gen = base.groupby('opponent_team')['pts'].mean()
    return gen - gen.mean()

def selftest():
    """Negative control (directive 0.2: a guard that has never fired is not a guard).
    Add 100 points to ONE scored game in week 8 of 2023. The in-sample term for that defence
    must move (it contains the game); the ex-ante term for the same week must not."""
    s = t[t['season']==2023].copy(); reg = s[s['week']<=14]
    row = s[s['week']==8].iloc[0]; opp = row['opponent_team']
    before_in, before_ex = generosity(s, reg, 8, True)[opp], generosity(s, reg, 8, False)[opp]
    s2 = s.copy(); s2.loc[row.name, 'pts'] += 100; reg2 = s2[s2['week']<=14]
    after_in, after_ex = generosity(s2, reg2, 8, True)[opp], generosity(s2, reg2, 8, False)[opp]
    moved_in, moved_ex = abs(after_in-before_in) > 1, abs(after_ex-before_ex) > 1e-9
    print(f'selftest: 2023 wk8 vs {opp}: in-sample moved {moved_in} ({before_in:+.2f} -> {after_in:+.2f}); '
          f'ex ante moved {moved_ex} ({before_ex:+.2f} -> {after_ex:+.2f})')
    if not moved_in or moved_ex:
        sys.exit('SELFTEST FAILED: the ex-ante generosity must ignore the scored game and the in-sample must not')
    print('selftest: PASS')
    sys.exit(0)

if args.selftest: selftest()

def run(window, label):
    A,B,swaps,sg,npair = [],[],0,[],0
    gaps=[]
    for yr, s in t.groupby('season'):
        reg = s[s['week']<=14]
        tot = reg.groupby('player_display_name').agg(g=('pts','size'), ppg=('pts','mean'))
        tot = tot[tot['g']>=8].sort_values('ppg',ascending=False)
        if len(tot) < 24: continue
        if label.startswith('mid'):
            elite, stream = list(tot.index[6:12]), list(tot.index[12:24])
        else:
            elite, stream = list(tot.index[:6]), list(tot.index[12:24])
        _hi = tot['ppg'].iloc[6:12] if label.startswith('mid') else tot['ppg'].iloc[:6]
        gaps.append(_hi.mean() - tot['ppg'].iloc[12:24].mean())
        win = s[s['week'].between(*window)].copy()
        # one generosity Series per scored week; in-sample mode returns the same Series each time
        gen_by_week = {w: generosity(s, reg, w) for w in sorted(win['week'].unique())}
        win['gen'] = [gen_by_week[w].get(opp, np.nan) for w, opp in zip(win['week'], win['opponent_team'])]
        win = win[win['gen'].notna()]
        idx = {(r.player_display_name, r.week): r for r in win.itertuples()}
        wks = sorted(win['week'].unique())
        pairs = (itertools.permutations(stream, 2) if label.startswith('stream')
                 else itertools.product(elite, stream))
        for e, o in pairs:
            a,b,sw,loc = [],[],0,[]
            for w in wks:
                re_, ro = idx.get((e,w)), idx.get((o,w))
                if re_ is None: continue
                a.append(re_.pts)
                if ro is not None and ro.gen > re_.gen:
                    b.append(ro.pts); sw+=1; loc.append(ro.pts-re_.pts)
                else: b.append(re_.pts)
            if len(a) < 3: continue
            npair+=1; swaps+=sw; sg+=loc
            A.append(np.mean(a)); B.append(np.mean(b))
    A,B = np.array(A), np.array(B); d = B-A
    se = d.std(ddof=1)/np.sqrt(len(d))
    sgn = np.array(sg)
    print(f'\n{label}, weeks {window[0]}-{window[1]}: n={npair} pairs')
    print(f'  always start TE1         : {A.mean():.2f} a week')
    print(f'  start the softer matchup : {B.mean():.2f} a week')
    print(f'  difference               : {d.mean():+.2f}  se {se:.2f}  t {d.mean()/se:+.2f}')
    if len(sgn):
        print(f'  when it benched TE1      : {sgn.mean():+.2f} a week, won {100*(sgn>0).mean():.0f}%, n={len(sgn)}')
    if gaps: print(f'  quality gap elite vs streamable: {np.mean(gaps):.2f} pts a week')

run((2,14),  'mid TE1 (ranks 7-12) + streamable TE2')
run((15,17), 'mid TE1 (ranks 7-12) + streamable TE2')
run((15,17), 'elite TE1 + streamable TE2')
run((15,17), 'streamable + streamable')
run((2,14),  'elite TE1 + streamable TE2')
run((2,14),  'streamable + streamable')
