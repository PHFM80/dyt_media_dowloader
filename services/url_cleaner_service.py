#services\url_cleaner_service.py
import re
from typing import List
from urllib.parse import urlparse


class URLCleanerService:
    """Servicio para limpiar y validar URLs"""

    @staticmethod
    def clean_url(url: str) -> str:
        """Limpia una URL individual"""
        url = url.strip()
        url = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', url)
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url

    @staticmethod
    def clean_urls(urls: List[str]) -> List[str]:
        """Limpia una lista de URLs"""
        cleaned = []
        for url in urls:
            cleaned_url = URLCleanerService.clean_url(url)
            if cleaned_url:
                cleaned.append(cleaned_url)
        return cleaned

    @staticmethod
    def validate_url(url: str) -> bool:
        """Valida si una URL es válida"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def extract_urls_from_text(text: str) -> List[str]:
        """Extrae URLs de un texto"""
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        urls = re.findall(url_pattern, text)
        return URLCleanerService.clean_urls(urls)

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Verifica si una URL es de YouTube"""
        try:
            parsed = urlparse(url)
            return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc
        except Exception:
            return False