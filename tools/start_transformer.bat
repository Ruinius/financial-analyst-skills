@echo off
echo Starting Tiger-Transformer Server...
cd /d "%~dp0.."
call venv\Scripts\activate
python tools\tiger_transformer_server.py
pause
