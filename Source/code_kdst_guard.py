#!/usr/bin/env python3
"""
code_kdst_guard.py — the single place K and D/ST are handled. Import this; do not re-implement.

WHY THIS FILE EXISTS
--------------------
K and D/ST have caused SIX separate defects in this project, all with the same root cause and
all found separately:
  C3   join on team name ("Houston Texans" vs "Texans D/ST") dropped all 32 D/ST, 29 hard-set to 50.0
  4.9  ESPN ADP unusable for K/DST (field-minus-ESPN median K +55.0, D/ST +33.2) -> Aubrey keeper error
  D3   19 of 44 kickers shipped as stale v2_carryover
  RT-1 greedy VBD policy drafted K/DST at median pick 75; cost 105.6 pts/manager-season (doc 41)
  A11  a validity gate keyed on the offensive SCORING map nulled 100% of K and D/ST actuals
  --   the v5 spine ranks Broncos D/ST 41st overall, ahead of Drake Maye and Tetairoa McMillan

ROOT CAUSE, STATED ONCE
-----------------------
Replacement level is computed as "Nth best of the position pool" for every position. That means
something completely different for K/DST than for skill positions, because the pools differ by
an order of magnitude:

    RB30   = 30th of 116 candidates -> bottom quartile of the pool  -> a genuinely replaceable RB
    D/ST12 = 12th of  32 candidates -> top THIRD of the pool        -> an above-average defense

Comparing the best defense to an above-average defense yields a large positive VBD (+32.5), which
then competes with round-4 skill players. But finding 4.8 establishes that 11-12 of 12 teams stream
a D/ST every season and 18-28 distinct kickers are added per year -- so the true replacement for a
streamed position is "the best one freely available on waivers", which is at or near the top of the
pool, making the realizable draft-day VBD approximately ZERO.

THE FIX
-------
Do not compute cross-position VBD for K and D/ST at all. Their draft-day VBD is not a small number,
it is an undefined one. Set it to NaN so any consumer that tries to rank them cross-position fails
loudly instead of silently placing a kicker 51st. Select them only at their designated picks.

USAGE
-----
    from code_kdst_guard import STREAMED, apply_kdst_guard, assert_no_kdst_before, KDST_DEADLINE
    spine = apply_kdst_guard(spine)                  # after computing vbd, before any ranking
    assert_no_kdst_before(picks_df, KDST_DEADLINE)   # after any simulated or backtest draft
"""
import pandas as pd

# The one definition. Every consumer imports this rather than writing {'K','D/ST'} inline.
STREAMED = frozenset({'K', 'D/ST'})

# Directive 4.7: league median first D/ST is round 12 (IQR 11-13); 95.8% of team-seasons take
# their first K at round 11+. Round 11 starts at overall pick 121. Doc 41 RT-2 swept this and
# found the result flat from round 10 onward, so it is not a knife-edge constant.
KDST_DEADLINE = 121

# Matt's designated slots (directive 2.1b): D/ST at 152, K at 161.
KDST_PICKS = {'D/ST': 152, 'K': 161}


def apply_kdst_guard(df, pos_col='pos', vbd_col='vbd'):
    """Null the cross-position VBD for streamed positions. Returns a copy.

    This is deliberately destructive: a NaN propagates into any sort/rank and shows up, whereas
    a plausible-looking +32.5 does not. See ERROR_PATTERNS B2 -- never default to a value inside
    the plausible range.
    """
    out = df.copy()
    mask = out[pos_col].isin(STREAMED)
    out.loc[mask, vbd_col] = pd.NA
    out['kdst_streamed'] = mask          # explicit provenance flag, per B5
    return out


def skill_only(df, pos_col='pos'):
    """The board a cross-position ranking should actually use."""
    return df[~df[pos_col].isin(STREAMED)]


def assert_no_kdst_before(picks, deadline=KDST_DEADLINE, pos_col='pos', pick_col='pick'):
    """Fail loudly if any simulated/backtested draft took a K or D/ST too early.

    Call this on the OUTPUT of any policy. This is the assertion whose absence let the
    doc-40 result ship: the policy was taking defenses at pick 49 and nothing objected.
    """
    bad = picks[picks[pos_col].isin(STREAMED) & (picks[pick_col] < deadline)]
    if len(bad):
        raise AssertionError(
            f"{len(bad)} K/D-ST selections before pick {deadline} "
            f"(earliest {int(bad[pick_col].min())}). Directive 4.7/4.8: this value is not "
            f"realizable. Median offending pick {bad[pick_col].median():.0f}."
        )
    return True


def assert_kdst_pool_intact(df, pos_col='pos', proj_col='proj_leaguepts'):
    """Catch a recurrence of C3 (name-join dropping defenses) and D3 (stale constant fills).

    code_integrity.py currently asserts a D/ST coverage threshold of 20, which the historical
    C3 defect (29 surviving rows) PASSES. There are exactly 32 NFL defenses; the threshold is 32.
    """
    problems = []
    n_dst = int((df[pos_col] == 'D/ST').sum())
    if n_dst != 32:
        problems.append(f"D/ST count is {n_dst}, expected exactly 32 (C3 name-join failure)")
    for pos in sorted(STREAMED):
        v = df.loc[df[pos_col] == pos, proj_col].dropna()
        if len(v) and v.nunique() == 1:
            problems.append(f"all {len(v)} {pos} projections are the identical value {v.iloc[0]} "
                            f"(stale constant fill -- see C3/D3)")
    if problems:
        raise AssertionError("; ".join(problems))
    return True
