# 296 -- the man who inherits must be a man who is playing

**12 September 2026.** Batch 1, second half. The first job of the day was the verification the
Saturday routine asks for, and it found a live wrong recommendation on the page Matt reads. That
is one whole item and it is finished; what it displaced is named at the end.

---

## 1. The pages rebuilt, and ten audit rows closed

Matt ran `ff.bat` twice on 11 Sept: 18:27, before the rebuild, and **20:14, after it**. The second
run carried every change from doc 295 and **the sheet opened by itself** (`SHEET OPENED` in the
log), which is the first live proof of that feature. Three pages written, both exits 0, no
traceback, `FREE_UNRANKED_20260911.csv` written with 71 off-board free skill players.

**Verified on the live pages by name, not by row count (0.5c5):** section 0 with the ranked move ·
the ruled-out block quoting his own DO NOT line · his to-do items · the watch list · the Kaelon
Black card · Mike Washington priced as Jeanty's handcuff · Hockenson in the drop table · the week-6
tight-end hole · 80 names carrying a hover tooltip · the footer reading `sheet_engine.py 72,267
bytes`, which is the file committed last night.

**`AUDIT_LEDGER.md`: rows 9, 10, 11, 12, 14, 15, 16, 17 and 23 grep clean and are CLOSED.**

**Row 13 closed too, and its TOKEN was wrong.** The token `class="p">Tyjae Spears` still matches,
in the **free pool** table, where Spears belongs: Matt dropped him and nobody claimed him. The drop
table itself is rebuilt from the roster and lists Hockenson. **A grep token that also matches a
legitimate row can neither close a row nor hold one open**, and this one would have held row 13
open forever.

---

## 2. THE DEFECT: the stash list named a man who was not playing

The wire's "One injury away" list named **Jordan James** as the back who would inherit
**McCaffrey's 303-point job**. Two things were wrong with that row:

* **ESPN's own pool, in the same run, had James OUT** (free, 2.1% rostered, status OUT).
* **He did not play in week 1.** PFF, 10 Sep 2026: James was inactive, so Kaelon Black had won the
  backup job in camp; Black led the team in carries. Yahoo, 11 Sep 2026: Black 16 snaps to
  McCaffrey's 15 in the first half.

**A man ESPN lists OUT is not one injury away. He is two.**

**And this is the two-lists defect, not a one-off.** The week sheet's seat box reads
`inherit_2026.csv`, which I corrected to Black last night. The wire's stash list reads
`depth_map.csv` through `next_man_up()`, which I did not, because I did not know it existed as a
second source. **Two files answer "who is behind this job" and only one of them was fixed.** That
is 0.5(c)4's collision rule applied to DATA rather than to filenames.

### The diagnosis was reproduced before the fix was written (0.2)

Testable form, stated first: *on the recorded 11 Sept pool, `next_man_up` names a man ESPN lists
OUT as the inheritor for at least one team, where a healthy back at the next depth on the same team
is free.* Run against `load_depth()`, the object production builds, not an equivalent one:

```
Brian Robinson Jr.  ATL  Bijan Robinson        315  ACTIVE
Jordan James        SF   Christian Mccaffrey   303  OUT        <-- reproduces the live page
DJ Giddens          IND  Jonathan Taylor       291  ACTIVE
Ty Johnson          BUF  James Cook III        262  QUESTIONABLE
```

The first four rows match the live page exactly, so the harness is exercising the real thing.

### The fix, and the one it replaced

`next_man_up()` now steps past a depth tier **only when every free man in it is somebody ESPN says
is not playing** (OUT, injured reserve, suspension, not active). `DOUBTFUL` and `QUESTIONABLE` stay
out of that set deliberately: a questionable back plays most weeks, and a stash is a bet on the
season, not on Sunday. The rule that an **owned** handcuff drops the whole team is untouched, and
the page now prints whom it stepped over: *"ahead of him Jordan James (out), so he is not the one
who inherits this week."* `in_doubt()` carries the same filter, because a cover who is himself out
covers nothing.

**MY FIRST VERSION OF THIS FIX WAS WRONG AND THE TEST DESIGN HID IT.** It computed the top depth
among FREE men rather than all men, which silently reversed the deliberate "an owned handcuff means
the team drops off" rule and surfaced third-stringers. I did not see it because I diffed the
patched function against *itself with the argument omitted* instead of against the shipped file.
**Against the shipped file the corrected fix moves exactly one team of thirty:**

```
teams whose named man changed: 1     SF: Jordan James -> Kaelon Black
teams dropped: none                  teams added: none
rows naming a man who is not playing: shipped 1 -> fixed 0
```

### Control C17, and it fires

Added to `Scripts\research\redteam\redteam_controls.py`, which now runs **44 checks**. With James
planted OUT in the recorded pool:

* the pre-change tree: **41 of 44**, the three new checks failing, the stash column naming James.
* the fixed tree: **44 of 44**.

**The first version of the CHECK was loose too** -- `'Jordan James' not in block` failed on the
fixed code, because the fix prints his name in the reason. It reads the first cell of each row now.
That is ledger row 13's defect in the opposite direction, on the same morning.

---

## 3. What this does NOT fix, and it is the bigger half

The code now refuses to name a man who is not playing. **It still cannot see who actually got the
work.** The stash order is a preseason depth chart: `depth_map.csv` has Black at depth 3 behind
James at depth 2, four days after Black played and James did not.

**NOT YET RUN, testable form and inputs named (0.5a4):** *re-derive each team's backfield depth
order from realised week-to-date usage (carries plus targets) rather than the preseason chart, and
check on 2021-2025 whether the usage order predicts the next absence's inheritor better than the
preseason order does.* Inputs: nflverse weekly player stats for the history, and for the live
weekly order either the same release or the ESPN box scores Matt's own pull already reaches. **Not
blocked; queued.**

---

## 4. One thing to correct in the to-do list, from his own pull

`matt_todo.txt` says two backfield seats were claimed on 11 Sept, **Jordan James (SF) and Brian
Robinson Jr. (ATL)**. His own 20:14 ESPN pull has **both of them free** in his league: James at
2.1% rostered and Robinson at 26.3%, and Robinson is the top row of the stash list. Whatever
happened, they are available now. The line is corrected.

---

## 5. What moved, and what did not

**Done:** the page verification and the ten ledger rows · the stash defect found, reproduced,
fixed, controlled and committed · `wire.py` 82,366 bytes, `redteam_controls.py` 20,159,
`check_kit.py` re-pinned, all archived first.

**Not started, and displaced by this:** A1 (the injury model), F2, F1, F3, B5, B9. A1 is still the
right next item and nothing here changes its shape.

**Waiting on Matt:** one more `ff.bat` run puts the corrected stash list on the page and closes
ledger rows 22 and 24. And the Kaelon Black decision from doc 295 is still his.
