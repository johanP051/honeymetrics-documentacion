# Matriz de Localización de Cambios — HoneyMetrics Backend
*(Formato canónico de ingeniería estilo TantauStock / Guía de Mantenimiento para DBAs, SecDevOps y SysAdmins)*

---

### Resumen del Análisis Arquitectónico
Esta matriz relaciona cada requerimiento o funcionalidad del sistema con su ubicación exacta en el código fuente del proyecto `honeymetrics-backend`. Si requiere modificar el comportamiento del sistema, busque el requerimiento en esta tabla para encontrar el archivo exacto.

## Matriz Exhaustiva de Localización de Cambios

| Área / Categoría | Requerimiento Técnico o Funcional | Archivo / Componente Afectado | Ruta del Archivo / Ubicación |
| :--- | :--- | :--- | :--- |
| 🗄️ **Base de Datos & Entorno** | Modificar cadena de conexión o credenciales de PostgreSQL | Variables de entorno del sistema | `.env`<br/>`.env.example` |
| 🗄️ **Base de Datos & Entorno** | Configurar pool de conexiones, engine SQLAlchemy | Inicializador de sesión ORM | `app/db/session.py` |
| 🗄️ **Base de Datos & Entorno** | Agregar o revisar scripts de migración de esquema | Historial de versiones Alembic | `alembic/versions/` |
| 🗄️ **Modelos ORM (SQLAlchemy)** | Modificar campos de Usuarios, hashes o flags de MFA | Modelo de datos de Usuario | `app/models/user.py` |
| 🗄️ **Modelos ORM (SQLAlchemy)** | Modificar campos de Roles y descripción funcional | Modelo de datos de Rol | `app/models/role.py` |
| 🗄️ **Modelos ORM (SQLAlchemy)** | Modificar esquema de amenazas activas (IOCs, IPs) | Modelo de Amenazas Activas | `app/models/threat.py` |
| 🗄️ **Modelos ORM (SQLAlchemy)** | Modificar historial de solicitudes y descargas de logs | Modelo de Exportaciones | `app/models/log_export.py` |
| 🔒 **Seguridad & Autenticación** | Modificar endpoints de autenticación (/login, /mfa) | Router de Autenticación | `app/api/v1/auth_router.py` |
| 🔒 **Seguridad & Autenticación** | Lógica de validación de contraseñas o reset tokens | Servicio de Autenticación | `app/services/auth_service.py` |
| 🔒 **Seguridad & Autenticación** | Configuración de doble factor (TOTP) y QR en base64 | Servicio de Usuario | `app/services/user_service.py` |
| 🛡️ **Control de Acceso (RBAC)** | Modificar nombres canónicos de roles en el sistema | Enumeración de Roles | `app/core/constants.py` |
| 🛡️ **Control de Acceso (RBAC)** | Inyección de dependencias para validación de roles | Dependencias de autorización | `app/api/deps.py` (`RoleChecker`) |
| 🛡️ **Control de Acceso (RBAC)** | Endpoints administrativos para crear/eliminar roles | Router de Roles | `app/api/v1/endpoints/roles.py` |
| 📨 **Telegram & Webhooks** | Chat ID de administrador o token secreto de webhook | Variables de entorno | `app/core/config.py` |
| 📨 **Telegram & Webhooks** | Enviar alertas interactivas y responder callbacks | Servicio de Telegram Bot | `app/services/telegram_service.py` |
| 📡 **Extracción de Logs & Wazuh** | Parámetros de conexión y credenciales Wazuh Indexer | Configuración global | `app/core/config.py` |
| 📡 **Extracción de Logs & Wazuh** | Gestión de solicitudes de extracción y streaming JSONL | Servicio de Logs | `app/services/logs_service.py` |
| 🎯 **Gestión de Amenazas** | Algoritmo de cálculo de Threat Score y resúmenes | Servicio CTI | `app/services/threat_service.py` |
| 📝 **Esquemas de Entrada & DTOs** | Esquemas Pydantic para Login, MFA y Roles | DTOs de Auth y Usuarios | `app/schemas/auth.py`, `app/schemas/user_admin.py` |
| 🐳 **DevOps & Despliegue** | Imagen Docker (Python 3.12, usuario no root) | Configuración Docker | `Dockerfile` |
| 🐳 **DevOps & Despliegue** | Mapeo de puertos, Cloudflare Tunnel y Base de Datos | Orquestador Compose | `docker-compose.yml`, `docker-compose.prod.yml` |
| 🗄️ **Modelos ORM (SQLAlchemy)** | Modificar Bóveda Forense (Auditoría inmutable de IOCs eliminados) | Modelo de Bóveda | `app/models/threat.py` (`ThreatIPVault`) |
| 🔒 **Seguridad & Autenticación** | Activar/Desactivar validación global de MFA (Switch Global) | Configuraciones Centrales | `app/core/config.py` (`MFA_ENABLED`) |
| 📨 **Telegram & Webhooks** | Interceptar respuestas (Callbacks) de Aprobación/Rechazo de Telegram | Router de Webhooks | `app/api/v1/endpoints/webhook_router.py` (o `logs.py`) |
| 🐳 **DevOps & Despliegue** | Modificar red backend, red proxy y políticas de reinicio | Orquestador Compose | `docker-compose.yml` |
