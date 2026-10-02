@echo off
cd /d "%~dp0"
echo.
echo   DRESS REHEARSAL -- no ESPN, nothing written. Ctrl+C ends it.
echo.
py rehearsal.py %*
echo.
pause
