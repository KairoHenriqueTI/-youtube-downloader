# 📹 YouTube Downloader

Site simples para baixar vídeos e playlists do YouTube em MP4 ou MP3.

## 🎯 Duas Formas de Usar

### 🌐 Opção 1: Site Hospedado (Com Limitações)
**URL:** https://youtube.kairohenrique.dev

⚠️ **Importante:** O site hospedado tem limitações devido ao bloqueio do YouTube em IPs de datacenter. Alguns vídeos podem não funcionar.

### 💻 Opção 2: Instalação Local (100% Funcional) ⭐ RECOMENDADO

Rode no seu computador para **zero bloqueios** e **100% de compatibilidade**!

**Instalação super fácil:**

#### Windows:
1. Clone/baixe este repositório
2. Execute `instalar-windows.bat`
3. Execute `iniciar.bat`
4. Acesse http://localhost:5000

#### Linux/macOS:
```bash
chmod +x instalar-linux.sh iniciar.sh
./instalar-linux.sh
./iniciar.sh
```

📖 **Guia completo:** [INSTALACAO-LOCAL.md](INSTALACAO-LOCAL.md)

---

## ✨ Funcionalidades

- 📹 **Download de vídeos** individuais
- 📋 **Download de playlists** completas
- 🎬 **MP4** - Vídeo completo com áudio
- 🎵 **MP3** - Apenas áudio (perfeito para música no carro!)
- 🍪 **Suporte a cookies** para contornar bloqueios
- 📊 **Logs em tempo real** para debug
- 🔒 **HTTPS** (versão hospedada)
- 📱 **Acesso via WiFi** de qualquer dispositivo na mesma rede

---

## 🚀 Uso Rápido

1. Cole a URL do YouTube
2. Escolha MP4 (vídeo) ou MP3 (áudio)
3. Marque se é playlist
4. Clique em "Baixar"
5. Arquivos salvos em `~/Downloads/youtube-videos/`

---

## 📚 Documentação

- **[INSTALACAO-LOCAL.md](INSTALACAO-LOCAL.md)** - Como rodar localmente (RECOMENDADO)
- **[GUIA-COOKIES.md](GUIA-COOKIES.md)** - Como exportar cookies do navegador
- **[DEPLOY.md](DEPLOY.md)** - Deploy na VPS ou Vercel
- **[SITUACAO-ATUAL.md](SITUACAO-ATUAL.md)** - Por que rodar local é melhor
- **[LOGS.md](LOGS.md)** - Como visualizar logs

---

## 🎯 Perfeito Para

- ✅ Baixar músicas para ouvir no carro
- ✅ Salvar playlists completas
- ✅ Converter vídeos em MP3
- ✅ Downloads offline
- ✅ Backup de vídeos importantes

---

## 🔧 Tecnologias

- **Backend:** Python + Flask + Gunicorn
- **Download:** yt-dlp (fork mantido do youtube-dl)
- **Conversão:** FFmpeg
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Deploy:** Nginx + Let's Encrypt SSL

---

## ⚠️ Avisos Importantes

### Versão Hospedada (youtube.kairohenrique.dev):
- YouTube bloqueia IPs de datacenters
- Necessário upload de cookies
- Alguns vídeos podem falhar
- Veja [SITUACAO-ATUAL.md](SITUACAO-ATUAL.md) para detalhes

### Versão Local (Recomendado):
- ✅ Funciona 100% - sem bloqueios
- ✅ Mais rápido e confiável
- ✅ Sem necessidade de cookies
- ✅ Privacidade total

---

## 📖 Guia Rápido de Instalação Local

### Windows (1 minuto):
```cmd
git clone https://github.com/KairoHenriqueTI/-youtube-downloader.git
cd -youtube-downloader
instalar-windows.bat
iniciar.bat
```

### Linux/macOS (1 minuto):
```bash
git clone https://github.com/KairoHenriqueTI/-youtube-downloader.git
cd -youtube-downloader
chmod +x *.sh
./instalar-linux.sh
./iniciar.sh
```

Acesse: http://localhost:5000

---

## 🤝 Contribuindo

PRs são bem-vindos! Para mudanças grandes, abra uma issue primeiro.

---

## 📜 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes

---

## 💡 Dica para Usar com o Pai

1. **Instale no PC** usando os scripts acima
2. **Deixe rodando** (não precisa fechar)
3. **Seu pai acessa do celular** (mesmo WiFi): `http://IP-DO-PC:5000`
4. **Cola link da playlist** de músicas
5. **Escolhe MP3**
6. **Baixa tudo de uma vez**
7. **Copia pro pendrive** da pasta Downloads
8. **Coloca no carro** 🚗🎵

**Simples assim!**

---

**Criado com ❤️ para facilitar os downloads do YouTube!**

