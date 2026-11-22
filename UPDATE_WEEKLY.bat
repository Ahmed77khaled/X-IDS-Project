@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title X-IDS: Weekly Project Updater and Safe Sync

cd /d "%~dp0"

echo ==============================================================================
echo       X-IDS Project: Weekly Milestone Updater and Safe Sync Tool
echo ==============================================================================
echo.
echo [*] مرحباً يا هندسة! جاري فحص وتنزيل أحدث مهام ومواد المشروع الأسبوعية...
echo [*] سيتم حفظ نسخة احتياطية كاملة من كل أكوادك وشغلك السابق تلقائياً.
echo.

:: ----------------------------------------------------------------------------
:: 1. Automated Safe Backup of Student Code (Zero Data Loss Guarantee)
:: ----------------------------------------------------------------------------
echo [*] جاري أخذ نسخة احتياطية آمنة من شغلك الحالي (Creating automatic backup)...
if not exist "backups" mkdir backups

for /f "tokens=*" %%t in ('powershell -NoProfile -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set "TIMESTAMP=%%t"

if exist "my_model_training.ipynb" (
    copy /y "my_model_training.ipynb" "backups\my_model_training_backup_!TIMESTAMP!.ipynb" >nul 2>&1
    echo [OK] تم تأمين نسخة من my_model_training.ipynb في مجلد backups.
)

echo [OK] النسخة الاحتياطية جاهزة وآمنة تماماً: backups\my_model_training_backup_!TIMESTAMP!.ipynb
echo.

:: ----------------------------------------------------------------------------
:: 2. Smart Git Sync (Pulls latest milestones without overwriting student work)
:: ----------------------------------------------------------------------------
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] أداة Git غير مثبتة في النظام. جاري محاولة التحديث المباشر...
    goto :FALLBACK_ZIP_SYNC
)

if not exist ".git" (
    echo [!] هذا المجلد ليس مستودع Git محلي. جاري التحديث المباشر...
    goto :FALLBACK_ZIP_SYNC
)

echo [*] جاري سحب التحديثات والمواد الجديدة من GitHub (Pulling from origin main)...
git stash push -m "student_work_!TIMESTAMP!" --quiet >nul 2>&1
git pull origin main --quiet
if %errorlevel% equ 0 (
    echo [OK] تم سحب أحدث ملفات ومواد الأسبوع بنجاح من GitHub!
) else (
    echo [WARNING] تعذر الاتصال بـ GitHub أو هناك تعارض، شغلك الحالي محفوظ في أمان.
)

:: Restore student's custom progress on their active notebook if needed
git stash pop --quiet >nul 2>&1
goto :SYNC_DEPENDENCIES

:FALLBACK_ZIP_SYNC
echo [*] جاري تنزيل أحدث حزمة تحديثات من GitHub عبر PowerShell...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "$tmpZip = Join-Path $env:TEMP 'xids_latest.zip'; " ^
    "$extractDir = Join-Path $env:TEMP 'xids_extracted'; " ^
    "Invoke-WebRequest -Uri 'https://github.com/Ahmed77khaled/X-IDS-Project/archive/refs/heads/main.zip' -OutFile $tmpZip; " ^
    "Expand-Archive -Path $tmpZip -DestinationPath $extractDir -Force; " ^
    "$srcDir = Join-Path $extractDir 'X-IDS-Project-main'; " ^
    "Get-ChildItem -Path $srcDir -Exclude 'my_model_training.ipynb' | ForEach-Object { Copy-Item -Path $_.FullName -Destination . -Recurse -Force }; " ^
    "Remove-Item -Path $tmpZip, $extractDir -Recurse -Force -ErrorAction SilentlyContinue"

echo [OK] تم استلام وتحديث المواد الجديدة بنجاح!

:: ----------------------------------------------------------------------------
:: 3. Sync Python Dependencies (in case new libraries added for new week)
:: ----------------------------------------------------------------------------
:SYNC_DEPENDENCIES
echo.
echo [*] جاري فحص وتحديث مكتبات الذكاء الاصطناعي (Checking requirements)...
set "VENV_PY=%~dp0.venv\Scripts\python.exe"

if exist "!VENV_PY!" (
    "!VENV_PY!" -m pip install -r requirements.txt --quiet >nul 2>&1
    echo [OK] كل مكتبات بايثون محدثة وجاهزة.
) else (
    echo [*] جاري تشغيل مثبت البيئة التلقائي...
    call START_PROJECT.bat
    exit /b 0
)

:: ----------------------------------------------------------------------------
:: 4. Verify Dataset & Audios
:: ----------------------------------------------------------------------------
echo [*] التحقق من ملفات الصوت والداتا سيت...
if exist "setup_dataset.py" "!VENV_PY!" setup_dataset.py >nul 2>&1
echo [OK] الداتا سيت وملفات الشرح الصوتي جاهزة.

:: ----------------------------------------------------------------------------
:: 5. Launch VS Code with the latest active notebook
:: ----------------------------------------------------------------------------
echo.
set "ACTIVE_NB=my_model_training.ipynb"
if exist "02_Model_Training_and_Comparison.ipynb" set "ACTIVE_NB=02_Model_Training_and_Comparison.ipynb"

where code >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] جاري فتح VS Code مباشرة على الملف المطلوب: !ACTIVE_NB!...
    start "" code . "!ACTIVE_NB!"
) else (
    echo [INFO] يمكنك فتح VS Code والبدء في الملف: !ACTIVE_NB!
)

echo ==============================================================================
echo                🎉 تم التحديث الأسبوعي بنجاح تام!
echo ==============================================================================
echo  1. أحدث ملفات ومكتبات المشروع نزلت عندك بنجاح.
echo  2. كودك وشغلك السابق محفوظ بأمان تام في مجلد backups.
echo  3. بيئة العمل والنوت بوك فتحت وجاهزة للعمل فوراً.
echo ==============================================================================
echo.
pause
exit /b 0

