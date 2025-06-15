<<<<<<< HEAD
# Create updated batch file
batch_content = '''@echo off
title Stellar Blade Menu Background Changer v1.0.0
echo ================================================================
echo Stellar Blade Menu Background Changer v1.0.0
echo Now with RAD Video Tools support for proper BK2 conversion!
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found. Checking for required modules...

REM Test tkinter import
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: tkinter module not found!
    echo.
    echo This usually means Python was installed without GUI support.
    echo Please reinstall Python and make sure "tcl/tk and IDLE" is selected.
    echo.
    pause
    exit /b 1
)

echo tkinter module found.

REM Check if RAD Video Tools reminder
echo.
echo IMPORTANT REMINDER:
echo RAD Video Tools is REQUIRED for this mod to work properly!
echo Download from: https://www.radgametools.com/down/Bink/RADTools.7z
echo Install to: C:\Program Files (x86)\RADVideo
echo.

REM Check if the Python script exists
if not exist "menu_background_changer.py" (
    echo ERROR: menu_background_changer.py not found in current directory!
    echo.
    echo Make sure all mod files are in the same folder:
    echo - menu_background_changer.py
    echo - run_stellar_blade_mod.bat
    echo - requirements.txt
    echo - installation_guide.md
    echo.
    pause
    exit /b 1
)

echo Starting Stellar Blade Mod Tool...
echo.

REM Run the Python script
python menu_background_changer.py

REM Check if there was an error
if errorlevel 1 (
    echo.
    echo ================================================================
    echo The application encountered an error.
    echo Please check the stellar_blade_mod.log file for details.
    echo ================================================================
    echo.
)

echo.
echo Application closed.
pause
'''

with open("run_stellar_blade_mod.bat", "w", encoding="utf-8") as f:
    f.write(batch_content)

=======
# Create updated batch file
batch_content = '''@echo off
title Stellar Blade Menu Background Changer v1.0.0
echo ================================================================
echo Stellar Blade Menu Background Changer v1.0.0
echo Now with RAD Video Tools support for proper BK2 conversion!
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Python found. Checking for required modules...

REM Test tkinter import
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERROR: tkinter module not found!
    echo.
    echo This usually means Python was installed without GUI support.
    echo Please reinstall Python and make sure "tcl/tk and IDLE" is selected.
    echo.
    pause
    exit /b 1
)

echo tkinter module found.

REM Check if RAD Video Tools reminder
echo.
echo IMPORTANT REMINDER:
echo RAD Video Tools is REQUIRED for this mod to work properly!
echo Download from: https://www.radgametools.com/down/Bink/RADTools.7z
echo Install to: C:\Program Files (x86)\RADVideo
echo.

REM Check if the Python script exists
if not exist "menu_background_changer.py" (
    echo ERROR: menu_background_changer.py not found in current directory!
    echo.
    echo Make sure all mod files are in the same folder:
    echo - menu_background_changer.py
    echo - run_stellar_blade_mod.bat
    echo - requirements.txt
    echo - installation_guide.md
    echo.
    pause
    exit /b 1
)

echo Starting Stellar Blade Mod Tool...
echo.

REM Run the Python script
python menu_background_changer.py

REM Check if there was an error
if errorlevel 1 (
    echo.
    echo ================================================================
    echo The application encountered an error.
    echo Please check the stellar_blade_mod.log file for details.
    echo ================================================================
    echo.
)

echo.
echo Application closed.
pause
'''

with open("run_stellar_blade_mod.bat", "w", encoding="utf-8") as f:
    f.write(batch_content)

>>>>>>> 95b0d987115a73739c1a92bc44a8cb03a8686d7e
print("Updated run_stellar_blade_mod.bat")