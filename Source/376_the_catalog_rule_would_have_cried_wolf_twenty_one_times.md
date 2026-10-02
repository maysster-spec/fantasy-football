# 376. THE CATALOG'S OWN RULE WAS WRONG, AND MEASURING IT FIRST IS THE ONLY REASON IT SHIPPED

*19 September 2026, 12:30 ET. Written after scoping the Fable red team Matt asked for. Population
for every count below: the six generated pages as built by the 19 Sept 11:51 ET run of `ff.bat` --
`WEEK_SHEET.html` (77,754 B), `MY_TODO.html` (91,682 B), `LINEUP_CHECK.html` (4,318 B),
`THE_WEEKLY_WIRE.html` (39,896 B), `Source\COMMANDS.html` (4,782 B, static) and `2026\COMMANDS.html`
(24,886 B). Doc 375 previous; that one is another session's and this does not restate it.*

---

## 0. WHAT TO DO

1. **The red team is scoped and the tasking file carries it.** `Source\REDTEAM_TASKING_PROMPT.md`
   has a SECTION C with four jobs. **Matt: the first one to send Fable is THE TAKE CONTRACT**, and
   it is on your list.
2. **Batch C of doc 374's catalog is SHIPPED, not described.** `Scripts\check_pages.py`, wired into
   `ff.bat` as step 7, pinned in `check_kit.py` from birth, ten negative controls run first.
3. **DOC 374'S BATCH C AS WRITTEN DOES NOT WORK AND MUST NOT BE QUOTED.** ~~"`{{`, `}}` and
   unsubstituted `{token}` in any built page"~~ produces **twenty-one false positives and zero true
   ones** on today's tree. Section 1 has the measurement and what shipped instead.
4. **A rule changed: the new jobs are NAMED, never numbered.** `JOB 4` already names two different
   things in two files. Section 2.
5. **Four of doc 374's eight batches are NOT Fable's.** A, B, E and F end in a guard on Matt's
   drive, which is section 0.4 work. They are recorded in the tasking file so nobody picks them up
   twice. Section 3.
6. **Section B's status is corrected: JOB 3 has RUN, JOB 4 has not, and JOB 4 is the one at risk of
   being marked done by mistake.** Section 2.

---

## 1. THE CATALOG SAID LINT FOR BRACES. BRACES ARE WHAT CSS IS MADE OF.

Doc 374 wrote batch C as *"`{{`, `}}` and unsubstituted `{token}` in any built page."* It is my own
catalog entry, written eighty minutes earlier, and I did not measure it before writing it. Section
0.2 says a diagnosis is a claim and must be tested before the fix; a **lint rule is a diagnosis about
a whole class of files** and the same rule applies to it.

**THE MEASUREMENT, RUN BEFORE A LINE OF THE GUARD WAS WRITTEN.**

| signature | hits across the six pages | true | false |
|---|---|---|---|
| `}}` anywhere | 20 | **0** | 20 |
| `{{` anywhere | 1 | **0** | 1 |
| `{token}` outside style and script | 0 | 0 | 0 |

**Every one of the twenty `}}` is a nested CSS close** -- `@media (max-width:640px){.secnav a{...}}`
and `:root{--ink:#eee;--ok:#3AA471}}` -- which is correct CSS that every page emits. **The single
`{{` is `MY_TODO.html`'s own prose**, the sentence describing the doc 369 bug: *"eleven CSS rules on
the commands page that shipped as literal `{{ }}`."*

**So the catalogued rule would have fired twenty-one times on its first run and been right zero
times.** That is not a noisy guard, it is a dead one: the second time a reader skips it, it has
stopped existing, and `check_vintage.py`'s own tolerance comment already says why
(*"flagging it would train the reader to ignore the guard"*).

**WHAT SHIPPED INSTEAD, four checks, each aimed at a defect this project actually shipped.**

| | what it refuses | the defect it comes from |
|---|---|---|
| **C1** | `{{` **inside a `<style>` block only** | doc 369. Two opening braces are never valid CSS anywhere; outside `<style>` they are usually somebody writing about the bug |
| **C2** | a `{token}` or a `%s` surviving into visible text or an attribute | the general case of C1, checked where a brace is not CSS and a percent is not a width |
| **C3** | a local `href` with no file behind it, resolved against **the page's own directory** | doc 353's commands link, doc 372's two pages with no way back |
| **C4** | a table cell whose whole content is `None`, `nan` or `NULL` | the rendered missing value. Doc 375's Pickens row is its cousin |

**TEN NEGATIVE CONTROLS, RUN FIRST, AND THE SECOND HALF IS THE HALF THAT MATTERS.** Six reproduce
defects that shipped and must fire: the doc 369 CSS verbatim in shape, a `{player}` in body text, a
`%s` in body text, a link to a file that is not there, a `nan` cell, and a page that was never built
at all. **Four reproduce the shapes that LOOK like those and must stay silent**: nested CSS closes,
`MY_TODO.html`'s prose about the bug, percentages beside an external link and an anchor and a
mailto, and a link that resolves beside a cell that is genuinely empty. `py check_pages.py
--selftest` runs all ten. **On the shipped tree it reports zero problems**, which is the correct
state for a guard whose controls prove it fires.

**AND THE ARCHIVE LINK WAS CHECKED RATHER THAN ASSUMED.** `Source\COMMANDS.html` links to
`../_archive/COMMANDS_Source_20260918_predraft.html`. In a partial copy of the tree that reads as a
dead link; on the drive the file is there, 47,036 bytes. **The check resolves against the page's own
directory, which is how a browser resolves it** -- resolving against the shell's working directory
is exactly how this check would have passed on Matt's machine and failed everywhere else.

---

## 2. `JOB 4` ALREADY NAMES TWO DIFFERENT JOBS, SO THESE FOUR HAVE NO NUMBER

The obvious move was to append doc 374's batches to the tasking file as `JOB 5` through `JOB 8`.
**The collision check (0.5(c)4) killed it.** `REDTEAM_TASKING_PROMPT.md` numbers its studies `JOB 1`
to `JOB 4`. The handover kits are numbered in a different file: `FABLE_HANDOVER_TEST.md` opens
*"FABLE JOB 6"* and says it *"replaces the JOB 5 kit in full"*, and an earlier kit shipped as doc
357 under the name `JOB 4`. **So `JOB 4` is already the riser-as-keeper study AND a handover test**,
and `AUDIT_LEDGER.md`'s standing note on it is *"the next kit should not be called JOB n."*
Numbering mine 5 to 8 would have put that collision into a third file.

**The jobs in section C are named by their subject and carry no number.** A name cannot silently
collide the way a number does. This is doc 146's two-names-for-one-job defect run backwards -- one
name for two jobs -- and it is the third time this project has paid for a shared identifier.

**AND CHECKING THAT TURNED UP A STATUS CORRECTION WORTH MORE THAN THE NAMING FIX.** The tasking
file's status box is dated 17 Sept and says *"JOBS 3 and 4 are queued."*

- **JOB 3 has RUN.** `FABLE_JOB3_seat_lane.md`, results in doc 352, ledger rows 114 and 115. Its
  Task B closed **DEAD on its own kill condition**: odds times rate did not beat odds alone.
- **JOB 4 is WRITTEN AND UNRUN**, and the ledger already flags it as the one most likely to be
  marked done by mistake, because a handover test carrying its name shipped as doc 357.

**A doc number collision costs an afternoon. A job-name collision costs a study that everyone
believes has been run.**

---

## 3. FOUR OF THE EIGHT BATCHES ARE MINE, AND SAYING SO IS PART OF THE SCOPE

Doc 374 listed eight batches and implied all eight append to the Fable tasking file. **Four of them
end in a guard committed to Matt's drive and pinned in `check_kit.py`.** That is section 0.4 work.
Handing it to Fable would be asking somebody else to do my job, dressed as delegation.

| batch | whose | state |
|---|---|---|
| **A** the page tells you what a number is | **mine** | not started. Doc 375 widened it: `half_ppr` scores neither passing nor kicking, so **every** consumer that differences it against a league-scored projection carries the defect. A's scope is now one league-scored column in `build_form`, which fixes `sheet_engine`, `wire` and `lineup` at once |
| **B** a base rate may not wear a player's name | **mine** | blocked behind the two-signal job below resolving whether that is a measurement or a label |
| **C** the generated-page linter | **mine** | **SHIPPED TODAY.** Section 1 |
| **D** which instrument governs a two-signal player | **Fable** | section C of the tasking file |
| **E** every hand-written constant that reaches a page | **mine** | not started |
| **F** the trackers | **mine** | not started |
| **G** the outside check | **Fable** | section C |
| **H** the directive itself | **Fable, last, different model** | section C |

**AND ONE BATCH WAS ADDED THAT DOC 374 DID NOT HAVE, because none of the eight answered what Matt
actually asked.** His words: *"The lack of consistency for player takes has been an ongoing issue
and we need it scoped fully."* A fixes the page's numbers, B fixes base rates, D fixes one
instrument. **Nothing audited the take itself.** So section C opens with **THE TAKE CONTRACT**: four
takes were wrong in twenty-four hours and **no two failed the same way** -- roster shape, the
fragility of the man ahead, a base rate quoted as a forecast, and a vintage. That is why "be more
careful" is not a fix, and it is the shape a five-part contract can catch and a rule cannot.

**The contract job carries its own population hole, stated in the brief (0.6):** a take made in a
reply and never written into a doc or the to-do file is not in the population and cannot be. That is
0.5(e)'s tracker defect one level up, and the job has to report how much of its own evidence it
could not see.

---

## 4. WHAT IS STILL OPEN, BY NAME

- **[OPEN] NOT YET RUN -- batch A**, now widened by doc 375 to one league-scored column in
  `build_form.py`. Testable form: *for each consumer of `half_ppr`, is the other side of the
  comparison league-scored?* Owner: me. This is the largest live one.
- **[OPEN] NOT YET RUN -- batches B, E and F.** Owner: me.
- **[OPEN] BLOCKED -- `LINEUP_CHECK.html` kickoff times and decision deadlines.** The exact missing
  input is a kickoff day and time per team per week; `Source\sched_2026.csv` carries only
  `week, team, opp, side`. Where it would come from: the league's own week schedule, which is
  already loaded for the pocket sheet. Tried: yes, on 19 Sept, and the column is not there.
- **[OPEN] NOT YET RUN -- `open_threads.py` still scrapes its own output**, 21 nested rows, 5 at
  four levels deep. Owner: me. It is batch F.
- **[OPEN]** The three online pages now link to each other in both directions. **`make_online.py`
  is written and tested in a container and is NOT on the drive**, so the online week sheet is
  republished by hand rather than by script. Owner: me.

*Sources: the six pages named in the population header above; `Scripts\check_pages.py` and its
`--selftest`; `Source\REDTEAM_TASKING_PROMPT.md` as it stood at 25,535 bytes before this edit;
`Source\AUDIT_LEDGER.md` rows 114, 115 and the JOB 4 row; `Source\FABLE_HANDOVER_TEST.md` first two
lines; docs 353, 369, 372, 374 and 375.*
