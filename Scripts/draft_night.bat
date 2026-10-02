@echo off
setlocal
REM ===========================================================================
REM  draft_night.bat  --  the whole 7:00 PM sequence, in order, with gates.
REM  doc 146: step 5 was still starting the OLD live board, the one that reads picks
REM  from ESPN's API. Doc 136 proved that API publishes a draft only after it ends,
REM  so on the night that path shows nothing. Step 5 now starts the browser bridge.
REM  Schedule ONE task for this at 6:55 PM on Mon Sep 7 2026.
REM  Do NOT schedule the steps separately: order matters and a silent
REM  out-of-order run is the failure mode this project keeps finding.
REM
REM  doc 81 changes:
REM    - step 3 now DEFAULTS TO REBUILD on a bare Enter. Rebuilding when the
REM      keepers are identical is a harmless no-op; skipping when they are not
REM      leaves a wrongly-removed player invisible to the engine all night.
REM      The costly direction must never be the one a fumbled keypress picks.
REM    - the errorlevel checks are out of the parenthesised blocks (nested
REM      parens with & inside an IF block are fragile in cmd).
REM ===========================================================================
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
title DRAFT NIGHT -- Sept 7
echo.
echo  ============================================================
echo   DRAFT NIGHT SEQUENCE      %DATE% %TIME%
echo   Draft starts 8:00 PM. Keeper lock 7:00 PM.
echo  ============================================================
echo.

echo  [1/5] Verifying the file tree...
py check_kit.py
if errorlevel 1 goto :kitfail
echo.

echo  [2/5] Fetching ACTUAL keepers from ESPN...
echo        (If the lock has not happened yet, this will refuse -- that is correct.)
py fetch_keepers.py --dry
echo.
echo  Review the 12 names above against ESPN's league page.
pause

py fetch_keepers.py --write
if errorlevel 1 goto :handedit
goto :step3

:handedit
echo.
echo  Automatic fetch did not write. Edit actual_keepers.csv by hand NOW --
echo  one row per team, 12 rows, a Player column. Save and close Notepad.
notepad actual_keepers.csv

:step3
echo.
echo  [3/5] Checking whether the board needs rebuilding...
py keeper_swap.py --check
echo.
echo  If it said IDENTICAL you can answer N -- but Y is safe either way
echo  (rebuilding an identical board just rewrites the same rows).
set DOSWAP=Y
set /p DOSWAP=  Rebuild the board? [Y]/N:
if /i "%DOSWAP%"=="N" goto :step4
py keeper_swap.py --write
if errorlevel 1 goto :swapfail

REM doc 101: the swap rebuilds the board FROM THE SPINE, which reverts every news override.
REM Reproduced 2026-08-31: a --write restored a suspended Josh Jacobs to rank 20, an hour
REM before the draft, while printing "IDENTICAL to the current board." keeper_swap now
REM re-applies news_overrides.csv itself -- and this is the gate that PROVES it did.
echo.
echo  [3b/5] Proving the rebuilt board is still arithmetically right...
py board_audit.py
if errorlevel 1 goto :auditfail

:step4
echo.
echo  [4a/5] Rebuilding the prerank ORDER on the board we just rebuilt...
REM doc 218. Matt asked whether the prerank was overdue. It was: the file was built
REM Aug 30 and the board has been re-frozen TWICE since (Sep 3, and Sep 7 12:59).
REM Neither this file nor sept5_after.bat ever ran make_prerank, so an expired clock
REM would have autodrafted off an eight-day-old ordering. It must run AFTER the keeper
REM swap -- the swap rewrites the board -- and AFTER check_kit, which has already run.
py make_prerank.py --write
echo.
echo  [4/5] Re-injecting the prerank list into ESPN, and verifying it...
py espn_draft_injector_Gemini.py
echo.
echo  PASS looks like:  ESPN reports 544 players stored (sent 544).
echo  If you see 512, the 32 defenses were rejected -- note it and continue.
echo.
echo  Now PROVING it landed, row by row -- read-only, ten seconds...
py verify_prerank.py
echo.
echo  Want:  ORDER MATCHES exactly  and  K / D-ST inside ESPN's top 250: 0
echo  If it says DIFFERS, run the injector again then re-run verify_prerank.py.
echo  Do NOT go to the draft on a DIFFERS.
pause
echo.

echo  [5/5] Starting the live board. THIS IS NOW THREE THINGS, IN ORDER.
echo.
echo   doc 136: ESPN does not publish a draft to its read API until the draft
echo   has ENDED, so the plain live board CANNOT see picks on the night. The
echo   picks are in the browser the whole time, so we read them from there.
echo.
cd live_draft
echo   [5a] Starting the listener in its own window. LEAVE THAT WINDOW OPEN.
start "ESPN BRIDGE -- leave this window open" cmd /k py bridge_server.py
echo.
echo   [5b] NOW, IN CHROME:
echo        - open chrome://extensions, turn on Developer mode,
echo          Load unpacked, and pick the folder
echo          G:\My Drive\_Fantasy\2026\Scripts\live_draft\espn_bridge
echo          (only needed once -- if it is already loaded, skip it)
echo        - open your ESPN draft room in that same Chrome
echo        - the listener window should start printing as picks arrive
echo.
pause
echo.
echo   [5c] Starting the board.
echo        The first poll line reports how many keeper rows are showing.
echo        12 is the expected number. If it says 0, that is probably ESPN not
echo        exposing keepers until the draft starts -- keeper availability does
echo        NOT depend on it (they are already off the board file). The real
echo        tell for a broken filter is the pick number running exactly 12
echo        ahead of ESPN's once picking begins.
echo.
echo        If you ever see  bridge file went BACKWARDS,  the listener was
echo        restarted mid-draft. Close this board and start it again too.
echo.
py live_draft.py --bridge
goto :eof

:kitfail
echo.
echo  *** check_kit FAILED. Something is stale or missing. ***
echo  *** Fix it before anything else. Nothing below is trustworthy. ***
pause
exit /b 1

:auditfail
echo.
echo  *** BOARD AUDIT FAILED after the keeper swap. ***
echo  *** Read the FAILED list above. If it names a news override, run:
echo  ***     py apply_news.py --write
echo  *** then  py board_audit.py  again. Do NOT draft off this board until it passes.
pause
exit /b 1

:swapfail
echo.
echo  *** SWAP FAILED -- read the message above. ***
echo  *** Most likely a keeper name does not match the spine; the message
echo  *** names the closest spelling. Fix actual_keepers.csv and re-run
echo  *** py keeper_swap.py --check  then  --write  by hand.
pause
exit /b 1
