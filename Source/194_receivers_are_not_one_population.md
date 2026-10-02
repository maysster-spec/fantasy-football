# 194 — Route depth, the third-year question, and an honest read on how we work

**2026-09-06 (T−1).** Matt: *"WRs have different roles… we don't want to paint a broad brush of
signals across all WRs… WRs in the 3rd year tend to break out, not the 2nd."*

## 1. THE BROAD-BRUSH CHARGE — he is right in shape, and I cannot confirm it at this n

Receivers split by **aDOT** (average yards downfield per target — the best route-tree proxy the data
supports), n=390 receiver-seasons. **BASELINE: half-PPR wks 1–14 on log(§1.1 preseason ADP), within
season; BEAT = residual; player-clustered.**

| route depth | n | mean beat | **SD of beat** | boom rate (beat > 50) |
|---|---|---|---|---|
| SHORT / slot (aDOT < 9) | 156 | −11.5 | **37.2** | 4% |
| INTERMEDIATE (9–12) | 138 | −14.4 | **42.8** | 7% |
| DEEP (12+) | 96 | −11.6 | **38.0** | 6% |

**(a) "Deep receivers are boom or bust" — NOT SUPPORTED.** The spreads are 37 / 43 / 38 and
**Levene's test for equal variance is p=0.572.** Deep threats are no more volatile *against their
price* than slot receivers. The boom rate is 4–7% in every group. `[TESTED — NULL]`

**(b) But the signals do behave differently by group, which is the real claim:**

| group | games played | in-10 targets | target share | aDOT itself |
|---|---|---|---|---|
| SHORT / slot | +2.2 (p=0.125) | +0.2 (0.835) | +9 (0.885) | −0.4 (0.819) |
| INTERMEDIATE | +0.7 (0.636) | −1.1 (0.457) | −57 (0.349) | +1.5 (0.735) |
| **DEEP (12+)** | **+2.4 (p=0.032)\*** | +0.6 (0.626) | +112 (p=0.089) | **−4.2 (p=0.040)\*** |

Two readings, and the second one is the honest one:
- **The availability signal lives almost entirely in the deep group**, and inside that group
  *going deeper is worse* — −4.2 points per yard of aDOT.
- **That is 12 tests and 2 came back under p=0.05. Chance alone predicts 0.6.** With a
  multiple-comparison correction neither survives. **`[SUGGESTIVE — NOT ESTABLISHED]`**

**So: the structural argument is sound and the evidence is not yet there.** Splitting receivers is
the right instinct and it is exactly what n=390 cannot resolve into three groups of ~100. This is a
power problem, not a logic problem, and it is the clearest case yet for more seasons.

## 2. YEAR THREE, NOT YEAR TWO — he is directionally right and the popular story is wrong

Never tested before. WR/TE by season in the league:

| season | n | mean beat |
|---|---|---|
| **2nd** | 69 | **−19.3** ← the worst band |
| 3rd | 70 | −12.3 |
| **4th** | 60 | **−8.9** ← the best band |
| 5th | 55 | −13.3 |
| 6th+ | 193 | −12.9 |

**The "second-year leap" is the *worst* band on this measure**, and it improves for two more years
after. As indicators: 2nd season −7.0 (p=0.143), 3rd season +1.2 (p=0.802) — **neither resolves.**
`[SUGGESTIVE]` His correction to my year-2 framing is directionally supported; his specific pick of
year three is not what the data points at — **year four is.** Neither is significant.

## 3. WHAT I STILL CANNOT DO — said plainly because he asked about separation

**PFF grades, separation, routes run and alignment (slot vs X vs Z) are not in any source this
project holds.** aDOT is the only route-tree proxy available and it is a crude one — it separates
depth, not release skill, not cut ability, not where a man lines up. **The route-tree analysis he is
describing is correct and I cannot run it.** Saying it needs the data is not a dodge; it is the
answer, and the fix is a PFF or Fantasy Points Data subscription, post-draft.

*(And it is Luther **Burden**.)*

## 4. THE PATTERN, MY READ — he asked, so this is honest rather than flattering

**What actually happens:** he opens wide, I narrow and measure, and then **his second question is
better than his first** because it is built on a result instead of a prior. Doc 188 (the biggest
finding here) came from his memory of an analyst take. Doc 191 came from him doubting my
one-at-a-time method. Doc 193 came from him saying "counter-intuitive, re-examine." **None of those
were on my list.**

**The split in his record is sharp and worth naming:** his *mechanisms* mostly die — the offensive
line, opportunity environment, the year-two bounce-back, age, boom-bust deep receivers. His
*process critiques* almost all land. `ERROR_PATTERNS` F4 already says this; tonight added three more
instances to the second column and four to the first.

**Where the method actually loses time — all three are mine:**
1. **I ship before I test.** The red-zone mark went onto the sheet, then got tested, then came off.
   That is the second time today. The fix is not his to apply.
2. **I report "null" without reporting what I could have detected.** Several results tonight were
   underpowered, not absent, and he had to ask before I said so. **State the detectable effect size
   with the test, every time — before the verdict, not after it.**
3. **I name the untestable category too late.** "Cannot be tested at all" — the unsettled-job flag,
   the analyst BUY flag, PFF separation — only got written down at doc 192. It should be the first
   thing said about any new signal, not the last.

**The one change I would make to the discourse:** when he opens a wide question, my first reply
should be the **three-way split** — what I can test now, what I can test with data I can go get,
and what is not testable at all — *before* any result. He has been supplying that structure himself
by asking follow-ups. It should not be his job.
