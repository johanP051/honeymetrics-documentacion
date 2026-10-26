# Guía de Despliegue en Ubuntu Server (Máquina Virtual / Homeserver)

Esta guía describe el procedimiento paso a paso para desplegar **HoneyMetrics v2.0** en una máquina virtual o servidor físico con **Ubuntu Server 22.04 / 24.04 LTS**, utilizando llaves de despliegue dedicadas (Deploy Keys) de SSH, Docker Compose multi-archivo con perfil de producción, aprovisionamiento de variables de entorno y Cloudflare Zero Trust Tunnel.

> **Ver también:**
> - [Guía de Despliegue Integral (guia-despliegue.md)](guia-despliegue.md) — Topología completa, requerimientos de hardware e inventario de variables.
> - [Manual Técnico (manual-tecnico.md)](manual-tecnico.md) — Arquitectura de 4 capas, contratos OpenAPI y Matriz de Localización de Cambios.
> - [Diccionario de Datos (diccionario-datos.md)](diccionario-datos.md) — Modelo físico relacional, matrices PoLP y PBAC.

---

## Índice

- [1. Configuración de Autenticación SSH (Deploy Key)](#1-configuracion-de-autenticacion-ssh-deploy-key)
- [2. Configuración de Variables de Entorno (.env)](#2-configuracion-de-variables-de-entorno-env)
- [3. Despliegue y Orquestación con Docker Compose](#3-despliegue-y-orquestacion-con-docker-compose)
- [4. Aprovisionamiento de Usuarios y Roles (RBAC Seed)](#4-aprovisionamiento-de-usuarios-y-roles-rbac-seed)
- [5. Publicación Segura con Cloudflare Zero Trust Tunnel](#5-publicacion-segura-con-cloudflare-zero-trust-tunnel)
- [6. Troubleshooting y Operaciones Cotidianas](#6-troubleshooting-y-operaciones-cotidianas)

---

## 1. Configuración de Autenticación SSH (Deploy Key)

Para clonar y sincronizar el repositorio en el servidor sin comprometer tus credenciales personales de GitHub ni requerir tokens de acceso personal (PAT) con vigencia efímera, configuramos una **Deploy Key** enjaulada y de solo lectura.

### 1.1 Generar el par de llaves SSH dedicado
Ejecuta el siguiente comando en la terminal de tu servidor Ubuntu para crear una llave basada en el algoritmo moderno `Ed25519`:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_hm_v2 -C "servidor-produccion-honeymetrics"
```

* **`-t ed25519`**: Algoritmo de curva elíptica de alta resistencia criptográfica y huella reducida.
* **`-f ~/.ssh/id_ed25519_hm_v2`**: Ruta y nombre del archivo de clave privada para evitar colisiones con otras llaves existentes.
* **`-C "servidor-produccion-honeymetrics"`**: Comentario identificador en el panel de GitHub.
* *Nota:* Cuando solicite contraseña (*passphrase*), presiona `Enter` dos veces para omitirla (necesario para procesos automáticos de CI/CD).

Asegura los permisos POSIX del archivo de clave:
```bash
chmod 600 ~/.ssh/id_ed25519_hm_v2
chmod 644 ~/.ssh/id_ed25519_hm_v2.pub
```

### 1.2 Configurar el alias de Host en SSH
Edita o crea el archivo de configuración de SSH en el servidor:

```bash
vim ~/.ssh/config
```

Agrega el siguiente bloque de enrutamiento:

```text
Host github.com-hm-v2
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_hm_v2
    IdentitiesOnly yes
```

**¿Qué hace esta directiva?**
Le indica al cliente SSH del sistema operativo que cada vez que intente conectarse al host virtual `github.com-hm-v2`, enrute la conexión hacia `github.com` empleando el usuario `git` y autenticándose exclusivamente con la llave privada `~/.ssh/id_ed25519_hm_v2`.

### 1.3 Registrar la llave pública en GitHub
Imprime la llave pública en la consola:

```bash
cat ~/.ssh/id_ed25519_hm_v2.pub
```

1. Copia el texto emitido completo (`ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI_CLAVE_PUBLICA_COMPLETA servidor-produccion-honeymetrics`).
2. Dirígete en tu navegador a tu repositorio en GitHub:
   `https://github.com/johanP051/honeymetrics-backend` ➔ **Settings** ➔ **Deploy keys** ➔ **Add deploy key**.
3. **Title:** `Ubuntu Homeserver Producción` (o nombre de la máquina).
4. **Key:** Pega el bloque copiado.
5. Deja **desmarcada** la casilla *Allow write access* (Principio de Menor Privilegio para entornos de ejecución).
6. Haz clic en **Add key**.

### 1.4 Validar la autenticación SSH
Prueba el canal criptográfico ejecutando:

```bash
ssh -T git@github.com-hm-v2
```

Salida esperada de éxito:
```text
Hi johanP051/honeymetrics-backend! You've successfully authenticated, but GitHub does not provide shell access.
```

### 1.5 Clonar o reconectar el repositorio local

* **Caso A: Clonar por primera vez el proyecto en el servidor:**
  ```bash
  git clone -b main --single-branch git@github.com-hm-v2:johanP051/honeymetrics-backend.git
  cd honeymetrics-backend
  ```

* **Caso B: Si ya tenías el directorio pero fallaba `git pull`:**
  ```bash
  cd honeymetrics-backend
  git remote set-url origin git@github.com-hm-v2:johanP051/honeymetrics-backend.git
  git fetch origin
  git pull origin main
  ```

---

## 2. Configuración de Variables de Entorno (.env)

1. Dentro de la carpeta raíz del proyecto, inicializa el archivo `.env`:
   ```bash
   cp .env.example .env
   chmod 600 .env
   vim .env
   ```

2. **Generar la `SECRET_KEY` de producción:**
   Ejecuta el generador criptográfico en Python para obtener un secreto de alta entropía (50 caracteres URL-safe):
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
   Copia el resultado e inyéctalo en `.env`:
   ```env
   SECRET_KEY=tu_clave_aleatoria_generada_aqui
   ```

3. **Generar token anti-SSRF para Telegram Webhook:**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(16))"
   ```
   Inyéctalo en `.env`:
   ```env
   TELEGRAM_WEBHOOK_SECRET=tu_token_hex_aqui
   ```

4. **Configurar la política de dominios de correo institucional (`ALLOWED_EMAIL_DOMAINS`):**
   Para autorizar correos corporativos y cuentas verificadas de Google:
   ```env
   EMAIL_DOMAIN_POLICY=allowlist
   ALLOWED_EMAIL_DOMAINS=ucundinamarca.edu.co,gmail.com
   ```

5. **Política de Doble Factor de Autenticación (`MFA_ENABLED`):**
   * `MFA_ENABLED=True`: Activa la exigencia obligatoria del código dinámico TOTP (Google Authenticator) durante el login para cuentas enroladas.
   * `MFA_ENABLED=False`: Modo bypass para auditorías o pruebas de conectividad rápida. El backend aplicará *Fail-Closed* bloqueando nuevos enrolamientos y el frontend mostrará un banner de alerta preventiva.

6. **Optimización de Docker Compose mediante `.env`:**
   Descomenta o agrega las siguientes dos líneas al final de tu `.env`:
   ```env
   COMPOSE_FILE=docker-compose.yml:docker-compose.prod.yml
   COMPOSE_PROFILES=tunnel
   ```

   **¿Por qué hacemos esto?**
   Por defecto, `docker compose` solo lee `docker-compose.yml`. Al declarar `COMPOSE_FILE`, Compose fusiona automáticamente la configuración base con `docker-compose.prod.yml` (que activa 4 workers Uvicorn, limita memoria de PostgreSQL y desactiva puertos públicos en el host). Además, `COMPOSE_PROFILES=tunnel` levanta el contenedor de Cloudflare Tunnel sin necesidad de teclear banderas manuales.

---

## 3. Despliegue y Orquestación con Docker Compose

1. **Construir y levantar los servicios:**
   ```bash
   docker compose up -d --build
   ```

2. **Inspeccionar el estado de los contenedores:**
   ```bash
   docker compose ps
   ```
   Debes verificar que los 3 contenedores estén en estado saludable (`healthy` o `Up`):
   * `hm_api`: FastAPI Application Server (puerto interno 8000).
   * `hm_db`: PostgreSQL 16 Alpine (puerto interno 5432).
   * `hm_api_cloudflared`: Agente de túnel Zero Trust saliente.

3. **Verificar los registros de arranque en tiempo real:**
   ```bash
   docker compose logs -f api
   ```

> [!CAUTION]
> ### 🚨 Regla de Oro: Cómo recargar cambios en `.env` correctamente
>
> Ejecutar `docker compose restart api` **NO recarga los cambios realizados en `.env`**.
>
> **Explicación Técnica:** El comando `restart` envía una señal `SIGTERM` / `SIGKILL` al proceso del contenedor existente y lo reinicia, pero el demonio de Docker mantiene **congeladas** las variables de entorno inyectadas al momento de su creación.
>
> Para que el backend reconozca modificaciones en `.env` (como agregar `gmail.com` o alternar `MFA_ENABLED`), se debe recrear el contenedor sin reiniciar la base de datos:
> ```bash
> docker compose up -d --no-deps api
> ```

---

## 4. Aprovisionamiento de Usuarios y Roles (RBAC Seed)

Una vez que el contenedor de base de datos y la API están en ejecución, aprovisiona la cuenta de administración inicial:

```bash
docker compose exec api python -m scripts.create_user
```

El script interactivo solicitará:
1. **Email del usuario:** (Ej: `johan.posada0521@gmail.com` o `admin@ucundinamarca.edu.co`).
2. **Contraseña:** Mínimo 8 caracteres, mayúscula, minúscula, número y símbolo especial.
3. **Repita la contraseña.**
4. **Rol del usuario:** Presiona `Enter` para aceptar el valor por defecto `[Administrador]` o selecciona entre `Analista`, `Directivo de T.I.` o `Consultor de Ciberseguridad`.

El sistema sembrará automáticamente los roles canónicos en la tabla `roles` y asociará el usuario con sus permisos PBAC (*scopes*) correspondientes.

---

## 5. Publicación Segura con Cloudflare Zero Trust Tunnel

HoneyMetrics no requiere abrir puertos entrantes (Port Forwarding) en el enrutador físico ni exponer la IP pública de tu hogar o laboratorio.

1. En el panel de **Cloudflare Zero Trust** (Networks ➔ Tunnels), copia el token del túnel configurado para tu dominio.
2. Inyecta el token en tu `.env`:
   ```env
   CLOUDFLARE_TUNNEL_TOKEN=tu_token_cloudflare_zero_trust_aqui
   ```
3. Recrea el servicio del túnel:
   ```bash
   docker compose up -d --no-deps tunnel
   ```
4. Configura en el panel de Cloudflare la ruta pública:
   * **Subdominio:** `api-honey-master-homeserver.johan-d3v.site`
   * **Servicio:** `HTTP` hacia `api:8000` (resolución interna por nombre DNS de Docker).
5. Verifica el endpoint de salud desde internet:
   ```bash
   curl -I https://api-honey-master-homeserver.johan-d3v.site/health
   ```
   Salida esperada: `HTTP/2 200`.

---

## 6. Troubleshooting y Operaciones Cotidianas

### 6.1 Conflicto de puerto PostgreSQL (`5432:5432`)
* **Síntoma:** `Error response from daemon: driver failed programming external connectivity on endpoint hm_db: Bind for 0.0.0.0:5432 failed: port is already allocated`.
* **Causa:** El sistema operativo host ya tiene un servicio local de PostgreSQL corriendo en el puerto 5432.
* **Solución:**
  1. Detén el servicio local del host: `sudo systemctl stop postgresql`.
  2. O asegúrate de utilizar el perfil de producción (`docker-compose.prod.yml`), el cual mapea el puerto hacia `127.0.0.1:5433:5432` protegiendo la interfaz perimetral.

### 6.2 Error `Permission denied (publickey)` al ejecutar `git pull`
* **Solución:**
  1. Verifica que la llave tenga permisos seguros: `chmod 600 ~/.ssh/id_ed25519_hm_v2`.
  2. Comprueba que el host alias responda: `ssh -T git@github.com-hm-v2`.
  3. Revisa la URL remota del repositorio:
     ```bash
     git remote -v
     # Debe mostrar: git@github.com-hm-v2:johanP051/honeymetrics-backend.git
     ```

### 6.3 Backup en caliente de la Base de Datos
```bash
docker compose exec hm_db pg_dump -U usr_honeymetrics honeymetrics_v2 > backup_$(date +%Y%m%d_%H%M%S).sql
```
