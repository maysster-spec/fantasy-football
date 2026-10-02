@echo off
REM  done.bat -- tick an item off the to-do list and rebuild the page.
REM
REM      done ff.bat                  tick the one open item matching that text
REM      done "PASTE THE DIRECTIVE"    quotes when the text has spaces
REM      done --list                   every open item, numbered
REM      done --check ff.bat           say what it would tick, change nothing
REM      done --undo ff.bat            put a ticked item back to open
REM
REM  It REFUSES on zero matches or two, and prints the candidates. Doc 355.
cd /d "%~dp0"
py done.py %*
