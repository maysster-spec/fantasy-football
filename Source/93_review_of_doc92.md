# 93 — Review of doc 92 (Fable). Step 1 corroborated, headline accepted, corroboration claim rejected.
*2026-08-30. Adversarial review, per §0.2. I did not re-run Fable's simulation — I checked what
could be checked independently and pushed on what could not.*

---

## VERDICT: act on the QB2 result. Do not act on the TE2 result. One claim inside it is wrong.

## 1. Step 1 is corroborated by measurements I made before the question arose

Earlier this session, for an unrelated purpose, I parsed the same four waiver files:

| | mine (independent) | doc 92 | doc 12 |
|---|---|---|---|
| executed adds | **1,230** | **1,230** | 951 |
| QB adds | ~130 | 135 events / 82 player-seasons | **34** |
| TE adds | 151 | 93 player-seasons | 53 |

**Two independent parses land on 1,230 exactly.** Doc 12's 951 and its n=34 are not reachable from
the raw files by any filter either of us tried. **Doc 12's sample sizes were wrong**, and the
+10-point conclusion this project carried for two weeks rested on them.

Doc 92 also corrects *me* in the other direction, and is right to: doc 91 claimed VBD overstated
streaming by **4.84 pts/week** at QB, computed against doc 12's unreproduced 15.25. Against the
re-measured 16.65 the real gap is **3.44**. My correction was itself overstated by 40%.

## 2. The crossover is arithmetically sound — checked

Refitting doc 92's own sweep: slope **−2.197 points per ppg** of streamer quality, zero crossing at
**21.67 ppg** (it claims 21.7), maximum residual from the line **0.01 points**. Its "linear to the
eye" is exact.

More usefully, **the slope reveals the load-bearing quantity**: 2.20 points per 1 ppg means the
backup effectively starts about **2.2 weeks a season** — one bye plus ~1.2 injury weeks. That is
plausible, it is nowhere stated in doc 92, and every number in the document scales with it. If the
true figure were 1.2 weeks, the crossover falls to roughly 17 ppg and the verdict tightens sharply.

## 3. REJECTED: "three independent methods now agree"

Doc 92 cites doc 12's +10.1, doc 91's +8–12, and its own +11.0 as three-way agreement.

- **doc 12 is irreproducible by doc 92's own step 1.** A document cannot demolish a source's sample
  sizes in §1 and then cite its output as corroboration in §2.
- **doc 91's +8–12 was my arithmetic, computed FROM doc 12's 15.25.** Not independent — the same
  number twice.

**It is one clean measurement.** The result may well be right; the support is a third as thick as
claimed. This is the same failure mode as doc 88's — treating a restatement as a replication.

## 4. The residual I cannot close, and it favours the backup

Doc 92's assumption (2): the streamer fill is a constant per position, with **no week-to-week
matchup selection**. So the sim gives the rostered QB2 his full projection while giving the streamer
a flat average — and *matchup selection is exactly where a good streamer's edge lives*. Doc 92 says
the sweep is the sensitivity for this. Partly: raising the mean fill stands in for skill on expected
points, but not for the *option* to start whichever is better that week.

**Direction is knowable even if the size is not: the machinery flatters the rostered backup.** With
Matt's 0.60 hit rate — the league's best — he is the manager for whom this matters most. It does not
plausibly cover a 21.7 ppg crossover, which is why the verdict survives; but the honest headline is
**+11 measured once on machinery that leans slightly the right way for its own conclusion.**

## 5. TE2: correctly surfaced, correctly quarantined, not actionable

Doc 92 reports **TE2 +4.07 ± 2.54** against doc 12's −13.4, and does not bury it. Credit for that.

It is not actionable, for three reasons doc 92 partly states: it is **1.6 sd from zero** (against
QB2's 3.6); the document **never states how the FLEX slot is modelled**, which is the entire
mechanism by which a TE2 could pay; and it sits against a shipped-board comparison where the best
FLEX-eligible RB/WR out-projects the best TE by **24.0 / 37.6 / 4.8 / 16.7** at the four bench
picks. **Filed, not acted on.** Doc 92's own framing — "your doctrine governs the night; the number
is filed for after" — is the right call.

## 6. What this changes on draft night

**At 104 or 113, a Goff/Mayfield-tier QB over an RB dart is now the measured play, worth about +11
points and +$14–18.** That is one of four late picks; §4.13's round-9 risk doctrine keeps the other
three. It contradicts Matt's stated doctrine, which §6 says is a preference and not to be argued
out of — **so it is his call, not mine to overwrite.** My recommendation is to take it, with the
caveats in §3 and §4 attached rather than buried.

**Nothing else moves.** TE2 stays no. Bench stays RB-to-the-cap-then-WR — and that rule got
*stronger*, since the re-measured RB streamer (6.60 ppg) still cannot replace a drafted RB.

## Assumptions, and what would invalidate each

1. **Doc 92's simulation does what it says.** I checked its inputs, its arithmetic and its internal
   consistency — not its code. A defect in the paired-seed handling or the lineup optimiser would
   not be visible from the document, and the TE2 anomaly is the kind of thing such a defect produces.
2. **~2.2 starts a season for the backup is right.** Inferred from the sweep's slope, not stated.
   It is the single number the whole result scales with, and it was never independently derived.
3. **Matt's streaming is not materially better than his league's average.** His 0.60–0.62 hit rate
   says he is better. The crossover at 21.7 is high enough to absorb it — unless the missing
   matchup-selection effect in §4 is larger than the mean-sweep represents.
