import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Configuración
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB por archivo
BACKUP_COUNT = 3             # Mantener 3 archivos de respaldo

# Asegurar que el directorio de logs exista
LOG_DIR.mkdir(exist_ok=True)

# Crear logger
logger = logging.getLogger("DescargarYouTube")
logger.setLevel(logging.DEBUG)

# Evitar duplicación de handlers si el módulo se importa múltiples veces
if not logger.handlers:
    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)s.%(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para archivo (Rotativo)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)