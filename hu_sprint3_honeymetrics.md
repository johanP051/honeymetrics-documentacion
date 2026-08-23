# Historias de Usuario - Sprint 3 (HoneyMetrics v2.0)

### HU: PB-HM-48.1
- **Código PB Padre:** PB-HM-48
- **Actor:** Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero visualizar el resumen de rendimiento de algoritmos de ML en un dashboard técnico para evaluar de manera integral la efectividad del modelo de clasificación de amenazas vigente.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que accedo al dashboard técnico de ML, Cuando visualizo las métricas principales, Entonces veo los KPIs actualizados de Accuracy, Precision, Recall, F1-Score y ROC AUC.
  - **Escenario 2:** Dado que necesito analizar la capacidad de discriminación del modelo, Cuando examino el dashboard en detalle, Entonces visualizo gráficamente la curva ROC y los promedios de tiempo de ejecución del algoritmo.

### HU: PB-HM-49.1
- **Código PB Padre:** PB-HM-49
- **Actor:** Analista
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero comparar el rendimiento entre múltiples versiones del modelo de IA para identificar cuál de los modelos iterados es más efectivo frente a los patrones de ataque recientes.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que existen múltiples modelos entrenados, Cuando selecciono dos o más versiones en el menú, Entonces visualizo un gráfico de barras comparativo que contrapone sus métricas de rendimiento.
  - **Escenario 2:** Dado que estoy viendo la gráfica comparativa, Cuando deselecciono una de las versiones, Entonces el gráfico se actualiza en tiempo real mostrando únicamente los modelos restantes.

### HU: PB-HM-50.1
- **Código PB Padre:** PB-HM-50
- **Actor:** Analista
- **Puntos:** 2
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero exportar las métricas de rendimiento de algoritmos en formato CSV para integrarlas en informes externos, reportes académicos y llevar un control histórico detallado.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que visualizo el panel con el historial de rendimiento de los modelos, Cuando hago clic en el botón de exportar, Entonces se descarga localmente un archivo CSV con todas las métricas en crudo.
  - **Escenario 2:** Dado que aún no hay datos ni métricas de ML calculadas, Cuando visualizo el panel de exportación, Entonces el botón correspondiente se encuentra deshabilitado.

### HU: PB-HM-51.1
- **Código PB Padre:** PB-HM-51
- **Actor:** Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero guardar filtros predeterminados de la Lista Negra para reutilizarlos de forma ágil y facilitar la preparación de nuevos datasets de entrenamiento.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que apliqué una configuración específica de filtros a la Lista Negra, Cuando hago clic en "Guardar Filtros" y le asigno un nombre único, Entonces esa combinación queda guardada en mi perfil de usuario.
  - **Escenario 2:** Dado que quiero guardar una nueva combinación, Cuando intento hacerlo y ya he alcanzado el límite de 10 filtros, Entonces el sistema me muestra un mensaje de advertencia indicando que debo eliminar uno existente.

### HU: PB-HM-52.1
- **Código PB Padre:** PB-HM-52
- **Actor:** Analista
- **Puntos:** 2
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero consultar mis filtros guardados de la Lista Negra para aplicar rápidamente configuraciones complejas sobre la tabla de amenazas con un solo clic.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que abro el panel de la Lista Negra, Cuando despliego el menú de filtros rápidos, Entonces visualizo la lista con los nombres de todos mis filtros previamente almacenados.
  - **Escenario 2:** Dado que he localizado un filtro guardado específico en el menú, Cuando hago clic sobre su nombre, Entonces la tabla se recarga aplicando inmediatamente todos los parámetros de filtrado correspondientes.

### HU: PB-HM-53.1
- **Código PB Padre:** PB-HM-53
- **Actor:** Analista
- **Puntos:** 1
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero eliminar un filtro predeterminado guardado que ya no utilizo para mantener limpia mi lista de filtros y liberar espacio (slots) para configuraciones más recientes.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que reviso mi lista de filtros guardados, Cuando selecciono la opción de borrar sobre uno de ellos, Entonces el sistema despliega un mensaje pidiendo mi confirmación antes de proceder.
  - **Escenario 2:** Dado que he confirmado la acción de borrado, Cuando la operación finaliza, Entonces el filtro desaparece de la vista y el contador de mis filtros disponibles se incrementa en uno.

### HU: PB-HM-54.1
- **Código PB Padre:** PB-HM-54
- **Actor:** Administrador / Consultor
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Administrador / Consultor quiero monitorear el estado de recursos del Honeypot (Orange Pi 5) en tiempo real para verificar si el equipo cuenta con la capacidad de hardware necesaria para seguir registrando amenazas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ingreso a la vista de monitoreo del Honeypot, Cuando finaliza la carga inicial, Entonces veo los gráficos de rendimiento: CPU (gráfico de anillo), RAM (barras) y almacenamiento (tipo gauge).
  - **Escenario 2:** Dado que mantengo activa la pestaña del dashboard de recursos, Cuando transcurren 60 segundos, Entonces el sistema sondea la telemetría y actualiza todos los gráficos dinámicamente sin recargar la página.

### HU: PB-HM-55.1
- **Código PB Padre:** PB-HM-55
- **Actor:** Administrador / Consultor
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Administrador / Consultor quiero alertar cuando el Honeypot pierde conectividad para estar al tanto de posibles caídas críticas del hardware o denegaciones de servicio y poder gestionar la reactivación rápida.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que el agente de telemetría del Honeypot dejó de enviar datos, Cuando el sistema cuenta 5 minutos sin recibir paquetes nuevos, Entonces muestra una alerta roja global indicando que se ha perdido la comunicación con la Orange Pi 5.
  - **Escenario 2:** Dado que la alerta de desconexión está activa, Cuando el hardware recupera la conexión y se reanuda el envío de métricas al servidor, Entonces el sistema detecta los paquetes y oculta automáticamente la alerta.

### HU: PB-HM-56.1
- **Código PB Padre:** PB-HM-56
- **Actor:** Todos
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero aplicar el cierre automático de sesión por inactividad tras 30 minutos para garantizar la seguridad de mi cuenta y evitar exposiciones en caso de dejar el equipo desatendido.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que me encuentro autenticado en el sistema, Cuando registro un periodo ininterrumpido de 30 minutos sin realizar interacciones (mouse/teclado), Entonces el sistema invalida mi token y me redirige forzosamente a la pantalla de Login.
  - **Escenario 2:** Dado que llevo 25 minutos inactivo, Cuando realizo un movimiento del mouse o pulsación de tecla, Entonces el temporizador interno del sistema se resetea inmediatamente a 0, evitando el cierre de mi sesión.

### HU: PB-HM-57.1
- **Código PB Padre:** PB-HM-57
- **Actor:** Todos
- **Puntos:** 2
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero visualizar los mensajes de error del sistema en lenguaje natural (español) para entender los problemas o advertencias sin ser confundido por texto técnico incomprensible ni detalles del código fuente.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que introduzco datos inválidos en un formulario, Cuando envío la información, Entonces aparece una alerta en español que me dice exactamente qué debo corregir, utilizando colores amigables (ej. amarillo/naranja).
  - **Escenario 2:** Dado que ocurre una falla interna (Status 500) en los servidores del backend, Cuando el frontend procesa la respuesta, Entonces despliega un mensaje rojo estándar tipo "Ha ocurrido un error inesperado, contacte soporte" sin mostrar trazas del código ni tecnologías implicadas.

### HU: PB-HM-58.1
- **Código PB Padre:** PB-HM-58
- **Actor:** Todos
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero tener soporte para modo oscuro y modo claro en toda la interfaz para adaptar la visualización de la plataforma a mi comodidad visual y condiciones lumínicas del entorno.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que me encuentro en las configuraciones de mi perfil, Cuando altero el switch a "Modo Oscuro", Entonces todas las vistas, fondos, tipografías y paletas de color de los gráficos se actualizan de forma instantánea.
  - **Escenario 2:** Dado que he seleccionado una preferencia visual previamente, Cuando inicio una nueva sesión en un dispositivo distinto, Entonces la plataforma recuerda el tema que guardé y lo aplica desde el primer pantallazo de carga.

### HU: PB-HM-59.1
- **Código PB Padre:** PB-HM-59
- **Actor:** Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor / Analista quiero recibir una notificación vía Telegram cuando mis descargas de logs o informes están listas para poder seguir trabajando sin tener que estar comprobando la plataforma manualmente.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que he solicitado una descarga asíncrona masiva de logs y tengo vinculado mi Telegram, Cuando el backend termina de generar el archivo, Entonces el Bot me envía un mensaje avisándome que está listo para ser descargado.
  - **Escenario 2:** Dado que la solicitud de exportación falla a mitad de proceso, Cuando el backend cancela la tarea, Entonces el sistema envía una notificación vía Telegram indicando la falla y sugiriendo que intente de nuevo.

### HU: PB-HM-60.1
- **Código PB Padre:** PB-HM-60
- **Actor:** Sistema
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Sistema quiero eliminar automáticamente los archivos de logs expirados pasados los 7 días para optimizar y asegurar la disponibilidad del espacio en disco del servidor de forma constante.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que existen archivos JSONL generados por descargas pasadas, Cuando el sistema ejecuta el cronjob programado de mantenimiento, Entonces evalúa su fecha de creación y borra permanentemente todos los que superan el límite de 7 días.
  - **Escenario 2:** Dado que el cron evalúa un archivo generado hace 4 días, Cuando detecta su fecha, Entonces lo ignora y lo mantiene disponible en el volumen de almacenamiento sin realizar ninguna acción.

### HU: PB-HM-64.1
- **Código PB Padre:** PB-HM-64
- **Actor:** Analista / Administrador
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Analista / Administrador quiero contar con un panel de Patch Intelligence (Priorización CVEs) para cruzar los ataques reales recibidos con las vulnerabilidades reportadas y saber qué debo parchar con mayor urgencia.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que un CVE con severidad alta (>7.0) está pendiente por parchar y Wazuh detecta eventos relacionados, Cuando consulto el panel, Entonces el sistema clasifica esta vulnerabilidad con una prioridad crítica como "Parchar HOY".
  - **Escenario 2:** Dado que reviso los CVEs priorizados, Cuando hago clic en ver el detalle de uno, Entonces la interfaz me muestra el número de ataques externos recientes que han intentado explotar esa brecha específica de mi sistema.

### HU: PB-HM-65.1
- **Código PB Padre:** PB-HM-65
- **Actor:** Consultor
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero disponer del Honeypot Advisor para visualizar los diccionarios SSH y nombres de usuario clasificados que emplean los atacantes con el fin de anticipar posibles amenazas dirigidas a perfiles específicos.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que los atacantes han intentado múltiples combinaciones de contraseñas por fuerza bruta, Cuando accedo al Advisor, Entonces se despliegan en listas estadísticas los nombres de usuario más probados en el periodo evaluado.
  - **Escenario 2:** Dado que consulto la lista de usuarios atacados, Cuando reviso el desglose, Entonces veo la información clasificada y categorizada según la industria del software o su finalidad (Ej. nombres de Odoo, Jenkins, Bases de datos, etc.).

### HU: PB-HM-66.1
- **Código PB Padre:** PB-HM-66
- **Actor:** Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero visualizar un Timeline de Integridad (FIM Correlacionado) para rastrear de forma temporal los intentos de penetración y cruzarlos de inmediato con cualquier alteración anómala interna en archivos críticos.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ha ocurrido un potencial compromiso post-explotación, Cuando accedo a la línea de tiempo FIM, Entonces puedo contrastar sincrónicamente sobre el mismo gráfico los intentos de acceso del atacante con la alteración detectada por dpkg.
  - **Escenario 2:** Dado que encuentro un evento anómalo del sistema FIM en el timeline, Cuando clico sobre él, Entonces el panel expande el registro exacto mostrándome qué archivo crítico fue modificado por el posible atacante.

### HU: PB-HM-67.1
- **Código PB Padre:** PB-HM-67
- **Actor:** Analista
- **Puntos:** 13
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero disponer del Kill Chain Visualizer alineado a MITRE ATT&CK para mapear el comportamiento entero de un atacante desde que hace el escaneo hasta los posibles indicios de post-explotación de manera gráfica.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que la IA o Wazuh ha enlazado múltiples eventos de un mismo actor malicioso, Cuando accedo a la vista Kill Chain, Entonces visualizo un diagrama paso a paso acomodando las acciones bajo las tácticas de reconocimiento, persistencia o impacto según MITRE.
  - **Escenario 2:** Dado que selecciono un atacante cuya IP cruzó varias fases, Cuando observo la representación visual, Entonces visualizo flechas y secuencias claras desde la fase exploratoria inicial hasta los eventos críticos más recientes en tiempo real.

### HU: PB-HM-68.1
- **Código PB Padre:** PB-HM-68
- **Actor:** Analista
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero poder utilizar un entorno HITL (Human-in-the-Loop) sobre Rootcheck para validar o rechazar alertas complejas de forma manual y reentrenar de mejor forma el modelo de detección.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que Rootcheck lanza una alerta por un posible troyano en un directorio del sistema (/bin/passwd), Cuando evalúo la información en el panel HITL, Entonces puedo decidir con botones explícitos marcarlo como "Compromiso Confirmado" o "Falso Positivo".
  - **Escenario 2:** Dado que marco el evento como falso positivo, Cuando confirmo mi acción, Entonces el sistema ajusta la alerta en el histórico y etiqueta internamente la firma de ese evento para ser descartado como amenaza en el próximo ciclo de ML.

### HU: PB-HM-69.1
- **Código PB Padre:** PB-HM-69
- **Actor:** Consultor
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero consultar un Dashboard de Compliance basado en el estándar CIS Benchmark para identificar deficiencias de hardening y saber exactamente cómo remediarlas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que Wazuh terminó sus tareas de auditoría de configuración SCA, Cuando cargo el dashboard de Compliance, Entonces observo de manera destacada el porcentaje de cumplimiento CIS general de mi entorno (ej. 45%).
  - **Escenario 2:** Dado que deseo aumentar mi nivel de hardening, Cuando bajo al desglose del reporte, Entonces encuentro listadas las recomendaciones de reparación (remediaciones) jerarquizadas por su peso o impacto sobre el score total del sistema.
