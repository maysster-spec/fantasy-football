#!/usr/bin/env python3
r"""
parse_takes.py -- turn the Gemini analyst sweeps into one machine-readable file.

    py parse_takes.py ..\10_Gemni\*.md            audit
    py parse_takes.py ..\10_Gemni\*.md --write    write analyst_takes.csv

Doc 116. Two sweeps came back in two different shapes -- the breadth pass used the four labels it
was asked for (BULL/BEAR/LEAN/QUOTE), the delta pass wrote prose. This reads BOTH and emits one
table: player, lean, bull, bear, quote, source, concrete.

It never invents a lean. If a block has no recognisable lean it is left blank, and a quote that
says NONE FOUND stays empty rather than being filled from the prose -- the whole point of that
instruction was to make an absent quote visible.
"""
import argparse, glob, os, re, sys
import pandas as pd

LEANS = ['strongly bull', 'lean bull', 'genuinely split', 'lean bear', 'strongly bear']

def clean(t):
    t = re.sub(r'\\([\\`*_{}\[\]()#+\-.!])', r'\1', t)
    t = re.sub(r'\*\*|\*', '', t)
    t = re.sub(r'(?<=[a-zA-Z.,")])\d{1,3}(?=[\s.,;]|$)', '', t)   # gemini's footnote markers
    return re.sub(r'\s+', ' ', t).strip()

def blocks(path):
    txt = open(path, encoding='utf-8').read()
    parts = re.split(r'\n#{2,3} ', txt)
    for p in parts[1:]:
        head, _, body = p.partition('\n')
        head = clean(head)
        m = re.match(r'([^|]+)\|\s*([A-Z]{2})\s*\|\s*([A-Z]{2,3})', head)
        if not m: continue
        yield m.group(1).strip(), m.group(2), m.group(3), clean(body)

def field(body, label, nxt):
    m = re.search(rf'{label}:\s*(.*?)(?=\s(?:{nxt}):|$)', body)
    return m.group(1).strip() if m else ''

def parse(body):
    out = dict(bull='', bear='', lean='', quote='', source='', concrete='')
    if 'BULL:' in body:
        out['bull']  = field(body, 'BULL',  'BEAR|LEAN|QUOTE|CONCRETE')
        out['bear']  = field(body, 'BEAR',  'LEAN|QUOTE|CONCRETE')
        out['lean']  = field(body, 'LEAN',  'QUOTE|CONCRETE')
        out['quote'] = field(body, 'QUOTE', 'CONCRETE')
        out['concrete'] = field(body, 'CONCRETE', 'BULL')
    else:
        # the prose shape: mine the lean phrase and the first real quotation
        out['bull'] = body[:400]
    low = body.lower()
    hit = [L for L in LEANS if L in low]
    if hit and not out['lean']:
        out['lean'] = min(hit, key=lambda L: low.index(L))
    for L in LEANS:                       # normalise whatever landed in `lean`
        if L in out['lean'].lower(): out['lean'] = L; break
    else:
        out['lean'] = out['lean'] if out['lean'] in LEANS else ''
    q = re.search(r'"([^"]{25,})"', out['quote'] or body)
    if q and 'NONE FOUND' not in (out['quote'] or ''):
        out['quote'] = q.group(1).strip()
        tail = (out['quote'] and body.split(out['quote'], 1)[-1]) or ''
        u = re.search(r'(https?://\S+)', tail[:300])
        who = re.match(r'["\s]*[-–]\s*([^,\n]{3,60})', tail)
        out['source'] = ((who.group(1).strip() + ' ') if who else '') + (u.group(1).rstrip('.,') if u else '')
    else:
        out['quote'] = ''
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='+'); ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    rows = []
    for pat in a.files:
        for f in glob.glob(pat):
            n = 0
            for name, pos, tm, body in blocks(f):
                d = parse(body); d.update(player=name, pos=pos, tm=tm, src_file=os.path.basename(f))
                rows.append(d); n += 1
            print(f"  {os.path.basename(f)}: {n} player blocks")
    t = pd.DataFrame(rows).drop_duplicates('player', keep='first')
    print(f"\n  {len(t)} unique players")
    print(f"  with a LEAN : {int((t.lean != '').sum())}")
    print(f"  with a QUOTE: {int((t.quote != '').sum())}   (the rest said NONE FOUND, which is the honest answer)")
    print('\n  lean distribution:', t[t.lean != ''].lean.value_counts().to_dict())
    if a.write:
        here = os.path.dirname(os.path.abspath(__file__))
        dest = os.path.join(here, 'analyst_takes.csv')
        t.to_csv(dest, index=False); print(f"\n  wrote {dest}")
        stamp_context(here, t)
    else:
        print('\n  (add --write to save analyst_takes.csv)')

def stamp_context(here, t):
    """doc 117. The live board's player card needs bull/bear/lean/quote, and the kit is a fixed
    set of files -- so they ride in player_context.csv, the same channel depth_map.py uses for the
    backfield label. UPDATE ONLY: it writes six columns and asserts that nothing else moved,
    because Matt's own takes live in this file and a clobber at 7:50 PM is unrecoverable."""
    ctx = os.path.join(here, 'live_draft', 'player_context.csv')
    if not os.path.exists(ctx):
        print("  (no player_context.csv -- the card fields were not stamped)"); return
    pc = pd.read_csv(ctx); before = pc.copy()
    key = t.set_index('player')
    cols = {'bull': 'bull', 'bear': 'bear', 'lean': 'lean', 'quote': 'quote',
            'source': 'qsource', 'concrete': 'concrete'}
    for src, dst in cols.items():
        if dst not in pc.columns: pc[dst] = ''
        vals = pc.player.map(key[src]) if src in key.columns else None
        if vals is not None:
            pc[dst] = vals.where(vals.notna(), pc[dst]).fillna('')
    for c_ in before.columns:
        if c_ in cols.values(): continue
        if not before[c_].fillna('').astype(str).equals(pc[c_].fillna('').astype(str)):
            sys.exit(f"  REFUSING TO WRITE: column '{c_}' changed in player_context.csv")
    pc.to_csv(ctx, index=False)
    n = int((pc.bull.astype(str).str.strip() != '').sum())
    print(f"  stamped analyst fields into player_context.csv ({n} players carry a bull case)")
    try:
        import hashlib
        chk = os.path.join(here, 'check_kit.py')
        d = open(ctx, 'rb').read().replace(b'\r\n', b'\n')
        cs = open(chk, encoding='utf-8').read()
        new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
        cs2 = re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                     lambda m: m.group(1) + new, cs, count=1)
        if cs2 != cs:
            open(chk, 'w', encoding='utf-8', newline='').write(cs2)
            print(f"  re-pinned player_context.csv -> {new.strip('(),')}")
    except Exception as e:
        print(f"  (could not re-pin: {e})")


if __name__ == '__main__':
    main()
