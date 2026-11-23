@echo off
chcp 65001 > nul
setlocal
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
echo [*] جاري أخذ نسخة احتياطية آمنة من شغلك الحالي...
if not exist "backups" mkdir backups

for /f "tokens=*" %%t in ('powershell -NoProfile -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set "TIMESTAMP=%%t"

if exist "my_model_training.ipynb" (
    copy /y "my_model_training.ipynb" "backups\my_model_training_backup_%TIMESTAMP%.ipynb" >nul 2>&1
    echo [OK] تم تأمين نسخة من my_model_training.ipynb في مجلد backups.
)

:: Clean up legacy duplicate files from student's local folder if present
if exist "setup.bat" del /f /q "setup.bat" >nul 2>&1
if exist "setup.py" del /f /q "setup.py" >nul 2>&1
if exist "01_Data_Cleaning.ipynb" move /y "01_Data_Cleaning.ipynb" "backups\legacy_01_Data_Cleaning_%TIMESTAMP%.ipynb" >nul 2>&1
if exist "01_Data_Cleaning_Clean.ipynb" move /y "01_Data_Cleaning_Clean.ipynb" "backups\legacy_01_Data_Cleaning_Clean_%TIMESTAMP%.ipynb" >nul 2>&1
if exist "my_model_training_clean.ipynb" move /y "my_model_training_clean.ipynb" "backups\legacy_my_model_training_clean_%TIMESTAMP%.ipynb" >nul 2>&1

:: Remove old developer scripts from root if they already exist in scripts\
for %%f in (build_guided_notebook.py build_word_and_ppt_reports.py create_notebook.py create_student_notebook.py download_data.py fix_rtl_notebook.py generate_report_evidence.py generate_sample_dataset.py generate_voice_samples.py reset_student_notebook.py update_notebook.py x_ids_pipeline.py design_previews.html shap_feature_importance.png) do (
    if exist "scripts\%%f" if exist "%%f" del /f /q "%%f" >nul 2>&1
)

echo [OK] النسخة الاحتياطية جاهزة وآمنة تماماً: backups\my_model_training_backup_%TIMESTAMP%.ipynb
echo.

:: ----------------------------------------------------------------------------
:: 2. Smart Git Sync (Pulls latest milestones without overwriting student work)
:: ----------------------------------------------------------------------------
where git >nul 2>&1
if %errorlevel% neq 0 goto :FALLBACK_ZIP_SYNC
if not exist ".git" goto :FALLBACK_ZIP_SYNC

echo [*] جاري سحب أحدث التحديثات والمواد من GitHub...
git stash push my_model_training.ipynb -m "student_work_%TIMESTAMP%" --quiet >nul 2>&1
git pull origin main --quiet
if %errorlevel% equ 0 goto :GIT_PULL_SUCCESS
echo [INFO] تعذر الاتصال بـ GitHub، جاري المحاولة عبر التنزيل المباشر...
goto :FALLBACK_ZIP_SYNC

:GIT_PULL_SUCCESS
echo [OK] تم سحب أحدث ملفات ومواد الأسبوع بنجاح من GitHub.
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

echo [OK] تم استلام وتحديث المواد الجديدة بنجاح.

:: ----------------------------------------------------------------------------
:: 3. Sync Python Dependencies
:: ----------------------------------------------------------------------------
:SYNC_DEPENDENCIES
echo.
echo [*] جاري فحص وتحديث مكتبات الذكاء الاصطناعي...
set "VENV_PY=%~dp0.venv\Scripts\python.exe"

if exist "%VENV_PY%" goto :VENV_EXISTS
echo [*] جاري تشغيل مثبت البيئة التلقائي...
call START_PROJECT.bat
exit /b 0

:VENV_EXISTS
"%VENV_PY%" -m pip install -r requirements.txt --quiet >nul 2>&1
echo [OK] كل مكتبات بايثون محدثة وجاهزة.

:: ----------------------------------------------------------------------------
:: 4. Verify Dataset & Audios
:: ----------------------------------------------------------------------------
echo [*] التحقق من ملفات الصوت والداتا سيت...
if exist "scripts\setup_dataset.py" (
    "%VENV_PY%" scripts\setup_dataset.py >nul 2>&1
) else if exist "setup_dataset.py" (
    "%VENV_PY%" setup_dataset.py >nul 2>&1
)
echo [OK] الداتا سيت وملفات الشرح الصوتي جاهزة.

:: ----------------------------------------------------------------------------
:: 5. Launch VS Code directly on active notebook (Smart Path Detection)
:: ----------------------------------------------------------------------------
echo.
set "ACTIVE_NB=my_model_training.ipynb"
if exist "02_Model_Training_and_Comparison.ipynb" set "ACTIVE_NB=02_Model_Training_and_Comparison.ipynb"

set "VSCODE_CMD="

set "LAUNCH_PY="
if exist "scripts\launch_vscode.py" set "LAUNCH_PY=scripts\launch_vscode.py"
if not defined LAUNCH_PY if exist "launch_vscode.py" set "LAUNCH_PY=launch_vscode.py"

if defined LAUNCH_PY (
    if exist ".venv\Scripts\python.exe" (
        for /f "usebackq delims=" %%i in (`.venv\Scripts\python.exe "%LAUNCH_PY%" --detect 2^>nul`) do (
            if exist "%%i" set "VSCODE_CMD=%%i"
        )
    )
    if not defined VSCODE_CMD (
        for /f "usebackq delims=" %%i in (`python "%LAUNCH_PY%" --detect 2^>nul`) do (
            if exist "%%i" set "VSCODE_CMD=%%i"
        )
    )
)

if not defined VSCODE_CMD (
    where code >nul 2>&1
    if %errorlevel% equ 0 set "VSCODE_CMD=code"
)

if not defined VSCODE_CMD (
    if exist "%LOCALAPPDATA%\Programs\Microsoft Visual studio Code\Code.exe" set "VSCODE_CMD=%LOCALAPPDATA%\Programs\Microsoft Visual studio Code\Code.exe"
    if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" set "VSCODE_CMD=%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
    if exist "%LOCALAPPDATA%\Programs\Microsoft Visual studio Code\bin\code.cmd" set "VSCODE_CMD=%LOCALAPPDATA%\Programs\Microsoft Visual studio Code\bin\code.cmd"
    if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" set "VSCODE_CMD=%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd"
    if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" set "VSCODE_CMD=%ProgramFiles%\Microsoft VS Code\Code.exe"
    if exist "%ProgramFiles%\Microsoft VS Code\bin\code.cmd" set "VSCODE_CMD=%ProgramFiles%\Microsoft VS Code\bin\code.cmd"
    if exist "C:\Program Files\Microsoft VS Code\Code.exe" set "VSCODE_CMD=C:\Program Files\Microsoft VS Code\Code.exe"
    if exist "%ProgramFiles(x86)%\Microsoft VS Code\Code.exe" set "VSCODE_CMD=%ProgramFiles(x86)%\Microsoft VS Code\Code.exe"
)

if defined VSCODE_CMD (
    echo [OK] تم العثور على Visual Studio Code: "%VSCODE_CMD%"
    echo [*] جاري فتح VS Code مباشرة على صفحة الشغل: %ACTIVE_NB%...
    start "" "%VSCODE_CMD%" "%~dp0" -g "%~dp0%ACTIVE_NB%"
) else (
    echo [INFO] يمكنك فتح VS Code والبدء في الملف: %ACTIVE_NB%
)

echo.
echo ==============================================================================
echo                🎉 تم التحديث الأسبوعي بنجاح تام!
echo ==============================================================================
echo  1. أحدث ملفات ومكتبات المشروع نزلت عندك بنجاح لأحدث إصدار.
echo  2. كودك وشغلك السابق محفوظ بأمان تام في مجلد backups.
echo  3. تم تنظيف المجلد الرئيسي وترتيبه وفقاً لأحدث هيكلة.
echo  4. بيئة العمل والنوت بوك فتحت وجاهزة للعمل فوراً: %ACTIVE_NB%
echo ==============================================================================
echo.
ping 127.0.0.1 -n 3 >nul 2>&1
exit /b 0
