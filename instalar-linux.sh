#!/bin/bash

echo "===================================="
echo " YouTube Downloader - Instalador"
echo "===================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo ""
    echo "Instale com:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "[OK] Python3 encontrado!"
echo ""

# Criar venv
echo "[*] Criando ambiente virtual..."
python3 -m venv venv

# Ativar venv
source venv/bin/activate

# Instalar dependências
echo "[*] Instalando dependências..."
pip install flask yt-dlp

# Verificar FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo ""
    echo "[AVISO] FFmpeg não encontrado!"
    echo "Para converter vídeos, instale FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  Fedora: sudo dnf install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo ""
    echo "O downloader funcionará sem FFmpeg, mas sem conversão."
    sleep 3
fi

echo ""
echo "===================================="
echo " Instalação Concluída!"
echo "===================================="
echo ""
echo "Para iniciar o servidor, execute:"
echo "  ./iniciar.sh"
echo ""
echo "Ou execute manualmente:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
