"""
engine.py -- draft simulator + competing pick-selection rules.
Objective: expected STARTING-LINEUP points, weeks 1-14, bye- and injury-adjusted.
Opponent model: eff_pick + N(0, K_NOISE*eff_pick), TE +15, Snyder/Allen behavioural.
"""
import numpy as np, pandas as pd

K_NOISE   = 0.30           # doc 53
ADP_CAP   = 70.0           # doc 53 corr. -- noise stops growing past here; beyond pick ~84
                           # a proportional sd over-disperses by 40-70% vs observed residuals
TE_SHIFT  = 15.0           # directive 4.12
GP_PROJ   = 15.32          # doc 42: ESPN projects this many games
GP_ACTUAL = 14.46          # doc 42: players actually play this many
P_WEEK    = GP_ACTUAL/17.0
WEEKS     = list(range(1,15))
MY_SKILL_PICKS = [8,17,32,41,56,65,80,89,104,113,128,137]
N_TEAMS, N_ROUNDS = 12, 14
TOTAL_PICKS = N_TEAMS*N_ROUNDS            # 168
MY_SLOT = 8
KEEPER = dict(player='George Pickens', pos='WR', proj=None, bye=14.0)

# starting lineup (K and D/ST excluded -- streamed, §4.8)
SLOTS = [('QB',1),('RB',2),('WR',2),('TE',1)]
FLEX_OK = ('RB','WR','TE')
# replacement per-season (directive 4.1); waiver fill is worse than draft-day replacement
REPL      = {'QB':341.603, 'RB':168.589, 'WR':163.540, 'TE':140.295}
# V5 (doc 57): these are the levels board_v7_2026.csv's own vbd column was built on,
# recovered as proj_leaguepts - vbd. Directive 4.1's 341.7/168.0/168.5/137.7 came from a
# 200-row v2 export and is stale -- WR was 5.0 points too high.
WAIVER_FRAC = 0.80

def load(board_csv='/tmp/build/board_v7_2026.csv', keeper_proj=None):
    b = pd.read_csv(board_csv)
    b = b[b.pos.isin(['QB','RB','WR','TE'])].reset_index(drop=True)
    if keeper_proj is None:                       # Pickens' own projection
        keeper_proj = 155.0
    return b, keeper_proj

class Sim:
    def __init__(self, b, keeper_proj, rng):
        self.rng = rng
        self.pos  = b.pos.values
        self.proj = b.proj_leaguepts.values.astype(float)
        self.vbd  = b.vbd.values.astype(float)
        self.bye  = b.bye.values.astype(float)
        self.name = b.player.values
        adp = b.eff_pick.values.astype(float).copy()
        self.adp_opp = adp + np.where(self.pos=='TE', TE_SHIFT, 0.0)
        self.n = len(b)
        self.pg = self.proj/GP_PROJ               # per-game
        self.keeper_pg = keeper_proj/GP_PROJ
        self.repl_pg = {p:REPL[p]/GP_PROJ*WAIVER_FRAC for p in REPL}
        self.repl_i  = {0:self.repl_pg['QB'],1:self.repl_pg['RB'],2:self.repl_pg['WR'],3:self.repl_pg['TE']}
        self.allen = int(np.where(self.name=='Josh Allen')[0][0]) if (self.name=='Josh Allen').any() else -1

    # ---------- opponent behaviour ----------
    def draw_pref(self):
        a = self.adp_opp
        return a + self.rng.normal(0, K_NOISE*np.minimum(a, ADP_CAP))

    OPP_WINDOW = 8      # calibrated below: opponents take the best VBD among the N players
                        # nearest the top of their noisy board -- i.e. they use a cheat sheet,
                        # they do not draft blindly down ADP.

    @staticmethod
    def opp_legal(counts, remaining):
        """cap board for an opponent roster; returns a set of allowed positions"""
        caps = dict(QB=2, RB=6, WR=6, TE=2)   # real managers do not roster 3 QBs
        ok = {p for p in caps if counts.get(p,0) < caps[p]}
        need = [p for p in ('QB','TE') if counts.get(p,0)==0]
        if need and remaining <= len(need):        # must fill QB/TE before the draft ends
            return set(need)
        return ok

# ---------------- lineup scoring ----------------
def score_roster(pos_list, pg_list, bye_list, repl_pg, rng, n_weeks_reps=1):
    """expected starting-lineup points, weeks 1-14, with per-week availability draws"""
    pos_list = list(pos_list); pg = np.array(pg_list, float); bye = np.array(bye_list, float)
    total = 0.0
    for _ in range(n_weeks_reps):
        for w in WEEKS:
            live = (bye != w) & (rng.random(len(pg)) < P_WEEK)
            pts = 0.0
            used = np.zeros(len(pg), bool)
            for slot, cnt in SLOTS:
                cand = [i for i in range(len(pg)) if live[i] and not used[i] and pos_list[i]==slot]
                cand.sort(key=lambda i: -pg[i])
                for j in range(cnt):
                    if j < len(cand):
                        pts += pg[cand[j]]; used[cand[j]] = True
                    else:
                        pts += repl_pg[slot]
            cand = [i for i in range(len(pg)) if live[i] and not used[i] and pos_list[i] in FLEX_OK]
            pts += max([pg[i] for i in cand], default=max(repl_pg[p] for p in FLEX_OK))
            total += pts
    return total/n_weeks_reps
