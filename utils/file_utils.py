#utils\file_utils.py
from pathlib import Path
import re


def sanitize_filename(filename: str) -> str:
    """Limpia un nombre de archivo de caracteres inválidos"""
    # Elimina caracteres no permitidos en nombres de archivo
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Reemplaza espacios múltiples con uno solo
    filename = re.sub(r'\s+', ' ', filename)
    
    # Limita la longitud
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename.strip()


def ensure_unique_filename(file_path: Path) -> Path:
    """Asegura que el nombre del archivo sea único agregando sufijos numéricos"""
    if not file_path.exists():
        return file_path
    
    base = file_path.stem
    suffix = file_path.suffix
    directory = file_path.parent
    
    counter = 1
    while True:
        new_filename = f"{base}_{counter}{suffix}"
        new_path = directory / new_filename
        if not new_path.exists():
            return new_path
        counter += 1


def get_file_size_mb(file_path: Path) -> float:
    """Obtiene el tamaño del archivo en MB"""
    if file_path.exists():
        return file_path.stat().st_size / (1024 * 1024)
    return 0.0