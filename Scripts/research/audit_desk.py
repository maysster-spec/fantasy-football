"""Every numbered link on the desk must point at a document something regenerates.
doc 146 found two links pointing at documents that had stopped existing; doc 161 found two
pointing at documents nothing re-dates. This makes both a one-command check."""
import re, sys, os
# doc 209: HERE is Scripts\research, and BOTH files it reads live one level up in Scripts.
# So this guard raised FileNotFoundError on every run it was ever given -- which is why the
# BOARD_GRID and TIER_SHEET links it exists to catch were missing for four days. S0.2: a
# guard that has never been executed is not a guard, and a broken path makes one look like one.
HERE=os.path.dirname(os.path.abspath(__file__))
SCRIPTS=os.path.dirname(HERE) if os.path.basename(HERE).lower()=='research' else HERE
sd=open(os.path.join(SCRIPTS,'sync_desk_copies.py'),encoding='utf-8').read()
ms=open(os.path.join(SCRIPTS,'make_shortcuts.py'),encoding='utf-8').read()
docs=re.findall(r'\("[^"]+",\s*"([^"]+\.(?:pdf|html|xlsx))"\)',
                re.search(r'DOCS = \[(.*?)\n\]', sd, re.S).group(1))
links=re.findall(r'\("(\d+ - [^"]+\.url)",\s*"([^"]+)_"',
                 re.search(r'DOCS = \[(.*?)\n\]', ms, re.S).group(1))
made={os.path.splitext(f)[0] for f in docs}
print('  sync_desk_copies.py re-dates:', ', '.join(sorted(made)))
bad=0
for url,pref in links:
    ok = pref in made; bad += (not ok)
    print(f'  {"ok  " if ok else "STALE"} {url:<34} -> {pref}_*.pdf')
extra = made - {p for _,p in links}
if extra: print(f'  note  re-dated but not linked from the desk: {", ".join(sorted(extra))}')
print(f'\n  {"PASS" if not bad else f"FAIL: {bad} link(s) point at a document nothing re-dates"}')
sys.exit(1 if bad else 0)
