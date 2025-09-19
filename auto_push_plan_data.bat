@echo off
REM Smart auto-push script for plan-data.json
REM Monitors for changes and pushes only when actual updates occur

set FILE=plan-data.json
set SLEEP=30

REM Store the initial hash
for /f %%i in ('certutil -hashfile "%FILE%" MD5 ^| find /i /v "md5"') do set OLDHASH=%%i

:loop
REM Wait for some time before checking again
timeout /t %SLEEP% /nobreak >nul

REM Calculate current hash
for /f %%i in ('certutil -hashfile "%FILE%" MD5 ^| find /i /v "md5"') do set NEWHASH=%%i

REM If hash changed, push to GitHub
if not "%OLDHASH%"=="%NEWHASH%" (
    echo Detected change in %FILE%. Pushing to GitHub...
    git add "%FILE%"
    git commit -m "Auto-update plan-data.json"
    git push
    set OLDHASH=%NEWHASH%
) else (
    echo No change in %FILE%. Monitoring...
)

goto loop
