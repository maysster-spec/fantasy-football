@echo off
REM ===========================================================================
REM  after_pull.bat -- THIS FILE IS A DUPLICATE. YOU CAN DELETE IT.
REM
REM  It was written on Sept 3 2026 without checking whether the same sequence
REM  already existed. It did: sept5_after.bat, from Aug 30, which does the same
REM  work and does it better (it shows you the market moves and asks before it
REM  writes anything). Rather than leave two files that drift apart, this one now
REM  just runs that one.
REM
REM  Nothing points here any more. Delete it whenever you like.
REM ===========================================================================
echo.
echo   after_pull.bat was a duplicate of sept5_after.bat.
echo   Running sept5_after.bat instead. You can delete this file.
echo.
timeout /t 4 >nul
call "G:\My Drive\_Fantasy\2026\Scripts\sept5_after.bat"
