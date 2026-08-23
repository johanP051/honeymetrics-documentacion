# Historias de Usuario — Sprint 2 — HoneyMetrics v2.0

### HU: PB-HM-26.1
- **Código PB Padre:** PB-HM-26
- **Actor:** Dir. T.I / Consultor / Analista / Adm.
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario autorizado quiero visualizar un dashboard principal con KPIs y cuatro gráficos dinámicos (torta para distribución por módulo, líneas spline para histórico, y barras horizontales max 40 caracteres para top agentes y eventos) para monitorear el estado general de las amenazas de forma rápida.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ingreso al sistema exitosamente, Cuando navego a la vista de "Dashboard", Entonces el sistema carga por defecto los datos de los últimos 7 días.
  - **Escenario 2:** Dado que visualizo los gráficos de "Top Agentes" y "Top Eventos", Cuando los nombres exceden la longitud permitida, Entonces el sistema recorta el texto a un máximo de 40 caracteres con puntos suspensivos en los gráficos de barras horizontales.

### HU: PB-HM-27.1
- **Código PB Padre:** PB-HM-27
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero filtrar la información del dashboard principal por rangos de fechas definidos (ej. now-7d/d) para analizar períodos específicos de actividad maliciosa.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que me encuentro en el dashboard principal, Cuando selecciono el filtro de "Últimas 24 horas", Entonces todos los gráficos y KPIs se actualizan instantáneamente sin recargar la página completa.
  - **Escenario 2:** Dado que selecciono un rango de fechas personalizado, Cuando el rango no tiene datos registrados, Entonces los gráficos muestran un mensaje amigable indicando "No hay datos disponibles para el rango seleccionado".

### HU: PB-HM-28.1
- **Código PB Padre:** PB-HM-28
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero visualizar un Mapa de Calor Interactivo mundial para identificar visualmente de qué países provienen la mayor cantidad de ataques.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ingreso a la sección del mapa de calor, Cuando el mapa termina de cargar, Entonces los países atacantes se pintan en una escala de verde a rojo dependiendo de la intensidad del ataque y se muestra una tabla de "Top 10 Países Atacantes".
  - **Escenario 2:** Dado que observo el mapa interactivo, Cuando paso el cursor (hover) sobre un país en rojo, Entonces aparece un tooltip mostrando el nombre del país y la cantidad total de eventos registrados.

### HU: PB-HM-29.1
- **Código PB Padre:** PB-HM-29
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero filtrar el Mapa de Calor por tipo de ataque específico para entender la distribución geográfica de amenazas particulares.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que visualizo el mapa de calor, Cuando selecciono "Fuerza Bruta SSH" en el selector de tipo de ataque, Entonces el mapa y el ranking se recalculan únicamente con los datos de ese tipo de ataque.
  - **Escenario 2:** Dado que aplico un filtro de ataque, Cuando deseo ver todos los ataques nuevamente, Entonces puedo limpiar el filtro y el mapa restaura la vista global original.

### HU: PB-HM-30.1
- **Código PB Padre:** PB-HM-30
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero ver un panel lateral con información detallada al seleccionar un país en el mapa de calor para obtener un desglose profundo de los incidentes provenientes de esa región.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que navego en el mapa de calor, Cuando hago clic izquierdo sobre "Rusia", Entonces se despliega un panel lateral derecho mostrando el top de IPs, los tipos de ataque y los periodos de actividad de ese país.
  - **Escenario 2:** Dado que tengo el panel lateral abierto, Cuando hago clic fuera del panel o en el botón "Cerrar", Entonces el panel se oculta y puedo seguir interactuando con el mapa mundial completo.

### HU: PB-HM-31.1
- **Código PB Padre:** PB-HM-31
- **Actor:** Dir. T.I / Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario autorizado quiero acceder a una vista de Estadística Descriptiva (media, mediana, moda, varianza, histograma, boxplot) para analizar el comportamiento profundo de las variables numéricas de los ataques.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ingreso a la vista de estadísticas descriptivas, Cuando selecciono la variable "Volumen de alertas por hora", Entonces se calculan la media, mediana, moda y desviación estándar, mostrándose un histograma de frecuencias.
  - **Escenario 2:** Dado que analizo la misma variable, Cuando visualizo la sección inferior de la pantalla, Entonces observo un diagrama de caja (boxplot) que me permite identificar visualmente los valores atípicos (outliers).

### HU: PB-HM-32.1
- **Código PB Padre:** PB-HM-32
- **Actor:** Dir. T.I / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero filtrar las estadísticas descriptivas por diferentes variables y rangos de fecha para personalizar mi análisis según el contexto temporal requerido.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que estoy viendo estadísticas descriptivas, Cuando cambio la variable analizada a "Duración del ataque en segundos", Entonces todos los cálculos y gráficos se actualizan inmediatamente con la nueva variable.
  - **Escenario 2:** Dado que ajusto el rango de fechas al "Mes pasado", Cuando se aplican los filtros, Entonces los resultados estadísticos reflejan de manera exacta únicamente los eventos que sucedieron en ese mes.

### HU: PB-HM-33.1
- **Código PB Padre:** PB-HM-33
- **Actor:** Analista
- **Puntos:** 2
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero poder descargar la tabla de métricas estadísticas en formato CSV para poder integrar estos resultados en reportes externos o presentaciones de gestión.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que he calculado medidas estadísticas, Cuando hago clic en el botón "Exportar CSV", Entonces el sistema genera y descarga un archivo CSV con las métricas actualmente mostradas en pantalla.
  - **Escenario 2:** Dado que no hay datos para el rango seleccionado, Cuando intento exportar, Entonces el botón de exportación se encuentra deshabilitado para evitar archivos vacíos.

### HU: PB-HM-34.1
- **Código PB Padre:** PB-HM-34
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario autorizado quiero visualizar una Matriz de Confusión interactiva (VP, FP, VN, FN) y sus indicadores derivados (Accuracy, Precision, Recall, F1) para evaluar la eficacia del modelo de IA en la detección.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que navego al panel de IA, Cuando el componente carga, Entonces visualizo una matriz 2x2 coloreada con tooltips explicativos que indican el significado de Verdaderos Positivos, Falsos Positivos, etc.
  - **Escenario 2:** Dado que visualizo el panel de IA, Cuando observo la parte inferior, Entonces veo tarjetas (cards) resaltando los porcentajes de Accuracy, Precision, Recall y F1-Score calculados.

### HU: PB-HM-35.1
- **Código PB Padre:** PB-HM-35
- **Actor:** Dir. T.I / Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero aplicar filtros temporales y de tipo de ataque a la Matriz de Confusión para medir cómo se comporta el modelo bajo condiciones y periodos específicos.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que estoy en el dashboard de la Matriz de Confusión, Cuando aplico el filtro de ataque "Inyección SQL", Entonces la matriz y las métricas F1/Recall se recalculan solo con los intentos de SQLi.
  - **Escenario 2:** Dado que selecciono un rango muy pequeño donde no hay predicciones, Cuando se actualiza la matriz, Entonces el sistema muestra 0 en las celdas y N/A en las métricas de rendimiento.

### HU: PB-HM-36.1
- **Código PB Padre:** PB-HM-36
- **Actor:** Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero hacer clic en una celda de la Matriz de Confusión (ej. Falsos Positivos) para desplegar una tabla con el detalle de las predicciones fallidas y analizarlas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que visualizo la matriz, Cuando hago clic en el cuadrante de "Falsos Positivos", Entonces se abre una tabla expansible listando la IP, fecha, clasificación real vs predicha y el % de confianza de la predicción.
  - **Escenario 2:** Dado que estoy analizando la tabla de Falsos Positivos, Cuando termino la inspección, Entonces puedo contraer la tabla fácilmente pulsando el botón de cierre para volver a la matriz completa.

### HU: PB-HM-37.1
- **Código PB Padre:** PB-HM-37
- **Actor:** Consultor / Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero solicitar la extracción de logs crudos (JSONL) estableciendo un rango de fechas de manera que el sistema lo procese de forma asíncrona sin bloquear la interfaz.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que estoy en el panel de extracción de logs, Cuando solicito logs de la última semana y hago clic en "Procesar", Entonces el sistema registra la petición con estado "Procesando" y me permite seguir navegando por la web.
  - **Escenario 2:** Dado que la solicitud se encuentra en segundo plano, Cuando el backend termina de construir el archivo JSONL, Entonces el estado de la tarea cambia automáticamente a "Listo".

### HU: PB-HM-38.1
- **Código PB Padre:** PB-HM-38
- **Actor:** Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero consultar el historial de mis solicitudes de descarga de logs en una tabla que se actualiza periódicamente para rastrear cuáles están listas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que abro la vista de historial de descargas, Cuando el componente carga, Entonces muestra mis solicitudes pasadas con ID, rango, total de registros, estado y fecha de creación.
  - **Escenario 2:** Dado que tengo una extracción en estado "Procesando", Cuando mantengo la vista abierta por 10 segundos, Entonces el frontend realiza un chequeo silencioso (polling/SSE) y actualiza el estado a "Listo" si finalizó, sin necesidad de refrescar el navegador.

### HU: PB-HM-39.1
- **Código PB Padre:** PB-HM-39
- **Actor:** Consultor / Analista
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero descargar el archivo de logs JSONL una vez procesado haciendo clic en un botón para almacenarlo en mi equipo local.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que tengo una solicitud en estado "Listo", Cuando presiono el icono de descarga, Entonces el navegador inicia la descarga del archivo .jsonl y el sistema me advierte que expirará en 7 días.
  - **Escenario 2:** Dado que una solicitud lleva más de 7 días lista, Cuando intento verla, Entonces el sistema la marca como "Expirada" y el botón de descarga desaparece, informando que el archivo fue eliminado para liberar espacio.

### HU: PB-HM-40.1
- **Código PB Padre:** PB-HM-40
- **Actor:** Consultor / Analista
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero que las solicitudes de descarga de logs masivos (>50,000 registros) queden "Pendientes" y envíen una alerta al Administrador vía Telegram para obtener aprobación y evitar abusos del sistema.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que configuro una solicitud de logs que abarcará 75,000 eventos, Cuando hago clic en "Procesar", Entonces la UI me avisa que requiere aprobación manual y el estado inicial es "Pendiente de Aprobación".
  - **Escenario 2:** Dado que la solicitud supera el umbral crítico, Cuando se registra en base de datos, Entonces el backend despacha instantáneamente un webhook o mensaje al bot de Telegram del Administrador informando de los detalles de la solicitud y botones interactivos.

### HU: PB-HM-41.1
- **Código PB Padre:** PB-HM-41
- **Actor:** Administrador
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Administrador quiero poder aprobar o rechazar desde Telegram (mediante el Bot interactivo) las descargas masivas de logs para tener control inmediato sin necesidad de entrar a la plataforma web.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que recibo el mensaje de alerta en Telegram, Cuando presiono el botón "Aprobar", Entonces el backend valida mi cuenta de Telegram, marca la solicitud como "Aprobada" y encola la generación asíncrona del archivo JSONL.
  - **Escenario 2:** Dado que determino que la petición es sospechosa o muy costosa computacionalmente, Cuando presiono "Rechazar" en Telegram, Entonces el estado en el frontend cambia a "Rechazada" y la descarga se bloquea.

### HU: PB-HM-42.1
- **Código PB Padre:** PB-HM-42
- **Actor:** Analista
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero generar client-side un Diccionario de Datos en PDF con el esquema de campos Wazuh para tener documentación estandarizada lista para presentar o para entrenar modelos.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que estoy en la vista de Logs, Cuando hago clic en "Generar Diccionario PDF", Entonces la aplicación web (React) construye en local el documento utilizando jsPDF + AutoTable y lanza la descarga de forma rápida.
  - **Escenario 2:** Dado que abro el PDF descargado, Cuando reviso el contenido, Entonces el documento incluye logotipo de HoneyMetrics, marca de tiempo de la generación, y una tabla describiendo el atributo, tipo de dato y descripción del modelo Wazuh.

### HU: PB-HM-43.1
- **Código PB Padre:** PB-HM-43
- **Actor:** Dir. T.I / Consultor
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero generar informes ejecutivos en CSV o Excel de manera asíncrona, con barra de progreso, para poder consolidar el resumen gerencial de incidentes de un periodo dado.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que selecciono un informe de tipo "Ejecutivo", Cuando pulso en "Generar Reporte", Entonces se muestra una barra de progreso que consulta el estado asíncrono y, al finalizar, me entrega el .xlsx listo.
  - **Escenario 2:** Dado que la solicitud del reporte implica un archivo extremadamente pesado, Cuando el servidor finaliza la construcción, Entonces el peso final no debe superar el límite duro configurado de 50 MB, informando en caso de truncamiento.

### HU: PB-HM-44.1
- **Código PB Padre:** PB-HM-44
- **Actor:** Consultor
- **Puntos:** 8
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero recibir alertas emergentes en pantalla cada vez que el sistema detecte anomalías críticas (ej. pico >300%) para poder actuar inmediatamente frente a ráfagas de ataques.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que el backend identifica un pico anómalo de severidad máxima, Cuando el frontend recibe el evento (via WebSocket/SSE), Entonces lanza un pop-up rojo persistente en mi pantalla con resumen y los botones "Ver Detalle" y "Descartar".
  - **Escenario 2:** Dado que hay múltiples anomalías sucesivas, Cuando el sistema lanza alertas, Entonces se aplica una política de "Debounce" que asegura que no haya más de un pop-up crítico cada 30 segundos para evitar saturación de la interfaz (alert fatigue).

### HU: PB-HM-45.1
- **Código PB Padre:** PB-HM-45
- **Actor:** Consultor
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero tener un panel lateral con el historial de alertas críticas recibidas en las últimas 24 horas para revisar eventos que pude haber descartado o ignorado rápidamente.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que abro el Drawer/Panel lateral de notificaciones, Cuando cargo la vista, Entonces veo la lista de anomalías del último día con estado claro (Atendida, Descartada, Ignorada).
  - **Escenario 2:** Dado que busco una alerta del día anterior, Cuando han pasado más de 24 horas, Entonces dicha alerta ya no figura en el panel lateral de "alertas rápidas" (aunque siga registrada en base de datos).

### HU: PB-HM-46.1
- **Código PB Padre:** PB-HM-46
- **Actor:** Consultor
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero hacer clic en "Ver Detalle" de una alerta para acceder a la radiografía completa del evento y tomar decisiones operativas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que interactúo con una alerta crítica, Cuando presiono "Ver Detalle", Entonces se abre un modal con el historial de la IP, gráfico temporal y tabla de los eventos específicos involucrados.
  - **Escenario 2:** Dado que analizo el detalle del evento en el modal, Cuando observo la parte inferior, Entonces el sistema me expone los botones rápidos "Agregar a Lista Negra" y "Marcar como Falso Positivo".

### HU: PB-HM-47.1
- **Código PB Padre:** PB-HM-47
- **Actor:** Consultor
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como Consultor quiero marcar una alerta como Falso Positivo desde su panel de detalle para que el modelo de IA se reentrene y deje de catalogar tráfico benigno similar como ataque.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que verifico que la IP de la alerta es un escáner interno autorizado, Cuando hago clic en "Marcar como Falso Positivo", Entonces el sistema pide confirmación y actualiza el estado de la alerta.
  - **Escenario 2:** Dado que se marca como Falso Positivo, Cuando la base de datos se actualiza, Entonces el registro es etiquetado internamente (flag) de manera que se excluya de métricas de riesgo y se envíe a la cola de "Dataset para Reentrenamiento".

### HU: PB-HM-62.1
- **Código PB Padre:** PB-HM-62
- **Actor:** Analista
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero que el sistema me sugiera el bloqueo de rangos CIDR (/24) tras identificar subredes (Botnets) que atacan coordinadamente para mitigar ataques distribuidos masivos más eficientemente.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que el sistema analiza tráfico en tiempo real, Cuando detecta múltiples IPs de la misma subred (ej. 192.168.1.x/24) atacando el honeypot simultáneamente, Entonces genera una recomendación visual de bloqueo CIDR.
  - **Escenario 2:** Dado que consulto la sugerencia, Cuando reviso el detalle, Entonces veo el volumen consolidado del bloque completo en lugar de ver registros aislados IP por IP.

### HU: PB-HM-63.1
- **Código PB Padre:** PB-HM-63
- **Actor:** Analista
- **Puntos:** 5
- **Estado:** Sin empezar
- **Narrativa:** Como Analista quiero un clasificador de comportamiento que distinga entre Bots automatizados y Humanos manuales utilizando su velocidad de eventos para priorizar amenazas dirigidas.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que una IP dispara más de 100 eventos maliciosos por hora en el honeypot, Cuando es analizada por el sistema, Entonces se etiqueta automáticamente como "Bot".
  - **Escenario 2:** Dado que una IP intenta accesos espaciados y lentos, Cuando la velocidad es inferior a los umbrales de ataque automatizado, Entonces el sistema la etiqueta como "Humano" y aumenta su prioridad en el dashboard de revisiones manuales.

### HU: PB-HM-70.1
- **Código PB Padre:** PB-HM-70
- **Actor:** Todos
- **Puntos:** 3
- **Estado:** Sin empezar
- **Narrativa:** Como usuario quiero visualizar un Heatmap de Riesgo Predictivo (días vs horas) para anticipar los horarios de mayor exposición y preparar defensas o ventanas de mantenimiento.
- **Criterios de Aceptación:**
  - **Escenario 1:** Dado que ingreso al dashboard, Cuando visualizo la sección del Heatmap Predictivo, Entonces veo una cuadrícula que compara los 7 días de la semana contra las 24 horas del día.
  - **Escenario 2:** Dado que el heatmap carga la historia, Cuando observo celdas coloreadas de rojo oscuro (Ej. Lunes de 11:00 a 12:00 UTC), Entonces interpreto que, según el patrón histórico, ese bloque de tiempo presentará el mayor volumen probable de ataques en el futuro.
