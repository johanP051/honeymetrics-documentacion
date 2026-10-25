# 📋 Product Backlog Consolidado — HoneyMetrics v2.0

> **Materia:** Ingeniería de Software II (IS2) — UDEC Facatativá
> **Equipo:** Johan Sebastián Posada Beltrán · Juan Pablo Fonseca Celis 
> **Arquitectura:** FastAPI + React 18 (Polyrepo)
> **Fuente:** SRS v6 + Análisis de datos reales Wazuh (165.247 eventos)

!!! warning "⚡ Reglas del Profesor — Convención Obligatoria"
    - Código: `PB-HM-01` a `PB-HM-70` (Fase 1 Oficial) / `PB-HM-71` a `PB-HM-80` (Enterprise Fase 2).
    - Perspectiva: **QUÉ** necesita el usuario, **nunca** el CÓMO técnico.
    - CRUD: cada operación = ítem separado.
    - Trazabilidad HU: `PB-HM-01.1`, `PB-HM-01.2` ... (Hoja 2 - HU).
    - Estado inicial: `Sin empezar`.
    - Prioridad: Alta / Media / Baja.
    - Fibonacci: 1, 2, 3, 5, 8, 13.

## 🗂️ HOJA 1 — PRODUCT BACKLOG (PB-HM-01 a PB-HM-70)

| Código | Descripción (Lenguaje de Negocio) | CU Origen | Actor | Prioridad | Puntos | Estado |
|---|---|---|---|---|---|---|
| PB-HM-01 | Visualizar página de inicio pública (Landing Page) — El sistema debe mostrar una página de bienvenida profesional que explique el propósito de HoneyMetrics y ofrezca el punto de acceso (Login). Incluye navbar, sección hero, muestra de código y mapa de calor ilustrativo. | CU-G-0 | Visitante / Todos | Alta | 3 | Sin empezar |
| PB-HM-02 | Iniciar sesión con credenciales institucionales — El usuario debe poder autenticarse en la plataforma usando su correo @ucundinamarca.edu.co y contraseña. El sistema debe validar credenciales, identificar el rol y redirigir al dashboard correspondiente. | CU-G-01 | Todos | Alta | 5 | Sin empezar |
| PB-HM-03 | Bloquear acceso por credenciales inválidas — El sistema debe rechazar el ingreso cuando el correo o contraseña sean incorrectos, mostrando un mensaje de error claro sin revelar cuál campo falló (anti-enumeración). | CU-G-01 | Todos | Alta | 2 | Sin empezar |
| PB-HM-04 | Forzar cambio de contraseña en primer inicio de sesión — Al detectar que el usuario tiene contraseña temporal, el sistema debe redirigirlo obligatoriamente a una vista de cambio de clave antes de permitir el acceso al dashboard. | CU-G-02 | Todos | Alta | 3 | Sin empezar |
| PB-HM-05 | Cambiar contraseña voluntariamente (usuario autenticado) — Cualquier usuario con sesión activa debe poder actualizar su contraseña desde su perfil, verificando la clave actual y cumpliendo los criterios de seguridad (min. 8 caracteres, no común, alfanumérica). | CU-G-02 | Todos | Alta | 3 | Sin empezar |
| PB-HM-06 | Restablecer contraseña olvidada vía correo electrónico — Un usuario que no pueda iniciar sesión debe poder solicitar un enlace de restablecimiento enviado a su correo institucional. El token debe ser de un solo uso y expirar en 24 horas. | CU-G-10 | Todos | Alta | 5 | Sin empezar |
| PB-HM-07 | Autenticar con segundo factor (2FA-OTP) — Después de ingresar usuario y contraseña correctamente, el sistema debe solicitar un código OTP de 6 dígitos generado por Google Authenticator para completar el acceso. | CU-G-07 | Todos | Alta | 5 | Sin empezar |
| PB-HM-08 | Vincular Google Authenticator en el primer inicio — Si el usuario no ha configurado el 2FA previamente, el sistema debe mostrar un código QR para que escanee con su app autenticadora, verificando la sincronización antes de conceder acceso. | CU-G-07 | Todos | Alta | 3 | Sin empezar |
| PB-HM-09 | Cerrar sesión de forma segura — El usuario debe poder finalizar su sesión desde cualquier vista del dashboard. El sistema debe invalidar el token JWT en el servidor y limpiar el almacenamiento local del navegador, impidiendo re-acceso con el botón "Atrás". | CU-G-09 | Todos | Alta | 2 | Sin empezar |
| PB-HM-10 | Redireccionar al login al acceder a rutas protegidas sin sesión — Cualquier intento de acceso a rutas del dashboard sin token de sesión válido debe resultar en redirección automática al Login. | CU-G-01 | Todos | Alta | 2 | Sin empezar |
| PB-HM-11 | Mostrar banner informativo a usuarios sin rol asignado — Si un usuario se autentica correctamente pero no tiene ningún rol asignado, el sistema debe mostrarlo con acceso mínimo y un mensaje informativo indicando que debe solicitar permisos al Administrador. | CU-G-01 | Todos | Media | 2 | Sin empezar |
| PB-HM-12 | Acceder al panel de administración del sistema — El Administrador debe poder acceder desde el frontend al panel de administración profunda haciendo clic en "Gestión", sin necesidad de escribir la URL manualmente. | CU-G-03 | Administrador | Alta | 2 | Sin empezar |
| PB-HM-13 | Crear un nuevo Rol/Grupo de permisos — El Administrador debe poder crear nuevos grupos de permisos con nombre único (ej. "Consultor de Ciberseguridad") y asignarles los permisos específicos disponibles en el sistema. | CU-ADM-01 | Administrador | Alta | 3 | Sin empezar |
| PB-HM-14 | Consultar la lista de Roles/Grupos existentes — El Administrador debe poder visualizar todos los grupos de permisos registrados en el sistema, con su nombre y la cantidad de usuarios asociados. | CU-ADM-02 | Administrador | Alta | 1 | Sin empezar |
| PB-HM-15 | Modificar un Rol/Grupo de permisos existente — El Administrador debe poder editar el nombre o los permisos asignados a un grupo. Los cambios deben aplicarse inmediatamente a todos los usuarios que posean ese rol. | CU-ADM-03 | Administrador | Alta | 2 | Sin empezar |
| PB-HM-16 | Eliminar un Rol/Grupo de permisos — El Administrador debe poder borrar permanentemente un grupo del sistema, previo aviso de cuántos usuarios quedarán sin ese rol. La eliminación debe requerir confirmación explícita. | CU-ADM-04 | Administrador | Alta | 2 | Sin empezar |
| PB-HM-17 | Crear cuenta de nuevo usuario — El Administrador debe poder registrar a un nuevo miembro del equipo (Directivo, Consultor o Analista) con nombre, correo institucional, contraseña temporal y rol asignado (máximo uno). | CU-ADM-05 | Administrador | Alta | 5 | Sin empezar |
| PB-HM-18 | Consultar la lista de usuarios registrados — El Administrador debe poder visualizar todos los usuarios del sistema en una tabla con columnas de: nombre, correo, rol y estado (activo/inactivo), con búsqueda y filtros. | CU-ADM-06 | Administrador | Alta | 2 | Sin empezar |
| PB-HM-19 | Modificar datos de un usuario existente — El Administrador debe poder editar la información de perfil de cualquier usuario (nombre, correo, rol asignado) sin necesidad de eliminar y recrear la cuenta. | CU-ADM-07 | Administrador | Alta | 3 | Sin empezar |
| PB-HM-20 | Eliminar un usuario del sistema — El Administrador debe poder borrar definitivamente un usuario y todos sus datos relacionados (en cascada), previo aviso detallado de los objetos que serán eliminados y confirmación explícita. | CU-ADM-08 | Administrador | Alta | 3 | Sin empezar |
| PB-HM-21 | Visualizar y editar perfil de usuario propio — Cualquier usuario debe poder acceder a su perfil personal para ver su rol, zona horaria, cambiar su foto de perfil (JPG/PNG, máx. 2MB) y su preferencia de tema (claro/oscuro). | CU-G-08 | Todos | Media | 3 | Sin empezar |
| PB-HM-22 | Consultar la Lista Negra de IPs — Todos los roles deben poder visualizar el repositorio de IPs marcadas como amenaza en una tabla interactiva con paginación del lado del servidor (10 registros/página por defecto), búsqueda global y columnas de: IP, tipo, país, ataque y usuario reportador. | CU-G-04 | Todos | Alta | 5 | Sin empezar |
| PB-HM-23 | Agregar una IP a la Lista Negra — Los usuarios con rol operativo (Administrador, Consultor, Analista) deben poder registrar una nueva IP amenaza mediante un formulario modal, con validación de formato IPv4/IPv6 y asignación automática del usuario en sesión como creador. | CU-G-05 | Adm. / Consultor / Analista | Alta | 5 | Sin empezar |
| PB-HM-24 | Eliminar una IP de la Lista Negra — Los usuarios con rol operativo deben poder remover un registro de la lista negra directamente desde la fila de la tabla, con confirmación previa para evitar borrados accidentales. | CU-G-06 | Adm. / Consultor / Analista | Alta | 3 | Sin empezar |
| PB-HM-25 | Exportar la Lista Negra de IPs (CSV / Excel) — Los usuarios deben poder descargar la lista negra completa o filtrada en formato CSV o Excel (.xlsx), respetando los filtros activos al momento de la exportación. El botón de exportación debe deshabilitarse si no hay datos. | CU-DASH-07 | Dir. T.I / Consultor / Analista | Media | 5 | Sin empezar |
| PB-HM-26 | Visualizar el Dashboard principal de ataques y estadísticas — Los usuarios deben poder ver un dashboard operativo con KPIs (total alertas, severidad promedio) y cuatro gráficos dinámicos: distribución por módulo (torta), histórico temporal (líneas), top agentes afectados (barras) y top eventos frecuentes (barras). El rango por defecto es la última semana. | CU-DASH-01 | Dir. T.I / Consultor / Analista / Adm. | Alta | 8 | Sin empezar |
| PB-HM-27 | Filtrar el Dashboard por rango de fechas — Los usuarios deben poder cambiar el rango temporal de los gráficos del dashboard (ej. últimas 24h, última semana, último mes) y ver los KPIs y gráficos actualizarse instantáneamente. | CU-DASH-01 | Dir. T.I / Consultor / Analista | Alta | 3 | Sin empezar |
| PB-HM-28 | Visualizar el Mapa de Calor Interactivo de ataques — Los usuarios deben poder visualizar un mapa mundial interactivo que muestre la procedencia geográfica de los ataques con escala de colores (verde a rojo según intensidad), tooltips por país y tabla "Top 10 Países Atacantes". | CU-DASH-02 | Dir. T.I / Consultor / Analista | Alta | 8 | Sin empezar |
| PB-HM-29 | Filtrar el Mapa de Calor por tipo de ataque — Los usuarios deben poder seleccionar un tipo de ataque específico (ej. "Fuerza Bruta SSH") y ver el mapa de calor actualizarse mostrando únicamente los ataques de ese tipo. | CU-DASH-02 | Dir. T.I / Consultor / Analista | Media | 3 | Sin empezar |
| PB-HM-30 | Ver panel de detalle de país al hacer clic en el mapa — Al hacer clic en un país del mapa de calor, el sistema debe desplegar un panel lateral con el desglose de IPs, tipos de ataque y períodos de actividad para ese territorio. | CU-DASH-02 | Dir. T.I / Consultor / Analista | Media | 3 | Sin empezar |
| PB-HM-31 | Visualizar Medidas de Tendencia Central (Estadística Descriptiva) — Los usuarios autorizados deben poder ver una vista de estadísticas con media, mediana, moda, desviación estándar y varianza de las variables de ataque, junto con un histograma de frecuencia y un diagrama de caja (boxplot). | CU-DASH-04 | Dir. T.I / Analista | Alta | 8 | Sin empezar |
| PB-HM-32 | Filtrar estadísticas descriptivas por variable de análisis y rango de fechas — Los usuarios deben poder seleccionar qué variable analizar y un rango de fechas, actualizando automáticamente todas las métricas y gráficos estadísticos. | CU-DASH-04 | Dir. T.I / Analista | Media | 3 | Sin empezar |
| PB-HM-33 | Exportar tabla de estadísticas descriptivas en CSV — El Analista debe poder descargar la tabla de medidas estadísticas en formato CSV con un solo clic. | CU-DASH-04 | Analista | Media | 2 | Sin empezar |
| PB-HM-34 | Visualizar Matriz de Confusión interactiva del modelo de IA — Los usuarios autorizados deben poder ver la matriz de confusión (VP, FP, VN, FN) comparando predicciones del modelo de IA vs. clasificaciones reales, con indicadores derivados (Accuracy, Precision, Recall, F1-Score) y tooltips explicativos por celda. | CU-DASH-03 | Dir. T.I / Consultor / Analista | Media | 8 | Sin empezar |
| PB-HM-35 | Filtrar la Matriz de Confusión por tipo de ataque y rango de fechas — Los usuarios deben poder filtrar la matriz de confusión para un tipo de ataque específico y un período de tiempo, recalculando todos los indicadores de rendimiento. | CU-DASH-03 | Dir. T.I / Consultor / Analista | Media | 3 | Sin empezar |
| PB-HM-36 | Ver tabla de detalle al hacer clic en una celda de la Matriz — Al hacer clic en una celda de la matriz (ej. "Falsos Positivos"), el sistema debe desplegar una tabla expandible con los registros específicos (IP, fecha, tipo predicho, clasificación real, confianza del modelo). | CU-DASH-03 | Consultor / Analista | Media | 3 | Sin empezar |
| PB-HM-37 | Solicitar descarga de logs crudos (JSONL) — Los usuarios autorizados deben poder seleccionar un rango de fechas y solicitar la extracción de eventos del Wazuh Indexer. El sistema procesa la petición en segundo plano (asincrónico) y notifica al usuario cuando el archivo esté listo. | CU-DASH-06 / CU-LOG-01 | Consultor / Analista | Alta | 8 | Sin empezar |
| PB-HM-38 | Consultar historial de solicitudes de descarga de logs — Los usuarios deben poder visualizar una tabla con todas sus solicitudes de descarga previas: ID, rango de fechas, cantidad de registros, estado (Pendiente, Procesando, Listo, Rechazada, Fallida) y fecha. La tabla se actualiza automáticamente cada 10 segundos. | CU-DASH-06 | Consultor / Analista | Alta | 3 | Sin empezar |
| PB-HM-39 | Descargar archivo JSONL de logs generado — Una vez que el archivo de logs está en estado "Listo", el usuario debe poder descargarlo con un clic. El archivo tiene una vigencia de 7 días y es eliminado automáticamente después de ese período. | CU-DASH-06 | Consultor / Analista | Alta | 3 | Sin empezar |
| PB-HM-40 | Solicitar descarga masiva que requiere aprobación del Administrador — Si la solicitud de logs supera el umbral de 50.000 registros, el sistema debe bloquear la descarga directa, crear una solicitud con estado "Pendiente" y notificar al Administrador vía Telegram con botones de Aprobar/Rechazar. | CU-DASH-08 / CU-ADM-09 | Consultor / Analista | Alta | 8 | Sin empezar |
| PB-HM-41 | Aprobar o rechazar solicitud de descarga masiva (vía Telegram) — El Administrador debe poder aprobar o rechazar solicitudes masivas directamente desde el Bot de Telegram de HoneyMetrics, con el sistema validando su identidad y actuando conforme a la decisión. | CU-ADM-09 | Administrador | Alta | 8 | Sin empezar |
| PB-HM-42 | Generar y descargar el Diccionario de Datos en PDF — El Analista debe poder generar, desde la vista de Logs, un documento PDF con el esquema técnico completo de los campos del evento Wazuh (atributo, tipo, descripción para ML), con logotipo de HoneyMetrics y marca de tiempo. Generado en el navegador del usuario (client-side). | CU-LOG-02 | Analista | Media | 5 | Sin empezar |
| PB-HM-43 | Generar y descargar informes ejecutivos y de rendimiento — Los usuarios autorizados deben poder generar informes en formato CSV o Excel seleccionando un rango de fechas y tipo de informe (Ejecutivo u Operativo). La generación se realiza en segundo plano con barra de progreso. Peso máximo: 50 MB. | CU-DASH-05 | Dir. T.I / Consultor | Media | 8 | Sin empezar |
| PB-HM-44 | Recibir alertas emergentes ante anomalías críticas en pantalla — El sistema debe detectar automáticamente anomalías críticas (picos de ataque >300%) y mostrar una ventana emergente clasificada por severidad (Roja/Naranja/Amarilla) con el resumen del evento, botón "Ver Detalle" y botón "Descartar". Máximo una alerta cada 30 segundos. | CU-CON-01 | Consultor | Alta | 8 | Sin empezar |
| PB-HM-45 | Consultar historial de alertas recibidas — El Consultor debe poder acceder a un panel lateral con todas las alertas generadas en las últimas 24 horas, su estado (Atendida, Descartada, Ignorada) y detalles del evento. | CU-CON-01 | Consultor | Media | 3 | Sin empezar |
| PB-HM-46 | Ver detalle completo de una anomalía detectada — Al hacer clic en "Ver Detalle" de una alerta, el sistema debe mostrar: tabla de registros asociados, historial de la IP, gráfico temporal de la anomalía y botones de acción ("Agregar a Lista Negra" y "Marcar como Falso Positivo"). | CU-CON-01 | Consultor | Alta | 5 | Sin empezar |
| PB-HM-47 | Marcar una alerta como Falso Positivo — El Consultor debe poder clasificar un evento detectado como falso positivo con confirmación del sistema, lo que debe actualizar el estado de la alerta y etiquetar el registro para el reentrenamiento futuro de la IA. | CU-CON-01 | Consultor | Media | 3 | Sin empezar |
| PB-HM-48 | Visualizar el Resumen de Rendimiento de Algoritmos de ML — El Analista debe poder ver un dashboard técnico con métricas del modelo vigente: KPIs (Accuracy, Precision, Recall, F1, ROC AUC), curva ROC, gráfico comparativo entre versiones y tiempos de ejecución. | CU-ANA-01 | Analista | Media | 8 | Sin empezar |
| PB-HM-49 | Comparar el rendimiento entre múltiples versiones del modelo de IA — El Analista debe poder seleccionar dos o más versiones del modelo y ver sus métricas de rendimiento comparadas en un gráfico de barras actualizado. | CU-ANA-01 | Analista | Media | 5 | Sin empezar |
| PB-HM-50 | Exportar métricas de rendimiento de algoritmos en CSV — El Analista debe poder descargar el historial completo de métricas de rendimiento de los modelos en formato CSV. | CU-ANA-01 | Analista | Baja | 2 | Sin empezar |
| PB-HM-51 | Guardar filtros predeterminados de Lista Negra (Analista) — El Analista debe poder guardar combinaciones de filtros recurrentes sobre la Lista Negra (hasta 10 por usuario) con nombre único y reutilizarlos rápidamente para preparar datasets de entrenamiento. | CU-ANA-02 | Analista | Media | 3 | Sin empezar |
| PB-HM-52 | Consultar filtros guardados de Lista Negra — El Analista debe poder ver su lista de filtros guardados y aplicar cualquiera con un solo clic para cargar automáticamente la configuración en la tabla de Lista Negra. | CU-ANA-02 | Analista | Media | 2 | Sin empezar |
| PB-HM-53 | Eliminar un filtro predeterminado guardado — El Analista debe poder borrar un filtro guardado que ya no necesite, con confirmación previa del sistema. | CU-ANA-02 | Analista | Baja | 1 | Sin empezar |
| PB-HM-54 | Monitorear el estado de recursos del Honeypot en tiempo real — El Administrador y el Consultor deben poder visualizar el rendimiento actual del hardware de la Orange Pi 5: CPU (gráfico de anillo), RAM (barras) y almacenamiento (gauge). Los gráficos se actualizan automáticamente cada 60 segundos. | CU-ADM-10 | Adm. / Consultor | Baja | 8 | Sin empezar |
| PB-HM-55 | Alertar cuando el Honeypot pierde conectividad — Si el sistema no recibe telemetría nueva del Honeypot en 5 minutos, debe mostrar una alerta roja persistente indicando la pérdida de comunicación con la Orange Pi 5. | CU-ADM-10 | Adm. / Consultor | Baja | 5 | Sin empezar |
| PB-HM-56 | Aplicar cierre automático de sesión por inactividad (30 min) — Si un usuario deja la plataforma abierta sin interacción (mouse/teclado) durante 30 minutos, el sistema debe cerrar la sesión automáticamente y redirigir al Login. | RNF-01 | Todos | Alta | 3 | Sin empezar |
| PB-HM-57 | Mostrar mensajes de error del sistema en lenguaje natural — Todos los errores de sistema, datos inválidos o fallos de conexión deben mostrarse con alertas de colores (rojo error, amarillo precaución) en español, sin revelar trazas de código al usuario. | RNF-03 | Todos | Alta | 2 | Sin empezar |
| PB-HM-58 | Soportar modo oscuro y modo claro en toda la interfaz — La plataforma debe ofrecer al usuario la opción de alternar entre tema claro y oscuro desde su perfil. La preferencia debe persistir entre sesiones. Los gráficos deben adaptarse automáticamente al tema activo. | CU-G-08 / CU-DASH-01 | Todos | Media | 5 | Sin empezar |
| PB-HM-59 | Notificar al usuario vía Telegram cuando su descarga está lista — Al finalizar el procesamiento de logs en segundo plano, el sistema debe enviar un mensaje de notificación al identificador de Telegram registrado en el perfil del usuario. | CU-LOG-01 / RNF-05 | Consultor / Analista | Media | 3 | Sin empezar |
| PB-HM-60 | Eliminar automáticamente archivos de logs expirados (7 días) — El sistema debe ejecutar una tarea programada periódica que elimine del servidor todos los archivos JSONL que superen los 7 días de vigencia, liberando espacio en disco de forma autónoma. | CU-LOG-01 / RNF-05 | Sistema | Media | 3 | Sin empezar |
| PB-HM-61 | Listar IPs registradas en el Intelligence Center con su Threat Score dinámico (0-100). | CU-ANA-03 | Analista | Alta | 8 | Sin empezar |
| PB-HM-62 | Identificar y alertar sobre ataques coordinados (Botnets) agrupando IPs por subred CIDR /24. | CU-ANA-03 | Analista | Alta | 5 | Sin empezar |
| PB-HM-63 | Clasificar a los atacantes como Bot (automatizado rápido) o Humano (dirigido lento) según su velocidad de ataque. | CU-ANA-03 | Analista | Alta | 5 | Sin empezar |
| PB-HM-64 | Visualizar panel de priorización de vulnerabilidades (Patch Intelligence) que cruza CVEs críticos sin parche con ataques reales. | CU-ANA-04 | Analista | Alta | 8 | Sin empezar |
| PB-HM-65 | Consultar diccionario de usuarios más probados por atacantes (Honeypot Advisor) para predecir vectores de fuerza bruta. | CU-ANA-03 | Consultor | Media | 3 | Sin empezar |
| PB-HM-66 | Visualizar línea de tiempo de integridad (FIM) para cruzar temporalmente accesos de atacantes con alteraciones de archivos. | CU-ANA-04 | Analista | Alta | 8 | Sin empezar |
| PB-HM-67 | Visualizar diagrama del ciclo de ataque completo de una amenaza mapeando sus acciones a las tácticas de MITRE ATT&CK. | CU-ANA-04 | Analista | Alta | 13 | Sin empezar |
| PB-HM-68 | Validar manualmente (HITL) las alertas de archivos comprometidos para re-entrenar el modelo de detección. | CU-ANA-04 | Analista | Media | 5 | Sin empezar |
| PB-HM-69 | Consultar panel de cumplimiento de seguridad (CIS Benchmark) para obtener recomendaciones exactas de remediación de hardening. | CU-ANA-05 | Consultor | Media | 5 | Sin empezar |
| PB-HM-70 | Visualizar mapa de calor predictivo de horarios de ataque (días vs horas) para anticipar picos de carga. | CU-DASH-02 | Todos | Media | 3 | Sin empezar |

---

## 🗓️ PROPUESTA DE SPRINTS (Cronograma IS2)
> Fecha de entrega: mediados de octubre 2026 (~8 semanas)

| SPRINT | PERÍODO | FOCO | HISTORIAS INCLUIDAS | PUNTOS (SP) |
|--------|---------|------|---------------------|:-----------:|
| **Sprint 1** | Semanas 2–3 | Autenticación Segura (JWT/2FA) y Gestión CRUD del Threat Intelligence Center. | `PB-HM-01` a `PB-HM-25` + `PB-HM-61` (26 HUs) | **87 SP** |
| **Sprint 2** | Semanas 4–6 | Visualización Analítica (Dashboards Plotly, Heatmap) y Extracción Asíncrona de Logs. | `PB-HM-26` a `PB-HM-47` + `PB-HM-62`, `PB-HM-63`, `PB-HM-70` (25 HUs) | **127 SP** |
| **Sprint 3** | Semanas 7–8 | Inteligencia Forense (Timeline FIM, Patch Intel), Rendimiento ML, validación HITL y CIS Benchmark. | `PB-HM-48` a `PB-HM-60` + `PB-HM-64` a `PB-HM-69` (19 HUs) | **92 SP** |
| **TOTAL** | | **Product Backlog Consolidado Fase 1 (70 Historias de Usuario)** | | **306 SP** |

---

## 📝 NOTAS PARA LA HOJA 2 (HISTORIAS DE USUARIO)

Los ítems del backlog se **desglosarán en HUs individuales** en la Hoja 2 usando la convención:

- `PB-HM-02.1` → HU: Formulario de Login (frontend React)
- `PB-HM-02.2` → HU: Endpoint POST /api/v1/auth/login que retorna JWT

Cada HU incluirá:

- Narrativa: "Como [ROL] quiero [ACCIÓN] para [BENEFICIO]"
- Criterios de aceptación BDD (Dado/Cuando/Entonces)
- Puntos Fibonacci
- Estado: `Sin empezar`
