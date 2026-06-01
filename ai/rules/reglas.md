# Reglas de comportamiento

## Generación de código

* Generar código únicamente cuando sea necesario para resolver el problema solicitado.
* Evitar soluciones monolíticas o excesivamente grandes.
* Priorizar cambios pequeños, claros y acotados.
* Antes de implementar, describir brevemente qué se va a hacer.
* Mantener funciones y clases con una única responsabilidad.
* Evitar código duplicado.

## Flujo de trabajo

* Trabajar en pasos pequeños e iterativos.
* No modificar múltiples partes del sistema sin necesidad.
* Mantener consistencia con la estructura actual del proyecto.
* Realizar únicamente los cambios necesarios para cumplir el objetivo solicitado.
* Evitar refactorizaciones masivas no solicitadas.

## Forma de respuesta

* Ser claro, directo y técnico.
* Evitar explicaciones innecesarias.
* Priorizar soluciones prácticas.
* Indicar brevemente los archivos afectados antes de realizar cambios.

## Toma de decisiones

* Priorizar soluciones simples.
* Evitar sobreingeniería.
* Reutilizar código existente antes de crear nuevo.
* Favorecer mantenibilidad y legibilidad sobre complejidad técnica innecesaria.

## Validación

* Si algo no está claro, preguntar antes de asumir.
* No inventar estructuras, módulos o patrones que no existen en el proyecto.
* Verificar dependencias antes de utilizarlas.
* Verificar que los cambios sean compatibles con la arquitectura definida.

## Enfoque del sistema

* Pensar siempre en código mantenible.
* Respetar la arquitectura del proyecto.
* No romper funcionalidades existentes.
* Mantener bajo acoplamiento entre módulos.
* Favorecer componentes reutilizables.

## Organización del código

* Respetar la estructura de carpetas existente.
* Crear nuevas carpetas o archivos únicamente cuando aporten claridad o separación de responsabilidades.
* Evitar concentrar demasiada lógica en un solo archivo.
* Ubicar cada cambio en el archivo correspondiente según su responsabilidad.
* Mantener coherencia con la organización general del proyecto.

## Dependencias

* No agregar nuevas dependencias sin justificación.
* Priorizar librerías ampliamente utilizadas y mantenidas.
* Evitar dependencias redundantes cuando exista una solución ya presente en el proyecto.

## Documentación

* Mantener actualizada la documentación cuando se agreguen funcionalidades relevantes.
* Documentar nuevas decisiones arquitectónicas cuando corresponda.
* Mantener consistencia con los archivos ubicados en `/ai/context`, `/ai/design`, `/ai/rules` y `/ai/skills`.

## Alcance de los cambios

* No implementar funcionalidades adicionales que no hayan sido solicitadas.
* No modificar comportamiento existente sin necesidad.
* Mantener el foco en la tarea actual.
* Informar posibles mejoras futuras sin implementarlas automáticamente.
