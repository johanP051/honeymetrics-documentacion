---
name: global-devops-deployment
description: >-
  Estándar de Infraestructura Híbrida y Despliegue Seguro para el ecosistema de Sebas:
  Estación Local (Exdrive), Homeservers Linux (192.168.33.2 / .31.235 / .32.11 / Orange Pi),
  Docker Non-Root, Nginx Hardening, Cloudflare Zero Trust Tunnels + Workers, Nube Estudiantil
  (Azure for Students / GCP Cost-Zero) y Kubernetes (k8s).
---

# 🚀 Hybrid Infrastructure, DevOps & Cloud-Native Deployment Standard

## 1. Topología de Hardware Conocida y Reglas de Ahorro de Recursos

El agente debe adaptar la configuración de contenedores y despliegue según el nodo destino elegido por el usuario:

1. **Estación Local de Desarrollo (`Laptop Linux` + Disco Externo `/media/sebas/Exdrive/Workspace`):**
   - **Regla Crítica de Montaje Externo:** En los archivos `docker-compose.yml` y `docker-compose.override.yml` de desarrollo local, configurar siempre `restart: "no"`. Nunca usar `restart: always` o `unless-stopped` en volúmenes atados a `/media/sebas/Exdrive/...`, ya que si el demonio de Docker inicia antes de que el disco externo se monte, creará directorios vacíos con propietario `root` rompiendo el punto de montaje.
   - Ideal para entrenamientos pesados de ML (aprovechando los 16 hilos de CPU) y pruebas E2E/Mobile QA.
2. **Homeservers de Laboratorio y Producción (`192.168.33.2` Staging, `192.168.31.235` Master, `192.168.32.11` SIEM/CTI, `Orange Pi 5` ARM):**
   - En nodos con RAM limitada (ej. `.31.235` o placas ARM), optimizar el consumo de memoria en `docker-compose.prod.yml` (`postgres -c shared_buffers=64MB -c work_mem=4MB -c max_connections=30`), limitar el número de workers de Uvicorn y permitir desactivar la carga de modelos pesados en RAM (`ML_ENABLED=False`) cuando el nodo actúe solo como API transaccional.
   - Usar **Deploy Keys SSH (`ed25519`) de solo lectura** por repositorio en `~/.ssh/config` para clonar y actualizar en los servidores sin exponer llaves personales globales.
   - **PROHIBIDO** incluir comandos destructivos con globs inversos (`rm -rf`, `mv !(...)`) sobre el directorio `~` del servidor en scripts `.sh` de despliegue.

### 1.1 Archivo Canónico `INFRASTRUCTURE.md` y Matriz Global de Puertos del Homelab (Pre-NetBox DCIM/IPAM)

Todo repositorio debe mantener en su raíz un archivo conciso `INFRASTRUCTURE.md` con sus puertos, dominios, Tunnel IDs y comandos de arranque, además de respetar la **Tabla Global de Puertos Ocupados del Homelab**:

| Nodo / Host | Rol / Propósito | Puertos Ocupados / Servicios |
| :--- | :--- | :--- |
| **`192.168.33.2`** | Nodo 1 Homeserver | `:22` (SSH), `:80` (`vuelos_frontend`), `:5432` (`vuelos_db_data`), `127.0.0.1:5433` (`hm_db` HoneyMetrics), `:6379` (`vuelos_redis`), `:8080` (`citas_api`) |
| **`192.168.31.235`** | Nodo 2 Laptop UDEC | `:9000` (Taiga Platform), stack `hm_v2_api` / `hm_v2_db` |
| **`192.168.32.11`** | Nodo SIEM / CTI | `:9200` (Wazuh Indexer), `:8443` (MISP), `:8090` (OpenCTI) |

- **Regla de Asignación:** Antes de asignar un puerto en cualquier proyecto nuevo, consultar `INFRASTRUCTURE.md` (o la instancia de **NetBox DCIM/IPAM** cuando esté desplegada).

---

## 2. Seguridad en Contenedores Docker y Nginx Hardening

1. **Dockerfiles Multi-Etapa y Usuario Non-Root Obligatorio:**
   - **Backend:** Compilar dependencias en etapa `builder` y ejecutar la etapa `runner` bajo usuario sin privilegios (`USER appuser`, UID `1001` o `10001`).
   - **Frontend:** Compilar estáticos con Node (`npm ci && npm run build`) y servir en etapa `runner` con `nginxinc/nginx-unprivileged:alpine` en puerto `8080` (mapeando `127.0.0.1:80:8080` en host si aplica).
2. **Aislamiento en `docker-compose.prod.yml` y Loopback-Only Port Binding para Bases de Datos:**
   - Forzar siempre explícitamente `ENVIRONMENT: "production"` y `DEBUG: "false"`.
   - **Prohibido exponer bases de datos en `0.0.0.0`** (ej. mapeos como `5432:5432`, `3306:3306`, `1433:1433`).
   - **Loopback-Only Port Binding (`127.0.0.1:<puerto_dedicado>:5432`):** Para permitir administración segura vía Túnel SSH (DBeaver) sin depender de IPs efímeras de contenedores Docker (`172.x.x.x`) ni chocar con otros proyectos en el mismo host, publicar el puerto atado **exclusivamente a loopback** en un puerto dedicado por proyecto (ej. `127.0.0.1:5433:5432` para HoneyMetrics cuando `5432` está ocupado por Vuelos).
3. **Cabeceras de Seguridad en Nginx (`nginx.conf`):**
   - Incluir `server_tokens off;`, `X-Frame-Options "DENY" always;`, `X-Content-Type-Options "nosniff" always;`, `Referrer-Policy "strict-origin-when-cross-origin" always;`, `Permissions-Policy "camera=(), microphone=(), geolocation=()" always;` y `Content-Security-Policy` estricto con `frame-ancestors 'none'`.
   - *Regla técnica de Nginx:* Recordar que cualquier bloque `location` que declare su propio `add_header` (ej. `Cache-Control` en `/assets/`) hereda cero `add_header` del bloque `server` padre, por lo que debe repetir o incluir las cabeceras de seguridad.

---

## 3. Cloudflare Zero Trust Tunnels (`cloudflared`) y Cloudflare Workers

1. **Prevención del Conflicto 502 por Doble Túnel:**
   - **NUNCA** usar el mismo `CLOUDFLARE_TUNNEL_TOKEN` simultáneamente en la laptop de desarrollo y en el homeserver de producción (provoca que Cloudflare balancee la mitad del tráfico público hacia el contenedor local apagado o en pruebas, causando errores `502 Bad Gateway` intermitentes).
   - Aislar siempre el servicio `cloudflared` bajo `profiles: ["tunnel"]`.
2. **Cero Tokens en Línea de Comandos (`ps aux` / `docker inspect`):**
   - En producción, queda **PROHIBIDO** usar `command: tunnel run --token ${CLOUDFLARE_TUNNEL_TOKEN}`.
   - Configurar `TUNNEL_TOKEN_FILE: /etc/cloudflared/token` montando el archivo local `.cloudflared_token` (ignorado en `.gitignore` y con permisos `chmod 600`) en modo solo lectura (`:ro`).
3. **Nomenclatura Estricta y Decodificación Base64 de Túneles Cloudflare:**
   - Nombrar todo túnel nuevo bajo el estándar `<proyecto>-<servicio>-<entorno>-<ubicacion>` (ej. `honeymetrics-api-prod-homeserver`).
   - Recordar que todos los `CLOUDFLARE_TUNNEL_TOKEN` de una misma cuenta empiezan con los mismos ~60 caracteres en Base64 porque codifican `{"a":"ACCOUNT_ID","t":"TUNNEL_ID","s":"SECRET"}`. Para diagnosticar a qué túnel apunta un `.env`, decodificar siempre el Base64 en Python e inspeccionar el campo `"t"`:
     ```python
     import base64, json
     # Rellenar padding Base64 y decodificar payload JSON
     payload = json.loads(base64.b64decode(token + '==='))
     print("Tunnel ID:", payload.get("t"))
     ```
4. **Cloudflare Workers / Pages para SPAs (React + Vite):**
   - En `wrangler.jsonc`, declarar siempre `"not_found_handling": "single-page-application"` dentro de `assets` (o incluir `public/_redirects` con `/* /index.html 200` en Cloudflare Pages) para evitar errores `404 Not Found` al recargar rutas de React Router.

---

## 4. Despliegues Remotos, Mantenimiento y Migraciones de Base de Datos

1. **Verificación Obligatoria de Migraciones Alembic en Despliegues Remotos:**
   - Todo despliegue o actualización de contenedor en el Homeserver debe verificar `docker exec <api_container> alembic current` y ejecutar `alembic upgrade head` (o `stamp` si proviene de un esquema legado) para impedir errores `HTTP 500 UndefinedColumn` en producción.
   - Comprobar en logs del contenedor API que la versión aplicada coincida con el último script de `alembic/versions/`.

---

## 5. Despliegue en Nube Estudiantil (Azure for Students / Google Cloud) y Kubernetes (k8s)

1. **Protección de Créditos en Azure for Students / GCP (*FinOps Estudiantil*):**
   - Priorizar servicios con capa gratuita o *Scale-to-Zero* (**GCP Cloud Run**, **Azure Container Apps**, **Cloudflare Workers**, **Supabase / Neon PostgreSQL Free Tier**) en lugar de dejar máquinas virtuales costosas o instancias gestionadas de base de datos encendidas 24/7 consumiendo el bono de $100 USD.
   - Si el docente exige una VM tradicional en Azure/GCP, usar tamaños elegibles en capa gratuita (`Standard_B1s` / `B1ls` en Azure o `e2-micro` en GCP) y configurar apagado automático nocturno (*Auto-shutdown*).
2. **Arquitectura Kubernetes-Ready (`k8s/`):**
   - Cuando el usuario o el docente solicite orquestación con **Kubernetes (k8s)**, generar los manifiestos limpios en la carpeta `k8s/`:
     - `deployment.yaml`: Con `replicas` ($\ge 2$), `securityContext` (`runAsNonRoot: true`, `runAsUser: 1001`, `readOnlyRootFilesystem`), límites de recursos (`requests` y `limits` de CPU/RAM) y sondas `readinessProbe` y `livenessProbe` apuntando a `/api/v1/health`.
     - `service.yaml` e `ingress.yaml`: Balanceo de carga interno (`ClusterIP`) y exposición perimetral.
     - `hpa.yaml` (*HorizontalPodAutoscaler*): Escalado automático entre 2 y 8 réplicas cuando el uso de CPU supere el `70%`.
