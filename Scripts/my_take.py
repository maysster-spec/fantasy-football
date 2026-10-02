#!/usr/bin/env python3
r"""
my_take.py -- put YOUR OWN call on the live board.

    py my_take.py "Kyle Monangai" up "red zone work late last year, Swift is 27"
    py my_take.py "Bucky Irving" down "not paying that price"
    py my_take.py "Rome Odunze" clear          remove your take
    py my_take.py --list                        show every take you have made
    py my_take.py --file my_takes.csv           apply a whole sheet of takes at once

THE SHEET: three columns -- player, direction, note. direction is up / down / clear.
Blank direction rows and #comment rows are skipped, so you can leave the file lying around
half-filled. EVERY name is resolved against the board BEFORE anything is written: one typo and
nothing is applied, so the file can never leave you half-done at 7:50 PM.
`py my_take.py --file` with no name reads my_takes.csv next to this script.

Your take outranks every other mark on the row -- panels, podcasts, depth chart. It is your
draft. An UP take shows a gold **MINE** badge; a DOWN take shows a red **MINE** on the caution
side and silences any green. Hovering shows your own words back to you.

Doc 108. Writes to Scripts\live_draft\player_context.csv and re-pins check_kit.py, so a take
added at 7:40 PM still passes the file check at 7:55.
"""
import argparse, hashlib, os, re, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
CTX   = os.path.join(HERE, 'live_draft', 'player_context.csv')
BOARD = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
CHECK = os.path.join(HERE, 'check_kit.py')


def resolve(name, board):
    exact = board[board.player.str.lower() == name.lower()]
    if len(exact) == 1: return exact.iloc[0]
    part = board[board.player.str.lower().str.contains(name.lower(), regex=False)]
    if len(part) == 1: return part.iloc[0]
    if len(part) == 0:
        sys.exit(f"  no player matching '{name}' on the board. Check the spelling.")
    sys.exit("  '%s' matches %d players: %s\n  Be more specific."
             % (name, len(part), ', '.join(part.player.head(8))))


def repin():
    if not os.path.exists(CHECK): return
    d = open(CTX, 'rb').read().replace(b'\r\n', b'\n')
    s = open(CHECK, encoding='utf-8').read()
    new = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
    s2 = re.sub(r"(    'player_context\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                lambda m: m.group(1) + new, s, count=1)
    if s2 != s:
        open(CHECK, 'w', encoding='utf-8', newline='').write(s2)
        print(f"  re-pinned player_context.csv -> {new.strip('(),')}")


def apply_sheet(path, c, board):
    """Resolve EVERY row before writing ANY. All-or-nothing on purpose (doc 112)."""
    if not os.path.exists(path):
        sys.exit(f"  no such file: {path}")
    sheet = pd.read_csv(path, comment='#')
    cols = {c_.lower().strip(): c_ for c_ in sheet.columns}
    for need in ('player', 'direction'):
        if need not in cols:
            sys.exit(f"  {os.path.basename(path)} needs columns: player, direction, note "
                     f"-- found {list(sheet.columns)}")
    notecol = cols.get('note')
    plan, bad = [], []
    for i, r in sheet.iterrows():
        name = str(r[cols['player']]).strip()
        d    = str(r[cols['direction']]).strip().lower()
        if not name or name.lower() == 'nan': continue
        if d in ('', 'nan'): continue                      # left blank on purpose
        if d not in ('up', 'down', 'clear'):
            bad.append(f"row {i+2}: direction '{d}' -- must be up, down or clear"); continue
        exact = board[board.player.str.lower() == name.lower()]
        part  = board[board.player.str.lower().str.contains(name.lower(), regex=False)]
        hit   = exact if len(exact) == 1 else part
        if len(hit) != 1:
            bad.append(f"row {i+2}: '{name}' matches {len(hit)} players"
                       + (f" ({', '.join(hit.player.head(5))})" if len(hit) else "")); continue
        note = '' if not notecol or str(r[notecol]) == 'nan' else str(r[notecol]).strip()
        plan.append((hit.iloc[0], d, note))
    if bad:
        print(f"  {len(bad)} problem(s) -- NOTHING was written:")
        for b in bad: print("   ", b)
        sys.exit(1)
    if not plan:
        sys.exit("  no usable rows (every direction was blank).")
    for row, d, note in plan:
        c = write_take(c, row, {'up': 1, 'down': -1, 'clear': 0}[d], note)
        print(f"  {'UP  ' if d=='up' else 'DOWN' if d=='down' else 'clr '}  "
              f"{row.player:<24} {note}")
    print(f"  {len(plan)} take(s) applied from {os.path.basename(path)}.")
    return c


def write_take(c, row, val, note):
    eid = int(row.espn_id)
    if eid in set(c.ESPN_ID):
        i = int(c.index[c.ESPN_ID == eid][0])
        c.loc[i, 'mine'] = val
        c.loc[i, 'mine_note'] = note
    else:
        blank = {col: '' for col in c.columns}
        blank.update(dict(ESPN_ID=eid, player=row.player, pos=row.pos, grade='', dart=0, buy=0,
                          resid=0.0, calls_up=0, calls_down=0, who='', why='',
                          mine=val, mine_note=note))
        c = pd.concat([c, pd.DataFrame([blank])], ignore_index=True)
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('player', nargs='?')
    ap.add_argument('direction', nargs='?', choices=['up', 'down', 'clear'])
    ap.add_argument('note', nargs='?', default='')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--file', nargs='?', const='my_takes.csv',
                    help='apply a whole sheet of takes (default my_takes.csv)')
    a = ap.parse_args()

    c = pd.read_csv(CTX)
    for col, dflt in (('mine', 0), ('mine_note', '')):
        if col not in c.columns: c[col] = dflt
    c['mine'] = c.mine.fillna(0).astype(int)
    c['mine_note'] = c.mine_note.fillna('')

    if a.list or (not a.player and not a.file):
        mine = c[c.mine != 0]
        if not len(mine):
            print("  no takes yet.  py my_take.py \"Player Name\" up \"why\"")
        else:
            print(f"  {len(mine)} take(s):")
            for _, r in mine.iterrows():
                print(f"    {'UP  ' if r.mine > 0 else 'DOWN'}  {r.player:<24} {r.mine_note}")
        return

    b = pd.read_csv(BOARD)

    if a.file:
        path = a.file if os.path.isabs(a.file) else os.path.join(HERE, a.file)
        c = apply_sheet(path, c, b)
        c.to_csv(CTX, index=False)
        repin()
        print("  Restart the live board (or it will pick it up on the next launch).")
        return

    row = resolve(a.player, b)
    val = {'up': 1, 'down': -1, 'clear': 0}[a.direction or 'up']
    c = write_take(c, row, val, a.note)

    c.to_csv(CTX, index=False)
    verb = {1: 'UP', -1: 'DOWN', 0: 'cleared'}[val]
    print(f"  {row.player} ({row.pos} {row.team_c}, goes at {row.eff_pick:.0f}) -> {verb}"
          + (f"  \"{a.note}\"" if a.note else ""))
    repin()
    print("  Restart the live board (or it will pick it up on the next launch).")


if __name__ == '__main__':
    main()
