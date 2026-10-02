@echo off
setlocal
REM ===========================================================================
REM  sept5_after.bat -- THE sequence you run after the projections are refreshed.
REM
REM  ONE FILE, TEN STEPS, IN THIS ORDER. Everything downstream reads the board, so
REM  rebuilding a printout before the board is refreshed puts yesterday's players on
REM  today's paper (doc 109). Do not run these separately unless one of them stops.
REM
REM  RUN IT WHATEVER THE VERDICT SAID. FREEZE / REBUILD is about the PROJECTIONS.
REM  This handles the MARKET, which moves far more -- 160 of the top 161 draft
REM  positions changed between the Aug-23 and Aug-30 pulls.
REM
REM  doc 146: after_pull.bat was a second copy of this file, written the same week.
REM  This is the one that survived; that one now just calls this one.
REM ===========================================================================
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
title After the refresh -- rebuild everything that reads the board
set STALE=

echo.
echo  ============================================================
echo   AFTER THE REFRESH        %DATE% %TIME%
echo  ============================================================
echo.
echo   Steps 1-3 check the numbers and STOP if anything is wrong.
echo   Steps 4-8 rebuild the pages.  Step 9 turns them into PDFs.
echo   Step 10 puts fresh copies on your desk.
echo   About three minutes. Nothing here writes to ESPN.
echo.

echo  ------------------------------------------------------------
echo   [1/13]  What has the draft market done since the last freeze?
echo  ------------------------------------------------------------
py refresh_adp.py
echo.
echo   That was a LOOK ONLY -- nothing has changed yet. Read the movers above.
set DOADP=Y
set /p DOADP=  Write the new draft positions into the board? [Y]/N:
if /i "%DOADP%"=="N" goto :skipadp
py refresh_adp.py --write
if errorlevel 1 goto :adpfail
:skipadp

echo.
echo  ------------------------------------------------------------
echo   [2/13]  Do the board's numbers still add up?
echo  ------------------------------------------------------------
py board_audit.py
if errorlevel 1 goto :auditfail

echo.
echo  ------------------------------------------------------------
echo   [3/13]  Who is behind whom -- rebuilding the depth chart
echo  ------------------------------------------------------------
py depth_map.py
if errorlevel 1 goto :mapfail

echo.
echo  ############################################################
echo   The next five steps each write a PAGE and then try to turn
echo   it into a PDF. This machine has no PDF maker installed, so
echo   you will see "wkhtmltopdf not on PATH" five times below.
echo   THAT IS EXPECTED AND IS NOT A FAILURE -- step 9 makes the
echo   PDFs with Chrome instead.
echo  ############################################################

echo.
echo  ------------------------------------------------------------
echo   [4/13]  The board you draft from
echo  ------------------------------------------------------------
py make_board.py
if errorlevel 1 set STALE=%STALE% DRAFT_BOARD

echo.
echo  ------------------------------------------------------------
echo   [5/13]  The paper backup, for if the live tool dies
echo  ------------------------------------------------------------
py make_fallback.py
if errorlevel 1 set STALE=%STALE% FALLBACK_BOARD

echo.
echo  ------------------------------------------------------------
echo   [6/13]  The few players the board cannot show correctly
echo  ------------------------------------------------------------
py mkoverride.py
if errorlevel 1 set STALE=%STALE% OVERRIDE_CARD

echo.
echo  ------------------------------------------------------------
echo   [7/13]  Re-reading the value ladder off the new board
echo  ------------------------------------------------------------
py parse_ladder.py
if errorlevel 1 goto :ladderfail

echo.
echo  ------------------------------------------------------------
echo   [8/13]  Building the value ladder page
echo  ------------------------------------------------------------
py mkvalue.py
if errorlevel 1 set STALE=%STALE% VALUE_LADDER

echo.
echo  ------------------------------------------------------------
echo   [9/13]  Rebuilding the 12-wide draft grid
echo  ------------------------------------------------------------
rem doc 188: make_gridboard.py was in NO rebuild path. It reads board_v8_fixed.csv,
rem values.csv and player_context.csv, and on Sept 5 the grid was built 40 minutes
rem before the board changed and four hours before the cards did -- while
rem sync_desk_copies happily carried the stale PDF to the desk and printed OK.
rem to_pdf --check cannot catch this: the page and its PDF go stale together.
py make_gridboard.py
if errorlevel 1 set STALE=%STALE% ADP_GRID
rem doc 203: the SAME grid filled in OUR order of value. One script, one flag.
py make_gridboard.py --board
if errorlevel 1 set STALE=%STALE% BOARD_GRID

echo.
echo  ------------------------------------------------------------
echo   [10/13]  Rebuilding the how-to page, then turning the pages into PDFs
echo  ------------------------------------------------------------
rem doc 163: make_howto regenerates HOW_TO_READ_IT.html from live_draft.COLGLOSS.
rem It was in NO rebuild path, so the page explaining the board froze whenever the
rem board's own legend changed. It must run BEFORE to_pdf, which now prints it.
py make_howto.py
if errorlevel 1 set STALE=%STALE% HOW_TO_READ_IT
py to_pdf.py
if errorlevel 1 goto :pdffail

echo.
echo  ------------------------------------------------------------
echo   [11/13]  Building the tier sheet
echo  ------------------------------------------------------------
rem doc 192: our ranking arranged by TIER rather than by rank or by pick. It imports
rem add_tiers from make_board.py -- one derivation two consumers -- so it must run AFTER
rem the board and BEFORE sync_desk_copies. It renders its own PDF via to_pdf.render.
py make_tiers.py
if errorlevel 1 set STALE=%STALE% TIER_SHEET

echo.
echo  ------------------------------------------------------------
echo  ------------------------------------------------------------
echo   [12/13]  Does the paper still talk like the paper?
echo  ------------------------------------------------------------
rem doc 208: the sheets are read at 60 seconds a pick. Section numbers, p-values and sample
rem sizes belong in Source\*.md, not on them. --warn so a wording slip never halts a rebuild.
py check_plain.py --warn

echo.
echo  ------------------------------------------------------------
echo   [13/13]  Putting fresh copies on your desk
echo  ------------------------------------------------------------
py sync_desk_copies.py
if errorlevel 1 goto :syncfail

if not "%STALE%"=="" goto :somestale

echo.
echo  ============================================================
echo   DONE. Every printout was rebuilt from the refreshed board.
echo.
echo   REPRINT:  the draft board, the value ladder, the override
echo             card and the paper backup.
echo.
echo   Then run  py make_shortcuts.py  once, so the links in your
echo   Desktop "FF2026 Draft" folder point at today's files.
echo.
echo   The ESPN prerank does NOT need re-injecting -- it is ordered
echo   by rank, and none of this changed rank. Only the TIMING moved.
echo  ============================================================
goto :hold

:somestale
echo.
echo  ============================================================
echo   FINISHED, BUT NOT EVERYTHING REBUILT.
echo   These printouts are now OLDER than the board and must not
echo   be trusted or printed:
echo      %STALE%
echo   Scroll up to the step that failed and read its message.
echo  ============================================================
goto :hold

:adpfail
echo. & echo  *** STOPPED at step 1. The market update refused to write.
echo  *** Almost always a keeper name that does not match the pull. It refuses
echo  *** rather than shifting everyone behind him by a pick. Fix actual_keepers.csv.
goto :hold
:auditfail
echo. & echo  *** STOPPED at step 2. The board's numbers do not add up.
echo  *** Read the FAILED list above. If it names a news override, run
echo  *** py apply_news.py --write  and then this file again.
echo  *** Do NOT print anything until this passes.
goto :hold
:mapfail
echo. & echo  *** STOPPED at step 3. The depth chart could not be matched to the board.
echo  *** Usually the name match dropped below 85%%. Every printout would be wrong.
goto :hold
:ladderfail
echo. & echo  *** STOPPED at step 7. The value ladder could not be rebuilt from the board.
echo  *** The old VALUE_LADDER is still there and is now out of date.
goto :hold
:pdffail
echo. & echo  *** Step 9 could not make every PDF. It named the pages it could not do.
echo  *** Open each one and press Ctrl+P, Save as PDF, over the file of the same name.
echo  *** Then run  py sync_desk_copies.py  yourself.
goto :hold
:syncfail
echo. & echo  *** Step 10 could not copy something to your desk.
echo  *** Usually the file is open in a PDF viewer. Close it and run
echo  *** py sync_desk_copies.py  again.
goto :hold

:hold
echo.
timeout /t 600
