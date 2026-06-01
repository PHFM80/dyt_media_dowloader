from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse, urlunparse

from media_downloader.integrations.ytdlp_client import YtDlpClient


def is_youtube_url(url: str) -> bool:
    hostname = urlparse(url).hostname or ""
    return hostname.endswith("youtube.com") or hostname.endswith("youtu.be")


def normalize_youtube_url(url: str) -> str:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    video_id = query.get("v", [None])[0]
    if not video_id and parsed.hostname and parsed.hostname.endswith("youtu.be"):
        video_id = parsed.path.lstrip("/") or None

    if video_id:
        return urlunparse(("https", "www.youtube.com", "/watch", "", f"v={video_id}", ""))

    return url


def is_youtube_playlist_url(url: str) -> bool:
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    return parsed.path == "/playlist" and bool(query.get("list"))


@dataclass(slots=True)
class YouTubeMetadata:
    title: str
    author: str
    duration: str
    is_playlist: bool
    playlist_entries: int


class YouTubePlatform:
    def can_handle(self, url: str) -> bool:
        return is_youtube_url(url)

    def get_metadata(self, url: str, client: YtDlpClient) -> YouTubeMetadata:
        metadata_url = url if is_youtube_playlist_url(url) else normalize_youtube_url(url)
        info = client.extract_info(metadata_url, download=False)
        duration = info.get("duration")
        duration_text = f"{duration // 60}:{duration % 60:02d}" if isinstance(duration, int) else "-"
        author = info.get("uploader") or info.get("channel") or info.get("artist") or "-"
        entries = info.get("entries") or []
        return YouTubeMetadata(
            title=info.get("title") or "-",
            author=author,
            duration=duration_text,
            is_playlist=bool(info.get("_type") == "playlist" or entries),
            playlist_entries=len(entries),
        )

    def expand_playlist(self, url: str, client: YtDlpClient) -> list[str]:
        info = client.extract_info(url, download=False)
        entries = info.get("entries") or []
        urls: list[str] = []
        for entry in entries:
            entry_url = entry.get("webpage_url") or entry.get("url")
            if not entry_url and entry.get("id"):
                entry_url = f"https://www.youtube.com/watch?v={entry['id']}"
            if entry_url:
                urls.append(entry_url)
        return urls

    def download(self, url: str, mode: str, client: YtDlpClient) -> dict:
        normalized_url = normalize_youtube_url(url)
        if mode == "audio":
            return client.download_audio(normalized_url)
        return client.download_video(normalized_url)
