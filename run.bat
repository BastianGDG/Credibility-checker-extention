@echo off
SETLOCAL

REM Check for Python in PATH
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    where py >nul 2>nul
    if %ERRORLEVEL% neq 0 (
        echo Python is not found in PATH. Please install Python or add it to PATH.
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=py
    )
) else (
    set PYTHON_CMD=python
)

REM Check if pip is available
%PYTHON_CMD% -m pip --version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo Installing required Python packages...
%PYTHON_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install requirements. Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Check if Server.py exists
if not exist ".\Python\Server.py" (
    echo Error: Server.py not found in Python directory
    pause
    exit /b 1
)

echo Starting Credibility Checker server...
cd Python
%PYTHON_CMD% Server.py

if %ERRORLEVEL% neq 0 (
    echo Server failed to start. Please check if port 5000 is available.
    pause
)

ENDLOCAL