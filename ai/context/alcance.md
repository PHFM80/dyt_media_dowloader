# Alcance del Sistema

## Incluye

### Descarga de contenido multimedia

* Descarga de videos individuales.
* Descarga de audios individuales.
* Descarga de listas de reproducción completas.
* Descarga selectiva de audio o video.
* Descarga desde plataformas compatibles.

### Plataforma principal

* Soporte completo para YouTube en la primera versión.

### Gestión de archivos

* Organización automática de descargas.
* Separación de audios y videos en carpetas independientes.
* Configuración de directorios de descarga.
* Renombrado automático utilizando metadatos disponibles.

### Información del contenido

* Obtención de título.
* Obtención de autor o canal.
* Obtención de duración.
* Visualización de información previa a la descarga.

### Arquitectura

* Sistema modular basado en skills.
* Separación entre interfaz, lógica de negocio e integraciones externas.
* Capacidad de agregar nuevas plataformas sin modificar la arquitectura principal.

### Futuras integraciones

La arquitectura deberá permitir incorporar:

* Spotify.
* TikTok.
* Instagram.
* Vimeo.
* Otras plataformas compatibles con yt-dlp.

---

## No incluye

### Gestión de usuarios

* Registro de usuarios.
* Inicio de sesión.
* Recuperación de contraseñas.
* Roles y permisos.

### Servicios en la nube

* Almacenamiento remoto.
* Sincronización entre dispositivos.
* Infraestructura cloud.

### Base de datos

* No se utilizará base de datos en la primera versión.
* La configuración se almacenará mediante archivos locales cuando sea necesario.

### Automatizaciones avanzadas

* Programación de descargas.
* Descargas automáticas periódicas.
* Monitoreo de canales.
* Notificaciones automáticas.

### Funcionalidades sociales

* Compartir contenido.
* Comentarios.
* Comunidad de usuarios.

### Monetización

* Pagos.
* Suscripciones.
* Licencias.

---

### Gestión de descargas

* Descarga individual mediante URL.
* Descarga masiva mediante múltiples URLs.
* Importación de listas de URLs desde archivo de texto.
* Procesamiento secuencial de una cola de descargas.
* Visualización del progreso de la cola.

### Organización de archivos

* Todas las descargas se almacenarán dentro del directorio `downloads`.
* Cada operación de descarga generará una carpeta independiente.
* El nombre de la carpeta seguirá el formato:

  `descarga_YYYYMMDD_HHMMSS`

Ejemplo:

`downloads/descarga_20260601_154530`

* Todos los archivos generados durante una misma operación se almacenarán dentro de la carpeta correspondiente.


## Decisiones clave

* Python será el lenguaje principal del proyecto.
* Streamlit será la interfaz gráfica inicial.
* yt-dlp será la herramienta principal para la descarga de contenido.
* FFmpeg será utilizado para procesamiento y conversión multimedia.
* El sistema será inicialmente local y monousuario.
* No se utilizará base de datos en la primera versión.
* La plataforma principal será YouTube.
* Las demás plataformas serán incorporadas mediante skills independientes.
* La arquitectura deberá ser extensible y preparada para futuras integraciones.
* Toda nueva funcionalidad deberá respetar la estructura modular definida por el proyecto.
* El sistema deberá soportar descargas individuales y descargas masivas.
* El sistema deberá procesar las descargas mediante una cola interna.
* Cada ejecución de descarga generará una carpeta independiente para facilitar la organización de archivos.
