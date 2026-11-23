@echo off

chcp 65001 > nul

setlocal enabledelayedexpansion

title X-IDS: One-Click Installer and Autonomous Setup

echo ==============================================================================

echo       X-IDS: Explainable Network Intrusion Detection System

echo                  One-Click Student Setup and Installer

echo ==============================================================================

echo.

echo [*] أهلاً بك في مشروع التخرج X-IDS.

echo [*] جاري إعداد وتثبيت كل ما تحتاجه للبدء في المشروع بضغطة زر واحدة...

echo.

:: ----------------------------------------------------------------------------

:: 1. If already inside the project folder, just run START_PROJECT.bat

:: ----------------------------------------------------------------------------

if exist "START_PROJECT.bat" (

    echo [*] أنت بالفعل داخل مجلد المشروع، جاري التشغيل المباشر...

    call START_PROJECT.bat

    exit /b 0

)

if exist "X-IDS-Project\START_PROJECT.bat" (

    cd X-IDS-Project

    call START_PROJECT.bat

    exit /b 0

)

:: ----------------------------------------------------------------------------

:: 2. Download / Clone the repository from GitHub

:: ----------------------------------------------------------------------------

echo [*] جاري تنزيل ملفات المشروع من GitHub (https://github.com/Ahmed77khaled/X-IDS-Project)...

where git >nul 2>&1

if %errorlevel% equ 0 (

    git clone https://github.com/Ahmed77khaled/X-IDS-Project.git

    if %errorlevel% equ 0 (

        echo [OK] تم استنساخ المشروع بنجاح عبر Git.

        cd X-IDS-Project

        call START_PROJECT.bat

        exit /b 0

    )

)

echo [*] جاري التنزيل المباشر عبر PowerShell (Standalone Zip Download)...

powershell -NoProfile -ExecutionPolicy Bypass -Command ^

    "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; " ^

    "$zipFile = 'X-IDS-Project-main.zip'; " ^

    "Invoke-WebRequest -Uri 'https://github.com/Ahmed77khaled/X-IDS-Project/archive/refs/heads/main.zip' -OutFile $zipFile; " ^

    "Expand-Archive -Path $zipFile -DestinationPath '.' -Force; " ^

    "Remove-Item -Path $zipFile -Force; " ^

    "if (Test-Path 'X-IDS-Project-main') { Rename-Item 'X-IDS-Project-main' 'X-IDS-Project' }"

if exist "X-IDS-Project\START_PROJECT.bat" (

    echo [OK] تم تنزيل واستخراج المشروع بنجاح.

    cd X-IDS-Project

    call START_PROJECT.bat

    exit /b 0

) else (

    echo [ERROR] تعذر تنزيل المشروع تلقائياً. تأكد من اتصال الإنترنت وحاول مجدداً.

    pause

    exit /b 1

)

