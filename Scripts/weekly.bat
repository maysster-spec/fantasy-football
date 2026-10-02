@echo off
REM ==========================================================================
REM  weekly.bat -- RETIRED 18 September 2026. It calls ff.bat and does nothing else.
REM
REM  It ran ONE step, `py wire.py --html`, which is step 2 of ff.bat. Its own header claimed
REM  Task Scheduler ran it as "FF2026 - Tuesday wire" -- and setup_tasks.bat DELETES that name
REM  and registers four tasks that all call ff.bat. So the header was false and the file was a
REM  second NAME for one JOB, which is doc 146's after_pull.bat defect exactly.
REM
REM  Same treatment after_pull.bat got: a stub, so an old shortcut or a typed habit still works
REM  and gets the full run instead of a third of it. Safe to delete. Doc 353.
REM ==========================================================================
call "%~dp0ff.bat" %*
