# 372. ONE NAV FOR FIVE PAGES, THE FORCED NEW TAB REVERSED, AND THE PART OF THE WIRE THAT NEVER REBUILDS

*19 September 2026. Batch 2 of the page red team. Matt, after testing batch 1: "i don't wish to open
a new tap to return back to the home page... The home page should act like a home page" and "i prefer
to replace the page instead of loading a new page... Otherwise i'll end up with a clutter of pages
open in Google Chrome." Population note (0.6): page content below is the Friday 18 Sept 08:57 build;
the generator changes were tested by building the pages that can be built without an ESPN pull.
Doc 371 is the previous number.*

---

## 0. WHAT TO DO

1. **Matt: run `.\ff.bat`.** Already on your list, and it now carries batch 2 as well as batch 1.
2. **The wire and the lineup check have a way home.** Both had none. Both now carry the same bar as
   every other page, with the week sheet first and marked as the way back.
3. **Every forced new tab is gone, everywhere.** Batch 1 added them; you tested and said no; they
   are removed. Middle-click and ctrl-click still open a new tab, which is your choice per link
   rather than mine for all of them. Section 1.
4. **The week sheet is the right home and I am not proposing another.** Section 1 says why in a line.
5. **A live defect on the wire, and it is why the page feels stale: its top block is hand-written
   and `ff.bat` cannot rebuild it.** It tells you to run a command that is no longer the command,
   and it asserts a claim-processing day that contradicts your settings file. Section 3.
6. **BLOCKED, one missing column: `sched_2026.csv` has no kickoff day or time**, which is the single
   enhancement that would have saved last night's kicker analysis. Section 4.

---

## 1. ONE NAV, AND THE NEW-TAB REVERSAL

**The nav is now a function, `sheet_engine.page_bar()`, and all five pages call it.** Before this,
three pages carried hand-written bars and two carried none. **Five copies of one bar is a second
NAME for one JOB**, which §0.5(c)4 names as the same defect as two files claiming one number, and
the two pages with no bar at all are exactly the dead ends Matt had to back out of.

The bar renders the current page as plain text rather than a link, so **no page links to itself**,
and the week sheet renders as `&larr; week sheet` everywhere else.

**THE FORCED NEW TAB IS REMOVED AND THE OUTSIDE CHECK SAYS MATT IS RIGHT (§0.5(c)6).** Batch 1 set
`target="_blank"` on cross-page links, reasoning that it protected the page you came from. Matt
tested it and rejected it. **The published guidance agrees with him, not with batch 1:** WCAG 2.2
success criterion **3.2.5 Change on Request** treats opening a new window without warning as a
failure, and Nielsen Norman Group's long-standing position is that forcing new windows takes the
back button away from the user. **So this was not a house-style preference that we differed on by
choice. It was a defect, and differing by accident is the thing (c)6 exists to catch.** Zero
`target="_blank"` remain in any of the four generators.

**ON HIS QUESTION "unless you recommend another option that is superior": no, the week sheet is the
home.** It is the only page that carries a decision rather than an input, it is the page `ff.bat`
opens when something changed, and it is the one he named. A separate index page would be a sixth
page to keep current, and §9 already records that every hand-maintained map in this project went
stale within hours.

---

## 2. WHAT WAS TESTED, AND WHAT COULD NOT BE

**Built for real:**
- `MY_TODO.html` from the live `matt_todo.txt`: 46 open items, count guard passing, the bar present,
  no self-link, no forced new tabs.
- `COMMANDS.html` in a mirrored tree with the five real batch files: the bar resolves every href
  through `Source/` because that page sits one folder up, and its own entry correctly renders as
  text rather than a link. That prefix case is the one most likely to break and it is the one the
  test exercises.
- **`LINEUP_CHECK.html` rendered by its own `page()` function**, with `requests` stubbed so the
  renderer under test is the real one and not a copy of it (§0.2: build the object production
  builds). Bar present, links home, does not link to itself, stylesheet inlined.
- `py_compile` with `-W error::SyntaxWarning` on all four, which is doc 144's Python 3.12 trap.

**NOT built: `WEEK_SHEET.html` and `THE_WEEKLY_WIRE.html`.** Both renderers need a live ESPN pull.
`wire.py` was imported and its two new names confirmed bound, and the edited line was read back, but
**the wire page itself has not been rendered since the change and that is the honest gap.** It is
one `ff.bat` away from being closed.

---

## 3. THE WIRE IS REBUILT. ITS TOP BLOCK IS NOT.

Matt: *"i don't remember the last time this page was updated so that current, relevant and valuable
information is included and included in the correct order."*

**THE DATA IS CURRENT. `ff.bat` rewrites `THE_WEEKLY_WIRE.html` on every run.** So the feeling is not
about the pool or the stash list.

**IT IS ABOUT THE TOP OF THE PAGE, WHICH IS A HAND-WRITTEN CONSTANT.** `wire.py` holds
`STATIC_TOP` (4,391 characters) and `STATIC_BOTTOM` (2,731). They are pasted into the page verbatim
on every build, so **no rebuild can ever make them current**, and `STATIC_TOP` is the first thing on
the page after the headline. Two things in it are wrong or unsourced:

1. **It tells him to run the wrong command.** *"Tuesday morning: run `py wire.py`."* `ff.bat` has
   been the one command since 17 September, it runs the wire itself, and a scheduled task already
   fires it Tuesday 06:00. **The page instructs a human to do a thing a scheduler already did.**
2. **It asserts a claim-processing day that nothing here sources.** *"Claims settle early Thursday
   morning."* `2026_League_Settings.txt` gives `Waiver Period: 2 Days` and names no day.
   **[OPEN] These two cannot both be relied on, and it is decision-relevant right now**: I quoted the
   two-day figure at Matt last night when he asked how long his Coleman claim would sit. Only the
   ESPN league page settles it, which is a §0.4 category-four lookup.

**THE GENERAL RULE THIS EARNS, and §0.5(f) says it goes in the instruction rather than only here:
a constant pasted into a generated page is not generated.** Every guard this project has ever
written checks that a page was rebuilt. None checks whether the parts that cannot rebuild are still
true. **NOT YET RUN**, testable form: *list every hand-written constant that reaches a rendered page,
and for each, name the fact it asserts and where that fact is checked.* Candidates already known:
`STATIC_TOP`, `STATIC_BOTTOM`, and the standing-rules block on the week sheet.

---

## 4. THE LINEUP CHECK: WHAT IT SHOULD SAY, AND THE ONE COLUMN THAT STOPS IT

Matt: *"consider enhancements that provide more context and information on player status when in
question."*

**THE HIGHEST-VALUE ADDITION IS NOT MEDICAL, IT IS THE CLOCK, AND LAST NIGHT PROVED IT.** The page
said `Eddy Pineiro, K, SF, Questionable` and stopped. Everything that made that decision hard was
absent: **his game was at 4:25, his inactive posted at 2:55, and every free kicker played at 1:00.**
The page had the player and not the deadline, so the deadline had to be reconstructed by hand from a
schedule page on the web.

**BLOCKED, one column.** `Source\sched_2026.csv` is 544 rows of `week, team, opp, side` and carries
**no kickoff day and no kickoff time**. Without it the page cannot say when a decision is due.
Tried: read the file's columns; checked `injuries_2026.csv`, which is week 1 only and cannot help.

**WHERE IT COMES FROM, and it is closer than it looks:** `lineup.py` already authenticates against
ESPN's API on Matt's machine, and the scoreboard payload carries kickoff times. So this is a build
rather than a true block: either add kickoff to `sched_2026.csv`, or read it from the payload the
script already fetches. **Mine to write, and it is the next thing in this lane.**

**THE THREE ADDITIONS, in the order they are worth doing:**
1. **Kickoff and the decision deadline** for every questionable man, plus the deadline for the
   position as a whole when his replacements play earlier than he does. That last clause is the one
   that mattered last night and no page in this project computes it.
2. **The best bench swap and what it costs**, in the same units as the week sheet's bar, so sitting
   a man is priced rather than guessed.
3. **Mark the men whose week is already over.** LaPorta played Thursday. He should not appear on a
   Sunday decision page at all.

**Practice participation stays out**, and that is deliberate rather than an omission: the only file
holding it is `injuries_2026.csv`, which covers week 1 and nothing rebuilds it, so a page showing it
would be showing a fortnight-old report as though it were today's.
