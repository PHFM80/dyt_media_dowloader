#models\download_task.py
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


@dataclass
class DownloadTask:
    """Representa una tarea de descarga individual"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    download_type: str = "video"  # 'video' | 'audio'
    quality: str = "best"
    status: str = "pending"  # 'pending' | 'downloading' | 'completed' | 'failed'
    file_path: Optional[Path] = None
    progress: float = 0.0
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    video_info: Optional[dict] = None
    
    def mark_as_downloading(self):
        """Marca la tarea como en progreso"""
        self.status = "downloading"
    
    def mark_as_completed(self, file_path: Path):
        """Marca la tarea como completada"""
        self.status = "completed"
        self.file_path = file_path
        self.progress = 100.0
        self.completed_at = datetime.now()
    
    def mark_as_failed(self, error: str):
        """Marca la tarea como fallida"""
        self.status = "failed"
        self.error_message = error
        self.completed_at = datetime.now()
    
    def update_progress(self, progress: float):
        """Actualiza el progreso de la descarga"""
        self.progress = progress