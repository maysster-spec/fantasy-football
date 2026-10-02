#!/usr/bin/env python3
r"""
delta_gaps.py -- WHERE OUR BOARD DISAGREES WITH THE MARKET AND NOBODY HAS EXPLAINED WHY.

    py delta_gaps.py              print the list
    py delta_gaps.py --prompt     also write ..\Source\GEMINI_DELTA_TAKES.txt
    py delta_gaps.py --wide       write ..\Source\GEMINI_WIDE_TAKES.txt instead: the players
                                  inside reach with NO analyst coverage at all, nearest his picks
                                  first, and no restriction on whose opinion counts

Doc 114.  Matt asked whether we need more analyst takes on the deltas.  Yes -- and this finds
which ones, instead of scraping everything again.

WHAT THIS IS NOT.  Directive 4.13 RETIRED "the market is sleeping on him" (ADP rank minus
projection rank) as a PREDICTIVE signal: tested on 324 player-seasons it was the WORST of three,
rho -0.079, and its coldest quintile broke out at 3.1% against a base rate near 11%.  **Nothing
here says a big delta is a good pick.**  This is a COVERAGE question: where our board and the
market disagree most, do we hold any human explanation of the disagreement?  A gap here means we
are taking a position we cannot articulate -- which is worth ten minutes of reading, not a pick.

The delta MUST be residualised.  Raw, it is dominated by two artifacts:
  POSITION -- 4.4 measures our board at QB +15.7 and TE +18.0 against FantasyPros ECR by
              construction, so every QB and TE looks like a disagreement and none of them is one.
  BAND     -- rank differences grow with ADP simply because the ranks spread out down the board.
Both are removed by demeaning within position x ADP band, the same correction the analyst
residual already uses.

Reads: live_draft\board_v8_fixed.csv, analyst_calls_joined.csv
"""
import argparse, os, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.normpath(os.path.join(HERE, '..', 'Source'))
BOARD = os.path.join(HERE, 'live_draft', 'board_v8_fixed.csv')
CALLS = os.path.join(HERE, 'analyst_calls_joined.csv')
REACH = 155          # eff_pick -- past this you are not picking anybody (4.14)
TOPN  = 10


def build():
    b = pd.read_csv(BOARD)
    s = b[(b.eff_pick <= REACH) & (b.pos.isin(['QB', 'RB', 'WR', 'TE']))
          & (b.proj_leaguepts > 0)].copy()      # proj 0 = a news override, not a disagreement
    s['raw'] = s.adp_pick.rank() - s.vbd.rank(ascending=False)
    s['band'] = pd.cut(s.adp_pick, [0, 24, 48, 84, 120, 160], labels=False)
    s['resid'] = s.raw - s.groupby(['pos', 'band']).raw.transform('mean')
    covered = set(pd.read_csv(CALLS).player) if os.path.exists(CALLS) else set()
    s['in_corpus'] = s.player.isin(covered)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prompt', action='store_true')
    ap.add_argument('--wide', action='store_true',
                    help='breadth pass: every uncovered player inside reach, nearest his picks first')
    ap.add_argument('--n', type=int, default=40, help='how many players in the --wide prompt')
    a = ap.parse_args()
    s = build()
    if a.wide:
        return wide(s, a.n)
    print(f"  population inside eff_pick {REACH}: {len(s)}   with any analyst call: {int(s.in_corpus.sum())}")
    print(f"  raw delta by position (the artifact this removes): "
          f"{ {k: round(v,1) for k,v in s.groupby('pos').raw.mean().items()} }")
    picks = []
    for lab, sub in (('WE rate him ABOVE the market', s.nlargest(25, 'resid')),
                     ('the MARKET rates him above US', s.nsmallest(25, 'resid'))):
        gap = sub[~sub.in_corpus].head(TOPN)
        picks.append((lab, gap))
        print(f"\n  {lab} -- and no analyst call on file")
        for _, r in gap.iterrows():
            print(f"    {r.player:<24}{r.pos:<4}{r.team_c:<4} goes at {r.eff_pick:>6.1f}   "
                  f"vbd {r.vbd:>7.1f}   delta {r.resid:>+6.1f}")
    if not a.prompt: 
        print("\n  (add --prompt to write the Gemini tasking file)")
        return
    lines = []
    for lab, gap in picks:
        lines.append(f"\n--- {lab.upper()} ---")
        for _, r in gap.iterrows():
            lines.append(f"{r.player} | {r.pos} | {r.team_c} | drafted around overall {r.eff_pick:.0f}")
    body = '\n'.join(lines)
    txt = f"""GEMINI — ANALYST OPINION SWEEP ON 20 SPECIFIC PLAYERS
Prepared {pd.Timestamp.now():%Y-%m-%d}. Draft is 2026-09-07. Half PPR, 6-point passing TDs.

USE DEEP RESEARCH WITH LIVE WEB SEARCH. Do not run this against a fixed set of attached
documents -- everything I need was published in the last six weeks.

WHY THESE TWENTY. My own projections and the draft market disagree about each of these players
by more than can be explained by position or by where they go in the draft, AND I have no analyst
commentary on file explaining the disagreement. I am not asking whether they are good picks. I am
asking WHAT THE ARGUMENT IS, on both sides, so I know what I am betting against.

FOR EACH PLAYER, IN THIS ORDER:
  1. The bull case, in one or two sentences, as its actual advocates put it.
  2. The bear case, the same way.
  3. Which side the weight of 2026 preseason commentary is on, and how lopsided.
  4. ONE verbatim quote for each side where you can find one, with the analyst's name, the outlet
     or show, the date, and the URL. If you cannot find a real quote for a side, write NONE FOUND.
     Do not paraphrase into quotation marks and do not attribute a line to someone who did not
     say it -- a previous sweep did both and every claim had to be thrown out.
  5. Anything CONCRETE that changed in the last six weeks: role, depth chart, scheme, coaching
     comment, injury, contract.

FORMAT: one short block per player under a heading with his name. No preamble, no summary
section, no ranking them against each other.

TWO NOTES ON WHO COUNTS. I follow the Fantasy Footballers, Justin Boone, Matt Harmon,
FantasyLife, JJ Zachariason, Ben Gretch, Chris Raybon and Rob Waziak -- quote them where they
have spoken. But that is a list of who I happen to read, NOT a quality ranking, and I have no
evidence any of them is better than anyone else. If a stronger case is made by somebody I have
never heard of, give me that one and name them.

{body}
"""
    dest = os.path.join(SRC, 'GEMINI_DELTA_TAKES.txt')
    open(dest, 'w', encoding='utf-8').write(txt)
    print(f"\n  wrote {dest}  ({len(txt):,} chars, {sum(len(g) for _,g in picks)} players)")


PICKS = [8, 17, 32, 41, 56, 65, 80, 89, 104, 113, 128, 137]


def wide(s, n):
    """Doc 114 (the coverage-not-quality argument).  The delta pass asks about 20 players we DISAGREE with the market on.  This asks
    about the ones nobody has said anything about at all -- 85 of 142 inside reach -- ordered by
    how close they land to one of Matt's actual picks, because a player he cannot reach is not
    worth an analyst's paragraph.

    It deliberately does NOT name any analyst.  The eight shows in the first corpus are the ones
    Matt happens to follow; 4.13d is explicit that nothing in this project can rank analysts on
    skill, so a narrow list is a coverage decision that has been quietly acting like a filter."""
    un = s[~s.in_corpus].copy()
    un['near'] = un.eff_pick.map(lambda e: min(abs(e - p) for p in PICKS))
    un = un.sort_values('near').head(n)
    print(f"  {int((~s.in_corpus).sum())} players inside reach carry NO analyst call.")
    print(f"  taking the {len(un)} nearest one of his picks:\n")
    for _, r in un.iterrows():
        print(f"    {r.player:<24}{r.pos:<4}{r.team_c:<4} goes at {r.eff_pick:>6.1f}   vbd {r.vbd:>7.1f}")
    body = '\n'.join(f"{r.player} | {r.pos} | {r.team_c} | drafted around overall {r.eff_pick:.0f}"
                      for _, r in un.iterrows())
    txt = f"""GEMINI - ANALYST OPINION SWEEP, BREADTH PASS ({len(un)} PLAYERS)
Prepared {pd.Timestamp.now():%Y-%m-%d}. Draft 2026-09-07. 12-team, half PPR, 6-point passing TDs,
one QB, two RB, two WR, one TE, one FLEX (RB/WR/TE).

USE DEEP RESEARCH WITH LIVE WEB SEARCH. Start clean with no documents attached.

WHY THESE PLAYERS. I have analyst commentary on file for some of my draft board and none at all
for these. This is a hole in what I have read, not a judgement about the players. I want a short,
honest read on each so that I am not making a pick in silence.

CAST WIDE ON WHO COUNTS. Do not restrict yourself to the biggest fantasy shows. National analysts,
beat writers who cover the team every day, team-site reporters, respected independents, and people
with no following at all are all fair game, and the beat writer is often better than the panel on
exactly the questions I am asking. Name whoever you quote and where they said it. If the strongest
opinion on a player comes from someone obscure, that is the one I want.

FOR EACH PLAYER, KEEP IT SHORT - four lines, no essay:
  BULL: the best case anyone is actually making, one sentence.
  BEAR: the best case against, one sentence.
  LEAN: which way the weight of 2026 preseason commentary points, and how lopsided
        (one of: strongly bull / lean bull / genuinely split / lean bear / strongly bear).
  QUOTE: one verbatim line from a named person with the outlet and date and URL.
         Write NONE FOUND if you do not have a real one. Do NOT paraphrase inside quotation
         marks and do NOT attribute a line to someone who did not say it - a previous sweep of
         mine did both and every claim in it had to be thrown away.

Also flag, in one line under the player, anything CONCRETE and recent: a role change, a depth-chart
move, a scheme or coaching change, a contract situation, a trade that changed his target share.
Injuries I already have separately - skip them unless the injury changed his role.

FORMAT: one block per player under a heading with his name, in the order given below. No opening
summary, no closing summary, no ranking them against each other.

THE PLAYERS
{body}
"""
    dest = os.path.join(SRC, 'GEMINI_WIDE_TAKES.txt')
    open(dest, 'w', encoding='utf-8').write(txt)
    print(f"\n  wrote {dest}  ({len(txt):,} chars)")


if __name__ == '__main__':
    main()
