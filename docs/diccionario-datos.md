# Diccionario de Datos

Este documento describe el Modelo Entidad-Relación (MER) del sistema HoneyMetrics, normalizado para PostgreSQL y gestionado vía SQLAlchemy.

> **Ver también:**
> - [Matriz de Cambios](./matriz-cambios.md) — Para encontrar los modelos ORM en el código fuente.

---

## Tabla: `users`
**Propósito:** Almacena las credenciales y el estado de los administradores y analistas del sistema.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTOINCREMENT` | Sí | Identificador único del usuario. |
| `email` | `VARCHAR` | `UNIQUE` | Sí | Correo electrónico de acceso. |
| `hashed_password`| `VARCHAR` | N/A | Sí | Contraseña hasheada con Bcrypt. |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Sí | Flag para desactivar temporalmente el acceso (Soft Delete). |
| `is_mfa_enabled` | `BOOLEAN` | `DEFAULT FALSE` | Sí | Indica si el usuario configuró su semilla TOTP. |
| `mfa_secret` | `VARCHAR` | N/A | No | Semilla secreta para validación de doble factor (PyOTP). |
| `role_id` | `INTEGER` | `FK (roles.id)` | Sí | Rol jerárquico asignado al usuario. |

---

## Tabla: `roles`
**Propósito:** Definición estricta de control de acceso (RBAC) gestionada vía `RoleEnum`.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTOINCREMENT` | Sí | Identificador único del rol. |
| `name` | `VARCHAR` | `UNIQUE` | Sí | Nombre canónico (Ej. "Administrador", "Analista de datos"). |
| `description` | `TEXT` | N/A | No | Descripción de las capacidades del rol en el sistema. |

---

## Tabla: `threat_ips`
**Propósito:** Centro de Inteligencia de Amenazas. Almacena las direcciones IP bloqueadas o bajo vigilancia.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTOINCREMENT` | Sí | Secuencia interna. |
| `ip` | `VARCHAR(45)`| `UNIQUE` | Sí | Dirección IP (Soporta IPv4 e IPv6). |
| `threat_score` | `INTEGER` | `CHECK (0-100)` | Sí | Puntuación de riesgo heurístico. |
| `category` | `VARCHAR` | N/A | Sí | Vector de ataque principal (Ej. "SSH Brute Force", "Port Scan"). |
| `status` | `VARCHAR` | N/A | Sí | Estado del bloqueo ("Activo", "En Observación"). |
| `created_at` | `TIMESTAMP` | `DEFAULT NOW()` | Sí | Fecha de detección de la amenaza. |

---

## Tabla: `threat_ips_vault`
**Propósito:** Bóveda de auditoría forense inmutable. Almacena amenazas que han sido eliminadas de la lista activa.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTOINCREMENT` | Sí | ID forense independiente. |
| `original_id` | `INTEGER` | N/A | Sí | ID que tenía la IP en la tabla `threat_ips`. |
| `ip` | `VARCHAR(45)`| N/A | Sí | Dirección IP preservada. |
| `deleted_at` | `TIMESTAMP` | `DEFAULT NOW()` | Sí | Fecha exacta del retiro de la lista negra. |

---

## Tabla: `log_exports`
**Propósito:** Trazabilidad de descargas masivas de eventos Wazuh para cumplimiento normativo y retención.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `VARCHAR` | `PK` (UUID) | Sí | UUID v4 de la solicitud de exportación. |
| `start_date` | `DATE` | N/A | Sí | Fecha inicial del bloque de logs. |
| `end_date` | `DATE` | N/A | Sí | Fecha final del bloque de logs. |
| `status` | `VARCHAR` | N/A | Sí | Estado ("Pendiente", "Completado", "Aprobado Telegram"). |
| `requested_by` | `INTEGER` | `FK (users.id)` | Sí | Usuario (Analista) que ejecutó la extracción. |
