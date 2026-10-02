@echo off
REM  weekend_check.bat -- double-click. Runs every pre-draft test in order.
REM  Does NOT write to ESPN. For the version that also re-injects the prerank,
REM  run:  py weekend_check.py --inject
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
REM
REM  doc 164: the output is ALSO written to weekend_check_log.txt, and overwritten
REM  each run. Claude has no shell on this machine and cannot see a console window,
REM  so every check run today had to be copied and pasted by hand. Deliberately NOT
REM  done to draft_night.bat -- that one asks questions you must read and answer live.
py -u weekend_check.py > weekend_check_log.txt 2>&1
type weekend_check_log.txt
echo.
echo   (saved to Scripts\weekend_check_log.txt)
pause
