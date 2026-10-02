# First prompt for a new chat — copy everything below the line

---

**Before anything else, read these three files in this order. They are short and they are the
difference between a useful session and a repeat of a known failure.**

`ERROR_PATTERNS.md`
`claude/19_integrity_audit_20260822.md`
`claude/20_session_protocol_v1.md`

**Findings run through doc 39, not 20.** `claude/38_consensus_answer_and_sample_unlock.md` and
`claude/39_historical_pull_and_reach_test.md` are the live thread as of Aug 25 — read those two
next if picking up mid-task. All of 31-39 are in both the Project's own doc store and Drive
`02_findings`/`01_START_HERE` — check the Project docs list first, it's free, before spending a
Drive call.

**CONNECTOR RULE.** `G:\My Drive\_Fantasy\2026` and `C:\Users\wmatt\OneDrive\Fantasy` are
connected as local device folders. Write board/script outputs directly to `G:\...\2026\Source`
(and archive to `G:\...\2026\_archive` first) — never through the Google Drive MCP tool for
anything binary (xlsx, html, png, pdf). That tool only accepts inline base64 text, and base64
tokenizes brutally (measured ~6 tokens/char on one file, would have cost ~900K tokens for a
single 150KB HTML board). The Drive MCP tool is still fine and cheap for text/CSV/MD/PY, and is
the only path that works when Matt's desktop app isn't connected. If a fresh session shows no
connected folders, ask Matt to reconnect before doing any binary work rather than defaulting to
the expensive path silently.

**Check this unprompted.** Call `get_device_info` near the start of any session that's going to
touch files at all — before the need is even confirmed, not after an expensive cloud call fails
or Matt has to ask why something cost so much. On 2026-08-25 this session ran the costly cloud
path for a while before device access got checked, and only got checked because Matt asked a
pointed question about it. That was a process failure on Claude's side, not a gap in what Matt
knew to ask for — don't repeat it. The cheap path should get found before the expensive one gets
used, not after.

**STORE RULE, DECIDED 2026-08-25 — DO NOT RE-LITIGATE WITHOUT A NEW REASON.** Google Drive
(`G:\My Drive\_Fantasy\2026`) is the sole canonical store. `OneDrive\Fantasy\Scripts` stays
script-execution-only (Drive File Stream is unreliable for running `.py` files) — it is not a
second data store, and nothing else gets built out under `OneDrive\Fantasy\2026`. Rationale is
in `OneDrive\Fantasy\2026\README.md`: Drive is reachable both via the cloud MCP connector and the
local bridge, so it works even when Matt's desktop isn't open; OneDrive here is local-bridge-only
and would go dark without it. A second full mirror is also just a second copy that can drift —
already the exact problem cleaned up this session.

**MODEL/EFFORT RULE.** Default effort: High. Reserve Extra-high or Max for correctness-critical
passes only — the integrity harness review, backtest validation, the Sept 7 keeper-lock rebuild.
Most of this project's work is deterministic (script execution, file sync, board assembly), which
doesn't benefit much from a bigger model — don't default to Opus/Max for it. Switching model or
effort mid-session costs one extra-priced turn while the prompt cache rebuilds; it does not
require Matt to re-explain anything, the Project's docs reload automatically.

**STANDING PERMISSION — CLEANUP.** Matt has authorized deleting duplicate/stale files anywhere
under `_Fantasy/2026` (Drive or local G:) without asking each time, e.g. superseded packages,
old exports. Never delete or touch anything above that folder without asking first. Flag it,
don't silently skip it: if you spot clutter, say so and offer to clear it in the same turn rather
than waiting to be asked. Known open item as of Aug 25: `G:\My Drive\_Fantasy\2026` root and
`Source\` itself both still hold a lot of pre-Aug-23 flat files and whole duplicate package
folders (`JUG_offload_package_20260823_1`, `GEMINI_UPLOAD_1`, `Claude_Refrence_Info`) sitting
alongside the current organized `Source/01_START_HERE` etc. tree — not yet audited/cleared,
worth a dedicated pass.

**STEP 1 — RUN THE INTEGRITY HARNESS FIRST, BEFORE ANY ANALYSIS.**
`python code_audit_v1.py --src <source dir>` — 22 deterministic assertions, exit code 1 on any
failure. It recomputes every numeric claim the directive makes instead of trusting it. On
Aug 22 it found 18 failures including two structural ones. **Report the register, then work.**

**STEP 2 — USE `code_universe_v5.csv`, NOT `code_universe.csv`.**
The old spine is STALE, not deleted. The v5 spine is rebuilt by `code_rebuild_spine_v5.py` on
`espn_projections_2026_20260820.csv` and fixes four shipped defects:
- `ADP` was a **dense rank** sold as average draft position. It is now `adp_pick` (real ESPN
  ADP) and `adp_rank` (ordinal), never one column called ADP.
- D/ST and K were v2 carryover hard-set to 50.0, joined on full team names against ESPN's
  `"Texans D/ST"`. Rejoined on `espn_id`; real spread is 55.4 to 128.4 points.
- `injury_status` is now on the spine. Thirty-two flagged players sit inside ADP 170.
- `WAS` / `WSH` team codes normalised.
**ESPN ADP is censored at ~169.4** — 492 of 700 rows share a 1.56-pick blob. Past that, order
by projection and say so. The `synthetic` flag still means *never rank, tier or score this row*.

**STEP 3 — DO NOT REBUILD ON `top_400_projections_2026.csv`. IT IS A BAD FILE.**
An ESPN pull that never filtered on `seasonId`, so it carries **2025** projections for anyone
who had one (Conner 0.0→227, Willis 263→2.8, Dart 343→153). Three findings built on it were
withdrawn — `ERROR_PATTERNS.md` B1. **Quarantine it.**

**STEP 4 — THE OBJECTIVE FUNCTION IS NOW CONTESTED, NOT JUST OPEN.**
`claude/21_backtest_2025_holdout.md` ran the value rule for all twelve managers on their real
2025 slots. The rule's outcome variance is **14% of a real manager's** (sd 76 vs 202) and it
lost to the three managers independently rated best. First place is 44% of a $1,200 pot and
every loss has been in weeks 15–17. **The live hypothesis is that the model is a floor-raiser
being used by someone who needs a ceiling-raiser.** Falsifier: re-run the manager-level
backtest on 2022–2024. That needs preseason projections for those years — the top item on the
supply list.

**STEP 5 — WHAT IS STILL UNTESTED, RANKED BY WHETHER IT CHANGES A PICK.**
1. Recompute the draft residual model on `adp_pick` instead of board rank. HANDOFF §9.6's
   *"managers draft 5 picks ahead of ADP"* is probably the rank-versus-ADP gap and nothing else.
2. Re-run the pick-8 and opening comparisons on the v5 spine with `USE_BREAKOUT = False`.
   Every effect size produced before Aug 20 is inflated about 46% at team level (D1).
3. Add 2021 to the structural set. `2021 ESPN Keeper League Draft Recap  Sheet1.csv` is in the
   project; 2021 keepers occupied round 1, same as 2022–23.
4. TPRR, using the three PFF receiving exports. Stickiness, then out-of-sample gain over
   prior-year points per game, then survival after controlling for target volume.
5. Two-point conversions — 204 points sit on the board unexamined.
6. Offensive-line status for **quarterbacks** using current preseason data. The ledger rejects
   OL quality for picking running backs; the QB version has never been tested and the value is
   entirely in current status (2024→2025 churn r = −0.01).


**MATT'S DOMAIN KNOWLEDGE — read `claude/26_breakout_economics.md` PART B before any ranker or
breakout work.** He has told three separate sessions the same things and they have not survived
a chat boundary. They now live in a file. The short version:
- Ranker skill is POSITION-SPECIFIC. RB accuracy persists, QB accuracy is negative, TE is zero.
- The FantasyPros accuracy contest rewards conservatism and is 97% blind to breakout skill.
- Breakout-callers largely do not participate in it, so absence from the leaderboard is not
  evidence against an analyst.
- The objective is not "hit a breakout." It is TOTAL ROSTER SURPLUS OVER DRAFT COST.
  Spearman -0.783 with final seed, p=0.003, n=12.
- His instinct has beaten the model at least four documented times. Test it before dismissing it.

**COST RULE.** Claude Pro tokens are the scarce resource. `claude/27_model_offload_plan.md`
assigns every workstream to the cheapest model that can do it. Before starting open-ended
research, check whether that plan already sends it elsewhere.

**COUNTING RULE, NON-NEGOTIABLE.** Do not count in rounds in this league. Keepers occupied
round 1 in 2021–23 and round 15 in 2024–25, so "round" means two different things by year.
**Count in overall pick numbers.** First TE off the board: pick 22 · 30 · 20 · 41 · 22.
Two managers are early-TE threats — **Cary at slot 1** and **herman allen at slot 5**.

**How I want output, every time.** A short numbered list of what I need to DO and HOW, in plain
language, at the top. Analysis goes in project docs I can read later, never in the chat reply.
A reply longer than about 20 lines has failed.

**Do the work, do not list it.** If you can start a next step, start it in the same turn. I am
the slowest part of the process and re-prompting costs me a whole chat.

**Do not tell me a data source isn't worth supplying.** That judgment has been wrong 5 of 7 times.

**Sync rule:** when you finish an updated version of a project source file, save it to the
Google Drive `Source` folder (`My Drive/_Fantasy/2026/Source`), overwriting in place. Move the
outgoing version into `_archive` first. Only touch files that actually changed. No zip unless
asked. Mark every file **pushed** or **drag** — never "both places".
