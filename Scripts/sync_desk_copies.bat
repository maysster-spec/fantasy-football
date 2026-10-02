@echo off
REM ---------------------------------------------------------------------------
REM  sync_desk_copies.bat -- thin wrapper. All logic is in sync_desk_copies.py.
REM  doc 84: the previous batch version used a parenthesised if/else with an
REM  escaped `^>` inside it. cmd read the `>` as a redirect and created two
REM  11-byte junk files named like the PDFs. Batch conditionals cannot be tested
REM  from where they are written, so there are none left here.
REM  Run it any time a guide or card is rebuilt.
REM ---------------------------------------------------------------------------
cd /d "G:\My Drive\_Fantasy\2026\Scripts"
py sync_desk_copies.py
echo.
REM  The copy itself is already finished by this line -- this hold is ONLY so the
REM  window stays readable. It is `timeout` and not `pause` because a pause leaves an
REM  unattended window open forever (see refresh_pull.bat). ANY KEY CLOSES IT NOW.
echo   Done. Press any key to close, or this window closes on its own in 20 seconds.
timeout /t 20 >nul
