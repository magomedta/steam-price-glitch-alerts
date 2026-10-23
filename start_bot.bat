@echo off
cd /d "%~dp0"
title Autonomous Price Glitch Hunter (@price_glitch_live)

:start
echo ===================================================
echo Starting Price Glitch Live Scanner 24/7...
echo ===================================================
python main.py
echo.
echo [!] Scanner process exited. Auto-restarting in 5 seconds...
timeout /t 5 /nobreak
goto :start
