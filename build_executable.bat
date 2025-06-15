@echo off
title Building Stellar Blade Mod Tool
echo ====================================
echo Building Stellar Blade Mod Tool
echo ====================================
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo PyInstaller found. Starting build...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "__pycache__" rmdir /s /q "__pycache__"

REM Build using spec file for better control
echo Building executable...
pyinstaller stellar_blade_mod.spec

if errorlevel 1 (
    echo.
    echo ====================================
    echo BUILD FAILED!
    echo ====================================
    pause
    exit /b 1
)

echo.
echo ====================================
echo BUILD SUCCESSFUL!
echo ====================================
echo.
echo Executable created at: dist\StellarBladeModTool.exe
echo.

REM Copy additional files to dist folder
echo Copying additional files...
copy "readme.md" "dist\" >nul 2>&1
copy "requirements.txt" "dist\" >nul 2>&1

echo.
echo Files ready for distribution in the 'dist' folder:
dir "dist"

echo.
echo ====================================
echo PACKAGING COMPLETE!
echo ====================================
echo.
echo You can now distribute the contents of the 'dist' folder.
echo The main executable is: StellarBladeModTool.exe
echo.
pause
