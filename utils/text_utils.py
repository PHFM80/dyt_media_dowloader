#utils\text_utils.py
import re

def clean_error_message(error: str) -> str:
    """Limpia códigos ANSI y traduce errores comunes de yt-dlp a mensajes amigables"""
    # Eliminar códigos de color ANSI
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_msg = ansi_escape.sub('', error)
    
    # Traducir errores comunes
    clean_msg = clean_msg.lower()
    if "sign in to confirm your age" in clean_msg:
        return "Restricción de edad (requiere configuración de cookies)"
    elif "video unavailable" in clean_msg or "copyright" in clean_msg:
        return "Video no disponible o eliminado por derechos de autor"
    elif "private video" in clean_msg:
        return "El video es privado"
    
    # Si no es un error conocido, devolver la primera línea limpia
    return clean_msg.split('\n')[0].strip().capitalize()