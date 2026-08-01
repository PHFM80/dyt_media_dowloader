#services\download_manager_service.py
import time
from pathlib import Path
from typing import List, Callable, Optional
from models.project import Project
from models.download_task import DownloadTask
from services.video_downloader_service import VideoDownloaderService
from services.music_downloader_service import MusicDownloaderService
from utils.file_utils import sanitize_filename, ensure_unique_filename
from yt_dlp import YoutubeDL


class DownloadManagerService:
    """Servicio orquestador de descargas con reintentos inteligentes"""
    
    def __init__(self):
        self._video_downloader = VideoDownloaderService()
        self._music_downloader = MusicDownloaderService()
    
    def get_video_info(self, url: str) -> dict:
        """Obtiene metadatos del video sin descargar"""
        options = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
        }
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        video_formats = set()
        audio_formats = set()

        for fmt in info.get("formats", []):
            if fmt.get("vcodec") != "none":
                height = fmt.get("height")
                ext = fmt.get("ext")
                if height:
                    video_formats.add(f"{height}p ({ext})")
            if fmt.get("acodec") != "none":
                abr = fmt.get("abr")
                ext = fmt.get("ext")
                if abr:
                    audio_formats.add(f"{int(abr)} kbps ({ext})")

        return {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "categories": info.get("categories"),
            "thumbnail": info.get("thumbnail"),
            "video_formats": sorted(video_formats, key=lambda x: int(x.split("p")[0])),
            "audio_formats": sorted(audio_formats, key=lambda x: int(x.split()[0])),
        }

    def _download_with_retry(
        self,
        url: str,
        download_type: str,
        quality: str,
        project: Project,
        progress_callback: Optional[Callable] = None,
        max_retries: int = 3
    ) -> DownloadTask:
        """Maneja la descarga con reintentos y degradación de calidad ante fallos"""
        task = DownloadTask(url=url, download_type=download_type, quality=quality)
        task.mark_as_downloading()
        
        current_quality = quality
        last_error = None
        
        for attempt in range(1, max_retries + 1):
            try:
                info = self.get_video_info(url)
                task.video_info = info
                
                ext = ".mp4" if download_type == "video" else ".mp3"
                filename = sanitize_filename(info['title']) + ext
                output_path = project.base_path / filename
                output_path = ensure_unique_filename(output_path)
                
                if download_type == "video":
                    self._video_downloader.download(url, output_path, current_quality, progress_callback)
                else:
                    self._music_downloader.download(url, output_path, current_quality, progress_callback)
                
                task.mark_as_completed(output_path)
                project.add_download(task)
                return task
                
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    # Degradación de calidad para el siguiente intento
                    if download_type == "video":
                        if current_quality == "best": current_quality = "1080"
                        elif current_quality == "1080": current_quality = "720"
                        else: current_quality = "480"
                    elif download_type == "audio":
                        if current_quality == "320": current_quality = "192"
                        else: current_quality = "128"
                    
                    task.quality = current_quality
                    time.sleep(2) # Pausa breve antes de reintentar
                else:
                    break
                    
        task.mark_as_failed(f"Fallo tras {max_retries} intentos. Último error: {last_error}")
        project.add_download(task)
        return task

    def download_video(self, url: str, quality: str, project: Project, progress_callback: Optional[Callable] = None) -> DownloadTask:
        return self._download_with_retry(url, "video", quality, project, progress_callback)

    def download_audio(self, url: str, quality: str, project: Project, progress_callback: Optional[Callable] = None) -> DownloadTask:
        return self._download_with_retry(url, "audio", quality, project, progress_callback)

    def download_batch(self, urls: List[str], download_type: str, quality: str, project: Project, progress_callback: Optional[Callable] = None) -> List[DownloadTask]:
        tasks = []
        for url in urls:
            task = self._download_with_retry(url, download_type, quality, project, progress_callback)
            tasks.append(task)
        return tasks