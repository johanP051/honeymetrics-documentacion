# Matriz Exhaustiva de Localización de Cambios (Dónde Tocar Qué)

Esta matriz categorizada de ingeniería permite a administradores de bases de datos (DBAs), ingenieros de software, analistas de ciberseguridad y profesionales de DevOps/SysAdmins ubicar de forma rápida, determinista y precisa el archivo exacto a modificar según el requerimiento operativo o funcional:

---

## Índice

- [1. Frontend y UI](#1-frontend-y-ui)
- [2. Backend y API](#2-backend-y-api)
- [3. Base de Datos y Persistencia](#3-base-de-datos-y-persistencia)
- [4. Machine Learning y CTI](#4-machine-learning-y-cti)
- [5. Seguridad e IAM](#5-seguridad-e-iam)
- [6. Reportes y Telemetría](#6-reportes-y-telemetria)
- [7. Infraestructura y Docker](#7-infraestructura-y-docker)
- [8. Documentación y Entregables](#8-documentacion-y-entregables)

---

## 1. Frontend y UI

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar modal de enrolamiento 2FA (código QR y verificación TOTP) | Componente `MfaModal` | `src/components/settings/MfaModal.jsx` |
| Modificar tarjeta de seguridad, alerta de `MFA_ENABLED=False` y cambio de clave | Componente `ProfileSecurityTab` | `src/components/settings/ProfileSecurityTab.jsx` |
| Ajustar hook de gestión de contraseñas, cálculo de fortaleza y llamadas 2FA | Custom Hook `useProfileSecurity` | `src/hooks/useProfileSecurity.js` |
| Modificar vista principal del perfil de usuario y pestañas de configuración | Vista de Ajustes | `src/pages/Settings.jsx` |
| Personalizar tema Cyber-Dark, paleta dorada CTI (`hm-gold`) y fuentes | Configuración de Estilos | `src/index.css`<br/>`vite.config.js` |
| Modificar cliente Axios, interceptores de JWT y manejo global de 401 | Cliente HTTP Central | `src/api/client.js` |
| Agregar o ajustar llamadas REST para administración de usuarios | Módulo API de Usuarios | `src/api/usersApi.js` |
| Actualizar datos simulados para desarrollo local sin backend activo | Mocks Offline | `src/mocks/usersMock.js`<br/>`src/mocks/threatsMock.js` |

---

## 2. Backend y API

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar rutas de login, verificación MFA, recuperación de contraseña y logout | Router de Autenticación | `app/api/v1/auth_router.py` |
| Modificar endpoints de perfil (`/me`), cambio de clave y setup/disable de 2FA | Router de Usuarios | `app/api/v1/endpoints/users.py` |
| Ajustar lógica de autenticación, hash timing hardening y emisión de JWT | Servicio de Autenticación | `app/services/auth_service.py` |
| Ajustar generación de QR TOTP, validación de contraseñas y CRUD de usuarios | Servicio de Usuarios | `app/services/user_service.py` |
| Modificar esquemas de validación para Login, Token JWT y MFA | DTOs de Autenticación | `app/schemas/auth.py` |
| Modificar contratos de entrada/salida de perfil de usuario y roles | DTOs de Administración | `app/schemas/user_admin.py` |
| Ajustar inyección de dependencias para validación de scopes PBAC | Dependencias de Seguridad | `app/api/deps.py` |

---

## 3. Base de Datos y Persistencia

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar credenciales, host o pool de conexiones a PostgreSQL | Inicializador de Sesión ORM | `app/db/session.py`<br/>`.env` |
| Modificar columnas de la tabla `users` (hashes, booleano `is_mfa_enabled`, etc.) | Modelo de Usuario | `app/models/user.py` |
| Modificar tabla de roles canónicos (`roles`) y descripciones institucionales | Modelo de Rol | `app/models/role.py` |
| Modificar tabla de lista negra de IPs atacantes (`threat_ips`) | Modelo de Amenazas Activas | `app/models/threat.py` |
| Modificar Bóveda Forense inmutable de auditoría (`threat_ips_vault`) | Modelo de Bóveda de Amenazas | `app/models/threat.py` (`ThreatIPVault`) |
| Modificar tabla de tokens revocados (Blacklist JWT para logout inmediato) | Modelo de Revocación | `app/models/revoked_token.py` |
| Modificar historial de auditoría de descargas forenses (`log_exports`) | Modelo de Exportaciones | `app/models/log_export.py` |
| Crear o ajustar scripts de migración de esquema relacional | Versiones de Alembic | `alembic/versions/` |

---

## 4. Machine Learning y CTI

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Ajustar algoritmo de cálculo de `threat_score` y tácticas MITRE ATT&CK | Pipeline ML v2 | `app/ml_v2/` |
| Modificar endpoints REST de inferencia analítica de amenazas | Router de ML | `app/api/v1/endpoints/ml.py`<br/>`app/api/v1/endpoints/ml_v2.py` |
| Ajustar umbrales de detección de anomalías y campañas de botnets | Reglas de Detección | `app/services/threat_service.py` |
| Registrar nuevos modelos serializados inmutables con hash SHA-256 | Modelos Entrenados | `models/*.joblib`<br/>`reports/ml/` |

---

## 5. Seguridad e IAM

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar matriz de mapeo entre Roles de Negocio y Scopes PBAC | Mapeo Canónico de Scopes | `app/core/permissions.py` (`ROLES_TO_SCOPES`) |
| Modificar algoritmo de firma JWT (HS256) o tiempo de expiración del token | Parámetros de Seguridad | `app/core/config.py`<br/>`app/core/security.py` |
| Activar o desactivar obligatoriedad de 2FA en el servidor | Feature Toggle Global | `app/core/config.py` (`MFA_ENABLED`)<br/>`.env` |
| Modificar dominios de correo permitidos (`allowlist`) o política de acceso | Política de Correo | `app/core/email_policy.py`<br/>`app/core/config.py` |
| Ajustar políticas de Rate Limiting por IP y protección contra fuerza bruta | Limitador de Peticiones | `app/core/rate_limit.py` |

---

## 6. Reportes y Telemetría

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Personalizar reportes ejecutivos en PDF (5 zonas, tablas y gráficos) | Exportador Cliente jsPDF | `src/components/threats/ExportPdfModal.jsx` |
| Ajustar conexión y consultas al clúster OpenSearch / Wazuh Indexer (`192.168.32.11`) | Servicio de Telemetría Wazuh | `app/services/logs_service.py` |
| Modificar endpoints de streaming JSONL y solicitud de auditoría forense | Router de Logs | `app/api/v1/endpoints/logs.py` |
| Modificar notificaciones interactivas y aprobación HITL en Telegram Bot | Servicio de Telegram | `app/services/telegram_service.py` |

---

## 7. Infraestructura y Docker

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar puertos internos, redes Docker (`hm_network`) o variables globales | Orquestación Base | `docker-compose.yml` |
| Ajustar configuración industrial (4 workers Uvicorn, tunel Zero Trust, sin puertos públicos) | Orquestación Producción | `docker-compose.prod.yml` |
| Configurar Deploy Key dedicada (`id_ed25519_hm_v2`) y alias SSH | Enrutamiento SSH del Host | `~/.ssh/config` (`Host github.com-hm-v2`) |
| Modificar tokens de Cloudflare Tunnel o credenciales del webhook de Telegram | Variables de Entorno | `.env` |
| Ajustar imagen Docker de Python (multi-stage builder, usuario no-root 1001) | Dockerfile de Backend | `Dockerfile` |

---

## 8. Documentación y Entregables

| Requerimiento Técnico o Funcional | Componente / Archivo Afectado | Ruta del Archivo en el Repositorio |
| :--- | :--- | :--- |
| Modificar estructura de navegación o temas del portal MkDocs Material | Archivo de Configuración | `mkdocs.yml` |
| Actualizar guía de despliegue paso a paso en Ubuntu con Deploy Key | Guía Práctica Ubuntu | `docs/guia_despliegue_ubuntu.md` |
| Actualizar especificación de requerimientos de software (SRS IEEE 830) | Documento de Requerimientos | `docs/entregables_profesor/` |
| Actualizar especificación de Diagramas UML y scripts de compilación PDF | Manifiesto y Scripts UML | `docs/assets/uml/`<br/>`/home/sebas/Documents/hm-UML/` |
