# 127 — The live-to-live test: `--watch`, and exactly how to run it

**Date:** 2026-09-01. Matt's stated priority: *"I want to see live to live actually work to have
full confidence the page will sync."* Right priority — it is the last untested thing in the chain.

---

## 1. WHY A NEW MODE INSTEAD OF JUST RUNNING THE TOOL

The question is one bit wide: **does ESPN's read API carry picks while a draft is running?**

Every attempt to answer it so far has been tangled in things that have nothing to do with it — the
board, the position caps, keeper depletion, slot detection, the rendered page. When Matt ran the
tool at a mock, four different things could have explained a stuck screen and it took three days
to find which.

**`--watch` removes all of it.** No board, no engine, no recommendations, no HTML. It polls one
endpoint and prints each pick as it lands. **It works on a league of any shape**, which is what
lets a throwaway test league answer the question for the real one.

```
  [19:04:12] pick   1  rd  1  team 13  Jahmyr Gibbs
  [19:04:41] pick   2  rd  1  team 11  Bijan Robinson
  [19:20:03] 24 of 180 slots filled  drafted=False  |  nothing new for 7s  (140 polls)
```

**PASS:** the count climbs and each pick appears within a few seconds of happening in the room.
**FAIL:** the count never moves while the room drafts — which is exactly what an ESPN mock does
(doc 126), and the reason this test needs a **real** league.

It says so itself: three minutes with no new pick while the grid is not full prints
*"If the room IS drafting, this endpoint is not carrying it."*

---

## 2. THE PROCEDURE

**Matt's part** (ESPN session, §0.4):

1. **Create a new ESPN fantasy football league.** Free, standard settings. The only ones that
   matter are **12 teams** and a **snake** draft, so the shape matches. Keepers off is fine —
   the keeper path is already covered by `--replay` and the rehearsal.
2. **~~Do not invite anyone. Leave the other 11 teams empty; ESPN autodrafts them.~~**
   **[CORRECTED 2026-09-02 — this was wrong, and Matt hit it.]** ESPN's own draft-date tooltip:
   *"if your league is not full one hour before your scheduled draft time, your draft will not
   begin."* An empty league will let you schedule a draft and then silently never start it.
   **You must fill all 12 slots** — a second email account claiming multiple teams works, which
   is what Matt did. Autodraft then covers the teams you are not sitting at.
3. **Set the draft to start in a few minutes**, and set the clock short — 10 or 15 seconds a pick.
   A 180-pick autodraft at 10s is about 30 minutes and needs no attention.
4. **Open the draft room and copy the URL out of the address bar.**
5. Start it, then in a PowerShell window:

```powershell
cd "G:\My Drive\_Fantasy\2026\Scripts\live_draft"
py live_draft.py --watch --url "<paste the draft URL in quotes>"
```

**That is the whole test.** It writes nothing to ESPN, it renders no page, and Ctrl+C ends it.

**Then, if the feed moves, run the real thing against the same league** to see the page sync:

```powershell
py live_draft.py --url "<the same URL>"
```

The recommendations will be nonsense — that board has his keepers removed and is built for his
league — **and that does not matter.** What is being watched is the pick counter climbing and
players leaving the board.

---

## 3. WHAT EACH OUTCOME MEANS

| result | reading | what to do |
|---|---|---|
| picks appear within seconds | **the chain works end to end.** The mock failure was a mock-only limitation | nothing. Confidence earned |
| picks appear but lag 30s+ | the endpoint is cached | raise `--interval`, and expect the board to trail the room by that much on Sept 7 |
| the count never moves | the read API does not carry live picks **for any league** | the live tool cannot work on draft night. **DRAFT_BOARD on paper becomes the plan**, and that is why it exists |
| 404 | the league is gone or not yours | `py live_draft.py --probe --league <id>` |

**The third row is the one worth knowing six days early rather than at 8:01 PM.**

---

## 4. A DEFECT THE NEW MODE FOUND ON ITS OWN FIRST RUN

`--watch` and `--probe` were dispatched **before** `--reads` took effect, so both modes called the
real ESPN while the operator believed they were pointed at a local test feed. The watch mode's
first run hit `lm-api-reads` through the container's proxy and failed — which is how it surfaced.

Harmless here, genuinely not harmless in general: **a diagnostic that silently ignores the flag
telling it where to look is worse than no diagnostic.** `--reads` is now applied before either
mode runs. `[FIXED, verified by execution]`

## ASSUMPTIONS

1. **A throwaway league exercises the same path as league 21985.** Same endpoint, same view, same
   cookies — the only difference is the id. Believed, and the test itself is the check.
2. **ESPN allows a draft to run with one human and eleven empty teams.** Standard behaviour, not
   verified by me.
3. **10–15 seconds a pick is enough time for the poller to see each one.** At a 3-second interval
   it should catch every pick; if picks are being missed, that is itself a finding worth having.
