@echo off
REM ---------------------------------------------------------------------------
REM  refresh_pull.bat  --  the Sept 5 (and any other) projection refresh.
REM  Point Windows Task Scheduler at THIS FILE. It needs no AI session, no cloud,
REM  and no network permission beyond what your browser already has.
REM
REM  Task Scheduler -> Create Basic Task -> Trigger: One time, Sat Sep 5 2026 08:00
REM  -> Action: Start a program -> Program:  this file's full path
REM  -> Finish. Tick "Open Properties", then "Run whether user is logged on or not"
REM     is NOT needed -- leave it as "Run only when user is logged on" so the
REM     ESPN cookies in the script are used under your own profile.
REM
REM  doc 81: the board-order test is now GATED. The pull script's PULL REJECTED
REM  guard only PRINTS -- it still writes the CSV and still exits 0. Ungated,
REM  sept5_check.py would pick up the corrupt file (it takes the newest) and print
REM  an authoritative FREEZE/REBUILD computed on garbage. The VERDICT line is the
REM  one thing you are told to read, so it must never be produced from a bad pull.
REM ---------------------------------------------------------------------------
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
echo ============================================================
echo  ESPN projection refresh  --  %DATE% %TIME%
echo ============================================================
echo.
echo Pulling. Output goes to pull_log.txt; this takes a minute.
py Espn_pull_projections.py --seasons 2026 --sort draft --yes >> pull_log.txt 2>&1
set PULLRC=%ERRORLEVEL%
echo Exit code %PULLRC% >> pull_log.txt

if not "%PULLRC%"=="0" goto :badpull
findstr /c:"PULL REJECTED" pull_log.txt >nul && goto :rejected

echo.
echo Pull OK. Running the board-order test against the new pull...
echo ============================================================
echo. >> pull_log.txt
echo ==== BOARD-ORDER TEST ==== >> pull_log.txt
py sept5_check.py > sept5_last.txt 2>&1
type sept5_last.txt
type sept5_last.txt >> pull_log.txt
echo ============================================================
echo.
echo Read the VERDICT line above. FREEZE = nothing to do.
echo.
echo If it says REBUILD: the new board is built from the pull and will NOT carry the
echo news overrides. After rebuilding, run  py apply_news.py --write  then
echo py board_audit.py  and  py make_fallback.py  -- in that order. (doc 101)
echo Everything above is also saved in pull_log.txt -- nothing is lost if this closes.
goto :hold

:badpull
echo.
echo  *** PULL FAILED, exit code %PULLRC%. ***
echo  *** The board-order test was NOT run -- it would have tested the PREVIOUS
echo  *** pull and printed a VERDICT that means nothing.
echo  *** Read the end of pull_log.txt, then just run this file again.
echo  *** A 401/403 there means the ESPN cookies need refreshing.
goto :hold

:rejected
echo.
echo  *** PULL REJECTED by the script's own integrity guard. ***
echo  *** Fewer than 400 players came back with a projection -- this is the 2023
echo  *** failure mode (doc 56). ESPN is nondeterministic here.
echo  *** The CSV was written for inspection but MUST NOT be used.
echo  *** The board-order test was NOT run. Just run this file again.
goto :hold

:hold
echo.
REM  timeout, NOT pause. `pause` waits forever for a keypress, which leaves the
REM  scheduled task stuck in "Running" and the window open if nobody is at the
REM  desk. This keeps it readable for 10 minutes, closes on any key, and lets
REM  the task report Ready when it finishes.
timeout /t 600
