from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import glob
from pathlib import Path

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
        if 'cookies' not in request.files:
            return jsonify({'success': False, 'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['cookies']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'Arquivo vazio'}), 400
        
        file.save(COOKIES_FILE)
        return jsonify({
            'success': True,
            'message': '✅ Cookies salvos! Agora os downloads devem funcionar.'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        url = data.get('url')
        is_playlist = data.get('is_playlist', False)
        format_type = data.get('format_type', 'mp4')  # 'mp4' ou 'mp3'
        
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
            'quiet': False,
            'no_warnings': False,
        }
        
        # Configurar formato específico
        if format_type == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:  # mp4
            ydl_opts['format'] = 'bv*+ba/b'
            ydl_opts['merge_output_format'] = 'mp4'
            ydl_opts['postprocessors'] = [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ]
        
        # Usar cookies se existir
        if os.path.exists(COOKIES_FILE):
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if is_playlist:
                videos = info.get('entries', [])
                titles = [v.get('title', 'Unknown') for v in videos if v]
                message = f'✅ Playlist baixada com sucesso! {len(titles)} arquivos em {format_type.upper()}.'
            else:
                title = info.get('title', 'Unknown')
                message = f'✅ "{title}" baixado em {format_type.upper()}!'
        
        return jsonify({
            'success': True,
            'message': message,
            'download_folder': DOWNLOAD_FOLDER
        })
    
    except Exception as e:
        error_msg = str(e)
        if 'Sign in to confirm' in error_msg or 'bot' in error_msg.lower():
            return jsonify({
                'success': False,
                'error': '❌ Bloqueio detectado! Você precisa fazer upload dos cookies do seu navegador. Veja as instruções acima.'
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

if __name__ == '__main__':
    print(f"\n🎬 YouTube Downloader iniciado!")
    print(f"📁 Vídeos serão salvos em: {DOWNLOAD_FOLDER}")
    print(f"🌐 Acesse: http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
