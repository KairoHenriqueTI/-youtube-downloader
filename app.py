from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import glob
import logging
from pathlib import Path
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/www/youtube-downloader/youtube-downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

DOWNLOAD_FOLDER = str(Path.home() / 'Downloads' / 'youtube-videos')
COOKIES_FILE = os.path.join('/var/www/youtube-downloader', 'cookies.txt')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-cookies', methods=['POST'])
def upload_cookies():
    try:
        logger.info("Recebendo upload de cookies")
        if 'cookies' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['cookies']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Arquivo vazio'}), 400
        
        file.save(COOKIES_FILE)
        logger.info(f"Cookies salvos em: {COOKIES_FILE}")
        
        # Verificar tamanho do arquivo
        size = os.path.getsize(COOKIES_FILE)
        logger.info(f"Tamanho do arquivo de cookies: {size} bytes")
        
        return jsonify({
            'success': True,
            'message': f'✅ Cookies salvos! ({size} bytes) Agora os downloads devem funcionar.'
        })
    except Exception as e:
        logger.error(f"Erro ao fazer upload de cookies: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        url = data.get('url')
        is_playlist = data.get('is_playlist', False)
        format_type = data.get('format_type', 'mp4')
        
        logger.info(f"=== NOVA REQUISIÇÃO ===")
        logger.info(f"URL: {url}")
        logger.info(f"Playlist: {is_playlist}")
        logger.info(f"Formato: {format_type}")
        
        if not url:
            return jsonify({'success': False, 'error': 'URL não fornecida'}), 400
        
        # Configurações base
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': not is_playlist,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'nocheckcertificate': True,
            'verbose': True,  # Ativar modo verbose
        }
        
        # Configurar formato específico
        if format_type == 'mp3':
            logger.info("Configurando para download MP3")
            ydl_opts['format'] = None  # Deixar yt-dlp escolher o melhor
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ydl_opts['writethumbnail'] = False
        else:  # mp4
            logger.info("Configurando para download MP4")
            ydl_opts['format'] = None  # Deixar yt-dlp escolher o melhor
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegMetadata',
            }]
        
        # Usar cookies se existir
        if os.path.exists(COOKIES_FILE):
            logger.info(f"Usando arquivo de cookies: {COOKIES_FILE}")
            ydl_opts['cookiefile'] = COOKIES_FILE
        else:
            logger.warning("Arquivo de cookies NÃO encontrado!")
        
        logger.info(f"Iniciando download...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if is_playlist:
                videos = info.get('entries', [])
                titles = [v.get('title', 'Unknown') for v in videos if v]
                logger.info(f"Playlist baixada: {len(titles)} arquivos")
                message = f'✅ Playlist baixada com sucesso! {len(titles)} arquivos em {format_type.upper()}.'
            else:
                title = info.get('title', 'Unknown')
                logger.info(f"Vídeo baixado: {title}")
                message = f'✅ "{title}" baixado em {format_type.upper()}!'
        
        logger.info("Download concluído com sucesso!")
        return jsonify({
            'success': True,
            'message': message,
            'download_folder': DOWNLOAD_FOLDER
        })
    
    except Exception as e:
        error_msg = str(e)
        logger.error(f"ERRO NO DOWNLOAD: {error_msg}", exc_info=True)
        
        if 'Sign in to confirm' in error_msg or 'bot' in error_msg.lower():
            return jsonify({
                'success': False,
                'error': '❌ Bloqueio detectado! Você precisa fazer upload dos cookies do seu navegador. Veja as instruções acima.'
            }), 500
        
        if 'Requested format is not available' in error_msg:
            logger.error("Erro de formato - vídeo pode ter proteção especial")
            return jsonify({
                'success': False,
                'error': f'❌ Formato não disponível. O vídeo pode ter proteção do YouTube. Tente outro vídeo. Detalhes: {error_msg}'
            }), 500
            
        return jsonify({
            'success': False,
            'error': f'Erro ao baixar: {error_msg}'
        }), 500

@app.route('/list-downloads')
def list_downloads():
    try:
        files = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*.mp4'))
        files += glob.glob(os.path.join(DOWNLOAD_FOLDER, '*.mp3'))
        files.sort(key=os.path.getmtime, reverse=True)
        
        file_list = []
        for f in files[:20]:
            file_list.append({
                'name': os.path.basename(f),
                'size': f"{os.path.getsize(f) / (1024*1024):.1f} MB",
                'path': f
            })
        
        return jsonify({
            'success': True,
            'files': file_list,
            'folder': DOWNLOAD_FOLDER,
            'has_cookies': os.path.exists(COOKIES_FILE)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/logs')
def view_logs():
    try:
        log_file = '/var/www/youtube-downloader/youtube-downloader.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                # Últimas 200 linhas
                lines = f.readlines()[-200:]
                log_content = ''.join(lines)
        else:
            log_content = 'Nenhum log ainda. Faça um download primeiro.'
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>📊 Logs do Sistema</title>
            <style>
                body {{ 
                    background: #1e1e1e; 
                    color: #d4d4d4; 
                    font-family: 'Consolas', 'Monaco', monospace;
                    padding: 20px;
                }}
                pre {{
                    background: #252526;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                    border: 1px solid #3e3e3e;
                    line-height: 1.5;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                }}
                .refresh {{
                    background: #007acc;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-bottom: 20px;
                }}
                .refresh:hover {{ background: #005a9e; }}
            </style>
            <script>
                function refreshLogs() {{
                    location.reload();
                }}
                // Auto-refresh a cada 5 segundos
                setTimeout(refreshLogs, 5000);
            </script>
        </head>
        <body>
            <div class="header">
                <h1>📊 Logs do YouTube Downloader</h1>
                <p>Últimas 200 linhas | Auto-refresh a cada 5 segundos</p>
            </div>
            <button class="refresh" onclick="refreshLogs()">🔄 Atualizar Agora</button>
            <pre>{log_content}</pre>
        </body>
        </html>
        """
    except Exception as e:
        return f"Erro ao ler logs: {str(e)}", 500

if __name__ == '__main__':
    print(f"\n🎬 YouTube Downloader iniciado!")
    print(f"📁 Vídeos serão salvos em: {DOWNLOAD_FOLDER}")
    print(f"🌐 Acesse: http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
