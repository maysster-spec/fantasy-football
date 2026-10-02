# METHOD_TRAPS -- the rules only, no war stories

**Attach this to every red-team tasking and every research job. One page. Read it before you
design a test, not after you get a number.**

**Why it exists (doc 303).** Every rule below is already in `00_PROJECT_DIRECTIVE.md`. It is 156 KB
and each rule is told as the story of the one case that produced it, filed next to that case. A
second reader on 2026-09-13 read the whole directive and still broke two of these, because the rule
that governed his work was inside a paragraph about ESPN under-projecting rushing yards. **The
directive is the record. This is the checklist.** Where they disagree the directive wins; tell
whoever maintains this file.

---

## A. BEFORE YOU DESIGN THE TEST

1. **State what would have to be true, in one line, before you run anything.** Population, outcome,
   direction. If you are testing someone's claim, quote their words rather than paraphrasing them.
   The paraphrase is the error mode. *(§0.5a2)*
2. **State the population every time, even when you inherited it.** A population stated once in the
   doc that built the dataset silently widens in every doc built on top. *(§0.6)*
3. **Name what the population EXCLUDES, and how big it is.** "D/ST excluded" is a fact.
   "D/ST excluded, which is 27% of all adds" is a warning. *(§0.6)*
4. **Check the data actually contains the category you are about to conclude about.** A silent
   `continue` on an unmapped row is the same defect as a silent skip on a missing column. *(§0.6)*
5. **Fix the falsifier before you compute.** Write down which result resolves which way. *(§4.18b)*

## B. THE FILTER TRAPS -- this is where the 2026 red team lost

6. **NEVER CONDITION ON AN OUTCOME-CORRELATED FILTER AND READ THE RESULT AS A PROPERTY OF THE
   PREDICTOR.** Selecting on games played selects on success. Selecting on "the starter kept his
   job" deletes every takeover. **Ask of every filter: could the event I am predicting have CAUSED
   a row to be dropped?** If yes, the filter is a decomposition and never a retraction. *(§4.23(a),
   doc 303 §3b)*
7. **A filter is legitimate when it is knowable BEFORE the outcome window opens.** Prior-season
   status, draft capital, price: fine. Anything measured during the outcome window: not a
   population, a conditional. Say which you are reporting. *(doc 303)*
8. **Cluster first on any team-level variable.** OL disruption, vacated share, pass rate and
   anything else that is a team constant has an honest n of 32, not of 142. *(§4.24, A5)*
9. **A selection group has its own base rate.** NGS only scores receivers who already have volume,
   so that subsample's base rate is 22% where the full set is 9.9%. Report the subsample's base
   rate, never the population's. *(§4.28)*

## C. WHAT COUNTS AS AN ANSWER

10. **Three answers, and "that isn't measurable" is not one:** TESTED (population, baseline, n,
    direction, number, including when it dies) · NOT YET RUN (with the testable form written down)
    · BLOCKED (naming the exact missing input, where it would come from, and whether you tried).
    *(§0.5a4)*
11. **A BLOCKED verdict is itself a claim and gets ONE falsification attempt before you write it
    down.** Try the sibling release, the other filename, the second source. Thirty seconds.
    *(doc 303 §2 -- the rule this file was born from)*
12. **Report the null as readily as the hit, and say whether it failed PREDICTION or POWER.** State
    the minimum detectable effect. An underpowered null invites more data; a refutation closes the
    file, and they are not the same sentence. *(§4.24(b), §0.5a4)*
13. **Report the interval of the thing that is uncertain, not the one that is cheap to shrink.** A
    Monte Carlo standard error printed beside a measured quantity reads as precision the
    measurement does not have. *(doc 302 §5.3)*
14. **Say which definition of the outcome you mean.** "Beat his price" and "was startable at all"
    point opposite ways on the same rows. *(§4.13b)*

15. **A generated page cannot prove that the thing it describes was EXECUTED.** Ask what the
    builder READ. `make_commands.py` builds the scheduled-task table by parsing
    `setup_tasks.bat`'s own text, so that table is evidence about the FILE and says nothing about
    Windows Task Scheduler. It was quoted as proof the file had been run, and the page's own
    comment calls it "the live schedule". **Evidence for "it ran" is something the RUN wrote and
    nothing else could have written**: a log line, an output file's timestamp, a row only that run
    produces. This is the exit-code rule one level out. There the return value was checked instead
    of the artifact; here the artifact was checked and it was the wrong artifact. *(0.2, doc 377)*

## D. CLAIMS ABOUT SIZE, SPEED AND CODE

15. **A severity estimate is a claim: measure it, never reason it.** This applies to claims made
    while READING CODE as much as to statistical ones. "Nine rows are exposed to this sort" is a
    count you can run; run it. It was three. *(§0.2, doc 303 §3e)*
16. **A performance diagnosis is a claim: profile, do not reason.** *(§0.2)*
17. **A diagnosis is a claim: reproduce the failure before writing the fix.** A fix aimed at an
    unverified cause creates a second defect on top of the first. *(§0.2)*
18. **Test the object PRODUCTION builds, not an equivalent one.** Same logic on a differently
    shaped object is not a test. If you write a variant builder, prove it reproduces the original
    exactly on default settings before you read any variant. *(§0.2, doc 303)*
19. **An exit code is not a result. Verify the artifact.** *(§0.2)*
20. **A guard that has never been executed is not a guard, and a check that exists only as a
    one-off manual run is not a control.** Run it against the specific defect that motivated it and
    show it FIRE on the broken tree before you claim it covers anything. *(§0.2, doc 302 §9)*
21. **Diff a patched function against the SHIPPED file, never against itself.** *(doc 296)*

## E. TOKENS, NAMES AND FILES

22. **A grep token that can match a legitimate row can neither close a ledger row nor hold one
    open.** Scope the token to the object you are auditing, then run it against both the broken and
    the fixed tree. *(AUDIT_LEDGER row 13, doc 302 §11)*
23. **Join on an id, or on name + position + team, never on less.** Normalise the name or refuse
    the join. Never default a missing join to a placeholder: assert. *(§3)*
24. **Never assume a stat id is the same in two payloads. Check both, on real rows.** *(§4.13 corollary)*
25. **List the folder before writing ANY new file.** Two names for one job is the same defect as
    two files claiming one number, and the naming rule does not catch it. *(§0.2, §0.5c4)*
26. **One quantity, one number.** When two exist, pick one, say which supersedes, and record the
    loser. *(§0.5c4)*
27. **Archive to `2026\_archive\` before overwriting anything.**

## F. WHEN YOU REPORT

28. **What survives is reported as readily as what died**, and by name.
29. **Do not leave a number in the directive that your run has moved.** If you propose directive
    text, the numbers in it must come from the full data, not a subset you could reach.
30. **List your own open threads by name, with owners**, and put anything a human must run in
    `Source\matt_todo.txt` the moment you say it -- a request made only in a reply is invisible to
    the tracker. *(§0.5e)*

## ESPN GIVES D/ST NEGATIVE PLAYER IDS, AND `(\d+)` DROPS THEM SILENTLY
**[doc 401, 23 Sept 2026. §0.6 was written about a D/ST exclusion; this is the same defect in a new place.]**

`waiver_report_*.csv` stores the player as `ADD Player ID 4248528`, and a team defence as **`ADD Player ID -16012`**.
A first pass at the claim-order question extracted it with `r'ADD Player ID (\d+)'`. That regex does not match the
minus sign, so **437 of 1,623 waiver rows, 27%, vanished with no error and no warning** — every one of them a D/ST.

**How it surfaced:** not by inspection. The population failed to reproduce doc 396's published counts (476 player-runs
against 745), and only then did the extracted-row count get checked. **Had the numbers happened to look plausible, a
D/ST-free population would have been published as "all waiver claims."**

**THE RULES:**
- **Any id extracted from an ESPN string uses `(-?\d+)`.** Negative ids are team defences, and they are real rows.
- **Assert the extraction count against the row count**, always: `assert df.pid.notna().sum() == len(df)`. An
  extraction that silently yields NaN is §3's silent-skip trap wearing a regex.
- **§0.6(2) then applies to whatever is genuinely excluded**: name it, and say how big it is. "D/ST excluded" is a
  fact; "D/ST excluded, which is 27% of waiver claims" is a warning.

---

## A SNAP-SHARE CHANGE IS NOT A CAUSE. READ THE MAN'S OWN STATUS BEFORE YOU EXPLAIN HIS USAGE.
**23 Sept 2026, doc 408. Matt: *"Dowdle, 26%, yes, he got injured week 2, lol. Somehow you still only see a
very narrow picture of what i see."***

**WHAT HAPPENED.** Rico Dowdle's snap share went 58% to 26% between weeks 1 and 2 while Jaylen Warren's went
37% to 71%. I read that as a job handover, named Warren as the man who took it, and recommended Dowdle as the
drop over Xavier Worthy. **He was injured mid-game. The snap share is an injury, not a demotion.**

**THE PART THAT MAKES IT A METHOD TRAP AND NOT A BAD LUCK STORY: the answer was in the file I had already
printed.** `MY_ROSTER.csv` carries a `status` column. It said `QUESTIONABLE` on the same row, in the same
table I rendered two calls earlier, and I read past it because I was looking at the backfield rather than at
the man. **I checked the incumbent's status and never checked the candidate's own** — the take contract's
line 3 obeyed against the wrong player.

**AND THE REAL GAP UNDERNEATH IT: there is no injury feed here at all.** What this project can see about a
roster is a preseason projection, two weeks of snap and target counts, and a one-word ESPN status string.
`cards_2026.csv`, the only news file, was built 11 Sept and carries no row for anybody on his roster.
**So a snap count can move for a dozen reasons and the data cannot tell them apart.** With that input set,
"Warren took the job" was never a finding. It was a guess with a number next to it, which is §0.2's oldest
failure wearing this week's clothes.

**THE RULES:**
- **Never explain a usage change without first quoting the player's OWN status and his snap COUNT, not just
  his share.** A share falls when he is hurt, when the game script flips, when the team trails, and when his
  job goes. Those are different objects (§0.5(a2)).
- **A status other than ACTIVE on the candidate is a STOP**, not a footnote. Say "injured, cause unknown"
  rather than picking the explanation that fits the story.
- **When the inputs cannot separate injury from demotion, say so and say it is BLOCKED** with the missing
  input named (§0.5(a4)). The missing input here is a game-level injury and news feed, which is mine to build.
- **Matt sees the games. This project sees a CSV.** When his direct account contradicts the table, the table is
  wrong about WHY even when it is right about WHAT (§0.6 rule 4). Ask what is not in the data before
  defending the number.

## A UNIT TEST OF THE NEW FUNCTION IS NOT A TEST OF THE FUNCTION THAT CALLS IT. WALK THE CALL PATH, OR READ ITS ORDER.

*29 Sept 2026, doc 448.* A logging call was added to `wire.py`'s `main()` fourteen lines above the line that
assigns the variable it reads. The new function had a unit test and passed it; `main()` needs ESPN and was
never run. The 20:06 `ff.bat` run died with UnboundLocalError: wire 1, no wire page, no week sheet, and the
online copy republished the 18:16 page with a fresh stamp. Every check in the tree was green, because every
check reads what a script WRITES and none reads the ORDER a script runs in.

**THE RULES:**
- **A function that cannot be run here (it needs ESPN, a login, his machine) is tested by walking its call
  path, not by testing the piece you added to it.** Read `main()` from the top to the new call and name the
  line that assigns each thing the call reads. If any is below the call, the call is dead on arrival.
- **`py check_locals.py` does that read for every function in every shipped script**, statically, in
  evaluation order, and `ff.bat` runs it after the kit check. It fired on the file that died and is quiet on
  the fix. A new call into `main()` is not shipped until it is quiet.
- **An exit code of 0 from the step AFTER the one that died is not a result** (0.2): `make_online.py`
  rebuilt the online copy from the stale page and printed `written`. The RESULT line's `wire 1` was the
  only true word in that run.
