@echo off
:: سكربت لمراقبة plan-data.json ورفع أي تعديل تلقائيًا للريبو في GitHub
:loop
timeout /t 5 >nul
for %%F in (plan-data.json) do (
    set "new=%%~tF"
)
if not defined old (
    set "old=%new%"
    goto :loop
)
if not "%new%"=="%old%" (
    echo تم تعديل الملف، يتم رفع التحديث...
    git add plan-data.json
    git commit -m "تحديث بيانات الخطة تلقائي"
    git push
    set "old=%new%"
) else (
    rem لم يحدث تعديل
)
goto loop
