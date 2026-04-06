from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import glob
import json
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
        is_playlist = data.get('is_playlist', False)
        
        if not url:
            return jsonify({'success': False, 'error': 'URL não fornecida'}), 400
        
        # Usar yt-dlp via subprocess para evitar problemas de detecção
        cmd = [
            'yt-dlp',
            '--format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            '--merge-output-format', 'mp4',
            '--output', os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            '--extractor-args', 'youtube:player_client=android_creator',
            '--no-check-certificates',
        ]
        
        if not is_playlist:
            cmd.append('--no-playlist')
        
        cmd.append(url)
        
        # Executar comando
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minutos de timeout
        )
        
        if result.returncode == 0:
            if is_playlist:
                message = '✅ Playlist baixada com sucesso!'
            else:
                message = '✅ Vídeo baixado com sucesso!'
            
            return jsonify({
                'success': True,
                'message': message,
                'download_folder': DOWNLOAD_FOLDER
            })
        else:
            error_msg = result.stderr if result.stderr else result.stdout
            return jsonify({
                'success': False,
                'error': f'Erro ao baixar: {error_msg}'
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Download demorou muito tempo (timeout de 10 minutos)'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro: {str(e)}'
        }), 500

@app.route('/list-downloads')
def list_downloads():
    try:
        files = glob.glob(os.path.join(DOWNLOAD_FOLDER, '*.mp4'))
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
            'folder': DOWNLOAD_FOLDER
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print(f"\n🎬 YouTube Downloader V2 iniciado!")
    print(f"📁 Vídeos serão salvos em: {DOWNLOAD_FOLDER}")
    print(f"🌐 Acesse: http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
