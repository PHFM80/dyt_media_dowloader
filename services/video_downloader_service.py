#services\video_downloader_service.py
from pathlib import Path
from typing import Optional, Callable

from yt_dlp import YoutubeDL


class VideoDownloaderService:
    def download(
        self,
        url: str,
        output_path: Path,
        quality: str = "best",
        progress_callback: Optional[Callable] = None
    ) -> Path:
        """Descarga video con calidad y ruta especificadas"""
        
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

        format_selector = {
            "best": "bestvideo+bestaudio/best",
            "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480": "bestvideo[height<=480]+bestaudio/best[height<=480]",
        }

        options = {
            "format": format_selector.get(quality, "bestvideo+bestaudio/best"),
            "merge_output_format": "mp4",
            "outtmpl": str(output_path),
            "noplaylist": True,
            "progress_hooks": [progress_hook] if progress_callback else [],
        }

        with YoutubeDL(options) as ydl:
            ydl.download([url])

        return output_path