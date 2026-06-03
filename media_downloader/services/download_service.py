from __future__ import annotations

from media_downloader.integrations.ytdlp_client import YtDlpClient
from media_downloader.models import DownloadProject, DownloadResult
from media_downloader.platforms.youtube import YouTubePlatform, is_youtube_url


class DownloadService:
    def __init__(self) -> None:
        self.youtube = YouTubePlatform()

    def _friendly_error_message(self, exc: Exception) -> str:
        message = str(exc).lower()
        if "copyright grounds" in message or "contains content from" in message:
            return "Este video tiene derechos de copyright y no se puede descargar."
        if "private video" in message:
            return "Este video es privado y no se puede descargar."
        if "requested format is not available" in message:
            return (
                "❌ El video tiene restricciones o formatos limitados que yt-dlp no puede acceder. "
                "Intenta:\n"
                "1. Ejecutar en terminal: `uv run python -m yt_dlp -U` para actualizar yt-dlp\n"
                "2. Probar otro video de YouTube\n"
                "3. Esperar - YouTube cambia sus sistemas frecuentemente"
            )
        if "video unavailable" in message:
            return "Este video no esta disponible y no se puede descargar."
        if "not available" in message:
            return "El contenido no esta disponible."
        if "http error 403" in message or "forbidden" in message:
            return (
                "YouTube bloqueó la descarga desde este entorno. "
                "En Streamlit Cloud puede requerir un cliente alternativo, un proxy o probar de nuevo mas tarde."
            )
        if "unable to extract" in message or "extractor error" in message:
            return "No se pudo extraer información del video. Puede estar limitado geográficamente o requerir autenticación."
        return str(exc)

    def _result_from_info(self, url: str, info: dict, status: str, message: str) -> DownloadResult:
        title = info.get("title") or info.get("fulltitle") or url
        return DownloadResult(url=url, title=title, status=status, message=message)

    def process_urls(
        self,
        project: DownloadProject,
        urls: list[str],
        mode: str,
        on_progress=None,
        video_format: str | None = None,
        audio_format: str | None = None,
    ) -> list[DownloadResult]:
        results: list[DownloadResult] = []
        client = YtDlpClient(project.folder)
        for index, url in enumerate(urls, start=1):
            if on_progress:
                on_progress(index, len(urls), url)

            if not is_youtube_url(url):
                results.append(
                    DownloadResult(
                        url=url,
                        title=url,
                        status="error",
                        message="URL no soportada por ahora. Solo YouTube esta habilitado en esta primera etapa.",
                    )
                )
                continue

            try:
                metadata = self.youtube.get_metadata(url, client)
                if metadata.is_playlist:
                    playlist_urls = self.youtube.expand_playlist(url, client)
                    if not playlist_urls:
                        results.append(
                            DownloadResult(
                                url=url,
                                title=metadata.title,
                                status="error",
                                message="No se encontraron elementos en la playlist.",
                            )
                        )
                        continue

                    for playlist_url in playlist_urls:
                        try:
                            info = self.youtube.download(playlist_url, mode, client, video_format, audio_format)
                            results.append(
                                self._result_from_info(
                                    playlist_url,
                                    info,
                                    "completed",
                                    f"Descarga completada en {project.folder}",
                                )
                            )
                        except Exception as item_exc:  # noqa: BLE001
                            results.append(
                                DownloadResult(
                                    url=playlist_url,
                                    title=playlist_url,
                                    status="error",
                                    message=self._friendly_error_message(item_exc),
                                )
                            )
                    continue

                try:
                    info = self.youtube.download(url, mode, client, video_format, audio_format)
                    results.append(
                        DownloadResult(
                            url=url,
                            title=metadata.title,
                            status="completed",
                            message=f"Descarga completada en {project.folder}",
                            output_path=info.get("_filename") if isinstance(info, dict) else None,
                        )
                    )
                except Exception as exc:  # noqa: BLE001
                    results.append(
                        DownloadResult(
                            url=url,
                            title=metadata.title,
                            status="error",
                            message=self._friendly_error_message(exc),
                        )
                    )
            except Exception as exc:  # noqa: BLE001
                results.append(
                    DownloadResult(
                        url=url,
                        title=url,
                        status="error",
                        message=self._friendly_error_message(exc),
                    )
                )
        return results
