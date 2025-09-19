@echo off

REM Batch script for auto-pushing plan-data.json

setlocal

set REPO=aliabdelaal-adm/inspection_plan
set FILE=plan-data.json
set GIT_DIR=%CD%\%REPO%

REM Change to the repository directory
cd %GIT_DIR%

REM Add, commit, and push the changes
git add %FILE%
git commit -m "Auto-push plan-data.json"
git push origin main

endlocal