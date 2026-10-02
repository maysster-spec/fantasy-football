#!/usr/bin/env python3
r"""
context_audit.py -- audit the NEWS on the board, not the numbers.

    py context_audit.py              the report
    py context_audit.py --days 4     change the staleness bar (default 4)

WHY THIS EXISTS (doc 166/167). `board_audit.py` checks the arithmetic; `audit_directive.py`
checks the directive. NOTHING checked the prose -- and the prose is what Matt reads at 60
seconds a pick. Two contaminations have now been found by hand:

  * Kenneth Walker III  -- his ankle claim was sourced to an article about Kenyon Sadiq.
    Caught by a previous session and annotated in the card itself.
  * Puka Nacua          -- carried Jordan Addison's DUI discipline, from an aggregator page
    whose headline was the QUESTION "is Puka Nacua suspended NFL week 1". Caught by MATT,
    reading his own board and googling it. That is one too many caught by the user.

So: four mechanical checks over `player_context.csv`, joined to the board, reported BY THE PICK
THEY AFFECT. None of them can prove a claim true -- they find the shapes that were wrong before.

  1. STALE      a judgement (AVOID/DISCOUNT) whose newest date is older than --days.
  2. UNDATED    a judgement carrying no date at all.
  3. CROSS-NAME a card whose text names a DIFFERENT player on the board. Usually innocent
                ("listed alongside Bucky Irving") -- but it is exactly how both contaminations
                read, so it is listed for the eye, not auto-failed.
  4. RISK CLAIM any mention of suspension / discipline / arrest / legal / exempt. doc 166's
                rule: those need TWO independent primary reports, and a headline phrased as a
                question is not one of them.

Standard library + pandas only, paths resolved against this file (SS0.4 v6.8).
"""
import argparse, os, re, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, 'live_draft')
BOARD = os.path.join(KIT, 'board_v8_fixed.csv')
CTX = os.path.join(KIT, 'player_context.csv')
MY_PICKS = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137]

# Words that are BADGE VOCABULARY, not player names. Without this the cross-name check
# reports every card carrying a DART badge, because Jaxson Dart is on the board.
BADGE_WORDS = {'Dart', 'Love', 'Brown', 'Jones', 'Smith', 'Williams', 'Warren', 'Hunter',
               'Price', 'Wilson', 'Moore', 'Allen', 'Johnson', 'Taylor', 'Harris', 'Mason'}
RISK = re.compile(r'suspend|disciplin|arrest|\blegal\b|exempt|charged|police|\bDUI\b', re.I)
DATE = re.compile(r'(20\d\d-\d\d-\d\d)')


def load():
    b = pd.read_csv(BOARD)
    c = pd.read_csv(CTX)
    key = 'ESPN_ID' if 'ESPN_ID' in c.columns else 'espn_id'
    return b.merge(c.drop(columns=[x for x in ('player', 'pos') if x in c.columns]),
                   left_on='espn_id', right_on=key, how='left')


def surnames(b):
    out = {}
    for p in b.player.astype(str):
        parts = p.split()
        if len(parts) < 2:
            continue
        s = re.sub(r'\b(Jr|Sr|II|III|IV|V)\.?$', '', parts[-1]).strip()
        if len(s) > 3 and s not in BADGE_WORDS:
            out.setdefault(s, set()).add(p)
    return out


def turn_for(adp):
    """Which of Matt's turns is this player's price nearest to?"""
    return min(MY_PICKS, key=lambda p: abs(p - adp))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=4,
                    help='a judgement older than this many days is STALE (default 4)')
    a = ap.parse_args()
    for p in (BOARD, CTX):
        if not os.path.exists(p):
            sys.exit(f'missing {p}')
    m = load()
    sur = surnames(m)
    today = pd.Timestamp.today().normalize()

    rows = []
    for _, r in m[m.why.notna() & (m.adp_pick < 168)].iterrows():
        w = re.sub(r'\s+', ' ', str(r.why))
        grade = str(r.get('grade') or '')
        dates = [pd.Timestamp(d) for d in DATE.findall(w)]
        # NEWS dd-mm stamps carry no year; treat them as this year
        for mm, dd in re.findall(r'NEWS (\d\d)-(\d\d)', w):
            dates.append(pd.Timestamp(year=today.year, month=int(mm), day=int(dd)))
        newest = max(dates) if dates else None
        flags = []
        if grade in ('AVOID', 'DISCOUNT'):
            if newest is None:
                flags.append('UNDATED')
            elif (today - newest).days > a.days:
                flags.append('STALE %dd' % (today - newest).days)
        if RISK.search(w):
            flags.append('RISK CLAIM')
        hits = sorted({s for s, names in sur.items()
                       if s not in str(r.player) and re.search(r'\b%s\b' % re.escape(s), w)})
        if hits:
            flags.append('names ' + ', '.join(hits[:3]))
        if flags:
            rows.append((turn_for(r.adp_pick), r.adp_pick, r.player, r.pos, grade, flags, w))

    print('=' * 78)
    print('  CONTEXT AUDIT -- the NEWS on the board, by the pick it affects')
    print('  %d of %d cards inside adp<168 raise something. Nothing here is proof of an error.'
          % (len(rows), int((m.adp_pick < 168).sum())))
    print('=' * 78)
    risk = [x for x in rows if any('RISK' in f for f in x[5])]
    if risk:
        print('\n  *** RISK CLAIMS -- need TWO independent primary reports (doc 166) ***')
        for _, adp, pl, pos, g, f, w in risk:
            print('    %-24s adp %6.1f  %s' % (pl[:24], adp, w[:110]))
    for pk in MY_PICKS:
        here = [x for x in rows if x[0] == pk]
        if not here:
            continue
        print('\n  PICK %d' % pk)
        for _, adp, pl, pos, g, f, w in sorted(here, key=lambda x: x[1]):
            print('    %-24s %-3s adp %6.1f  %-8s  %s' % (pl[:24], pos, adp, g, ' | '.join(f)))
    print('\n  STALE means the newest dated line on that card is older than %d days --' % a.days)
    print('  it does NOT mean the claim is wrong. Week-1 practice reports do not publish')
    print('  until game week, so beat reporting is the only source before the draft.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
