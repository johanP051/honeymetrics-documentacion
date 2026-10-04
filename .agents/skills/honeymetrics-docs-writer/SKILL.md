---
name: honeymetrics-docs-writer
description: >-
  Skill de escritura de documentación técnica de nivel Enterprise para el proyecto HoneyMetrics v2.0.
  Actívala cuando se te pida redactar o mejorar cualquier documento en docs/ del repositorio
  honeymetrics-documentacion. Contiene las reglas de oro anti-superficialidad, las métricas
  mínimas de profundidad por tipo de documento, los patrones de contenido obligatorios y los
  archivos de referencia canónicos que DEBES leer antes de escribir.
---

# 📚 Skill: Escritura de Documentación Enterprise (HoneyMetrics v2.0)

## ⚠️ LEE ESTO ANTES DE ESCRIBIR UNA SOLA LÍNEA

El principal error al generar documentación es el de **profundidad superficial**: crear esqueletos con títulos y párrafos introductores en lugar de manuales completos. Este error se comete incluso cuando hay ejemplos disponibles.

**La causa raíz:** Sin restricciones métricas explícitas, los modelos de lenguaje optimizan hacia lo que perciben como "suficientemente bueno". El antídoto son las reglas que siguen.

---

## PASO 0 — Lectura Obligatoria de Referencias (ANTES de Escribir)

Antes de redactar cualquier documento, **DEBES leer los siguientes archivos** para calibrar el nivel de profundidad esperado. No leerlos equivale a adivinar el estándar:

```
# Referencia de Diccionario de Datos (ver extensión y formato de tablas):
/media/sebas/Exdrive/Workspace/HoneyMetrics/docs/database.md        (14 KB / 145 líneas)

# Referencia de Manual de Usuario (ver empatía operativa y matrices):
/media/sebas/Exdrive/Workspace/HoneyMetrics/docs/manual-usuario.md  (29 KB / 539 líneas)

# Referencia de Arquitectura y Secuencia (ver diagramas Mermaid):
/media/sebas/Exdrive/Workspace/HoneyMetrics/docs/architecture.md    (23 KB / 427 líneas)

# Referencia de Guía de Despliegue y Troubleshooting:
/media/sebas/Exdrive/Workspace/HoneyMetrics/docs/deployment.md      (18 KB / 242 líneas)

# Referencia de Operaciones y Cheatsheets:
/media/sebas/Exdrive/Workspace/HoneyMetrics/docs/operations.md      (27 KB / 425 líneas)

# Referencia Gold Standard de Manual de Usuario con CSS:
/media/sebas/Exdrive/Workspace/TantauStock/docs/manual-usuario.md   (33 KB / 674 líneas)

# Referencia Gold Standard de Manual Técnico con ADRs:
/media/sebas/Exdrive/Workspace/TantauStock/docs/manual-tecnico.md   (33 KB / 629 líneas)
```

---

## REGLAS DE ORO ANTI-SUPERFICIALIDAD (Mandatorias)

Estas reglas son **no-negociables**. Si no las cumples, el documento será rechazado.

### Regla 1 — Banner de Navegación Inicial
Todo documento **DEBE** comenzar con un bloque `> **Ver también:**` que enlace a 2-4 documentos relacionados con **deep-links a secciones específicas**, no solo al archivo raíz:

```markdown
> **Ver también:**
> - [manual-tecnico.md → Sección 3: Flujos de Secuencia](./manual-tecnico.md#3-flujos-críticos-mermaid) — Para entender cómo las tablas participan en los flujos de autenticación y CTI.
> - [matriz-cambios.md → Modelos ORM](./matriz-cambios.md#modelos-orm-sqlalchemy) — Ruta exacta de cada modelo en el código fuente.
```

### Regla 2 — Índice con Anclas Profundas
Todo documento **DEBE** tener un índice (TOC) con anclas que apunten a subsecciones individuales, no solo a los encabezados H2 principales. Ejemplo:

```markdown
## Índice
- [2. Diccionario de Datos](#2-diccionario-de-datos)
  - [Tabla: users](#tabla-users)
  - [Tabla: roles](#tabla-roles)
  - [Tabla: threat\_ips](#tabla-threat_ips)
```

### Regla 3 — Diagramas Mermaid para Todo Flujo Crítico
Cualquier flujo de negocio con más de 3 pasos **DEBE** tener un diagrama Mermaid. Usa siempre:
- `autonumber` en diagramas de secuencia
- `box` con colores diferenciados por capa: `box LightCyan Frontend`, `box LightYellow Backend/Services`, `box LightPink Database`, `box LightGreen External APIs`
- Bloques `alt/else` para manejar caminos de error
- `activate` / `deactivate` en los lifelines

### Regla 4 — Tabla Canónica de 5 Columnas para el Diccionario
Cada tabla del modelo de datos **DEBE** documentarse con esta estructura exacta:

```markdown
### Tabla: `nombre_tabla`
**Propósito de la tabla:** [2-3 oraciones explicando para qué existe esta tabla en el negocio]

**Archivo ORM:** `app/models/archivo.py` — Clase `NombreClase`.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :---: | :--- |
| `campo` | `TIPO(n)` | `PK/FK/UNIQUE/etc` | ✅ / ❌ | [Descripción de mínimo 2 líneas explicando por qué existe este campo, qué regla de negocio implementa y cuándo se usa] |
```

La columna "Descripción detallada" **NUNCA** debe tener menos de 30 palabras. Debe explicar el propósito de negocio, no solo el tipo técnico.

### Regla 5 — "El Por Qué Técnico" en Secciones de Configuración
Toda decisión de ingeniería no-obvia **DEBE** tener una justificación explícita bajo el patrón "El Por Qué Técnico". No documentar solo el "cómo":

```markdown
> [!NOTE]
> **El Por Qué Técnico — `VARCHAR(45)` para IPs:** RFC 5952 define que la representación textual
> máxima de una dirección IPv6 es de 39 caracteres. Sin embargo, las notaciones de IPv4 mapeadas
> a IPv6 (ej. `::ffff:192.168.1.1`) pueden alcanzar los 45 caracteres. Usar `VARCHAR(45)` garantiza
> compatibilidad sin migraciones futuras.
```

Admonitions disponibles: `[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`

### Regla 6 — Comandos con Flags Explicados
Todo bloque de comandos **DEBE** documentar qué hace cada flag. Nunca:

```bash
docker compose up -d --build  # ❌ Incompleto
```

Siempre:
```bash
# --build: Reconstruye la imagen Docker aunque no haya cambios en el Dockerfile.
#          OBLIGATORIO cuando se modificaron dependencias en requirements.txt.
# -d: Modo detached (daemon). El proceso corre en background y libera la terminal.
docker compose up -d --build
```

### Regla 7 — Matriz de Troubleshooting al Cierre de Guías
Toda guía de despliegue u operaciones **DEBE** cerrar con una tabla de resolución de problemas de **mínimo 10 filas**:

```markdown
## Resolución de Problemas Comunes

| Síntoma | Causa Probable | Solución |
| :--- | :--- | :--- |
| `OSError: [Errno 98] Address already in use` | El puerto 8000 ya está ocupado por otro proceso (posiblemente el backend de FastAPI o un contenedor Docker previo) | Ejecutar `lsof -i :8000` para identificar el proceso y terminarlo con `kill -9 <PID>`, o iniciar MkDocs en otro puerto: `mkdocs serve -a 127.0.0.1:8008` |
```

### Regla 8 — Delegación de Contenido (No Duplicar)
Si un tema está documentado en otro archivo, **NO** lo copies. Delega con un enlace y una frase de contexto:

```markdown
Para los comandos exactos de inicialización de base de datos, consultar:
- 📄 **[guia-despliegue.md → Sección 3: Seeding](./guia-despliegue.md#3-inicialización)** — Cómo ejecutar `seed_admin.py`.
```

---

## MÉTRICAS MÍNIMAS DE PROFUNDIDAD POR TIPO DE DOCUMENTO

Estas son las metas cuantitativas. Si tu documento no las alcanza, está incompleto.

| Documento | Mínimo de Líneas | Mínimo de KB | Secciones H2 Obligatorias | Elementos Mermaid |
| :--- | :---: | :---: | :---: | :---: |
| `diccionario-datos.md` | **400 líneas** | **30 KB** | 6+ (MER, Enums, un H2 por Módulo, FK, Índices, Seeding) | 1 (`erDiagram`) |
| `manual-tecnico.md` | **600 líneas** | **45 KB** | 6+ (Visión, Arquitectura, Flujos, RBAC, Seguridad, ADRs) | 4+ (secuencia por flujo crítico) |
| `guia-despliegue.md` | **400 líneas** | **25 KB** | 7+ (Topología, Prerrequisitos, `.env`, Pasos, Cheatsheet, Migración, Troubleshooting) | 1 (topología de red) |
| `manual-usuario.md` | **350 líneas** | **22 KB** | 5+ (Requisitos, Primer Acceso, Notificaciones, Guías por Rol, FAQ) | Opcional |
| `index.md` (Pitch) | **180 líneas** | **12 KB** | 4+ (El Dolor, La Solución, Momento Show, Modelo de Negocio) | 1 (`flowchart` del flujo honeypot) |

---

## ESTRUCTURA INTERNA DETALLADA POR DOCUMENTO

### Para `diccionario-datos.md`
1. Introducción + Banner `> **Ver también:**`
2. Índice con anclas a cada tabla
3. Diagrama MER en Mermaid (`erDiagram`) — con TODOS los campos relevantes y relaciones FK
4. Enumeraciones del sistema (una tabla por Enum con valores y semántica de negocio)
5. Un H2 por módulo funcional, con un H3 por tabla dentro de cada módulo
6. Por cada tabla: Propósito, Archivo ORM, Tabla de 5 columnas, Admonitions con decisiones de diseño
7. Tabla de Relaciones FK con políticas `ON DELETE` / `ON UPDATE`
8. Tabla de Índices Críticos con justificación de rendimiento
9. Sección de Seeding delegando a `guia-despliegue.md`

### Para `manual-tecnico.md`
1. Introducción + Banner `> **Ver también:**`
2. Índice profundo
3. Visión General Polyrepo (tabla de repositorios y sus roles)
4. Arquitectura FastAPI (diagrama de flujo del enrutamiento)
5. Flujos Críticos — UN diagrama de secuencia Mermaid por flujo:
   - Login con MFA (TOTP)
   - Detección y Bloqueo CTI (Wazuh → FastAPI → Telegram → Firewall)
   - Descarga Masiva de Logs con aprobación HITL
   - Anti-SSRF del Webhook de Telegram
   - Creación de Usuario por Administrador
6. Control de Acceso RBAC — Antes/Después del `RoleEnum` y tabla Rol → Permisos
7. Seguridad Criptográfica — JWT, Bcrypt, TOTP, HMAC (con "El Por Qué Técnico")
8. Integración Wazuh SIEM — Índices duales, Modo Fallback
9. Decisiones de Arquitectura (ADRs) adicionales (jsPDF en cliente, JSONL vs CSV, UUID vs ID legible)

### Para `guia-despliegue.md`
1. Introducción + Banner
2. Topología de Red (diagrama ASCII o Mermaid con IPs reales de `topologia_hardware.md`)
3. Prerrequisitos HW/SW (tabla con versiones mínimas y comandos de verificación)
4. Configuración `.env` — TABLA de 5 columnas con CADA variable: nombre, ejemplo, obligatoria, descripción, riesgo si se omite
5. Despliegue Paso a Paso — Comandos numerados con flags explicados
6. Inicialización de Datos Semilla (Seeding) — `seed_admin.py` paso a paso
7. Configuración del Webhook de Telegram — `set_telegram_webhook.py`
8. Cheatsheet de Operaciones Cotidianas (reiniciar, ver logs, backup, redeploy)
9. Migración de Servidor (dump, transfer, restore)
10. Resolución de Problemas — Tabla de mínimo 12 filas

### Para `manual-usuario.md`
1. Introducción + Banner
2. Índice
3. Requisitos del cliente (navegadores, resolución, acceso de red)
4. Primer Acceso y Configuración MFA — pasos numerados, con referencias a mockups en `/mockups/`
5. Diccionario de Notificaciones de Interfaz — tabla 4 columnas: Color/Tipo | Ejemplo | Qué Significa | Qué Hacer
6. Guías por Rol (un H3 por cada rol del sistema):
   - Administrador
   - Analista de datos
   - Consultor de Ciberseguridad
   - Directivo de T.I.
7. Casos Borde y Preguntas Frecuentes — mínimo 8 preguntas con respuestas completas

---

## CONTEXTO DEL PROYECTO (Para alimentar cada documento)

- **Proyecto:** HoneyMetrics v2.0 — Plataforma CTI y monitoreo de Honeypots
- **Backend:** FastAPI + PostgreSQL + SQLAlchemy + Alembic (`honeymetrics-backend`)
- **Frontend:** React SPA con Tailwind Dark CTI (`honeymetrics-frontend`)
- **SIEM:** Wazuh OpenSearch Indexer en nodo dedicado LAN
- **Sensor:** Orange Pi 5 como Honeypot perimetral (Cowrie/Dionaea)
- **Aprobaciones:** Bot de Telegram con flujo HITL para bloqueos y exportaciones masivas
- **Roles del sistema:** `Administrador`, `Analista de datos`, `Consultor de Ciberseguridad`, `Directivo de T.I.`
- **EXCLUIR de toda documentación:** Cualquier mención a Machine Learning, HMM, Clustering, LightGBM, modelos predictivos. Si el tema emerge, redirigir con "Objetivo de Fase 2 Enterprise".
- **Objetivo Académico:** Sustentación universitaria. Enfocarse en CTI, analítica de datos Wazuh, RBAC y arquitectura de software.

---

## PROCESO DE ESCRITURA RECOMENDADO

1. **Lee** los archivos de referencia listados en el Paso 0.
2. **Lee** el código fuente relevante del repositorio `honeymetrics-backend` para el documento que vas a escribir (modelos ORM, servicios, endpoints).
3. **Redacta** sección por sección, sin saltarte ninguna de las obligatorias.
4. **Verifica** con `wc -l` que el archivo cumple la métrica mínima de líneas.
5. **Revisa** que cada tabla de diccionario tenga descripción de más de 30 palabras por campo.
6. **Confirma** que cada flujo crítico tiene su diagrama Mermaid.
7. **Haz commit** con mensaje descriptivo: `docs(tipo): descripción del contenido agregado`.
