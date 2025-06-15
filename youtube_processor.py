import yt_dlp
import os
from analyzer import run_fake_analysis

def download_youtube_video(url, download_dir='uploads'):
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'),
        'format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        if not filename.endswith('.mp4'):
            base = os.path.splitext(filename)[0]
            filename = base + '.mp4'
        return filename

def analyze_youtube_url(url):
    filepath = download_youtube_video(url)
    filename = os.path.basename(filepath)
    return run_fake_analysis(filename)
