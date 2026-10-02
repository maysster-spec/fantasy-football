#!/usr/bin/env python3
r"""
import_injury_sweep.py -- load the Gemini injury sweep into the live board.

    py import_injury_sweep.py sweep.csv            audit only, writes nothing
    py import_injury_sweep.py sweep.csv --write    apply it

Doc 112/113.  The sweep exists because the injury sheet went stale: Kyle Monangai hyperextended
a knee on Aug 16 and our Aug 30 sheet did not mention it.  SILENCE was the failure, so this
script's first job is to REPORT WHAT THE SWEEP DID NOT COVER, not just load what it did.

What it writes: `grade` and `why` in live_draft\player_context.csv, nothing else.  It never
touches vbd, adp, dart, buy, analyst calls, or YOUR takes (mine / mine_note).  A player who is
OUT_SEASON / SUSPENDED / EXEMPT_LIST is NOT zeroed here -- that is apply_news.py's job and it is
deliberately a separate, deliberate act.  This script prints the apply_news rows for you instead.

CHECKS BEFORE IT WILL WRITE
  1. required columns present
  2. every player resolves to exactly one board row (by name; ambiguous = refuse)
  3. risk_grade is one of AVOID / DISCOUNT / NEUTRAL (blank allowed, means no change)
  4. a dated status must carry a source_url -- an undated or unsourced claim is DROPPED and named
  5. coverage report: which of the 143 shortlist players the sweep did not return a row for
  6. IT WILL NOT CLEAR AN EXISTING WARNING ON A WEAK SOURCE.  A sweep row that upgrades a player
     we already graded AVOID or DISCOUNT to NEUTRAL is REFUSED unless it is HIGH confidence AND
     dated within 14 days.  The Aug-31 sweep tried to make Jonathon Brooks NEUTRAL -- clearing a
     documented double-ACL -- on the strength of a July blog post about a Hall of Fame game.
     Downgrades always apply; only the all-clear has to earn it.
"""
import argparse, hashlib, os, re, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
CTX   = os.path.join(HERE, 'live_draft', 'player_context.csv')
BOARD = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
CHECK = os.path.join(HERE, 'check_kit.py')
NEED  = ['player', 'status_now', 'risk_grade', 'one_line']
GRADES = ('AVOID', 'DISCOUNT', 'NEUTRAL')
ZERO_STATUS = ('OUT_SEASON', 'SUSPENDED', 'EXEMPT_LIST')


def norm(s):
    s = re.sub(r'\b(jr|sr|ii|iii|iv|v)\b', '', str(s).lower())
    return re.sub(r'\s+', ' ', re.sub(r"[^a-z ]", '', s)).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sweep')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()

    if not os.path.exists(a.sweep): sys.exit(f"  no such file: {a.sweep}")
    s = pd.read_csv(a.sweep)
    s.columns = [c.strip().lower() for c in s.columns]
    missing = [c for c in NEED if c not in s.columns]
    if missing: sys.exit(f"  sweep is missing required column(s): {missing}\n  got: {list(s.columns)}")
    for opt in ('date_current', 'source_url_current', 'expected_games_2026', 'repeat_injury',
                'injury_history', 'confidence', 'injury_current'):
        if opt not in s.columns: s[opt] = ''
    s = s.fillna('')

    b = pd.read_csv(BOARD); b['k'] = b.player.map(norm)
    c = pd.read_csv(CTX)

    plan, dropped, unresolved, refused = [], [], [], []
    for i, r in s.iterrows():
        name = str(r.player).strip()
        if not name: continue
        hit = b[b.k == norm(name)]
        if len(hit) != 1:
            unresolved.append(f"row {i+2}: '{name}' -> {len(hit)} board matches"); continue
        row = hit.iloc[0]
        g = str(r.risk_grade).strip().upper()
        if g and g not in GRADES:
            dropped.append(f"row {i+2}: {name} -- risk_grade '{g}' is not one of {GRADES}"); continue
        st = str(r.status_now).strip().upper()
        if st and st != 'HEALTHY' and not str(r.source_url_current).strip():
            dropped.append(f"row {i+2}: {name} -- status '{st}' with NO source_url; not loading it")
            continue
        # GUARD 6: an all-clear must be recent and confident to overturn a standing warning.
        prior = ''
        pi = c.index[c.ESPN_ID == int(row.espn_id)]
        if len(pi): prior = str(c.loc[int(pi[0]), 'grade'] or '').strip().upper()
        if g == 'NEUTRAL' and prior in ('AVOID', 'DISCOUNT'):
            conf = str(r.confidence).strip().upper()
            dt = pd.to_datetime(str(r.date_current).strip(), errors='coerce')
            fresh = (dt is not pd.NaT) and dt == dt and \
                    (pd.Timestamp.now().normalize() - dt).days <= 14
            if not (conf == 'HIGH' and fresh):
                refused.append(f"{name}: sweep says NEUTRAL but we have {prior} -- "
                               f"confidence {conf or 'blank'}, dated {str(r.date_current) or 'never'}. "
                               f"Keeping {prior}, loading the note only.")
                g = ''            # keep our grade, still take the text
        bits = [x for x in (
            f"{st}" if st and st != 'HEALTHY' else '',
            str(r.injury_current).strip(),
            f"({str(r.date_current).strip()})" if str(r.date_current).strip() else '',
            str(r.one_line).strip(),
            f"history: {str(r.injury_history).strip()}" if str(r.injury_history).strip() else '',
            "REPEAT INJURY" if str(r.repeat_injury).strip().upper() == 'YES' else '',
            f"exp {str(r.expected_games_2026).strip()} gm" if str(r.expected_games_2026).strip() else '',
            f"[{str(r.confidence).strip().lower()} confidence]" if str(r.confidence).strip() else '',
        ) if x]
        plan.append((int(row.espn_id), row.player, row.pos, g, ' | '.join(bits), st))

    print(f"  sweep rows: {len(s)}   usable: {len(plan)}")
    if unresolved:
        print(f"  {len(unresolved)} UNRESOLVED NAME(S) -- nothing will be written for these:")
        for u in unresolved: print("   ", u)
    if dropped:
        print(f"  {len(dropped)} row(s) DROPPED:")
        for d in dropped: print("   ", d)
    if refused:
        print(f"  {len(refused)} ALL-CLEAR(S) REFUSED -- a weak source cannot clear a standing warning:")
        for x in refused: print("   ", x)

    # what the sweep did NOT cover -- the whole point
    covered = {p[0] for p in plan}
    short = b[(b.eff_pick <= 155) & (b.pos.isin(['QB', 'RB', 'WR', 'TE']))]
    gaps = short[~short.espn_id.isin(covered)]
    print(f"\n  COVERAGE: {len(short) - len(gaps)} of {len(short)} shortlist players returned a row.")
    if len(gaps):
        print(f"  {len(gaps)} NOT COVERED -- the sweep is silent on these, which is exactly the")
        print("  failure mode it was written to fix. Re-run the prompt on this list:")
        for _, g_ in gaps.head(40).iterrows():
            print(f"    {g_.player} ({g_.pos} {g_.team_c}, goes at {g_.eff_pick:.0f})")
        if len(gaps) > 40: print(f"    ... and {len(gaps)-40} more")

    zero = [p for p in plan if p[5] in ZERO_STATUS]
    if zero:
        print(f"\n  {len(zero)} player(s) are OUT for the season / suspended / exempt.")
        print("  This script does NOT zero them. Add these rows to news_overrides.csv and run")
        print("  py apply_news.py --write  -- removing a player from the board is a deliberate act:")
        for eid, name, pos, g, note, st in zero:
            print(f"    {eid},{name},out,{pd.Timestamp.now():%Y-%m-%d},\"{st} per the sweep\"")

    changed = [p for p in plan if p[3]]
    print(f"\n  {len(changed)} player(s) carry a risk_grade and would be written.")
    for eid, name, pos, g, note, st in changed[:25]:
        print(f"    {g:<9}{name:<24}{note[:80]}")
    if len(changed) > 25: print(f"    ... and {len(changed)-25} more")

    if not a.write:
        print("\n  AUDIT ONLY -- nothing written. Re-run with --write to apply.")
        return

    before = c.copy()
    for eid, name, pos, g, note, st in plan:
        i = c.index[c.ESPN_ID == eid]
        if len(i) == 0:
            blank = {col: '' for col in c.columns}
            blank.update(dict(ESPN_ID=eid, player=name, pos=pos, grade=g, dart=0, buy=0,
                              resid=0.0, calls_up=0, calls_down=0, who='', why=note))
            c = pd.concat([c, pd.DataFrame([blank])], ignore_index=True)
            continue
        i = int(i[0])
        if g: c.loc[i, 'grade'] = g
        if note: c.loc[i, 'why'] = note + ' || ' + str(c.loc[i, 'why'] or '')
    for col in ('mine', 'mine_note', 'dart', 'buy', 'calls_up', 'calls_down'):
        if col in before.columns and not before[col].fillna('').astype(str).equals(
                c.loc[:len(before)-1, col].fillna('').astype(str)):
            sys.exit(f"  REFUSING TO WRITE: column '{col}' changed")
    c.to_csv(CTX, index=False)
    print(f"\n  wrote {CTX}  ({len(c)} rows)")
    try:
        d = open(CTX, 'rb').read().replace(b'\r\n', b'\n')
        cs = open(CHECK, encoding='utf-8').read()
        new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
        cs2 = re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                     lambda m: m.group(1) + new, cs, count=1)
        if cs2 != cs:
            open(CHECK, 'w', encoding='utf-8', newline='').write(cs2)
            print(f"  re-pinned player_context.csv -> {new.strip('(),')}")
    except Exception as e:
        print(f"  (could not re-pin: {e})")
    print("\n  NOW REBUILD THE PAPER, or it disagrees with the screen:")
    print("      py make_board.py          (the grades tint rows and print the reason)")
    print("      .\\sync_desk_copies.bat    (dated copy to the 2026 desk)")
    print("  And restart the live board if it is running.")


if __name__ == '__main__':
    main()
