from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class DownloadProject:
    name: str
    slug: str
    folder: Path


@dataclass(slots=True)
class ParsedInput:
    urls: list[str]
    source_label: str


@dataclass(slots=True)
class DownloadResult:
    url: str
    title: str
    status: str
    message: str
    output_path: str | None = None

