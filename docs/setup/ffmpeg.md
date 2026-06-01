# FFmpeg y FFprobe

## Objetivo

La aplicacion requiere `ffmpeg` y `ffprobe` para:

* fusionar video y audio al descargar video.
* convertir audio a `mp3`.

## Streamlit Community Cloud

Para que este software este disponible en el servidor, el proyecto incluye un archivo `packages.txt` en la raiz.

Contenido:

```text
ffmpeg
```

En Debian, el paquete `ffmpeg` instala tanto `ffmpeg` como `ffprobe`.

## Resolucion de binarios

La app busca los binarios en este orden:

1. Variables de entorno `FFMPEG_PATH` y `FFPROBE_PATH`.
2. Binarios disponibles en `PATH`.

## Notas de despliegue

* Mantener `packages.txt` en la raiz del repo.
* No subir binarios pesados al repositorio.
* Confirmar que el entorno de despliegue use Linux compatible con `apt`.

