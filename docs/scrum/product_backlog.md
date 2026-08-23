# 📋 Product Backlog — HoneyMetrics v2.0 (Features CTI Avanzadas)

> **Materia:** Ingeniería de Software II (IS2) — UDEC Facatativá
> **Equipo:** Johan Sebastián Posada Beltrán · Juan Pablo Fonseca Celis · Manuel Alejandro Aldana Rincón
> **Fuente:** Análisis de 165.247 eventos reales Wazuh | SRS v6 (4.795 líneas)
> **Fecha:** Agosto 2026

> [!IMPORTANT]
> **Reglas del Profesor — Convención Obligatoria**
> - Código: `PB-HM-61` en adelante (continúa numeración del backlog base).
> - Perspectiva: **QUÉ** necesita el usuario, **nunca** el CÓMO técnico.
> - CRUD: cada operación = ítem separado.
> - Trazabilidad HU: `PB-HM-61.1`, `PB-HM-61.2` ... (Hoja 2 - HU).
> - Estado inicial: `Sin empezar`.
> - Prioridad: Alta / Media / Baja.
> - Fibonacci: 1, 2, 3, 5, 8, 13.

## Tabla de Product Backlog

| Código | Descripción (Lenguaje de Negocio) | Actor | Prioridad | Puntos | Estado |
|---|---|---|---|---|---|
| PB-HM-61 | Listar IPs registradas en el Intelligence Center con su Threat Score dinámico (0-100). | Analista | Alta | 8 | Sin empezar |
| PB-HM-62 | Identificar y alertar sobre ataques coordinados (Botnets) agrupando IPs por subred CIDR /24. | Analista | Alta | 5 | Sin empezar |
| PB-HM-63 | Clasificar a los atacantes como Bot (automatizado rápido) o Humano (dirigido lento) según su velocidad de ataque. | Analista | Alta | 5 | Sin empezar |
| PB-HM-64 | Visualizar panel de priorización de vulnerabilidades (Patch Intelligence) que cruza CVEs críticos sin parche con ataques reales. | Analista | Alta | 8 | Sin empezar |
| PB-HM-65 | Consultar diccionario de usuarios más probados por atacantes (Honeypot Advisor) para predecir vectores de fuerza bruta. | Consultor | Media | 3 | Sin empezar |
| PB-HM-66 | Visualizar línea de tiempo de integridad (FIM) para cruzar temporalmente accesos de atacantes con alteraciones de archivos. | Analista | Alta | 8 | Sin empezar |
| PB-HM-67 | Visualizar diagrama del ciclo de ataque completo de una amenaza mapeando sus acciones a las tácticas de MITRE ATT&CK. | Analista | Alta | 13 | Sin empezar |
| PB-HM-68 | Validar manualmente (HITL) las alertas de archivos comprometidos para re-entrenar el modelo de detección. | Analista | Media | 5 | Sin empezar |
| PB-HM-69 | Consultar panel de cumplimiento de seguridad (CIS Benchmark) para obtener recomendaciones exactas de remediación de hardening. | Consultor | Media | 5 | Sin empezar |
| PB-HM-70 | Visualizar mapa de calor predictivo de horarios de ataque (días vs horas) para anticipar picos de carga. | Todos | Media | 3 | Sin empezar |
| PB-HM-71 | Listar tabla completa e historiada de todas las amenazas categorizadas en el Intelligence Center. | Analista | Media | 5 | Sin empezar |
| PB-HM-72 | Registrar manualmente una nueva amenaza externa en el Intelligence Center proporcionando evidencia de ataque. | Analista | Media | 5 | Sin empezar |
| PB-HM-73 | Actualizar la clasificación, severidad o anotaciones de una amenaza previamente registrada en el Intelligence Center. | Analista | Baja | 3 | Sin empezar |
| PB-HM-74 | Retirar definitivamente una amenaza del Intelligence Center previa confirmación de seguridad. | Analista | Baja | 2 | Sin empezar |
| PB-HM-75 | Recibir alerta automática inmediata cuando el Threat Score de una IP monitoreada supere el umbral crítico de APT. | Consultor | Alta | 5 | Sin empezar |
| PB-HM-76 | Exportar el reporte detallado de amenazas activas del Intelligence Center en un documento PDF estructurado. | Analista | Media | 3 | Sin empezar |
| PB-HM-77 | Comparar visualmente la evolución del Threat Score de una IP entre dos o más períodos de tiempo históricos. | Analista | Baja | 3 | Sin empezar |
| PB-HM-78 | Visualizar historial detallado de ataques de una IP específica presentados en una línea de tiempo cronológica interactiva. | Analista | Media | 5 | Sin empezar |
| PB-HM-79 | Solicitar revisión o bloqueo total de un rango CIDR completo detectado como botnet coordinada persistente. | Consultor | Media | 3 | Sin empezar |
| PB-HM-80 | Ver lista de recomendaciones de hardening jerarquizadas por su impacto directo en la mejora del score CIS general. | Consultor | Media | 5 | Sin empezar |

## Resumen de Estimaciones V2

| Categoría | Cantidad de Ítems | Total Story Points |
|---|---|---|
| Threat Intelligence | 9 | 44 |
| Dashboards & Visualización | 4 | 19 |
| ML & Forense | 7 | 44 |
| **Total Backlog V2** | **20** | **107 SP** |
