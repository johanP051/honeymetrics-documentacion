> **Ver también:** [Inicio](index.md) · [Manual Técnico](manual-tecnico.md) · [Despliegue & Operaciones](guia-despliegue.md) · [Manual de usuario](manual-usuario.md)

## Índice

- [Criterios de lectura y alcance](#criterios-de-lectura-y-alcance)
- [Modelo entidad-relación](#modelo-entidad-relacion)
- [Trazabilidad relacional y UML](#trazabilidad-relacional-y-uml)
- [Entidades implementadas](#entidades-implementadas)
- [Extensiones propuestas pendientes](#extensiones-propuestas-pendientes)
- [Procedimientos almacenados y triggers](#procedimientos-almacenados-y-triggers)

# Diccionario de Datos de HoneyMetrics v2.0 — PostgreSQL 16

## Criterios de lectura y alcance

Este documento refleja las migraciones Alembic presentes en el backend y los modelos SQLAlchemy correspondientes. “Obligatorio” describe `nullable=False` en la migración, no una expectativa de negocio inferida. `default ORM` identifica valores asignados por Python; no implica `DEFAULT` en PostgreSQL. Las referencias sin FK se señalan expresamente.

Hay seis tablas implementadas. La política de permisos vive actualmente en código Python; `permissions` y `role_permissions` no están creadas por migraciones. Las demás extensiones listadas son propuestas sin tablas, modelos ni endpoints confirmados.

## Modelo entidad-relación

[FIGURA PENDIENTE: Insertar aquí imagen del Modelo Entidad-Relación (MER) StarUML]
*Figura 1. Modelo entidad-relación verificado de HoneyMetrics v2.0; las entidades implementadas deben distinguirse con borde continuo y las extensiones propuestas con borde punteado y etiqueta «pendiente».*

## Trazabilidad relacional y UML

| Tabla SQL | Modelo SQLAlchemy | Clase UML sugerida | Estado y relación |
|---|---|---|---|
| `roles` | `app.models.role.Role` | `CD01 Role` | Implementada; users.role_id referencia roles.id. |
| `users` | `app.models.user.User` | `CD01 User` / `CD02 Identity API` | Implementada; rol con FK y campos MFA/auth_version. |
| `threat_ips` | `app.models.threat.ThreatIP` | `CD01 ThreatIP` / `CD03 Threat API` | Implementada; IP única. |
| `threat_ips_vault` | `app.models.threat.ThreatIPVault` | `CD01 ThreatIPVault` / `CD05 Threat Service` | Implementada; original_id y deleted_by_user_id son referencias lógicas, sin FK. |
| `log_exports` | `app.models.log_export.LogExport` | `CD01 LogExport` / `CD05 Logs Service` | Implementada; metadatos e historial de exportación. |
| `revoked_tokens` | `app.models.revoked_token.RevokedToken` | `CD06 RevokedToken` / `CD04 Auth Service` | Implementada; token_jti único para consumo atómico. |
| `permissions` | No existe | `«pendiente» Permission` | Extensión propuesta; autorización actual reside en código. |
| `role_permissions` | No existe | `«pendiente» RolePermission` | Extensión propuesta, dependiente de permissions. |
| `user_profiles` | No existe | `«pendiente» UserProfile` | Extensión propuesta; evaluar duplicación con users. |
| `blacklist_records` | No existe | `«pendiente» BlacklistRecord` | Extensión potencialmente redundante con threat_ips. |
| `user_saved_filters` | No existe | `«pendiente» UserSavedFilter` | Extensión propuesta sin endpoint vigente. |
| `security_alerts` | No existe | `«pendiente» SecurityAlert` | Extensión propuesta sin persistencia vigente. |

## Entidades implementadas
### Tabla: `roles`

**Propósito de la tabla:** Catálogo de roles que asigna la API a cada identidad y que sirve como entrada para resolver los scopes efectivos durante la autorización de solicitudes protegidas.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK; autoincremental | Sí | Identifica de forma única cada rol persistido y permite que users.role_id lo referencie. SQLAlchemy y la migración lo declaran como clave primaria; la aplicación no debe reasignarlo manualmente. |
| `name` | VARCHAR | UNIQUE; índice único | Sí | Nombre canónico del rol usado por las dependencias de autorización y por la administración de usuarios. La unicidad evita identidades de rol duplicadas y facilita mapear cada rol a sus scopes. |
| `description` | VARCHAR | Ninguna | No | Texto opcional para explicar el propósito operativo del rol en interfaces administrativas y respuestas de catálogo. No concede permisos por sí mismo; las autorizaciones se calculan desde la política de scopes del backend. |

### Tabla: `users`

**Propósito de la tabla:** Registro de identidad, credenciales, rol, recuperación de contraseña, configuración TOTP y versión de autenticación consultada al validar sesiones JWT.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK; índice | Sí | Identificador numérico primario de la identidad, generado por la persistencia y usado como referencia interna por servicios, dependencias de autenticación y relaciones con roles. No representa un dato de inicio de sesión. |
| `email` | VARCHAR | UNIQUE; índice único | Sí | Dirección de correo normalizada que el servicio de autenticación acepta como identificador de inicio de sesión y destino de recuperación. La restricción única impide que dos cuentas compartan la misma identidad registrada. |
| `hashed_password` | VARCHAR | Ninguna | Sí | Hash de contraseña producido por el contexto Passlib configurado en el servicio de identidad; el código activo usa bcrypt. Solo el verificador de autenticación lo consume y el valor nunca debe contener la contraseña original. |
| `is_active` | BOOLEAN | Nullable en migración | No | Indicador de habilitación de cuenta leído por la autenticación y administración. La migración permite NULL, por lo que clientes y servicios deben tratar explícitamente ese estado y no asumir que la columna tiene NOT NULL. |
| `role_id` | INTEGER | FK (roles.id) | Sí | Clave foránea al catálogo roles que determina el perfil de acceso evaluado por app.core.permissions. La integridad referencial garantiza que cada usuario apunte a un rol existente, sin almacenar permisos directamente en esta fila. |
| `must_change_password` | BOOLEAN | Nullable en migración | No | Bandera que permite exigir una actualización de contraseña después del aprovisionamiento administrativo. La consume la lógica de sesión y perfil cuando corresponde; la base actual admite NULL y no define un CHECK adicional. |
| `auth_version` | INTEGER | NOT NULL; server default 0 | Sí | Contador de invalidación global de sesiones incorporado como claim del JWT. Al incrementar la versión después de cambios sensibles, auth dependencies rechaza tokens emitidos con valores anteriores sin depender únicamente de su vencimiento. |
| `totp_secret` | VARCHAR | Nullable en migración | No | Secreto compartido usado por pyotp para producir códigos TOTP durante el enrolamiento y la verificación de MFA. El servicio de usuario lo consulta al confirmar códigos; debe protegerse como material de autenticación sensible. |
| `is_mfa_enabled` | BOOLEAN | Nullable en migración | No | Estado persistido que indica si la cuenta completó el enrolamiento multifactor y requiere desafío TOTP durante el login. AuthService y UserService lo consultan; NULL debe interpretarse con política segura y explícita. |
| `reset_token` | VARCHAR | Índice no único; nullable | No | Token temporal emitido para el flujo de recuperación de contraseña, buscado por el servicio de autenticación y vinculado con reset_token_expires. La columna no impone unicidad en SQL y debe validarse junto con expiración. |
| `reset_token_expires` | TIMESTAMP WITHOUT TIME ZONE | Nullable en migración | No | Fecha límite del token de recuperación evaluada por reset_user_password antes de cambiar credenciales. La comparación temporal es responsabilidad del servicio y la migración no declara zona horaria ni restricción de consistencia. |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | Nullable en migración | No | Marca temporal de creación disponible para listados y trazabilidad administrativa. El modelo puede suministrar valor durante la inserción, pero la migración permite NULL y no registra una restricción server-side de default. |

### Tabla: `threat_ips`

**Propósito de la tabla:** Lista operativa de indicadores de compromiso IP administrados por Threat Center, consultada junto con datos de telemetría para generar resúmenes CTI.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK; índice | Sí | Identificador primario autoincremental de cada indicador, utilizado por rutas CRUD para obtener, actualizar y eliminar una amenaza específica. No es un identificador externo de Wazuh ni contiene semántica de clasificación. |
| `ip` | VARCHAR(45) | UNIQUE; índice único | Sí | Dirección IP canonicalizada que identifica el IOC en Threat Center; el servicio valida IPv4 e IPv6, incluidas direcciones IPv4 mapeadas. La unicidad evita duplicados exactos y el tamaño soporta la representación textual IPv6. |
| `type` | VARCHAR(20) | NOT NULL; default ORM | Sí | Familia de dirección o categoría de tipo, normalmente IPv4 o IPv6, derivada durante la validación del IOC. La migración requiere un valor, aunque el default declarado en ORM puede no ser un default físico del servidor. |
| `country` | VARCHAR(100) | NOT NULL; default ORM | Sí | Dato contextual del país asociado al indicador, con valor predeterminado de aplicación cuando no se aporta enriquecimiento. La usan las vistas CTI; no existe una clave foránea a un catálogo geográfico. |
| `threat_score` | INTEGER | NOT NULL; sin CHECK SQL | Sí | Puntaje entero de amenaza que consume el dashboard para priorizar indicadores y ordenar resultados. La migración no impone rango numérico mediante CHECK, por lo que las validaciones de dominio se realizan en schemas y servicios. |
| `category` | VARCHAR(50) | NOT NULL | Sí | Etiqueta de clasificación del IOC presentada en filtros y vistas de análisis. El esquema no la vincula a una tabla de categorías ni define enum de base de datos; el servicio valida el contrato de entrada. |
| `status` | VARCHAR(30) | NOT NULL | Sí | Estado operativo asignado al indicador y mostrado por los controles de Threat Center. No hay catálogo relacional ni CHECK en PostgreSQL; las reglas permitidas proceden de la lógica de negocio vigente. |
| `notes` | TEXT | Nullable | No | Anotaciones de contexto conservadas con el IOC y copiadas al snapshot forense al eliminarlo. Puede estar ausente; los endpoints aplican esquemas de entrada y salida para controlar su intercambio con clientes autorizados. |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL; default ORM | Sí | Fecha de creación del registro usada en ordenación, auditoría operativa y captura histórica. El tipo no conserva zona horaria; el ORM aporta valor al crear el objeto y la migración marca la columna requerida. |
| `updated_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL; default y onupdate ORM | Sí | Última fecha de actualización asignada por el ORM cuando se modifica el IOC. El campo ayuda a mostrar vigencia y rastrear cambios, pero no sustituye un historial completo ni es actualizado por un trigger SQL. |

### Tabla: `threat_ips_vault`

**Propósito de la tabla:** Snapshots de los IOC retirados de la lista activa, preservando sus valores al eliminar la amenaza. original_id y deleted_by_user_id son referencias lógicas sin FK.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK; índice | Sí | Identificador primario autoincremental del snapshot de bóveda. Sirve para consultar cada evento archivado de manera independiente y no reemplaza original_id, que conserva el identificador previo del IOC activo. |
| `original_id` | INTEGER | Ninguna; sin FK | Sí | Identificador lógico del registro threat_ips eliminado, conservado para correlacionar la evidencia histórica con su origen. No existe una FK porque el registro activo desaparece; su interpretación requiere mantener el valor capturado. |
| `ip` | VARCHAR(45) | NOT NULL | Sí | Dirección IP copiada desde el IOC antes de retirarlo, de modo que el valor probado siga disponible aunque el registro activo ya no exista. La bóveda no declara unicidad y puede guardar múltiples eventos históricos. |
| `type` | VARCHAR(20) | Nullable en migración | No | Tipo de dirección copiado al snapshot durante la eliminación, como IPv4 o IPv6 cuando está disponible. La columna admite NULL según la migración para preservar compatibilidad con registros antiguos o datos parcialmente informados. |
| `country` | VARCHAR(100) | Nullable en migración | No | Contexto de país que tenía el IOC al momento de archivarse, copiado por ThreatCRUDService. La nulabilidad permite conservar snapshots incompletos y el valor no se actualiza después de la eliminación. |
| `threat_score` | INTEGER | NOT NULL | Sí | Puntaje de amenaza conservado exactamente al crear el snapshot para permitir reconstruir la prioridad histórica del IOC. La base requiere un entero, pero no contiene una regla CHECK de rango para este campo. |
| `category` | VARCHAR(50) | Nullable en migración | No | Clasificación histórica del indicador copiada desde threat_ips para consulta forense. No existe relación con catálogo de categorías, y la migración permite NULL en snapshots donde el dato original no estaba disponible. |
| `status` | VARCHAR(30) | Nullable en migración | No | Estado que tenía la amenaza antes de su eliminación, conservado para reconstruir la situación observada. El campo acepta NULL y no se modifica mediante operaciones posteriores sobre la lista activa. |
| `notes` | TEXT | Nullable | No | Notas del indicador guardadas como parte de la evidencia archivada. Su conservación permite revisar contexto operacional después de eliminar el IOC, pero la tabla no guarda versiones sucesivas de cada edición previa. |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL | Sí | Marca temporal original de creación del IOC activo antes de entrar en la bóveda. Se copia para distinguir antigüedad del indicador de deleted_at; PostgreSQL no almacena zona horaria en el tipo declarado. |
| `deleted_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL | Sí | Momento en que ThreatCRUDService registra el snapshot y elimina el IOC activo dentro de una transacción. Permite ordenar eventos de archivo; no existe trigger automático y el servicio produce el valor. |
| `deleted_by_user_id` | INTEGER | Nullable; sin FK | No | Identificador lógico del usuario que ejecutó la eliminación, recibido por la operación de servicio para atribución. No tiene FK a users, así que no se debe afirmar que la integridad referencial del actor está garantizada por SQL. |

### Tabla: `log_exports`

**Propósito de la tabla:** Metadatos e historial de solicitudes de extracción de eventos JSONL, incluidos rango de fechas, estado, formato y marcas temporales.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | VARCHAR(30) | PK | Sí | Identificador textual de la solicitud de exportación generado por el servicio y usado en rutas de historial, aprobación, estadísticas y streaming. La migración fija hasta treinta caracteres y no asigna secuencia SQL. |
| `start_date` | DATE | NOT NULL | Sí | Fecha inicial del intervalo de consulta solicitado por el usuario para seleccionar registros de dataset. Se usa junto con end_date en los filtros de LogsService y no conserva hora dentro del día. |
| `end_date` | DATE | NOT NULL | Sí | Fecha final del intervalo solicitado para producir el archivo JSONL. La validación temporal y el conteo se ejecutan en la aplicación; la migración no incluye CHECK que compare esta fecha con start_date. |
| `date_range` | VARCHAR(60) | NOT NULL | Sí | Etiqueta textual del período elegida o construida por el flujo de exportación para presentar la solicitud en la interfaz y mensajes de aprobación. No sustituye los dos campos DATE que delimitan la consulta. |
| `count` | INTEGER | NOT NULL | Sí | Número de registros estimado o asociado a la exportación, mostrado en historial y usado para decisiones de aprobación de solicitudes grandes. La tabla no define CHECK de no negatividad; la lógica de servicio aporta el valor. |
| `status` | VARCHAR(40) | NOT NULL; default ORM | Sí | Estado actual del proceso, por ejemplo pendiente, procesando, aprobado o completado según el flujo de servicio. Se actualiza desde API y webhook; la base no usa enum ni constraint para limitar los textos. |
| `file_format` | VARCHAR(20) | NOT NULL; default ORM | Sí | Formato asociado a la extracción, cuyo flujo actual entrega líneas JSONL. Se conserva para que interfaz y endpoint identifiquen el artefacto esperado; el campo es texto y no tiene CHECK de formato permitido. |
| `created_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL | Sí | Instante de registro de la solicitud usado para ordenar el historial y correlacionar aprobaciones. Se escribe desde el ORM, no contiene zona horaria en el esquema y no representa fecha de cada evento exportado. |
| `updated_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL | Sí | Instante de última modificación del estado o metadatos de la exportación, asignado por el modelo ORM. Facilita seguimiento operativo, pero la migración no define trigger SQL para garantizar actualización ante cambios externos. |

### Tabla: `revoked_tokens`

**Propósito de la tabla:** Registro de identificadores jti consumidos o revocados para impedir la reutilización de JWT, incluyendo desafíos MFA de un solo uso.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK; índice | Sí | Identificador interno autoincremental del registro de revocación. Se usa para la clave primaria y mantenimiento del repositorio; la lógica de seguridad busca tokens por token_jti, no por este valor. |
| `token_jti` | VARCHAR | UNIQUE; índice único | Sí | Identificador único del JWT insertado para registrar consumo o revocación. La restricción UNIQUE permite que inserciones concurrentes compitan atómicamente y solo una operación consuma un desafío MFA específico. |
| `expires_at` | TIMESTAMP WITHOUT TIME ZONE | NOT NULL | Sí | Vencimiento del token cuya jti se almacena, usado para determinar vigencia y permitir limpieza de registros expirados. No incluye zona horaria en el tipo de columna y su interpretación depende de UTC aplicado por la lógica. |

## Extensiones propuestas pendientes

Las siguientes definiciones son un inventario conceptual para futuras decisiones de arquitectura. No describen objetos existentes en PostgreSQL y no deben utilizarse como contrato de ejecución. Los tipos y restricciones están sujetos a migraciones revisadas.
### Tabla: `permissions`

**Propósito de la tabla:** Catálogo propuesto de permisos atómicos que podría formalizar scopes funcionales separados de los roles. No existe tabla ORM ni migración vigente; el modelo futuro debe alinearse con app/core/permissions.py.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK propuesta | Sí | Identificador propuesto para cada permiso atómico. No está desplegado ni existe en migraciones; la obligatoriedad y el mecanismo de generación son decisiones pendientes para una futura evolución del esquema. |
| `name` | VARCHAR | UNIQUE propuesta | Sí | Código propuesto del permiso para mapear scopes como threats:read o logs:export. No es estructura implementada; debe definirse contra las políticas vigentes antes de crear una migración. |
| `description` | VARCHAR | Pendiente | No | Explicación propuesta del alcance del permiso destinada a interfaces administrativas y auditoría. Esta columna no existe actualmente y no debe tratarse como fuente efectiva de autorización. |

### Tabla: `role_permissions`

**Propósito de la tabla:** Relación propuesta muchos-a-muchos entre roles y permisos; la autorización actual se calcula en código y esta tabla no está migrada.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `role_id` | INTEGER | FK propuesta (roles.id) | Sí | Rol que se vincularía con el permiso en el diseño futuro. La FK, reglas de borrado y clave compuesta no existen en el esquema implementado y requieren decisión antes de migrar. |
| `permission_id` | INTEGER | FK propuesta (permissions.id) | Sí | Permiso que se asignaría al rol mediante la relación propuesta. La tabla permissions aún no existe; este campo es conceptual y no puede utilizarse en consultas actuales de la API. |

### Tabla: `user_profiles`

**Propósito de la tabla:** Extensión propuesta para atributos de perfil no esenciales de autenticación. No existe como tabla separada, dado que el modelo users conserva actualmente los campos implementados.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `user_id` | INTEGER | FK propuesta (users.id), UNIQUE | Sí | Identidad a la que pertenecería el perfil extendido en una relación uno a uno. No está implementado y debe evitar duplicar campos ya presentes en users antes de aprobar su inclusión. |
| `display_name` | VARCHAR | Pendiente | No | Nombre visible propuesto para preferencias de interfaz y reportes. La aplicación actual usa datos de identidad existentes, por lo que este campo no está disponible para clientes ni servicios. |
| `preferences` | JSONB | Pendiente | No | Configuración flexible propuesta para preferencias de usuario. Tipo, validación, privacidad y compatibilidad aún no han sido definidos por migración ni contrato API; no asumir que existe en PostgreSQL actual. |

### Tabla: `blacklist_records`

**Propósito de la tabla:** Nombre de extensión heredado para una lista adicional de IPs; la funcionalidad activa ya vive en threat_ips, por lo que la tabla propuesta puede ser redundante.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK propuesta | Sí | Identificador propuesto de un registro de lista negra separado. Actualmente la lista activa es threat_ips; no se debe migrar esta tabla sin justificar cómo evita duplicar la entidad existente. |
| `ip` | VARCHAR(45) | UNIQUE propuesta | Sí | Dirección IP que contendría la tabla futura si se aprueba. El formato y canonicalización deben reutilizar _validate_ip; no hay columna ni índice con este nombre en el esquema desplegado. |
| `source` | VARCHAR | Pendiente | No | Origen de inteligencia propuesto para diferenciar captura manual e integración externa. Actualmente no se conserva este campo en threat_ips y su incorporación requiere contrato, reglas de procedencia y política de retención. |

### Tabla: `user_saved_filters`

**Propósito de la tabla:** Filtros CTI guardados por persona como extensión propuesta para acelerar consultas repetidas. No existe endpoint ni persistencia equivalente verificada en la versión actual.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK propuesta | Sí | Identificador que permitiría gestionar cada filtro guardado individualmente. La entidad no existe en modelos ni migraciones, por lo que tipo final y secuencia permanecen sujetos a diseño. |
| `user_id` | INTEGER | FK propuesta (users.id) | Sí | Propietario del filtro para aislar preferencias por cuenta. La relación y autorización de acceso no están implementadas; antes de crearla se deberá definir eliminación y control de acceso. |
| `name` | VARCHAR | Pendiente | Sí | Etiqueta elegida por el usuario para encontrar el filtro dentro de una interfaz futura. Longitud, unicidad por usuario y reglas de normalización están pendientes de especificación. |
| `criteria` | JSONB | Pendiente | Sí | Criterios estructurados de búsqueda que consumiría el dashboard si se desarrolla esta función. No hay esquema de validación, índice ni endpoint vigente asociado a este campo propuesto. |

### Tabla: `security_alerts`

**Propósito de la tabla:** Alertas persistentes de seguridad sugeridas para una ampliación futura. Actualmente el repositorio no define tabla ORM o migración con este nombre.

| Nombre del Campo | Tipo de Dato | Restricción | Obligatorio | Descripción detallada |
|---|---|---|---|---|
| `id` | INTEGER | PK propuesta | Sí | Identificador propuesto para cada alerta persistida. No está presente en el esquema real; su estrategia de retención, volumen y generación debe definirse antes de introducir índices o particionamiento. |
| `severity` | VARCHAR | CHECK propuesto | Sí | Nivel de severidad que clasificaría una alerta en un futuro módulo. Valores permitidos y reglas de validación están pendientes, por lo que no debe confundirse con threat_score. |
| `event_type` | VARCHAR | Pendiente | Sí | Categoría del evento de seguridad que originaría la alerta. No existe contrato de evento persistido actual; su vocabulario requerirá trazabilidad a fuentes como Wazuh y controles de deduplicación. |
| `created_at` | TIMESTAMP WITH TIME ZONE | Pendiente | Sí | Fecha propuesta para ordenar alertas con zona horaria explícita. El esquema vigente no contiene esta entidad y la decisión de tipos y UTC debe validarse con los casos de uso. |

## Guía de Conexión a Base de Datos en DBeaver

Para la administración e inspección forense de PostgreSQL 16 (`hm_db`), en producción (`docker-compose.prod.yml`) el servicio `db` publica exclusivamente en loopback local (`127.0.0.1:5433:5432`) para impedir exposición a la LAN/Internet y evitar colisiones con el puerto `5432` del host (`vuelos_db_data`).

- **Pestaña SSH:** Host `192.168.33.2`, Port `22`, Usuario `sebas` (Autenticación por llave `id_ed25519`).
- **Pestaña Main:** Host `127.0.0.1`, Port `5433`, Database `honeymetrics`, Username `postgres`.

## Procedimientos almacenados y triggers

En PostgreSQL 16 se encuentran desplegados y verificados los 3 Procedimientos Almacenados (`sp_archive_and_purge_expired_exports_and_tokens`, `sp_consolidate_duplicate_threat_notes`, `fn_generate_user_security_audit_report`) y los 3 Triggers de seguridad (`trg_audit_deleted_threats_vault`, `trg_rate_limit_log_exports`, `trg_sanitize_and_validate_threat_ip`).

## Matriz de Privilegios del Motor de Base de Datos (Principio de Menor Privilegio - PoLP)

Para garantizar la seguridad perimetral de la base de datos en producción, el sistema implementa una separación estricta entre la cuenta administrativa del motor y la cuenta de servicio de la aplicación:

| Rol / Cuenta PostgreSQL | Login | Privilegios de Motor | Uso Autorizado |
| :--- | :---: | :--- | :--- |
| `postgres` (Superusuario) | Sí | `SUPERUSER`, `ALL PRIVILEGES` en el clúster. | **Exclusivo para administración forense** vía DBeaver por Túnel SSH en loopback (`127.0.0.1:5433`). **Jamás usado por FastAPI**. |
| `usr_honeymetrics` (App User) | Sí | `CONNECT` en BD `honeymetrics`, `USAGE` en schema `public`, `SELECT, INSERT, UPDATE, DELETE` en tablas, `USAGE, SELECT` en secuencias. `REVOKE CREATE ON SCHEMA public`. | **Conexión habitual de la API FastAPI** (`hm_api`). No puede alterar tablas, eliminar esquemas ni crear bases de datos. |
| `hm_migrator` (Deploy User) | Sí | `CONNECT`, `USAGE` y `CREATE` en schema `public` de `honeymetrics`. Sin `SUPERUSER` ni `CREATEDB`. | **Ejecución de migraciones Alembic** en pipelines de despliegue. |

## Matriz de Control de Acceso de la Aplicación (RBAC / PBAC)

Define los permisos a nivel lógico en la API, validados mediante scopes en tokens JWT:

| Módulo / Acción | Scope Requerido | Administrador | Analista | Directivo de T.I. | Consultor de Ciberseguridad |
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


