---
name: global-security-sast
description: >-
  Estándar enciclopédico de Seguridad de Aplicaciones (Omni-AppSec), SAST, OWASP Top 10 Web,
  OWASP API Security Top 10, OWASP ASVS L2/L3, CWE Top 25 y OWASP LLM Top 10. Opera en dos fases
  obligatorias: (Fase A) Reglas de Codificación Segura durante el desarrollo y (Fase B) Suite
  Exhaustiva de Pruebas de Seguridad y Pentesting Automatizado después de codificar.
---

# 🛡️ Global AppSec, SAST & Automated Pentesting Standard (Omni-AppSec)

Esta skill es de aplicación obligatoria en **dos momentos de cada tarea**:
- **FASE A (Mientras codificas):** Aplica los 12 Dominios de Codificación Segura desde la primera línea de código.
- **FASE B (Al terminar de codificar):** Ejecuta y escribe las pruebas de la **Batería de 10 Suites de Pentesting y Abuso** contra el código recién escrito. Ninguna tarea está terminada si solo tiene pruebas de "camino feliz" (*Happy Path*).

---

# 🛠️ FASE A: LOS 12 DOMINIOS DE CODIFICACIÓN SEGURA (PREVENTIVO)

## 1. Criptografía, Hashing, Gestión de Secretos y Entropía (OWASP A02)
- **MUST (Hashing de Contraseñas):** Usar exclusivamente **Argon2id** (preferido) o **bcrypt** (controlando explícitamente el truncamiento de 72 bytes o pre-hasheando con HMAC-SHA256). Prohibido usar MD5, SHA-1 o SHA-256 sin sal ni factor de trabajo para contraseñas.
- **MUST (Mitigación de Timing Enumeration en Login):** Cuando un correo/usuario no exista en la base de datos durante el login, ejecutar igualmente una verificación de hash ficticia (*dummy password hash verification*) antes de responder `401`, evitando que un atacante enumere cuentas midiendo la diferencia de milisegundos en la respuesta.
- **MUST (CSPRNG Exclusivo):** Prohibido usar `random` (Python) o `Math.random()` (JS) para tokens, contraseñas temporales, códigos OTP, sales, desafíos CSRF o IDs de recursos. Usar siempre `secrets` (Python) y `window.crypto.getRandomValues()` / `crypto.randomUUID()` (JS).
- **MUST (Cifrado en Reposo de Secretos en BD):** Toda semilla TOTP (`totp_secret` / `mfa_secret`), API Key de terceros o token OAuth almacenado en base de datos debe cifrarse simétricamente en reposo usando **AES-256-GCM** o **Fernet** con una llave maestra separada de la base de datos.
- **MUST (Comparación en Tiempo Constante):** Comparar todos los tokens, firmas HMAC, códigos de recuperación, webhooks y API keys usando `hmac.compare_digest(a, b)` o `crypto.timingSafeEqual()`.

## 2. Autenticación, MFA Atómico, OAuth2/OIDC y Sesiones (OWASP A07)
- **MUST (Validación Estricta de JWT):** Verificar firma criptográfica, algoritmo explícito en lista blanca (rechazar `alg: "none"` y confusión de llave pública RS256 usada como secreto HS256), expiración (`exp`), emisión (`iat`), sujeto (`sub`) e identificador único (`jti`).
- **MUST (Tokens de Paso Único Atómicos):** Todo `mfa_token` (`mfa_pending=True`), token de reseteo de clave o magic link **DEBE** ser de **uso único atómico** y corta duración ($\le 5\text{–}15\text{ min}$).
  1. Un `mfa_token` **DEBE** ser rechazado con `401` en cualquier endpoint distinto a `/auth/login/mfa-verify`.
  2. Al invocar `/mfa-verify`, el `jti` del `mfa_token` debe insertarse/consumirse en `revoked_tokens` (manejando `IntegrityError`) **ANTES** de evaluar `totp.verify()`. Si el código TOTP falla, el `mfa_token` queda quemado e inutilizable para reintentos.
- **MUST (Revocación en Eventos Críticos):** Al cambiar la contraseña, restablecer clave, desactivar usuario (`is_active=False`) o cambiar su rol, invalidar las sesiones/tokens previos. En frameworks basados en sesiones (Django), rotar el ID de sesión tras el login (`cycle_key()`) para prevenir *Session Fixation*.
- **MUST (OAuth2 / SSO):** Exigir `PKCE` (`code_challenge_method="S256"`), validar `state` aleatorio vinculado a la sesión contra CSRF y validar `redirect_uri` contra una lista blanca de URLs exactas.
- **MUST (Timestamps Uniformes):** Utilizar siempre `datetime.now(timezone.utc)` (UTC aware); prohibido mezclar `datetime.utcnow()` (naive) con fechas aware.

## 3. Autorización en Tiempo Real, Anti-IDOR (BOLA), Anti-Mass Assignment (BOPLA) y Multi-Tenancy (OWASP A01 / API1 / API3 / API5)
- **MUST (Revalidación en Servidor en Cada Request):**En `deps.py` (`get_current_user`), consultar primero el usuario en la base de datos, verificar `user.is_active == True`, y calcular los scopes efectivos en vivo desde su rol actual en BD (`get_scopes_for_role(user.role.name)`). Nunca confiar únicamente en la lista `scopes` estática dentro de un JWT antiguo.
- **MUST (Anti-IDOR / BOLA):** Toda consulta, actualización o descarga sobre un recurso identificado por ID (`/items/{id}`, `/logs/download/{id}`) **DEBE** comprobar pertenencia (`record.user_id == current_user.id`) o scope administrativo explícito.
- **MUST (Anti-Mass Assignment / BOPLA):**
  1. Prohibido pasar `request.json()` o `payload.model_dump()` directamente a un constructor o actualización ORM sin filtrar campos privilegiados (`role_id`, `is_superuser`, `is_staff`, `is_active`, `balance`, `status`).
  2. Configurar `model_config = ConfigDict(extra="forbid")` en esquemas de entrada sensibles y definir siempre `response_model` explícito en cada ruta para no filtrar columnas internas del ORM (`hashed_password`, `totp_secret`, `reset_token`).
- **MUST (Auto-Protección Administrativa):** Impedir con `400 Bad Request` que un administrador elimine su propia cuenta, se desactive a sí mismo, se quite el rol de `Administrador` o elimine el rol `Administrador`.
- **MUST (Aislamiento Multi-Tenant):** En sistemas multi-empresa, incluir `tenant_id` en todas las cláusulas `WHERE`, índices únicos y claves de caché Redis.

## 4. Validación de Entradas y Prevención Total de Inyecciones (OWASP A03)
- **MUST (SQLi & NoSQLi):** Usar consultas 100% parametrizadas u ORM. Si se requiere ordenar dinámicamente (`ORDER BY`), validar el nombre de la columna contra un diccionario/Enum cerrado de columnas permitidas; jamás interpolar strings del usuario en cláusulas SQL.
- **MUST (OS Command Injection):** Prohibido usar `os.system()`, ` subprocess.Popen(..., shell=True)` o ejecutar `ssh`/`rsync` desde procesos expuestos de la API web. Si un worker aislado invoca un binario, usar lista de argumentos `["binario", arg1]`, `shell=False`, `timeout` estricto y validar argumentos con regex de lista blanca (`^[a-zA-Z0-9_.-]+$`).
- **MUST (XSS & HTML Injection):** Escapar con `html.escape()` toda variable dinámica interpolada en correos HTML (`email_service.py`), reportes o plantillas.
- **MUST (CSV / Formula Injection — CWE-1236):** Al exportar datos a CSV o Excel (`.xlsx`), o al guardar textos que puedan exportarse (nombres, notas, razones), neutralizar cualquier celda cuyo valor comience con `=`, `+`, `-`, `@`, `\t` o `\r` (anteponiendo una comilla simple `'`).
- **MUST (ReDoS — Regular Expression DoS):** Evitar expresiones regulares con cuantificadores anidados ambiguos (`(a+)+$`) sobre entradas de usuario no acotadas; imponer siempre `max_length` antes de evaluar regex.
- **MUST (CRLF / Header & Log Injection):** Sanitizar saltos de línea (`\r`, `\n`) en nombres de archivos de cabeceras `Content-Disposition` y en entradas registradas en logs.

## 5. Seguridad de Archivos, Parsers, Deserialización y Path Traversal (OWASP A08 / CWE-22 / CWE-502)
- **MUST (Deserialización Segura y Sincronización de Hashes ML):**
  1. Prohibido invocar `joblib.load()`, `pickle.load()` o `yaml.load()` directamente.
  2. Usar siempre `safe_joblib_load()`, verificando el SHA-256 en streaming sobre el mismo descriptor de archivo antes de deserializar.
  3. Cuando un pipeline de reentrenamiento legítimo (`retrain_pipeline.py`) genere nuevos artefactos `.joblib` que superen la validación de no-degradación, debe actualizar atómicamente el manifiesto de hashes o el ciclo de `hot_reload()` rechazará los nuevos modelos.
- **MUST (Path Traversal & Zip Slip):** Resolver siempre la ruta real con `target = Path(base_dir, user_path).resolve()` y comprobar `target.relative_to(Path(base_dir).resolve())` antes de abrir, leer, escribir o borrar cualquier archivo.
- **MUST (Subida de Archivos y Parsers):** Limitar tamaño máximo en bytes, verificar *Magic Bytes* reales del contenido binario, prohibir `.svg`/`.html` inline, renombrar con `UUIDv4` fuera del webroot público y desactivar entidades externas XML (`resolve_entities=False` / `defusedxml`) para prevenir XXE.

## 6. Redes Salientes, Anti-SSRF, Validación Canónica de IPs y Webhooks (OWASP A10 / API7:2023)
- **MUST (Validación Canónica de Direcciones IP):** En toda validación de IPs externas (`ThreatCRUDService._validate_ip`, filtros de red, etc.):
  1. Parsear con `ip = ipaddress.ip_address(raw_ip.strip())`.
  2. Desempaquetar direcciones IPv6 con IPv4 mapeada: `effective_ip = ip.ipv4_mapped if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped else ip`.
  3. Rechazar con `422` si `effective_ip.is_loopback`, `is_private`, `is_link_local` (`169.254.0.0/16`, `fe80::/10`), `is_multicast`, `is_reserved`, `is_unspecified` (`0.0.0.0`, `::`) o `not effective_ip.is_global`.
  4. Evaluar la `WHITELIST` sobre `str(effective_ip)` y almacenar siempre la forma canónica.
- **MUST (Anti-SSRF en Peticiones Salientes):** Nunca hacer `requests.get(user_url)` sin validar esquema (`https`), resolver el DNS y comprobar que todas las IPs resueltas sean globales públicas (bloqueando metadatos cloud `169.254.169.254` y localhost), con `follow_redirects=False` y `timeout` estricto ($\le 15\text{s}$).
- **MUST (Anti-Spoofing de IP en Proxy):** En `get_real_client_ip`, ignorar `CF-Connecting-IP` y `X-Forwarded-For` a menos que `request.client.host` pertenezca a `settings.TRUSTED_PROXY_CIDRS`. Recorrer `X-Forwarded-For` de derecha a izquierda descartando saltos confiables hasta tomar la primera IP externa válida.
- **MUST (Webhooks Blindados):**
  1. Verificar firma/secreto en cabecera (`X-Telegram-Bot-Api-Secret-Token` o `signature.checksum` en Wompi) con `hmac.compare_digest`.
  2. En bots (Telegram), verificar que `str(chat_id) == str(settings.ADMIN_TELEGRAM_CHAT_ID)`.
  3. Validar ventana temporal del timestamp cuando el proveedor lo envíe y garantizar idempotencia sobre el ID del evento/transacción.

## 7. Concurrencia, Condiciones de Carrera (TOCTOU), Transacciones Financieras y Máquinas de Estado (CWE-362)
- **MUST (Bloqueo Pesimista en BD):** En cualquier flujo *Check-Then-Act* (ej. verificar stock y descontar, verificar estado `"Pendiente de Aprobación"` y pasar a `"Listo"`, o verificar saldo y transferir), bloquear el registro con `.with_for_update()` (`SELECT ... FOR UPDATE`) dentro de una transacción atómica.
- **MUST (Ordenamiento Anti-Deadlock):** Al bloquear múltiples filas en una misma transacción (ej. carrito de herramientas o lote de ítems), ordenar siempre los ítems por su clave primaria ascendente antes de iterar los bloqueos.
- **MUST (Precios y Cálculos en Servidor):** En pagos/e-commerce (`EstefChips`), usar enteros en centavos o `Decimal`, ignorar montos del cliente, firmar la intención de pago con `SHA-256(reference + amount_in_cents + currency + integrity_secret)` en el backend y verificar que el monto pagado en el webhook coincida exactamente con el total de la orden.
- **MUST (Escritura Atómica en Disco):** Al guardar archivos JSON/Parquet/WAL locales (`analyst_overrides.json`, `autopilot_history.json`, `.wal`), usar un `threading.Lock()`, escribir en un archivo temporal en el mismo directorio (`tempfile.mkstemp`), ejecutar `f.flush()` + `os.fsync(f.fileno())` y reemplazar atómicamente con `os.replace()`.

## 8. Seguridad en Frontend, Navegador, Cookies, CORS y Almacenamiento (OWASP A05)
- **MUST (Fail-Closed Absoluto en el Cliente):**
  1. Prohibido aceptar `mock-token` cuando `import.meta.env.DEV && import.meta.env.VITE_ENABLE_OFFLINE_MOCK === 'true'` sea falso.
  2. Prohibido que un bloque `catch` en `Login.jsx`, `AuthContext.jsx`, `Settings.jsx`, `AdminHub.jsx` o `useThreatCRUD.js` invente un perfil `Administrador`, inyecte `scopes: ['admin:all']` o agregue/edite/elimine registros falsos en el estado local de React en producción cuando la API devolvió error o está caída.
- **MUST (CORS Estricto):** Especificar lista explícita de orígenes en `BACKEND_CORS_ORIGINS`; jamás combinar `allow_origins=["*"]` con `allow_credentials=True`.
- **MUST (Cookies y CSRF):** Si se usan cookies de sesión/token, fijar `HttpOnly=True`, `Secure=True`, `SameSite="lax"` (o `"strict"`).
- **MUST (Prevención de Fuga por BFCache):** En respuestas de API con datos sensibles y al cerrar sesión (`logout`), limpiar tanto `localStorage` como `sessionStorage` y redirigir limpiamente.
- **MUST (Reconexión Limpia en Frontend y Telemetría Real en SIEM):** Cuando el backend vuelve a estar en línea o el usuario inicia sesión / pulsa `[Reconectar]`, limpiar inmediatamente `hm_use_mocks` del `localStorage` para no dejar al usuario atrapado en modo demostración, y en `LogsService` consultar siempre a Wazuh Indexer en vivo con paginación `search_after` (cero generadores sintéticos en producción).

## 9. Protección contra Denegación de Servicio (DoS), Event Loop, GraphQL y WebSockets (OWASP API4:2023)
- **MUST (Cotas en Todos los Esquemas Pydantic):**
  - Toda lista de entrada (`events`, `items`, `commands_sequence`, `history_events`, `unique_tokens`, `observed_ttps`) **DEBE** tener `Field(..., min_length=..., max_length=...)` (máx. 500 para lotes, máx. 200 para secuencias).
  - Todo `str` de entrada debe tener `max_length` (ej. `email <= 254`, `ip <= 45`, `notes <= 1000`, `command <= 2048`).
  - Todo `int`/`float` debe tener cotas lógicas (`ge`, `le`).
- **MUST (No Bloquear el Event Loop ASGI):**
  - En FastAPI, si un endpoint llama a funciones síncronas (consultas SQLAlchemy síncronas, `pandas`, `numpy`, `scikit-learn`, `lightgbm`, `hmmlearn`, `requests`), declararlo como `def` síncrono (para que corra en el *threadpool*) o usar `await loop.run_in_executor(None, ...)`.
  - Prohibido usar `time.sleep()` dentro de tareas en segundo plano o endpoints; usar `await asyncio.sleep()` si la función es `async`.
- **MUST (Rate Limiting Multi-Clave):** Aplicar `@limiter.limit(...)` en login, verificación MFA, recuperación de clave, registro de amenazas, solicitud de exportaciones y disparo de pipelines ML.

## 10. Seguridad en Machine Learning e IA Generativa / LLMs (OWASP LLM Top 10)
- **MUST (Zero-IP & Anti-Leakage en ML):** En modelos conductuales Session-First (`ml_v2`), rechazar con `ValueError` / `400 Bad Request` cualquier payload que contenga claves prohibidas de red (`FORBIDDEN_MODEL_FEATURES`: `ip`, `srcip`, `dstip`, `subnet`, `asn`, `country`, etc.) o patrones de secretos.
- **MUST (Desactivación por Defecto de Procesos Autónomos Pesados):** `ML_AUTOPILOT_ENABLED`, `ML_AUTOPILOT_ON_STARTUP` y `ML_REMOTE_SYNC_ENABLED` deben ser `False` por defecto en `config.py`.
- **MUST (Apps con LLMs / RAG):** Separar prompts de sistema de entradas del usuario, sanitizar salidas del LLM antes de renderizarlas en HTML o pasarlas a herramientas, usar usuarios de BD de solo lectura si hay consultas generadas por IA y fijar `max_tokens` + rate limit por usuario (*anti-Denial of Wallet*).

## 11. Configuración de Producción, Superficie Expuesta y Dependencias (OWASP A05 / A06)
- **MUST (Validación de Arranque en Producción):** En `config.py`, abortar el inicio si `ENVIRONMENT in {"staging", "production"}` y `SECRET_KEY` es vacía, menor de 32 caracteres o conserva el valor de ejemplo (`supersecretkey_change_in_production...`), o si `DATABASE_URL` usa superusuarios.
- **MUST (Ocultamiento de Documentación Interactiva en Producción):** Si `ENVIRONMENT in {"staging", "production"}` y `DEBUG is False`, desactivar `/docs`, `/redoc` y `/openapi.json` públicos (o protegerlos tras autenticación de superusuario).
- **MUST (Mantenimiento de Tablas de Seguridad):** Purgar periódicamente los tokens ya expirados (`expires_at < now`) de la tabla `revoked_tokens` para evitar crecimiento ilimitado en disco.
- **MUST (Higiene de `.env` y Prohibición de `.env.backup_*`):** Eliminar de los archivos `.env` cualquier bloque de variables obsoletas de motores antiguos (ej. variables `DB_PORT=3307` de MariaDB en proyectos PostgreSQL). Asegurar siempre en `.gitignore` las reglas `.env`, `.env.*`, `!.env.example`, `.cloudflared_token` y eliminar cualquier archivo `.env.backup_*` o `.env.swp` tras editar.

## 12. Logging Seguro, Trazabilidad Forense y Privacidad (OWASP A09)
- **MUST NOT:** Prohibido registrar contraseñas en texto plano, tokens JWT completos, semillas `totp_secret`, `IRIS_API_KEY`, `RESEND_API_KEY` o `TELEGRAM_BOT_TOKEN` en archivos de log o `print()`.
- **MUST:** Registrar en bitácora de auditoría quién ejecutó acciones destructivas (`deleted_by_user_id` en bóveda forense `ThreatIPVault` / `blacklist_audit_vault`).

---

# 🧪 FASE B: BATERÍA EXHAUSTIVA DE PRUEBAS DE SEGURIDAD POST-CÓDIGO (PENTESTING AUTOMATIZADO)

**REGLA DE CIERRE INNEGOCIABLE:** Cuando el agente termine de escribir o modificar código, **ANTES** de dar la tarea por finalizada, debe revisar su implementación ejecutando y/o agregando las pruebas correspondientes de las siguientes **10 Suites de Verificación de Seguridad**:

### Suite 1: Pruebas de Abuso de Autenticación y Ciclo de Vida de Tokens (`test_auth_security`)
- [ ] **1.1 Token ausente, malformado o expirado:** Enviar petición sin header `Authorization`, con token truncado, con `alg: "none"` y con `exp` en el pasado $\to$ `401 Unauthorized`.
- [ ] **1.2 Uso indebido de `mfa_token`:** Intentar usar un `mfa_token` (`mfa_pending: true`) como Bearer token para consultar `/users/me`, `/dashboard` o `/threats` $\to$ `401 Unauthorized`.
- [ ] **1.3 Quema de `mfa_token` al primer intento (Fallido o Exitoso):**
  - Iniciar login $\to$ obtener `mfa_token` $\to$ enviar código TOTP inválido (`000000`) $\to$ recibe `401`.
  - Reenviar el **mismo** `mfa_token` inmediatamente con el código TOTP válido actual (`pyotp.TOTP(secret).now()`) $\to$ **DEBE** recibir `401 Unauthorized` (prueba anti-fuerza bruta sobre MFA).
  - Reenviar un `mfa_token` ya usado exitosamente por segunda vez $\to$ **DEBE** recibir `401 Unauthorized` (prueba anti-replay).
- [ ] **1.4 Revocación efectiva en `/logout`:** Hacer login $\to$ llamar a `POST /auth/logout` con el Bearer token $\to$ intentar usar ese mismo token en `/users/me` $\to$ `401 Unauthorized`.
- [ ] **1.5 Anti-Enumeración en Recuperación de Clave (CWE-200):** Llamar a recuperación de contraseña con un correo existente y con uno inexistente $\to$ ambos deben devolver `200 OK` con idéntico mensaje JSON.
- [ ] **1.6 Cuenta suspendida (`is_active=False`):** Emitir un JWT válido para un usuario, cambiar `user.is_active = False` en BD e invocar un endpoint con ese JWT $\to$ `403 Forbidden`.

### Suite 2: Pruebas de Autorización Vertical, Horizontal (IDOR/BOLA) y Mass Assignment (`test_rbac_and_bola`)
- [ ] **2.1 Matriz Negativa Rol $\times$ Endpoint:** Probar cada endpoint protegido con un token de un rol que **no** tenga el scope requerido (ej. `Directivo` o `Operador` intentando `POST /threats-center/`, `DELETE /threats-center/{id}`, `POST /roles`, `GET /users` o `POST /ml/autopilot/trigger`) $\to$ `403 Forbidden`.
- [ ] **2.2 Revocación de Privilegios en Caliente (Persistencia cero en `deps.py`):** Emitir un JWT cuando el usuario tiene rol `Administrador`, actualizar su `role_id` en la base de datos a `Directivo` (o `Guest`), e invocar `GET /users` con el JWT viejo $\to$ **DEBE** ser rechazado con `403 Forbidden`.
- [ ] **2.3 Protección contra Auto-Eliminación / Auto-Suspensión:** Un administrador autenticado intenta hacer `DELETE /users/{su_propio_id}` o desactivar su propia cuenta $\to$ `400 Bad Request`.
- [ ] **2.4 Protección de Roles Críticos:** Intentar `DELETE /roles/{id_rol_administrador}` o eliminar un rol que aún tiene usuarios asignados $\to$ `400 Bad Request`.
- [ ] **2.5 Prueba Anti-Mass Assignment (BOPLA):** Enviar campos extra no permitidos o privilegiados en el JSON de entrada (ej. `{"ip": "1.2.3.4", "srcip": "1.2.3.4"}` en ML v2, o campos inesperados en actualización de perfil) $\to$ rechazo con `400`/`422` o ignorado seguro sin alterar columnas sensibles.

### Suite 3: Pruebas de Validación de Red, Anti-SSRF y Anti-Spoofing de Rate Limit (`test_network_and_ip_security`)
- [ ] **3.1 Anti-Spoofing de Cabeceras de Proxy:** Con `TRUSTED_PROXY_CIDRS = ["10.0.0.0/24"]`, simular una petición cuyo peer TCP es `203.0.113.20` (no confiable) enviando `CF-Connecting-IP: 198.51.100.7` y `X-Forwarded-For: 198.51.100.8` $\to$ `get_real_client_ip(request)` **DEBE** devolver `203.0.113.20`.
- [ ] **3.2 Resolución de Cadena de Proxies Confiables:** Con peer TCP `10.0.0.2` (confiable) y `X-Forwarded-For: 198.51.100.9, 10.0.0.3` $\to$ `get_real_client_ip(request)` **DEBE** devolver `198.51.100.9` (y si el header contiene basura como `"not-an-ip"`, hacer fallback seguro a `10.0.0.2`).
- [ ] **3.3 Batería Completa de IPs Prohibidas y Mapeadas en IPv6 (Threat Center / Blacklist):**
  Verificar que `POST /threats-center/` y `PUT /threats-center/{id}` rechacen con `422 Unprocessable Entity` todas las siguientes entradas:
  - Loopback IPv4 e IPv6: `127.0.0.1`, `::1`, `::ffff:127.0.0.1`.
  - Privadas RFC 1918 y mapeadas: `10.0.0.1`, `192.168.1.1`, `172.16.0.1`, `::ffff:10.0.0.1`, `::ffff:192.168.1.1`.
  - Link-Local y Cloud Metadata: `169.254.169.254`, `fe80::1`.
  - Multicast, Reservadas y No Especificadas: `224.0.0.1`, `240.0.0.1`, `0.0.0.0`, `::`, `255.255.255.255`.
  - Whitelist en formato IPv4 e IPv6 mapeado: `8.8.8.8`, `8.8.4.4`, `1.1.1.1`, `1.0.0.1`, `::ffff:8.8.8.8`, `::ffff:1.1.1.1`.
  - Formatos malformados: `"999.999.999.999"`, `"http://1.2.3.4"`, `"1.2.3.4/24"`.

### Suite 4: Pruebas de Integridad Criptográfica de Artefactos ML y Gobernanza Zero-IP (`test_ml_security`)
- [ ] **4.1 Paridad de Manifiesto de Hashes:** Comprobar que todos los archivos listados en `app/ml/artifact_hashes.json` existan en disco y su SHA-256 coincida bit a bit.
- [ ] **4.2 Rechazo Pre-Deserialización ante Alteración (Mock de `joblib.load`):** Reemplazar `joblib.load` con un mock que lance `AssertionError("Nunca debió ejecutarse")`, pasar a `safe_joblib_load` un archivo cuyo contenido fue alterado en 1 byte o que no tiene hash en el manifiesto $\to$ debe lanzar `ValueError` y **confirmar que `joblib.load` nunca fue invocado**.
- [ ] **4.3 Invariante Zero-IP y Anti-Secretos en ML v2 / Shadow Mode:** Enviar payloads que incluyan claves prohibidas (`srcip`, `ip`, `country`, `asn`, `subnet_cidr`) o valores con tokens/claves privadas a `CanonicalEvent`, `CanonicalSession`, `SessionAnalysisRequest`, `ShadowEventPayload` y `ShadowInferenceWorker` $\to$ deben ser rechazados inmediatamente con `ValueError` / `400` / `422`.

### Suite 5: Pruebas de Concurrencia, Condiciones de Carrera (TOCTOU) e Idempotencia (`test_concurrency_and_idempotency`)
- [ ] **5.1 Consumo Concurrente de Token de Uso Único:** Ejecutar llamadas simultáneas a `consume_mfa_token` con el mismo `jti` $\to$ exactamente 1 debe retornar `True` y todas las demás `False`, quedando 1 sola fila en `revoked_tokens`.
- [ ] **5.2 Idempotencia en Webhooks y Spool WAL:** Enviar 2 veces el mismo evento de pago/webhook o el mismo `dedup_hash` $\to$ el sistema debe procesarlo exactamente 1 vez sin duplicar transacciones, descuentos de stock ni alertas.
- [ ] **5.3 Atomicidad en Escritura de Archivos:** Verificar que fallos simulados durante la escritura de overrides o archivos `.tmp` no corrompan el archivo destino existente ni sean leídos como confirmados (`.wal`) por lectores concurrentes.

### Suite 6: Pruebas de Webhooks y Autenticación de Sensores (`test_webhooks_and_ingest`)
- [ ] **6.1 Webhook de Telegram (`/logs/webhook/telegram`):**
  - Petición sin header `X-Telegram-Bot-Api-Secret-Token` o con secreto incorrecto $\to$ `403` / `503`.
  - Petición con secreto válido pero proveniente de un `chat.id` distinto a `ADMIN_TELEGRAM_CHAT_ID` $\to$ **DEBE** ser rechazada sin cambiar el estado de la exportación en BD.
- [ ] **6.2 Ingesta de Wazuh (`/ingest/wazuh/events`):**
  - Petición con `WAZUH_API_KEY` vacía en configuración $\to$ `503 Service Unavailable`.
  - Petición con `X-Wazuh-Token` incorrecto $\to$ `403 Forbidden`.

### Suite 7: Pruebas de Límites de Recursos, Fechas y Prevención de DoS (`test_dos_and_bounds`)
- [ ] **7.1 Cotas en Lotes ML y Secuencias:** Enviar lista vacía (`events: []`) y lista que supere el límite (`501` eventos) a los endpoints batch de ML $\to$ `422 Unprocessable Entity`.
- [ ] **7.2 Validación de Rangos de Fechas (`/logs/request-export` y `/threats/summary`):** Enviar `startDate > endDate`, fechas futuras o formatos inválidos $\to$ `400` / `422`.

### Suite 8: Pruebas de Cabeceras de Seguridad HTTP y Manejo de Errores 500 (`test_headers_and_errors`)
- [ ] **8.1 Verificación de Security Headers:** Comprobar en respuestas de la API la presencia exacta de `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin` y `Strict-Transport-Security`.
- [ ] **8.2 Cero Fuga de Stacktraces:** Simular un fallo inesperado en un servicio y verificar que la respuesta HTTP 500 no exponga trazas internas ni rutas del sistema de archivos.

### Suite 9: Pruebas de Seguridad en Frontend y Fail-Closed (`authSecurity.test.js` & UI Tests)
- [ ] **9.1 Validación de Tokens en Cliente:** Comprobar con `node --test` que `isTokenValid()` rechace `mock-token` cuando `allowOfflineDemo=false`, rechace tokens con `alg: "none"`, tokens sin firma (3er segmento vacío), tokens sin `exp` numérico y tokens expirados.
- [ ] **9.2 Extracción de Autorización:** Comprobar que `extractAuthAuthorization()` nunca infiera el rol a partir de `role_id: 1` ni del correo del usuario.
- [ ] **9.3 Fail-Closed ante Caída de Red:** Verificar que si `getMyProfileApi()` o `login()` fallan por error de red en modo producción, el frontend no asigne rol `Administrador` ni `scopes: ['admin:all']`.

### Suite 10: Escaneo SAST, Auditoría de Dependencias y Verificación de Invariantes en Código (Recibos RDD)
Antes de dar por finalizada la tarea, ejecutar y adjuntar el recibo de:
```bash
# 1. Escaneo SAST estático y auditoría de CVEs en dependencias
bandit -r app/ -ll -ii
pip-audit
npm audit --audit-level=moderate

# 2. Verificación de invariantes de código seguro (todos deben dar 0 hallazgos inseguros)
! grep -rn "joblib\.load(" app/ --exclude="ml_integrity.py"
! grep -rn "shell=True" app/
! grep -rn "Math\.random()" src/
! grep -rn "mock-token" src/ --exclude="authSecurity.js"
! grep -rn "dangerouslySetInnerHTML" src/
! grep -rn "detail=.*str(e)" app/api/
! grep -rn "\-\-token" docker-compose*.yml
```

### Criterio de Aprobación Final (Gate Pass)

Una tarea o Pull Request **SOLO** aprueba el Gate de Seguridad cuando:
1. Cumple los 12 Dominios de Codificación Segura (Fase A).
2. Pasa el 100% de las pruebas aplicables de las Suites 1 a 9 en `pytest` / `node --test` / `vitest` (Fase B).
3. Los escaneos e invariantes de la Suite 10 arrojan **0 vulnerabilidades** y **0 patrones prohibidos**.
