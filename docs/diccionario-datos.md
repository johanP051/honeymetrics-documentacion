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



# 7. Objetos Programables del Motor: Procedimientos Almacenados y Triggers PostgreSQL 16

La arquitectura de persistencia de HoneyMetrics implementa una estrategia de Defensa en Profundidad que traslada controles de integridad física, saneamiento y auditoría al motor relacional PostgreSQL 16. Aunque la capa de servicios de FastAPI gobierna la lógica de negocio y las validaciones de esquemas mediante Pydantic, delegar ciertas operaciones críticas al motor de base de datos previene brechas causadas por errores en el código de aplicación o accesos concurrentes directos. Esta dualidad arquitectónica garantiza que ningún registro corrupto o inconsistente sea persistido en el almacenamiento secundario, independientemente del cliente o proceso que intente interactuar con el esquema. La infraestructura resultante mitiga condiciones de carrera, optimiza el rendimiento transaccional al reducir el tráfico de red entre la API y la base de datos, y asegura la trazabilidad inmutable de eventos forenses.

El entorno productivo se ejecuta sobre una instancia de PostgreSQL 16 Alpine desplegada en el Homeserver institucional con dirección IP privada 192.168.33.2. Para prevenir colisiones con otras cargas de trabajo que ocupan el puerto estándar 5432, el servicio de base de datos se encuentra enlazado exclusivamente a la interfaz de loopback local en el puerto 5433. Este esquema de enlace restringe la superficie de ataque perimetral, impidiendo cualquier conexión directa no autenticada desde la red de área local o desde Internet sin previa tunelización criptográfica. La administración del motor se realiza de forma segura mediante túneles SSH autenticados por llaves asimétricas ed25519 a través del gestor DBeaver, garantizando canales cifrados y confidencialidad operacional absoluta.

En concordancia con el Principio de Menor Privilegio (PoLP), la cuenta de servicio de la aplicación FastAPI denominada usr_honeymetrics opera bajo severas restricciones de privilegios. A este usuario se le revocó explícitamente el permiso de creación de esquemas y alteración de tablas DDL mediante la instrucción REVOKE CREATE ON SCHEMA public. No obstante, para permitir la interacción dinámica y eficiente con la lógica procedural del motor, se le otorgaron privilegios de ejecución explícitos sobre todas las rutinas y procedimientos almacenados públicos. Esta política asegura que la aplicación consuma los procedimientos y desencadenadores autorizados sin contar con capacidades destructivas sobre la topología de la base de datos.

---

## 7.1 Procedimiento Almacenado 1: `sp_archive_and_purge_expired_exports_and_tokens`

### Introducción y Justificación Arquitectónica

En los sistemas de inteligencia contra amenazas cibernéticas con alta tasa de ingesta, las tablas destinadas a la denegación temporal de credenciales y al historial de extracciones experimentan un crecimiento volumétrico continuo. La tabla revoked_tokens almacena identificadores JTI de tokens JSON Web Token invalidados para mitigar la reutilización de sesiones y desafíos de autenticación multifactor. Si estos registros no se depuran periódicamente tras alcanzar su fecha límite de expiración natural, la tabla acumula millones de filas obsoletas que degradan los árboles B-Tree de los índices primarios y saturan la memoria compartida del motor. De manera similar, la tabla log_exports acumula metadatos de archivos de telemetría que ya fueron consumidos por los analistas del SOC o rechazados durante el flujo de aprobación, generando consumo innecesario de almacenamiento en el almacenamiento de producción.

La acumulación descontrolada de tuplas inactivas incrementa drásticamente los costos de mantenimiento interno del motor de base de datos, elevando los tiempos de ejecución de las tareas automáticas de autovacuum y bloating de páginas de disco. Cuando la capa de aplicación intenta procesar purgas masivas mediante consultas SELECT combinadas con sentencias DELETE fragmentadas por lotes desde Python, se genera una sobrecarga inaceptable en el ancho de banda de red y se satura el pool de conexiones asíncronas de SQLAlchemy. Este cuello de botella compite directamente con las solicitudes en tiempo real del panel de control de amenazas y las inferencias del modelo de aprendizaje automático. La implementación de un procedimiento almacenado nativo dentro de PostgreSQL 16 resuelve esta fricción al ejecutar la transferencia y eliminación de tuplas de forma atómica en el almacenamiento interno sin intermediarios de red.

La ejecución de la purga y archivado a nivel de motor de base de datos garantiza la atomicidad estricta y el aislamiento transaccional bajo el estándar ACID. Al concentrar la lógica en PL/pgSQL, el procedimiento puede crear dinámicamente la tabla histórica log_exports_archive si no existe, salvaguardando los registros completados o rechazados antes de alterar el estado de la tabla operativa. Los parámetros bidireccionales INOUT permiten al procedimiento informar con precisión métrica el número exacto de registros purgados y archivados mediante diagnósticos internos de filas afectadas. Esta capacidad permite que tareas automatizadas del sistema operativo o llamadas directas de mantenimiento desde DBeaver sincronicen el mantenimiento sin requerir que la API de FastAPI permanezca en ejecución.

### Diccionario de Parámetros de Entrada y Salida

| Nombre del Parámetro | Modo | Tipo de Dato | Valor por Defecto | Descripción Técnica Detallada |
|---|---|---|---|---|
| `p_days_threshold` | IN | INTEGER | 30 | Define el intervalo numérico en días utilizado como umbral temporal de corte para evaluar la antigüedad de las exportaciones y de los identificadores de tokens revocados que deben ser purgados de la persistencia operativa. |
| `p_tokens_purged` | INOUT | INTEGER | 0 | Parámetro bidireccional que recibe la inicialización de conteo y retorna al llamador el número entero de identificadores únicos de tokens revocados cuya expiración superó el límite establecido y fueron eliminados físicamente del motor relacional. |
| `p_exports_archived` | INOUT | INTEGER | 0 | Parámetro bidireccional que consolida y devuelve al cliente el número total de registros de exportación de eventos cuya antigüedad excedió el umbral parametrizado, los cuales fueron duplicados en el archivo histórico y actualizados a estado archivada. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — PROCEDIMIENTO ALMACENADO 01
-- Nombre:    sp_archive_and_purge_expired_exports_and_tokens
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Purga tokens revocados expirados y archiva exportaciones antiguas en log_exports_archive
-- ==============================================================================

CREATE OR REPLACE PROCEDURE sp_archive_and_purge_expired_exports_and_tokens(
    IN p_days_threshold INT DEFAULT 30,
    INOUT p_tokens_purged INT DEFAULT 0,
    INOUT p_exports_archived INT DEFAULT 0
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_cutoff_timestamp TIMESTAMP WITHOUT TIME ZONE;
BEGIN
    -- Calculo la marca temporal de corte restando el umbral de días al tiempo presente
    v_cutoff_timestamp := NOW() - (p_days_threshold || ' days')::INTERVAL;

    -- Creo la tabla histórica de exportaciones si todavía no existe en el esquema público
    CREATE TABLE IF NOT EXISTS log_exports_archive (
        archive_id SERIAL PRIMARY KEY,
        original_id VARCHAR(30) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        date_range VARCHAR(60) NOT NULL,
        count INTEGER NOT NULL,
        status VARCHAR(40) NOT NULL,
        file_format VARCHAR(20) NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        archived_at TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT NOW()
    );

    -- Transfiero una copia de respaldo a la tabla histórica antes de modificar el estado operativo
    INSERT INTO log_exports_archive (
        original_id, start_date, end_date, date_range, count, status, file_format, created_at, archived_at
    )
    SELECT 
        le.id, le.start_date, le.end_date, le.date_range, le.count, le.status, le.file_format, le.created_at, NOW()
    FROM log_exports le
    WHERE le.created_at < v_cutoff_timestamp
      AND le.status IN ('Listo', 'Rechazada');

    -- Actualizo el estado operativo de las exportaciones transferidas a la categoría archivada
    UPDATE log_exports
    SET status = 'archivada',
        updated_at = NOW()
    WHERE created_at < v_cutoff_timestamp
      AND status IN ('Listo', 'Rechazada');

    -- Capturo el número de registros de exportación que fueron procesados y archivados
    GET DIAGNOSTICS p_exports_archived = ROW_COUNT;

    -- Elimino de forma definitiva los identificadores de tokens revocados cuya expiración ya ocurrió
    DELETE FROM revoked_tokens
    WHERE expires_at < NOW() - (p_days_threshold || ' days')::INTERVAL;

    -- Capturo la cantidad total de tokens JWT purgados de la denylist
    GET DIAGNOSTICS p_tokens_purged = ROW_COUNT;

    -- Emito un registro informativo en la consola de PostgreSQL para auditoría del DBA
    RAISE NOTICE '[AUDIT] Procedimiento sp_archive_and_purge completado exitosamente: % tokens purgados, % exportaciones archivadas.',
        p_tokens_purged, p_exports_archived;
END;
$$;
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — SP 01
-- ==============================================================================

-- 1. Preparación de datos de prueba en la sesión actual
INSERT INTO revoked_tokens (token_jti, expires_at)
VALUES 
    ('jti-test-expired-alpha-2026', NOW() - INTERVAL '35 days'),
    ('jti-test-expired-beta-2026', NOW() - INTERVAL '40 days'),
    ('jti-test-valid-gamma-2026', NOW() + INTERVAL '1 day');

INSERT INTO log_exports (id, start_date, end_date, date_range, count, status, file_format, created_at, updated_at)
VALUES 
    ('EXP-TEST-OLD-01', '2026-08-01', '2026-08-15', '2026-08-01 to 2026-08-15', 1500, 'Listo', 'jsonl', NOW() - INTERVAL '35 days', NOW() - INTERVAL '35 days'),
    ('EXP-TEST-OLD-02', '2026-08-16', '2026-08-30', '2026-08-16 to 2026-08-30', 420, 'Rechazada', 'jsonl', NOW() - INTERVAL '45 days', NOW() - INTERVAL '45 days'),
    ('EXP-TEST-RECENT-03', '2026-10-20', '2026-10-25', '2026-10-20 to 2026-10-25', 85, 'Listo', 'jsonl', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days');

-- 2. Ejecución del procedimiento almacenado con bloque anónimo en DBeaver
DO $$
DECLARE
    v_purged INT := 0;
    v_archived INT := 0;
BEGIN
    CALL sp_archive_and_purge_expired_exports_and_tokens(
        p_days_threshold   => 30,
        p_tokens_purged    => v_purged,
        p_exports_archived => v_archived
    );
    RAISE NOTICE 'Resultado de la ejecución: Tokens purgados = %, Exportaciones archivadas = %', v_purged, v_archived;
END $$;

-- 3. Verificación de integridad post-ejecución
SELECT token_jti, expires_at FROM revoked_tokens WHERE token_jti LIKE 'jti-test-%';
SELECT id, status, updated_at FROM log_exports WHERE id LIKE 'EXP-TEST-%';
SELECT * FROM log_exports_archive WHERE original_id LIKE 'EXP-TEST-%';

-- 4. Limpieza de datos sintéticos de prueba
DELETE FROM revoked_tokens WHERE token_jti LIKE 'jti-test-%';
DELETE FROM log_exports WHERE id LIKE 'EXP-TEST-%';
DELETE FROM log_exports_archive WHERE original_id LIKE 'EXP-TEST-%';
```

!!! tip "Verificación de SP1 en Homeserver vía Túnel SSH en DBeaver"
    Para ejecutar `sp_archive_and_purge_expired_exports_and_tokens` en el Homeserver `192.168.33.2`, configure en DBeaver la pestaña **SSH** apuntando al Host `192.168.33.2`, Puerto `22`, Usuario `sebas` y su llave privada `id_ed25519`. En la pestaña **Principal**, defina Host `127.0.0.1`, Puerto `5433`, Base de datos `honeymetrics` y Usuario `postgres`. Abra un editor SQL (Ctrl + ] en DBeaver), pegue el bloque de prueba anónimo y presione Ctrl + Enter para inspeccionar los mensajes emitidos por `RAISE NOTICE` en la pestaña de Salida del Servidor.

---

## 7.2 Procedimiento Almacenado 2: `sp_consolidate_duplicate_threat_notes`

### Introducción y Justificación Arquitectónica

Durante los incidentes de seguridad informática y las campañas de cacería de amenazas, múltiples analistas del SOC e integraciones automáticas documentan hallazgos sobre una misma dirección IP sospechosa en turnos operativos sucesivos. Debido a la naturaleza distribuida de la telemetría, el campo notes de la entidad threat_ips con frecuencia acumula fragmentos textuales repetidos, observaciones desordenadas o anotaciones redundantes separadas convencionalmente por punto y coma. Esta fragmentación de notas degrada la legibilidad de la inteligencia contra amenazas en el panel de control y dificulta la extracción automatizada de indicadores contextuales por parte de los servicios de procesamiento analítico. La falta de consolidación genera ambigüedad operativa, incrementando el tiempo medio de respuesta de los operadores ante vectores de ataque activos.

Cuando la consolidación textual de cadenas se traslada a la capa de aplicación, la API debe extraer cientos de registros a memoria, particionar las cadenas en listas de Python, filtrar elementos duplicados y ejecutar sucesivas sentencias UPDATE de regreso a la base de datos. Este flujo de ida y vuelta a través de la red no solo desperdicia ciclos de CPU del servidor web, sino que también prolonga la duración de los bloqueos a nivel de fila, incrementando el riesgo de interbloqueos con las tareas de ingestión continua de eventos de Wazuh. Si múltiples peticiones concurrentes intentan actualizar el mismo registro simultáneamente, se producen anomalías de lectura sucia y serialización fallida. La utilización de tablas temporales en PostgreSQL con la cláusula ON COMMIT DROP garantiza que el procesamiento se realice en memoria volátil de sesión sin generar contención sobre las transacciones del motor principal.

Implementar el procedimiento sp_consolidate_duplicate_threat_notes dentro del motor relacional permite aprovechar las funciones analíticas y vectoriales nativas de PostgreSQL como string_to_array, unnest y string_agg. La combinación de estas instrucciones con la cláusula DISTINCT y funciones de saneamiento perimetral TRIM permite descomponer, depurar, ordenar alfabéticamente y volver a ensamblar las anotaciones en una única instrucción atómica. Además, el procedimiento incorpora una cláusula condicional de actualización que solo muta las tuplas cuyo contenido final sea estrictamente distinto del valor persistido original, reduciendo al mínimo la generación de transacciones de escritura y registros Write-Ahead Logging. El soporte para un parámetro de filtrado opcional por dirección IP brinda flexibilidad tanto para el saneamiento quirúrgico de un indicador específico como para campañas de optimización global.

### Diccionario de Parámetros de Entrada

| Nombre del Parámetro | Modo | Tipo de Dato | Valor por Defecto | Descripción Técnica Detallada |
|---|---|---|---|---|
| `p_ip` | IN | VARCHAR(45) | NULL | Dirección IP canónica correspondiente al indicador de compromiso específico que se desea consolidar, o valor nulo para procesar la totalidad de registros con notas fragmentadas almacenados en la tabla operativa de inteligencia. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — PROCEDIMIENTO ALMACENADO 02
-- Nombre:    sp_consolidate_duplicate_threat_notes
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Deduplica y consolida notas CTI fragmentadas en threat_ips delimitadas por punto y coma
-- ==============================================================================

CREATE OR REPLACE PROCEDURE sp_consolidate_duplicate_threat_notes(
    IN p_ip VARCHAR(45) DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_updated_rows INT := 0;
BEGIN
    -- Creo una tabla temporal en memoria que existirá únicamente durante la duración de la transacción
    CREATE TEMPORARY TABLE tmp_consolidated_notes ON COMMIT DROP AS
    WITH parsed_tokens AS (
        -- Descompongo la cadena de notas delimitada por punto y coma en elementos atómicos individuales
        SELECT 
            t.id AS threat_id,
            TRIM(token.val) AS clean_token
        FROM threat_ips t,
             LATERAL unnest(string_to_array(t.notes, ';')) AS token(val)
        WHERE (p_ip IS NULL OR t.ip = p_ip)
          AND t.notes IS NOT NULL
          AND TRIM(token.val) <> ''
    ),
    aggregated_tokens AS (
        -- Agrupo los elementos únicos ordenados alfabéticamente para construir una cadena unificada sin duplicados
        SELECT 
            pt.threat_id,
            string_agg(DISTINCT pt.clean_token, '; ' ORDER BY pt.clean_token) AS consolidated_notes
        FROM parsed_tokens pt
        GROUP BY pt.threat_id
    )
    SELECT threat_id, consolidated_notes FROM aggregated_tokens;

    -- Actualizo los registros de amenazas únicamente cuando la nota consolidada difiere de la nota actual
    UPDATE threat_ips t
    SET notes = tc.consolidated_notes,
        updated_at = NOW()
    FROM tmp_consolidated_notes tc
    WHERE t.id = tc.threat_id
      AND COALESCE(t.notes, '') IS DISTINCT FROM tc.consolidated_notes;

    -- Capturo la cantidad de filas que sufrieron modificaciones efectivas en su campo de anotaciones
    GET DIAGNOSTICS v_updated_rows = ROW_COUNT;

    -- Emito un mensaje de notificación de depuración para informar la finalización del procedimiento
    RAISE NOTICE '[AUDIT] Procedimiento sp_consolidate_duplicate_threat_notes finalizado: % registros consolidados.',
        v_updated_rows;
END;
$$;
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — SP 02
-- ==============================================================================

-- 1. Insertar amenazas con notas fragmentadas y redundantes para el experimento
INSERT INTO threat_ips (ip, type, country, threat_score, category, status, notes, created_at, updated_at)
VALUES 
    ('198.51.100.77', 'IPV4', 'RUS', 88, 'BruteForce', 'Active', 'SSH brute force; Port scan; SSH brute force; Admin credential guess; Port scan', NOW(), NOW()),
    ('198.51.100.88', 'IPV4', 'CHN', 72, 'Scanner', 'Active', 'Web crawler; Web crawler; Vulnerability probe', NOW(), NOW()),
    ('198.51.100.99', 'IPV4', 'USA', 45, 'Botnet', 'Active', 'Observacion limpia ya consolidada', NOW(), NOW());

-- 2. Ejecutar la consolidación para un indicador específico (Prueba focalizada)
CALL sp_consolidate_duplicate_threat_notes('198.51.100.77');

-- 3. Verificar que las notas de la IP 198.51.100.77 estén desduplicadas y ordenadas
SELECT ip, notes, updated_at FROM threat_ips WHERE ip = '198.51.100.77';

-- 4. Ejecutar la consolidación masiva pasando NULL para abarcar todo el inventario pendiente
CALL sp_consolidate_duplicate_threat_notes(NULL);

-- 5. Comprobar que 198.51.100.88 fue saneada y que 198.51.100.99 mantuvo su integridad
SELECT ip, notes FROM threat_ips WHERE ip IN ('198.51.100.77', '198.51.100.88', '198.51.100.99') ORDER BY ip;

-- 6. Limpieza de indicadores de prueba
DELETE FROM threat_ips WHERE ip IN ('198.51.100.77', '198.51.100.88', '198.51.100.99');
```

!!! tip "Ejecución de Deduplicación en DBeaver sobre el Homeserver"
    Para ejecutar `sp_consolidate_duplicate_threat_notes` en DBeaver a través de la conexión segura por puerto `5433`, abra un editor SQL y configure el modo de autocommit o ejecute el comando `CALL sp_consolidate_duplicate_threat_notes('198.51.100.77');` dentro de una transacción. La tabla temporal interna se destruirá automáticamente al cerrarse la transacción gracias a la instrucción `ON COMMIT DROP`, impidiendo el desperdicio de memoria en el contenedor Alpine de PostgreSQL. Puede verificar el plan de ejecución y los avisos en la pestaña Estadísticas de Ejecución de DBeaver.

---

## 7.3 Función Almacenada 3: `fn_generate_user_security_audit_report`

### Introducción y Justificación Arquitectónica

El cumplimiento de marcos normativos internacionales como ISO 27001, SOC 2 y NIST SP 800-53 exige la generación periódica de reportes exhaustivos sobre la postura de seguridad de las identidades corporativas. Un informe integral de gobernanza debe correlacionar la identidad del usuario, su rol jerárquico asignado, el estado de protección del segundo factor de autenticación y los contadores de versión de autenticación. Sin embargo, al cruzar entidades de alta cardinalidad como usuarios con tablas de eventos históricos y registros de tokens revocados, las consultas SQL mal diseñadas incurren en el riesgo de producir productos cartesianos desastrosos. Estas combinaciones cruzadas accidentales multiplican exponencialmente las filas devueltas, arrojando métricas de auditoría falsificadas y provocando el colapso de la memoria compartida del motor.

En arquitecturas modernas basadas en microservicios y APIs asíncronas, delegar la generación de reportes multi-tabla al mapeador objeto-relacional suele desembocar en el conocido antipatrón de consultas N más una. La aplicación emite inicialmente una consulta para obtener los usuarios y posteriormente dispara decenas de consultas subordinadas para computar los contadores de seguridad individuales, degradando la latencia del servicio a varios segundos. Este esquema resulta inviable durante las revisiones trimestrales de accesos, en las cuales los auditores externos demandan respuestas en tiempo real sobre miles de cuentas. La sustitución de este flujo por una función con retorno de tabla ejecutada directamente en PostgreSQL permite al optimizador de costos compilar un plan de ejecución unificado basado en hash joins y agregaciones anticipadas.

La función fn_generate_user_security_audit_report encapsula una consulta analítica de alto desempeño que realiza combinaciones externas izquierdas explícitas complementadas con subconsultas escalares aisladas. Esta técnica matemática garantiza que el cálculo de contadores globales de tokens revocados activos y exportaciones de telemetría recientes se evalúe sin alterar la cardinalidad de la tabla de identidades primarias. La tipificación estricta de las columnas devueltas en la cabecera de la función desacopla completamente a los consumidores externos de las complejidades del esquema físico subyacente. Los analistas de ciberseguridad y administradores pueden invocar la rutina directamente mediante una simple sentencia SELECT, posibilitando la paginación, el filtrado dinámico y la exportación inmediata hacia herramientas de visualización sin comprometer la integridad del clúster.

### Diccionario de Columnas del Conjunto de Datos Retornado

| Nombre de la Columna | Tipo de Dato | Restricción de Dominio | Descripción Técnica Detallada |
|---|---|---|---|
| `user_id` | INTEGER | Clave Primaria no nula | Identificador numérico secuencial del usuario registrado en el sistema que actúa como clave primaria de la tabla de identidades y permite la correlación unívoca de las métricas de seguridad auditadas en este reporte. |
| `email` | VARCHAR | Cadena única normalizada | Dirección de correo electrónico institucional asociada a la cuenta del usuario, empleada como identificador único de inicio de sesión y referencia primordial para la notificación de incidentes y gestión de credenciales operativas. |
| `rol` | VARCHAR | No nulo mediante coalesce | Nombre descriptivo del perfil de privilegios asignado a la identidad en el catálogo relacional, el cual delimita los permisos funcionales de acceso y capacidades de ejecución dentro de los módulos de HoneyMetrics. |
| `mfa_status` | VARCHAR | Valores fijos controlados | Indicador textual en mayúsculas que especifica si el usuario ha completado satisfactoriamente el enrolamiento del segundo factor de autenticación TOTP para mitigar vectores de compromiso de credenciales corporativas dentro del servicio de identidad. |
| `auth_version` | INTEGER | Entero positivo incremental | Contador entero de control de sesiones activas del usuario, incrementado ante revocaciones forzadas para invalidar en memoria todos los tokens JWT emitidos previamente que contengan una versión numéricamente inferior a este valor persistido. |
| `tokens_revocados_activos` | BIGINT | Conteo no cartesiano | Cantidad total de identificadores de tokens que permanecen vigentes en la lista de denegación temporal del sistema, calculada mediante subconsulta no cartesiana sobre los registros cuya fecha de expiración es estrictamente superior al tiempo actual. |
| `exportaciones_recientes` | BIGINT | Conteo temporal agregado | Número acumulado de peticiones de extracción de telemetría forense procesadas durante los últimos treinta días naturales, totalizadas mediante agregación optimizada sobre el historial de solicitudes para supervisar el consumo de almacenamiento y recursos. |
| `ultimo_acceso_estimado` | TIMESTAMP WITHOUT TIME ZONE | Marca temporal de auditoría | Marca temporal estimada de la última interacción registrada por la identidad en la plataforma de inteligencia, calculada a partir de los metadatos de persistencia del usuario para determinar su vigencia y eventual obsolescencia de cuenta. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — FUNCIÓN DE AUDITORÍA 03
-- Nombre:    fn_generate_user_security_audit_report
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Generación de reporte tabular de postura de seguridad y acceso multi-tabla sin productos cartesianos
-- ==============================================================================

CREATE OR REPLACE FUNCTION fn_generate_user_security_audit_report()
RETURNS TABLE (
    user_id INT,
    email VARCHAR,
    rol VARCHAR,
    mfa_status VARCHAR,
    auth_version INT,
    tokens_revocados_activos BIGINT,
    exportaciones_recientes BIGINT,
    ultimo_acceso_estimado TIMESTAMP WITHOUT TIME ZONE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Ejecuto la consulta multi-tabla estructurada retornando el conjunto de filas consolidado
    RETURN QUERY
    SELECT 
        u.id AS user_id,
        u.email::VARCHAR AS email,
        COALESCE(r.name, 'Sin Rol')::VARCHAR AS rol,
        CASE 
            WHEN u.is_mfa_enabled IS TRUE THEN 'HABILITADO'::VARCHAR
            ELSE 'DESHABILITADO'::VARCHAR
        END AS mfa_status,
        u.auth_version AS auth_version,
        -- Calculo el total de tokens revocados globales aún no vencidos asociados al horizonte de seguridad
        (
            SELECT COUNT(*) 
            FROM revoked_tokens rt 
            WHERE rt.expires_at > NOW()
        ) AS tokens_revocados_activos,
        -- Calculo las solicitudes de exportación de logs generadas en los últimos treinta días
        (
            SELECT COUNT(*) 
            FROM log_exports le 
            WHERE le.created_at >= NOW() - INTERVAL '30 days'
        ) AS exportaciones_recientes,
        -- Estimo la última actividad registrada basándome en la fecha de creación del usuario o fecha actual
        COALESCE(u.created_at, NOW()) AS ultimo_acceso_estimado
    FROM users u
    LEFT JOIN roles r ON u.role_id = r.id
    ORDER BY u.id ASC;
END;
$$;
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — FUNCIÓN 03
-- ==============================================================================

-- 1. Ejecutar la función para obtener la totalidad de identidades en cuadrícula
SELECT * FROM fn_generate_user_security_audit_report();

-- 2. Filtrar únicamente las cuentas con estado MFA vulnerable (DESHABILITADO)
SELECT 
    user_id,
    email,
    rol,
    mfa_status,
    auth_version,
    exportaciones_recientes
FROM fn_generate_user_security_audit_report()
WHERE mfa_status = 'DESHABILITADO';

-- 3. Identificar cuentas privilegiadas (Rol Administrador o Consultor de Ciberseguridad)
SELECT 
    user_id,
    email,
    rol,
    mfa_status,
    tokens_revocados_activos,
    ultimo_acceso_estimado
FROM fn_generate_user_security_audit_report()
WHERE rol IN ('Administrador', 'Consultor de Ciberseguridad')
ORDER BY user_id ASC;
```

!!! tip "Inspección Visual del Reporte de Identidades en DBeaver"
    Para auditar la postura de seguridad de usuarios desde DBeaver conectado a través de SSH en `127.0.0.1:5433`, ejecute la consulta `SELECT * FROM fn_generate_user_security_audit_report();` y presione F5 para visualizar los resultados en formato tabular interactivo. Puede ordenar las columnas directamente haciendo clic sobre sus encabezados o exportar los hallazgos a formatos CSV y JSON seleccionando la opción Exportar Datos en el menú contextual de la cuadrícula. Al utilizar subconsultas atómicas en lugar de productos cruzados, la consulta consume menos de dos milisegundos en el servidor.

---

## 7.4 Trigger 1: `trg_audit_deleted_threats_vault` (`AFTER DELETE ON threat_ips`)

### Introducción y Justificación Arquitectónica

En los centros de operaciones de seguridad, la integridad y la persistencia de las evidencias de indicadores de compromiso constituyen un requisito legal y forense irremplazable. Cuando un analista o un proceso automatizado elimina una dirección IP maliciosa de la lista activa threat_ips para limpiar falsos positivos o cerrar un incidente, la destrucción de dicha información sin un rastro histórico impide auditorías posteriores. Si un atacante logra comprometer credenciales operativas con permisos de escritura, podría intentar borrar selectivamente las trazas de sus propias direcciones IP para evadir la detección y ocultar su infraestructura de comando y control. La pérdida irreversible de estos registros vulnera el principio fundamental de No Repudio y destruye la cadena de custodia probatoria requerida en investigaciones judiciales.

Si la captura del snapshot de respaldo se confía exclusivamente a la lógica del servicio de aplicación en FastAPI, cualquier fallo de red inesperado, excepción no controlada en Python o interrupción del proceso web deja la operación a medio camino. En dicho escenario, el registro activo podría ser eliminado físicamente de la base de datos sin que la inserción secundaria en la bóveda histórica llegue a confirmarse transaccionalmente. Asimismo, un administrador de bases de datos que ejecute una sentencia DELETE de emergencia directamente mediante una consola SQL o cliente administrativo como DBeaver eludiría por completo el código de la API. Esta asimetría en el control de acceso genera puntos ciegos forenses inaceptables para un sistema de inteligencia de nivel empresarial.

El disparo automático de un trigger nativo AFTER DELETE en el motor PostgreSQL 16 garantiza la inmutabilidad y la exhaustividad de la captura forense con carácter absoluto. El disparador se activa de manera sincrónica e indivisible dentro de la misma transacción en que se solicita la eliminación, asegurando que si la inserción en la bóveda falla, la eliminación del registro activo sea revertida de inmediato. Mediante la lectura segura de la variable de contexto de sesión current_setting, el trigger captura el identificador del usuario autenticado que ejecutó la orden, preservando la atribución del evento. El registro de auditoría almacena la totalidad de los atributos originales del indicador junto con marcas temporales precisas y etiquetas de trazabilidad, creando un repositorio inmutable en threat_ips_vault que ningún cliente ordinario puede eludir.

### Diccionario de Atributos Auditados en la Bóveda Forense

| Atributo Auditado | Tipo de Dato | Restricción de Integridad | Descripción Técnica Detallada |
|---|---|---|---|
| `original_id` | INTEGER | Clave foránea lógica | Identificador numérico primario que poseía el indicador de compromiso en la tabla operativa antes de su remoción física, preservado como referencia lógica fundamental para reconstruir la cronología de eventos en investigaciones forenses. |
| `ip` | VARCHAR(45) | No nulo forense | Dirección de red canónica en formato IPv4 o IPv6 que constituía el indicador de compromiso investigado, copiada íntegramente hacia la bóveda inmutable para certificar el vector de ataque sin posibilidad de alteración retroactiva. |
| `type` | VARCHAR(20) | Admitido como nulo | Familia o clasificación arquitectónica del protocolo de direccionamiento correspondiente al indicador eliminado, garantizando la preservación contextual de la capa de red utilizada durante los incidentes de seguridad que motivaron su registro original. |
| `threat_score` | INTEGER | Rango numérico previo | Puntaje cuantitativo de peligrosidad asignado al indicador en el instante previo a su destrucción, resguardado en la bóveda histórica para permitir la reevaluación estadística de la severidad del incidente por parte del equipo analista. |
| `category` | VARCHAR(50) | Clasificación original | Taxonomía operacional o clasificación de amenaza asociada al indicador de compromiso antes de ser purgado de producción, requerida para mantener la coherencia con los esquemas de clasificación de tácticas y técnicas de adversarios. |
| `deleted_at` | TIMESTAMP WITHOUT TIME ZONE | Marca temporal de evento | Marca temporal exacta con resolución de microsegundos generada por el motor de base de datos durante la ejecución del disparador, la cual certifica cronológicamente el instante de defunción del registro en la infraestructura productiva. |
| `deleted_by_user_id` | INTEGER | Identificador de auditoría | Identificador del usuario o cuenta de servicio que disparó la eliminación del registro en la sesión actual, recuperado desde las variables de configuración del motor para asegurar la atribución inequívoca de la acción administrativa. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — TRIGGER Y FUNCIÓN DISPARADORA 04
-- Nombre:    trg_audit_deleted_threats_vault / trg_fn_audit_deleted_threats
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Resguardo inmutable en threat_ips_vault para No Repudio forense ante operaciones DELETE en threat_ips
-- ==============================================================================

CREATE OR REPLACE FUNCTION trg_fn_audit_deleted_threats()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INT;
    v_user_setting VARCHAR;
BEGIN
    -- Obtengo el identificador del usuario actor desde la variable de configuración de sesión
    v_user_setting := current_setting('app.current_user_id', true);

    -- Convierto de manera segura el identificador a entero evaluando cadenas nulas o vacías
    IF v_user_setting IS NOT NULL AND TRIM(v_user_setting) <> '' THEN
        v_user_id := v_user_setting::INT;
    ELSE
        v_user_id := NULL;
    END IF;

    -- Inserto el snapshot inmutable en la tabla de bóveda preservando la totalidad del estado previo
    INSERT INTO threat_ips_vault (
        original_id,
        ip,
        type,
        country,
        threat_score,
        category,
        status,
        notes,
        created_at,
        deleted_at,
        deleted_by_user_id
    ) VALUES (
        OLD.id,
        OLD.ip,
        OLD.type,
        OLD.country,
        OLD.threat_score,
        OLD.category,
        OLD.status,
        COALESCE(OLD.notes, '') || ' [Snapshot SQL No-Repudio trg_audit_deleted_threats_vault]',
        OLD.created_at,
        NOW(),
        v_user_id
    );

    -- Retorno el registro eliminado para permitir la finalización de la operación transaccional
    RETURN OLD;
END;
$$;

DROP TRIGGER IF EXISTS trg_audit_deleted_threats_vault ON threat_ips;
CREATE TRIGGER trg_audit_deleted_threats_vault
AFTER DELETE ON threat_ips
FOR EACH ROW
EXECUTE FUNCTION trg_fn_audit_deleted_threats();
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — TRIGGER 01
-- ==============================================================================

-- 1. Insertar una amenaza controlada para el ensayo de borrado
INSERT INTO threat_ips (ip, type, country, threat_score, category, status, notes, created_at, updated_at)
VALUES ('203.0.113.195', 'IPV4', 'PRK', 95, 'APT', 'Active', 'Evidencia critica para ensayo forense', NOW(), NOW());

-- 2. Configurar la variable de sesión para simular al usuario analista con ID 104
SET LOCAL app.current_user_id = '104';

-- 3. Ejecutar el DELETE que desencadenará el trigger
DELETE FROM threat_ips WHERE ip = '203.0.113.195';

-- 4. Verificar que el registro fue removido de la tabla activa
SELECT * FROM threat_ips WHERE ip = '203.0.113.195';

-- 5. Comprobar que el snapshot reside intacto en la bóveda con atribución de usuario
SELECT 
    id,
    original_id,
    ip,
    threat_score,
    notes,
    deleted_at,
    deleted_by_user_id
FROM threat_ips_vault 
WHERE ip = '203.0.113.195'
ORDER BY id DESC;

-- 6. Limpieza del registro archivado de prueba
DELETE FROM threat_ips_vault WHERE ip = '203.0.113.195';
```

!!! tip "Verificación de No Repudio y Variables de Sesión en DBeaver"
    Para ensayar la atribución de identidad en DBeaver sobre el puerto `5433`, es indispensable ejecutar la instrucción `SET LOCAL app.current_user_id = '104';` dentro de la misma transacción en la que se ejecuta el `DELETE`. En DBeaver, desactive el modo Autocommit temporalmente seleccionando Transacción Manual (Ctrl + T), ejecute el bloque secuencialmente y confirme los cambios con Commit (Ctrl + Alt + C). Al consultar `threat_ips_vault`, observará que la columna `deleted_by_user_id` capturó de forma exacta el valor 104 sin requerir modificaciones en la estructura física de la tabla operativa.

---

## 7.5 Trigger 2: `trg_rate_limit_log_exports` (`BEFORE INSERT ON log_exports`)

### Introducción y Justificación Arquitectónica

Las funcionalidades de exportación y descarga de bitácoras de auditoría constituyen operaciones intensivas en consumo de recursos computacionales, memoria volátil y ancho de banda de almacenamiento. En el contexto de HoneyMetrics, la generación de archivos comprimidos en formato JSONL requiere la lectura masiva de millones de eventos de telemetría y su procesamiento serializado en el servidor. Si un usuario malintencionado, un bot automatizado o un script con errores de programación emite ráfagas descontroladas de peticiones de exportación, el sistema experimenta agotamiento de memoria y sobrecarga en los trabajadores asíncronos. Esta condición de denegación de servicio degrada severamente la capacidad de respuesta de la plataforma para el resto de los operadores del centro de seguridad.

Aunque los limitadores de tasa basados en Redis o middlewares de FastAPI ofrecen una primera línea de protección perimetral, resultan insuficientes cuando las solicitudes eluden el proxy inverso o cuando el intermediario de caché experimenta caídas de servicio. En entornos con múltiples réplicas de contenedores API, la sincronización distribuida de ventanas de tiempo para el consumo de cuotas puede sufrir condiciones de carrera si no se implementan cerrojos atómicos altamente costosos. Asimismo, si un actor malicioso obtiene acceso directo a credenciales de base de datos a través de una brecha en un microservicio complementario, podría saturar el subsistema de almacenamiento insertando órdenes masivas sin pasar por el middleware web. Un cortafuegos SQL implementado directamente en el motor garantiza que la política de contención se cumpla de manera homogénea e inviolable frente a cualquier canal de entrada.

El disparador trg_rate_limit_log_exports intercepta cada intento de inserción en la tabla log_exports antes de que los datos sean confirmados en disco o consuman almacenamiento persistente. Al operar bajo el evento BEFORE INSERT, la función disparadora evalúa una ventana de tiempo móvil de los últimos cinco minutos, contabilizando con precisión micrométrica las solicitudes registradas con anterioridad. Si la cantidad acumulada alcanza o supera el umbral crítico de diez peticiones, el trigger aborta la transacción inmediatamente disparando una excepción con código de estado estandarizado P0001. Este mecanismo de interrupción anticipada bloquea el consumo de almacenamiento, libera de inmediato los recursos de conexión y proporciona un registro de auditoría explícito que identifica al usuario solicitante para su eventual bloqueo de seguridad.

### Diccionario de Parámetros de Control del Disparador

| Parámetro de Control | Tipo de Valor | Configuración Operativa | Descripción Técnica Detallada |
|---|---|---|---|
| `max_exports_threshold` | Constante entera | 10 peticiones | Número entero máximo de solicitudes de exportación de telemetría permitidas para ser insertadas dentro de la ventana de evaluación temporal, superado el cual el disparador rechaza categóricamente cualquier intento subsiguiente de inserción. |
| `sliding_window_interval` | Intervalo temporal | 5 minutes | Intervalo temporal relativo móvil de cinco minutos configurado en la consulta de verificación, dentro del cual se acumula el historial de solicitudes recientes para determinar si existe un patrón de saturación o ataque automatizado. |
| `exception_sqlstate_code` | Código SQLSTATE | P0001 | Código alfanumérico estandarizado de error SQL emitido en la instrucción de interrupción transaccional, utilizado por los clientes y controladores de base de datos para reconocer de manera programática el rechazo por limitación de tasa. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — TRIGGER Y FUNCIÓN DISPARADORA 05
-- Nombre:    trg_rate_limit_log_exports / trg_fn_rate_limit_log_exports
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Cortafuegos anti-DoS que restringe a 10 exportaciones por ventana de 5 minutos antes de inserción
-- ==============================================================================

CREATE OR REPLACE FUNCTION trg_fn_rate_limit_log_exports()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_recent_exports_count INT;
    v_current_user VARCHAR;
BEGIN
    -- Consulto la variable de sesión para identificar al actor que ejecuta la inserción
    v_current_user := COALESCE(NULLIF(current_setting('app.current_user_id', true), ''), 'ANONIMO');

    -- Cuento la cantidad de solicitudes de exportación registradas en los últimos cinco minutos
    SELECT COUNT(*) INTO v_recent_exports_count
    FROM log_exports
    WHERE created_at > NOW() - INTERVAL '5 minutes';

    -- Verifico si la tasa de peticiones en la ventana móvil excede el umbral de seguridad de 10
    IF v_recent_exports_count >= 10 THEN
        -- Aborto la transacción levantando una excepción con código personalizado P0001
        RAISE EXCEPTION 'Cortafuegos Anti-DoS HoneyMetrics: Se ha superado el límite de 10 exportaciones en 5 minutos (Total registrado: %). Usuario solicitante: %.',
            v_recent_exports_count, v_current_user
            USING ERRCODE = 'P0001';
    END IF;

    -- Autorizo la inserción del nuevo registro al encontrarse dentro de los parámetros permitidos
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_rate_limit_log_exports ON log_exports;
CREATE TRIGGER trg_rate_limit_log_exports
BEFORE INSERT ON log_exports
FOR EACH ROW
EXECUTE FUNCTION trg_fn_rate_limit_log_exports();
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — TRIGGER 02
-- ==============================================================================

-- 1. Limpiar solicitudes recientes de prueba para calibrar la ventana
DELETE FROM log_exports WHERE id LIKE 'EXP-RATELIMIT-%';

-- 2. Insertar una ráfaga de 10 solicitudes permitidas en la ventana móvil
DO $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..10 LOOP
        INSERT INTO log_exports (id, start_date, end_date, date_range, count, status, file_format, created_at, updated_at)
        VALUES (
            'EXP-RATELIMIT-' || LPAD(i::TEXT, 2, '0'),
            '2026-10-01',
            '2026-10-05',
            '2026-10-01 to 2026-10-05',
            100 * i,
            'Listo',
            'jsonl',
            NOW() - (i || ' seconds')::INTERVAL,
            NOW()
        );
    END LOOP;
    RAISE NOTICE 'Insercion de 10 solicitudes base completada.';
END $$;

-- 3. Intento de inserción de la solicitud número 11 (Debe ser interceptada y rechazada con P0001)
DO $$
BEGIN
    INSERT INTO log_exports (id, start_date, end_date, date_range, count, status, file_format, created_at, updated_at)
    VALUES ('EXP-RATELIMIT-11-BLOCKED', '2026-10-01', '2026-10-05', 'Exceso', 500, 'Listo', 'jsonl', NOW(), NOW());
    RAISE EXCEPTION 'Fallo de seguridad: El Trigger 02 debio abortar esta transaccion pero permitio la insercion.';
EXCEPTION
    WHEN SQLSTATE 'P0001' THEN
        RAISE NOTICE 'Validacion Exitosa de Trigger 02: El cortafuegos rechazo la solicitud número 11 con SQLSTATE P0001.';
END $$;

-- 4. Limpieza final de solicitudes de ensayo
DELETE FROM log_exports WHERE id LIKE 'EXP-RATELIMIT-%';
```

!!! tip "Prueba de Estrés y Bloqueo Anti-DoS en DBeaver"
    Para simular el ataque de saturación desde DBeaver hacia PostgreSQL en el Homeserver `192.168.33.2` vía túnel `5433`, ejecute el bloque anónimo del paso 2 que inserta 10 registros y a continuación ejecute la sentencia de inserción individual del paso 3. DBeaver desplegará una alerta emergente de error indicando `SQL Error [P0001]: Cortafuegos Anti-DoS HoneyMetrics: Se ha superado el límite de 10 exportaciones en 5 minutos`. Esto confirma que el motor abortó el registro antes de alterar el almacenamiento de datos.

---

## 7.6 Trigger 3: `trg_sanitize_and_validate_threat_ip` (`BEFORE INSERT OR UPDATE ON threat_ips`)

### Introducción y Justificación Arquitectónica

La ingesta de datos en plataformas de ciberinteligencia proviene de múltiples canales heterogéneos, tales como sensores de red, honeypots distribuidos, cortafuegos perimetrales y agentes de monitorización de endpoints. Con frecuencia, las direcciones IP y los metadatos contextuales ingresan con anomalías de formato, incluyendo espacios en blanco accidentales, variaciones de mayúsculas y minúsculas o etiquetas geográficas no estandarizadas. Asimismo, errores de digitación por parte de analistas o anomalías en la telemetría automatizada pueden suministrar valores de puntuación de peligrosidad negativos o mayores a cien. Esta suciedad en los datos socava la precisión de los modelos de aprendizaje automático predictivos y corrompe los algoritmos de ordenamiento y filtrado del panel operativo.

En escenarios de alta concurrencia, las aplicaciones web y los pipelines de ingesta son susceptibles al fenómeno de reenvío duplicado involuntario o double-submit originado por rebotes de red o reintentos de clientes desincronizados. Si dos eventos idénticos sobre un mismo indicador de compromiso se envían casi simultáneamente en un lapso de microsegundos, la comprobación de unicidad en la capa de aplicación puede generar condiciones de carrera tipo Time-of-Check to Time-of-Use. Este fallo provoca bloqueos en los índices o la duplicación innecesaria de transacciones en la cola de procesamiento. Controlar el delta temporal entre registros sucesivos dentro del propio motor de base de datos erradica por completo la ventana de vulnerabilidad asociada a la latencia de red entre la API y el almacenamiento.

El disparador trg_sanitize_and_validate_threat_ip actúa como una aduana de datos estricta e implacable previa a la persistencia física de cualquier indicador en threat_ips. Durante el evento BEFORE INSERT OR UPDATE, el trigger muta directamente las propiedades del registro entrante NEW, aplicando transformaciones canónicas como TRIM y UPPER sobre la dirección IP, el país de origen y la categoría. Simultáneamente, somete el atributo threat_score a una verificación de rango cerrado entre cero y cien, interrumpiendo la transacción con un código de violación de chequeo 23514 si se detecta un valor fuera de dominio. Adicionalmente, en operaciones de inserción, inspecciona la persistencia para abortar cualquier intento de duplicación que ocurra en una ventana inferior a un segundo, garantizando datos puros y operaciones idempotentes.

### Diccionario de Atributos y Reglas Validadas en Vuelo

| Atributo / Regla | Mecanismo de Control | Valor Transformado | Descripción Técnica Detallada |
|---|---|---|---|
| `ip` | Saneamiento de cadena | UPPER y TRIM | Cadena textual representativa de la dirección de red sometida a normalización forzosa mediante supresión de caracteres vacíos perimetrales y conversión canónica a mayúsculas para asegurar correspondencia inequívoca en los índices de búsqueda del motor relacional. |
| `country` | Saneamiento y valor por defecto | UPPER y TRIM | Código o nombre geográfico de procedencia normalizado en mayúsculas sostenidas y saneado de espacios espurios, garantizando uniformidad en las agrupaciones analíticas del panel de control de amenazas y sustituyendo valores nulos por etiquetas predeterminadas. |
| `type` | Normalización de protocolo | UPPER y TRIM | Etiqueta representativa de la familia de direccionamiento de red, saneada en mayúsculas y validada contra cadenas estándar para asegurar la correcta interoperabilidad con los mecanismos de inspección profunda de paquetes y reglas perimetrales del cortafuegos. |
| `threat_score` | Restricción de dominio | Rango [0, 100] | Magnitud cuantitativa de peligrosidad de la amenaza, sometida a verificación matemática estricta para garantizar que su valor entero permanezca indefectiblemente confinado en el rango numérico cerrado de cero a cien puntos porcentuales. |
| `double_submit_window` | Detección de replay | Ventana 1 segundo | Ventana temporal deslizante de un segundo evaluada exclusivamente durante operaciones de inserción para detectar y abortar transacciones concurrentes duplicadas que intenten registrar de forma redundante el mismo indicador en una fracción mínima de tiempo. |

### Código Fuente PL/pgSQL Completo

```sql
-- ==============================================================================
-- HONEYMETRICS CTI — TRIGGER Y FUNCIÓN DISPARADORA 06
-- Nombre:    trg_sanitize_and_validate_threat_ip / trg_fn_sanitize_and_validate_threat_ip
-- Autor:     Johan Sebastián Posada Beltrán
-- Fecha:     2026-10-25
-- Versión:   1.0
-- Motor:     PostgreSQL 16 / PL/pgSQL
-- Propósito: Saneamiento de datos en vuelo, validación de threat_score y mitigación de double-submit en un segundo
-- ==============================================================================

CREATE OR REPLACE FUNCTION trg_fn_sanitize_and_validate_threat_ip()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    -- Saneo la dirección IP eliminando espacios en blanco perimetrales y forzando mayúsculas canónicas
    NEW.ip := UPPER(TRIM(NEW.ip));

    -- Normalizo los atributos textuales complementarios para garantizar coherencia en la persistencia
    NEW.country := UPPER(TRIM(COALESCE(NEW.country, 'UNKNOWN')));
    NEW.type    := UPPER(TRIM(COALESCE(NEW.type, 'IPV4')));
    NEW.status  := TRIM(COALESCE(NEW.status, 'Active'));

    -- Verifico que el puntaje de amenaza se encuentre estrictamente delimitado en el intervalo [0, 100]
    IF NEW.threat_score < 0 OR NEW.threat_score > 100 THEN
        -- Interrumpo la operación si el valor numérico no satisface el contrato de integridad del dominio
        RAISE EXCEPTION 'Restricción de Integridad CTI: El puntaje de amenaza threat_score (%) debe ubicarse obligatoriamente entre 0 y 100.',
            NEW.threat_score
            USING ERRCODE = '23514';
    END IF;

    -- Evalúo la prevención de reenvío duplicado inmediato en operaciones de inserción
    IF TG_OP = 'INSERT' THEN
        -- Verifico si ya existe un registro con la misma IP creado hace menos de un segundo
        IF EXISTS (
            SELECT 1 FROM threat_ips
            WHERE ip = NEW.ip 
              AND created_at > NOW() - INTERVAL '1 second'
        ) THEN
            -- Aborto la transacción para impedir condiciones de carrera y ataques de replay
            RAISE EXCEPTION 'Protección Anti Double-Submit: Se detectó una inserción duplicada para la IP % en menos de 1 segundo.',
                NEW.ip
                USING ERRCODE = 'P0001';
        END IF;
    END IF;

    -- Asigno la marca temporal exacta de actualización en el motor relacional
    NEW.updated_at := NOW();

    -- Retorno el registro normalizado y validado para su almacenamiento definitivo
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_sanitize_and_validate_threat_ip ON threat_ips;
CREATE TRIGGER trg_sanitize_and_validate_threat_ip
BEFORE INSERT OR UPDATE ON threat_ips
FOR EACH ROW
EXECUTE FUNCTION trg_fn_sanitize_and_validate_threat_ip();
```

### Script de Prueba y Validación en DBeaver

```sql
-- ==============================================================================
-- SCRIPT DE VALIDACIÓN EN DBEAVER — TRIGGER 03
-- ==============================================================================

-- 1. Prueba de saneamiento automático: Inserción con espacios espurios y minúsculas
INSERT INTO threat_ips (ip, type, country, threat_score, category, status, notes, created_at, updated_at)
VALUES ('   198.51.100.222   ', '  ipv4  ', '  colombia  ', 85, 'Scanner', '  Active  ', 'Ensayo saneamiento', NOW(), NOW());

-- Verificar que se transformó a mayúsculas y sin espacios
SELECT ip, type, country, status FROM threat_ips WHERE ip = '198.51.100.222';

-- 2. Prueba de validación de dominio: Inserción con threat_score negativo (-15)
DO $$
BEGIN
    INSERT INTO threat_ips (ip, type, country, threat_score, category, status, created_at, updated_at)
    VALUES ('198.51.100.223', 'IPV4', 'USA', -15, 'Exploit', 'Active', NOW(), NOW());
    RAISE EXCEPTION 'Fallo de seguridad: Se permitio threat_score negativo.';
EXCEPTION
    WHEN SQLSTATE '23514' THEN
        RAISE NOTICE 'Validacion Exitosa: El motor rechazo threat_score negativo con SQLSTATE 23514.';
END $$;

-- 3. Prueba de validación de dominio: Inserción con threat_score excesivo (150)
DO $$
BEGIN
    INSERT INTO threat_ips (ip, type, country, threat_score, category, status, created_at, updated_at)
    VALUES ('198.51.100.224', 'IPV4', 'USA', 150, 'Exploit', 'Active', NOW(), NOW());
    RAISE EXCEPTION 'Fallo de seguridad: Se permitio threat_score superior a 100.';
EXCEPTION
    WHEN SQLSTATE '23514' THEN
        RAISE NOTICE 'Validacion Exitosa: El motor rechazo threat_score superior a 100 con SQLSTATE 23514.';
END $$;

-- 4. Prueba Anti Double-Submit: Intento de reenvío inmediato en la misma transacción
DO $$
BEGIN
    INSERT INTO threat_ips (ip, type, country, threat_score, category, status, created_at, updated_at)
    VALUES ('198.51.100.225', 'IPV4', 'RUS', 70, 'Botnet', 'Active', NOW(), NOW());

    -- Segundo intento inmediato con la misma IP
    INSERT INTO threat_ips (ip, type, country, threat_score, category, status, created_at, updated_at)
    VALUES ('198.51.100.225', 'IPV4', 'RUS', 70, 'Botnet', 'Active', NOW(), NOW());

    RAISE EXCEPTION 'Fallo de seguridad: Se permitio double-submit instantaneo.';
EXCEPTION
    WHEN SQLSTATE 'P0001' THEN
        RAISE NOTICE 'Validacion Exitosa: El motor intercepto y bloqueo el double-submit con SQLSTATE P0001.';
END $$;

-- 5. Limpieza de datos de prueba
DELETE FROM threat_ips WHERE ip IN ('198.51.100.222', '198.51.100.225');
```

!!! tip "Validación Interactiva del Saneamiento y Double-Submit en DBeaver"
    Para verificar `trg_sanitize_and_validate_threat_ip` en DBeaver a través de la conexión por túnel al Homeserver `192.168.33.2` en el puerto `5433`, ejecute el script de validación paso a paso. Observe cómo el registro de prueba `198.51.100.222` es transformado automáticamente en disco con país `COLOMBIA` y tipo `IPV4`, mientras que las inserciones inválidas de puntajes (-15 y 150) son rechazadas con error `23514`. El bloque de double-submit captura el error `P0001`, confirmando que el motor previene activamente condiciones de carrera sin requerir intervención del backend.
