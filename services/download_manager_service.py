#services\download_manager_service.py
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Callable, Optional

from models.project import Project
from models.download_task import DownloadTask
from services.video_downloader_service import VideoDownloaderService
from services.music_downloader_service import MusicDownloaderService
from utils.file_utils import sanitize_filename, ensure_unique_filename
from utils.logger import logger
from yt_dlp import YoutubeDL


class DownloadManagerService:
    """Servicio orquestador de descargas con soporte secuencial y paralelo."""

    def __init__(self):
        self._video_downloader = VideoDownloaderService()
        self._music_downloader = MusicDownloaderService()

    def get_video_info(self, url: str) -> dict:
        logger.debug(f"Obteniendo metadatos para: {url}")
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": False,
            "noplaylist": True,
        }
        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)
            logger.debug(f"Metadatos obtenidos exitosamente para: {info.get('title')}")
            return self._parse_formats(info)
        except Exception as e:
            logger.error(f"Error al obtener metadatos de {url}: {str(e)}")
            raise

    def _parse_formats(self, info: dict) -> dict:
        video_formats = set()
        audio_formats = set()
        for fmt in info.get("formats", []):
            if fmt.get("vcodec") != "none" and fmt.get("height"):
                video_formats.add(f"{fmt['height']}p ({fmt.get('ext', 'mp4')})")
            if fmt.get("acodec") != "none" and fmt.get("abr"):
                audio_formats.add(f"{int(fmt['abr'])} kbps ({fmt.get('ext', 'mp3')})")
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
        max_retries: int = 3,
    ) -> DownloadTask:
        task = DownloadTask(url=url, download_type=download_type, quality=quality)
        task.mark_as_downloading()
        current_quality = quality
        last_error = ""

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(
                    f"Iniciando descarga ({download_type}, {current_quality}) - Intento {attempt}/{max_retries}: {url}"
                )
                info = self.get_video_info(url)
                task.video_info = info

                ext = ".mp4" if download_type == "video" else ".mp3"
                filename = sanitize_filename(info["title"]) + ext
                output_path = project.base_path / filename
                output_path = ensure_unique_filename(output_path)

                if download_type == "video":
                    self._video_downloader.download(url, output_path, current_quality, progress_callback)
                else:
                    self._music_downloader.download(url, output_path, current_quality, progress_callback)

                task.mark_as_completed(output_path)
                project.add_download(task)
                logger.info(f"Descarga completada exitosamente: {output_path.name}")
                return task

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Intento {attempt} fallido para {url}. Error: {last_error}")
                if attempt < max_retries:
                    if download_type == "video":
                        if current_quality == "best":
                            current_quality = "1080"
                        elif current_quality == "1080":
                            current_quality = "720"
                        else:
                            current_quality = "480"
                    elif download_type == "audio":
                        if current_quality == "320":
                            current_quality = "192"
                        else:
                            current_quality = "128"
                    task.quality = current_quality
                    logger.info(f"Degradando calidad a {current_quality} para el siguiente intento.")
                    time.sleep(2)
                else:
                    logger.error(f"Descarga fallida definitivamente para {url} tras {max_retries} intentos.")
                    break

        task.mark_as_failed(f"Fallo tras {max_retries} intentos. Último error: {last_error}")
        project.add_download(task)
        return task

    def download_video(self, url: str, quality: str, project: Project, progress_callback: Optional[Callable] = None) -> DownloadTask:
        return self._download_with_retry(url, "video", quality, project, progress_callback)

    def download_audio(self, url: str, quality: str, project: Project, progress_callback: Optional[Callable] = None) -> DownloadTask:
        return self._download_with_retry(url, "audio", quality, project, progress_callback)

    def download_batch(
        self,
        urls: List[str],
        download_type: str,
        quality: str,
        project: Project,
        progress_callback: Optional[Callable] = None,
    ) -> List[DownloadTask]:
        """Descarga por lotes de forma secuencial (compatibilidad)."""
        logger.info(f"Iniciando descarga SECUENCIAL de {len(urls)} elementos.")
        tasks = [
            self._download_with_retry(url, download_type, quality, project, progress_callback)
            for url in urls
        ]
        logger.info(
            f"Proceso secuencial finalizado. Completados: {sum(1 for t in tasks if t.status == 'completed')}"
        )
        return tasks

    def download_batch_parallel(
        self,
        urls: List[str],
        download_type: str,
        quality: str,
        project: Project,
        max_workers: int = 3,
        progress_callback: Optional[Callable] = None,
    ) -> List[DownloadTask]:
        """Descarga por lotes en paralelo usando ThreadPoolExecutor.
        
        Args:
            max_workers: Número máximo de descargas concurrentes (recomendado: 2-4).
        """
        logger.info(
            f"Iniciando descarga PARALELA de {len(urls)} elementos con {max_workers} workers."
        )

        if max_workers < 1:
            raise ValueError("max_workers debe ser al menos 1")

        tasks: List[DownloadTask] = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self._download_with_retry,
                    url,
                    download_type,
                    quality,
                    project,
                    None,
                ): url
                for url in urls
            }

            for future in as_completed(futures):
                url = futures[future]
                try:
                    task = future.result()
                    tasks.append(task)
                    if progress_callback:
                        completed_count = sum(1 for t in tasks if t.status == "completed")
                        progress_callback(
                            {
                                "url": url,
                                "status": task.status,
                                "completed": completed_count,
                                "total": len(urls),
                            }
                        )
                except Exception as e:
                    logger.error(f"Error no capturado en descarga paralela de {url}: {e}")
                    failed_task = DownloadTask(url=url, download_type=download_type, quality=quality)
                    failed_task.mark_as_failed(str(e))
                    project.add_download(failed_task)
                    tasks.append(failed_task)

        completed = sum(1 for t in tasks if t.status == "completed")
        logger.info(f"Proceso paralelo finalizado. Completados: {completed}/{len(urls)}")
        return tasks