from __future__ import annotations

import logging
import os
import random
from datetime import datetime, timedelta

import requests

logger = logging.getLogger(__name__)


class ProxyManager:
    """Gestor de proxies para evitar bloqueos de YouTube en Streamlit Cloud."""

    # Lista de proxies públicos gratuitos (fallback)
    FREE_PROXIES = [
        "http://proxy.yundaex.com:80",
        "http://43.226.231.159:8080",
        "http://103.59.176.154:8080",
        "http://195.201.123.77:8118",
        "http://194.32.146.146:8118",
    ]

    def __init__(self):
        self.current_proxy = None
        self.last_updated = None
        self.failed_proxies = set()
        self.proxy_timeout = 300  # Reintenta proxies cada 5 min

    def get_proxy(self, force_update: bool = False) -> str | None:
        """Obtiene proxy actual o None si no hay disponible."""
        # Si hay proxy en env var, usarlo
        env_proxy = os.getenv("YOUTUBE_PROXY")
        if env_proxy:
            logger.info(f"Usando proxy desde env: {env_proxy}")
            return env_proxy

        # Si tenemos proxy activo y no expiró, usarlo
        if self.current_proxy and not force_update:
            if self._is_proxy_valid(self.current_proxy):
                return self.current_proxy

        # Intentar obtener proxy de lista libre
        self.current_proxy = self._get_free_proxy()
        self.last_updated = datetime.now()
        return self.current_proxy

    def _is_proxy_valid(self, proxy: str) -> bool:
        """Verifica si proxy sigue siendo válido."""
        if proxy in self.failed_proxies:
            return False

        if self.last_updated:
            elapsed = (datetime.now() - self.last_updated).total_seconds()
            if elapsed > self.proxy_timeout:
                return False

        return True

    def _get_free_proxy(self) -> str | None:
        """Obtiene proxy gratuito de lista pública."""
        proxies_to_try = [p for p in self.FREE_PROXIES if p not in self.failed_proxies]

        if not proxies_to_try:
            logger.warning("Todos los proxies libres fallaron, limpiando fallidos")
            self.failed_proxies.clear()
            proxies_to_try = self.FREE_PROXIES

        random.shuffle(proxies_to_try)

        for proxy in proxies_to_try[:3]:
            try:
                # Test rápido del proxy
                response = requests.head("http://www.google.com", proxies={"http": proxy}, timeout=5)
                if response.status_code < 500:
                    logger.info(f"Proxy válido: {proxy}")
                    return proxy
            except Exception as e:
                logger.debug(f"Proxy inválido {proxy}: {e}")
                self.failed_proxies.add(proxy)
                continue

        logger.warning("No hay proxies gratuitos disponibles en este momento")
        return None

    def mark_proxy_failed(self, proxy: str | None) -> None:
        """Marca proxy como fallido."""
        if proxy:
            self.failed_proxies.add(proxy)
            if proxy == self.current_proxy:
                self.current_proxy = None
