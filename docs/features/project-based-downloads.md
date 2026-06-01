# Proyecto de descarga

## Comportamiento

* `downloads/` es la carpeta raiz del sistema.
* Cada ejecucion activa crea un proyecto de descarga propio.
* El proyecto agrupa todas las URLs cargadas antes de iniciar una nueva sesion.
* Al recargar la pagina se crea un proyecto nuevo en memoria.

## Entradas soportadas

* URLs pegadas manualmente.
* Archivo `.txt` con una URL por linea.
* Archivo `.docx` con URLs embebidas en el texto.

## Salida

* Todo el contenido descargado se guarda dentro de la carpeta del proyecto activo.
* El nombre del proyecto se usa como base del nombre de la carpeta generada.

