# Arquitectura del sistema

## Organización general

* El sistema está organizado por módulos funcionales.
* Cada módulo debe tener una responsabilidad clara y bien definida.
* La plataforma principal es YouTube, pero la arquitectura debe permitir incorporar nuevas plataformas.
* Cada plataforma debe implementarse de forma independiente.

---

## Estructura principal

### UI

Responsabilidades:

* Interfaz de usuario.
* Captura de entradas.
* Visualización de resultados.
* Visualización del progreso de las descargas.

La UI no debe contener lógica de negocio.

---

### Services

Responsabilidades:

* Orquestar los procesos del sistema.
* Gestionar colas de descarga.
* Gestionar archivos y carpetas.
* Coordinar llamadas a módulos externos.

Toda la lógica de negocio debe residir aquí.

---

### Platforms

Responsabilidades:

* Implementar la integración específica de cada plataforma.
* Validar URLs.
* Obtener metadatos.
* Descargar contenido.

Cada plataforma debe estar aislada de las demás.

Ejemplos:

* youtube
* spotify
* tiktok
* instagram

---

### Integraciones

Responsabilidades:

* Encapsular herramientas externas.
* Aislar dependencias de terceros.

Ejemplos:

* yt-dlp
* FFmpeg

La lógica de integración no debe mezclarse con la lógica de negocio.

---

### Configuración

Responsabilidades:

* Configuración general del sistema.
* Rutas de descarga.
* Preferencias del usuario.
* Parámetros globales.

---

## Flujo general

1. El usuario ingresa una o varias URLs.
2. El sistema identifica la plataforma.
3. Se selecciona el módulo correspondiente.
4. Se obtienen los metadatos necesarios.
5. Se genera una cola de procesamiento.
6. Se crea una carpeta de descarga única.
7. Se procesan los elementos de la cola.
8. Los archivos se almacenan en la carpeta generada.

---

## Gestión de descargas

* Todas las descargas se almacenan dentro del directorio `downloads`.
* Cada ejecución genera una carpeta independiente.
* Formato recomendado:

```text
downloads/descarga_YYYYMMDD_HHMMSS
```

Ejemplo:

```text
downloads/descarga_20260601_154530
```

* Todos los archivos generados durante la misma operación deben almacenarse en dicha carpeta.

---

## Cola de procesamiento

El sistema debe soportar:

* URL individual.
* Múltiples URLs pegadas manualmente.
* Archivo de texto con URLs.
* Playlists.

Todas las entradas deben transformarse en una cola común de procesamiento.

---

## Escalabilidad

* Nuevas plataformas deben agregarse sin modificar el núcleo del sistema.
* Nuevas funcionalidades deben respetar la separación de responsabilidades.
* Evitar dependencias directas entre plataformas.

---

## Consistencia

* Utilizar nombres descriptivos y consistentes.
* Mantener los mismos patrones en todos los módulos.
* Mantener una estructura homogénea entre plataformas.

---

## Modificaciones

* Antes de agregar código, revisar si ya existe funcionalidad similar.
* Evitar duplicación de lógica.
* Evitar refactorizaciones innecesarias.
* Mantener compatibilidad con funcionalidades existentes.
