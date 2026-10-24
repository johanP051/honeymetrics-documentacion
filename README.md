# 📚 HoneyMetrics Documentation — Single Source of Truth (SSOT)

Portal unificado y repositorio central de documentación técnica, arquitectura, manuales operativos, modelado UML, especificaciones ágiles y entregables académicos para la plataforma **HoneyMetrics v2.0**.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Docs-24292e?style=for-the-badge&logo=github&logoColor=white)](https://johanp051.github.io/honeymetrics-documentacion/)
[![MkDocs Material](https://img.shields.io/badge/MkDocs-Material%20v9.5-526CFE?style=for-the-badge&logo=materialformkdocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)
[![Mermaid.js](https://img.shields.io/badge/UML-36%20Diagrams-FF3670?style=for-the-badge&logo=mermaid&logoColor=white)](https://mermaid.js.org/)
[![DOCX Builder](https://img.shields.io/badge/DOCX-Academic%20Suite-2B579A?style=for-the-badge&logo=microsoftword&logoColor=white)](https://github.com/johanP051/honeymetrics-documentacion)

---

## 🌐 Enlace del Portal Desplegado

El portal oficial de documentación viva se compila y despliega de manera continua mediante GitHub Actions:

👉 **[https://johanp051.github.io/honeymetrics-documentacion/](https://johanp051.github.io/honeymetrics-documentacion/)**

---

## 🏛️ Estructura del Repositorio y SSOT

Para mantener la higiene arquitectónica del ecosistema HoneyMetrics, los repositorios de código ([`honeymetrics-backend`](https://github.com/johanP051/honeymetrics-backend) y [`honeymetrics-frontend`](https://github.com/johanP051/honeymetrics-frontend)) delegan toda la documentación formal a este repositorio centralizado.

```
honeymetrics-documentacion/
├── .github/workflows/
│   └── deploy-docs.yml         # CI/CD: Compilación y despliegue a GitHub Pages (OIDC)
├── docs/
│   ├── assets/
│   │   ├── screenshots/        # 11 capturas de pantalla reales en alta resolución (fig01..fig10)
│   │   └── videos/             # 5 videos 1080p Full HD grabados con Playwright y cursor dinámico
│   ├── index.md                # Presentación ejecutiva y visión del proyecto
│   ├── manual-tecnico.md       # Arquitectura Clean 5-capas, API REST, Service Layer y ML
│   ├── manual-usuario.md       # Manual operativo con videos interactivos, capturas y guías por rol
│   ├── diccionario-datos.md    # Esquema relacional, tablas, tipos, llaves y cardinalidades
│   ├── guia-despliegue.md      # Despliegue híbrido, Docker Compose, Nginx y Cloudflare Tunnels
│   ├── matriz-cambios.md       # Matriz de trazabilidad y gobernanza de código
│   ├── scrum/                  # Historias de Usuario, Criterios BDD y Definition of Done
│   ├── uml/                    # Catálogo de 36 diagramas UML v2.0 (Secuencia, Estados, Clases, Despliegue)
│   └── entregables_profesor/   # (Ignorado en git) Fuentes y compilados .docx para el Docente Oscar Gómez
├── scripts/
│   ├── build_entregables_docx.js # Compilador Headless de entregables Word con inserción de imágenes
│   └── capture_docs_media.py     # Script coreografiado de Playwright (cursor animado + grabación 1080p)
├── mkdocs.yml                  # Configuración temática MkDocs Material con soporte Mermaid y navegación fluida
└── README.md
```

---

## 🚀 Previsualización Local (MkDocs)

Para ejecutar el servidor de desarrollo local de MkDocs con recarga en vivo:

```bash
# Opción 1: Ejecución directa con pipx (sin contaminar entornos globales)
pipx run --spec mkdocs-material mkdocs serve

# Opción 2: Dentro de un entorno virtual Python
python3 -m venv .venv
source .venv/bin/activate
pip install mkdocs-material
mkdocs serve
```

El portal estará disponible de inmediato en `http://127.0.0.1:8000/`.

Para verificar la integridad de todos los enlaces y sintaxis con validación estricta:

```bash
pipx run --spec mkdocs-material mkdocs build --strict
```

---

## 📄 Compilación de Entregables Académicos (.docx)

Para generar los 4 documentos Word formales solicitados por la cátedra de Ingeniería de Software (UDEC):

```bash
# Requiere Node.js 18+ y la librería 'docx'
node scripts/build_entregables_docx.js
```

Los artefactos generados se almacenan localmente en `docs/entregables_profesor/`:
1. `01_Manual_Tecnico_HoneyMetrics_v2.docx`
2. `02_Diccionario_Datos_HoneyMetrics_v2.docx`
3. `03_Manual_Usuario_HoneyMetrics_v2.docx` (incluye las 11 figuras embebidas automáticamente)
4. `04_Manual_Tecnico_Frontend_HoneyMetrics_v2.docx`

---

## 🎬 Producción Multimedia Autónoma con Playwright

Las capturas y los videos demostrativos se generan de forma reproducible contra la aplicación local activa (`http://localhost:5173` y `http://localhost:8000`):

```bash
# Requiere python-playwright y ffmpeg
python3 scripts/capture_docs_media.py
```

El script ejecuta un cursor dorado interactivo (`#hm-cursor`), cadencia de interacción humana pedagógica y compresión web rápida (`-crf 18 -preset slow -pix_fmt yuv420p -movflags +faststart`).
