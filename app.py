from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import glob
from pathlib import Path

app = Flask(__name__)

DOWNLOAD_FOLDER = str(Path.home() / 'Downloads' / 'youtube-videos')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    try:
        data = request.json
        url = data.get('url')
        format_type = data.get('format', 'mp4')
        is_playlist = data.get('is_playlist', False)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL não fornecida'}), 400
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'noplaylist': not is_playlist,
            'progress_hooks': [],
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            # Opções para evitar detecção de bot
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android_creator'],
                    'skip': ['hls', 'dash'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            },
            'nocheckcertificate': True,
            'age_limit': None,
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if is_playlist:
                videos = info.get('entries', [])
                titles = [v.get('title', 'Unknown') for v in videos if v]
                message = f'✅ Playlist baixada com sucesso! {len(titles)} vídeos baixados.'
            else:
                title = info.get('title', 'Unknown')
                message = f'✅ Vídeo "{title}" baixado com sucesso!'
        
        return jsonify({
            'success': True,
            'message': message,
            'download_folder': DOWNLOAD_FOLDER
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao baixar: {str(e)}'
        }), 500

@app.route('/list-downloads')
def list_downloads():
    try:
        files = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*.mp4'))
        files.sort(key=os.path.getmtime, reverse=True)
        
        file_list = []
        for f in files[:20]:  # Últimos 20 arquivos
            file_list.append({
                'name': os.path.basename(f),
                'size': f"{os.path.getsize(f) / (1024*1024):.1f} MB",
                'path': f
            })
        
        return jsonify({
            'success': True,
            'files': file_list,
            'folder': DOWNLOAD_FOLDER
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print(f"\n🎬 YouTube Downloader iniciado!")
    print(f"📁 Vídeos serão salvos em: {DOWNLOAD_FOLDER}")
    print(f"🌐 Acesse: http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
