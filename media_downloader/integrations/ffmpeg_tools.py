from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class FfmpegBinaries:
    ffmpeg: str | None
    ffprobe: str | None

    @property
    def location(self) -> str | None:
        if self.ffmpeg:
            return str(Path(self.ffmpeg).parent)
        if self.ffprobe:
            return str(Path(self.ffprobe).parent)
        return None


def _env_path(name: str) -> str | None:
    value = os.getenv(name)
    return value or None


def _windows_winget_links_path(binary_name: str) -> str | None:
    links_dir = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links"
    candidate = links_dir / binary_name
    if candidate.exists():
        return str(candidate)
    return None


def _windows_winget_package_paths(binary_name: str) -> str | None:
    packages_dir = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Packages"
    if not packages_dir.exists():
        return None

    for candidate in packages_dir.rglob(binary_name):
        if candidate.is_file():
            return str(candidate)
    return None


def _discover_binary(name: str, env_var: str) -> str | None:
    return (
        _env_path(env_var)
        or shutil.which(name)
        or _windows_winget_links_path(f"{name}.exe")
        or _windows_winget_package_paths(f"{name}.exe")
    )


def discover_ffmpeg_binaries() -> FfmpegBinaries:
    ffmpeg = _discover_binary("ffmpeg", "FFMPEG_PATH")
    ffprobe = _discover_binary("ffprobe", "FFPROBE_PATH")

    return FfmpegBinaries(ffmpeg=ffmpeg, ffprobe=ffprobe)


def ffmpeg_is_available() -> bool:
    binaries = discover_ffmpeg_binaries()
    return bool(binaries.ffmpeg and binaries.ffprobe)


def ffmpeg_status_message() -> str:
    binaries = discover_ffmpeg_binaries()
    if binaries.ffmpeg and binaries.ffprobe:
        return "ffmpeg y ffprobe disponibles"
    if binaries.ffmpeg and not binaries.ffprobe:
        return "ffmpeg disponible pero ffprobe falta"
    if not binaries.ffmpeg and binaries.ffprobe:
        return "ffprobe disponible pero ffmpeg falta"
    return "ffmpeg y ffprobe no estan disponibles"
