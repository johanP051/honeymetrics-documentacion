> **Ver también:** [Inicio](index.md) · [Manual Técnico & Arquitectura](manual-tecnico.md) · [Diccionario de Datos](diccionario-datos.md) · [Despliegue & Operaciones](guia-despliegue.md)

## Índice

- [1. Introducción](#1-introduccion)
- [2. Objetivo](#2-objetivo)
- [3. Alcance](#3-alcance)
- [4. Requisitos para usar HoneyMetrics](#4-requisitos-para-usar-honeymetrics)
  - [4.1 Conocimientos previos](#41-conocimientos-previos)
  - [4.2 Requisitos de hardware recomendados](#42-requisitos-de-hardware-recomendados)
  - [4.3 Conexión a internet](#43-conexion-a-internet)
  - [4.4 Credenciales y custodia de acceso](#44-credenciales-y-custodia-de-acceso)
- [5. Aplicaciones de software](#5-aplicaciones-de-software)
  - [5.1 Navegador web](#51-navegador-web)
  - [5.2 Aplicación autenticadora móvil (MFA / TOTP)](#52-aplicacion-autenticadora-movil-mfa-totp)
  - [5.3 Cliente de correo electrónico](#53-cliente-de-correo-electronico)
  - [5.4 Aplicación de mensajería Telegram](#54-aplicacion-de-mensajeria-telegram)
  - [5.5 Visores de archivos (JSONL y PDF)](#55-visores-de-archivos-jsonl-y-pdf)
- [6. Funcionalidades generales](#6-funcionalidades-generales)
  - [6.1 Inicio de sesión seguro](#61-inicio-de-sesion-seguro)
  - [6.2 Configuración y verificación de Autenticación de Doble Factor (MFA)](#62-configuracion-y-verificacion-de-autenticacion-de-doble-factor-mfa)
  - [6.3 Cierre de sesión seguro](#63-cierre-de-sesion-seguro)
  - [6.4 Recuperación de contraseña olvidada](#64-recuperacion-de-contrasena-olvidada)
  - [6.5 Gestión de perfil, preferencias visuales y cambio de clave](#65-gestion-de-perfil-preferencias-visuales-y-cambio-de-clave)
  - [6.6 Tutorial paso a paso: Vinculación con Telegram](#66-tutorial-paso-a-paso-vinculacion-con-telegram)
- [7. Funcionalidades operativas (Núcleo del sistema)](#7-funcionalidades-operativas-nucleo-del-sistema)
  - [7.1 Dashboard de Inteligencia de Amenazas (CTI)](#71-dashboard-de-inteligencia-de-amenazas-cti)
  - [7.2 Threat Center (Gestión de Lista Negra de IPs Maliciosas)](#72-threat-center-gestion-de-lista-negra-de-ips-maliciosas)
  - [7.3 Solicitud, Aprobación y Descarga de Logs & Reportes](#73-solicitud-aprobacion-y-descarga-de-logs-reportes)
- [8. Funcionalidades específicas por rol](#8-funcionalidades-especificas-por-rol)
  - [8.1 Rol: Administrador](#81-rol-administrador)
  - [8.2 Rol: Consultor de Ciberseguridad](#82-rol-consultor-de-ciberseguridad)
  - [8.3 Rol: Analista de Datos](#83-rol-analista-de-datos)
  - [8.4 Rol: Directivo de T.I.](#84-rol-directivo-de-ti)
- [9. Preguntas frecuentes y resolución de problemas](#9-preguntas-frecuentes-y-resolucion-de-problemas)

# Manual de Usuario de HoneyMetrics v2.0

## 1. Introducción

HoneyMetrics v2.0 es una plataforma web especializada en Inteligencia de Amenazas Cibernéticas (*Cyber Threat Intelligence - CTI*) y monitoreo avanzado de sensores trampa (*honeypots*).

HoneyMetrics actúa como un centro de mando operativo que transforma volúmenes masivos de registros crudos y telemetría de eventos de seguridad en información clara, estructurada y accionable para los equipos de respuesta y toma de decisiones. A través de una interfaz moderna y reactiva, la plataforma permite supervisar ataques dirigidos contra la infraestructura, catalogar direcciones IP hostiles, anticipar patrones anómalos de tráfico mediante algoritmos predictivos y coordinar flujos de exportación controlada de evidencias forenses.

Este manual ha sido redactado con un enfoque 100% centrado en el operador humano, prescindiendo deliberadamente de tecnicismos internos de programación para proporcionar un acompañamiento claro, pedagógico y práctico a lo largo de todas las operaciones disponibles en la interfaz.

---

## 2. Objetivo

Proporcionar a los usuarios de HoneyMetrics una guía operativa integral, didáctica y de consulta ágil que les permita dominar las funciones de la plataforma según su rol asignado.

De manera específica, el manual persigue:

1. Orientar al usuario en el cumplimiento de los requerimientos técnicos de conectividad, hardware y aplicaciones complementarias necesarias para acceder al servicio.
2. Detallar paso a paso los procedimientos de autenticación robusta, matriculación de doble factor (MFA) y vinculación con canales de notificación como Telegram.
3. Explicar en profundidad la interpretación analítica de cada componente visual del Dashboard, la administración de indicadores en el Threat Center y la solicitud controlada de registros forenses.
4. Delimitar las capacidades, restricciones y mejores prácticas operativas para cada uno de los cuatro roles del sistema: *Administrador*, *Consultor de Ciberseguridad*, *Analista de Datos* y *Directivo de T.I.*
5. Brindar soluciones inmediatas ante los incidentes y dudas más frecuentes de operación diaria.

---

## 3. Alcance

Este manual cubre el ciclo completo de interacción del usuario con HoneyMetrics v2.0 a través de su interfaz web accesible desde cualquier navegador moderno. Incluye:

- **Gestión de Identidad y Seguridad Personal:** Inicio de sesión, matriculación y validación de doble factor (TOTP), recuperación autónoma de credenciales, cambio de clave con medidor visual de robustez y vinculación con Telegram.
- **Visualización y Analítica CTI:** Interpretación de indicadores clave de rendimiento (KPIs), líneas de tiempo de eventos, categorización por severidad, mapa térmico predictivo y recomendaciones del asistente inteligente.
- **Operación de Lista Negra (Threat Center):** Búsqueda predictiva, registro de indicadores con puntuación de riesgo, actualización de contexto y consulta de la bóveda forense de registros archivados.
- **Extracción de Evidencias Forenses:** Solicitud de logs de seguridad, seguimiento del ciclo de vida de cada solicitud, descarga de archivos en formato JSONL y emisión de reportes ejecutivos consolidados en formato PDF.
- **Gobernanza y Roles:** Alcance funcional de los cuatro perfiles de usuario, administración de cuentas y flujo interactivo de aprobación de descargas masivas vía Telegram para administradores.

!!! note "⚡ Nota de Alcance"
    El manual no cubre tareas de administración interna del servidor físico, configuración del motor de bases de datos PostgreSQL ni orquestación de contenedores Docker en infraestructura, aspectos documentados en el [Manual Técnico & Arquitectura](manual-tecnico.md) y la [Guía de Despliegue & Operaciones](guia-despliegue.md).

---

## 4. Requisitos para usar HoneyMetrics

Para garantizar una experiencia óptima y segura al operar HoneyMetrics, el usuario debe verificar el cumplimiento de los siguientes requisitos previos:

### 4.1 Conocimientos previos

- Manejo básico de navegadores de internet y aplicaciones web modernas.
- Comprensión elemental de conceptos de ciberseguridad: dirección IP, puerto de red, intento de intrusión, severidad de alerta e indicador de compromiso (IOC).
- Familiaridad con el uso de aplicaciones móviles de autenticación en dos pasos (como Google Authenticator o Microsoft Authenticator).

### 4.2 Requisitos de hardware recomendados

- **Procesador:** Intel Core i3 de séptima generación o superior (o procesador equivalente AMD Ryzen 3).
- **Memoria RAM:** Mínimo 4 GB disponibles; se recomiendan 8 GB para una navegación fluida al renderizar gráficas con alta densidad de datos.
- **Almacenamiento en disco:** Al menos 500 MB de espacio libre disponible para el almacenamiento local de reportes en PDF y archivos de telemetría forense (.jsonl).
- **Resolución de pantalla:** Resolución mínima recomendada de 1366 × 768 píxeles (pantallas Full HD 1920 × 1080 brindan el mejor confort visual en paneles de gráficos y tablas de indicadores).

### 4.3 Conexión a internet

- Ancho de banda estable de al menos 5 Mbps de bajada y 2 Mbps de subida.
- Conectividad segura mediante protocolo HTTPS hacia la dirección web o dominio corporativo proporcionado por el departamento de tecnología.

### 4.4 Credenciales y custodia de acceso

- Contar con un nombre de usuario o correo electrónico corporativo registrado previamente por el Administrador de la plataforma.
- Disponer de un dispositivo móvil inteligente (Android o iOS) con cámara funcional para el escaneo del código QR durante la activación del doble factor de autenticación.
- Custodiar estrictamente las contraseñas y códigos temporales generados; queda prohibido compartir credenciales con terceros o anotarlas en lugares visibles.

---

## 5. Aplicaciones de software

El ecosistema de HoneyMetrics interactúa de forma complementaria con herramientas comunes de productividad y seguridad que deben estar instaladas en su estación de trabajo o dispositivo móvil:

### 5.1 Navegador web
La plataforma ha sido construida para operar en navegadores web de última generación con soporte para HTML5, CSS3 y JavaScript moderno:

- Google Chrome (versión 110 o superior).
- Mozilla Firefox (versión 110 o superior).
- Microsoft Edge (versión 110 o superior).
- Brave Browser o navegadores basados en Chromium.
- Apple Safari (versión 16 o superior en macOS / iOS).

!!! note "⚡ Nota"
    HoneyMetrics está optimizado para estándares web contemporáneos. No se garantiza el funcionamiento en Microsoft Internet Explorer o navegadores desactualizados. Asegúrese de mantener su navegador actualizado para disfrutar de todas las transiciones visuales y medidas de protección criptográfica.

### 5.2 Aplicación autenticadora móvil (MFA / TOTP)
Es un requisito obligatorio para acceder a la plataforma. Debe instalar en su teléfono inteligente cualquiera de las siguientes aplicaciones gratuitas de generación de códigos de un solo uso (TOTP):

- **Google Authenticator** (disponible en Google Play Store y Apple App Store).
- **Microsoft Authenticator**.
- **Twilio Authy**.
- **1Password / Bitwarden** (con función de autenticador incorporada).

### 5.3 Cliente de correo electrónico
Cualquier cliente de correo (Gmail, Microsoft Outlook, Thunderbird o webmail corporativo) con acceso a la bandeja de entrada de la cuenta registrada, necesario para recibir los enlaces de recuperación de contraseña en caso de olvido.

### 5.4 Aplicación de mensajería Telegram
Recomendada para todos los usuarios y **obligatoria para los Administradores**:

- Aplicación de Telegram instalada en su teléfono móvil o en su computadora (Telegram Desktop o versión Web).
- Permite a los operadores recibir notificaciones automáticas inmediatas cuando sus extracciones de logs están listas para descarga.
- Permite a los Administradores recibir solicitudes de aprobación para descargas masivas y autorizarlas o denegarlas mediante botones interactivos directamente en el chat.

### 5.5 Visores de archivos (JSONL y PDF)

- **Para archivos JSONL:** Editores avanzados de texto y código como Visual Studio Code, Notepad++, Sublime Text, o utilidades de línea de comandos como `jq`.
- **Para reportes ejecutivos PDF:** Cualquier visor estándar de documentos PDF como Adobe Acrobat Reader, Foxit Reader o el propio visor integrado de su navegador web.

---

## 6. Funcionalidades generales

Estas funciones se encuentran disponibles para todos los usuarios autenticados, sin importar el rol asignado.

### 6.1 Inicio de sesión seguro
Para ingresar a HoneyMetrics:

1. Abra su navegador web y digite la dirección URL oficial provista por el departamento de tecnología (por ejemplo, `https://honeymetrics-frontend.johan-sebastianposada.workers.dev/` o la dirección local designada).
2. La pantalla de bienvenida le presentará el formulario de autenticación con fondo de ciberseguridad.
3. En el campo **Usuario o Correo Electrónico**, escriba su identificador registrado.
4. En el campo **Contraseña**, escriba su clave personal. Puede hacer clic sobre el **ícono del ojo** ubicado a la derecha del campo para alternar la visualización y verificar que los caracteres ingresados sean correctos.
5. Haga clic sobre el botón **Iniciar Sesión**.

<video poster="../assets/screenshots/fig01_login.png" controls width="100%" playsinline class="docs-video">
  <source src="../assets/videos/01_login_y_navegacion.mp4" type="video/mp4">
  Su navegador no soporta la reproducción de video HTML5.
</video>
*Video 1. Inicio de sesión institucional y recorrido inicial de navegación.*

![Figura 1. Formulario de acceso al sistema con opción de verificación visual de contraseña](assets/screenshots/fig01_login.png)
*Figura 1. Formulario de acceso al sistema con opción de verificación visual de contraseña.*

![Figura 1b. Interfaz responsiva adaptada a dispositivos móviles](assets/screenshots/fig01b_mobile_landing.png)
*Figura 1b. Interfaz responsiva adaptada a dispositivos móviles (390×844 px).*

!!! note "⚡ Nota de Seguridad"
    Si introduce credenciales incorrectas, el sistema emitirá un aviso visual de error. Por políticas de protección contra ataques de fuerza bruta, el número de intentos consecutivos está limitado. Si no recuerda su clave, utilice la opción de recuperación explicada más adelante.

### 6.2 Configuración y verificación de Autenticación de Doble Factor (MFA)
El sistema exige de forma obligatoria la validación por dos factores para proteger las cuentas contra accesos no autorizados.

**A. Configuración Inicial (Primer Ingreso del Usuario):**

1. Al autenticarse exitosamente por primera vez, el sistema detectará que su cuenta aún no tiene enrolado un dispositivo y desplegará automáticamente la ventana modal **Configuración de Autenticación de Doble Factor (MFA)**.
2. En la pantalla se mostrará un **código QR bidimensional** junto con una clave secreta alfanumérica de respaldo.
3. Abra su aplicación autenticadora en el teléfono móvil (ej. Google Authenticator) y pulse sobre el botón **Añadir cuenta (+)**.
4. Seleccione la opción **Escanear código QR** y apunte la lente de la cámara hacia la pantalla de su computador. Si la cámara presenta inconvenientes, elija *Introducir clave manualmente* y escriba la clave alfanumérica provista en pantalla.
5. Su aplicación registrará de inmediato la entrada bajo el nombre **HoneyMetrics** y comenzará a generar códigos numéricos dinámicos de seis dígitos que cambian cada 30 segundos.
6. En el formulario web, escriba en la casilla de verificación el código de 6 dígitos que observa actualmente en su teléfono y haga clic en **Confirmar y Activar MFA**. El sistema validará la sincronización y habilitará el ingreso a la plataforma.

![Figura 2. Proceso de enrolamiento de doble factor con código QR](assets/screenshots/fig02_mfa_enrolamiento.png)
*Figura 2. Proceso de enrolamiento de doble factor con código QR y censura de seguridad.*

**B. Verificación en Inicios de Sesión Posteriores:**

1. Tras ingresar su usuario y contraseña en los accesos cotidianos, el sistema le presentará de inmediato el paso de validación temporal.
2. Abra su aplicación autenticadora móvil y consulte el código de 6 dígitos vigente para HoneyMetrics.
3. Ingréselo en el recuadro numérico y haga clic en **Verificar Código**.

!!! note "⚡ Nota de Tolerancia Horaria"
    El sistema admite una ventana de tolerancia temporal de ±30 segundos para compensar pequeñas desincronizaciones horarias en los dispositivos móviles. Si el código está a punto de expirar en su teléfono (círculo temporizador en rojo), espere a que aparezca el siguiente código de 6 dígitos antes de hacer clic en Verificar.

### 6.3 Cierre de sesión seguro
Para salvaguardar la confidencialidad de la información, el usuario dispone de dos mecanismos inmediatos para cerrar su sesión:

- **Desde la barra superior de navegación:** Haga clic sobre el ícono de salida rápida ubicado en la esquina superior derecha de la interfaz.
- **Desde el menú de usuario:** Haga clic sobre su fotografía o nombre de perfil en la esquina superior derecha y seleccione la opción **Cerrar Sesión** en el menú desplegable.

El sistema destruirá inmediatamente la sesión local y redirigirá al navegador a la pantalla pública de bienvenida.

!!! warning "⚡ Recomendación Vital"
    Recuerde cerrar sesión siempre que se ausente de su estación de trabajo o cuando opere desde un equipo compartido en salas de monitoreo.

### 6.4 Recuperación de contraseña olvidada
Si ha olvidado su contraseña de acceso, puede restablecerla de forma autónoma mediante el siguiente procedimiento:

1. En la pantalla principal de inicio de sesión, haga clic en el enlace **¿Olvidó su contraseña?**.
2. En la ventana emergente, ingrese la dirección de correo electrónico institucional asociada a su usuario.
3. Haga clic en el botón **Enviar Enlace de Recuperación**. El sistema procesará la solicitud y emitirá una confirmación en pantalla.
4. Diríjase a su bandeja de entrada de correo electrónico y localice el mensaje remitido por HoneyMetrics (verifique también su carpeta de correo no deseado o *Spam*).
5. Abra el mensaje y haga clic sobre el enlace seguro de restablecimiento, el cual cuenta con un período de validez temporal limitado por seguridad.
6. El enlace le conducirá a una pantalla especial donde deberá escribir su **Nueva Contraseña** y confirmarla en el segundo campo.
7. Haga clic en **Guardar Contraseña**. El sistema confirmará el cambio exitoso y lo redirigirá a la pantalla de login para que inicie sesión con su nueva clave.

![Figura 3. Pantalla de solicitud y confirmación de enlace de restablecimiento](assets/screenshots/fig03_recuperacion_clave.png)
*Figura 3. Pantalla de solicitud y confirmación de enlace de restablecimiento con protección anti-enumeración.*

### 6.5 Gestión de perfil, preferencias visuales y cambio de clave
Para acceder a la administración de su perfil personal:

1. Despliegue el menú de usuario en la esquina superior derecha y seleccione **Mi Perfil** (o ingrese a **Configuración** desde el menú lateral).
2. En este módulo podrá gestionar:

   - **Foto y datos personales:** Visualizar su nombre, correo y rol asignado.
   - **Tema de la interfaz (Personalización visual):** HoneyMetrics permite alternar entre dos temas:

     - *Tema Oscuro (Dark CTI - Predeterminado):* Fondo grafito profundo y acentos de color cian/ámbar, especialmente diseñado para salas de operaciones de seguridad (SOC) y jornadas prolongadas.
     - *Tema Claro (Light):* Fondo limpio en tonos claros, óptimo para entornos con alta iluminación natural.
   - **Zona horaria:** Configuración de la zona horaria geográfica para que todas las marcas de tiempo de las alertas en gráficas y tablas se muestren adaptadas a su horario local.
   - **Cambio de clave activa:** En la sección *Cambiar Contraseña*, introduzca su contraseña actual, seguida de la nueva contraseña y su confirmación.
   - **Medidor visual de fortaleza:** Mientras escribe la nueva clave, una barra interactiva de tres colores le indicará el nivel de seguridad alcanzado:

     - *Rojo (Débil):* Clave muy corta o predecible (menos de 8 caracteres o puramente alfabética).
     - *Amarillo (Media):* Cumple con la longitud básica pero requiere mayor variedad de caracteres.
     - *Verde (Fuerte):* Contraseña robusta que combina mayúsculas, minúsculas, números y caracteres especiales.

### 6.6 Tutorial paso a paso: Vinculación con Telegram
Vincular su cuenta de Telegram le permite recibir alertas automáticas cuando sus solicitudes de exportación de logs estén listas para descarga, y a los Administradores les permite autorizar solicitudes masivas desde su teléfono móvil.

Siga estos pasos sencillos para obtener su identificador numérico y vincularlo en la plataforma:

**Paso 1: Obtener su ID de Chat mediante `@userinfobot`**

1. Abra su aplicación de Telegram (en su teléfono móvil o en su computadora).
2. En la barra superior de búsqueda de Telegram, escriba: `@userinfobot`.
3. Seleccione el bot oficial identificado con dicho nombre (suelen acompañarlo títulos como *User Info Bot* o *Get ID*).
4. Inicie el chat y envíe el comando: `/start`.
5. El bot responderá de forma instantánea con un mensaje que contiene sus datos de usuario de Telegram, incluyendo una línea rotulada como `Id: 123456789` (una secuencia de números enteros).
6. Copie ese número entero de identificación en su portapapeles.

**Paso 2: Iniciar conversación con el bot de HoneyMetrics**

1. Regrese a la barra de búsqueda de Telegram y escriba: `@HoneyMetrics` (o el nombre exacto del bot institucional configurado).
2. Seleccione el bot de la lista de resultados.
3. En la parte inferior de la conversación, pulse el botón **Iniciar** o envíe el comando `/start`. Este paso es indispensable para autorizar al bot a remitirle mensajes directos.

**Paso 3: Guardar su ID en la plataforma web**

1. Vuelva a su navegador web donde tiene abierto HoneyMetrics.
2. Ingrese a **Mi Perfil** o **Configuración**.
3. Localice el campo rotulado como **ID de Chat de Telegram**.
4. Pegue allí el número numérico obtenido en el Paso 1.
5. Haga clic en el botón **Guardar Cambios**. A partir de ese instante, su perfil se encuentra oficialmente enlazado para recibir notificaciones operativas.

---

## 7. Funcionalidades operativas (Núcleo del sistema)

El núcleo operativo de HoneyMetrics comprende las tres herramientas principales de análisis, respuesta y extracción de datos forenses:

### 7.1 Dashboard de Inteligencia de Amenazas (CTI)
El Dashboard es la pantalla central de mando y monitoreo situacional de la plataforma. Para acceder, pulse sobre **Dashboard** en el menú de navegación lateral.

<video poster="../assets/screenshots/fig04_dashboard_cti.png" controls width="100%" playsinline class="docs-video">
  <source src="../assets/videos/02_dashboard_cti_filtros.mp4" type="video/mp4">
  Su navegador no soporta la reproducción de video HTML5.
</video>
*Video 2. Filtrado dinámico de eventos, exploración de gráficos Plotly y recomendaciones defensivas.*

![Figura 4. Panel de visualización ejecutiva y táctica de inteligencia de amenazas](assets/screenshots/fig04_dashboard_cti.png)
*Figura 4. Panel de visualización ejecutiva y táctica de inteligencia de amenazas (Dashboard CTI).*

El panel se compone de los siguientes elementos visuales y analíticos:

1. **Selector de Período Temporal (Filtros Rápidos):**
   Ubicado en la parte superior derecha del tablero. Permite conmutar la ventana de observación con un solo clic:

   - *Últimas 24 Horas:* Para monitoreo en tiempo real de incidentes del día.
   - *Últimos 7 Días:* Para detectar campañas semanales persistentes.
   - *Últimos 30 Días:* Para análisis mensual y tendencias consolidadas.
   - *Personalizado:* Permite abrir un selector de fechas de inicio y fin para auditar un incidente específico.

2. **Tarjetas de Indicadores Clave de Rendimiento (KPIs):**
   - **Total de Alertas:** Cifra global de intentos de ataque o sondeos registrados por los sensores honeypot en el período seleccionado.
   - **Severidad Promedio:** Puntuación consolidada que mide la criticidad de los eventos analizados en una escala del 1 al 15. Puntuaciones elevadas alertan sobre intentos directos de intrusión o explotación activa.
   - **Alertas Críticas:** Conteo de incidentes de máxima gravedad que requieren atención inmediata de los equipos de respuesta.
   - **Bloqueos Activos:** Número de direcciones IP maliciosas que han sido catalogadas y neutralizadas en las listas negras del sistema.

3. **Línea de Tiempo de Eventos (Evolución Temporal):**
   Gráfica de barras interactivas que muestra la distribución de los ataques hora a hora o día a día. Permite identificar de inmediato picos anómalos de tráfico, ataques de denegación o ráfagas de escaneos masivos. Al pasar el cursor del mouse sobre cada barra, se despliega una ventana flotante con el desglose exacto de eventos.

4. **Distribución por Severidad:**
   Gráfica circular de tipo dona que clasifica las alertas en cuatro niveles cromáticos intuitivos:

   - *Baja (Azul/Verde):* Escaneos preliminares y peticiones benignas.
   - *Media (Amarillo):* Sondeos a puertos de servicios conocidos.
   - *Alta (Naranja):* Intentos de autenticación con credenciales predeterminadas o fuerza bruta.
   - *Crítica (Rojo):* Inyecciones de código malicioso, exploits de día cero y comandos remotos.

5. **Mapa de Calor Predictivo:**
   Matriz visual que cruza los días de la semana con los rangos horarios de 24 horas, iluminando con colores más intensos las franjas horarias donde los modelos predictivos y el histórico de eventos detectan la mayor probabilidad de actividad hostil. Sirve como insumo vital para planificar guardias y refuerzos en el SOC.

6. **Módulo Honeypot Advisor (Asistente Inteligente):**
   Caja de recomendaciones automatizadas que analiza el comportamiento del tráfico reciente y sugiere medidas defensivas concretas, tales como: *"Alta concentración de ataques al puerto 22 (SSH); se recomienda habilitar reglas de bloqueo geográfico para subredes no reconocidas"*.

### 7.2 Threat Center (Gestión de Lista Negra de IPs Maliciosas)
El Threat Center es el módulo táctico donde los operadores consultan, registran, catalogan y neutralizan direcciones IP hostiles detectadas por los honeypots.

Para acceder, haga clic en **Threat Center** (o **Lista Negra**) en el menú de navegación.

<video poster="../assets/screenshots/fig05_threat_center_ioc.png" controls width="100%" playsinline class="docs-video">
  <source src="../assets/videos/03_threat_center_y_boveda.mp4" type="video/mp4">
  Su navegador no soporta la reproducción de video HTML5.
</video>
*Video 3. Búsqueda y catalogación de direcciones IP en la Lista Negra.*

![Figura 5. Módulo de administración de indicadores de compromiso (IOC)](assets/screenshots/fig05_threat_center_ioc.png)
*Figura 5. Módulo de administración de indicadores de compromiso (IOC).*

**A. Búsqueda y Filtrado de Indicadores:**
En la parte superior de la tabla encontrará una barra de búsqueda predictiva. Puede escribir cualquier término: una dirección IP completa o parcial (ej. `192.168`), el nombre de un país (ej. `China`, `Rusia`), una categoría de ataque (ej. `Brute Force`, `SSH Scan`) o las notas del analista. La tabla filtrará los resultados en tiempo real sin recargar la página.

**B. Registro de una Nueva IP en la Lista Negra:**

1. Haga clic sobre el botón **+ Agregar Indicador** (o **Agregar IP**) ubicado encima de la tabla.
2. Se desplegará un formulario modal con los siguientes campos a diligenciar:

   - **Dirección IP:** Digite la dirección IPv4 o IPv6 que desea catalogar (ej. `203.0.113.45`).
   - **País de Origen:** Seleccione o verifique el país asociado a la geolocalización de la IP.
   - **Categoría de Amenaza:** Seleccione en el menú desplegable la tipología del ataque observado (*Fuerza Bruta SSH, Escaneo Web, Inyección SQL, Botnet, Malware*).
    - **Threat Score (Nivel de Amenaza de 0 a 100):** Asigne una puntuación numérica entre 0 y 100 representativa de la peligrosidad de la IP.

        !!! warning "⚡ Regla de Bloqueo Automático"
            Toda dirección IP registrada con un **Threat Score superior a 70 puntos ($>70$)** es clasificada de forma automática por el sistema bajo el estado de **Bloqueada**, lo que activa su sincronización prioritaria con las políticas de defensa perimetral.

    - **Notas del Analista:** Campo de texto libre para justificar el registro (ej. *"Detectada realizando más de 500 intentos de inicio de sesión por minuto en el sensor Cowrie"*).
3. Haga clic en **Guardar Indicador**. La IP aparecerá listada en la tabla principal.

**C. Modificación de un Indicador Existente:**

1. En la fila correspondiente a la IP deseada, haga clic en el botón de **Editar** (representado por el **ícono de lápiz**).
2. Se abrirá el formulario con los valores actuales. Modifique la categoría, la puntuación o agregue notas adicionales de seguimiento.
3. Haga clic en **Actualizar Cambios**.

**D. Retiro / Eliminación de una IP y la Bóveda Forense:**

1. Si un analista determina que un indicador ya no representa riesgo o requiere ser retirado, debe hacer clic sobre el botón de **Eliminar** (representado por el **ícono de papelera**).
2. El sistema mostrará un cuadro de diálogo de confirmación advirtiendo sobre la operación.
3. Al confirmar, la IP se retira inmediatamente de la tabla operativa de bloqueo activo.
4. **Consulta en la Bóveda Forense:** La plataforma no destruye la evidencia; traslada una copia histórica de la IP junto con sus notas y el usuario que ordenó el retiro hacia la pestaña **Bóveda Forense** (ubicada como una subpestaña dentro del Threat Center). Desde allí, cualquier analista o auditor puede consultar los indicadores archivados para fines de trazabilidad histórica.

### 7.3 Solicitud, Aprobación y Descarga de Logs & Reportes
Este módulo permite extraer paquetes estructurados de registros de seguridad para investigaciones forenses externas o comités de auditoría.

Para acceder, pulse sobre **Logs & Reportes** en el menú de navegación.

<video poster="../assets/screenshots/fig06_exportacion_logs_modal.png" controls width="100%" playsinline class="docs-video">
  <source src="../assets/videos/04_logs_export_y_pdf.mp4" type="video/mp4">
  Su navegador no soporta la reproducción de video HTML5.
</video>
*Video 4. Solicitud de exportación en rango temporal real, descarga y visualización del Esquema Canónico en PDF.*

**A. Solicitar una Nueva Extracción de Telemetría:**

1. Haga clic en el botón **Nuevo Export** para abrir la ventana de parámetros.
2. Seleccione la **Fecha de Inicio** del rango temporal que desea auditar.
3. Seleccione la **Fecha de Fin**.
4. Haga clic en **Solicitar Exportación**.

![Figura 6. Modal interactivo de solicitud de rangos de fechas para exportación](assets/screenshots/fig06_exportacion_logs_modal.png)
*Figura 6. Modal interactivo de solicitud de rangos de fechas para exportación de telemetría.*

**B. Mecánica de Aprobación según el Volumen de Datos:**
El sistema evalúa de forma automática el volumen de registros comprendido en el rango solicitado:

- **Extracción Directa (Menor o igual a 50.000 eventos):** Se aprueba automáticamente al instante. El sistema programa la tarea en segundo plano y pasa a generar el archivo sin requerir intervención humana adicional.
- **Extracción Masiva (Mayor a 50.000 eventos):** Para evitar sobrecargas y fuga involuntaria de grandes volúmenes de datos, la solicitud queda catalogada como masiva y entra en estado de espera hasta que el **Administrador la autorice formalmente a través del bot de Telegram**.

**C. Estados del Ciclo de Vida de una Solicitud:**
En la tabla de historial de solicitudes, el operador puede verificar el avance de cada petición mediante las siguientes etiquetas de estado:

- 🟡 **Pendiente de Aprobación:** Solicitud masiva que se encuentra a la espera de que el Administrador presione el botón de autorización en su aplicación de Telegram.
- 🔵 **Procesando:** La solicitud ha sido aprobada y el motor del sistema se encuentra empaquetando y comprimiendo los registros en segundo plano.
- 🟢 **Listo (o Completado):** El paquete de datos ha sido generado exitosamente y los botones de descarga se encuentran habilitados para el usuario.
- 🔴 **Rechazada:** La solicitud fue evaluada y denegada por el Administrador mediante Telegram.

![Figura 7. Historial de solicitudes con botones de descarga directa en JSONL y PDF](assets/screenshots/fig09_analista_logs_pdf.png)
*Figura 7. Historial de solicitudes con botones de descarga directa en JSONL y PDF.*

**D. Descarga del Archivo de Telemetría Cruda (JSONL):**

1. Ubique en la tabla una solicitud que se encuentre en estado **Listo**.
2. Haga clic sobre el botón de descarga rotulado como **JSONL**.
3. Su navegador descargará un archivo comprimido con extensión `.jsonl`. Cada línea de este archivo contiene un objeto estructurado en formato JSON con la totalidad de los campos del evento de seguridad (dirección IP de origen, puerto destino, sensor atacado, encabezados y reglas disparadas), idóneo para ser analizado en entornos como Python, Pandas, Splunk o Elasticsearch.

**E. Descarga del Reporte Ejecutivo de Esquema (PDF):**

1. En la misma fila con estado **Listo**, haga clic sobre el botón rotulado como **Esquema (PDF)**.
2. El sistema compilará en tiempo real un informe técnico-ejecutivo de alta presentación visual.
3. El archivo descargado contiene un resumen consolidado con tablas comparativas, distribución de ataques por categoría, principales direcciones hostiles detectadas y conclusiones automáticas del período, listo para ser adjuntado en informes de gestión de seguridad.

!!! note "⚡ Período de Retención"
    Los archivos de datos generados permanecen disponibles para descarga en la plataforma durante un período de **7 días calendario**. Transcurrido este plazo, los archivos pesados son depurados automáticamente del almacenamiento temporal para optimizar espacio, conservando en el historial el registro de la solicitud.

---

## 8. Funcionalidades específicas por rol

HoneyMetrics implementa un modelo de control de acceso riguroso que adapta la interfaz y los privilegios a las responsabilidades de cada miembro de la organización. A continuación se desglosan las características operativas de los cuatro perfiles del sistema:

### 8.1 Rol: Administrador
El Administrador es la máxima autoridad técnica y de gobernanza dentro de HoneyMetrics. Posee supervisión integral sobre la plataforma y custodia los accesos de los demás colaboradores.

- **Capacidades:**
  - Acceso total a todas las Funcionalidades Generales, Dashboard CTI, Threat Center y Logs & Reportes.
  - Administración de usuarios del sistema desde la ruta **Configuración → Gestión de Usuarios & Roles**: creación de nuevas cuentas, modificación de nombres y correos, asignación de roles y revocación inmediata de accesos.
  - **Aprobación de descargas masivas en Telegram:** Cuando un analista genera una petición superior a 50.000 eventos, el bot oficial de HoneyMetrics envía una notificación interactiva al chat personal del Administrador con los datos del solicitante, período y volumen estimado. El Administrador puede pulsar los botones interactivos **[ Aprobar ]** o **[ Rechazar ]** directamente desde su teléfono móvil.
  - Capacidad de consultar y depurar registros archivados en la Bóveda Forense.

<video poster="../assets/screenshots/fig07_admin_usuarios_roles.png" controls width="100%" playsinline class="docs-video">
  <source src="../assets/videos/05_admin_usuarios_y_roles.mp4" type="video/mp4">
  Su navegador no soporta la reproducción de video HTML5.
</video>
*Video 5. Creación de usuarios con contraseñas seguras CSPRNG, control de acceso basado en roles (RBAC) y medidor dinámico de contraseñas.*

![Figura 8. Panel de gobernanza de identidades y creación de cuentas en Admin Hub](assets/screenshots/fig07_admin_usuarios_roles.png)
*Figura 8. Panel de gobernanza de identidades y creación de cuentas en Admin Hub.*

- **Limitaciones:**
  - Por sanas prácticas de gobierno de seguridad, el Administrador no debe utilizar su cuenta privilegiada para tareas cotidianas de navegación u ocio digital; debe emplear una cuenta operativa especializada cuando solo requiera realizar análisis de datos rutinarios.

- **Recomendaciones de uso:**
  - Mantener siempre enrolado y activo el doble factor de autenticación (MFA).
  - Responder oportunamente a las solicitudes de Telegram para evitar cuellos de botella en las investigaciones de los consultores y analistas.
  - Realizar una auditoría mensual del listado de usuarios activos para deshabilitar cuentas de personal que haya cambiado de funciones o concluido su ciclo en la organización.

### 8.2 Rol: Consultor de Ciberseguridad
El Consultor de Ciberseguridad es el perfil táctico orientado a la investigación activa de incidentes, triaje de alertas y enriquecimiento de inteligencia de amenazas.

- **Capacidades:**
  - Uso completo de todas las Funcionalidades Generales (perfil, doble factor, preferencias).
  - Supervisión y filtrado dinámico del Dashboard CTI en todas sus ventanas temporales (24h, 7d, 30d y fechas personalizadas).
  - **Operación total del Threat Center:** Búsqueda avanzada, creación de nuevas direcciones IP maliciosas con su puntaje de amenaza correspondiente, edición de registros existentes y retiro de indicadores con traslado automático a la Bóveda Forense.
  - Consulta permanente de los registros históricos resguardados en la Bóveda Forense.
  - Emisión de solicitudes de extracción de telemetría y descarga tanto de paquetes JSONL como de reportes ejecutivos en PDF.

![Figura 9. Vista de auditoría e investigación forense para el perfil Consultor](assets/screenshots/fig08_consultor_cti_boveda.png)
*Figura 9. Vista de auditoría e investigación forense para el perfil Consultor.*

- **Limitaciones:**
  - No tiene acceso al módulo de administración de usuarios ni puede alterar las cuentas o roles de otros miembros del equipo.
  - Sus solicitudes de logs que excedan los 50.000 eventos quedan sujetas a la aprobación previa del Administrador.

- **Recomendaciones de uso:**
  - Contrastar siempre las direcciones IP detectadas con fuentes públicas de inteligencia (como VirusTotal o AbuseIPDB) antes de asignar un Threat Score crítico.
  - Documentar con precisión el campo *Notas del Analista* al dar de alta una IP, detallando el vector de ataque y la evidencia observada para facilitar el trabajo de auditorías futuras.
  - Apoyarse en el Mapa de Calor Predictivo para identificar las franjas horarias de mayor incidencia hostil.

### 8.3 Rol: Analista de Datos
El Analista de Datos enfoca su labor en la explotación cuantitativa de la telemetría, el descubrimiento de patrones a gran escala y la correlación estadística del comportamiento de las amenazas.

- **Capacidades:**
  - Uso de las Funcionalidades Generales del sistema.
  - Visualización integral del Dashboard CTI y exploración de sus gráficas de tendencia temporal y mapas térmicos.
  - **Extracción masiva de información:** Es el principal operador del módulo de Logs & Reportes, facultado para programar solicitudes de datos para períodos prolongados con el fin de alimentarlos en modelos de minería o librerías de analítica de datos (Python, R, Jupyter Notebooks).
  - Descarga ágil de archivos JSONL para procesamiento matricial y reportes PDF de síntesis.
  - Consulta y búsqueda en la tabla de indicadores de la Lista Negra (Threat Center).

- **Limitaciones:**
  - No puede gestionar usuarios, perfiles ajenos ni configuraciones globales de la plataforma.
  - Sus extracciones superiores al límite de 50.000 registros requieren la autorización del Administrador en Telegram para prevenir descargas desproporcionadas.

- **Recomendaciones de uso:**
  - Definir ventanas temporales acotadas para sus extracciones cuando realice análisis exploratorios preliminares, evitando solicitar rangos anuales completos en un solo paquete.
  - Utilizar herramientas locales de procesamiento eficiente de flujos (como `jq` o scripts en Python con carga iterativa) para manipular los archivos JSONL sin saturar la memoria RAM de su equipo.
  - Compartir con el equipo de Consultores de Ciberseguridad cualquier hallazgo anómalo o correlación imprevista que amerite la catalogación de nuevos rangos de IPs en la Lista Negra.

### 8.4 Rol: Directivo de T.I.
El Directivo de T.I. (o CISO / Gerente de Seguridad) es un perfil consultivo de alto nivel que requiere visibilidad ejecutiva sobre el estado de protección de la organización, sin participar en la manipulación operativa de registros.

- **Capacidades:**
  - Uso de las Funcionalidades Generales del sistema (acceso seguro, configuración de perfil y contraseña).
  - **Visualización completa del Dashboard CTI:** Acceso a la totalidad de las tarjetas de KPIs ejecutivos, gráficas de severidad y comparativas temporales.
  - **Consulta en modo de solo lectura del Threat Center:** Puede buscar, ordenar e inspeccionar los indicadores de amenaza catalogados y sus puntajes, sin riesgo de alteración accidental.
  - **Emisión de Reportes Ejecutivos en PDF:** Descarga de informes de alto nivel diseñados específicamente para su presentación en comités de dirección y juntas directivas.

![Figura 10. Resumen de inteligencia estratégica y métricas consolidadas para el Directivo de T.I.](assets/screenshots/fig10_directivo_resumen.png)
*Figura 10. Resumen de inteligencia estratégica y métricas consolidadas para el Directivo de T.I.*

- **Limitaciones:**
  - Perfil de solo lectura: No puede crear, editar ni eliminar direcciones IP en la Lista Negra.
  - No tiene facultades para solicitar la descarga de archivos crudos de telemetría forense (.jsonl).
  - No tiene acceso a la gestión de cuentas ni a los controles de aprobación en Telegram.

- **Recomendaciones de uso:**
  - Emplear las métricas del Dashboard (KPIs de Total de Alertas, Severidad y Alertas Críticas) para medir la efectividad de las defensas y evaluar la exposición de la red frente a ataques recurrentes.
  - Exportar periódicamente los reportes ejecutivos en PDF para sustentar inversiones en infraestructura de ciberdefensa ante la junta directiva.
  - Validar las sugerencias del Honeypot Advisor para alinear las políticas corporativas de seguridad con el comportamiento real de los atacantes.

---

## 9. Preguntas frecuentes y resolución de problemas

**P1: Mi aplicación autenticadora genera el código de 6 dígitos, pero el sistema indica que el código es inválido.**
*Respuesta:* La causa más común es una ligera desincronización entre el reloj interno de su teléfono móvil y la hora estándar de internet. Ingrese a los ajustes de fecha y hora de su teléfono móvil y asegúrese de tener activada la opción **Fecha y hora automáticas (proporcionadas por la red)**. Posteriormente, espere a que la aplicación genere un nuevo código de 6 dígitos e inténtelo nuevamente.

**P2: No he recibido el correo electrónico con el enlace de recuperación de contraseña.**
*Respuesta:* Verifique en primer lugar su carpeta de *Spam*, *Correo no deseado* o *Promociones*. Si tras unos minutos no aparece el mensaje, asegúrese de haber escrito correctamente la dirección de correo registrada. Por motivos de seguridad y privacidad, la plataforma no revela si una dirección existe o no en el sistema. Si el problema persiste, contacte a su Administrador.

**P3: Solicité una extracción de logs hace varios minutos y su estado permanece en "Pendiente de Aprobación".**
*Respuesta:* Esto significa que su consulta abarca un volumen superior a los 50.000 eventos de seguridad y ha sido remitida a los Administradores a través de Telegram para su autorización. Una vez que el Administrador presione el botón de aprobación en su teléfono móvil, el estado cambiará automáticamente a *Procesando* y luego a *Listo*.

**P4: El Dashboard muestra un mensaje de advertencia que indica "Modo de contingencia / Datos offline". ¿Qué significa?**
*Respuesta:* Este aviso se presenta cuando la plataforma no logra establecer una comunicación directa en tiempo real con el servidor de registros en ese instante puntual (por ejemplo, durante labores de mantenimiento programado de la red). En dicho escenario, la interfaz despliega métricas de demostración o datos cacheados para permitirle familiarizarse con la herramienta. Las alertas mostradas en ese estado no deben interpretarse como eventos en tiempo real hasta que el enlace sea restablecido.

**P5: ¿Puedo tener HoneyMetrics abierto en varios navegadores o computadores al mismo tiempo?**
*Respuesta:* Sí, puede acceder desde diferentes puestos de trabajo autorizados; sin embargo, si por motivos de seguridad usted cambia su contraseña personal desde un equipo, las sesiones activas en los demás dispositivos caducarán automáticamente y le solicitarán volver a identificarse con su nueva clave.
