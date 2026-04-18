@echo off
echo Starting Tiger-Transformer Server...
cd /d "%~dp0.."
uv run tools\tiger_transformer_server.py
pause
