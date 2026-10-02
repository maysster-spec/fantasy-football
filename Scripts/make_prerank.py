#!/usr/bin/env python3
r"""
make_prerank.py -- build ESPN_prerank_with_ids.csv so it does not REACH.

    py make_prerank.py             audit: show what would move, write nothing
    py make_prerank.py --write     rebuild the file (archives the old one first)
    py make_prerank.py --slack 8   how far ahead of his own ADP a player may be listed

Doc 126. Matt, after a mock: "Stafford and Warren were listed on the ESPN board as best player
available. Makes me wonder about our preranking."

He was right. The prerank was a **pure VBD sort, monotone, with no roster or market logic at all**
-- and ESPN's "best player available" in the draft room reads YOUR custom rankings, so that flat
list is what the draft room was recommending to him all night.

    prerank #36  Tyler Warren     TE  vbd 28.1   ADP 49.5
    prerank #40  Matthew Stafford QB  vbd 21.2   ADP **79.8**
    prerank #41  Bucky Irving     RB  vbd 20.0   ADP 54.5

Stafford is listed FORTY PLACES ahead of where the market takes him. Following that list means
paying pick ~40 for a player available at ~80 and losing whoever was on the board in between.
That is not a projection error -- the VBD is right -- it is that **a value ranking is not a draft
order.** Directive 4.4 measures this board at **QB +15.7 and TE +18.0 against consensus**, so a
naked VBD sort front-loads exactly those two positions by construction, which is precisely the two
positions Matt was being offered.

THE RULE, and why this one and not something cleverer:
  A player may not be listed more than `slack` slots ahead of his own ADP.
  If he will still be there later, taking him now costs you the player you could have had -- which
  is the live engine's own `cost vs #1` idea, applied statically.
This deliberately does NOT try to predict anything. Directive 4.13 RETIRED ADP-minus-projection as
a predictive signal (rho -0.079, the worst of three tested). ADP is used here only as a PRICE --
when you can get him -- never as an opinion about how good he is. VBD still decides who is better;
ADP only stops you paying early for it.

K and D/ST keep their existing treatment (4.9: ESPN ADP is broken for both).

Reads:  live_draft\board_v8_fixed.csv  (+ the current prerank, for the diff)
Writes: live_draft\ESPN_prerank_with_ids.csv, old copy to ..\_archive\, re-pins check_kit.
AFTER WRITING you must RE-INJECT it to ESPN -- this file alone changes nothing in the draft room.
"""
import argparse, datetime as dt, hashlib, os, re, shutil, sys
import pandas as pd

HERE  = os.path.dirname(os.path.abspath(__file__))
KIT   = os.path.join(HERE, 'live_draft')
ARCH  = os.path.normpath(os.path.join(HERE, '..', '_archive'))
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
OUT   = os.path.join(KIT, 'ESPN_prerank_with_ids.csv')
CHECK = os.path.join(HERE, 'check_kit.py')
SENTINEL = 168          # past this ESPN's ADP is a fabricated blob (4.14) -- do not price on it


def build(slack):
    b = pd.read_csv(BOARD).copy()
    b['vbd'] = pd.to_numeric(b.vbd, errors='coerce').fillna(-999)
    b['adp_pick'] = pd.to_numeric(b.adp_pick, errors='coerce')
    b = b.sort_values('vbd', ascending=False).reset_index(drop=True)
    b['vbd_slot'] = b.index + 1                       # where a naked VBD sort would put him

    # PRICE FLOOR: the earliest slot he may occupy. Inside the real-ADP region that is his ADP
    # minus the slack; in the sentinel blob there is no real price, so VBD stands alone.
    floor = (b.adp_pick - slack).where(b.adp_pick < SENTINEL, other=0).fillna(0)
    b['floor'] = floor.clip(lower=0)
    # K and D/ST are not priced by ESPN ADP at all (4.9) -- leave them on VBD order.
    b.loc[b.pos.isin(['K', 'D/ST']), 'floor'] = 0

    # order by "the later of what he is worth and what he costs", VBD breaking ties
    b['key'] = b[['vbd_slot', 'floor']].max(axis=1)
    out = b.sort_values(['key', 'vbd'], ascending=[True, False]).reset_index(drop=True)
    out['prerank'] = out.index + 1
    out['moved'] = out.prerank - out.vbd_slot
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--slack', type=int, default=8,
                    help='slots a player may be listed ahead of his ADP (default 8)')
    ap.add_argument('--top', type=int, default=120, help='rows to report on')
    a = ap.parse_args()

    new = build(a.slack).rename(columns={'espn_id': 'ESPN_ID'})
    print(f"  slack = {a.slack} slots ahead of ADP\n")
    big = new[(new.moved.abs() >= 6) & (new.prerank <= a.top)]
    print(f"  {len(big)} players inside the top {a.top} move 6+ slots:\n")
    print(f"  {'was':>4}{'now':>5}  {'player':<24}{'pos':<5}{'vbd':>7}{'adp':>7}  why")
    for _, r in big.sort_values('prerank').iterrows():
        why = 'was listed ahead of his price' if r.moved > 0 else 'rises as others drop back'
        print(f"  {r.vbd_slot:>4}{r.prerank:>5}  {r.player:<24}{r.pos:<5}{r.vbd:>7.0f}"
              f"{(r.adp_pick if pd.notna(r.adp_pick) else 0):>7.0f}  {why}")

    pos_top = new[new.prerank <= 60].pos.value_counts().to_dict()
    print(f"\n  position mix in the new top 60: {pos_top}")
    if os.path.exists(OUT):
        old = pd.read_csv(OUT)
        j = old[['ESPN_ID', 'prerank']].merge(
            new[['ESPN_ID', 'prerank']], on='ESPN_ID', suffixes=('_old', '_new'))
        print(f"  rows in common with the current file: {len(j)} of {len(old)}; "
              f"median |move| = {(j.prerank_new - j.prerank_old).abs().median():.0f}")

    if not a.write:
        print("\n  AUDIT ONLY -- nothing written. Re-run with --write to rebuild the file.")
        return

    cols = [c for c in ('prerank', 'ESPN_ID', 'player', 'pos', 'team_c', 'bye', 'vbd', 'adp_pick')
            if c in new.columns]
    missing = [c for c in ('prerank', 'ESPN_ID', 'player') if c not in cols]
    if missing:
        sys.exit(f"  REFUSING TO WRITE: the rebuilt frame has no {missing}. "
                 f"columns present: {list(new.columns)}")
    keep = new[cols]
    # The board holds skill players only. The SHIPPED prerank also carries 32 D/ST and 32 K at
    # the tail (481-544), which the board has never contained -- and a rebuild that dropped them
    # would hand ESPN a 480-row list and let it autodraft a kicker of its own choosing. They keep
    # their existing order: 4.9 records that ESPN's ADP is broken for both, so there is nothing
    # here to re-price them with.
    if os.path.exists(OUT):
        prev = pd.read_csv(OUT)
        tail = prev[~prev.ESPN_ID.isin(set(keep.ESPN_ID))].sort_values('prerank')
        if len(tail):
            tail = tail[[c for c in keep.columns if c in tail.columns]].copy()
            for c in keep.columns:
                if c not in tail.columns: tail[c] = pd.NA
            tail = tail[keep.columns]
            keep = pd.concat([keep, tail], ignore_index=True)
            keep['prerank'] = range(1, len(keep) + 1)
            print(f"  carried {len(tail)} non-board rows (K and D/ST) through to the tail")
    if len(keep) < len(pd.read_csv(OUT)) if os.path.exists(OUT) else False:
        sys.exit("  REFUSING TO WRITE: the rebuilt list is SHORTER than the shipped one.")
    if os.path.exists(OUT):
        os.makedirs(ARCH, exist_ok=True)
        shutil.copy2(OUT, os.path.join(ARCH, f"ESPN_prerank_with_ids_{dt.datetime.now():%Y%m%d_%H%M}.csv"))
    keep.to_csv(OUT, index=False)
    print(f"\n  wrote {OUT}  ({len(keep)} rows)")
    try:
        d = open(OUT, 'rb').read().replace(b'\r\n', b'\n')
        cs = open(CHECK, encoding='utf-8').read()
        newpin = f"({len(d)}, '{hashlib.sha256(d).hexdigest()[:16]}'),"
        cs2 = re.sub(r"(    'ESPN_prerank_with_ids\.csv':\s+)\(\d+, '[0-9a-f]{16}'\),",
                     lambda m: m.group(1) + newpin, cs, count=1)
        if cs2 != cs:
            open(CHECK, 'w', encoding='utf-8', newline='').write(cs2)
            print(f"  re-pinned -> {newpin.strip('(),')}")
    except Exception as e:
        print(f"  (could not re-pin: {e})")
    print("\n  ** THIS CHANGES NOTHING IN THE DRAFT ROOM UNTIL YOU RE-INJECT IT. **")
    print("  Then  py verify_prerank.py  to read back what ESPN actually stored.")


if __name__ == '__main__':
    main()
