# 🏗️ Diseño del Sistema — Arquitectura Polyrepo

> **Principio rector:** Separación estricta de responsabilidades. Ningún repositorio mezcla capas de otro.
> **Stack de decisión:** FastAPI (asíncrono nativo) + React 18 SPA. Django descartado por su naturaleza monolítica.
> **Fuente de datos:** 165.247 eventos reales de Wazuh Indexer | 5 meses | Abril — Agosto 2026

## 1. Visión General del Ecosistema

```mermaid
graph TD
    subgraph INTERNET["🌐 Internet / Atacantes"]
        ATK["🔴 Atacantes<br/>1.107 IPs únicas"]
    end

    subgraph EDGE["☁️ Capa de Borde (Cloudflare)"]
        CF["Cloudflare Tunnel<br/>TLS Termination + DDoS Protection"]
    end

    subgraph SERVER["🖥️ Servidor (Orange Pi 5 — 1GB RAM)"]
        direction TB
        NGINX["🔵 Nginx<br/>Reverse Proxy"]
        REACT["⚛️ React 18 SPA<br/>:80 → /"]
        API["⚡ FastAPI + Gunicorn<br/>:8000 → /api/ & /admin/"]
        PG["🐘 PostgreSQL<br/>Auth & Metadata"]
        WZ["🟠 Wazuh Indexer<br/>OpenSearch :9200"]
    end

    subgraph HONEYPOT["🍯 Honeypot (Orange Pi 5)"]
        HP["Agente Wazuh<br/>srvotsub1 / svm100"]
    end

    ATK --> HP
    HP --> WZ
    CF --> NGINX
    NGINX --> REACT
    NGINX --> API
    API --> PG
    API --> WZ
    
    %% PG y WZ no tienen puertos expuestos hacia NGINX o el host público.
```

## 2. Diagrama de Componentes Internos

```mermaid
graph LR
    subgraph FE["honeymetrics-frontend"]
        direction TB
        PAGES["📄 Pages<br/>/dashboard /threats /logs"]
        HOOKS["🪝 Custom Hooks<br/>useThreatCRUD, useAuth"]
        MOCKS["📦 Mocks Offline<br/>src/mocks/*.json"]
        UTILS["🛠️ Utils<br/>PdfGenerator.js (jsPDF)"]
        CTX["🔐 AuthContext<br/>JWT+RBAC"]
        
        PAGES --> HOOKS
        PAGES --> CTX
        PAGES --> UTILS
    end

    subgraph BE["honeymetrics-backend"]
        direction TB
        ROUTER["🚏 Thin Routers<br/>(<15 líneas)"]
        SERVICE["⚙️ Fat Services"]
        SCHEMA["📋 Pydantic v2<br/>Schemas"]
        DB["🗄️ SQLAlchemy ORM"]
        
        ROUTER --> SERVICE
        SERVICE --> SCHEMA
        SERVICE --> DB
    end

    subgraph DOCS["honeymetrics-documentacion"]
        direction TB
        BACKLOG["📋 Product Backlog"]
        HU["📖 HUs BDD"]
        ARCH["🗺️ Diagramas Mermaid"]
    end

    HOOKS -->|"HTTP /api/v1/"| ROUTER
    MOCKS -.->|"Contract-First (dev)"| HOOKS
```

## 3. Flujo de Autenticación JWT + 2FA

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant FE as React SPA
    participant BE as FastAPI
    participant DB as PostgreSQL
    participant TOTP as pyotp (TOTP)

    U->>FE: Ingresa credenciales + OTP
    FE->>BE: POST /api/v1/auth/login
    BE->>DB: SELECT usuario WHERE email=? (hash)
    DB-->>BE: Retorna usuario + rol + secret TOTP
    BE->>TOTP: pyotp.TOTP.verify(OTP)
    alt OTP Válido
        TOTP-->>BE: True
        BE-->>FE: { access_token, refresh_token, role }
        FE->>FE: Guarda token en localStorage
        FE-->>U: Redirige al dashboard por rol
    else OTP Inválido
        TOTP-->>BE: False
        BE-->>FE: 401 Unauthorized
        FE-->>U: Mensaje de error genérico (sin revelar campo fallido)
    end
```

## 4. Regla de Oro: Offloading de PDF (Protección de RAM)

El servidor Orange Pi 5 opera con **1GB de RAM compartida** entre Nginx, FastAPI con Gunicorn (workers), y el Wazuh Indexer. La generación de PDFs grandes en el servidor causaría OOM (Out of Memory) en producción. Esta es una **decisión arquitectónica irrevocable**.

```mermaid
flowchart LR
    A["👤 Analista hace clic<br/>en 'Generar PDF'"] --> B["⚛️ React — PdfGenerator.js<br/>jsPDF + AutoTable<br/>100% en navegador"]
    B --> C["📄 PDF generado<br/>Descarga automática al disco"]
    
    D["❌ FastAPI — PROHIBIDO<br/>No renderiza PDFs"]
    
    style B fill:#d4af37,color:#0d1117,stroke:#d4af37
    style D fill:#f85149,color:#e6edf3,stroke:#30363d
```

| Estrategia | Dónde se procesa | RAM del servidor consumida | Estado |
|---|---|---|---|
| PDF Client-Side (jsPDF) | Navegador del cliente | 0 MB adicional | ✅ Obligatorio |
| PDF Server-Side | FastAPI / Gunicorn | 200-500 MB por solicitud | 🚫 Prohibido |

## 5. Flujo de Datos: Threat Intelligence Center

```mermaid
sequenceDiagram
    autonumber
    actor Analista
    participant FE as React ThreatCenter
    participant Hook as useThreatCRUD Hook
    participant BE as FastAPI
    participant TS as ThreatService
    participant WZ as Wazuh Indexer

    Analista->>FE: Abre vista de Threat Intelligence Center
    FE->>Hook: useEffect() llama a fetchThreats()
    Hook-->>FE: isLoading: true (Muestra Skeleton)
    Hook->>BE: GET /api/v1/threats/summary
    BE->>TS: Thin Router delega a ThreatService
    TS->>WZ: Query OpenSearch de Aggregation
    WZ-->>TS: JSON (top IPs, volumen, severidad)
    TS->>TS: calculate_threat_score() por cada IP
    TS-->>BE: List[ThreatSummarySchema]
    BE-->>Hook: 200 OK + JSON
    Hook-->>FE: isLoading: false, data: [...]
    FE-->>Analista: Tabla renderizada con Badges APT/Botnet
```

## 6. Entornos de Despliegue

| Entorno | Archivo Docker Compose | Características Clave | Notas de Seguridad |
|---|---|---|---|
| **Desarrollo** | `docker-compose.override.yml` | Live Reload (Vite/Uvicorn), Mocks habilitados | Puertos internos expuestos para debug (`8000`, `5173`) |
| **Staging** | `docker-compose.yml` | Cloudflare Tunnel, datos reales limitados | Sin puertos expuestos al host público |
| **Producción** | `docker-compose.prod.yml` | Multi-Stage builds, Gunicorn con Uvicorn workers | Non-root users, TLS termination en CF |

> [!CAUTION]
> **Regla de seguridad explícita:** Las bases de datos (PostgreSQL, Wazuh Indexer) **JAMÁS** exponen puertos al host en `docker-compose.prod.yml`. El mapeo `5432:5432` o `9200:9200` está explícitamente prohibido. Solo Nginx expone los puertos necesarios internamente (o al host si CF Tunnel no lo absorbe).
