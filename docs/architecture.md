> **Ver también:** [Inicio](index.md) · [Diccionario de datos](diccionario-datos.md) · [Despliegue](deployment.md) · [Operaciones](operations.md) · [Manual de usuario](manual-usuario.md)

## Índice

- [1. Contexto, límites y modelo de capas](#1-contexto-limites-y-modelo-de-capas)
- [2. Catálogo de casos de uso](#2-catalogo-de-casos-de-uso)
- [3. Capas del backend FastAPI](#3-capas-del-backend-fastapi)
- [4. Capas del frontend React](#4-capas-del-frontend-react)
- [5. Flujos de interacción y seguridad](#5-flujos-de-interaccion-y-seguridad)
- [6. Modelo y trazabilidad UML](#6-modelo-y-trazabilidad-uml)
- [7. Matriz de localización de código](#7-matriz-de-localizacion-de-codigo)
- [8. El Por Qué Técnico — ADRs](#8-el-por-que-tecnico-adrs)
- [9. Entornos y límites](#9-entornos-y-limites)

# Arquitectura de HoneyMetrics v2.0

## 1. Contexto, límites y modelo de capas

HoneyMetrics separa una SPA React de una API FastAPI y del almacenamiento PostgreSQL. Las integraciones con Wazuh Indexer, Telegram y Cloudflare se comunican a través de límites configurados; no comparten acceso directo al DOM ni a la base de datos.

La expresión “cinco capas” describe grupos de responsabilidades arquitectónicas y no cinco paquetes físicos estrictamente independientes. El código actual conserva utilidades transversales de seguridad y configuración, y algunos servicios consultan SQLAlchemy directamente. La matriz de este documento apunta a las implementaciones reales, incluso cuando la separación pudiera fortalecerse en una evolución futura.

Las cajas de componentes que deben reproducirse en StarUML son: `React 18 SPA`, `FastAPI Routers`, `Service Layer` y `PostgreSQL 16 / Wazuh-alerts`. En los diagramas de componentes se deben distinguir interfaces HTTP, dependencias internas y conexiones de red, además de las entidades persistidas.

### 1.1 Principios de diseño observables

- **Validación en el límite:** Pydantic valida request/response y los schemas de React controlan la presentación de campos.
- **Reglas de aplicación en servicios:** routers delegan operaciones de autenticación, recuperación, amenazas, logs y ML a servicios por dominio.
- **Persistencia relacional:** SQLAlchemy gestiona transacciones y modelos; Alembic describe los cambios desplegables.
- **Autorización explícita:** dependencias verifican identidad, versión de autenticación y scopes requeridos por endpoint.
- **Defensa en profundidad:** tokens de vida acotada, MFA, limitación de tasa, CORS, validación de IP, confianza explícita de proxies y verificación de artefactos.
- **Degradación visible:** los mocks de contingencia en frontend deben presentarse como modo offline, sin atribuir sus resultados a telemetría consultada en vivo.

### 1.2 Límites externos

Wazuh Indexer entrega alertas de telemetría consumidas por servicios de dashboard. La disponibilidad y fidelidad de sus resultados dependen de credenciales, certificados, conectividad y nombres de índices configurados.

Telegram es un canal de aprobación humana para algunos procesos de exportación. El webhook debe autenticar su secreto y comparar material sensible en tiempo constante donde la implementación lo dispone. La operación de extracción no debe darse por aprobada solamente porque el bot esté configurado.

Cloudflare Tunnel publica una ruta de entrada sin requerir que el backend exponga directamente un puerto a internet. El túnel no reemplaza autenticación de la API, CORS ni reglas de autorización.

## 2. Catálogo de casos de uso

Los identificadores CU-01 a CU-13 son una organización documental de capacidades existentes. El actor identifica el rol backend previsto; si la matriz de permisos o guardas de frontend diverge, debe resolverse en código y no asumir que la descripción concede acceso.

| Código | Caso de uso | Actor principal | Alcance y controles |
|---|---|---|---|
| CU-01 | Iniciar sesión y completar MFA | Cualquier usuario activo | Credenciales; si MFA está activo, TOTP completa desafío temporal de un solo uso. |
| CU-02 | Recuperar y cambiar contraseña | Usuario propietario; servicio de correo | Respuesta anti-enumeración, token expirable y revocación lógica de sesiones mediante auth_version. |
| CU-03 | Administrar perfil y factores | Usuario autenticado | Consulta perfil, cambio de clave, setup/verify/disable MFA bajo sesión válida. |
| CU-04 | Consultar dashboard CTI | Administrador, consultor, analista y perfiles de lectura permitidos | Lectura de métricas y consultas Wazuh sujetas a scopes y disponibilidad externa. |
| CU-05 | Filtrar el resumen por período | Usuario con dashboard:read | Entrega rango temporal al endpoint y servicio; fecha validada y parámetros acotados. |
| CU-06 | Consultar indicadores de Threat Center | Usuario con threats:read | Lista activa, resumen, persistentes, botnets y bóveda forense autorizada. |
| CU-07 | Registrar un indicador | Administrador o Consultor con threats:write | Valida IP y campos, verifica duplicado y persiste la amenaza. |
| CU-08 | Actualizar indicador | Administrador o Consultor con threats:write | Recupera por id, aplica cambios permitidos y registra updated_at desde ORM. |
| CU-09 | Retirar indicador a bóveda | Administrador con threats:delete conforme a policy | Snapshot transaccional a threat_ips_vault seguido de eliminación activa. |
| CU-10 | Solicitar exportación JSONL | Usuario con logs:export | Filtra fuentes de DATASET_PATHS y registra metadatos de la solicitud. |
| CU-11 | Aprobar exportación por Telegram | Administrador / aprobador configurado | Valida origen/secreto del webhook y actualiza el estado del job. |
| CU-12 | Descargar/consultar exportación | Usuario con permiso de lectura/exportación | Consulta historial, estadísticas y stream JSONL sujeto a ownership/reglas vigentes. |
| CU-13 | Ejecutar inferencia o revisar modelos | Usuario con ml:predict | Invoca ML v1 o capacidades ML v2 autorizadas; la respuesta experimental no constituye promoción. |

El catálogo no implica que existan pantallas distintas para cada uso ni que todos los roles tengan el mismo nombre en UI y backend. Verifique `ROLES_TO_SCOPES`, guards React y configuración de rutas antes de crear cuentas.

## 3. Capas del backend FastAPI

### 3.1 Presentación y transporte HTTP

`app/main.py` crea la aplicación, registra middleware, CORS, límites y routers. `app/api/v1/router.py` agrega grupos de rutas y establece el prefijo configurado por `API_V1_STR`.

Los routers de `app/api/v1/` traducen requests HTTP a llamadas de servicios, declaran dependencias de usuario/scopes y serializan las respuestas con esquemas Pydantic. Sus responsabilidades incluyen códigos de estado, parámetros de transporte y límites de payload; no deberían convertirse en contenedores de algoritmos de negocio.

Rutas principales: `auth_router.py`, `endpoints/users.py`, `threats.py`, `threats_crud.py`, `dashboard.py`, `logs.py`, `ml.py` y `ml_v2.py`. `health.py` comunica disponibilidad de la API y `ingest.py` expone un punto de entrada Wazuh cuyo comportamiento actual es de stub.

### 3.2 Aplicación y orquestación

`app/services/` coordina las operaciones del sistema. `auth_service.py` verifica credenciales, firma JWT, construye desafío MFA, procesa recuperación y revoca tokens. `user_service.py` mantiene perfil, contraseña y configuración MFA.

`threat_crud_service.py` implementa operaciones CRUD y snapshots. `logs_service.py` registra solicitudes, filtra archivos, integra el webhook y transmite JSONL. `telegram_service.py` controla mensajes y callbacks. `dashboard_service.py` y `threat_service.py` consultan métricas y Wazuh.

`ml_service.py` administra inferencias v1, mientras `ml_v2_service.py` incorpora servicios experimentales v2. La ejecución simulada de una tarea corta usa FastAPI BackgroundTasks; no se debe documentar como Celery sin integrar esa dependencia.

### 3.3 Dominio y contratos

`app/schemas/` define contratos Pydantic agrupados por autenticación, amenazas, dashboard, logs y ML. Las reglas invariantes de dominio incluyen canonicalizar IP, limitar transiciones de exportación y comprobar códigos TOTP.

Los modelos ORM definen entidades relacionales: Role, User, ThreatIP, ThreatIPVault, LogExport y RevokedToken. Las reglas de permisos se mantienen en `app/core/permissions.py`; las tablas `permissions` y `role_permissions` no están migradas.

Los servicios deberían recibir datos ya validados y devolver objetos o resultados que los routers traduzcan a HTTP. En algunos flujos actuales, el esquema de request, modelo ORM y lógica de aplicación conviven de forma cercana; la documentación no atribuye abstracciones de repositorio que no estén presentes.

### 3.4 Persistencia e infraestructura

`app/db/session.py` crea el engine y las sesiones a partir de `DATABASE_URL`; `app/db/base.py` importa modelos para metadatos y Alembic. `alembic/versions/` versiona el schema.

PostgreSQL 16 es el motor de despliegue documentado en Compose. SQLite aparece como default de settings y puede usarse para pruebas; no es el objetivo productivo de esta guía.

Integraciones externas: requests al Wazuh Indexer, API HTTP de Telegram, envío de correo mediante proveedor configurado, Cloudflare Tunnel y rutas locales declaradas por `DATASET_PATHS`. Cada integración debe tener timeout, validación de TLS y secretos externos configurados por ambiente.

### 3.5 Transversales de seguridad y configuración

`app/core/security.py` implementa hashing/verificación y token; `app/core/permissions.py` asigna scopes; `app/api/deps.py` valida tokens y versión de autenticación; `app/core/rate_limit.py` aplica limitación configurada.

`app/core/config.py` valida listas CORS, `TRUSTED_PROXY_CIDRS`, `DATASET_PATHS`, Wazuh, Telegram y modo productivo. En producción exige clave JWT no predeterminada y configuración Wazuh completa según el validador observado.

`app/utils/ml_integrity.py` valida SHA-256 con el manifiesto y evita deserializar un artefacto si el hash no coincide. El secreto JWT y los tokens de integraciones no se deben copiar en manuales, capturas ni argumentos de comandos.

### 3.6 Matriz Dual de Seguridad y Control de Acceso (PoLP + PBAC)

La arquitectura de HoneyMetrics v2.0 implementa una separación estricta entre la seguridad física del motor de base de datos y la autorización lógica de la API REST:

#### 1. Matriz A — Privilegios en el Motor PostgreSQL 16 (Nivel Infraestructura / PoLP)

Bajo el **Principio de Menor Privilegio (PoLP)** y la Regla de Oro *"1 App = 1 Usuario Dedicado"*, en producción (`docker-compose.prod.yml`) la API jamás se conecta utilizando la cuenta superusuario del motor:

| Rol / Cuenta PostgreSQL | Login | Privilegios de Motor | Uso Autorizado |
| :--- | :---: | :--- | :--- |
| `postgres` (Superusuario) | Sí | `SUPERUSER`, `ALL PRIVILEGES` en el clúster. | **Exclusivo para administración forense** vía DBeaver por Túnel SSH en loopback (`127.0.0.1:5433`). **Jamás usado por FastAPI**. |
| `usr_honeymetrics` (App User) | Sí | `CONNECT` en BD `honeymetrics`, `USAGE` en schema `public`, `SELECT, INSERT, UPDATE, DELETE` en tablas, `USAGE, SELECT` en secuencias. `REVOKE CREATE ON SCHEMA public`. | **Conexión habitual de la API FastAPI** (`hm_api`). Aprovisionado mediante `scripts/hardening_db_roles_polp.sql`. No puede alterar tablas, eliminar esquemas ni crear bases de datos. |
| `hm_migrator` (Deploy User) | Sí | `CONNECT`, `USAGE` y `CREATE` en schema `public` de `honeymetrics`. Sin `SUPERUSER` ni `CREATEDB`. | **Ejecución de migraciones Alembic** en pipelines de despliegue controlados. |

#### 2. Matriz B — Control de Acceso Lógico en la Aplicación (Nivel Negocio / PBAC)

Define los permisos a nivel lógico en la API, validados mediante scopes en tokens JWT:

| Módulo / Acción | Scope Requerido | Administrador / Superusuario | Analista de datos | Directivo de T.I. | Consultor de Ciberseguridad |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Ver Métricas y Gráficas** | `dashboard:read` | Sí | Sí | Sí | Sí |
| **Ver Amenazas e IPs** | `threats:read` | Sí | No | Sí | Sí |
| **Registrar / Editar Amenazas** | `threats:write` | Sí | No | No | Sí |
| **Eliminar Amenazas (Vault)** | `threats:delete` | Sí | No | No | No |
| **Ver Historial de Logs** | `logs:read` | Sí | Sí | Sí | Sí |
| **Solicitar y Descargar Logs** | `logs:export` | Sí | Sí | No | Sí |
| **Inferencias ML (Scoring / MITRE)** | `ml:predict` | Sí | Sí | No | No |
| **Ingesta de Telemetría (SIEM)** | `ingest:write` | Sí | No | No | No |
| **Gestión de Usuarios y Roles** | `admin:all` | Sí | No | No | No |

**Justificación Arquitectónica de Desempeño:**
Los scopes se validan en memoria (<0.5 ms) en FastAPI a partir del token JWT stateless firmado con HS256, evitando JOINs recursivos contra tablas relacionales en cada petición para garantizar el SLA de latencia (<5 ms por inferencia). La revocación inmediata de privilegios está asegurada con `users.auth_version` y la denylist atómica en `revoked_tokens`.

## 4. Capas del frontend React

### 4.1 Presentación y navegación

La SPA usa React 18 y React Router para componer páginas en `src/pages/`. El login, dashboard, Threat Center, logs, configuración y análisis ML son vistas de alto nivel. Componentes compartidos viven bajo `src/components/` y features bajo `src/features/`.

La estructura debe separar elementos presentacionales (formulario, tabla, modal, tarjeta) de la lógica de servidor y de navegación. Tailwind CSS define tokens y clases; los recursos visuales permanecen en `public/` o el módulo correspondiente.

### 4.2 Hooks y estado de aplicación

Los hooks propios encapsulan estado, carga, efectos, validación y acciones reutilizables. Por ejemplo, un hook de seguridad de perfil agrupa peticiones de setup MFA y cambio de contraseña; la vista presenta estados idle/loading/error/success sin crear endpoints artificiales.

Los hooks deben evitar llamadas dobles por efectos de montaje cuando sea posible y no registrar tokens ni secretos. Para acciones idempotentes, la API y el contrato de UI deben minimizar resultados distintos por reintento.

### 4.3 Infraestructura frontend

El cliente HTTP centralizado en `src/services/` o `src/api/` adjunta la sesión, aplica timeout y normaliza errores. La localización exacta se verifica mediante la matriz de código más abajo.

Plotly.js y `react-plotly.js` renderizan visualizaciones interactivas; jsPDF y autotable permiten generar reportes en el navegador; Canvas convierte recursos gráficos a imágenes que jsPDF incorpora al PDF sin trasladar esa maquetación al backend.

Vite con SWC compila el bundle. El repositorio frontend tiene build oficial `npm run build` y Node soportado por `package.json`; Nginx sirve la aplicación en Compose y `wrangler.jsonc` declara publicación de assets SPA en Cloudflare Workers. Esa configuración no acredita que un deployment esté activo.

## 5. Flujos de interacción y seguridad

### 5.1 Login, desafío MFA TOTP y consumo de jti

El endpoint de configuración de MFA es idempotente mientras el enrolamiento siga pendiente: `UserService.setup_mfa` reutiliza la semilla ya guardada y evita reemplazar el QR que ya está en pantalla. Para activar MFA, `verify_and_enable_mfa` acepta `valid_window=1`; este ajuste de tolerancia aplica al enrolamiento.


1. El usuario envía correo y contraseña al formulario; el hook llama `POST /api/v1/auth/login`.
2. `auth_router.login` delega a `authenticate_user`, que localiza usuario, comprueba su hash bcrypt y estado de cuenta.
3. Si MFA no está activo, se emite un access token JWT con expiración, scopes y auth_version sujeto a la política vigente.
4. Si MFA está activo, se emite un token temporal de desafío, no una sesión completa; el cliente muestra el formulario TOTP.
5. El usuario introduce el código del autenticador y el cliente envía `POST /api/v1/auth/login/mfa-verify`.
6. `verify_login_mfa` valida firma, propósito MFA y vencimiento, y luego `consume_mfa_token` registra el jti en `revoked_tokens` antes de validar el TOTP. El índice UNIQUE hace atómico el primer consumo.
7. El servicio busca la cuenta y verifica código TOTP con la ventana por defecto de PyOTP (`valid_window=0`); solo un código válido después del consumo puede emitir access token de sesión.
8. Si el código es incorrecto, el desafío ya quedó consumido. El usuario debe volver a enviar credenciales para obtener otro; las llamadas concurrentes o repetidas con el mismo jti se rechazan. Ninguno de estos errores emite sesión.

[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RF01 Inicio de sesión, desafío MFA TOTP y consumo de jti]
*Figura 1. Secuencia de autenticación con desafío TOTP y garantía de consumo único del token temporal.*

### 5.2 Recuperación y restablecimiento de contraseña

1. El usuario solicita recuperación con una dirección de correo. `POST /auth/forgot-password` recibe la petición sin revelar si la cuenta existe.
2. `process_password_recovery` responde de forma genérica para reducir CWE-200 de enumeración de cuentas y puede enviar un mensaje solo cuando la identidad es elegible.
3. El token de recuperación aleatorio y su vencimiento se guardan asociados al usuario; el correo entrega el enlace correspondiente cuando el proveedor está configurado.
4. El navegador abre la ruta de restablecimiento y envía token y nueva contraseña a `POST /auth/reset-password`.
5. `reset_user_password` localiza token, verifica vencimiento y aplica el hash de contraseña. Un token inválido, inexistente o expirado falla sin cambiar la cuenta.
6. Al completar el cambio, limpia datos temporales y aumenta `auth_version`; los JWT emitidos con una versión anterior dejan de pasar dependencias protegidas.
7. El usuario vuelve a iniciar sesión con la credencial nueva y, si está habilitado, completa MFA.

[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RF02 Recuperación y restablecimiento de contraseña]
*Figura 2. Flujo anti-enumeración, verificación de expiración y revocación de sesiones por auth_version.*

### 5.3 Threat Center CRUD, IP canónica y snapshot de bóveda

1. Un cliente autenticado solicita el listado o una operación sobre un IOC. La dependencia de API verifica JWT, auth_version y scope `threats:read`, `threats:write` o `threats:delete` según la acción.
2. La request se valida con `ThreatIPCreate` o `ThreatIPUpdate`; `ThreatCRUDService._validate_ip` parsea y canonicaliza IPv4/IPv6 y maneja direcciones IPv4 mapeadas.
3. En creación, el servicio comprueba duplicados bajo la unicidad de `threat_ips.ip`; errores de integridad se traducen a respuesta controlada.
4. En actualización, el servicio recupera por id, restringe los campos modificables y persiste la nueva marca temporal desde ORM.
5. En eliminación, el servicio copia los atributos actuales en `threat_ips_vault` junto con `original_id`, fecha y actor lógico, y elimina el IOC activo dentro de la transacción de sesión.
6. El snapshot ofrece trazabilidad operacional posterior, pero sus campos de usuario/origen no son FK ni el registro tiene firma criptográfica. El concepto de no repudio debe limitarse a evidencia de aplicación y permisos.
7. Si el IOC no existe, la IP no es válida, el usuario carece de scope o falla la transacción, el sistema no debe informar borrado exitoso.

[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RF03 Threat Center CRUD y bóveda forense]
*Figura 3. Validación canónica de IOC, autorización y persistencia de snapshot al retirar una amenaza.*

### 5.4 Dashboard CTI, Wazuh y reporte PDF cliente

1. Una vista del dashboard solicita métricas y rango temporal al endpoint protegido de dashboard o amenazas.
2. El servicio consulta las fuentes disponibles: consultas al Wazuh Indexer y datos del modelo CTI local según la ruta concreta. Cualquier fallo de TLS, conexión o autorización se expone como estado de error, no como métrica confirmada.
3. La API devuelve estructuras tipadas para agregaciones, listas o series; el cliente las presenta con componentes React y Plotly.js.
4. Si el usuario pide un reporte, la interfaz prepara los datos ya cargados y el cliente genera un documento PDF mediante jsPDF, tablas compatibles y Canvas para rasterizar los elementos gráficos que la vista incorpora.
5. El navegador descarga el archivo final. La generación de presentación ocurre en cliente y no debe confundirse con archivo PDF persistido en backend.
6. Las respuestas offline/mocks deben aparecer identificadas como contingencia y no atribuirse a una consulta activa a Wazuh.

[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RF04 Dashboard CTI y exportación de reporte PDF]
*Figura 4. Consulta CTI a Wazuh Indexer y generación de PDF en el navegador del usuario.*

### 5.5 Exportación JSONL, aprobación Telegram e inferencia ML

1. El usuario con `logs:export` solicita rango de fechas; el router valida identidad y delega a LogsService.
2. LogsService recorre únicamente archivos configurados en `DATASET_PATHS`, parsea líneas JSON y aplica las fechas solicitadas. Un path inaccesible o una línea inválida debe registrarse como error controlado sin filtrar secretos.
3. La solicitud registra metadatos en `log_exports`. Las tareas cortas se ejecutan mediante `BackgroundTasks` en la API; no hay garantía de cola persistente ante reinicio de proceso.
4. Solicitudes que requieren aprobación se comunican al Bot de Telegram. El webhook valida el secreto configurado y la comparación debe usar `hmac.compare_digest` donde aplica la política.
5. Una decisión aprobatoria actualiza estado y habilita descarga según permisos. Denegación, webhook no autenticado o expiración bloquean la descarga.
6. El usuario obtiene un stream JSONL y puede ejecutar inferencia ML sobre datos autorizados. El endpoint ML valida el schema y la carga de modelo utiliza `safe_joblib_load` con SHA-256 comparado con manifiesto.
7. Un hash distinto, manifiesto inconsistente o artefacto ausente causa rechazo/carga degradada; nunca se debe deserializar un artefacto no verificado.
8. Los resultados de ML v2 permanecen sujetos a sus reportes de validación y no deben tratarse como decisión de bloqueo sin proceso de promoción aprobado.

[FIGURA PENDIENTE: Insertar aquí imagen de Diagrama de Secuencia StarUML — RF05 Exportación JSONL, aprobación Telegram e inferencia ML]
*Figura 5. Flujo de lectura de datasets, aprobación humana y análisis con artefactos de integridad validada.*

## 6. Modelo y trazabilidad UML

El diccionario documenta seis tablas actuales: `roles`, `users`, `threat_ips`, `threat_ips_vault`, `log_exports` y `revoked_tokens`. `threat_ips_vault.original_id` y `deleted_by_user_id` no declaran FK.

La generación de diagramas UML debe realizarse en StarUML y mantenerse sincronizada con el código. Separar diagramas de clase para reducir densidad y usar estos identificadores de vista:

| Diagrama | Contenido | Paquetes / dependencias sugeridas |
|---|---|---|
| CD01 Dominio/Modelos | Role, User, ThreatIP, ThreatIPVault, LogExport, RevokedToken | app.models y relaciones físicas verificadas |
| CD02 API Identidad | AuthRouter, User endpoints, schemas, deps | Contratos de autenticación y perfil |
| CD03 API Negocio | Threats, Dashboard, Logs, ML routers | Endpoints, dependencias y schemas |
| CD04 Servicios Identidad | AuthService, UserService, Security utilities | JWT, TOTP, recuperación y auth_version |
| CD05 Servicios Negocio | ThreatCRUDService, LogsService, TelegramService, Dashboard/ML | Reglas y gateways observados |
| CD06 Core y Seguridad | Settings, permissions, rate limit, deps, ML integrity | Políticas transversales y configuración |

Las extensiones `permissions`, `role_permissions`, `user_profiles`, `blacklist_records`, `user_saved_filters` y `security_alerts` solo deben dibujarse con borde punteado y estereotipo `«pendiente»`. No conectarlas con una línea de FK sólida si esa relación no existe en migración.

## 7. Matriz de localización de código

| Requerimiento / control | Backend: archivo y símbolo | Frontend: archivo / módulo | Evidencia observable |
|---|---|---|---|
| Inicio de sesión | `app/api/v1/auth_router.py:login`; `app/services/auth_service.py:authenticate_user` | `src/features/auth/` y `src/pages/Login.jsx` | POST `/auth/login` |
| Token JWT y claims | `app/services/auth_service.py:create_access_token`; `app/core/security.py` | `src/services/` cliente HTTP | JWT firmado y expiración |
| Desafío MFA de login | `app/api/v1/auth_router.py:verify_login_mfa`; `auth_service.py:verify_login_mfa` | `src/features/auth/` | POST `/auth/login/mfa-verify` |
| Consumo único de MFA jti | `auth_service.py:consume_mfa_token`; `app/models/revoked_token.py:RevokedToken` | gestión de estado de autenticación | UNIQUE `token_jti` |
| Recuperación de contraseña | `auth_router.py:forgot_password`; `auth_service.py:process_password_recovery` | `src/pages/ForgotPassword.jsx` | respuesta genérica y correo |
| Cambio de contraseña / versión | `auth_router.py:reset_password`; `auth_service.py:reset_user_password` | vista/hook de contraseña | incremento `auth_version` |
| Validación de identidad y scope | `app/api/deps.py:get_current_user`; `app/core/permissions.py:get_scopes_for_role` | `src/guards/` y configuración de rutas | dependencias `require_scopes` |
| Perfil y enrolamiento MFA | `app/api/v1/endpoints/users.py:setup_mfa`; `app/services/user_service.py:setup_mfa` | `src/components/settings/ProfileSecurityTab.jsx` | QR/secret y confirmación OTP |
| Verificar/activar MFA | `users.py:verify_mfa`; `user_service.py:verify_and_enable_mfa` | `src/components/settings/MfaModal.jsx` | `is_mfa_enabled` cambia tras validación |
| Desactivar MFA | `users.py:disable_mfa`; `user_service.py:disable_mfa` | Settings / Profile security | endpoint protegido |
| Catálogo de roles | `app/api/v1/endpoints/roles.py`; `app/services/role_service.py` | `src/pages/Settings.jsx` / admin | operaciones de rol permitidas |
| CRUD de amenazas | `app/api/v1/endpoints/threats_crud.py`; `app/services/threat_crud_service.py` | `src/pages/ThreatCenter.jsx` | GET/POST/PUT/DELETE `/threats` |
| Canonicalización de IP | `threat_crud_service.py:_validate_ip` | formularios de IOC | IPv4/IPv6 validada antes de persistir |
| Bóveda de amenazas | `threat_crud_service.py:delete`; `app/models/threat.py:ThreatIPVault` | tabla de bóveda en Threat Center | snapshot antes de delete |
| Resumen CTI | `app/api/v1/endpoints/threats.py:get_threat_summary`; `app/services/threat_service.py:get_threat_summary` | Dashboard CTI y componentes Plotly | agregaciones / Wazuh |
| Exportación de logs | `app/api/v1/endpoints/logs.py:request_log_export`; `app/services/logs_service.py:request_export` | `src/pages/Logs.jsx` | crea metadatos y procesa rango |
| Fuentes JSONL | `app/core/config.py:Settings.DATASET_PATHS`; `logs_service.py:_dataset_candidate_paths` | selector/solicitud de rango | paths explícitos del entorno |
| Webhook Telegram | `logs.py:telegram_webhook`; `logs_service.py:process_telegram_webhook`; `telegram_service.py:handle_callback_query` | no requiere vista pública de aprobación | token secreto y respuesta del bot |
| Streaming JSONL | `logs.py:download_log_export`; `logs_service.py:stream_jsonl_dataset` | acción de descarga | streaming controlado por autorización |
| Dashboard ejecutivo | `app/api/v1/endpoints/dashboard.py:get_executive_report`; `dashboard_service.py:get_executive_report` | `src/pages/Dashboard.jsx` | datos ejecutivos tipados |
| Inferencia ML v1 | `app/api/v1/endpoints/ml.py`; `app/services/ml_service.py:MLService` | páginas/components ML | endpoints `ml:predict` |
| Inferencia ML v2 | `app/api/v1/endpoints/ml_v2.py`; `app/services/ml_v2_service.py:MLV2Service` | análisis de sesión | capacidades experimentales |
| Integridad de artefactos | `app/utils/ml_integrity.py:safe_joblib_load`; `app/ml/artifact_hashes.json` | no aplica | verificación SHA-256 pre-carga |
| Proxy confiable | `app/core/config.py:Settings.TRUSTED_PROXY_CIDRS` | Nginx en repo frontend | CIDR validado y headers limitados |
| Rate limiting | `app/core/rate_limit.py` | mensajes UI ante 429 | protección de frecuencia |
| PDF cliente | no requiere endpoint de renderizado; datos provienen de API | jsPDF en páginas de reporte frontend | descarga generada en browser |
| health check | `app/api/v1/endpoints/health.py:health_check` | monitorización | GET health |
| ingesta Wazuh | `app/api/v1/endpoints/ingest.py:ingest_wazuh_events` | integración externa | stub actual; no persistencia de eventos |

## 8. El Por Qué Técnico — ADRs

### ADR-01 — Separación por responsabilidades en cinco capas

**Contexto.** Routers HTTP, reglas de negocio, acceso a datos e integración externa cambian por motivos distintos. Si todo vive en endpoints, los errores de protocolo, persistencia y dominio se vuelven difíciles de aislar.

**Decisión.** Mantener routers FastAPI delgados, delegar casos de uso a servicios, validar contratos en schemas Pydantic, modelar entidades SQLAlchemy y encapsular configuración/seguridad en `app/core` y utilidades. En React, separar vistas, hooks y componentes de presentación.

**Beneficio.** Se puede revisar permisos y errores en un límite conocido, reutilizar servicios y probar reglas con menos acoplamiento. El código existente todavía mezcla algunas responsabilidades; por ello esta ADR expresa el diseño objetivo alineado a la implementación, no una afirmación de perfección arquitectónica.

### ADR-02 — MFA de un solo uso por jti único

**Contexto.** Un token de desafío MFA podría repetirse o llegar concurrentemente desde peticiones duplicadas. Una validación de firma por sí sola no impide reutilización dentro de su vida útil.

**Decisión.** Asignar jti al token temporal y registrar su consumo en `revoked_tokens`, con índice UNIQUE en `token_jti`. La operación de base es la autoridad concurrente: una inserción gana y una repetición choca con la unicidad.

**Beneficio.** El consumo se coordina de forma atómica entre workers y protege el desafío de replay sin mantener estado de sesión en memoria del proceso. Una limpieza futura de tokens debe respetar `expires_at`.

### ADR-03 — Confiar proxies solamente por CIDR explícito

**Contexto.** Cabeceras `X-Forwarded-For` o equivalentes pueden ser falsificadas por un cliente si la API confía cualquier conexión proxy. Eso afecta auditoría, limitación de tasa y decisiones basadas en IP.

**Decisión.** Validar `TRUSTED_PROXY_CIDRS` como redes CIDR y derivar identidad de proxy solo de redes declaradas por operador. Compose de producción configura el valor esperado del proxy frontend.

**Beneficio.** Se reduce spoofing de cabeceras y la confianza se restringe a infraestructura identificada. Cada despliegue debe hacer coincidir la CIDR con la red real, evitando usar el ejemplo por defecto sin inspección.

### ADR-04 — Verificar SHA-256 antes de deserializar joblib

**Contexto.** `joblib.load` puede reconstruir objetos Python y un archivo no confiable podría ejecutar carga peligrosa. La presencia de un modelo en disco no demuestra que sea el artefacto aprobado.

**Decisión.** Comparar digest calculado contra el manifiesto `artifact_hashes.json` y usar `safe_joblib_load` como puerta de carga antes de deserializar el modelo.

**Beneficio.** Se detectan cambios accidentales o sustitución de artefactos antes de cargar. El hash aporta integridad frente a un valor esperado confiable, no firma de procedencia si manifiesto y modelo pueden modificarse juntos; proteger ambos en el proceso de release.

### ADR-05 — Generar PDF en el cliente

**Contexto.** Los reportes de presentación se construyen a partir de información ya consultada y su generación en el servidor añade consumo de CPU, almacenamiento temporal y endpoints de ciclo de vida.

**Decisión.** Utilizar jsPDF y plugins de tablas desde el frontend para maquetar y descargar el documento en navegador.

**Beneficio.** Se descarga un archivo sin mantener artefactos PDF persistentes y se escala la presentación hacia el usuario. El backend sigue siendo responsable de autorizar datos y devolverlos con minimización adecuada; el cliente no puede elevar permisos.

### ADR-06 — JSONL por DATASET_PATHS configurados

**Contexto.** Los eventos crudos pueden residir fuera de PostgreSQL y cambiar por día/mes. Buscar rutas arbitrarias entregadas por usuario generaría riesgo de acceso a archivos locales.

**Decisión.** Exponer un conjunto de archivos aprobados mediante `DATASET_PATHS` y filtrar fechas en el servicio de exportación.

**Beneficio.** El origen de extracción es explícito y controlado por operaciones. La carpeta montada debe ser solo lectura cuando sea posible, acotada y comprobada para evitar enlaces o permisos inesperados.

### ADR-07 — Sesiones stateless con auth_version

**Contexto.** JWT reduce consultas de sesión, pero una contraseña cambiada o una cuenta afectada requiere revocar tokens emitidos con anterioridad.

**Decisión.** Incluir `auth_version` como claim y compararlo con el valor vigente del usuario en dependencias de autenticación.

**Beneficio.** Los cambios sensibles invalidan de forma lógica sesiones existentes mientras mantienen expiración del JWT. La API sigue consultando estado de usuario para validar versión y cuenta activa; “stateless” describe formato de credencial, no ausencia absoluta de lectura de persistencia.

## 9. Entornos y límites

La tabla de puertos y entornos se mantiene en [Inicio](index.md#3-ambientes-servidores-contenedores-y-puertos). El compose de desarrollo evita publicar DB y API salvo una override local; el frontend puede ejecutarse con Vite en el host.

La producción usa Docker non-root para API, PostgreSQL no publicado directamente y Nginx/Cloudflare en repositorio frontend e infraestructura del despliegue. El perfil de Tunnel requiere archivo de token solo lectura y DNS/rutas configuradas en la cuenta Cloudflare.

No se hallaron definiciones SQL de stored procedures o triggers en las migraciones actuales. Las extensiones de esquema propuestas permanecen marcadas `«pendiente»` en [Diccionario de datos](diccionario-datos.md).
