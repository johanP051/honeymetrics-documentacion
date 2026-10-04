# Guía de Despliegue y Puesta en Marcha

> **Ver también:**
> - [Matriz de Localización de Cambios](./matriz-cambios.md) — Para encontrar dónde modificar los puertos en el código fuente.

## 1. Topología de Red Recomendada
Para evitar colapsos de memoria y aislar los servicios, se requiere un esquema distribuido:
- **Nodo A (Sensor Perimetral / Honeypot):** Máquina de recursos bajos (Ej. Orange Pi 5) expuesta a internet.
- **Nodo B (Cerebro Central):** Servidor local (16GB RAM recomendados) que alojará la base de datos PostgreSQL, el backend en FastAPI y el indexador de Wazuh.

## 2. Preparación del Entorno (Backend)

Clonar el repositorio y configurar las variables de entorno para FastAPI:

```bash
cp .env.example .env
nano .env
```

Asegúrese de configurar los 4 pilares:
1. **PostgreSQL:** Credenciales del motor relacional.
2. **JWT Secret:** Llave criptográfica para los tokens de sesión.
3. **Telegram Webhook:** El `TELEGRAM_BOT_TOKEN`, el `ADMIN_TELEGRAM_CHAT_ID` y un secreto personalizado anti-SSRF para el Webhook.
4. **Wazuh Indexer:** Endpoint de OpenSearch (`WAZUH_INDEXER_URL`) y credenciales.

## 3. Despliegue con Docker Compose
Toda la suite central se levanta mediante un entorno orquestado:

```bash
# Construir la imagen del backend y levantar base de datos
docker-compose up -d --build
```

> [!WARNING]
> Nunca utilice el archivo `docker-compose.override.yml` en producción, ya que monta los volúmenes en caliente (Live Reload) exponiendo el código fuente.

## 4. Inicialización de Datos Semilla (DBA-Friendly)
Una vez levantada la base de datos, ejecute el seed de roles base y administrador:

```bash
docker exec -it honeymetrics-backend python scripts/seed_admin.py
```
Este script inyecta los roles canónicos (`Administrador`, `Analista de datos`, etc.) de manera segura e idempotente.
