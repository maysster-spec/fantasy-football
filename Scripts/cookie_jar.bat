@echo off
REM  cookie_jar.bat -- double-click this if ESPN starts throwing 401/403.
REM  It tests, tries to read Chrome automatically, and only asks you to copy
REM  anything if the automatic read fails. All logic is in cookie_jar.py.
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
py cookie_jar.py
echo.
pause
