# Despliegue en Streamlit Cloud

## Requisitos

* Python 3.11 o superior.
* `uv`.
* `streamlit`.
* `yt-dlp`.
* `ffmpeg` y `ffprobe`.

## Archivos importantes

* `pyproject.toml`
* `uv.lock`
* `packages.txt`

## Dependencias del sistema

El archivo `packages.txt` instala `ffmpeg` en Streamlit Cloud.
En Debian, ese paquete deja disponibles `ffmpeg` y `ffprobe`.

## Comando de arranque

```bash
streamlit run main.py
```

## Variables de entorno opcionales

* `FFMPEG_PATH`
* `FFPROBE_PATH`

## Notas

* Las descargas se guardan en `Downloads/`.
* La app crea un proyecto por sesion.
* Al recargar la pagina se genera un proyecto nuevo.

