@echo off
title nevartrend E-Ticaret Sunucusu (Trenddesen)
echo ========================================================
echo    nevartrend E-Ticaret Platformu Baslatiliyor...
echo    by Trenddesen
echo ========================================================
echo.
cd /d "%~dp0"
python -m pip install -r requirements.txt
echo.
echo Tarayicinizda aciliyor: http://127.0.0.1:8000
start http://127.0.0.1:8000
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
