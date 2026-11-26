@echo off
setlocal enabledelayedexpansion
title X-IDS: One-Click Autonomous Installer

echo ==============================================================================
echo        X-IDS: Explainable Network Intrusion Detection System
echo                  One-Click Student Setup and Installer
echo ==============================================================================
echo.
echo [*] Welcome to the X-IDS Academic Graduation Project.
echo [*] Initializing automated environment setup and dependency verification...
echo.

:: ----------------------------------------------------------------------------
:: 1. If already inside the project folder, just run START_PROJECT.bat
:: ----------------------------------------------------------------------------
if exist "START_PROJECT.bat" (
    echo [*] Project repository already located. Launching environment...
    call START_PROJECT.bat
    exit /b %errorlevel%
)

if exist "X-IDS-Project\START_PROJECT.bat" (
    echo [*] Entering project directory: X-IDS-Project...
    cd X-IDS-Project
    call START_PROJECT.bat
    exit /b %errorlevel%
)

:: ----------------------------------------------------------------------------
:: 2. Download / Clone the repository from GitHub
:: ----------------------------------------------------------------------------
echo [*] Fetching project files from GitHub (https://github.com/Ahmed77khaled/X-IDS-Project)...

where git >nul 2>&1
if %errorlevel% equ 0 (
    git clone https://github.com/Ahmed77khaled/X-IDS-Project.git
    if %errorlevel% equ 0 (
        echo [OK] Project cloned successfully via Git.
        cd X-IDS-Project
        call START_PROJECT.bat
        exit /b %errorlevel%
    )
)

echo [*] Downloading latest project package via PowerShell (Standalone Zip)...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^
    "$zipFile = 'X-IDS-Project-main.zip'; " ^
    "Invoke-WebRequest -Uri 'https://github.com/Ahmed77khaled/X-IDS-Project/archive/refs/heads/main.zip' -OutFile $zipFile; " ^
    "Expand-Archive -Path $zipFile -DestinationPath '.' -Force; " ^
    "Remove-Item -Path $zipFile -Force; " ^
    "if (Test-Path 'X-IDS-Project-main') { Rename-Item 'X-IDS-Project-main' 'X-IDS-Project' }"

if exist "X-IDS-Project\START_PROJECT.bat" (
    echo [OK] Project files extracted successfully.
    cd X-IDS-Project
    call START_PROJECT.bat
    exit /b %errorlevel%
) else (
    echo [ERROR] Failed to download project files automatically.
    echo         Please check your internet connection and try again.
    if not defined CI if not defined GITHUB_ACTIONS pause
    exit /b 1
)
