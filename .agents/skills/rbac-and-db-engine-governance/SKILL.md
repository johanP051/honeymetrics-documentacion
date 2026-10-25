---
name: rbac-and-db-engine-governance
description: >-
  Gobernanza de Control de Acceso en 2 Niveles (Matriz RBAC de Negocio + Roles de Motor SQL PoLP)
  y Estándar Docente para el diseño, codificación y prueba de Stored Procedures (SPs) y Triggers en DBeaver.
---

# 🔐 RBAC de Negocio, Seguridad de Motor SQL y Estándar de SPs/Triggers

## 1. Separación Estricta de Roles en 2 Niveles (Defensa en Profundidad)

### Nivel 1: Roles del Motor de Base de Datos (PostgreSQL / SQL Server / MariaDB)
- **MUST NOT:** Queda **PROHIBIDO** conectar la aplicación en producción utilizando superusuarios del motor (`postgres`, `sa`, `root`).
- **MUST:** Diseñar y aprovisionar siempre 3 roles de base de datos bajo el Principio de Menor Privilegio (PoLP):
  1. `<app>_migrator`: Propietario del esquema. Ejecuta migraciones DDL (`CREATE`, `ALTER`, `DROP` vía Alembic o Django `migrate`), sin privilegios de `SUPERUSER` ni `sysadmin`.
  2. `<app>_runtime` (ej. `usr_honeymetrics`, `hm_app`, `usr_tantaustock`): Usuario con el que se conecta el backend en `.env`. Posee únicamente permisos DML (`SELECT, INSERT, UPDATE, DELETE`) sobre tablas operativas, y **solo `INSERT, SELECT`** (sin `DELETE` ni `UPDATE`) sobre tablas de bóveda forense (`*_vault`, `*_archive`), garantizando el **No Repudio** incluso si la aplicación web es vulnerada.
  3. `<app>_readonly`: Exclusivo `SELECT` para consultas analíticas o reportes externos.
- **MUST:** En `app/core/config.py`, validar en arranque que cuando `ENVIRONMENT in {"staging", "production"}`, la cadena `DATABASE_URL` no utilice el usuario `postgres`, `root` ni `sa`.
- **MUST (Script SQL Idempotente de Hardening PoLP — `scripts/hardening_db_roles_polp.sql`):**
  - Implementar la regla *"1 App = 1 Usuario Dedicado"* creando el usuario de aplicación (ej. `usr_honeymetrics`) con permisos estrictamente DML (`CONNECT`, `USAGE ON SCHEMA public`, `SELECT, INSERT, UPDATE, DELETE` en tablas, `USAGE, SELECT` en secuencias) y ejecutando explícitamente:
    ```sql
    REVOKE CREATE ON SCHEMA public FROM usr_<app>;
    ```
  - **Recibo RDD Obligatorio:** Comprobar con la sesión de `usr_<app>` que las consultas operativas funcionen (`SELECT 1 FROM threats;`) y que cualquier intento de modificación DDL (`CREATE TABLE test_should_fail (id int);`) aborte inmediatamente con:
    ```text
    ERROR: permission denied for schema public
    ```
- **MUST (Documentación Obligatoria de la Matriz Dual — Matriz A + Matriz B):**
  - Todo Diccionario de Datos y Manual Técnico debe incluir obligatoriamente:
    1. **Matriz A (Privilegios de Motor PostgreSQL):** Matriz que documenta los permisos a nivel de base de datos (`CONNECT`, `USAGE`, `CREATE`, `SELECT`, `INSERT`, `UPDATE`, `DELETE`) contrastando `postgres` (Superusuario DBA) vs `usr_<app>` (Backend Runtime PoLP) vs `<app>_migrator` (Migraciones DDL).
    2. **Matriz B (Control de Acceso Lógico PBAC):** Matriz que cruza los roles de negocio contra la totalidad de scopes granulares del JWT (`admin:all`, `threats:write`, `threats:read`, `users:manage`, `audit:read`, etc.).

### Nivel 2: Roles de Negocio de la Aplicación y Matriz RBAC/PBAC
- **MUST:** Antes de implementar permisos, definir con el usuario la **Matriz RBAC de Negocio** por Caso de Uso empleando la convención:
  - `✅` Permitido directamente
  - `❌` No permitido (El backend DEBE responder `403 Forbidden`)
  - `◐` Permitido bajo condición verificable (aprobación dual en Telegram, confirmación explícita o registro de auditoría)
  - `—` No corresponde a la responsabilidad principal
- **MUST (Equivalencia Canónica de Roles — `"Administrador"` $\leftrightarrow$ `"Superusuario"`):**
  - En `app/core/permissions.py` (`ROLES_TO_SCOPES` y `get_scopes_for_role`), mapear siempre tanto `"Administrador"` como `"Superusuario"` al bloque completo de scopes administrativos (`ALL_SCOPES` o `admin:all`).
  - Soportar e integrar las variaciones canónicas de nomenclatura para roles de negocio:
    - `"Directivo"` $\leftrightarrow$ `"Directivo de T.I."`
    - `"Analista"` $\leftrightarrow$ `"Analista de datos"`
    - `"Consultor"` $\leftrightarrow$ `"Consultor de Ciberseguridad"`
  - Garantizar que ningún token JWT, prueba automatizada o flujo de interfaz falle por utilizar indistintamente la nomenclatura técnica del código o la nomenclatura de los diagramas UML.
- **MUST (Separación de Funciones - SoD):** Consultar (`:read`), crear/editar (`:write`), eliminar definitivamente (`:delete`) y aprobar operaciones críticas (`:approve`) son capacidades distintas y **DEBEN** tener scopes separados.
- **MUST:** Mantener paridad 1 a 1 entre la tabla `ROLES_TO_SCOPES` del backend y los guardias de ruta (`RoleGuard`, `hasScope`) del frontend.

---

## 2. Estándar Académico para Procedimientos Almacenados (SPs) y Triggers

Cuando el proyecto tenga requerimiento académico de lógica en base de datos (típicamente **mínimo 3 a 5 SPs y 3 a 5 Triggers** según la rúbrica docente), el agente **DEBE**:

### 2.1 Selección Inteligente de Candidatos (Qué delegar al motor SQL)
Proponer al usuario candidatos que aporten valor real de integridad, rendimiento y seguridad sin contradecir la arquitectura de servicios:
- **Triggers Recomendados (Ineludibles incluso desde clientes SQL externos como DBeaver):**
  1. **Bóveda de Auditoría Forense y No Repudio (`AFTER DELETE`):** Captura el registro eliminado mediante `OLD`, serializa sus columnas en un objeto `JSON` / `JSONB` (`JSON_OBJECT()` en MySQL/MariaDB o `to_jsonb(OLD)` en PostgreSQL) y lo inserta en la tabla inmutable `*_audit_vault`.
  2. **Data Firewall & Rate Limiting Anti-Bot (`BEFORE INSERT`):** Cuenta las inserciones del mismo usuario en una ventana temporal corta (ej. últimos 1 o 5 minutos) y aborta la transacción con `SIGNAL SQLSTATE '45000'` (MySQL) o `RAISE EXCEPTION USING ERRCODE = 'P0001'` (PostgreSQL) si supera el umbral.
  3. **Prevención de Double-Submit y Saneamiento en Vuelo (`BEFORE INSERT OR UPDATE`):** Bloquea inserciones idénticas en ventanas de 5 segundos y normaliza campos (`NEW.country = UPPER(TRIM(NEW.country))`).
- **Stored Procedures (SPs) Recomendados (Procesamiento por Lotes y Cruces Pesados):**
  1. **Archiving y Purga Transaccional con Cursores y ACID:** Traslada registros vencidos (`expires_at < NOW()`) a tablas históricas usando `CURSOR`, `LOOP`, `START TRANSACTION`, `COMMIT` y `HANDLER FOR SQLEXCEPTION` / `EXCEPTION WHEN OTHERS THEN ROLLBACK`.
  2. **Consolidación y Deduplicación (*Merge & Purge*):** Utiliza tablas temporales en memoria (`CREATE TEMPORARY TABLE`) para agrupar registros duplicados, concatenar orígenes/eventos sin bloqueo prolongado y eliminar clones.
  3. **Reporte Consolidado de Auditoría Multi-Tabla:** Cruza 4 o 5 tablas relacionales usando `LEFT JOIN` sobre subconsultas pre-agregadas para evitar productos cartesianos.
  4. **Contingencia de Cifrado en Reposo:** Cifrado/descifrado condicional de columnas sensibles (`pgp_sym_encrypt` en PostgreSQL o `AES_ENCRYPT` en MySQL) verificando formato previo con expresiones regulares para evitar el doble cifrado.

### 2.2 Formato Obligatorio del Código SQL y Script de Pruebas para DBeaver
Todo SP y Trigger entregado para evaluación académica **DEBE** incluir sin excepción:
1. **Bloque de Encabezado Formal del Docente:**
   ```sql
   -- ========================================================================
   -- APLICACION      : [Nombre del Proyecto]
   -- OBJETIVO        : ¿Qué hace?: [Explicación clara]
   --                   ¿Para qué sirve?: [Beneficio de seguridad/rendimiento]
   --                   ¿Quién lo usaría?: [Backend / DBA / Tarea programada / Automático]
   --                   Partes del código útiles: [ACID / Cursores / OLD-NEW / Tablas Temp]
   --                   Funciones utilizadas: [Lista de funciones SQL nativas]
   --                   Variables: [Parámetros IN/OUT y variables locales]
   -- AUTOR           : [Nombre del Estudiante]
   -- FECHA           : AAAA/MM/DD
   -- ========================================================================
   -- MODIFICACIONES:
   -- | Fecha      | Autor            | Descripción del cambio
   -- ========================================================================
   -- | AAAA/MM/DD | [Autor]          | Creación inicial
   -- ========================================================================
   ```
2. **Comentarios Línea por Línea en Primera Persona:** Redactar los comentarios internos explicando cada paso en primera persona (*"-- Declaro las variables locales...", "-- Inicio la transacción para asegurar los principios ACID...", "-- Verifico si la cantidad supera el umbral..."*).
3. **Script de Pruebas Reproducible (`Script de Pruebas`):** Añadir después de cada rutina el bloque SQL exacto (`INSERT`, `SELECT` antes, `CALL`, `SELECT` después, y disparo intencional del error/alerta) listo para ejecutar en **DBeaver** y capturar las pantallas de evidencia.
