# 75 — INJURY CONTEXT SHEET v2: THE DESIGN

**Aug 29, 2026.** What v1 got wrong, what the schema should be, and the division of labour.
**Read this before reading `DEEP_RESEARCH_injury_prompt.txt`.**

---

## 1. WHAT v1 ACTUALLY DELIVERED, AND WHY IT IS NOT ENOUGH

v1 took ESPN's `seasonOutlook` prose, found the sentence naming an injury, and printed it in ADP
order. That was a retrieval job. It surfaced the right sixteen players — but every row still hands
Matt a **sentence**, and a sentence cannot be acted on in sixty seconds.

Compare the two forms for the same player:

> **v1:** *"Nabers is on the comeback trail after a torn ACL limited him to only four appearances
> last season."*
>
> **v2:** `ACL-12mo · re-inj 6% · GP 15 (13-16) · form 85% wks1-5 · priors 0 · hedge W.Robinson ·
> DISCOUNT · adj vbd +39.3 → +12.4 · rank 30 → 47`

The first tells Matt something he mostly knew. The second tells him **what it costs**, and where
the player actually belongs on his board. That gap is the whole point of this document.

## 2. THE PRINCIPLE

**An injury is not a label. It is a distribution over two things: games available, and per-game
production while playing.** ESPN's `proj_leaguepts` is a healthy-17-game number — doc 74 measured
that it carries no injury adjustment at all. So the correct treatment is a **haircut on the
projection**, computed from two researched quantities, then re-ranked on the same board.

That is why the schema below asks for `GP` and `FORM%` as *numbers*. Everything else is context;
those two are the arithmetic.

## 3. THE SCHEMA — nine fields, all short, fixed vocabulary

| field | what it is | why it earns a column |
|---|---|---|
| `CLASS` | injury class from a **fixed** vocabulary (§4) | a free-text label cannot be joined to a base rate. A fixed token can |
| `RE-INJ%` | probability of recurrence **within the coming season** | the number Matt named himself: hamstrings run 30-38%. This is the field that turns "he's fine now" into a risk he can price |
| `PRIORS` | count of prior same-class injuries | the single strongest predictor of recurrence in the literature. Nabers with 0 prior ACLs and a WR with 3 prior hamstrings are not the same bet |
| `GP` | expected games available, out of 17, plus a low-high | drives the haircut |
| `FORM%` | expected per-game production vs healthy baseline, and for how many weeks | Matt's own case 2 — "misses one week, hobbled all year." Invisible to every other source |
| `HEDGE` | the direct beneficiary if this player misses time | converts a risk into an action. §4.13 says take that swing from round 9 |
| `VERDICT` | one of `AVOID` / `DISCOUNT` / `NEUTRAL` / `TARGET-LATE` | the scannable left edge |
| `WHY` | 12 words maximum | the reason, not the story |
| `SRC` | source tag + date | §3 forbids an unsourced claim |

**Two derived fields are computed here, not researched:**

```
adj_pts  = proj_leaguepts x (GP / 17) x form_factor
adj_vbd  = adj_pts - replacement[pos]        RB 168.589 · WR 163.540 · QB 341.603 · TE 140.295
Δrank    = new board rank - current board rank
```

`Δrank` is the payoff. **Matt reads a rank move, not a paragraph.**

**[FRAMEWORK, NOT A MEASURED RESULT.]** This haircut has no historical validation available in
this project — doc 74 §A4 established that historical injury status is contaminated the same way
ADP is, so a backtest cannot be run. It is external base rates plus arithmetic, and it should be
labelled that way on the sheet itself. It is still far better than a red word that means nothing.

## 4. THE FIXED CLASS VOCABULARY

Research must return one of these, never free text:

`ACL-<12mo` · `ACL-12-24mo` · `ACHILLES-<12mo` · `ACHILLES-12-24mo` · `HAMSTRING-1st` ·
`HAMSTRING-recur` · `HIGH-ANKLE` · `ANKLE-other` · `KNEE-scope` · `KNEE-other` · `LISFRANC` ·
`SHOULDER` · `BACK` · `CONCUSSION-recur` · `GROIN-recur` · `FOOT` · `SUSPENSION` · `NONE`

Two classes matter most to Matt and both are in his own examples: `HAMSTRING-recur` (his 30-38%
figure) and `ACL-<12mo` / `ACL-12-24mo` (his Barkley-2021 "ceiling suppressed in year one" case).
The vocabulary exists so those two are never buried in prose again.

## 5. THE OUTPUT FORMAT — one page, ADP order, scannable left edge

```
VERDICT | ADP | PLAYER            POS | CLASS          RE-INJ | GP    FORM%      | vbd -> adj  Δrank | HEDGE        | WHY
DISCOUNT|  34 | Malik Nabers       WR | ACL-12-24mo     6%    | 15    85% wk1-5  | +39 -> +12   -17  | W.Robinson   | year-1 ceiling suppressed
AVOID   |  97 | George Kittle      TE | ACHILLES-<12mo 12%    |  9    80% wk1-8  |  +2 -> -31   -35  | Ja.Bell      | 38yo, out now, one full season ever
TARGET  | 156 | Zach Charbonnet    RB | ACL-<12mo      —      |  7    90% wk1-4  | -45 -> -78    —   | (is the hedge)| round-9 dart only
```

Rules: ADP order (matches the flow of the draft). Verdict token left-aligned so the eye lands on
it first. No sentences. Fits one landscape page beside `DRAFT_CARD` and `FALLBACK_BOARD`.

## 6. DIVISION OF LABOUR — and why this is offloaded

**Deep Research supplies** the base rates and the two numbers per player. That is genuinely
external work: sports-medicine recurrence literature, return-to-play studies, and current beat
reporting. It is bounded, citable, and needs no project context — which is exactly what makes it
a clean handoff.

**This chat supplies** the schema, the arithmetic, the re-ranking against the shipped board, and
the final one-page artifact. Deep Research must not be asked for rankings, draft advice, or
"who should Matt take" — the board already answers that. Asking it to opine on value would import
a second, uncalibrated ranking system into a project that has spent three weeks calibrating one.

## 7. WHAT MATT SHOULD EXPECT THIS TO BE WORTH

Unknown, and it should not be oversold. Only **3** of his top 180 are actually injured today, and
the sixteen-player list is mostly *history*, not current absence. The realistic value is:

1. **Not flinching** on McCaffrey, Nacua, Hall, Love — 33 red tags that mean nothing (doc 74).
2. **Pricing the two or three real ones** instead of guessing under a clock.
3. **The hedge column**, which turns a worry into a round-9 dart with a name on it.
4. A reusable artifact — the class base-rate table is good every season, not just this one.
