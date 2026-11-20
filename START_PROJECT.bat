@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title X-IDS: Autonomous Environment Setup & Launcher

cd /d "%~dp0"

echo ==============================================================================
echo    Welcome to X-IDS: Explainable AI Network Intrusion Detection System
echo ==============================================================================
echo.

:: ----------------------------------------------------------------------------
:: 1. Check Python installation (Auto-install if missing)
:: ----------------------------------------------------------------------------
echo [*] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed or not in PATH.
    echo [*] Attempting automated Python installation...
    
    where winget >nul 2>&1
    if %errorlevel% equ 0 (
        echo [*] Installing Python 3.11 via Windows Package Manager (winget)...
        winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    ) else (
        echo [*] Downloading Python installer...
        powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe', 'python_setup.exe')"
        echo [*] Running silent Python installer (adding to PATH)...
        start /wait python_setup.exe /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
        if exist python_setup.exe del /f /q python_setup.exe
    )
    
    :: Refresh Environment PATH
    for /f "tokens=*" %%p in ('powershell -Command "[Environment]::GetEnvironmentVariable('Path', 'User') + ';' + [Environment]::GetEnvironmentVariable('Path', 'Machine')"') do set "PATH=%%p"
    
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Automatic Python installation could not be completed.
        echo Please manually install Python 3.8+ from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
)

for /f "tokens=*" %%v in ('python --version') do set PYTHON_VER=%%v
echo [OK] Python is ready: !PYTHON_VER!
echo.

:: ----------------------------------------------------------------------------
:: 2. Setup Isolated Virtual Environment (.venv)
:: ----------------------------------------------------------------------------
if not exist ".venv" (
    echo [*] Creating isolated virtual environment (.venv)...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created successfully.
) else (
    echo [OK] Virtual environment (.venv) already exists.
)
echo.

:: ----------------------------------------------------------------------------
:: 3. Activate Virtual Environment
:: ----------------------------------------------------------------------------
echo [*] Activating virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo [ERROR] Activation script not found in .venv! Recreating...
    rmdir /s /q .venv
    python -m venv .venv
)
call .venv\Scripts\activate.bat
echo [OK] Virtual environment active.
echo.

:: ----------------------------------------------------------------------------
:: 4. Verify & Install Requirements
:: ----------------------------------------------------------------------------
echo [*] Checking AI and Data Science libraries...
python -c "import pandas, sklearn, xgboost, shap, ipykernel" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing required packages from requirements.txt (first-time only, ~1-2 min)...
    python -m pip install --upgrade pip --quiet
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [WARNING] Some dependencies had warnings during install.
    ) else (
        echo [OK] All dependencies installed successfully.
    )
) else (
    echo [OK] All libraries are already installed and up to date.
)
echo.

:: ----------------------------------------------------------------------------
:: 5. Register Jupyter / VS Code Kernel
:: ----------------------------------------------------------------------------
echo [*] Registering Jupyter Kernel for VS Code...
python -m ipykernel install --user --name xids-env --display-name "Python (X-IDS Machine Learning)" >nul 2>&1
echo [OK] Kernel registered as: "Python (X-IDS Machine Learning)"
echo.

:: ----------------------------------------------------------------------------
:: 6. Check Dataset Presence
:: ----------------------------------------------------------------------------
echo [*] Checking dataset availability...
if exist "Dataset\CICIDS2017_improved\Wednesday-workingHours.pcap_ISCX.csv" (
    echo [OK] Dataset verified: Wednesday-workingHours.pcap_ISCX.csv
) else (
    echo [NOTE] Dataset file is not present locally.
    echo        Path: Dataset\CICIDS2017_improved\Wednesday-workingHours.pcap_ISCX.csv
    echo        (The dataset is ~1.4GB and not hosted on GitHub. Ask your team for the file).
)
echo.

:: ----------------------------------------------------------------------------
:: 7. Launch VS Code directly to Notebook
:: ----------------------------------------------------------------------------
echo ==============================================================================
echo                         SETUP COMPLETED SUCCESSFULLY!
echo ==============================================================================
echo.
echo [*] Opening VS Code to 'my_model_training.ipynb'...
where code >nul 2>&1
if %errorlevel% equ 0 (
    code my_model_training.ipynb
    echo [OK] VS Code launched successfully.
) else (
    echo [INFO] 'code' command not in PATH. Please open VS Code manually and open:
    echo        my_model_training.ipynb
)
echo.
echo ==============================================================================
echo                          4 SIMPLE INSTRUCTIONS:
echo ==============================================================================
echo  1. VS Code has opened 'my_model_training.ipynb'.
echo  2. Look at the top-right corner of the notebook and click: [ Select Kernel ]
echo  3. Choose: [ Python Environments... ] -> [ Python (X-IDS Machine Learning) ]
echo  4. Press the audio play button on each task to listen to Fel7o and run code!
echo ==============================================================================
echo.
pause
