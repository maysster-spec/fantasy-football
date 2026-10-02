# 345 — THE CAP ATE THE ROW THE PAGE WAS SHOUTING ABOUT, AND NOTHING PINNED THE HARNESS

**2026-09-18, 03:1x EDT.** Continues doc 344 (the section-A red team) and doc 316. Three things:
the drive copies of everything written on 17 Sept verified BY CONTENT; doc 316's cap exception
restored to `sheet_engine.py` with a control that was shown failing first; and the harness pinned.

---

## 1. THE VERIFICATION MATT ASKED FOR — BY CONTENT, NOT BY THE COMMIT RESULT

Every file written on 17 Sept was staged back off the drive and hashed on normalised bytes
(`sha256(bytes.replace(CRLF, LF))[:16]`), then read for the FEATURE, not only the hash.

| file | drive bytes | normalised | pin | verdict |
|---|---|---|---|---|
| `Scripts\sheet_engine.py` | 115,530 | 115,530 | `e951cbd7dbceae3c` | matches |
| `Scripts\wire.py` | 110,233 | 110,233 | `c54f62930b739842` | matches |
| `Scripts\todo_page.py` | 3,583 | 3,583 | `bae0db33217a6a89` | matches |
| `Scripts\ff.bat` | 4,939 | **4,846** | `d554b881cf1ee72e` | matches — the 93 bytes are CRLF |
| `Scripts\research\wk1\job_opens.py` | 9,050 | 9,050 | `29bec3ab533069a4` | matches |

And by feature, not by hash: `wire.py`'s three `load_form()` early returns all return THREE values
(the crash of doc 342); `sheet_engine.py` carries `seat_odds`, `load_todo_all`, `write_todo_page`,
`_todo_kind`, `TODO_LINKS`, `TODO_CMDS`; `sheet_constants.json` carries `p_opens_by_band`
(0.476 / 0.438 / 0.533 / 0.636 on n = 42 / 32 / 30 / 22) and the `weeks_played_note` recording the
claim that died; `inherit_2026.csv` carries `wk1_share`, `wk1_work` and `wk1_band`, 25 of 32 rows
filled. `check_kit.py`'s pins for all five files agree with the bytes on the drive.

**ONE CORRECTION TO MY OWN SUMMARY.** I wrote that the seven unjoined rows are blank and that no
row is zero. **There IS one zero row: Dylan Sampson, `wk1_share` 0.000.** That is the case
`seat_odds` routes to the flat 0.46 with the "on the field in week one and touched the ball no
times" note, which is right — doc 343's zero-touch population went 0 for 41 — but the sentence I
wrote about the data was wrong and the code was not.

**AND I RE-RAN THE HARNESS MYSELF RATHER THAN TAKE THE REPORT'S WORD: 56 of 56 against the drive
copies**, C18 to C21 present and passing. Doc 344's restore is confirmed by execution.

---

## 2. DOC 316's CAP EXCEPTION — RESTORED, AND THE DEFECT REPRODUCED BEFORE THE FIX

**THE CLAIM, STATED BEFORE THE RUN (§0.5 a2).** *On the harness's recorded pool, a free man whose
contest band prints "Put him first" (10+ carries and targets in his last game) ranks BELOW fifth on
worth, so `now[:5]` drops him from "Priority pickups, in order" while his own warning says he is the
one claim that has to spend the priority. With the exception restored he is shown, WITH the
sentence, and the first five are unchanged in identity and order.*

**REPRODUCED, unmutated, on the frozen 10 Sept pool.** Probing the full list the cap slices:

```
 1 Broncos D/ST     worth 25.6   touches  -    no band
 2 Brandon Aubrey   worth 22.1   touches  -    no band
 3 Dalton Schultz   worth 11.1   touches  8    29% contested
 4 Michael Mayer    worth 11.1   touches  7    29% contested
 5 Malik Washington worth  3.7   touches  8    29% contested      <- the cap cuts here
 ...
12 Kaelon Black     worth  1.5   touches 15    56% contested      <- the only claim-first row
```

**Kaelon Black — the player Matt named on 16 Sept — is twelfth on worth and the only row on the page
that earns "Put him first".** Doc 316 recorded him sixth at 2.4 against a fifth place of 3.3; on
today's inputs he is twelfth at 1.5. Same defect, different depth, and I am quoting the number I
measured rather than doc 316's.

**THE ELEVEN LINES ARE BACK**, from `_archive\sheet_engine_20260916_0300.py`, with one change: the
local is `_picks_shown`, not `_shown`. **`_shown` is already a live local in the seat-table block
seventy lines above, in the same function** — the archive's name would have shadowed it. That is
the kind of quiet reuse this project pays for later, and it was found by grepping the name before
pasting rather than after.

**THE RE-ADMIT KEYS ON THE SENTENCE, NOT ON THE 0.38 THRESHOLD, AND THAT IS DELIBERATE.**
`contest()` decides in one place whether a man is told to go first. A second copy of the number here
could drift from it silently, and a row re-admitted without the sentence would be this defect
inverted. **It also means doc 344's finding 3 — that the printed band is P(2+ claims | someone
filed) and the claimant's-seat rate is 30 / 56 / 68 / 82 — needs no second edit here: re-cut the
sentence and the re-admit follows it.**

**THE CONTROL WAS SHOWN FAILING FIRST (§0.2).** New `C23`, four checks, run against the 17 Sept
shipping `sheet_engine.py` (pin `e951cbd7dbceae3c`, `now[:5]` with no exception):

```
PRE-RESTORE   [PASS] the section was found at all
              [FAIL] a man the page says to claim first is ON the priority list
              [FAIL] and his claim-first sentence is printed, not just his row
              [PASS] the re-admit did not promote him: he is not in the first five
              58 of 60 checks pass
POST-RESTORE  all four PASS,  60 of 60,  order ['Broncos', 'Brandon Aubrey', 'Dalton Schultz',
              'Michael Mayer', 'Malik Washington', 'Kaelon Black'] — the five unchanged
```

**AND THE FIRST VERSION OF C23 PASSED AGAINST THE CODE IT WAS WRITTEN TO FAIL.** My `page_section`
helper found the heading and returned `txt[i:]` — the whole rest of the page — so it found Black in
the SEAT TABLE further down and called that a pass. A helper that cannot bound its own section now
returns nothing rather than everything, and says so in its docstring. **A control that has never
been shown firing is not a control, and mine nearly shipped as one.**

---

## 3. WHAT IS LIVE ON TONIGHT'S PAGE, AND THE ONE NAME DOC 344 GOT WRONG

Doc 344 says "Black is cut at sixth tonight." **He is not in the priority lane tonight at all** — he
is on the 17 Sept page in the SEAT table (McCaffrey's job, 302.4, 46%), and `WIRE_20260917.csv` does
not carry him. The defect is live; the player is not.

**The live 17 Sept page prints "Put him first" ZERO times**, and its five pickups are all 29%
contested. Three free men on that night's wire clear the threshold:

| man | carries + targets, last game | band |
|---|---|---|
| Tyler Allgeier, ARI | 19 | **56% contested** |
| Woody Marks, HOU | 10 | 40% |
| Emmett Johnson, KC | 10 | 40% |

**Whether the restore re-admits them depends on their worth rank, which needs the live free pool
and therefore Matt's ESPN session. NOT YET RUN, and it is one `ff.bat` away.**

**SEPARATE, AND IT QUALIFIES ALL THREE ROWS ABOVE: the workload lane is reading WEEK ONE on
17 September.** `form_2026.csv` holds weeks 0 and 1 only — and so does its source,
`stats_player_week_2026.csv`, downloaded 17 Sept 21:33, and `snap_counts_2026.csv` with it. So the
page is not stale against what it could have; **nflverse's 2026 weekly release was a week behind the
calendar last night.** `py research\wk1\build_form.py` is the test and it needs internet, which is
why `ff.bat` deliberately does not run it. `[NOT YET RUN — the input is named]`

---

## 4. THE HARNESS IS PINNED FOR THE FIRST TIME

Doc 344's most useful fact: 16 Sept 08:05 held 44 checks, 19:15 held 56, and 17 Sept 21:30 held the
08:05 BYTES AGAIN, hash-identical. **Four controls vanished and nothing made a sound, because
nothing pinned the file.** `redteam_controls.py` now has a `check_kit.py` entry —
`(32148, '6e042353879fe338')`, 60 checks, C0 to C23 — under a nested name in `SCRIPTS`, which
resolves because the `Scripts` folder is not an exact set. Verified by running `check_kit.py`
against the patched tree: both new entries report `ok`.

**AND ONE COMMENT IN `check_kit.py` CITED A CONTROL THAT WAS NEVER WRITTEN.** It said the
LOAD_PROBLEM branch was *"Verified by C22 and C22c in redteam_controls.py, 65 of 65."* The harness
runs 60 checks and contains no C22 at any version in any archive. Per §0.5(a4) it now carries one of
the three answers instead of a false one: **NOT YET RUN, with the testable form written into the
file** — mock `kona_player_info` returning `{'players': []}` and assert the wire page prints the
load-problem line rather than reading an empty pool as "nobody is free". **The pin proves a file has
not changed and nothing about whether what is in it is true — doc 321's lesson, one level up.**

---

## 5. WHAT WAS WRITTEN, AND HOW IT WAS VERIFIED

| file | pin after | verified |
|---|---|---|
| `Scripts\sheet_engine.py` | **116,976 B `78a1c4d945c95f49`** | staged back, content matched |
| `Scripts\research\redteam\redteam_controls.py` | **32,148 B `6e042353879fe338`** | staged back, content matched |
| `Scripts\check_kit.py` | **36,672 B `42c106595360fef0`** | staged back, content matched |
| `_archive\sheet_engine_20260917_1709.py` | 115,530 B `e951cbd7dbceae3c` | staged back, content matched |
| `_archive\redteam_controls_20260917_1840.py` | 29,356 B `8ef338e6e95c0393` | staged back, content matched |
| `_archive\check_kit_20260917_1709.py` | 35,084 B `01c5a45d19bdf492` | staged back, content matched |

All six committed from a container path created this session and read back off the drive before
being called done — ledger row 89's rule, applied and passed.

---

## 6. OPEN, BY NAME

- **The contest sentence re-cut on the claimant's-seat rate** (30 / 56 / 68 / 82). The cap exception
  follows it automatically; the sentence itself does not.
- **C22, the LOAD_PROBLEM control.** Form written into `check_kit.py`. `[NOT YET RUN]`
- **Whether tonight's three claim-first men are re-admitted on the live pool.** Needs `ff.bat`.
- **Whether nflverse has NFL week 2 yet.** Needs `build_form.py`, which needs internet.
- `matt_todo.txt` and `waiver_report_2026.csv` on the harness copy list — the DO NOT lane has never
  been exercised by a control (doc 344).
- The rest of doc 344's list: the ladder's K and D/ST double count, the "floor" rounding on the
  Browns row, the seat rate as pooled per-game times P(he is the man), the script behind
  `relief_ppg` 12.13 and `weeks_played` 3.02.
