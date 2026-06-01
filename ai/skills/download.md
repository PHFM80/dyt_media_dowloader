# Skill: Gestión de Descargas

## Objetivo

Centralizar la organización y procesamiento de todas las descargas del sistema.

## Responsabilidades

* Crear carpetas de descarga.
* Gestionar colas de procesamiento.
* Organizar archivos descargados.
* Registrar resultados de las descargas.

## Estructura de carpetas

Todas las descargas deben almacenarse dentro de:

downloads/

Cada operación genera una carpeta independiente:

downloads/descarga_YYYYMMDD_HHMMSS

Ejemplo:

downloads/descarga_20260601_154530

## Cola de procesamiento

Toda entrada debe convertirse a una cola común.

Fuentes válidas:

* URL individual
* Múltiples URLs
* Archivo TXT
* Playlist

## Procesamiento

Los elementos deben procesarse secuencialmente.

Estados posibles:

* Pendiente
* Procesando
* Completado
* Error

## Organización de archivos

Mantener todos los archivos de una misma operación dentro de la carpeta generada.

## Restricciones

* No mezclar lógica de plataforma.
* No realizar descargas directamente.
* Solo coordinar el flujo de procesamiento.
