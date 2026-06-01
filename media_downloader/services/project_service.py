from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from media_downloader.config import DOWNLOADS_ROOT
from media_downloader.models import DownloadProject


def _slugify(text: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    normalized = re.sub(r"_+", "_", normalized).strip("._-")
    return normalized or "descarga"


def create_project(project_name: str | None) -> DownloadProject:
    base_name = _slugify(project_name or "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_name = f"{base_name}_{timestamp}"
    folder = DOWNLOADS_ROOT / folder_name
    suffix = 1
    while folder.exists():
        suffix += 1
        folder = DOWNLOADS_ROOT / f"{folder_name}_{suffix}"
    folder.mkdir(parents=True, exist_ok=False)
    return DownloadProject(name=project_name or base_name, slug=folder.name, folder=folder)


def ensure_download_root() -> Path:
    DOWNLOADS_ROOT.mkdir(parents=True, exist_ok=True)
    return DOWNLOADS_ROOT
