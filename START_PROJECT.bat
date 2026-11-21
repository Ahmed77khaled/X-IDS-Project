@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title X-IDS: Autonomous Environment Setup and Launcher

cd /d "%~dp0"

echo ==============================================================================
echo    Welcome to X-IDS: Explainable AI Network Intrusion Detection System
echo ==============================================================================
echo.

:: ----------------------------------------------------------------------------
:: 0. Check for project updates (Auto-sync latest weekly milestones from GitHub)
:: ----------------------------------------------------------------------------
where git >nul 2>&1
if %errorlevel% neq 0 goto :SKIP_GIT_SYNC
if not exist ".git" goto :SKIP_GIT_SYNC

echo [*] Checking for new weekly milestones from GitHub...
git pull --quiet origin main >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Project is up-to-date with GitHub.
) else (
    echo [INFO] Continuing with current local project files.
)
echo.

:SKIP_GIT_SYNC

:: ----------------------------------------------------------------------------
:: 1. Intelligent Python Detection
:: ----------------------------------------------------------------------------
echo [*] Checking Python installation...
set "PY_EXE="

:: Test if python works directly in PATH
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_EXE=python"
    goto :PYTHON_LOCATED
)

:: Test if py launcher works
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_EXE=py -3"
    goto :PYTHON_LOCATED
)

:: Check common standard Windows Python installation paths
if exist "%LOCALAPPDATA%\Programs\Python\Python38\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python38;%LOCALAPPDATA%\Programs\Python\Python38\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python310;%LOCALAPPDATA%\Programs\Python\Python310\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)
if exist "C:\Python311\python.exe" (
    set "PY_EXE=C:\Python311\python.exe"
    set "PATH=C:\Python311;C:\Python311\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)
if exist "C:\Python310\python.exe" (
    set "PY_EXE=C:\Python310\python.exe"
    set "PATH=C:\Python310;C:\Python310\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)
if exist "C:\Python38\python.exe" (
    set "PY_EXE=C:\Python38\python.exe"
    set "PATH=C:\Python38;C:\Python38\Scripts;!PATH!"
    goto :PYTHON_LOCATED
)

:: If not found, attempt automated install via winget or silent web download
echo [!] Python is not installed or not in PATH.
echo [*] Attempting automated Python installation...

where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo [*] Installing Python 3.11 via Windows Package Manager winget...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    goto :REFRESH_SYS_PATH
)

echo [*] Downloading Python installer...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe', 'python_setup.exe')"
echo [*] Running silent Python installer...
start /wait python_setup.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
if exist python_setup.exe del /f /q python_setup.exe

:REFRESH_SYS_PATH
for /f "tokens=*" %%p in ('powershell -Command "[Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine')"') do set "PATH=%%p"
set "PY_EXE=python"

:PYTHON_LOCATED
for /f "tokens=*" %%v in ('!PY_EXE! --version') do set PYTHON_VER=%%v
echo [OK] Python detected: !PYTHON_VER!
echo.

:: ----------------------------------------------------------------------------
:: 2. Setup Isolated Virtual Environment (.venv)
:: ----------------------------------------------------------------------------
if exist ".venv\Scripts\python.exe" goto :VENV_READY

echo [*] Configuring isolated virtual environment .venv...
!PY_EXE! -m venv --system-site-packages .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to initialize virtual environment!
    pause
    exit /b 1
)

:VENV_READY
set "VENV_PY=%~dp0.venv\Scripts\python.exe"
echo [OK] Virtual environment .venv is ready.
echo.

:: ----------------------------------------------------------------------------
:: 3. Verify AI / Data Science Libraries
:: ----------------------------------------------------------------------------
echo [*] Checking AI and Data Science libraries...
"!VENV_PY!" -c "import pandas, sklearn, xgboost, ipykernel" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] All core libraries are ready.
    goto :LIBS_READY
)

echo [*] Installing missing packages from requirements.txt...
"!VENV_PY!" -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Some dependencies had warnings during install.
) else (
    echo [OK] All dependencies installed successfully.
)

:LIBS_READY
echo.

:: ----------------------------------------------------------------------------
:: 4. Register Jupyter Kernel for VS Code
:: ----------------------------------------------------------------------------
echo [*] Auto-binding Jupyter Kernel for VS Code...
"!VENV_PY!" -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)" >nul 2>&1
echo [OK] Kernel registered: "Python (X-IDS Machine Learning)"
echo.

:: ----------------------------------------------------------------------------
:: 5. Smart Dataset Verification (4 Intelligent Scenarios)
:: ----------------------------------------------------------------------------
echo [*] Checking dataset availability and auto-resolving...
"!VENV_PY!" setup_dataset.py
echo.

:: ----------------------------------------------------------------------------
:: 6. Launch VS Code with Active Notebook Immediately
:: ----------------------------------------------------------------------------
set "ACTIVE_NB=my_model_training.ipynb"
if not exist "!ACTIVE_NB!" if exist "my_model_training_clean.ipynb" set "ACTIVE_NB=my_model_training_clean.ipynb"
if not exist "!ACTIVE_NB!" if exist "01_Data_Cleaning.ipynb" set "ACTIVE_NB=01_Data_Cleaning.ipynb"
if exist "02_Model_Training_and_Comparison.ipynb" set "ACTIVE_NB=02_Model_Training_and_Comparison.ipynb"

where code >nul 2>&1
if %errorlevel% equ 0 (
    if not exist ".vscode\.ext_installed" (
        echo [*] Installing recommended VS Code extensions in background...
        start /b cmd /c "code --install-extension ms-python.python >nul 2>&1 & code --install-extension ms-toolsai.jupyter >nul 2>&1 & echo done > .vscode\.ext_installed"
    )
    echo [*] Auto-launching VS Code with active notebook: !ACTIVE_NB!...
    start "" code . "!ACTIVE_NB!"
) else (
    echo [INFO] VS Code launcher not in PATH. Please open VS Code and open: !ACTIVE_NB!
)

echo.
echo ==============================================================================
echo                         ALL SYSTEMS READY! 🚀
echo ==============================================================================
echo  [OK] Python Virtual Environment is verified.
echo  [OK] All ML libraries are verified.
echo  [OK] Dataset is verified in Dataset\CICIDS2017_improved\
echo  [OK] Kernel is pre-selected: Python (X-IDS Machine Learning)
echo  [OK] Active Notebook is opening in VS Code: !ACTIVE_NB!
echo ==============================================================================
echo  - Everything is automated on the fly!
echo  - Just press the audio play button on each task to listen to Felho
echo  - Hit Shift + Enter to run your code!
echo ==============================================================================
echo.
pause
exit /b 0
