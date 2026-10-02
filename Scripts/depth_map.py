#!/usr/bin/env python3
r"""
depth_map.py -- who is the direct backup, and to whom.

Parses 2026_NFL_Depth_Charts_All_Teams.csv (a scraped chart whose names carry provenance tags
like "Mason, Jordan T/SF", "Dobbins, J.K. U/LAC", "Fryar, Josh CF25") and produces, for every
skill player: his depth slot, and the player listed ahead of him.

Doc 102. Written because the first version of this parse silently missed anyone whose tag did
not match a hand-listed set -- Jordan Mason and David Montgomery both dropped out, which is the
name-join failure mode this project has hit ten times. The tag rule is now GENERAL: strip any
trailing token containing '/' or matching a year pattern, and report the match rate so a bad
parse cannot pass quietly.
"""
import os, re, sys, unicodedata
import pandas as pd
import numpy as np

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Source'))
CHART = os.path.join(SRC, '2026_NFL_Depth_Charts_All_Teams.csv')
BOARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_draft', 'board_v8_fixed.csv')
_VSTAMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_draft', 'adp_vintage.txt')
_VINTAGE = (open(_VSTAMP, encoding='utf-8').read().strip()
            if os.path.exists(_VSTAMP) else 'espn_projections_2026_20260823.csv')
ADP = os.path.join(SRC, _VINTAGE)          # the source pull: keepers still present (doc 111)
POS_OF = {'RB':'RB','FB':'RB','LWR':'WR','RWR':'WR','SWR':'WR','WR':'WR','TE':'TE','QB':'QB'}
FB_OFFSET = 10          # a fullback can never outrank a real back (doc 275)
TAG = re.compile(r'\s+(?:\S*/\S*|CF\d+\*?|SF\d+|PS\d*|IR|\d{2}FA|\d{2}/\d+)\s*$')

def strip_tags(v):
    v = unicodedata.normalize('NFKD', str(v)).encode('ascii','ignore').decode().strip()
    prev = None
    while prev != v:                       # a name can carry more than one tag
        prev = v; v = TAG.sub('', v).strip()
    return v

def display(v):
    v = strip_tags(v)
    if ',' in v:
        last, first = [x.strip() for x in v.split(',',1)]
        v = f"{first} {last}"
    return ' '.join(w.title() if w.isupper() and len(w) > 3 else w for w in v.split())

def key(v):
    # The suffix can be attached to the LAST name inside the chart's "Last, First" form
    # ("JONES SR., AARON") as well as trailing the board's form ("Aaron Jones Sr."). Strip it
    # in both places, case-insensitively, or thirteen players fall out of the join silently.
    v = display(v)
    v = re.sub(r'[^A-Za-z ]','', v)
    v = re.sub(r'(?i)\b(jr|sr|ii|iii|iv|v)\b','', v)
    return re.sub(r'\s+',' ', v).strip().lower()

def build():
    dc = pd.read_csv(CHART); dc = dc[dc.Pos.notna()]
    rows = []
    for _, r in dc.iterrows():
        raw = str(r.Pos).strip().upper()
        fam = POS_OF.get(raw)
        if not fam: continue
        # A FULLBACK IS NOT THE MAN WHO INHERITS A RUNNING BACK'S JOB (doc 275).  ESPN files FB
        # under RB, and the chart gives every team its own FB row whose Player 1 is slot 1 -- so
        # sort_values('slot') + drop_duplicates kept the fullback AHEAD of the real starter.
        # Measured on the shipped file: 12 of 32 teams had a fullback at depth 1, which made
        # wire.py's "the man ahead" a fullback on those teams and nothing fired.  Push the FB
        # chain below every real back instead of dropping it, so no row disappears.
        off = FB_OFFSET if raw == 'FB' else 0
        starter = r.get('Player 1')
        for k, col in enumerate(['Player 1','Player 2','Player 3','Player 4','Player 5'], 1):
            v = r.get(col)
            if isinstance(v, str) and v.strip():
                rows.append(dict(key=key(v), fam=fam, slot=k + off, tm=str(r.Team).strip(),
                                 ahead=(display(starter) if k > 1 and isinstance(starter,str) else '')))
    S = pd.DataFrame(rows).sort_values('slot').drop_duplicates(['key','fam'])
    return S

def preseason_ceiling():
    """The lead-RB projection from the EARLIEST 2026 pull on the drive, per team (doc 307).

    WHY THIS EXISTS. `ceil[tm]` below is defined as ESPN's projection for the man currently
    holding the job (directive 4.20). When that man is removed from the team, ESPN cuts HIS
    projection, and the code then reads the cut number as what the JOB pays. The job did not get
    smaller; the man left. Green Bay: Josh Jacobs went on the Commissioner's Exempt List on
    30 Aug 2026, ESPN moved him 241.0 -> 152.5, and the wire told Matt the one indefinitely vacant
    backfield in the league was worth 152.

    THE SAME ARITHMETIC PRODUCES ONE RIGHT ANSWER AND ONE WRONG ONE, which is why this is easy to
    miss: `job_gap` collapsing 163 -> 28 correctly flips the label to UNSETTLED, and it is left
    alone. Only the CEILING is lifted.

    THE THRESHOLD IS MEASURED, NOT CHOSEN. Across all 32 teams between the 08-23 and 09-07 pulls
    the lead-RB projection moved by a median of 0.5 points, p90 of 3.0, and the largest fall other
    than Green Bay was 2.9. Green Bay fell 88.6. At 40 this guard fires on exactly one team and
    cannot reach the noise.

    NOTE it cannot key on injuryStatus: ESPN carries Jacobs as DAY_TO_DAY, not OUT, because an
    exempt-list absence has no injury code. A status guard would not have fired.
    """
    import glob
    cands = sorted(glob.glob(os.path.join(SRC, 'espn_projections_2026_*.csv')))
    if not cands:
        return {}, ''
    f = cands[0]                      # filenames carry YYYYMMDD, so sorted() is chronological
    try:
        d = pd.read_csv(f, low_memory=False)
    except Exception as exc:          # a missing baseline must not take the gate down
        print(f'  preseason ceiling unavailable ({type(exc).__name__}); job_ceil left as pulled')
        return {}, ''
    d.columns = [c.replace('\ufeff', '') for c in d.columns]
    d = d[d.pos == 'RB'].copy()
    d['proj'] = pd.to_numeric(d.proj_2026, errors='coerce').fillna(0)
    out = {}
    for tm, g in d.groupby('team'):
        v = g.sort_values('proj', ascending=False).proj.values
        if len(v):
            out[tm] = float(v[0])
    return out, os.path.basename(f)


def main():
    S = build()
    b = pd.read_csv(BOARD); b['key'] = b.player.map(key)
    m = b.merge(S[['key','fam','slot','ahead']], left_on=['key','pos'], right_on=['key','fam'], how='left')
    hit = m.slot.notna()
    top = m[m.eff_pick <= 175]
    print(f"depth chart entries : {len(S)}")
    print(f"board rows matched  : {hit.sum()} / {len(m)}  ({hit.mean()*100:.0f}%)")
    print(f"  inside pick 175   : {top.slot.notna().sum()} / {len(top)}  ({top.slot.notna().mean()*100:.0f}%)")
    if top.slot.notna().mean() < 0.85:
        sys.exit("  MATCH RATE TOO LOW -- the parse is broken, do not use this output.")
    # doc 110/111: HOW OPEN IS THE JOB.  Matt's rule: a backup is worth a dart when the job is
    # genuinely UNSETTLED (someone can win it) or when the starter owns a big job (so an injury
    # hands over something worth having) -- NOT when two men permanently split a small pie.
    #
    # Computed from the SOURCE pull, not the board: the board has the 12 keepers removed, which
    # deletes DAL's, NYG's and NE's lead backs and makes those backfields look empty (doc 111).
    #
    # MEASURED: the team RB pie barely varies (IQR 317-355 proj pts, +/-6%).  So "big pie vs small
    # pie" is nearly a constant and cannot be the second axis.  What the gap actually measures is
    # ESPN's UNCERTAINTY about who wins -- which is Matt's target, not his avoid.  The old
    # COMMITTEE label was therefore polarised backwards.
    src = pd.read_csv(ADP)
    src.columns = [c.replace('\ufeff','') for c in src.columns]
    srb = src[src.pos == 'RB'].copy()
    srb['proj'] = pd.to_numeric(srb.proj_2026, errors='coerce').fillna(0)
    gap, pie, ceil = {}, {}, {}
    for tm, g in srb.groupby('team'):
        v = g.sort_values('proj', ascending=False).proj.values
        if len(v) < 2: continue
        gap[tm]  = float(v[0] - v[1])
        pie[tm]  = float(v[:3].sum())
        ceil[tm] = float(v[0])          # ESPN's own estimate of what the lead job is worth
    # A JOB'S WORTH MAY NOT FALL BECAUSE ITS HOLDER LEFT (doc 307). gap and pie are untouched:
    # the gap collapsing is real information and is what flips the label to UNSETTLED.
    pre, pre_file = preseason_ceiling()
    lifted = []
    for tm_, v_ in list(ceil.items()):
        v0 = pre.get(tm_)
        if v0 and (v0 - v_) > 40:
            lifted.append((tm_, v_, v0))
            ceil[tm_] = v0
    if lifted:
        print(f'  job ceiling restored from {pre_file} (the holder left; the job did not shrink):')
        for tm_, v_, v0 in sorted(lifted):
            print(f'    {tm_}  {v_:.0f} -> {v0:.0f}')

    tm_fix = {'WSH':'WAS'}
    for d_ in (gap, pie, ceil):
        for a, b_ in tm_fix.items():
            if a in d_: d_[b_] = d_[a]
    m['job_gap']  = m.team_c.map(gap).round(0)
    m['job_pie']  = m.team_c.map(pie).round(0)
    m['job_ceil'] = m.team_c.map(ceil).round(0)
    def label(x):
        if pd.isna(x):   return ''
        if x < 60:       return 'UNSETTLED'      # job to be won -- Matt's archetype
        if x < 150:      return 'contested'
        return 'LEAD BACK'                       # starter owns it; backup pays only on injury
    m['job'] = m.job_gap.map(label)
    # a backup on an UNSETTLED or LEAD BACK team, priced late, is the shape Matt wants
    # gate to the real-ADP region: past ~pick 168 ESPN serves an undrafted sentinel and the
    # ordering is fabricated (directive 4.14), so a "dart" there is not a dart, it is noise.
    m['dart_shape'] = np.where(
        (m.pos == 'RB') & (m.slot.fillna(0) >= 2) & (m.eff_pick >= 90) &
        (m.adp_pick < 168) & (m.job.isin(['UNSETTLED','LEAD BACK'])), 'Y', '')
    out = m[hit][['espn_id','player','pos','team_c','bye','vbd','adp_pick','eff_pick','slot',
                  'ahead','job_gap','job_pie','job_ceil','job','dart_shape']]
    out = out.rename(columns={'team_c':'tm','eff_pick':'goes_at','slot':'depth'})
    out.depth = out.depth.astype(int)
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'depth_map.csv')
    out.to_csv(dest, index=False)
    print(f"  wrote {dest}  ({len(out)} rows)")

    # doc 112: put the job label where the LIVE BOARD can see it.  The kit is exactly six files
    # and depth_map.csv is not one of them, so the label rides in player_context.csv, which is.
    # UPDATE ONLY -- never adds a row, never touches a column it does not own.  Matt's own takes
    # live in this file (mine / mine_note) and clobbering them at 7:50 PM would be unrecoverable.
    ctx = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_draft', 'player_context.csv')
    if os.path.exists(ctx):
        pc = pd.read_csv(ctx)
        before = pc.copy()
        # RB ONLY.  The label describes a team's BACKFIELD; stamping it on a WR or a QB made
        # Patrick Mahomes a "LEAD BACK" in the first run of this code.
        rbs = m[m.pos == 'RB'].dropna(subset=['espn_id'])
        jm = rbs.set_index(rbs.espn_id.astype('Int64'))
        is_rb = pc.pos.astype(str).str.upper() == 'RB'
        for col in ('job', 'job_ceil'):
            if col not in pc.columns: pc[col] = ''
            vals = pc.ESPN_ID.map(jm[col]).where(is_rb)
            pc[col] = vals.where(vals.notna(), pc[col]).fillna('')
        pc['job_ceil'] = pc.job_ceil.map(lambda v: '' if v == '' or pd.isna(v) else int(float(v)))
        # nothing outside the two job columns may change
        for c_ in before.columns:
            if c_ in ('job', 'job_ceil'): continue
            if not before[c_].fillna('').astype(str).equals(pc[c_].fillna('').astype(str)):
                sys.exit(f"  REFUSING TO WRITE: column '{c_}' changed in player_context.csv")
        pc.to_csv(ctx, index=False)
        n_job = int((pc.job.astype(str) != '').sum())
        print(f"  stamped job labels into player_context.csv ({n_job} rows carry one)")
        try:
            import hashlib, re as _re
            chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'check_kit.py')
            d = open(ctx, 'rb').read().replace(b'\r\n', b'\n')
            cs = open(chk, encoding='utf-8').read()
            new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
            cs2 = _re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                          lambda mm: mm.group(1) + new, cs, count=1)
            if cs2 != cs:
                open(chk, 'w', encoding='utf-8', newline='').write(cs2)
                print(f"  re-pinned player_context.csv -> {new.strip('(),')}")
        except Exception as e:
            print(f"  (could not re-pin: {e} -- run check_kit.py and repin by hand)")
    miss = m[~hit & (m.eff_pick <= 175)].player.tolist()
    if miss: print(f"  unmatched inside 175 ({len(miss)}): {', '.join(miss[:12])}")

if __name__ == '__main__':
    main()
