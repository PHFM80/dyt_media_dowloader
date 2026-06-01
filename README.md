# Documentación del Proyecto

Toda la documentación funcional, técnica y de arquitectura debe almacenarse dentro del directorio:

```text
docs/
```

## Objetivo

Centralizar la documentación del proyecto para facilitar:

* Desarrollo.
* Mantenimiento.
* Incorporación de nuevas funcionalidades.
* Comprensión de la arquitectura.
* Trabajo asistido por IA.

---

## Estructura recomendada

```text
docs/
├── architecture/
├── features/
├── integrations/
├── setup/
├── decisions/
└── roadmap/
```

### architecture/

Documentación relacionada con:

* Arquitectura general.
* Diagramas.
* Flujos del sistema.
* Organización de módulos.

### features/

Documentación funcional.

Ejemplos:

* Descarga de videos.
* Descarga de playlists.
* Cola de procesamiento.
* Gestión de archivos.

### integrations/

Documentación de integraciones externas.

Ejemplos:

* yt-dlp
* FFmpeg
* Spotify
* TikTok
* Instagram

### setup/

Documentación de instalación y configuración.

Ejemplos:

* Instalación local.
* Variables de entorno.
* Dependencias.

### decisions/

Registro de decisiones técnicas y arquitectónicas.

Ejemplos:

* Elección de tecnologías.
* Cambios de arquitectura.
* Restricciones del proyecto.

### roadmap/

Planificación de funcionalidades futuras.

Ejemplos:

* Próximas versiones.
* Mejoras previstas.
* Funcionalidades pendientes.

---

## Reglas de documentación

* Mantener la documentación actualizada.
* Documentar funcionalidades relevantes.
* Documentar cambios arquitectónicos importantes.
* Evitar documentación duplicada.
* Utilizar nombres descriptivos para los archivos.

---

## Convenciones

* Utilizar formato Markdown (`.md`).
* Un tema por archivo.
* Mantener estructura clara y fácil de navegar.
* Incluir ejemplos cuando aporten valor.

---

## Relación con AI Context

La documentación ubicada en `docs/` complementa la información definida en:

```text
ai/context/
ai/design/
ai/rules/
ai/skills/
```

Los archivos de `ai/` contienen instrucciones para asistentes de IA.

Los archivos de `docs/` contienen documentación funcional y técnica del proyecto.
