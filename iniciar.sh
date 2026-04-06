#!/bin/bash

echo "===================================="
echo " YouTube Downloader - Iniciando"
echo "===================================="
echo ""
echo "[*] Iniciando servidor local..."
echo ""

# Ativar ambiente virtual
source venv/bin/activate

# Descobrir IP local
IP=$(hostname -I | awk '{print $1}')

echo "✅ Servidor iniciado!"
echo ""
echo "📱 Acesse de qualquer dispositivo na mesma rede WiFi:"
echo ""
echo "   http://localhost:5000"
echo "   http://$IP:5000"
echo ""
echo "💡 No celular/tablet, use: http://$IP:5000"
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

# Iniciar servidor
python app.py
