# 🚀 YouTube Downloader - Instalação Local

## 📥 Download

```bash
git clone https://github.com/KairoHenriqueTI/-youtube-downloader.git
cd -youtube-downloader
```

Ou baixe o ZIP: https://github.com/KairoHenriqueTI/-youtube-downloader/archive/refs/heads/main.zip

---

## 🪟 Windows

### Instalação Rápida:

1. **Baixe o projeto** (link acima)
2. **Execute:** `instalar-windows.bat`
3. **Inicie:** `iniciar.bat`
4. **Acesse:** http://localhost:5000

### Instalação Manual:

```cmd
# 1. Instalar Python (se não tiver)
# Baixe de: https://www.python.org/downloads/
# IMPORTANTE: Marque "Add Python to PATH"

# 2. Instalar dependências
pip install flask yt-dlp

# 3. Instalar FFmpeg (opcional, para conversão)
# Baixe de: https://ffmpeg.org/download.html
# Ou use Chocolatey: choco install ffmpeg

# 4. Iniciar servidor
python app.py
```

---

## 🐧 Linux / 🍎 macOS

### Instalação Rápida:

```bash
# 1. Tornar scripts executáveis
chmod +x instalar-linux.sh iniciar.sh

# 2. Instalar
./instalar-linux.sh

# 3. Iniciar
./iniciar.sh
```

### Instalação Manual:

```bash
# 1. Instalar Python e FFmpeg
# Ubuntu/Debian:
sudo apt install python3 python3-pip ffmpeg

# Fedora:
sudo dnf install python3 python3-pip ffmpeg

# macOS:
brew install python3 ffmpeg

# 2. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install flask yt-dlp

# 4. Iniciar servidor
python app.py
```

---

## 📱 Acessar de Outros Dispositivos

### Descubra o IP do seu PC:

**Windows:**
```cmd
ipconfig
```
Procure por "IPv4" (exemplo: 192.168.1.100)

**Linux/macOS:**
```bash
ifconfig
# ou
hostname -I
```

### Acesse do celular/tablet:

```
http://192.168.1.100:5000
```
(substitua pelo seu IP)

---

## 🎯 Uso

1. **Abra o navegador:** http://localhost:5000
2. **Cole a URL** do vídeo/playlist do YouTube
3. **Escolha o formato:**
   - 🎬 MP4 - Vídeo completo
   - 🎵 MP3 - Só áudio (música)
4. **Clique em "Baixar"**
5. **Arquivos salvos em:** `~/Downloads/youtube-videos/`

---

## ❓ Problemas Comuns

### "Python não encontrado"
- Windows: Reinstale Python e marque "Add to PATH"
- Linux: `sudo apt install python3`
- macOS: `brew install python3`

### "FFmpeg não encontrado"
- Funciona sem FFmpeg, mas não converte formatos
- Windows: https://ffmpeg.org/download.html
- Linux: `sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`

### "Porta 5000 já em uso"
Edite `app.py` e mude a porta:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Downloads dão erro
- Tente fazer upload dos cookies (veja instruções no site)
- Alguns vídeos têm proteção do YouTube
- Tente outro vídeo primeiro

---

## 🔥 Vantagens da Versão Local

✅ **Funciona 100%** - Sem bloqueios do YouTube  
✅ **Mais rápido** - Download direto no seu PC  
✅ **Sem limites** - Baixe quantos vídeos quiser  
✅ **Privacidade** - Tudo local, nada na nuvem  
✅ **Acesso WiFi** - Celular/tablet podem usar  
✅ **Gratuito** - Sem custos de servidor  

---

## 💡 Dica para o Pai

1. **Deixe o PC ligado** com o servidor rodando
2. **Seu pai acessa do celular** (mesmo WiFi)
3. **Cola o link da playlist** de música
4. **Escolhe MP3**
5. **Baixa tudo**
6. **Copia pro pendrive** da pasta Downloads
7. **Coloca no carro** 🚗🎵

Pronto! Sistema 100% funcional e fácil de usar!
