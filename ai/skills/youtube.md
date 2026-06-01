# Skill: YouTube

## Objetivo

Gestionar todo el contenido proveniente de YouTube.

## Responsabilidades

* Validar URLs de YouTube.
* Detectar videos individuales.
* Detectar playlists.
* Obtener metadatos.
* Descargar video.
* Descargar audio.
* Gestionar descargas masivas.

## Entradas soportadas

### Video individual

Ejemplo:

https://www.youtube.com/watch?v=xxxx

### Playlist

Ejemplo:

https://www.youtube.com/playlist?list=xxxx

### Múltiples URLs

Lista de URLs proporcionadas por el usuario.

### Archivo de URLs

Archivo de texto con una URL por línea.

## Salidas soportadas

### Video

* MP4

### Audio

* MP3

## Metadatos

Intentar obtener:

* Título
* Artista
* Canal
* Duración

## Nombres de archivo

Prioridad:

1. Artista - Título
2. Canal - Título
3. Título original

Evitar caracteres inválidos para el sistema operativo.

## Playlists

* Permitir descargar playlist completa.
* Permitir descargar únicamente audio.
* Permitir descargar únicamente video.
* Mantener una cola de procesamiento para todos los elementos.

## Restricciones

* No implementar lógica de interfaz.
* No gestionar almacenamiento fuera de la carpeta de descargas.
* No realizar procesamiento multimedia fuera de FFmpeg.
