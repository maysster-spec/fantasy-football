"""Check the DIRECTIVE's load-bearing numbers against the files that are actually shipping.
Nothing here is read off the doc; every value is recomputed.
v9.8 (doc 367): SECTION 4 lives in Source\\DIRECTIVE_FINDINGS.md; the two SS4.14 counts are read from there."""
import sys, os, re, hashlib
import pandas as pd, numpy as np
# doc 165 wave 5: these three were HARDCODED to the container this script was written in --
# SS0.4 v6.8's exact failure ("a script that runs in your container is not a script that runs").
# The directive tells Matt this audit exists; it could not run on his machine. Resolve
# everything against the script's own location instead.
HERE = os.path.dirname(os.path.abspath(__file__))          # ...\Scripts\research
SCR  = os.path.normpath(os.path.join(HERE, '..')) + os.sep  # ...\Scripts\
ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))     # ...\2026
SRC  = os.path.join(ROOT, 'Source') + os.sep
KIT  = os.path.join(SCR, 'live_draft')
sys.path.insert(0, KIT)
import code_live_engine as CLE
b=pd.read_csv(os.path.join(KIT,'board_v8_fixed.csv'))
OK=FAIL=0
def chk(label, got, want, tol=None):
    global OK, FAIL
    if tol is None: ok = got == want
    else:
        try: ok = abs(float(got)-float(want)) <= tol
        except Exception: ok = False
    print(f"  {'ok  ' if ok else 'FAIL'} {label:<52} directive {want}   actual {got}")
    OK, FAIL = OK+ok, FAIL+(not ok)

print('=== SECTION 2.1(b) — the fourteen selections ===')
chk('MY_PICKS + D/ST + K', list(CLE.MY_PICKS)+[CLE.DST_PICK,CLE.K_PICK],
    [8,17,32,41,56,65,80,89,104,113,128,137,152,161])

print('\n=== SECTION 4.1 — replacement levels (proj - vbd, per position) ===')
for p,w in (('QB',341.603),('RB',168.589),('WR',163.540),('TE',140.295)):
    s=b[b.pos==p]; got=round(float((s.proj_leaguepts-s.vbd).mean()),3)
    chk(f'{p} replacement', got, w, 0.001)
print('  CAPS (SS6 doctrine: never 3 QB / 3 TE):', CLE.CAPS)
chk('CAPS QB', CLE.CAPS.get('QB'), 2); chk('CAPS TE', CLE.CAPS.get('TE'), 2)

print('\n=== SECTION 4.1 / 4.2 / 4.3 — the quoted VBDs ===')
for nm,w in (('Jahmyr Gibbs',162.3),('Puka Nacua',131.3),('Christian McCaffrey',134.9),
             ('Brock Bowers',51.2),('Trey McBride',47.6),('Mark Andrews',0.0),
             ('Amon-Ra St. Brown',101.33),('Josh Allen',80.31),('Lamar Jackson',33.02),
             ('Matthew Stafford',21.19),('Tyler Warren',28.1)):
    r=b[b.player==nm]
    chk(nm, round(float(r.vbd.iloc[0]),2) if len(r) else 'NOT ON BOARD', w, 0.06)

# doc 180: these two expectations WERE hand-copied constants, so when SS4.14 was corrected on
# 09-05 the doc and its own auditor disagreed and the audit still said FAIL. That is the
# one-number-in-two-places defect the naming rule exists for, inside the tool meant to catch it.
# Read them OUT of the directive; fall back to the constants and SAY SO if the wording moves.
def from_directive(pattern, fallback, what):
    """Pull a load-bearing number out of SS4.14's prose. A parse miss must be LOUD, not silent."""
    # v9.8 (doc 367): SECTION 4 moved whole to Source\DIRECTIVE_FINDINGS.md and the directive keeps
    # only an index. Read the findings file first; fall back to the directive so this runs on either
    # side of the split; and say which file the number came from.
    txt, src = None, None
    for fn in ('DIRECTIVE_FINDINGS.md', '00_PROJECT_DIRECTIVE.md'):
        try:
            txt = open(os.path.join(SRC, fn), encoding='utf-8').read(); src = fn
        except Exception:
            continue
        if re.search(pattern, txt):
            break
    if txt is None:
        print(f'       !! could not read DIRECTIVE_FINDINGS.md or the directive -- using the built-in {what}={fallback}')
        return fallback
    m = re.search(pattern, txt)
    if not m:
        print(f'       !! SS4.14 wording moved (looked in DIRECTIVE_FINDINGS.md then the directive) -- could not parse {what}; using the built-in {fallback}')
        return fallback
    print(f'       ({what} read from {src})')
    return int(m.group(1))

print('\n=== SECTION 4.14 — the undrafted sentinel ===')
top=b.adp_pick.round(0).value_counts().idxmax()
n_sent=int((b.adp_pick>=top-1).sum())
want_sent = from_directive(r'\((\d+) of \d+ rows on the [\d-]+ freeze', 328, 'sentinel rows')
want_real = from_directive(r'Only ~(\d+) rows', 152, 'genuine-ADP rows')
chk('rows inside the sentinel blob', n_sent, want_sent)
chk('rows with a genuine draft position', len(b)-n_sent, want_real)
print(f'       (the sentinel now sits at adp ~{top:.0f}; it was ~158 on the 08-23 board)')

print('\n=== SECTION 9 — the kit ===')
# doc 165 wave 5: this counted DIRECTORY ENTRIES and reported 14 against the directive's 9.
# The folder legitimately also holds RUNTIME OUTPUT -- bridge_picks.json, bridge_raw.jsonl,
# adp_vintage.txt, DRAFT_ROOM_RECON.txt, replay_log.txt -- which are not kit members. The
# directive's "nine" means nine PINNED files, so count those, and say so when one is missing.
KITMEMBERS = ['live_draft.py', 'code_live_engine.py', 'board_v8_fixed.csv',
              'board_v7_kdst_separate.csv', 'ESPN_prerank_with_ids.csv', 'player_context.csv',
              'bridge_server.py', 'bench_lineup.py', 'probe_sources.py']
present = [f for f in KITMEMBERS if os.path.exists(os.path.join(KIT, f))]
chk('kit files (pinned members present)', len(present), 9)
if len(present) != 9:
    print('       MISSING:', [f for f in KITMEMBERS if f not in present])
chk('espn_bridge files', len(os.listdir(os.path.join(KIT, 'espn_bridge'))), 5)

print('\n=== SECTION 8 — the pull script size ===')
d=open(SCR+'Espn_pull_projections.py','rb').read().replace(b'\r\n',b'\n')
chk('Espn_pull_projections.py bytes', len(d), 15194)

print('\n=== SECTION 2.1(c) — keepers gone ahead / effective ADP available ===')
# SS2.1(c) says this table is "solved as a fixed point on the keeper ADPs", so solve it the same
# way. The board's own `gone_ahead` column is PER PLAYER, not per pick -- reading it as the table
# is what made my first pass report a false failure at pick 41.
import unicodedata
def _key(n):
    n=unicodedata.normalize('NFKD',str(n)).encode('ascii','ignore').decode()
    n=re.sub(r"[^A-Za-z ]",'',n); n=re.sub(r'(?i)\b(jr|sr|ii|iii|iv|v)\b','',n)
    return ' '.join(n.split()).lower()
# [1 Oct, doc 468] THE TABLE IS A FUNCTION OF THE LIST AND THE FREEZE IT NAMES, SO SOLVE ON THOSE.
# The draft book says the table was solved on the 09-03 keeper ADPs of the PREDICTED list
# (predicted_keepers_v5.csv); on that pull and that list the twelve ADPs reproduce exactly. The
# first in-season run of this auditor read actual_keepers.csv against the NEWEST pull and reported
# fifteen false failures (section 1.1: ESPN's ADP drifts toward what happened once the season
# starts; and the lock replaced two predicted keepers with a kicker and a defense). The published
# table is checked as published; the post-lock table is printed beneath it as information.
FREEZE = '20260903'
_glob = __import__('glob')
_pulls = sorted(_glob.glob(SRC+'espn_projections_2026_*.csv'))
def _pull_at(cutoff):
    at = [q for q in _pulls if re.search(r'_(\d{8})', os.path.basename(q)).group(1) <= cutoff]
    return (at or [None])[-1]
def _kadp(pullpath, listpath):
    pl=pd.read_csv(pullpath); km={_key(r.Player):r.espn_adp for _,r in pl.iterrows()}
    kp=pd.read_csv(listpath)
    return sorted(float(km[_key(n)]) for n in kp.Player)
def _solve(kadp, pk):
    e=pk
    for _ in range(20):
        e2=pk+sum(1 for a in kadp if a<e)
        if e2==e: break
        e=e2
    return sum(1 for a in kadp if a<e), e
TABLE={8:(0,8),17:(0,17),32:(4,36),41:(10,51),56:(10,66),65:(10,75),80:(11,91),89:(11,100),
       104:(12,116),113:(12,125),128:(12,140),137:(12,149),152:(12,164),161:(12,173)}
pull = _pull_at(FREEZE)
pred = os.path.join(SRC, 'predicted_keepers_v5.csv')
if pull is None or not os.path.exists(pred):
    print(f'  !! the {FREEZE} pull or predicted_keepers_v5.csv is not in Source, so the published table cannot be checked as published')
    for pk,(wn,we) in TABLE.items():
        chk(f'pick {pk}: keepers ahead', 'NOT CHECKED', wn); chk(f'pick {pk}: eff ADP available', 'NOT CHECKED', we)
else:
    kadp=_kadp(pull, pred)
    print(f'  keeper ADPs from {os.path.basename(pull)} on predicted_keepers_v5.csv: {[round(x,1) for x in kadp]}')
    for pk,(wn,we) in TABLE.items():
        n,e=_solve(kadp, pk)
        chk(f'pick {pk}: keepers ahead', n, wn)
        chk(f'pick {pk}: eff ADP available', e, we, 1)
    # the table the lock actually produced, for the record (the draft is over; nothing reads it)
    actual = SCR+'actual_keepers.csv'; dpull = _pull_at('20260907')
    if os.path.exists(actual) and dpull is not None:
        ka=_kadp(dpull, actual)
        rows=[]
        for pk,(wn,we) in TABLE.items():
            n,e=_solve(ka, pk)
            if (n,e)!=(wn,we): rows.append(f'{pk}: {wn}/{we} -> {n}/{e}')
        print(f'  post-lock, actual_keepers.csv on {os.path.basename(dpull)}: {[round(x,1) for x in ka]}')
        print('  rows the lock moved (information, not failures): ' + ('; '.join(rows) if rows else 'none'))

print(f'\n  {OK} ok, {FAIL} FAIL')
