@echo off
echo ====================================
echo  YouTube Downloader - Instalador
echo ====================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Baixe e instale Python de: https://www.python.org/downloads/
    echo Marque a opcao "Add Python to PATH" durante instalacao
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

REM Instalar dependências
echo [*] Instalando dependencias...
pip install flask yt-dlp

REM Verificar FFmpeg
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo.
    echo [AVISO] FFmpeg nao encontrado!
    echo Para converter videos, baixe FFmpeg de: https://ffmpeg.org/download.html
    echo Ou use Chocolatey: choco install ffmpeg
    echo.
    echo O downloader funcionara sem FFmpeg, mas sem conversao.
    timeout /t 5
)

echo.
echo ====================================
echo  Instalacao Concluida!
echo ====================================
echo.
echo Para iniciar o servidor, execute:
echo   iniciar.bat
echo.
echo Ou execute manualmente:
echo   python app.py
echo.
pause
