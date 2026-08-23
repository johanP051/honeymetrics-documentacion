# 📊 Sprint 2 — Dashboards Avanzados, Logs & Reportes

> **Período:** Semanas 4–6
> **Foco:** Visualización Plotly Dark Mode, Heatmap Predictivo, extracción asíncrona de logs JSONL y generación de PDF client-side
> **Dato clave:** Los picos de ataque ocurren los Lunes entre 11:00-12:00 UTC (28% del volumen total histórico)

---
### 🧩 HU: PB-HM-26.1 — Dashboard KPIs y Gráficos Plotly

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-26 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_plotly_dashboard.jpg` |

**Narrativa:**
> Como **Usuario** quiero **visualizar un dashboard con KPIs y 4 gráficos interactivos Plotly** para **entender el volumen y la distribución de los ataques de forma rápida.**

**Tareas de Desarrollo:**
- [ ] Integrar librería Plotly.js con fondos transparentes (paper_bgcolor)
- [ ] Implementar 4 tipos de gráficos: torta, líneas spline, y dos de barras horizontales
- [ ] Cargar datos iniciales (default: 7 días)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el usuario accede a la vista principal del Dashboard
Cuando los datos se cargan correctamente desde la API
Entonces el sistema renderiza exitosamente los 4 gráficos Plotly mostrando información de los últimos 7 días.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que un gráfico de barras debe mostrar etiquetas textuales largas
Cuando el texto de la etiqueta supera los 40 caracteres de longitud
Entonces el gráfico trunca automáticamente el texto y añade "..." al final para no deformar el contenedor.
```

---
### 🧩 HU: PB-HM-27.1 — Filtro Temporal del Dashboard

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-27 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_time_filter.jpg` |

**Narrativa:**
> Como **Usuario** quiero **filtrar el dashboard mediante un selector temporal** para **analizar ataques en ventanas de tiempo específicas (24h, 7d, 30d, custom).**

**Tareas de Desarrollo:**
- [ ] Crear componente selector de fechas (Dropdown y DatePicker)
- [ ] Conectar cambio de fecha a la recarga de los gráficos (estado global)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el dashboard muestra datos por defecto
Cuando el usuario selecciona "Últimas 24h" en el filtro temporal
Entonces todos los KPIs y gráficos se actualizan dinámicamente sin requerir la recarga completa de la página.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el usuario utiliza el filtro personalizado
Cuando selecciona un rango de fechas que no posee ningún registro de ataque
Entonces el sistema muestra un mensaje amigable "Sin datos para el período seleccionado" en lugar de un error.
```

---
### 🧩 HU: PB-HM-70.1 — Heatmap Predictivo de Ataques (Días x Horas)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-70 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_predictive_heatmap.jpg` |

**Narrativa:**
> Como **Usuario** quiero **visualizar un mapa de calor que cruce días contra horas** para **identificar patrones temporales recurrentes en las oleadas de ataque.**

**Tareas de Desarrollo:**
- [ ] Configurar Plotly Heatmap
- [ ] Mapear matriz de datos (7 días x 24 horas)
- [ ] Ajustar gradiente de colores (Rojo oscuro para picos altos)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el Heatmap Predictivo está completamente cargado
Cuando el sistema evalúa la matriz de datos históricos
Entonces la celda correspondiente al Lunes a las 11:00 UTC se renderiza en rojo oscuro intenso, destacando el 28% del volumen histórico.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista interactúa con el Heatmap
Cuando hace hover con el ratón sobre la celda de máxima intensidad (Lunes 11:00)
Entonces aparece un tooltip detallado que indica: "Lunes 11:00 UTC — 40.062 eventos históricos (máximo registrado)".
```

---
### 🧩 HU: PB-HM-37.1 — Solicitar Extracción JSONL (Asíncrona)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-37 |
| **Actor** | Consultor / Analista |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_async_export.jpg` |

**Narrativa:**
> Como **Analista** quiero **solicitar la extracción de logs masivos en formato JSONL de manera asíncrona** para **no bloquear la interfaz de usuario mientras el servidor procesa la consulta pesada.**

**Tareas de Desarrollo:**
- [ ] Interfaz de solicitud de extracción
- [ ] Feedback visual de "Proceso en segundo plano iniciado"

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista envía una solicitud de extracción JSONL por fechas
Cuando el servidor acepta el comando
Entonces el sistema marca la tarea como "Procesando" y permite al usuario seguir navegando por la plataforma libremente.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que una solicitud se encuentra en estado "Procesando"
Cuando el backend termina exitosamente la escritura del archivo
Entonces el estado de la tarea en la interfaz cambia automáticamente a "Listo" para ser descargado.
```

---
### 🧩 HU: PB-HM-38.1 — Historial de Solicitudes de Extracción (Polling)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-38 |
| **Actor** | Consultor / Analista |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_export_history.jpg` |

**Narrativa:**
> Como **Analista** quiero **ver un historial en vivo de mis solicitudes de exportación** para **saber cuándo mis archivos están listos para ser descargados.**

**Tareas de Desarrollo:**
- [ ] Implementar tabla de tareas asíncronas
- [ ] Hook con polling silencioso (`setInterval` 10s)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista accede a la pestaña de exportaciones
Cuando la vista renderiza la información
Entonces se muestra una tabla detallando ID de solicitud, rango de fechas, cantidad de registros, estado actual y fecha de petición.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el usuario tiene una solicitud activa en estado "Procesando"
Cuando el usuario mantiene abierta la vista del historial
Entonces el sistema realiza un polling silencioso cada 10 segundos actualizando el estado de la solicitud sin recargar la página.
```

---
### 🧩 HU: PB-HM-39.1 — Descargar Archivo JSONL Terminado

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-39 |
| **Actor** | Consultor / Analista |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_jsonl_download.jpg` |

**Narrativa:**
> Como **Analista** quiero **poder descargar a mi equipo local el archivo JSONL completado** para **ingestarlo en herramientas analíticas locales o retenerlo como evidencia.**

**Tareas de Desarrollo:**
- [ ] Botón de descarga condicional al estado "Listo"
- [ ] Lógica visual de expiración (7 días)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que existe una solicitud finalizada con estado "Listo"
Cuando el analista hace clic en el botón de descarga
Entonces el navegador inicia la descarga del archivo `.jsonl` y se muestra un aviso indicando que el enlace tiene una vigencia de 7 días.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista revisa el historial de descargas
Cuando visualiza una solicitud generada hace más de 7 días
Entonces el sistema marca su estado como "Expirada" y oculta el botón de descarga permanentemente.
```

---
### 🧩 HU: PB-HM-40.1 — Extracción Masiva con Aprobación Telegram

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-40 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_telegram_approval.jpg` |

**Narrativa:**
> Como **Analista** quiero **que el sistema requiera aprobación de un superior vía Telegram al extraer más de 50.000 registros** para **prevenir exfiltración masiva de datos sensibles sin autorización.**

**Tareas de Desarrollo:**
- [ ] Condicional de volumen en el flujo de solicitud
- [ ] Feedback visual de "Requiere Aprobación"

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que un analista solicita exportar 75.000 eventos (superando el límite de 50k)
Cuando envía la solicitud
Entonces la interfaz gráfica informa "Requiere aprobación" y deja la tarea en estado "Pendiente".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que una solicitud masiva se encuentra pendiente
Cuando la petición es procesada
Entonces el bot supervisor de Telegram recibe un mensaje detallando la solicitud, con botones integrados para "Aprobar" o "Rechazar".
```

---
### 🧩 HU: PB-HM-42.1 — Generar Diccionario ML en PDF (Client-Side)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-42 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_pdf_generator.jpg` |

**Narrativa:**
> Como **Analista** quiero **exportar el diccionario de datos de ML en un PDF estilizado** para **compartirlo en reuniones técnicas sin saturar la memoria RAM del servidor.**

**Tareas de Desarrollo:**
- [ ] Integrar `jspdf` y `jspdf-autotable`
- [ ] Diseñar layout del PDF (Logo, Título, Timestamp, Tabla de campos)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista visualiza el diccionario de datos de Machine Learning
Cuando hace clic en el botón "Generar PDF"
Entonces el sistema construye un documento estilizado con el logo HoneyMetrics, timestamp y tabla, y lo descarga automáticamente al disco del cliente.
```

**Escenario 2 — Error / Edge Case (Regla Crítica de Arquitectura):**
```gherkin
Dado que el analista hace clic en "Generar PDF"
Cuando el proceso de generación e instanciación del documento inicia
Entonces no se realiza ninguna petición HTTP al servidor de FastAPI, comprobando que el archivo se compila 100% del lado del navegador del cliente (Client-Side).
```

---
### 🧩 HU: PB-HM-44.1 — Alertas Emergentes para Picos de Ataque

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-44 |
| **Actor** | Consultor |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_spike_alert.jpg` |

**Narrativa:**
> Como **Consultor** quiero **ver una alerta emergente cuando el volumen de ataque supera el 300% del promedio** para **poder reaccionar instantáneamente ante un ataque DDoS o de fuerza bruta masivo.**

**Tareas de Desarrollo:**
- [ ] Componente Pop-Up global (z-index alto, color rojo crítico)
- [ ] Lógica de debounce/throttling (30s) para evitar spam

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el sistema detecta un pico de ataque inusual superior al 300%
Cuando se evalúa el contexto en tiempo real
Entonces se dispara un pop-up rojo crítico en la interfaz con el resumen de la anomalía y botones de "Ver Detalle" o "Descartar".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que ocurre un ataque masivo y prolongado (múltiples picos consecutivos en segundos)
Cuando el sistema intenta notificar repetidas veces
Entonces el mecanismo de debounce actúa, asegurando que solo se despliegue una única alerta visible cada 30 segundos, evitando la fatiga visual del usuario.
```

---
### 🧩 HU: PB-HM-65.1 — Honeypot Advisor (Diccionario de Usuarios)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-65 |
| **Actor** | Consultor |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_honeypot_advisor.jpg` |

**Narrativa:**
> Como **Consultor** quiero **visualizar el Honeypot Advisor con los nombres de usuario más probados por atacantes** para **determinar qué perfiles o servicios de mi infraestructura están buscando explotar.**

**Tareas de Desarrollo:**
- [ ] Componente de lista categorizada
- [ ] Mapeo de datos (usuarios y su frecuencia)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el Consultor accede al Honeypot Advisor
Cuando la vista termina de renderizar
Entonces observa un panel con el Top 10 de nombres de usuario más probados por atacantes, como por ejemplo "root: 108.282 intentos".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el Consultor analiza la lista completa del Honeypot Advisor
Cuando revisa el panel de clasificación
Entonces visualiza los nombres de usuario agrupados correctamente por categorías de amenaza esperada (Ej: Administración, Cloud, DevOps, BD, Cripto).
```
