# 454. THE PROJECTION IS PULLED ONCE A DAY NOW, AND THE ONCE-A-WEEK RULE WAS MINE

*30 Sept 2026, 00:30 ET. Claude (Cowork). Matt, 29 Sept: "why is the pull step limited in the first place. Is there harm
running it less than five days apart for example?" 454 reserved by listing `Source\` (453 is the screen doc). No em dashes.*

---

## 0. WHAT TO DO

1. **No harm, and the limit is gone: every run pulls when the newest pull is more than half a day old** (one pull a day at most,
   on whichever run comes first; the Tuesday task always pulls). The five-day gate of doc 451 lasted three hours. Nothing to run.
2. **After each pull the log says what ESPN moved** (`proj_due.py --report`: players in both pulls, how many season projections
   changed, the five biggest moves), so by mid-October the log is ESPN's cadence, measured, instead of my assumption of it.
3. **Source\ keeps the newest three pulls; older in-season pulls move to `_archive\projections\`** (the CSV and its raw JSON;
   moved, never deleted; the draft-era pulls of August and September stay, because `depth_map.py` reads one of them by name).
4. **The reason for the limit was two claims, one trivial and one untested.** A pull writes 5.6 MB (5.1 of it the raw JSON) and
   takes seconds; at one a day that is about 40 MB a week, which the prune keeps out of Source\. "ESPN re-projects once a week"
   was never measured; the only pairs on file are preseason (3 to 5 Sept, and two the same morning) and ESPN moved nothing between
   them, while the 5 to 24 Sept pair moved 419 of 422. So ESPN is not churning by the hour, and a daily pull will often bring back
   the same numbers; the cost of that is nothing, and the cost of the alternative was on the sheet last night.

---

## 1. WHAT WAS MEASURED, AND WHAT WAS NOT

Three pairs of pulls compared on `proj_2026` (the rest-of-season projection): 5 Sept 08:00 to 10:40, 0 of 499 players changed;
3 Sept 09:02 to 5 Sept 08:00, 0 of 499; 5 Sept to 24 Sept, 419 of 422 changed, median move 15.5 season points, the largest
Jameis Winston 10 to 245 and Marvin Harrison 159 to 88. All three are preseason or straddle the start; there is no in-season
pair on file, so the in-season cadence is NOT MEASURED and the report line is how it gets measured, one run at a time.

`proj_due.py`: the gate at 0.5 days (three controls), `--report` (one control), `--prune` (keeps the newest three by the stamp
in the file name, skips a file already in the archive, leaves anything stamped before 10 Sept and the league projection file;
two controls, and a dry run on the real September pulls moved exactly the oldest and left the rest). `ff.bat` runs the report
and the prune only after a pull that exited 0. Both scripts re-pinned.

## 2. OPEN, BY NAME

- **Matt's:** nothing from this doc.
- **Mine, waiting on events:** the 07:30 run (the first pull under the new gate, the first report line, the first prune of the
  24 Sept pull once three newer exist); the in-season cadence read off the log after two or three weeks.
