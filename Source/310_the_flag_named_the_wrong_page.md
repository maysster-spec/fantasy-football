# 310 -- the flag named the wrong page, and I gave him the command without it

**15 September 2026.** Matt ran the three commands exactly as written and asked what else was
needed. **Two of the three did their job. The third never touched the file he was trying to fix,
and the reason is a command I wrote.**

---

## 1. WHAT HIS RUN ACTUALLY PRODUCED

Verified on his own files, not on his word (0.5d):

| file | result |
|---|---|
| `Source\form_2026.csv` | **130,626 bytes, 2,236 rows, week 1 = 32 of 32 clubs.** LAR and WSH both present and joining. Doc 309's cache fix worked |
| `Source\WIRE_20260915.csv` | 22,131 bytes, 280 rows, **four new columns** (`snap_pct`, `w1_targets`, `tgt_share`, `form_sig`), **six rows tagged 2-of-3 or better**, 149 of 280 rows carrying a week-1 line |
| `Source\WEEK_SHEET.html` | **UNCHANGED. Same mtime as before the run.** |

## 2. THE CAUSE IS ONE LINE OF ARGPARSE AND IT IS OLDER THAN ANY OF THIS

```python
ap.add_argument('--html', action='store_true', help='also write THE_WEEKLY_WIRE.html')
...
if a.html:
    #  ... the whole WEEK_SHEET.html build lives in here
```

**One flag, named in its own help text after ONE artifact, silently gating the OTHER page -- the
one Matt reads every week.** `py wire.py` with no flag rewrites the wire and skips the sheet, and
says nothing about it: no error, no warning, no line in the console. **That is 0.2's exit-code rule
raised to the level of a command-line interface.** The previous sheet at 15:33 came from a run that
happened to carry `--html`, which is why nobody had noticed.

**AND THE PROXIMATE CAUSE IS 0.4, IN ITS MOST EXPENSIVE FORM: I put `py wire.py` in
`matt_todo.txt` and in the reply.** He ran precisely what he was asked, the page did not move, and
he had to come back and ask why. The directive's own words: *asking Matt to do something you could
have done is a defect of the same class as an unmeasured severity claim.* Asking him to run the
WRONG thing is worse, because it costs the round trip AND leaves him holding a stale page he has
every reason to believe is current.

## 3. THE FIX IS NOT "ADD THE FLAG"

Telling him to type `--html` repairs today and leaves the trap armed for every future session that
reads the help text and believes it. **So the gate is inverted instead:**

- **`WEEK_SHEET.html` is built by DEFAULT**, every run, whenever the roster read succeeds.
- **`--no-sheet`** opts out, and PRINTS that it did.
- **`--html`** now controls `THE_WEEKLY_WIRE.html` and nothing else, and its help text says so.

This also restores what doc 273 already claimed in prose -- *"the sheet rebuilds itself"* -- which
had been true only for invocations carrying a flag named after a different file.

**CONTROL, all four combinations, run against the patched parser:**

| command | WEEK_SHEET | THE_WEEKLY_WIRE |
|---|---|---|
| `py wire.py` | **BUILD** | no |
| `py wire.py --html` | **BUILD** | yes |
| `py wire.py --no-sheet` | SKIP (and says so) | no |
| `py wire.py --html --no-sheet` | SKIP (and says so) | yes |

## 4. WHAT THE PAGE NOW SAYS, BUILT FROM HIS OWN REBUILT FILES

Through the production writer, on his real roster and his 15 Sept wire:

| # | | | expected |
|---|---|---|---|
| 1 | **Dalton Schultz** | TE HOU | **11.1** |
| 2 | Malik Washington | WR MIA | 3.7 |
| 3 | Devaughn Vele | WR NO | 3.3 |
| 4 | Caleb Douglas | WR MIA | 3.3 |
| 5 | Kalif Raymond | WR CHI | 3.3 |

**Jalen McMillan, who took no snap in week 1, is off the list** (doc 304's defect, now closed by
measurement rather than by a demotion rule). The `a week` mislabel is gone from the page (row 48).

`wire.py` re-pinned **94658 / 36acbd6d3cdd0419**.

## 5. THE CLASS OF DEFECT, BECAUSE IT WILL RECUR

**Nothing in this project checks that the artifact a command is SUPPOSED to produce actually
changed.** `check_kit.py` pins scripts, not outputs. The missing-row check in 0.5(c)5 fires after a
build that HAPPENED; it has nothing to say about a build that silently did not run.
**NOT YET RUN, and it is the general form of this:** a step in the weekly sequence that records each
rendered page's mtime before and after, and names any page that did not move. That would have caught
this in the same second it happened, and it would also have caught doc 146's PDF builders exiting 0
without a renderer.
