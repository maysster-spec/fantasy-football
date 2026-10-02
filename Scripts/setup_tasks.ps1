# SUPERSEDED 2026-09-08. The PowerShell route built one task with three triggers
# and the Thursday trigger did not appear on Matt's machine twice running. There is
# no PowerShell in my container, so I could never execute this before shipping it.
# The live file is setup_tasks.bat, which registers a single task from ff_task.xml
# using schtasks.exe -- no execution policy, no module, and the XML is readable.
Write-Host ""
Write-Host "This file is superseded. Run this instead, in an ADMIN Command Prompt:" -ForegroundColor Yellow
Write-Host '    "G:\My Drive\_Fantasy\2026\Scripts\setup_tasks.bat"'
Write-Host ""
