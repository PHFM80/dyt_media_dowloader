# Backend - Criterios de desarrollo

## Enfoque general
- Pensar siempre en un sistema real en producción.
- Priorizar claridad y mantenibilidad del código.
- Evitar soluciones innecesariamente complejas.

## Diseño
- Priorizar soluciones simples y entendibles.
- No anticipar problemas que no existen (evitar sobreingeniería).
- Implementar solo lo necesario para el requerimiento actual.

## Reutilización
- Reutilizar código existente antes de crear nuevo.
- Evitar duplicación de lógica.

## Organización
- Mantener funciones y módulos pequeños y enfocados.
- Separar responsabilidades claramente.

## Modelado
- Pensar primero en los datos antes que en la lógica.
- Mantener consistencia en nombres y estructuras.

## Cambios en el sistema
- Realizar cambios acotados y controlados.
- Evitar modificar múltiples partes del sistema sin necesidad.
- No romper funcionalidad existente.

## Lectura del proyecto
- Analizar el código existente antes de proponer cambios.
- Adaptarse al estilo y estructura del proyecto.

## Principios de diseño (SOLID)

- Aplicar principios SOLID cuando sea necesario.
- Mantener responsabilidad única por módulo o clase.
- Diseñar componentes abiertos a extensión, cerrados a modificación.
- Evitar dependencias directas entre módulos de alto y bajo nivel.
- Preferir abstracciones sobre implementaciones concretas.
- No aplicar SOLID si agrega complejidad innecesaria.

## Integraciones externas

* Toda integración con servicios externos debe estar encapsulada.
* No mezclar lógica de negocio con llamadas a herramientas externas.
* Cambios en una integración no deben impactar el resto del sistema.
* yt-dlp y FFmpeg deben considerarse dependencias externas aisladas.

## Gestión de descargas

* Toda descarga debe procesarse mediante una cola interna.
* Las descargas individuales y masivas deben compartir el mismo flujo de procesamiento.
* Evitar lógica específica para cada tipo de entrada cuando pueda reutilizarse una cola común.

## Escalabilidad

* Nuevas plataformas deben poder incorporarse sin modificar el núcleo del sistema.
* Cada plataforma debe implementarse como un módulo independiente.
* Evitar dependencias directas entre plataformas.

## Manejo de archivos

* Centralizar la gestión de rutas y carpetas.
* No construir rutas manualmente en múltiples lugares.
* Mantener una única fuente de verdad para la ubicación de descargas.
