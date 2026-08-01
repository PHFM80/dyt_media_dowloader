#config\settings.py
from pathlib import Path
from dataclasses import dataclass
import os


@dataclass
class Settings:
    """Configuración global de la aplicación"""
    
    # Directorio base de descargas
    downloads_dir: Path
    
    # Directorio temporal
    temp_dir: Path
    
    # Calidades por defecto
    default_video_quality: str = "best"
    default_audio_quality: str = "320"
    
    # Nombre de la aplicación
    app_name: str = "DescargarYouTube"
    
    def __post_init__(self):
        """Inicializa directorios después de la creación"""
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """Obtiene la configuración de la aplicación"""
    # Usa la carpeta Descargas del usuario
    user_downloads = Path(os.path.expanduser("~")) / "Downloads"
    app_downloads = user_downloads / "DescargarYouTube"
    
    return Settings(
        downloads_dir=app_downloads,
        temp_dir=app_downloads / "temp"
    )