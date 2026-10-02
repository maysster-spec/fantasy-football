#!/usr/bin/env python3
"""Matt's claim, stated before testing (0.5a2), in his words:
"the offence could [crater] and then the defense is on the field too much and gets tired by the
last quarter. Think, the longer the opposing team's offence on the field the greater chance that
team will score."

Two testable forms, both stated before running:
  T1 TIRED:  POPULATION team-games 2021-2025 regular season (n~2,720 defence-games).
             PREDICTOR  scrimmage plays faced in quarters 1-3.
             OUTCOME    points allowed in quarter 4 alone.
             CONTROL    the defence's own team-season mean (both sides demeaned, so a bad
                        defence being busy AND leaky cannot produce the result), and the score
                        margin entering Q4 (garbage time is the other confound).
             DIRECTION  more plays faced -> MORE Q4 points allowed.
  T2 CRATER: same population. PREDICTOR his own offence's EPA per play, Q1-Q3, demeaned.
             OUTCOME    the defence's league-scored D/ST fantasy points for the whole game.
             DIRECTION  worse own offence -> FEWER D/ST points.
"""
# INPUTS: play_by_play_{2021..2025}.csv.gz from
#   https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_<year>.csv.gz
#   plus Source\\dst_weekly_2021_2025.csv. ~95 MB of play-by-play, so this is a research
#   script for the record and not part of any weekly run.
import gzip, math, numpy as np, pandas as pd

COLS = ['game_id','season','week','season_type','posteam','defteam','posteam_type','qtr',
        'play_type','epa','posteam_score_post','defteam_score_post','play_id',
        'fixed_drive','drive_play_count','fixed_drive_result','home_team','away_team']
frames=[]
for yr in range(2021,2026):
    d=pd.read_csv(f'play_by_play_{yr}.csv.gz', compression='gzip', usecols=COLS, low_memory=False)
    d=d[d.season_type=='REG']
    frames.append(d)
pbp=pd.concat(frames, ignore_index=True)
print(f"  plays loaded: {len(pbp):,}   games: {pbp.game_id.nunique():,}")

# --- running score after each play, mapped to home/away, forward-filled within game ---
ish = pbp.posteam_type.eq('home')
pbp['home_after'] = np.where(ish, pbp.posteam_score_post, pbp.defteam_score_post)
pbp['away_after'] = np.where(ish, pbp.defteam_score_post, pbp.posteam_score_post)
pbp = pbp.sort_values(['game_id','play_id'])
pbp[['home_after','away_after']] = pbp.groupby('game_id')[['home_after','away_after']].ffill()

SCRIM = {'pass','run'}
pbp['scrim'] = pbp.play_type.isin(SCRIM)

# score at end of Q3 and end of Q4 (regulation), per game
def last_at(maxq):
    s = pbp[pbp.qtr<=maxq].groupby('game_id')[['home_after','away_after']].last()
    return s
q3 = last_at(3).rename(columns={'home_after':'h3','away_after':'a3'})
q4 = last_at(4).rename(columns={'home_after':'h4','away_after':'a4'})
gm = pbp.groupby('game_id')[['season','week','home_team','away_team']].first().join(q3).join(q4)

# defensive plays faced, Q1-3 and full game, by defteam
faced13 = pbp[(pbp.qtr<=3)&pbp.scrim].groupby(['game_id','defteam']).size().rename('faced13')
facedall= pbp[pbp.scrim].groupby(['game_id','defteam']).size().rename('faced_all')
# own offence Q1-3: plays and epa/play
own13 = pbp[(pbp.qtr<=3)&pbp.scrim].groupby(['game_id','posteam']).agg(
            own_plays13=('scrim','size'), own_epa13=('epa','mean'))
# three-and-outs by own offence, Q1-3
dr = pbp[pbp.qtr<=3].groupby(['game_id','posteam','fixed_drive']).agg(
        pc=('drive_play_count','max'), res=('fixed_drive_result','last')).reset_index()
dr['tao'] = (dr.pc<=3) & dr.res.isin(['Punt','Turnover'])
tao = dr.groupby(['game_id','posteam']).tao.sum().rename('three_and_outs13')

rows=[]
for gid, g in gm.iterrows():
    for team, opp, is_home in ((g.home_team, g.away_team, True), (g.away_team, g.home_team, False)):
        opp_q4 = (g.a4-g.a3) if is_home else (g.h4-g.h3)          # points the OPPONENT scored in Q4
        my_q3  = g.h3 if is_home else g.a3
        op_q3  = g.a3 if is_home else g.h3
        rows.append(dict(game_id=gid, season=int(g.season), week=int(g.week), team=team, opp=opp,
                         q4_allowed=opp_q4, margin_q4=my_q3-op_q3))
tg = pd.DataFrame(rows)
tg = (tg.merge(faced13, left_on=['game_id','team'], right_index=True, how='left')
        .merge(facedall, left_on=['game_id','team'], right_index=True, how='left')
        .merge(own13,   left_on=['game_id','team'], right_index=True, how='left')
        .merge(tao,     left_on=['game_id','team'], right_index=True, how='left'))
assert tg.faced13.notna().all(), tg[tg.faced13.isna()].head()

dst = pd.read_csv('dst_weekly_2021_2025.csv')
tg = tg.merge(dst[['season','week','team','dst_pts','allowed']], on=['season','week','team'], how='left')
miss = tg.dst_pts.isna().sum()
print(f"  defence-games: {len(tg):,}   D/ST points joined on {len(tg)-miss:,}  (unjoined {miss})")
tg = tg.dropna(subset=['dst_pts'])

# --- demean within team-season (0.5: the defence's own quality cannot drive the result) ---
def dm(col):
    return tg[col] - tg.groupby(['team','season'])[col].transform('mean')
for c in ['q4_allowed','faced13','faced_all','own_epa13','own_plays13','three_and_outs13',
          'dst_pts','margin_q4','allowed']:
    tg['dm_'+c]=dm(c)

def ols(y, Xcols, label):
    d = tg[[y]+Xcols].dropna()
    X = np.column_stack([np.ones(len(d))]+[d[c].values for c in Xcols])
    yv = d[y].values
    b, *_ = np.linalg.lstsq(X, yv, rcond=None)
    resid = yv - X@b
    n,k = X.shape
    s2 = resid@resid/(n-k)
    se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    print(f"\n  {label}   n={n:,}")
    for name,bi,si in zip(['(const)']+Xcols, b, se):
        t = bi/si
        # normal approx two-sided p
        p = 2*(1-0.5*(1+math.erf(abs(t)/np.sqrt(2)))) if abs(t)<40 else 0.0
        star = '  <<<' if p<0.05 and name!='(const)' else ''
        print(f"      {name:<22} {bi:+9.4f}   se {si:6.4f}   t {t:+6.2f}   p {p:.4f}{star}")
    return b, se

print("\n" + "="*78)
print("  T1 -- DOES A BUSY FIRST THREE QUARTERS COST POINTS IN THE FOURTH?")
print("="*78)
print(f"  plays faced Q1-3: mean {tg.faced13.mean():.1f}, sd {tg.faced13.std():.1f}"
      f"   |  Q4 points allowed: mean {tg.q4_allowed.mean():.2f}, sd {tg.q4_allowed.std():.2f}")
ols('dm_q4_allowed', ['dm_faced13'], 'raw, demeaned by team-season')
ols('dm_q4_allowed', ['dm_faced13','dm_margin_q4'], '+ score margin entering Q4 (the garbage-time control)')
tg['abs_margin']=tg.margin_q4.abs(); tg['dm_abs_margin']=dm('abs_margin')
ols('dm_q4_allowed', ['dm_faced13','dm_margin_q4','dm_abs_margin'], '+ |margin| as well')

print("\n" + "="*78)
print("  T2 -- DOES HIS OWN OFFENCE CRATERING COST THE DEFENCE FANTASY POINTS?")
print("="*78)
ols('dm_dst_pts', ['dm_own_epa13'], 'D/ST points ~ own offence EPA/play Q1-3')
ols('dm_dst_pts', ['dm_three_and_outs13'], 'D/ST points ~ own three-and-outs Q1-3')
ols('dm_dst_pts', ['dm_faced_all'], 'D/ST points ~ plays faced, whole game')
ols('dm_allowed',  ['dm_faced_all'], 'points allowed ~ plays faced, whole game')

# the band question: how much D/ST fantasy value is at stake per +1 sd of plays faced?
sd = tg.dm_faced_all.std()
print(f"\n  sd of demeaned plays faced (whole game) = {sd:.2f}")
tg.to_csv('tired_games.csv', index=False)
print("  wrote tired_games.csv")
