from __future__ import annotations

import os
from pathlib import Path

from yt_dlp import YoutubeDL

from media_downloader.integrations.ffmpeg_tools import discover_ffmpeg_binaries


class YtDlpClient:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.ffmpeg = discover_ffmpeg_binaries()

    def _ffmpeg_options(self) -> dict:
        options: dict = {}
        if self.ffmpeg.location:
            options["ffmpeg_location"] = self.ffmpeg.location
        return options

    def _headers_options(self) -> dict:
        """Headers que simulan navegador real para evitar bloqueos de YouTube."""
        return {
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        }

    def _youtube_options(self) -> dict:
        raw_clients = os.getenv("YOUTUBE_PLAYER_CLIENTS", "mweb,web,android,ios")
        clients = [client.strip() for client in raw_clients.split(",") if client.strip()]
        if not clients:
            clients = ["mweb", "web", "android", "ios"]
        return {
            "extractor_args": {
                "youtube": {
                    "player_client": clients,
                    "player_skip": ["js", "configs"],
                }
            }
        }

    def _base_options(self) -> dict:
        options = {
            "paths": {"home": str(self.output_dir)},
            "noplaylist": False,
            "quiet": True,
            "no_warnings": True,
            "windowsfilenames": True,
            "restrictfilenames": False,
            "socket_timeout": 30,
            "retries": {"default": 3, "http": 5},
            # Configurar runtime de JavaScript para YouTube
            "js_runtimes": {"node": {}},
        }
        options.update(self._ffmpeg_options())
        options.update(self._headers_options())
        options.update(self._youtube_options())
        return options

    def extract_info(self, url: str, download: bool = False) -> dict:
        options = self._base_options()
        options["skip_download"] = not download
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)

    def download_video(self, url: str) -> dict:
        """Descarga video con mejor formato automático (estrategia flexible)."""
        options = self._base_options()
        options.update(
            {
                "format": "bestvideo*[ext=mp4]+bestaudio[ext=m4a]/bestvideo*+bestaudio/best[ext=mp4]/best",
                "merge_output_format": "mp4",
                "outtmpl": {"default": "%(title).200B [%(id)s] [%(upload_date)s].%(ext)s"},
            }
        )
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=True)

    def download_audio(self, url: str) -> dict:
        options = self._base_options()
        options.update(
            {
                "format": "bestaudio/best",
                "outtmpl": {"default": "%(title).200B [%(id)s] [%(upload_date)s].%(ext)s"},
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }
        )
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=True)

    def list_formats(self, url: str) -> dict[str, list[dict]]:
        """Retorna los formatos disponibles separados en video y audio."""
        options = self._base_options()
        options["skip_download"] = True
        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])
                
                videos = []
                audios = []
                
                for fmt in formats:
                    fmt_id = fmt.get("format_id", "")
                    ext = fmt.get("ext", "")
                    height = fmt.get("height")
                    fps = fmt.get("fps", 30)
                    abr = fmt.get("abr")
                    
                    # Video: tiene altura pero no tiene bitrate de audio
                    if height and not abr:
                        label = f"{fmt_id}: {height}p @ {fps}fps ({ext})"
                        videos.append({"id": fmt_id, "label": label, "height": height})
                    # Audio: tiene bitrate de audio pero no altura
                    elif abr and not height:
                        label = f"{fmt_id}: {abr}kbps ({ext})"
                        audios.append({"id": fmt_id, "label": label, "bitrate": abr})
                
                # Si no encontramos video/audio separados, es un formato combinado
                if not videos or not audios:
                    return {"videos": [], "audios": [], "combined": True}
                
                return {
                    "videos": sorted(videos, key=lambda x: x.get("height", 0), reverse=True),
                    "audios": sorted(audios, key=lambda x: x.get("bitrate", 0), reverse=True),
                    "combined": False,
                }
        except Exception as e:
            # Si no puede obtener formatos, retornar que use el mejor automático
            return {"videos": [], "audios": [], "combined": True, "error": str(e)}

    def download_video_with_format(self, url: str, video_format: str, audio_format: str) -> dict:
        """Descarga video con formato específico seleccionado por el usuario."""
        options = self._base_options()
        # Intentar primero con formato específico, si falla usar fallback flexible
        format_spec = f"{video_format}+{audio_format}/bestvideo*+bestaudio/best"
        options.update(
            {
                "format": format_spec,
                "merge_output_format": "mp4",
                "outtmpl": {"default": "%(title).200B [%(id)s] [%(upload_date)s].%(ext)s"},
                "format_sort": ["vcodec:h264", "res", "acodec:aac"],
            }
        )
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=True)
