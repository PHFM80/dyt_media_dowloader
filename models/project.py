#models\project.py
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


@dataclass
class Project:
    """Representa un proyecto de descarga"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    downloads: list = field(default_factory=list)
    base_path: Optional[Path] = None
    is_single_session: bool = False
    
    def __post_init__(self):
        """Inicializa el proyecto"""
        if not self.name:
            self.name = f"Proyecto_{self.created_at.strftime('%Y%m%d_%H%M%S')}"
    
    def add_download(self, download_task):
        """Agrega una tarea de descarga al proyecto"""
        self.downloads.append(download_task)
    
    def get_download_path(self) -> Path:
        """Obtiene la ruta de descarga del proyecto"""
        if self.base_path:
            return self.base_path
        return Path.cwd()
    
    def clear_downloads(self):
        """Limpia la lista de descargas"""
        self.downloads.clear()