@echo off
REM ==========================================================================
REM  gameday.bat -- RETIRED 18 September 2026. It calls ff.bat and does nothing else.
REM
REM  It ran ONE step, `py lineup.py --html`, which is step 1 of ff.bat. Its header named a
REM  scheduled task, "FF2026 - Lineup check", that setup_tasks.bat deletes. Running it instead
REM  of ff.bat got you the lineup check and NOT the wire, the week sheet, the to-do page or the
REM  kit check -- so the shortcut that looked quicker was the one that left three pages stale.
REM
REM  A stub, so the old habit still gets the full run. Safe to delete. Doc 353.
REM ==========================================================================
call "%~dp0ff.bat" %*
