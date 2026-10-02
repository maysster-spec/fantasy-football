# Where the QB2 / TE2 question lives — one page, so you stop hunting

**Current verdict, 2026-08-30, directive v5.6 §4.16:**

| | verdict | why |
|---|---|---|
| **Three QBs or three TEs** | **never** | your rule; engine `CAPS QB:2, TE:2` enforces it |
| **Second TE** | **no** | best FLEX RB/WR out-projects best TE at all four bench picks (24.0 / 37.6 / 4.8 / 16.7); doc 12 measured TE2 at −12 to −13; §4.13 says floor is the wrong buy after round 9 |
| **Second QB** | **coin flip, ~+10** | *not* closed. Open, and handed to Fable |
| **Bench order** | **RB to the cap, then WR** | RB waiver adds hit **22%**, QB adds **62%**. Draft the position waivers cannot save you at |

**On the night:** take a second QB only if the board hands you a cheap one at 113+ *and* your RBs
are already filled. Never a second TE. Never a third of either.

---

## The thread, in order — read only if you want the reasoning

| doc | what it established | status |
|---|---|---|
| `09_sim_rebuild.md` | roster-shape grid: QB2 +15, TE2 +16, target 2QB/5RB/5WR/2TE | **superseded** — ran on the board later found 39% fabricated |
| `11_corrections_and_challenges.md` | added streaming to the sim. **TE2 collapses +16.0 → +0.4, withdrawn.** QB2 survives ~+15 but "soft" | partly superseded |
| `12_red_team.md` (F34) | measured streaming from **951 executed waiver adds**. QB 15.25 ppg / 62% hit · TE 5.53 / 42% · WR 6.54 / 31% · RB 5.43 / 22%. Re-ran shapes: **QB2/TE1 +10.1 best**, TE2 −12 to −13 | **live**, but n=34 at QB and the sim ran on the old board |
| `88_stream_vs_roster_qb_te.md` | your league 2022–25 is a **null** both ways (QB p=0.87, TE p=0.71). FLEX comparison kills TE2. Concluded "QB2 IS CLOSED" | **QB2 half RETRACTED** |
| `90_te_flex_floor_and_the_keeper_field.md` | TE has the **best floor and tightest spread** of the three FLEX positions (p25 0.684 vs 0.538/0.540), and the **worst hit rate** (12.5% vs RB 20.0%) | live |
| `91_the_streaming_baseline_was_wrong.md` | **the retraction.** QB12 is not the streaming baseline; VBD overstates streaming by 4.84 pts/wk at QB. Goff is +3.95/wk over a real streamer | live |
| `FABLE_TASKING_PROMPT.txt` | hands the open QB2 question to Fable, with the damage to both sides and an instruction not to inherit *any* baseline | pending |

## The three errors, because the pattern is the lesson

1. **doc 88** — asserted QB12 was the streaming baseline. It is not.
2. **doc 88/90** — same premise on the TE side: "Andrews sits at exactly 0.0." He is +2.72/week
   over a real TE streamer. The TE conclusion survives on other grounds; that reason does not.
3. **the first draft of the Fable prompt** — told Fable to *use* 15.25, which rests on **n=34**.
   Inheriting a baseline instead of testing it, a third time. Corrected before it was sent.

**All three are the same error: comparing a bench player against a number nobody checked.**
