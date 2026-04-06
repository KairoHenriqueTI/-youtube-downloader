# 📊 Visualizador de Logs

Para ver os logs em tempo real na VPS:

```bash
# Conectar na VPS
ssh root@143.110.205.106

# Ver logs em tempo real
tail -f /var/www/youtube-downloader/youtube-downloader.log

# Ver últimas 100 linhas
tail -100 /var/www/youtube-downloader/youtube-downloader.log

# Ver apenas erros
grep -i error /var/www/youtube-downloader/youtube-downloader.log

# Ver logs do systemd
journalctl -u youtube-downloader -f
```

## O que é registrado:

- ✅ Cada requisição de download
- ✅ URL e parâmetros
- ✅ Se está usando cookies
- ✅ Formato escolhido (MP3/MP4)
- ✅ Erros detalhados com stack trace
- ✅ Sucesso dos downloads
- ✅ Upload de cookies

## Localização do arquivo de log:

`/var/www/youtube-downloader/youtube-downloader.log`
