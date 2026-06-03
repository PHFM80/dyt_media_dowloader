from __future__ import annotations

import logging
import os
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProxyManager:
    """Gestor de proxies para evitar bloqueos de YouTube en Streamlit Cloud."""

    # Proxies públicos más confiables (verificados)
    # Formato: lista de (proxy, tipo) para mejor matching
    PROXY_LIST = [
        # Proxies datacenter verificados
        ("http://proxy.yundaex.com:80", "datacenter"),
        ("http://195.201.123.77:8118", "datacenter"),
        ("http://194.32.146.146:8118", "datacenter"),
        # Proxies con mejor tasa de éxito
        ("http://103.180.113.182:8080", "datacenter"),
        ("http://37.120.192.154:8080", "datacenter"),
    ]

    def __init__(self):
        self.current_proxy = None
        self.last_updated = None
        self.failed_proxies = set()
        self.proxy_timeout = 300  # Reintenta proxies cada 5 min
        self.use_proxy = True

    def get_proxy(self, force_update: bool = False) -> str | None:
        """Obtiene proxy actual o None si no hay disponible."""
        # Si hay proxy en env var, usarlo siempre
        env_proxy = os.getenv("YOUTUBE_PROXY")
        if env_proxy:
            logger.info(f"✅ Usando proxy desde env var: {env_proxy}")
            return env_proxy

        # Si está deshabilitado el uso de proxies, retornar None
        if not self.use_proxy:
            return None

        # Si tenemos proxy activo y no expiró, usarlo
        if self.current_proxy and not force_update:
            if self._is_proxy_valid(self.current_proxy):
                logger.debug(f"Usando proxy en cache: {self.current_proxy}")
                return self.current_proxy

        # Intentar obtener proxy de lista
        proxy = self._get_working_proxy()
        if proxy:
            self.current_proxy = proxy
            self.last_updated = datetime.now()
            logger.info(f"✅ Proxy obtenido: {proxy}")
            return proxy

        logger.warning("❌ No hay proxies disponibles, continuando sin proxy")
        self.use_proxy = False
        return None

    def _is_proxy_valid(self, proxy: str) -> bool:
        """Verifica si proxy sigue siendo válido."""
        if proxy in self.failed_proxies:
            return False

        if self.last_updated:
            elapsed = (datetime.now() - self.last_updated).total_seconds()
            if elapsed > self.proxy_timeout:
                return False

        return True

    def _get_working_proxy(self) -> str | None:
        """Obtiene primer proxy que funciona de la lista."""
        proxies_to_try = [p[0] for p in self.PROXY_LIST if p[0] not in self.failed_proxies]

        if not proxies_to_try:
            logger.warning("Todos los proxies fallaron, limpiando fallidos")
            self.failed_proxies.clear()
            proxies_to_try = [p[0] for p in self.PROXY_LIST]

        random.shuffle(proxies_to_try)

        for proxy in proxies_to_try[:3]:
            if self._test_proxy(proxy):
                return proxy

        logger.warning("No hay proxies funcionando en este momento")
        return None

    def _test_proxy(self, proxy: str) -> bool:
        """Testa si el proxy funciona."""
        try:
            import requests

            # Test simple y rápido
            response = requests.head(
                "http://www.google.com",
                proxies={"http": proxy, "https": proxy},
                timeout=3,
                allow_redirects=False,
            )
            
            # Aceptar cualquier respuesta que no sea un error de proxy
            if response.status_code >= 500:
                logger.debug(f"Proxy {proxy}: Error {response.status_code}")
                self.failed_proxies.add(proxy)
                return False
            
            logger.debug(f"✅ Proxy {proxy} funciona (status: {response.status_code})")
            return True
        except Exception as e:
            logger.debug(f"❌ Proxy {proxy} falló: {type(e).__name__}: {str(e)[:100]}")
            self.failed_proxies.add(proxy)
            return False

    def mark_proxy_failed(self, proxy: str | None) -> None:
        """Marca proxy como fallido."""
        if proxy:
            self.failed_proxies.add(proxy)
            logger.warning(f"Proxy marcado como fallido: {proxy}")
            if proxy == self.current_proxy:
                self.current_proxy = None
            
            # Si muchos proxies fallaron, deshabilitar temporalmente
            if len(self.failed_proxies) >= len(self.PROXY_LIST):
                logger.warning("Todos los proxies fallaron, deshabilitando proxies")
                self.use_proxy = False

