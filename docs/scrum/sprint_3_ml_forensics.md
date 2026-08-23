# 🔬 Sprint 3 — ML, Forense Digital & Compliance

> **Período:** Semanas 7–8
> **Foco:** Inteligencia de parches, Kill Chain MITRE ATT&CK, validación humana de Rootcheck y cumplimiento CIS
> **Datos que justifican este sprint:**
> - 1.721 CVEs críticos (≥7.0) sin parche durante 4+ meses
> - 1.139 detecciones Rootcheck en `/bin/passwd` y `/usr/bin/chsh`
> - Score CIS Benchmark: 45-50% (Reprobado) en todos los agentes durante 4 meses
> - 8 tácticas MITRE ATT&CK mapeadas en los 165.247 eventos reales

---
### 🧩 HU: PB-HM-64.1 — Panel Patch Intelligence

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-64 |
| **Actor** | Analista / Administrador |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_patch_intel.jpg` |

**Narrativa:**
> Como **Analista / Administrador** quiero **ver un panel que cruce mis CVEs sin parchear con los ataques recibidos** para **saber exactamente qué vulnerabilidades están siendo explotadas activamente y priorizarlas.**

**Tareas de Desarrollo:**
- [ ] Componente visual de lista jerarquizada
- [ ] Lógica visual de cruce (CVE activo + match de evento de ataque)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el sistema detecta un CVE crítico (ej. CVE-2026-23241, severidad 9.8) que carece de parche y además recibe ataques relacionados
Cuando el Analista consulta el panel de Patch Intelligence
Entonces el sistema destaca esta vulnerabilidad en rojo bajo la máxima prioridad etiquetada como "Parchar HOY".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que existe una vulnerabilidad activa reportada por el escáner
Cuando el sistema verifica que no hay registros de eventos de ataque externos intentando explotarla
Entonces categoriza el CVE bajo prioridad media etiquetándolo en amarillo como "Este mes".
```

---
### 🧩 HU: PB-HM-66.1 — Timeline de Integridad FIM Correlacionado

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-66 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_fim_timeline.jpg` |

**Narrativa:**
> Como **Analista** quiero **visualizar un timeline que muestre cambios en archivos críticos y los cruce con eventos de ataque** para **detectar compromisos exitosos (post-explotación).**

**Tareas de Desarrollo:**
- [ ] Construir componente de Timeline interactivo vertical
- [ ] Renderizar panel de detalles al expandir un nodo (hash differences)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que ocurre un ataque externo en la misma ventana temporal en que un archivo sensible del sistema operativo (ej. `/bin/passwd`) es modificado
Cuando el Analista revisa el Timeline FIM Correlacionado
Entonces el sistema dispara una alerta roja con el texto "Posible compromiso post-explotación" indicando la correlación.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el Analista desea investigar una alteración sospechosa en la línea de tiempo
Cuando hace clic sobre el evento específico de FIM en el timeline
Entonces el panel se expande mostrando el detalle exacto: la ruta del archivo modificado, el hash MD5/SHA anterior y el nuevo, evidenciando el cambio.
```

---
### 🧩 HU: PB-HM-67.1 — (Kill Chain) Algoritmo de Mapeo MITRE ATT&CK (Backend)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-67 |
| **Actor** | Sistema interno |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A (Lógica backend)` |

**Narrativa:**
> Como **Sistema interno** quiero **correlacionar eventos de múltiples fuentes para una IP y mapearlos a las tácticas de MITRE ATT&CK** para **construir la matriz lógica del ciclo de ataque del adversario.**

**Tareas de Desarrollo:**
- [ ] Implementar motor de correlación en `ThreatService`
- [ ] Mapear Reglas Wazuh hacia tácticas MITRE específicas

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que una IP atacante (ej. `45.148.10.151`) genera eventos consecutivos de múltiples sensores (SSH, FIM, Rootcheck)
Cuando el motor de mapeo del backend procesa la IP
Entonces construye satisfactoriamente el objeto Kill Chain asociando las tácticas de "Reconocimiento", "Credential Access" y "Defense Evasion".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que una IP genera únicamente eventos de escaneo de puertos (un solo tipo de evento)
Cuando el backend ejecuta el algoritmo de mapeo MITRE
Entonces retorna un objeto Kill Chain parcial (una sola fase cubierta) sin incluir ni forzar fases vacías irrelevantes.
```

---
### 🧩 HU: PB-HM-67.2 — (Kill Chain) Visualizador Interactivo MITRE (Frontend)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-67 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_kill_chain_ui.jpg` |

> [!NOTE]
> **Justificación del fraccionamiento:** La HU original PB-HM-67 (13 SP) viola el principio INVEST "Small". Se divide en: **67.1** (Lógica de backend - 8 SP) y **67.2** (Componente visual React - 5 SP). Ambas son atómicas, independientes y entregables por separado.

**Narrativa:**
> Como **Analista** quiero **ver el ciclo de ataque de una IP renderizado como un diagrama visual MITRE ATT&CK interactivo** para **comprender intuitivamente qué tan lejos llegó el atacante.**

**Tareas de Desarrollo:**
- [ ] Componente visual de diagrama de flujo horizontal (fases)
- [ ] Lógica responsive para no romper el layout en pantallas chicas

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el Analista selecciona una IP con un ciclo de ataque avanzado
Cuando el componente visual carga los datos estructurados del backend
Entonces renderiza un diagrama secuencial que ilustra claramente las fases MITRE superadas, utilizando flechas de progresión y tooltips informativos por cada táctica.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que una amenaza presenta un Kill Chain complejo que abarca las 8 fases identificadas
Cuando el componente visual se renderiza en un monitor estándar (resolución de 1280px)
Entonces el diseño es fluido y adapta todas las fases de manera legible sin generar scroll horizontal que perjudique la UX.
```

---
### 🧩 HU: PB-HM-68.1 — HITL Rootcheck: Validación Humana

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-68 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_hitl_rootcheck.jpg` |

**Narrativa:**
> Como **Analista** quiero **poder clasificar manualmente las alertas de rootkits detectadas por el sistema** para **corregir falsos positivos y proveer datos etiquetados al modelo de ML.**

**Tareas de Desarrollo:**
- [ ] Interfaz de panel con botones "Confirmar" y "Rechazar"
- [ ] Petición POST para etiquetar el evento en la DB

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que Rootcheck lanza una alerta por un posible troyano en el binario `/bin/passwd`
Cuando el Analista examina el evento y presiona el botón "Compromiso Confirmado"
Entonces el sistema etiqueta el registro en la base de datos como una amenaza real, reservándolo para el próximo reentrenamiento del modelo de Machine Learning.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que Rootcheck emite una alerta dudosa
Cuando el Analista investiga y la clasifica accionando el botón "Falso Positivo"
Entonces la firma técnica de ese evento específico queda excluida de las amenazas en el modelo para el próximo ciclo de inferencia.
```

---
### 🧩 HU: PB-HM-69.1 — Dashboard Compliance CIS Benchmark

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-69 |
| **Actor** | Consultor |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_cis_compliance.jpg` |

**Narrativa:**
> Como **Consultor** quiero **visualizar mi score de cumplimiento CIS Benchmark junto con instrucciones de remediación** para **cerrar brechas de seguridad en las configuraciones del sistema.**

**Tareas de Desarrollo:**
- [ ] Gauge gráfico de Score (0-100%)
- [ ] Lista de remediaciones ordenadas por impacto

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el score general de cumplimiento CIS del entorno es reprobatorio (ej. 45%)
Cuando el Consultor accede al Dashboard de Compliance
Entonces el sistema lista el Top 10 de fallas de configuración críticas, proveyendo instrucciones exactas y priorizadas para su corrección.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el Consultor aplica exitosamente una de las medidas de corrección indicadas (hardening)
Cuando el sistema Wazuh realiza la nueva auditoría y el score sube de 45% a 52%
Entonces la UI renderiza el nuevo valor destacando el incremento del 7% mediante un indicador visual en color verde.
```

---
### 🧩 HU: PB-HM-48.1 — Resumen Rendimiento Algoritmos ML

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-48 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_ml_metrics.jpg` |

**Narrativa:**
> Como **Analista** quiero **visualizar las métricas de clasificación (Accuracy, F1, ROC AUC) del modelo actual e histórico** para **entender qué tan certera está siendo mi detección de amenazas.**

**Tareas de Desarrollo:**
- [ ] Plotly line chart para curva ROC
- [ ] Gráfico de barras comparativo para múltiples versiones de modelos

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el Analista navega a la sección de Machine Learning
Cuando el dashboard de rendimiento de algoritmos carga por completo
Entonces se renderiza la curva ROC junto con las tarjetas de métricas (Accuracy, Precision, Recall, F1) del modelo vigente.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que existen métricas de modelos de meses anteriores
Cuando el Analista selecciona dos versiones del modelo en el menú de comparación
Entonces el gráfico de barras se actualiza dinámicamente en tiempo real contraponiendo el rendimiento de ambos sin requerir una nueva recarga de página.
```

---
### 🧩 HU: PB-HM-56.1 — Auto-cierre de Sesión por Inactividad (30 min)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-56 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A (Lógica global)` |

**Narrativa:**
> Como **Usuario** quiero **que mi sesión se cierre automáticamente tras 30 minutos sin actividad** para **mitigar el riesgo de acceso no autorizado si dejo mi estación de trabajo desatendida.**

**Tareas de Desarrollo:**
- [ ] Implementar un listener global de eventos (mouse/teclado)
- [ ] Timer central en el `AuthContext`

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que un usuario autenticado deja su estación de trabajo
Cuando transcurren 30 minutos exactos sin registrar interacción alguna de teclado o mouse
Entonces el sistema invalida su token local y lo redirige de forma forzosa hacia la pantalla de Login.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el temporizador interno de inactividad alcanza los 25 minutos
Cuando el usuario interactúa nuevamente con la plataforma moviendo el mouse o pulsando una tecla
Entonces el temporizador se resetea inmediatamente a 0, asegurando que la sesión continúe ininterrumpida.
```
