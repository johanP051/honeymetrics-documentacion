# Plan: Hoja 2 — Historias de Usuario + Mockups (Monolito + Advanced AI/ML)

## Descripción

Este plan detalla la generación de las **Historias de Usuario (Hoja 2)** y **Mockups** para HoneyMetrics v2.0.
Tras revisar el análisis estadístico exhaustivo de los 165.247 eventos reales de Wazuh, el plan se estructura en base a las **3 grandes evoluciones arquitectónicas (features "estrella")** que separan a HoneyMetrics de un simple visor de logs para convertirlo en una plataforma Enterprise:

1. **Rediseño de la Blacklist → Threat Intelligence Center:** Incorporando Threat Score (0-100) y Detección de Enjambres/Botnets por CIDR.
2. **Nuevo módulo correlacionado → Patch Intelligence Panel:** Cruzando CVEs críticos activos con FIM (File Integrity Monitoring) y Rootcheck con validación "Human-in-the-Loop".
3. **Nueva pantalla interactiva → Kill Chain Visualizer:** Trazabilidad completa basada en MITRE ATT&CK.

> [!TIP]
> **Compatibilidad con Claude y Excel:** Todos los entregables `.md` (Hoja 2) utilizarán una estructura semántica estricta (Listas Markdown de clave-valor). Esto garantiza que si le pasas los archivos a Claude, él pueda convertirlos en un archivo `.xlsx` perfecto en un solo prompt, sin que las celdas o saltos de línea se rompan.

---

## User Review Required

> [!IMPORTANT]
> **Nuevas Características Agregadas al Backlog (PB-HM-61 a PB-HM-70):**
> El backlog base original (SRS v6) no contemplaba los hallazgos reales. Se modificará `product_backlog_honeymetrics.md` para incluir:
> - **Threat Intelligence Center:** Threat Score, Agrupación CIDR (Botnets) y categorización (🤖 Bot automatizado >100ev/h vs 🧑 Ataque dirigido).
> - **Honeypot Advisor ("Esto buscan hoy"):** Análisis del diccionario SSH (ej. Odoo, Jenkins, Cripto).
> - **Patch Intelligence:** Priorización de 1.915 CVEs activos correlacionados con intentos de ataque.
> - **Human-in-the-Loop (HITL) para Rootcheck:** Flujo para que el analista valide si cambios en `/bin/passwd` son reales o falsos positivos.
> - **Heatmap de Riesgo Predictivo:** Identificación de patrones temporales (ej. Picos recurrentes 11-12 UTC).
> - **Kill Chain Visualizer:** Mapa visual del ataque.
> - **Dashboard de Compliance:** CIS Benchmark (ej. score estancado en 45%) con planes de remediación accionables.

> [!WARNING]
> **Ajuste de Prioridades:**
> - `PB-HM-54` y `PB-HM-55` (Hardware Monitor de Orange Pi) bajan a prioridad **Baja** para dar paso a las características de ML/IA que aportan valor de negocio real.

---

## Proposed Changes

### Componente 1 — Expansión del Product Backlog (Hoja 1)
#### [MODIFY] `product_backlog_honeymetrics.md`
- Reescribir el archivo agregando las historias de IA/ML bajo los nuevos PBs.
- Mantener la tabla Markdown estricta.

### Componente 2 — Mockups de IA (Diseño Fiel al Monolito)
Generaremos **9 Mockups PNG** inyectando los tokens extraídos del código de `global-theme.css` (GitHub Dark `#0d1117`, Cards `#161b22`, Dorado HoneyMetrics `#d4af37`). 
*Nuevos mockups agregados por el análisis:*
- `mockup_threat_intelligence.png` (Reemplaza a la vieja lista negra).
- `mockup_patch_intelligence.png` (Cruce CVE + FIM).
- `mockup_kill_chain_visualizer.png`.

### Componente 3 — Hoja 2: Sprint 1 (Auth + Usuarios + Threat Intel)
#### [NEW] `hu_sprint1_honeymetrics.md`
- ~65 Historias de usuario estructuradas.
- Flujos reales del monolito (animación globo 3D, OTP QR dinámico).
- El CRUD básico de IPs evoluciona a la base del **Threat Intelligence Center**.

### Componente 4 — Hoja 2: Sprint 2 (Dashboards + Botnets + Heatmap)
#### [NEW] `hu_sprint2_honeymetrics.md`
- ~70 Historias de usuario.
- Integración del **Heatmap de Riesgo Predictivo**, **Clasificador Bot vs Humano**, y **Honeypot Advisor**. Gráficos Plotly reales mapeados a HUs.

### Componente 5 — Hoja 2: Sprint 3 (Forense + Patch Intel + Compliance)
#### [NEW] `hu_sprint3_honeymetrics.md`
- ~60 Historias de usuario.
- Desglose BDD del **Patch Intelligence**, el flujo **Human-in-the-Loop** para FIM/Rootcheck, **Kill Chain Visualizer** y **CIS Compliance Panel**.

---

## Verification Plan

### Criterio de Éxito para Exportación a Excel
Formato lineal para la Hoja 2:
```markdown
### HU: PB-HM-61.1
- **Código PB Padre:** PB-HM-61
- **Actor:** Analista SOC
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista SOC quiero ver el Threat Score dinámico de una IP atacante para priorizar la respuesta ante Amenazas Persistentes.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que accedo al Threat Intelligence Center...
```

### Orden de Ejecución en `/agent`
1. Re-escribir `product_backlog_honeymetrics.md` (Integrando los nuevos PBs Enterprise).
2. Generar 9 Mockups de UI (Incluyendo Kill Chain y Patch Intel).
3. Generar `hu_sprint1_honeymetrics.md`.
4. Generar `hu_sprint2_honeymetrics.md`.
5. Generar `hu_sprint3_honeymetrics.md`.
6. Generar `README_backlog.md` (Índice maestro).

*Plan actualizado por Antigravity — Integrando Monolito, SRS v6 y Análisis Forense Real (165k eventos).*
