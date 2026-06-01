# Proyecto

## Descripción

Aplicación desarrollada en Python para descargar contenido multimedia desde distintas plataformas online. El sistema está diseñado con una arquitectura modular basada en skills, permitiendo incorporar nuevas plataformas y funcionalidades de forma sencilla.

La plataforma principal es YouTube, aunque la arquitectura debe permitir futuras integraciones con otros servicios como Spotify, TikTok, Instagram, Vimeo y similares.

---

## Objetivo

Proporcionar una herramienta simple y eficiente para descargar videos, audios y listas de reproducción desde múltiples plataformas, ofreciendo una experiencia unificada para el usuario y una arquitectura extensible para futuras mejoras.

---

## Tipo de sistema

Aplicación local desarrollada en Python con interfaz gráfica basada en Streamlit.

El sistema funcionará inicialmente como una aplicación monousuario, sin autenticación ni gestión de cuentas, almacenando los archivos descargados en el equipo local del usuario.

---

## Usuarios del sistema

### Usuario final

Persona que desea descargar contenido multimedia desde plataformas compatibles.

### Desarrollador

Responsable del mantenimiento, evolución y ampliación de funcionalidades mediante la incorporación de nuevas skills e integraciones.

---

## Funcionalidades principales

### YouTube

* Descargar videos individuales.
* Descargar audios individuales.
* Descargar listas de reproducción completas.
* Descargar únicamente los videos de una lista.
* Descargar únicamente los audios de una lista.
* Seleccionar calidad de descarga cuando esté disponible.
* Obtener información básica del contenido antes de la descarga.
* Renombrar automáticamente los archivos descargados utilizando metadatos disponibles.

### Gestión de archivos

* Organización automática de descargas.
* Separación de contenido de audio y video en carpetas independientes.
* Configuración de rutas de descarga.

### Arquitectura extensible

* Incorporación de nuevas plataformas mediante módulos independientes.
* Detección automática de la plataforma a partir de la URL ingresada.
* Separación entre lógica de interfaz, lógica de negocio e integraciones externas.

---

## Integraciones externas

### Descarga de contenido

* yt-dlp

### Procesamiento multimedia

* FFmpeg

### Plataformas previstas

* YouTube
* Spotify (importación de playlists y metadatos)
* TikTok
* Instagram
* Vimeo
* Otras plataformas compatibles con yt-dlp

---

## Estado del proyecto

En desarrollo.
