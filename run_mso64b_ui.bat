@echo off
setlocal

cd /d "%~dp0"

echo Starting MSO64B local bench UI...
echo.
echo Open this address in a browser:
echo http://127.0.0.1:5000
echo.
echo Press CTRL+C in this window to stop the UI.
echo.

python scripts\mso64b_ui.py

pause
