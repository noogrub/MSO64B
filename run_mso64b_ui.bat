@echo off
setlocal

cd /d "%~dp0"

set "ARIA_JUPYTER_PYTHON=C:\Users\John\jupyter\Scripts\python.exe"

echo Starting MSO64B local bench UI...
echo.
echo Open this address in a browser:
echo http://127.0.0.1:5000
echo.
echo Press CTRL+C in this window to stop the UI.
echo.

if exist "%ARIA_JUPYTER_PYTHON%" (
    echo Using Python: %ARIA_JUPYTER_PYTHON%
    "%ARIA_JUPYTER_PYTHON%" scripts\mso64b_ui.py
) else (
    echo Using Python from PATH.
    python scripts\mso64b_ui.py
)

pause
