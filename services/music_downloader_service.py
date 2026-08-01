#services\music_downloader_service.py
from pathlib import Path
from typing import Optional, Callable

from yt_dlp import YoutubeDL


class MusicDownloaderService:
    def download(
        self,
        url: str,
        output_path: Path,
        quality: str = "320",
        progress_callback: Optional[Callable] = None
    ) -> Path:
        """Descarga audio en MP3 con calidad especificada"""
        
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                progress_callback({
                    'status': 'downloading',
                    'percent': d.get('_percent_str', '0%'),
                    'speed': d.get('_speed_str', 'N/A'),
                    'eta': d.get('_eta_str', 'N/A')
                })
            elif progress_callback and d['status'] == 'finished':
                progress_callback({
                    'status': 'finished',
                    'percent': '100%'
                })

        options = {
            "format": "bestaudio/best",
            "outtmpl": str(output_path.with_suffix('.%(ext)s')),
            "noplaylist": True,
            "progress_hooks": [progress_hook] if progress_callback else [],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": quality,
                }
            ],
        }

        with YoutubeDL(options) as ydl:
            ydl.download([url])

        return output_path.with_suffix('.mp3')