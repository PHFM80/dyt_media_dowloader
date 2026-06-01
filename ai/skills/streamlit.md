# Skill: Streamlit UI

## Objetivo

Proporcionar una interfaz simple y clara para interactuar con las funcionalidades del sistema.

## Responsabilidades

* Capturar entradas del usuario.
* Mostrar información de los contenidos detectados.
* Mostrar progreso de descargas.
* Mostrar resultados y errores.
* Permitir configurar opciones de descarga.

## Entradas soportadas

### URL individual

Una única URL de una plataforma soportada.

### Múltiples URLs

Lista de URLs pegadas manualmente.

### Archivo TXT

Archivo con una URL por línea.

## Opciones de descarga

* Descargar audio.
* Descargar video.
* Descargar audio y video.
* Seleccionar calidad cuando esté disponible.

## Información mostrada

Cuando sea posible mostrar:

* Título.
* Canal o autor.
* Duración.
* Tipo de contenido.
* Cantidad de elementos en la cola.

## Restricciones

* No implementar lógica de negocio.
* No ejecutar descargas directamente.
* No contener lógica específica de plataformas.
* Utilizar servicios del sistema para todas las operaciones.

## Principios

* Interfaz simple.
* Pocos pasos para iniciar una descarga.
* Priorizar facilidad de uso.
* Mostrar errores de forma clara.
