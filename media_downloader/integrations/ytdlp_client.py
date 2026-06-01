from __future__ import annotations

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

    def _base_options(self) -> dict:
        options = {
            "paths": {"home": str(self.output_dir)},
            "noplaylist": False,
            "quiet": True,
            "no_warnings": True,
            "windowsfilenames": True,
            "restrictfilenames": False,
        }
        options.update(self._ffmpeg_options())
        return options

    def extract_info(self, url: str, download: bool = False) -> dict:
        options = self._base_options()
        options["skip_download"] = not download
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=download)

    def download_video(self, url: str) -> dict:
        options = self._base_options()
        options.update(
            {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": {"default": "%(title).200B [%(id)s].%(ext)s"},
            }
        )
        with YoutubeDL(options) as ydl:
            return ydl.extract_info(url, download=True)

    def download_audio(self, url: str) -> dict:
        options = self._base_options()
        options.update(
            {
                "format": "bestaudio/best",
                "outtmpl": {"default": "%(title).200B [%(id)s].%(ext)s"},
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
