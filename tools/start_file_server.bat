@echo off
echo Starting Static File Server on http://localhost:8181 ...
echo Serving from: %~dp0..
echo.
cd /d "%~dp0.."
python -m http.server 8181 --bind 127.0.0.1
pause
