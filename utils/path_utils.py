#utils\path_utils.py
from pathlib import Path
import shutil


def get_downloads_dir() -> Path:
    """Obtiene el directorio de descargas del sistema"""
    from config.settings import get_settings
    return get_settings().downloads_dir


def get_temp_dir() -> Path:
    """Obtiene el directorio temporal"""
    from config.settings import get_settings
    return get_settings().temp_dir


def create_project_dir(project_name: str, base_path: Path = None) -> Path:
    """Crea el directorio para un proyecto"""
    if base_path is None:
        base_path = get_downloads_dir()
    
    project_path = base_path / project_name
    project_path.mkdir(parents=True, exist_ok=True)
    return project_path


def cleanup_temp_files(temp_dir: Path = None):
    """Limpia archivos temporales"""
    if temp_dir is None:
        temp_dir = get_temp_dir()
    
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)


def ensure_directory_exists(path: Path):
    """Asegura que un directorio exista"""
    path.mkdir(parents=True, exist_ok=True)