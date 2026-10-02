#!/usr/bin/env python3
r"""
apply_research.py -- put DATED RESEARCH FACTS where the live board can see them.

    py apply_research.py                 show what would change (default, writes nothing)
    py apply_research.py --write         apply it

WHY THIS EXISTS.  The Gemini sweep came back with 23 dated, sourced facts about players who are
live at Matt's picks -- and there was nowhere for them to go.  `player_context.csv` is the ONLY
file the live board reads for player notes (doc 100), and every one of its note columns was
already owned by another pipeline: `why`/`concrete`/`bull`/`bear` by the analyst + injury sweep,
`job`/`job_ceil` by depth_map.py, `mine`/`mine_note` reserved for Matt.  A finding that lives in
a CSV nobody reads is not a finding.

WHAT IT DOES.  PREPENDS one segment to `why`, formatted `NEWS <date>: <fact>`, followed by ` || `.
live_draft.py splits `why` on `||` and renders the first segment as the row's STATUS/NOTE line and
the next two as extras -- so the new fact becomes the most prominent line on the card and NOTHING
that was there before is lost, it moves down one slot.  Verified by rendering, not by reading.

WHAT IT REFUSES TO DO.  It never adds a row, never changes grade / dart / buy / job / mine, and
exits non-zero if any column other than `why` differs after the write (depth_map.py's guard,
copied).  It is idempotent: a row that already carries the same NEWS segment is skipped, so
running it twice does not stack duplicates.
"""
import argparse, datetime as dt, hashlib, os, re, shutil, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, 'live_draft')
CTX  = os.path.join(KIT, 'player_context.csv')
CHK  = os.path.join(HERE, 'check_kit.py')
ARCH = os.path.normpath(os.path.join(HERE, '..', '_archive'))


def norm(s):
    """the project's canonical normaliser -- board_audit.py:111 / keeper_swap.py:32 (SS3)."""
    s = re.sub(r"\s+(Jr\.|Sr\.|II|III|IV|V)$", '', str(s).strip(), flags=re.I)
    return re.sub(r"[.'’-]", '', s).lower()


def fact_of(row):
    """one sentence, the most decision-relevant of the three columns. Health beats job beats role:
    a hurt starter is a different player; a healthy one whose ROLE grew is only a nudge."""
    for col in ('health', 'job', 'role'):
        v = row.get(col)
        if isinstance(v, str) and v.strip() and v.strip().lower() != 'nan':
            return ' '.join(v.split())[:200]
    return ''


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--findings', default=os.path.join(HERE, 'gemini_findings.csv'))
    ap.add_argument('--date', default=dt.date.today().isoformat()[5:])
    a = ap.parse_args(argv)

    g = pd.read_csv(a.findings)
    assert 'player' in g.columns, f'{a.findings} has no player column'
    pc = pd.read_csv(CTX)
    before = pc.copy()
    if 'why' not in pc.columns: sys.exit('  player_context.csv has no why column')
    pc['why'] = pc.why.fillna('').astype(str)
    key = {norm(p): i for i, p in enumerate(pc.player)}

    print('=' * 78)
    print(f"  DATED RESEARCH -> player_context.csv" + ('' if a.write else '   (dry run)'))
    print('=' * 78)
    hit = skip = miss = 0
    for _, r in g.iterrows():
        f = fact_of(r)
        if not f:
            continue
        i = key.get(norm(r.player))
        if i is None:
            print(f'  --  not on the context file: {r.player}'); miss += 1; continue
        seg = f'NEWS {a.date}: {f}'
        if seg in pc.at[i, 'why']:
            skip += 1; continue
        cur = pc.at[i, 'why']
        # RED TEAM, finding 2 (mine, before shipping): without this the script STACKS. Run it
        # again tomorrow with a new --date and the row carries two NEWS segments, the older one
        # renders as an extra, and the card shows a superseded fact next to the current one.
        # Drop any NEWS segment this script wrote before, whatever its date.
        parts = [x for x in cur.split('||') if not re.match(r'\s*NEWS \d\d-\d\d:', x)]
        # RED TEAM, finding 1: live_draft.py:903 drops a leading 'no injury news found' segment
        # ONLY when it is why[0]. Prepending pushes it to position 1, where that guard cannot see
        # it -- so 'no injury news found' would come BACK onto cards it had been cleaned off.
        # Do the same strip here, on the same condition (no grade, or NEUTRAL).
        gr = str(pc.at[i, 'grade'] or '').strip().upper()
        if parts and parts[0].strip().lower().startswith('no injury news found') \
                and gr in ('', 'NEUTRAL', 'NAN'):
            parts = parts[1:]
        pc.at[i, 'why'] = ' || '.join([seg] + [x.strip() for x in parts if x.strip()])
        print(f'  ->  {r.player:<24} {seg[:96]}')
        hit += 1
    print(f'\n  {hit} rows updated, {skip} already carried it, {miss} unmatched')

    for c in before.columns:
        if c == 'why': continue
        if not before[c].fillna('').astype(str).equals(pc[c].fillna('').astype(str)):
            sys.exit(f"  REFUSING TO WRITE: column '{c}' changed")
    if len(before) != len(pc):
        sys.exit('  REFUSING TO WRITE: row count changed')
    if not a.write:
        print('\n  nothing written. re-run with --write to apply.'); return 0
    os.makedirs(ARCH, exist_ok=True)
    shutil.copy(CTX, os.path.join(ARCH, f'player_context_{dt.date.today():%Y%m%d}.csv'))
    pc.to_csv(CTX, index=False)
    print(f'  written. old copy archived to _archive\\')
    try:
        d = open(CTX, 'rb').read().replace(b'\r\n', b'\n')
        cs = open(CHK, encoding='utf-8').read()
        new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
        cs2 = re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                     lambda m: m.group(1) + new, cs, count=1)
        if cs2 != cs:
            open(CHK, 'w', encoding='utf-8', newline='').write(cs2)
            print(f"  re-pinned player_context.csv -> {new.strip('(),')}")
        else:
            print('  !! could not find the pin line in check_kit.py -- run it and repin by hand')
    except Exception as e:
        print(f'  (could not re-pin: {e})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
