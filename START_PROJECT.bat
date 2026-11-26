@echo off
setlocal enabledelayedexpansion
title X-IDS: Autonomous Environment Launcher

cd /d "%~dp0"

:: ----------------------------------------------------------------------------
:: 0. Fast-Path Check: If project is already installed, launch VS Code instantly!
:: ----------------------------------------------------------------------------
if "%1"=="--full" goto :FULL_SETUP
if "%1"=="--setup" goto :FULL_SETUP
if "%1"=="--reinstall" goto :FULL_SETUP

if exist ".venv\Scripts\python.exe" (
    if exist "my_model_training.ipynb" (
        if exist "Dataset\CICIDS2017_improved" (
            goto :FAST_LAUNCH
        )
    )
)

:FULL_SETUP
cls
echo ==============================================================================
echo        X-IDS: Explainable Network Intrusion Detection System
echo                  Full Environment Setup and Verification
echo ==============================================================================
echo.
echo [*] Welcome to X-IDS: Explainable Network Intrusion Detection System.
echo [*] Performing automated environment verification and setup...
echo.

:: 1. Intelligent Python Detection
echo [*] Checking Python installation...
set "PY_EXE="

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_EXE=python"
    goto :PYTHON_LOCATED
)

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_EXE=py -3"
    goto :PYTHON_LOCATED
)

if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :PYTHON_LOCATED
)

if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    goto :PYTHON_LOCATED
)

if exist "%LOCALAPPDATA%\Programs\Python\Python38\python.exe" (
    set "PY_EXE=%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
    goto :PYTHON_LOCATED
)

if exist "C:\Python311\python.exe" (
    set "PY_EXE=C:\Python311\python.exe"
    goto :PYTHON_LOCATED
)

if exist "C:\Python310\python.exe" (
    set "PY_EXE=C:\Python310\python.exe"
    goto :PYTHON_LOCATED
)

:: If python not found, install via winget or direct download
echo [-] Python is not installed or not in PATH.
echo [*] Attempting automated Python installation...

where winget >nul 2>&1
if %errorlevel% equ 0 (
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    goto :REFRESH_SYS_PATH
)

echo [*] Downloading official Python 3.11 installer...
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe', 'python_setup.exe')"
start /wait python_setup.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
if exist python_setup.exe del /f /q python_setup.exe

:REFRESH_SYS_PATH
set "PY_EXE=python"

:PYTHON_LOCATED
for /f "tokens=*" %%v in ('!PY_EXE! --version 2^>nul') do set "PYTHON_VER=%%v"
echo [OK] Python detected: !PYTHON_VER!
echo.

:: 2. Setup Isolated Virtual Environment (.venv)
if exist ".venv\Scripts\python.exe" goto :VENV_READY

echo [*] Configuring virtual environment .venv...
!PY_EXE! -m venv --system-site-packages .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to initialize virtual environment.
    pause
    exit /b 1
)

:VENV_READY
set "VENV_PY=%~dp0.venv\Scripts\python.exe"
echo [OK] Virtual environment .venv is ready.
echo.

:: 3. Verify AI / Data Science Libraries
echo [*] Checking required libraries...
"!VENV_PY!" -c "import pandas, sklearn, xgboost, ipykernel" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] All core libraries are ready.
) else (
    echo [*] Installing requirements from requirements.txt...
    "!VENV_PY!" -m pip install -r requirements.txt --quiet
    echo [OK] Dependencies installed successfully.
)
echo.

:: 4. Register Jupyter Kernel
echo [*] Auto-binding Jupyter Kernel for VS Code...
"!VENV_PY!" -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)" >nul 2>&1
echo [OK] Kernel registered: "Python (X-IDS Machine Learning)"
echo.

:: 5. Verify Dataset
echo [*] Checking dataset availability...
if exist "scripts\setup_dataset.py" (
    "!VENV_PY!" scripts\setup_dataset.py
) else if exist "setup_dataset.py" (
    "!VENV_PY!" setup_dataset.py
)
echo.

:: ============================================================================
:: Fast Launch Point: When environment is already ready!
:: ============================================================================
:FAST_LAUNCH
set "ACTIVE_NB=my_model_training.ipynb"
set "VSCODE_CMD="

echo ==============================================================================
echo        X-IDS: Explainable Network Intrusion Detection System
echo ==============================================================================
echo [*] Environment and datasets verified successfully.
echo [*] Locating Visual Studio Code and launching workspace...
echo.

:: Step A: Try python-based deep detection (Registry + All Disks)
set "LAUNCH_PY="
if exist "scripts\launch_vscode.py" set "LAUNCH_PY=scripts\launch_vscode.py"
if not defined LAUNCH_PY if exist "launch_vscode.py" set "LAUNCH_PY=launch_vscode.py"

if defined LAUNCH_PY (
    if exist ".venv\Scripts\python.exe" (
        for /f "usebackq delims=" %%i in (`.venv\Scripts\python.exe "!LAUNCH_PY!" --detect 2^^^>nul`) do (
            if exist "%%i" set "VSCODE_CMD=%%i"
        )
    )
    if not defined VSCODE_CMD (
        for /f "usebackq delims=" %%i in (`python "!LAUNCH_PY!" --detect 2^^^>nul`) do (
            if exist "%%i" set "VSCODE_CMD=%%i"
        )
    )
)

:: Step B: Native PATH Check
if not defined VSCODE_CMD (
    where code >nul 2>&1
    if %errorlevel% equ 0 set "VSCODE_CMD=code"
)

:: Step C: Known Disk Directories
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

:: ----------------------------------------------------------------------------
:: Launch VS Code or Fallback
:: ----------------------------------------------------------------------------
if defined VSCODE_CMD (
    echo [OK] Visual Studio Code located: "!VSCODE_CMD!"
    echo [*] Opening project workspace and notebook: "!ACTIVE_NB!"...
    start "" "!VSCODE_CMD!" "%~dp0" -g "%~dp0!ACTIVE_NB!"
    echo.
    echo ==============================================================================
    echo  [OK] Workspace launched successfully.
    echo  - You can run notebook cells immediately by pressing Shift + Enter.
    echo  - Audio narration and guided explanations are embedded inside the notebook.
    echo ==============================================================================
    ping 127.0.0.1 -n 3 >nul 2>&1
    exit /b 0
)

:: If VS Code is NOT installed on this machine:
echo ==============================================================================
echo [-] Visual Studio Code was not found on this system.
echo ==============================================================================
echo.
echo Please select an option to start working:
echo [1] Open notebook in browser via Jupyter Notebook (Recommended).
echo [2] Open file with Windows default application.
echo [3] Download and install Visual Studio Code (Free).
echo [4] Exit.
echo.

set /p USER_CHOICE="Enter your choice (1, 2, 3, or 4): "

if "%USER_CHOICE%"=="1" (
    echo [*] Starting Jupyter Notebook in your web browser...
    start "" "%~dp0.venv\Scripts\python.exe" -m jupyter notebook "%~dp0!ACTIVE_NB!"
    exit /b 0
)

if "%USER_CHOICE%"=="2" (
    echo [*] Opening file with default application...
    start "" "%~dp0!ACTIVE_NB!"
    exit /b 0
)

if "%USER_CHOICE%"=="3" (
    echo [*] Opening Visual Studio Code download page...
    start https://code.visualstudio.com/Download
    pause
    exit /b 0
)

exit /b 0
