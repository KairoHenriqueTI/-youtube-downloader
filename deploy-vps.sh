#!/bin/bash

# Script de deploy para VPS
# Execute com: bash deploy-vps.sh

echo "🚀 Iniciando deploy na VPS..."

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Diretório do projeto
PROJECT_DIR="/home/$(whoami)/projects/youtube-downloader"

# 1. Instalar dependências do sistema
echo -e "${YELLOW}📦 Instalando dependências do sistema...${NC}"
sudo apt update
sudo apt install -y python3-pip python3-venv nginx ffmpeg

# 2. Criar e ativar ambiente virtual
echo -e "${YELLOW}🐍 Configurando ambiente Python...${NC}"
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 3. Criar serviço systemd
echo -e "${YELLOW}⚙️  Criando serviço systemd...${NC}"
sudo tee /etc/systemd/system/youtube-downloader.service > /dev/null <<EOF
[Unit]
Description=YouTube Downloader Web App
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:app

[Install]
WantedBy=multi-user.target
EOF

# 4. Configurar Nginx
echo -e "${YELLOW}🌐 Configurando Nginx...${NC}"
sudo tee /etc/nginx/sites-available/youtube-downloader > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    client_max_body_size 100M;
    proxy_read_timeout 300s;
    proxy_connect_timeout 300s;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Ativar site
sudo ln -sf /etc/nginx/sites-available/youtube-downloader /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração do Nginx
sudo nginx -t

# 5. Iniciar serviços
echo -e "${YELLOW}🔄 Iniciando serviços...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable youtube-downloader
sudo systemctl start youtube-downloader
sudo systemctl restart nginx

# 6. Verificar status
echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo ""
echo "📊 Status dos serviços:"
sudo systemctl status youtube-downloader --no-pager -l
echo ""
echo "🌐 Acesse o site em: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "📝 Comandos úteis:"
echo "  - Ver logs: sudo journalctl -u youtube-downloader -f"
echo "  - Reiniciar: sudo systemctl restart youtube-downloader"
echo "  - Parar: sudo systemctl stop youtube-downloader"
