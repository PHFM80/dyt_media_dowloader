#services\playlist_service.py
import logging
from typing import List
from yt_dlp import YoutubeDL
from utils.logger import logger

class PlaylistService:
    """Servicio para extraer metadatos de playlists de YouTube"""

    def get_playlist_entries(self, url: str) -> List[dict]:
        logger.info(f"Extrayendo metadatos de playlist: {url}")
        options = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": "in_playlist",
            "noplaylist": False,
            "ignoreerrors": True,
        }

        try:
            with YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=False)

            if not info:
                logger.error(f"No se pudo obtener información de la playlist: {url}")
                raise ValueError("No se pudo obtener información de la playlist")

            entries = info.get("entries") or []
            valid_entries = [e for e in entries if e and e.get("id")]
            
            logger.info(f"Playlist procesada exitosamente. Videos válidos encontrados: {len(valid_entries)}")
            
            playlist_title = info.get("title", "Playlist sin título")
            return [
                {
                    "id": entry.get("id"),
                    "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "title": entry.get("title", "Sin título"),
                    "uploader": entry.get("uploader") or entry.get("channel", "Desconocido"),
                    "duration": entry.get("duration"),
                    "thumbnail": entry.get("thumbnail"),
                    "playlist_title": playlist_title,
                }
                for entry in valid_entries
            ]
        except Exception as e:
            logger.error(f"Error crítico al procesar playlist {url}: {str(e)}")
            raise