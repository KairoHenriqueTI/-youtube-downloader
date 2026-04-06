# 🚀 Guia de Deploy

## Opção 1: Deploy na Vercel (Fácil e Grátis)

### ⚠️ IMPORTANTE: Limitações da Vercel
A Vercel tem **limite de 50MB** para downloads e **10 segundos** de execução. Para vídeos grandes ou playlists, use a **VPS** (Opção 2).

### Passo a passo:

1. **Instale a CLI da Vercel:**
```bash
npm install -g vercel
```

2. **Entre na pasta do projeto:**
```bash
cd ~/projects/youtube-downloader
```

3. **Faça login na Vercel:**
```bash
vercel login
```

4. **Deploy:**
```bash
vercel --prod
```

5. **Pronto!** A Vercel vai te dar um link tipo: `https://seu-projeto.vercel.app`

### 🔄 Para atualizar:
```bash
vercel --prod
```

---

## Opção 2: Deploy na VPS (Recomendado para vídeos grandes)

### ✅ Vantagens da VPS:
- Sem limites de tamanho de vídeo
- Sem limites de tempo de download
- Playlists grandes funcionam perfeitamente
- Mais controle e velocidade

### Passo a passo:

1. **Conecte na sua VPS:**
```bash
ssh seu-usuario@ip-da-vps
```

2. **Clone ou envie o projeto para a VPS:**
```bash
# Se tiver git:
git clone seu-repositorio
cd youtube-downloader

# Ou copie os arquivos:
scp -r ~/projects/youtube-downloader seu-usuario@ip-da-vps:/home/seu-usuario/projects/
```

3. **Execute o script de deploy:**
```bash
cd ~/projects/youtube-downloader
chmod +x deploy-vps.sh
bash deploy-vps.sh
```

4. **Acesse no navegador:**
```
http://IP-DA-SUA-VPS
```

### 🔧 Comandos úteis na VPS:

```bash
# Ver logs em tempo real
sudo journalctl -u youtube-downloader -f

# Reiniciar o serviço
sudo systemctl restart youtube-downloader

# Ver status
sudo systemctl status youtube-downloader

# Parar o serviço
sudo systemctl stop youtube-downloader

# Iniciar o serviço
sudo systemctl start youtube-downloader
```

### 🌐 Configurar domínio (opcional):

Se você tiver um domínio, edite o nginx:

```bash
sudo nano /etc/nginx/sites-available/youtube-downloader
```

Troque a linha:
```nginx
server_name _;
```

Por:
```nginx
server_name seudominio.com.br;
```

E reinicie:
```bash
sudo systemctl restart nginx
```

### 🔒 SSL/HTTPS com Let's Encrypt (opcional):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seudominio.com.br
```

---

## 🎯 Qual escolher?

### Use **Vercel** se:
- ✅ Quer algo rápido e gratuito
- ✅ Vai baixar apenas vídeos individuais pequenos
- ✅ Não quer se preocupar com servidor

### Use **VPS** se:
- ✅ Vai baixar playlists grandes
- ✅ Quer baixar vídeos HD/4K
- ✅ Precisa de mais controle
- ✅ Já tem uma VPS disponível

---

## 📱 Acessar de outro dispositivo na mesma rede

Se quiser que seu pai acesse do celular/tablet na mesma rede WiFi:

1. Descubra o IP da sua máquina:
```bash
hostname -I
```

2. Acesse no navegador do outro dispositivo:
```
http://SEU-IP:5000
```

Exemplo: `http://192.168.1.100:5000`

---

## ❓ Problemas Comuns

### Erro "ffmpeg not found"
```bash
sudo apt install ffmpeg
```

### Porta 5000 já está em uso
Mude a porta no `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Nginx não está rodando
```bash
sudo systemctl start nginx
sudo systemctl status nginx
```
