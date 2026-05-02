@echo off
REM Bloch Sphere - One-click environment setup (Windows)
setlocal enabledelayedexpansion

echo === Bloch Sphere Environment Setup ===

where conda >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: conda not found. Please install Miniforge or Anaconda first.
    pause
    exit /b 1
)

set ENV_NAME=bloch
set SCRIPT_DIR=%~dp0

conda env list | findstr /B /C:"%ENV_NAME% " >nul
if %ERRORLEVEL% EQU 0 (
    echo Environment '%ENV_NAME%' already exists.
    set /p answer="Remove and recreate? [y/N]: "
    if /I "!answer!"=="y" (
        conda env remove -n %ENV_NAME% -y
    ) else (
        echo Activate with: conda activate %ENV_NAME%
        echo Run with: streamlit run app.py
        pause
        exit /b 0
    )
)

echo Creating conda environment '%ENV_NAME%'...
conda env create -f "%SCRIPT_DIR%environment.yml"

echo.
echo === Setup Complete ===
echo Activate:  conda activate %ENV_NAME%
echo Run:       streamlit run app.py
pause
