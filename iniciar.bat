@echo off
title YouTube Downloader - Servidor Local

echo ====================================
echo  YouTube Downloader - Iniciando
echo ====================================
echo.
echo [*] Iniciando servidor local...
echo [*] Aguarde...
echo.

REM Descobrir IP local
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do set IP=%%a
set IP=%IP: =%

python app.py

REM Se der erro, mostrar mensagem
if errorlevel 1 (
    echo.
    echo [ERRO] Falha ao iniciar servidor!
    echo.
    echo Execute primeiro: instalar-windows.bat
    echo.
    pause
)
