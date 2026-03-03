@echo off
echo Starting Tiger-Skills Frontend Server...
echo.
echo   URL: http://127.0.0.1:3000/?ticker=ADBE
echo.
cd /d "%~dp0.."
call venv\Scripts\activate
python tools\simple_frontend_server.py
pause
