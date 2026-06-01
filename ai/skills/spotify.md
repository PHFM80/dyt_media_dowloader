# Skill: Spotify

## Objetivo

Importar información de playlists y canciones de Spotify para integrarlas al flujo de descargas del sistema.

## Responsabilidades

* Validar URLs de Spotify.
* Obtener información de playlists.
* Obtener información de canciones.
* Transformar playlists en una cola de procesamiento.

## Entradas soportadas

### Playlist

Ejemplo:

https://open.spotify.com/playlist/xxxx

### Canción individual

Ejemplo:

https://open.spotify.com/track/xxxx

## Información a obtener

* Nombre de la canción.
* Artista.
* Álbum.
* Duración.
* Nombre de playlist.

## Flujo esperado

1. Obtener canciones de Spotify.
2. Generar cola interna.
3. Entregar la cola al sistema de descargas.

## Restricciones

* No descargar contenido desde Spotify.
* No almacenar credenciales dentro del código.
* No implementar lógica de descarga multimedia.

## Futuras mejoras

* Exportación de playlists.
* Sincronización de listas.
* Importación masiva de playlists.
