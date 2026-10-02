# 205 — The waiver scheme: what the four-year record already decides

*2026-09-06. Matt asked for a weekly waiver scheme and strategy. This is the measured foundation;
the scheme itself needs his actual roster and lands Tuesday.*

---

## 0. WHAT THE DATA ALREADY DECIDES

1. **Claim it. Never wait for it to clear to free agency.** A waiver claim hits at a higher rate
   than a free-agent add **at all four positions**, and gains more over the man dropped.
2. **The wire does not dry up.** Hit rate is flat all season — wk 1–3 **22.1%** vs wk 10–14
   **23.1%**, p=0.83. There is no "get in early" effect and no late-season desert.
3. **Priority costs nothing in this league.** §2: *waivers reset weekly to inverse standings, not
   FAAB.* A claim does not spend a rolling asset. **There is no reason to hoard it, ever.**
4. **Matt is not losing on the DROP side.** His adds beat his drops by **+1.57 ppg** (n=30,
   2024–25) — the best point estimate in the league sample, though p=0.24.

---

## 1. CLAIM vs FREE AGENT — the load-bearing result

**POPULATION: 982 executed adds, 2022–2025, D/ST excluded. BASELINE: rest-of-season ppg from the
week AFTER the move through week 14, against the position's measured replacement
(QB 20.09 · RB 9.92 · WR 9.62 · TE 8.25, doc 12).**

**Hit rate, n=653 adds that scored afterwards:**

| position | free agent | **waiver claim** |
|---|---|---|
| QB | 22.9% (n=48) | **30.4%** (n=56) |
| RB | 14.8% (n=108) | **18.4%** (n=103) |
| WR | 16.1% (n=112) | **24.5%** (n=94) |
| TE | 18.1% (n=72) | **30.0%** (n=60) |

**Consistent in all four. And on the paired add-minus-drop measure, n=443:**

| | added | dropped | gain | p |
|---|---|---|---|---|
| **waiver claim** | 7.59 | 6.41 | **+1.18** | **0.0016** |
| free agent | 6.59 | 6.07 | +0.52 | 0.29 |
| all adds | 7.13 | 6.25 | +0.88 | 0.0039 |

**A free-agent add is statistically indistinguishable from doing nothing.** The whole measured
return to churning the roster comes from claims.

**CAVEAT, stated because it changes the reason and not the rule:** this is partly selection — a
recently dropped or newly relevant player sits on waivers first and only becomes a free agent after
the period clears, so the waiver pool is the FRESH pool by construction. The causal share is not
separable here. **The practical instruction is identical either way: get him during the waiver
period.**

## 2. WHAT THIS DOES NOT SAY

- **It does not say churn more.** §4.19 measured Matt at RB: 20.5% hit (n=39), top of the league
  table and not significantly ahead of it, and **four of five RBs he adds never give him a startable
  stretch.** Volume is not the lever.
- **It does not resolve the §4.19 paradox.** He is **1.05 weeks ahead** of the field at RB and first
  to the player **57% vs 42%**, yet his 3-week lift is **+0.39** against the league's +0.74. The
  add-vs-drop cut above says the leak is not on the drop side, so being early is either landing on
  the wrong names or landing before the role is confirmed. **Untested. Post-draft.**
- **Matt's 2022 and 2023 rows are unresolved** — the league renames teams every year and
  `manager_identity_map.csv` was not used here, so his personal cut is 2024–25 only (n=30).
  §4.19's n=88 used the map; this doc did not. **Re-run against the map post-draft.**

## 3. THE SCHEME NEEDS THE ROSTER — three things it will turn on

1. **Which roster spot is the churn spot.** §6: 14 selections, and **a waiver pickup can never
   become a keeper** (§2.1a). So churning a bench slot costs nothing in 2027 terms, and churning an
   *audition* slot costs the audition. The scheme has to name which spot is which on the actual roster.
2. **The drop rule.** His measured strength is that he does not drop value. The rule should protect
   that: never drop a rounds 5–8 pick still inside its audition window (§6) to make room for a claim.
3. **The position rule.** Doc 12's table is the argument: QB adds hit 62% of the time and RB adds
   22%. **An RB hole cannot be patched from the wire and a QB hole can** — which is why the bench is
   built RB-first and the wire is used QB-first.

---

*Reproduce: `Source\waiver_report_{2022..2025}.csv` filtered to `Status == EXECUTED`, transaction
parsed as `ADD x | DROP y`, joined by suffix-stripped name to nflverse weekly scoring under §2,
D/ST excluded, rest-of-season window = the week after the move through week 14.*
