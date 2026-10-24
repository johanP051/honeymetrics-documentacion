---
name: documentacion-mkdocs
description: >-
  Skill maestra de Documentación en 3 Etapas: (1) Documentación técnica viva en Markdown para
  MkDocs Material, (2) Pre-entregables académicos en Markdown (Manual Técnico, Manual de Usuario,
  Diccionario de Datos, SRS IEEE 830 y UML) para revisión rápida del usuario, y (3) Compilación
  fiel a Word (.docx) bajo las plantillas oficiales del docente Oscar Gómez (UDEC).
---

# 📚 Skill: Documentación Viva en MkDocs & Entregables Académicos en DOCX

Esta skill gobierna toda la documentación técnica, arquitectónica, científica (ML) y académica de los proyectos, separando las **Reglas Universales** (aplicables a cualquier software como `HoneyMetrics`, `TantauStock`, `EstefChips` o nuevos desarrollos) del **Formato Institucional UDEC** para entregas al docente.

---

## 1. El Flujo de Trabajo en 3 Etapas (Regla de Operación)

Cada vez que se desarrolle o documente un proyecto, el agente seguirá estrictamente este orden:

### Etapa 1: Documentación Técnica Viva en `docs/` (MkDocs Material) — *[Se mantiene SIEMPRE]*
- Vive dentro del repositorio (`docs/`) y se mantiene sincronizada en tiempo real con el código en cada Sprint/PR.
- Sigue el estilo de ingeniería de `TantauStock`, `EstefChips` y `HoneyMetrics`:
  - Navegación cruzada en la cabecera (`> **Ver también:** ...`) e índice de anclas (`## Índice`).
  - Diagramas en **Mermaid** (`sequenceDiagram` con `autonumber`, bloques `box` por capa arquitectónica, `activate`/`deactivate`, `alt`/`else` para errores 401/403/400/422 y `loop`; `flowchart` de infraestructura; `erDiagram` + archivo DBML para `dbdiagram.io`).
  - **Tabla de Servidores, Entornos y Puertos** (distinguiendo puertos internos de Docker, proxy Nginx y túneles públicos).
  - **Matriz Exhaustiva de Localización de Cambios:** Tabla que mapea *"Si necesitas cambiar X funcional/técnico $\to$ modifica el archivo Y en la ruta Z"*.
  - **Sección "El Por Qué Técnico" (ADRs):** Explicación razonada de las decisiones de ingeniería (ej. *Por qué usar bloqueo pesimista `select_for_update`*, *Por qué firma HMAC-SHA256 en tiempo constante*, *Por qué Client-Side PDF Offloading*, *Por qué Cache Busting*).
  - **Cheatsheet de Comandos Operativos:** Comandos copiables de Docker, migraciones, seeding, tests con cobertura y troubleshooting común.

### Etapa 2: Borrador Markdown de los Entregables del Profesor — *[Solo cuando el usuario lo solicite]*
- **Pregunta de Activación:** Al planificar o cerrar tareas de documentación, el agente preguntará: *"¿Necesitas generar también los entregables académicos para el profesor (Manual Técnico, Manual de Usuario, Diccionario de Datos o SRS IEEE 830)?"*
- Si el usuario responde que **SÍ**, el agente **NO genera el `.docx` directamente**. Primero redacta o actualiza los documentos completos en **Markdown** (ej. en `docs/entregables_profesor/`) siguiendo al pie de la letra las secciones, tablas y numeración de las plantillas del docente Oscar Gómez.
- **Aislamiento Estricto en `.gitignore`:** La carpeta `docs/entregables_profesor/` (Etapas 2 y 3) **SIEMPRE DEBE** añadirse a `.gitignore` en cada repositorio donde se alojen borradores académicos para no contaminar el repositorio de código ni el build público de MkDocs.
- **Revisión Humana Rápida:** El agente presenta estos archivos Markdown al usuario para que los lea, valide el contenido y solicite ajustes rápidamente en texto plano.

### Etapa 3: Compilación Fiel a Word (`.docx`) — *[Solo cuando el usuario apruebe la Etapa 2 y diga "Pásalo a docx"]*
- Dado que el docente califica sobre el archivo Word/PDF y no siempre ingresa al repositorio Git, una vez aprobado el Markdown de la Etapa 2, el agente ejecuta un script reproducible en Python (`python-docx`) para generar el archivo `.docx` final cumpliendo todas las especificaciones visuales de la Sección 2 de esta skill.

---

## 2. Especificaciones Visuales y Estructurales del `.docx` Académico (Estándar Docente Oscar Gómez — UDEC)

Todo archivo `.docx` generado en la Etapa 3 **DEBE** cumplir de forma exacta estos criterios derivados de los documentos oficiales del curso:

### 2.1 Encabezado Institucional en Todas las Páginas Interiores (Tabla de 3 Columnas con Bordes)
| Columna Izquierda (20%) | Columna Central (55%) | Columna Derecha (25% — Dividida en 2 filas) |
| :---: | :---: | :--- |
| Escudo oficial de la **Universidad de Cundinamarca** centrado verticalmente | **TIPO DE DOCUMENTO** (ej. `MANUAL TÉCNICO` / `MANUAL DE USUARIO` / `Especificación de Requerimientos`)<br>**NOMBRE DEL PROYECTO** | **Fila superior:** `Fecha: AAAA-MM-DD`<br>──────────<br>**Fila inferior:** `Versión: X.Y.Z` |

- **Pie de Página:** Centrado o a dos columnas indicando la asignatura (ej. `INGENIERÍA DE SOFTWARE – UDEC`) y numeración `Página X de Y`.
- **Portada (Página 1):** Título del documento en mayúsculas, nombre del proyecto, lista de integrantes con nombres completos, fecha y versión, sin mostrar el cuadro de control interno en la primera hoja.

### 2.2 Tablas de Gobernanza Documental (Justo después de la Tabla de Contenido)
1. **Tabla `REGISTRO DE CAMBIOS`:**
   - Cabecera gris con texto en negrita: `VERSIÓN | FECHA DE CAMBIO | MOTIVO DEL CAMBIO`.
2. **Tabla `CONTROL DEL DOCUMENTO`:**
   - Cabecera gris con texto en negrita: `VERSIÓN | ELABORADO | REVISADO | APROBADO`.
   - En la columna `APROBADO`, colocar siempre **`Oscar Gómez`** (o el nombre del docente titular indicado por el usuario).

### 2.3 Estructura Canónica de los 4 Entregables Académicos

#### A. Manual Técnico (`MANUAL TÉCNICO`)
1. `1. INTRODUCCIÓN`
2. `2. OBJETIVO`
3. `3. ALCANCE` (Qué incluye y qué no incluye el sistema)
4. `4. GENERALIDADES` (Módulos o aplicaciones que componen la plataforma)
5. `5. PRERREQUISITOS DEL SISTEMA` (`5.1 HARDWARE` y `5.2 SOFTWARE` con versiones exactas)
6. `6. FRAMEWORK Y ESTÁNDARES` (`6.1 FRAMEWORKS Y DEPENDENCIAS` con tabla `Nombre | Versión | Descripción`, y `6.2 ESTÁNDARES DE ARQUITECTURA Y SEGURIDAD`: metodología, encriptación, JWT, MFA, correo, reportes, consumo de APIs)
7. `7. DIAGRAMAS DE CASOS DE USO` (Separados por cada actor/rol del sistema + tabla de catálogo `Código | Caso de Uso | Descripción Corta | Actor Autorizado`)
8. `8. LÓGICA DEL SISTEMA Y DIAGRAMAS DE SECUENCIA` (Explicación del patrón arquitectónico + diagramas de secuencia renderizados en alta resolución)
9. `9. MODELO ENTIDAD RELACIÓN` (Explicación de integridad ACID + imagen nítida del MER)
10. `10. DICCIONARIO DE DATOS DEL SISTEMA` (Todas las tablas de dominio, auditoría y framework)
11. `11. GUÍA DE DESPLIEGUE Y EJECUCIÓN (DATABASE SEEDING)`
12. `12. ANEXOS`:
    - Comandos útiles, Git/Conventional Commits y pruebas unitarias (Patrón AAA: *Arrange, Act, Assert* y reporte de Coverage).
    - **Lógica de Procedimientos Almacenados (SPs) y Disparadores (Triggers):** Mínimo 3 a 5 SPs y 3 a 5 Triggers (según pida la plantilla del corte), cada uno con su **Bloque de Encabezado Formal**, **Código Fuente comentado en primera persona**, **Script de Pruebas en DBeaver** y **Capturas de evidencia del resultado antes/después o alerta de bloqueo**.

#### B. Diccionario de Datos (`DICCIONARIO DE DATOS DEL SISTEMA`)
Por cada tabla física de la base de datos, incluir el título `Tabla: <nombre_tabla>`, el párrafo `Propósito de la tabla: ...` y una tabla con **exactamente estas 5 columnas**:
`Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada`
*(En `Restricción` indicar `PK`, `FK (tabla)`, `UNIQUE`, `CHECK >= 0` o `Ninguna`; en `Obligatorio` indicar `Sí` o `No`).*

#### C. Especificación de Requerimientos — IEEE 830 (`SRS`)
1. `1. INTRODUCCIÓN` (`1.1 Propósito`, `1.2 Alcance`, `1.3 Visión General`, `1.4 Supuestos y Restricciones`).
2. `2. MODELO FUNCIONAL` (`2.1 Tabla de Actores`, `2.2 Lista de Casos de Uso con estado EJECUTADO/ACTUALIZADO/NUEVO`, `2.3 Diagramas de Casos de Uso por Rol`).
3. `3. ESPECIFICACIÓN DETALLADA DE CASOS DE USO`:
   Cada `CU-XX` debe documentarse con: Actor Principal, Descripción, Precondiciones, Reglas de Negocio (`RN01-CU-XX`), tabla de **Flujo Básico** (`PASO | ACTOR(ES) | ACCIÓN`), **Flujos Alternos (`FA-XX`)**, **Flujos de Excepción (`FE-XX`)**, **Postcondiciones (Éxito y Fallo)** y enlace a Mockup/Vista.
4. `4. REQUISITOS NO FUNCIONALES (RNF)` con criterios de aceptación verificables.

#### D. Manual de Usuario (`MANUAL DE USUARIO`)
1. `1. INTRODUCCIÓN`
2. `2. OBJETIVO`
3. `3. ALCANCE`
4. `4. MANUAL DE USUARIO`:
   - `4.1 PRE-REQUISITOS DE USO` (Conocimientos previos, hardware mínimo, conexión, credenciales).
   - `4.2 APLICACIONES DE SOFTWARE` (Navegadores soportados, app autenticadora TOTP, correo, Telegram, visores).
   - `4.3 FUNCIONALIDADES`: Dividido en **Funcionalidades Generales** (Login, MFA QR, Cierre de sesión, Recuperación de clave, Perfil) y **Funcionalidades Específicas por Rol**, paso a paso con capturas reales y bloques de nota (`⚡ Nota:`).
   - **Regla Estricta de Lenguaje 100% de Usuario Final:** Queda terminantemente **PROHIBIDO** incluir jerga interna de código o variables de backend/frontend (tales como `ROLES_TO_SCOPES`, `DATASET_PATHS`, `admin:all`, `ml:predict`, `auth_version`, `jti` o rutas de archivos `.py`/`.jsx`). Debe redactarse paso a paso desde la perspectiva visual del operador humano que utiliza la interfaz web.
   - **Tutoriales Prácticos Obligatorios:** Debe incluir tutoriales prácticos paso a paso para integraciones externas, como la configuración de Telegram mediante el bot de telemetría y `@userinfobot` (`/start`, captura de ID numérico y vinculación con `@HoneyMetrics`).
   - **Desglose Exhaustivo de Componentes Visuales:** Explicación funcional detallada de cada tarjeta/KPI, gráfica de Línea de Tiempo, Severidad, Mapa de Calor Predictivo, recomendaciones del Honeypot Advisor y filtros de período.
   - **Estados de Flujo:** Desglose riguroso de cada estado de solicitud de logs/reportes (*Pendiente de Aprobación, Procesando, Listo, Rechazada*), aclarando la diferencia entre extracción directa y masiva con aprobación interactiva en Telegram.
   - **Estructura Tridimensional por Rol:** Por cada rol (*Administrador, Consultor de Ciberseguridad, Analista de Datos, Directivo de T.I.*), desglosar obligatoriamente sus **Capacidades**, **Limitaciones** y **Recomendaciones de uso**.

---

## 3. Trazabilidad UML por Capas y Gobernanza Científica MLOps

1. **Trazabilidad 1 a 1 Código $\leftrightarrow$ UML $\leftrightarrow$ MER:**
   - Dividir los diagramas de clases por capas (`CD01 Dominio/Modelos`, `CD02 API Identidad`, `CD03 API Negocio`, `CD04 Servicios Identidad`, `CD05 Servicios Negocio`, `CD06 Core y Seguridad`) para garantizar legibilidad en página A4/Carta.
   - En el MER, distinguir con **borde continuo** las tablas implementadas en el ORM actual y con **borde punteado + etiqueta `«pendiente»`** las extensiones futuras propuestas, manteniendo una tabla de trazabilidad `Tabla SQL <-> Clase ORM <-> Clase UML`.
2. **Gobernanza en Proyectos con Machine Learning (`MLOps`):**
   - Documentar siempre: hash SHA-256 de datasets de entrada y de artefactos `.joblib` (actualizando `artifact_hashes.json`), método de partición cronológica estricta (*Out-Of-Time Validation: Train $\to$ Val $\to$ Test* sin *Data Leakage*), comparación honesta frente a al menos 2 *Baselines* simples, métricas calibradas (F1 Macro/Weighted, Brier Score, ECE) y latencias de inferencia ($p50, p95, p99$).

---

## 4. Verificación Visual Post-Generación del `.docx` (Recibo RDD)
Tras generar cualquier archivo `.docx`, el agente **DEBE** verificar antes de entregarlo:
1. Que los diagramas Mermaid hayan sido convertidos e incrustados como imágenes PNG de alta resolución (nunca dejar bloques de texto ````mermaid` crudos dentro del Word).
2. Que las tablas tengan ancho ajustado a la página sin desbordar los márgenes.
3. Que todas las imágenes referenciadas existan y se visualicen correctamente (pudiendo convertir el `.docx` a PDF temporalmente con LibreOffice `soffice --headless --convert-to pdf` para inspeccionar el conteo de páginas y el renderizado real).

---

## 5. Protocolo de Producción Multimedia Autónoma con Playwright (Videos 1080p + Capturas DOCX)

Para garantizar una experiencia visual inmersiva de nivel Enterprise (a la par de `TantauStock` y `EstefChips`), todo proyecto debe enriquecerse con capturas de pantalla reales en alta resolución y micro-videos demostrativos grabados de forma autónoma con Playwright bajo las siguientes directrices:

### 5.1 Resolución Nativa 1080p Full HD (Eliminar borrosidad)
1. **Configuración de Contexto en Playwright:** Por defecto, Playwright escala los videos a `800×450` si solo se especifica el `viewport`. Para garantizar nitidez de texto perfecta en tablas y código, es **estrictamente obligatorio** definir ambos parámetros en `browser.new_context()`:
   ```python
   viewport={"width": 1920, "height": 1080},
   record_video_size={"width": 1920, "height": 1080},
   device_scale_factor=1,
   ```
2. **Transcodificación de Calidad Editorial con ffmpeg:** Convertir los archivos temporales `.webm` a `.mp4` web-ready utilizando codificación H.264 de alta fidelidad:
   ```bash
   ffmpeg -y -i input.webm -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart output.mp4
   ```

### 5.2 Cursor Dorado 100% Visible y Movimiento Humano (`#hm-cursor` + `human_click`)
1. **Inyección Temprana en el DOM:** Para evitar que `document.body` sea `null` en navegaciones iniciales, inyectar el cursor flotante directamente sobre `document.documentElement`:
   ```javascript
   const cursor = document.createElement('div');
   cursor.id = 'hm-cursor';
   cursor.style = 'position:fixed;width:24px;height:24px;border-radius:50%;background:rgba(212,175,55,0.85);border:3px solid #ffffff;box-shadow:0 0 14px rgba(212,175,55,0.95);pointer-events:none;z-index:2147483647;transform:translate(-50%,-50%);transition:transform 0.08s ease-out;display:block;';
   document.documentElement.appendChild(cursor);
   ```
2. **Onda Expansiva en Clics (`#hm-click-ripple`):** Ante cada evento `mousedown`, generar un anillo visual dorado `#hm-click-ripple` que se expanda dinámicamente durante 250ms antes de desvanecerse.
3. **Movimiento Progresivo y Helpers:**
   - Prohibido el salto instantáneo del puntero; utilizar `page.mouse.move(cx, cy, steps=28)` actualizando las coordenadas de `#hm-cursor` en pantalla de forma continua.
   - Implementar funciones auxiliares `ensure_cursor(page)`, `smooth_hover(page, locator, steps=28)` y `human_click(page, locator, steps=28)`.
4. **Cadencia Humana y Pausas Pedagógicas:**
   - Utilizar tipeo progresivo (`press_sequentially(texto, delay=50)`).
   - Pausas de observación (`wait_for_timeout(1200)` a `1800`) al abrir modales, confirmar alertas o cargar gráficos de Plotly (`.js-plotly-plot`), esperando a que desaparezcan los esqueletos de carga (*skeletons*).
   - Censura de secretos mediante `filter: blur(6px)` en el DOM antes de capturar formularios con credenciales o códigos QR de MFA.

### 5.3 Los 5 Videos Independientes de Flujo Completo (Cero Modales Vacíos)
Queda terminantemente prohibido abrir modales y cerrarlos sin completar la acción. Cada video debe ilustrar una interacción funcional completa:
1. **`01_login_y_navegacion.mp4`:** Landing Page $\to$ clic en *Ingresar a Plataforma* $\to$ digitación carácter por carácter $\to$ alternancia del ícono del ojo para revelar/ocultar contraseña $\to$ ingreso exitoso al Dashboard $\to$ recorrido lateral de módulos.
2. **`02_dashboard_cti_filtros.mp4`:** Selector temporal (*24h* $\to$ *7 días* $\to$ *30 días*) viendo actualizar los KPIs $\to$ interacción y tooltips sobre las curvas de Plotly $\to$ scroll suave hacia abajo $\to$ inspección de celdas en el Mapa de Calor Predictivo $\to$ tarjetas del *Honeypot Advisor*.
3. **`03_threat_center_y_boveda.mp4`:** Threat Center $\to$ *Añadir Amenaza* $\to$ **Validación negativa:** ingreso de IP privada `127.0.0.1` con visualización de la alerta de bloqueo 422 $\to$ **Corrección y registro:** ingreso de IP pública real `45.148.10.215`, país, score 92 y notas $\to$ comprobación en la tabla activa $\to$ **Eliminación y archivo:** clic en eliminar, confirmación y consulta inmediata del indicador en la **Bóveda Forense**.
4. **`04_logs_export_y_pdf.mp4`:** Logs & Reportes $\to$ *Nuevo Export* con rango real de fechas $\to$ envío de solicitud $\to$ descarga del archivo $\to$ renderizado y visualización en pantalla completa del reporte oficial en PDF mediante conversión con `pdftoppm`.
5. **`05_admin_usuarios_y_roles.mp4`:** Configuración $\to$ *Gestión de Usuarios & Roles* $\to$ creación de usuario con contraseña generada por CSPRNG (*Generar Segura*) $\to$ filtrado reactivo por rol $\to$ transición a *Mi Perfil & Seguridad* $\to$ prueba del medidor dinámico de contraseñas (Rojo $\to$ Amarillo $\to$ Verde).

### 5.4 Doble Destino y Vistas Responsive
1. **En MkDocs (`docs/`):** Embeber los videos `.mp4` optimizados mediante `<video controls width="100%" playsinline class="docs-video">` acompañados de capturas `.png` de alta resolución.
2. **En Entregables `.docx` (`docs/entregables_profesor/`):** Reemplazar automáticamente los marcadores `[CAPTURA PENDIENTE: ...]` por las imágenes reales en alta resolución usando `ImageRun` con pie de figura institucional.
3. **Vistas Responsive:** Validar resolución Desktop (`1920×1080`) y vista Móvil (`390×844`).

---

## 6. Reglas de Ejecución Obligatoria para Documentación (Actualización 2026-10)

Estas reglas tienen precedencia sobre opciones de diagramación incompatibles descritas en secciones anteriores. Aplicarlas antes de redactar documentos y especialmente en HoneyMetrics v2.0.

### 6.1 Entrevista Previa Obligatoria

Antes de redactar o modificar documentación, preguntar al usuario y esperar respuesta sobre:

1. **Alcance:** ¿Solo Etapa 1 (documentación modular de ingeniería en `docs/` para GitHub/MkDocs) o también Etapa 2 (pre-entregables autocontenidos con formato UDEC/Oscar Gómez)?
2. **Diagramas:** ¿Generar código Mermaid o dejar marcadores estandarizados `[FIGURA PENDIENTE: ...]` para diagramas externos elaborados en StarUML?
3. **SQL:** ¿Documentar ahora Stored Procedures y Triggers ya implementados, o dejarlos formalmente pendientes?

No comenzar la redacción documental dependiente de estas decisiones hasta recibir respuesta. Se puede inspeccionar repositorios, consultar fuentes y preparar inventarios mientras se espera. Nunca afirmar que SPs, Triggers, evidencia o diagramas existen si no se verificaron.

### 6.2 Separación entre Documentación de Ingeniería y Entregables Docentes

**Etapa 1 — `docs/` del repositorio:** documentación modular de ingeniería orientada a MkDocs/GitHub. Según aplique, mantener `index.md`, `architecture.md`, `diccionario-datos.md`, `deployment.md`, `operations.md`, `unit-tests.md` y `manual-usuario.md`. Cada archivo comienza, en este orden, con el bloque `> **Ver también:**` y el encabezado `## Índice`. No incluir portadas universitarias, nombre de asignaturas ni tablas de control como `Aprobado: Oscar Gómez` en estos archivos. No eliminar contenido existente sin comprobar su función, duplicación y enlaces entrantes.

**Etapa 2 — `docs/entregables_profesor/`:** documentos académicos monolíticos, autocontenidos y con formato UDEC autorizado por el usuario. Incluir portada institucional, integrantes, `REGISTRO DE CAMBIOS` y `CONTROL DEL DOCUMENTO` con el aprobador indicado por el usuario. Incrustar en cada documento todas las tablas, explicaciones, flujos y guías necesarios. No sustituir contenido por referencias relativas como `../architecture.md`; se permiten referencias bibliográficas que no deleguen secciones. Respetar las plantillas y numeración que entregue el usuario.

### 6.3 Convención Condicional de Diagramas Externos StarUML

Si el usuario elige Mermaid, producir Mermaid válido y apropiado al repositorio; no insertar diagramas Mermaid en el documento docente cuando se haya elegido StarUML externo.

Si el usuario elige diagramas externos de StarUML, **no generar bloques Mermaid** para los diagramas solicitados. Explicar completamente el flujo, actores, reglas de negocio y controles de seguridad en el texto, y ubicar el marcador con su pie de figura:

```markdown
[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RFXX Nombre del Flujo]
*Figura X. Diagrama de secuencia e interacción para [descripción del flujo].*
```

Para el MER usar `[FIGURA PENDIENTE: Insertar aquí imagen del Modelo Entidad-Relación (MER) StarUML]`. No presentar marcadores como diagramas terminados ni declarar certificación visual inexistente.

### 6.4 Densidad, Trazabilidad y Exactitud

- **Directiva Anti-Resumen (`Verbosity: High`):** Queda terminantemente prohibido comprimir, resumir o recortar guías operativas, tablas de parámetros, flujos paso a paso o bloques de comandos bajo pretextos de concisión o brevedad. Se debe mantener una densidad *Deep Dive* completa y detallada, garantizando que el operador humano disponga de cada instrucción, advertencia visual y contexto sin omitir pasos intermedios.
- En los diccionarios de datos, describir cada campo en **20 a 45 palabras**, incluyendo propósito funcional, restricciones y los servicios/componentes consumidores cuando estén verificados. Aplicar tanto al diccionario modular como al entregable académico. Automatizar conteo de palabras y bloquear la entrega si algún campo queda bajo el mínimo.
- Las tablas del diccionario tienen exactamente cinco columnas: `Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada`.
- En HoneyMetrics v2.0, verificar tablas, columnas, restricciones, endpoints, símbolos y dependencias contra el código actual, modelos, migraciones, configuración y manifiestos. Marcar propuestas o extensiones no implementadas como `«pendiente»`; no inventar estructura.
- Si se solicita la Matriz de Localización de Código, mapear los requerimientos funcionales y controles de seguridad al archivo y símbolo real, evitando nombres inferidos.
- En documentación MLOps, identificar claramente evidencia medida, resultados históricos, limitaciones y propuestas. No convertir supuestos o resultados históricos en afirmaciones de estado actual.

### 6.5 Matriz de Alcance para Auditorías Deep Dive HoneyMetrics v2.0

Cuando la tarea incluya la actualización profunda descrita por el usuario, usar sus umbrales y contenidos como criterios de aceptación: `index.md` (120+ líneas), `architecture.md` (250+), `diccionario-datos.md` (180+), `deployment.md` y `operations.md` (220+ combinadas), `manual-usuario.md` (220+), manual técnico docente (500+), diccionario docente (180+) y manual de usuario docente (240+). Confirmar cada conteo mediante script y evitar relleno: cada sección debe aportar explicación verificable.

El manual técnico docente debe ser autocontenido e incluir en línea las tablas de las seis entidades implementadas, secuencias o marcadores seleccionados, despliegue y anexos. El diccionario debe cubrir las seis tablas reales y las extensiones futuras solicitadas, claramente rotuladas como pendientes. La guía de usuario debe cubrir requisitos, funcionalidades generales y por rol, límites, recomendaciones, pasos y preguntas frecuentes. Mantener fidelidad al estado real del producto incluso si difiere de instrucciones heredadas.

La documentación modular de arquitectura puede incluir catálogo de CU-01 a CU-13, cinco flujos, matriz con al menos 18 filas, ADRs y MLOps únicamente cuando cada elemento pueda trazarse a evidencia del proyecto; de lo contrario, identificar explícitamente el vacío y no fabricar hechos.

### 6.6 Verificación Bloqueante y Sincronización de la Skill

Cuando el usuario solicite sincronizar esta skill en varias rutas, inventariar primero todas las copias y sus estados Git, preservar la autorización del usuario para sincronizar, actualizar la fuente maestra y propagar el mismo archivo byte por byte. Informar rutas divergentes o repositorios con cambios previos.

Para tareas que incluyan los criterios cuantitativos de esta sección, ejecutar un recibo automatizado que verifique:

1. SHA-256 idéntico en todas las copias solicitadas de `SKILL.md`.
2. Ausencia de nombres/tablas institucionales en `docs/` modular, excluyendo `entregables_profesor/`.
3. Umbrales de líneas, autocontención y ausencia de enlaces relativos que deleguen contenido.
4. Mínimo de 20 palabras por descripción de campo en ambos diccionarios.
5. `mkdocs build --strict` exitoso sin errores ni advertencias.

Resolver errores de configuración, advertencias editoriales o enlaces rotos antes de certificar el build. No crear DOCX salvo que se alcance Etapa 3 y el usuario la autorice expresamente.

### 6.7 Protocolo de Aislamiento Gráfico Estricto en Compiladores DOCX

Para evitar la contaminación cruzada de capturas y diagramas entre manuales académicos dispares, el compilador programático de entregables DOCX (`build_entregables_docx.js`) debe acatar estrictamente las siguientes reglas de aislamiento:

1. **Desacoplamiento Estricto por Nombre de Documento (`docFile`):**
   - El motor de resolución de marcadores `resolvePlaceholderToImage(placeholderText, nextLine, docFile)` debe recibir obligatoriamente el identificador del archivo que está compilando (`docFile`). Prohibido deducir la imagen basándose únicamente en el número de figura general (`Figura 1`, `Figura 2`), ya que cada documento tiene su propia numeración independiente.

2. **Matriz de Asignación Exclusiva de Artefactos Visuales:**
   - **`01_Manual_Tecnico_HoneyMetrics_v2.md`:** Acepta **únicamente** diagramas arquitectónicos UML (Casos de Uso por Rol `cu01`..`cu05`, Diagramas de Secuencia `rf01`..`rf08`, Diagrama de Clases de Arquitectura Limpia `main_class_diagram.png`) y el Modelo Entidad-Relación (`mer_honeymetrics_v2.png`). Queda **estrictamente prohibido** incrustar capturas de pantallas de interfaz de usuario final (login, dashboard, export modal).
   - **`02_Diccionario_Datos_HoneyMetrics_v2.md`:** Acepta **únicamente** el Modelo Entidad-Relación oficial (`mer_honeymetrics_v2.png`). Queda **terminantemente prohibido** inyectar pantallazos de la aplicación web. Los marcadores de verificación de SPs o Triggers en DBeaver deben renderizarse como cajas placeholder estilizadas a menos que exista una captura de base de datos dedicada.
   - **`03_Manual_Usuario_HoneyMetrics_v2.md`:** Acepta **únicamente** capturas reales de la interfaz de usuario en producción (`fig01_login.png`, `fig01b_mobile_landing.png`, `fig02_mfa_enrolamiento.png` hasta `fig10_directivo_resumen.png`). Cero diagramas StarUML de secuencia o modelos de base de datos.
   - **`04_Manual_Tecnico_Frontend_HoneyMetrics_v2.md`:** Acepta **únicamente** diagramas de contexto, jerarquía de actores (`cu00_jerarquia_actores.png`) y diagramas de secuencia frontend. Cero capturas de interfaz final de usuario.

3. **Escalado Proporcional Sin Distorsión de Aspecto:**
   - Toda función de incrustación de imagen (`getImageDimensions`) debe inspeccionar los metadatos reales del archivo PNG (bytes `readUInt32BE(16)` y `readUInt32BE(20)`) y calcular un factor de escala uniforme `scale = Math.min(maxW / origW, maxH / origH, 1.0)`.
   - Límites máximos estandarizados en página Carta:
     - Diagramas horizontales y capturas Desktop: ancho máximo de `540 pt` y alto máximo de `380 pt`.
     - Capturas móviles verticales (Mobile Viewport `390×844`): ancho máximo de `230 pt` y alto máximo de `480 pt`.
   - Se prohíbe fijar dimensiones estáticas que deformen las relaciones de aspecto de diagramas o textos.
