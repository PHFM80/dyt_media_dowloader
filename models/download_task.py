#models\download_task.py
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import threading
import uuid


@dataclass
class DownloadTask:
    """Representa una tarea de descarga individual, thread-safe."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    url: str = ""
    download_type: str = "video"
    quality: str = "best"
    status: str = "pending"
    file_path: Optional[Path] = None
    progress: float = 0.0
    error_message: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    video_info: Optional[dict] = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    def mark_as_downloading(self):
        with self._lock:
            self.status = "downloading"

    def mark_as_completed(self, file_path: Path):
        with self._lock:
            self.status = "completed"
            self.file_path = file_path
            self.progress = 100.0
            self.completed_at = datetime.now()

    def mark_as_failed(self, error: str):
        with self._lock:
            self.status = "failed"
            self.error_message = error
            self.completed_at = datetime.now()

    def update_progress(self, progress: float):
        with self._lock:
            self.progress = progress