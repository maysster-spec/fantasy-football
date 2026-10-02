# 274 — The weekly conversation, and what it needs from him

2026-09-10. Matt: *"how should we start that discussion? what do you need from me"* — on the one
part doc 273 left with me: the page cannot read news, cannot see a starter limp off, and cannot
judge whether a gap is real.

**The short answer is that it needs almost nothing from him, and that is the design.** If the
weekly loop depends on him remembering to start it, it is the same failure doc 273 just fixed one
level up — a process that only runs when asked.

---

## So it starts itself

**Scheduled task created: "Tuesday wire read — the judgement layer", Tuesdays 8:05am Eastern,
bound to his computer.** It fires two hours after `ff.bat TUE` has rebuilt the sheets, which puts it
ahead of Wednesday's claim window (doc 213: ESPN processes daily at 3–5am ET, concentrated into
Wednesday and Thursday by the NFL calendar).

Each firing is a fresh session with no memory of this one, so the instruction is standalone. It:

1. **Reads `ff_log.txt` first.** If this morning's run wrote `*** NO ... ON DISK`, that is the
   headline and nothing else matters. The judgement layer checks the artifact before it trusts it.
2. **Diffs this week's `WIRE_<date>.csv` against last week's.** Who newly entered the free pool is
   the whole point of a weekly run — it is exactly what Matt named: *"people will drop players."*
3. **Does the half a script cannot** — web search on every man on `MY_ROSTER.csv` and on the newly
   free names carrying a `screen` or a `flags` value, with every source's publication date stated
   before use (`ERROR_PATTERNS` B7).
4. **Sends a short read** in §0.1 form: the one move, or "no move" said plainly; anyone newly free
   who clears a screen this project has already measured; anything the news changed on his roster;
   and whichever dated item on `matt_todo.txt` falls due that week.

**The boundaries are in the task's own text and they are absolute:** it does not file a claim, does
not drop anybody, does not write to ESPN, does not spend his priority. §0.4's four categories, in
the instruction rather than in a doc where a fresh session might not reach them.

**And it fails loudly.** If his computer is not reachable, the run says so in one line, does the news
half from the web alone, and names which half is missing — rather than sending a confident read
built on last week's files.

---

## What it needs from him

**Weekly: nothing.** That is the point.

**When it happens, and only then, three things no file on the drive can hold:**

1. **Something he saw that is not in a file.** A starter limping off, a beat writer's line, a trade
   offer, a coach's press conference. The projection pull is a Sunday-night snapshot; his eyes are
   not.
2. **A decision he has already made that the files do not know.** "I'm holding Washington whatever
   the number says" is an input, not an argument — and it saves a session from re-deriving a
   recommendation he has already rejected. That exact sentence saved one this week.
3. **A hunch to test.** This is the highest-yield input in the project by a distance and it is worth
   saying so plainly: on mechanisms he has proposed, the honest count is **12 confirmed or partly
   confirmed, 1 underpowered in his direction, 7 null** (§0.5(a), doc 243). Better than a coin flip
   on the mechanism, and on the narrower question *"is this answerable at all?"* he has been right
   nearly every time. The hot kicker went from *"not sure it works"* to a measured **+1.25 a week**
   in one afternoon.

**And the standing one: when he thinks a number is wrong.** His record there is close to perfect —
Lloyd's −90, Jacobs' bench spot, Adams at 32, the empty ladder page, the market-anchor read, my own
test design, and this week the kicker pool I called flat on a projection that turns out to be worth
almost nothing. **A price or a process he says is wrong is evidence, not an objection.**

---

## What that leaves genuinely open

- **Not yet run:** the Tuesday task has never fired. Next run **2026-09-15, 8:05am ET**. Like
  everything shipped yesterday, it is tested by construction and not by execution, and the first
  firing is what makes it real.
- **Open, deliberately:** no Thursday task. `ff.bat` rebuilds the sheets Thursday at 5:30pm ahead of
  Thursday's waiver run, so the numbers are there — but a second Claude read has not been argued
  for, and four scheduled runs a week from one league is already close to the line where a report
  stops being read. **One task, one week, and add the second only if the first proves it is needed.**
