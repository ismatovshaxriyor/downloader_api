import yt_dlp
import os
from pathlib import Path
from django.conf import settings

def download_video(url: str, platform: str = "youtube") -> str:
    """Video yuklab olish"""
    output_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    if platform.lower() == "instagram":
        ydl_opts['format'] = 'best'
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    elif platform.lower() == "youtube":
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
        ydl_opts['merge_output_format'] = 'mp4'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

        # Relative path for MEDIA_URL
        relative_path = os.path.relpath(filename, settings.MEDIA_ROOT)
        return relative_path

def download_audio(url: str, platform: str = "youtube") -> str:
    """Audio yuklab olish"""
    output_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    if platform.lower() == "instagram":
        ydl_opts['http_headers'] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        base_filename = ydl.prepare_filename(info)
        audio_path = os.path.splitext(base_filename)[0] + '.mp3'

        relative_path = os.path.relpath(audio_path, settings.MEDIA_ROOT)
        return relative_path