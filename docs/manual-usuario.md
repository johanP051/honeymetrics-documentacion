# Manual de Usuario — HoneyMetrics v2.0
**Plataforma Enterprise de Ciberinteligencia de Amenazas (CTI) y Monitoreo de Sensores Honeypot**

> **Ver también:**
> - [manual-tecnico.md → Sección 4: Control de Acceso RBAC](./manual-tecnico.md#4-control-de-acceso-basado-en-roles-rbac) — Matriz de autorización formal, políticas de privilegios y arquitectura criptográfica.
> - [guia-despliegue.md → Sección 5: Despliegue Paso a Paso](./guia-despliegue.md#5-despliegue-paso-a-paso) — Topología de red, puertos de servicio y verificación de conectividad perimetral.
> - [diccionario-datos.md → Sección 3: Módulo 1 Seguridad y RBAC](./diccionario-datos.md#3-módulo-1--seguridad-autenticación-y-control-de-acceso) — Esquema relacional de tablas `users`, `roles` y `threat_ips`.

---

## Índice
- [1. Introducción al Ecosistema HoneyMetrics](#1-introducción-al-ecosistema-honeymetrics)
  - [1.1 Propósito Operativo de la Plataforma](#11-propósito-operativo-de-la-plataforma)
  - [1.2 Filosofía de Diseño Visual y Modo Dark CTI](#12-filosofía-de-diseño-visual-y-modo-dark-cti)
- [2. Requisitos del Cliente (Navegadores, Resolución, Red)](#2-requisitos-del-cliente-navegadores-resolución-red)
  - [2.1 Navegadores Web Compatibles](#21-navegadores-web-compatibles)
  - [2.2 Resolución de Pantalla y Hardware Recomendado](#22-resolución-de-pantalla-y-hardware-recomendado)
  - [2.3 Conectividad y Políticas de Red](#23-conectividad-y-políticas-de-red)
- [3. Primer Acceso y Configuración MFA](#3-primer-acceso-y-configuración-mfa)
  - [3.1 Flujo de Autenticación Primaria y Credenciales Iniciales](#31-flujo-de-autenticación-primaria-y-credenciales-iniciales)
  - [3.2 Enrolamiento de Doble Factor (TOTP vía Código QR)](#32-enrolamiento-de-doble-factor-totp-vía-código-qr)
  - [3.3 Actualización Obligatoria de Contraseña en Primer Acceso](#33-actualización-obligatoria-de-contraseña-en-primer-acceso)
  - [3.4 Vinculación con Bot de Telegram para Notificaciones y Alertas](#34-vinculación-con-bot-de-telegram-para-notificaciones-y-alertas)
- [4. Diccionario de Notificaciones](#4-diccionario-de-notificaciones)
  - [4.1 Semántica de Componentes Visuales](#41-semántica-de-componentes-visuales)
  - [4.2 Matriz Canónica de Notificaciones y Acciones Operativas](#42-matriz-canónica-de-notificaciones-y-acciones-operativas)
- [5. Guía por Rol](#5-guía-por-rol)
  - [5.1 Rol: Administrador](#51-rol-administrador)
  - [5.2 Rol: Analista de datos](#52-rol-analista-de-datos)
  - [5.3 Rol: Consultor de Ciberseguridad](#53-rol-consultor-de-ciberseguridad)
  - [5.4 Rol: Directivo de T.I.](#54-rol-directivo-de-ti)
- [6. Casos Borde y Preguntas Frecuentes](#6-casos-borde-y-preguntas-frecuentes)
  - [P1: ¿Qué hacer si pierdo mi dispositivo móvil o el código TOTP es rechazado?](#p1-qué-hacer-si-pierdo-mi-dispositivo-móvil-o-el-código-totp-es-rechazado)
  - [P2: ¿Por qué una solicitud de logs queda en "Pendiente de Aprobación"?](#p2-por-qué-una-solicitud-de-logs-queda-en-pendiente-de-aprobación)
  - [P3: ¿Qué ocurre al intentar ingresar una IP privada o ya registrada en el Threat Center?](#p3-qué-ocurre-al-intentar-ingresar-una-ip-privada-o-ya-registrada-en-el-threat-center)
  - [P4: ¿Por qué el reporte PDF se descarga al instante y la telemetría JSONL tarda más?](#p4-por-qué-el-reporte-pdf-se-descarga-al-instante-y-la-telemetría-jsonl-tarda-más)
  - [P5: ¿Por qué un usuario Directivo no puede ver los botones de edición de amenazas?](#p5-por-qué-un-usuario-directivo-no-puede-ver-los-botones-de-edición-de-amenazas)
  - [P6: ¿Qué sucede exactamente al pulsar "Aprobar Bloqueo" en el bot de Telegram?](#p6-qué-sucede-exactamente-al-pulsar-aprobar-bloqueo-en-el-bot-de-telegram)
  - [P7: ¿Cómo responde la plataforma si se pierde la conexión con el nodo Wazuh?](#p7-cómo-responde-la-plataforma-si-se-pierde-la-conexión-con-el-nodo-wazuh)
  - [P8: ¿Cuánto tiempo se conservan los archivos de logs generados en el servidor?](#p8-cuánto-tiempo-se-conservan-los-archivos-de-logs-generados-en-el-servidor)
  - [P9: ¿Qué significa el mensaje HTTP 403 Forbidden y cómo resolverlo?](#p9-qué-significa-el-mensaje-http-403-forbidden-y-cómo-resolverlo)
  - [P10: ¿Cuál es el procedimiento seguro para cerrar sesión en puestos compartidos?](#p10-cuál-es-el-procedimiento-seguro-para-cerrar-sesión-en-puestos-compartidos)

---

## 1. Introducción al Ecosistema HoneyMetrics

### 1.1 Propósito Operativo de la Plataforma
HoneyMetrics v2.0 es una plataforma corporativa de Inteligencia de Amenazas Cibernéticas (CTI) y Centro de Operaciones de Seguridad (SOC) diseñada para transformar eventos crudos recolectados por sensores perimetrales honeypot en conocimiento táctico, estratégico y ejecutable. En infraestructuras modernas de defensa, los sensores trampa (como nodos físicos Orange Pi 5 desplegados en zonas desmilitarizadas ejecutando los servicios Cowrie y Dionaea) reciben continuamente intentos de intrusión hostil, incluyendo escaneos masivos de puertos, ataques de fuerza bruta hacia servicios de administración remota y descargas de binarios maliciosos.

HoneyMetrics se conecta de forma directa con el clúster de indexación del SIEM Wazuh (Wazuh Indexer / OpenSearch), normalizando miles de registros de seguridad y presentándolos mediante una interfaz reactiva, intuitiva y centralizada. A través de este sistema, los equipos de seguridad pueden evaluar el nivel de hostilidad de los atacantes, correlacionar indicadores de compromiso (IOCs), gestionar listas de bloqueo perimetral, generar informes ejecutivos en formato PDF y exportar telemetría cruda en formato JSONL para investigaciones forenses bajo estricta cadena de custodia.

### 1.2 Filosofía de Diseño Visual y Modo Dark CTI
La interfaz de usuario de HoneyMetrics v2.0 ha sido desarrollada bajo la arquitectura Single Page Application (SPA) con React y Tailwind CSS, implementando un diseño de alta densidad informativa denominado *Dark CTI Theme*. Esta paleta visual utiliza un fondo base oscuro (`#0d1117`), contenedores de tarjetas analíticas (`#161b22`), bordes de delimitación sutiles (`#30363d`) y acentos en dorado corporativo (`#d4af37`).

Este esquema cromático no responde a una preferencia estética arbitraria, sino a un estándar ergonómico para entornos SOC donde los analistas operan frente a múltiples monitores durante turnos prolongados. La reducción de luminosidad disminuye drásticamente la fatiga visual, mientras que el contraste semántico resalta instantáneamente eventos de criticidad severa (rojo `#ef4444`), alertas altas (naranja `#f97316`), anomalías medias (amarillo `#eab308`) y confirmaciones operativas (verde `#22c55e`).

---

## 2. Requisitos del Cliente (Navegadores, Resolución, Red)

Para garantizar un rendimiento óptimo de los tableros interactivos, la generación de reportes en el navegador y el consumo fluido de eventos, la estación de trabajo del operador debe cumplir con las siguientes especificaciones técnicas.

### 2.1 Navegadores Web Compatibles
HoneyMetrics v2.0 hace un uso intensivo de APIs modernas de JavaScript, incluyendo Web Cryptography API, Canvas 2D para renderizado vectorial de métricas y streams asíncronos para la descarga eficiente de grandes volúmenes de datos.

| Navegador Web | Compatibilidad | Versión Mínima | Notas Técnicas y Recomendaciones |
| :--- | :---: | :---: | :--- |
| **Google Chrome** | ✅ Totalmente Soportado | 120.0 (64-bit) | Motor V8 optimizado. Recomendado para máxima velocidad en exportación de reportes. |
| **Mozilla Firefox** | ✅ Totalmente Soportado | 120.0 (64-bit) | Excelente gestión de memoria y aislamiento estricto de cookies `SameSite`. |
| **Brave Browser** | ✅ Totalmente Soportado | 1.60.0 (64-bit) | Compatible. Requiere mantener habilitadas las conexiones seguras hacia la API REST. |
| **Microsoft Edge** | ✅ Totalmente Soportado | 120.0 (64-bit) | Motor Chromium idéntico a Chrome; plena compatibilidad corporativa bajo Windows. |
| **Apple Safari** | ⚠️ Compatibilidad Parcial | 16.4+ (macOS) | Soporta visualización básica; se recomienda desactivar bloqueos estrictos de cookies. |
| **Internet Explorer** | ❌ Incompatible | Cualquier versión | Obsoleto. El sistema bloquea el acceso por ausencia de soporte para ES2022 y Crypto. |

### 2.2 Resolución de Pantalla y Hardware Recomendado
La interfaz del Centro de Operaciones contiene múltiples paneles de visualización simultánea (histogramas temporales, matrices de calor, listas tabulares de IOCs y mapas de enjambres de red). Se recomienda desplegar la plataforma en monitores dedicados de alta resolución.

| Componente | Requisito Mínimo Absoluto | Requisito Recomendado (Estación SOC) |
| :--- | :--- | :--- |
| **Resolución de Pantalla** | 1366 × 768 píxeles (Escalado 100%) | 1920 × 1080 (Full HD) o superior (configuración multipantalla) |
| **Procesador (CPU)** | Dual-Core 2.0 GHz (x86_64 o ARM64) | Quad-Core 2.5 GHz o superior (Intel Core i5 / AMD Ryzen 5 / Apple Silicon) |
| **Memoria RAM Libre** | 4 GB dedicados al navegador | 8 GB o superior disponibles para procesamiento concurrente |
| **Almacenamiento Local** | 500 MB libres en disco | 2 GB libres en unidad de estado sólido (SSD) para telemetría JSONL |
| **Dispositivo Auxiliar** | Smartphone básico con cámara | Smartphone con aplicación autenticadora (TOTP) y cliente Telegram |

> [!NOTE]
> **El Por Qué Técnico — Requisitos de Memoria y Renderizado Client-Side:** HoneyMetrics v2.0 traslada la renderización de informes ejecutivos en formato PDF directamente a la memoria del navegador del cliente mediante la librería `jsPDF`. Esta decisión técnica libera a los servidores centrales de sobrecargas de CPU, pero exige que la estación del analista cuente con suficiente memoria RAM disponible para estructurar documentos voluminosos sin provocar cierres inesperados de pestaña.

### 2.3 Conectividad y Políticas de Red
* **Ancho de banda disponible:** Conexión de red corporativa estable con al menos 10 Mbps simétricos (mínimo 5 Mbps).
* **Puertos de comunicación saliente:** Acceso abierto y directo hacia el puerto TCP 443 (HTTPS) sobre el dominio institucional de la plataforma (`https://honey.johan-d3v.site/` o la dirección interna configurada).
* **Políticas de inspección de tráfico:** Las soluciones corporativas de seguridad perimetral (Next-Generation Firewalls, proxies de inspección SSL profunda o balanceadores) no deben alterar ni truncar las cabeceras HTTP `Authorization` con tokens Bearer ni interceptar las conexiones WebSocket o Server-Sent Events utilizadas en el flujo de monitoreo en tiempo real.
* **Acceso a la nube de Telegram:** Para los usuarios con responsabilidades administrativas o de consultoría táctica, la estación de trabajo y el dispositivo móvil deben permitir tráfico HTTPS saliente hacia `api.telegram.org` para la recepción de mensajes del bot de autorización.

---

## 3. Primer Acceso y Configuración MFA

El acceso a HoneyMetrics v2.0 está protegido mediante un esquema riguroso de autenticación de dos factores (2FA / MFA) obligatorio basado en algoritmos de contraseñas de un solo uso basadas en el tiempo (TOTP, RFC 6238). Ningún usuario puede operar en la plataforma sin completar este enrolamiento.

### 3.1 Flujo de Autenticación Primaria y Credenciales Iniciales
1. Abra el navegador web e ingrese a la dirección URL oficial provista por el equipo de administración (por ejemplo, `https://honey.johan-d3v.site/`).
2. En la pantalla inicial de bienvenida, observe el formulario central de inicio de sesión con el emblema de HoneyMetrics. *(Referencia: `mockups/mockup_landing_login_1787432668250.jpg`)*.
3. En el campo **Correo Electrónico**, escriba su dirección de correo corporativo. El sistema normaliza automáticamente las mayúsculas a minúsculas para prevenir discrepancias.
4. En el campo **Contraseña**, introduzca la contraseña temporal de 12 caracteres que le fue suministrada de forma segura por el Administrador del sistema durante la creación de su cuenta.
5. Utilice el icono del ojo ubicado en el extremo derecho del campo si requiere inspeccionar la clave escrita para descartar caracteres accidentales.
6. Haga clic en el botón principal **Iniciar Sesión**.
7. Si las credenciales primarias son válidas, el sistema emitirá un token JWT transitorio (con vigencia estricta de 5 minutos) y lo redirigirá inmediatamente a la pantalla de enrolamiento de segundo factor.

### 3.2 Enrolamiento de Doble Factor (TOTP vía Código QR)
1. Al acceder por primera vez, el sistema presentará el asistente de configuración de seguridad, exhibiendo un código QR generado dinámicamente y una clave alfanumérica de respaldo codificada en Base32. *(Referencia: `mockups/mockup_perfil_2fa_1787432936474.jpg`)*.
2. Tome su dispositivo móvil y abra su aplicación autenticadora de preferencia (Google Authenticator, Microsoft Authenticator o Aegis OTP).
3. Seleccione la opción para agregar una nueva cuenta mediante el botón **Escanear código QR**.
4. Apunte la cámara de su dispositivo móvil hacia la pantalla del monitor hasta que la aplicación reconozca el patrón bidimensional.
5. Si su cámara presenta problemas físicos de enfoque, haga clic en el enlace **"¿Problemas para escanear? Ingresar clave manualmente"** en la interfaz web, copie la cadena secreta de 32 caracteres y péguela en la aplicación móvil en modo "Basada en tiempo (TOTP)".
6. La aplicación autenticadora registrará una nueva entrada denominada `HoneyMetrics (su_email@empresa.com)` y desplegará un código numérico dinámico de 6 dígitos que se actualiza cada 30 segundos.
7. Ingrese el código actual de 6 dígitos en el recuadro interactivo de la página web y presione el botón **Verificar y Activar MFA**.
8. Una vez comprobada la clave, el sistema activará el flag permanente de doble factor en su perfil y lo conducirá a la pantalla de actualización obligatoria de contraseña.

> [!NOTE]
> **El Por Qué Técnico — Ventana de Tolerancia Temporal en TOTP (RFC 6238):** Los códigos TOTP se calculan combinando la clave secreta compartida con la marca de tiempo Unix actual en intervalos de 30 segundos. Para mitigar problemas ocasionados por pequeños desajustes entre el reloj del servidor central y el reloj del teléfono móvil del analista, el backend de HoneyMetrics implementa una ventana de tolerancia de ±30 segundos (admite el código del intervalo inmediatamente anterior, el actual y el inmediatamente posterior).

### 3.3 Actualización Obligatoria de Contraseña en Primer Acceso
Por directrices de seguridad corporativa, todas las cuentas aprovisionadas por un administrador poseen la condición `must_change_password = True` activada en la base de datos.
1. Al superar la verificación TOTP inicial, la interfaz desplegará el formulario forzado de cambio de clave.
2. Ingrese su **Contraseña Actual** (la clave temporal asignada por el Administrador).
3. Escriba su **Nueva Contraseña**, asegurándose de satisfacer la política de contraseñas de HoneyMetrics:
   * Longitud mínima de 10 caracteres.
   * Al menos una letra mayúscula (A-Z) y una letra minúscula (a-z).
   * Al menos un dígito numérico (0-9).
   * Al menos un carácter especial (`!@#$%^&*()-_+=`).
   * No coincidir con contraseñas comunes ni contener fragmentos de su nombre o correo.
4. Repita la nueva clave en el campo **Confirmar Nueva Contraseña**.
5. Haga clic en **Actualizar y Continuar**. El sistema procesará el hash criptográfico mediante el algoritmo adaptativo Bcrypt y revocará la sesión temporal, obligándolo a ingresar nuevamente con sus credenciales definitivas y su código TOTP para certificar la validez del ciclo completo.

### 3.4 Vinculación con Bot de Telegram para Notificaciones y Alertas
La vinculación de su identificador de Telegram es indispensable para recibir confirmaciones de descargas masivas de telemetría y, en el caso de administradores, para emitir autorizaciones operativas.
1. Abra su aplicación personal de Telegram en su teléfono inteligente o cliente de escritorio.
2. En la barra de búsqueda superior, busque el bot oficial `@HoneyMetrics` (o el nombre de bot configurado en su despliegue corporativo).
3. Inicie una conversación con el bot pulsando el botón **Iniciar** o enviando el comando `/start`. El bot responderá saludándolo y confirmando que está listo para asociar su cuenta.
4. Para conocer su identificador numérico de usuario en Telegram, abra una conversación con el bot de utilidad `@userinfobot`, el cual le responderá de inmediato con su `Id` (una secuencia de números enteros, por ejemplo `512345678`).
5. En la plataforma HoneyMetrics, diríjase a la esquina superior derecha, haga clic sobre su nombre y seleccione **Mi Perfil**.
6. En la sección de configuración de perfil, localice el campo **ID de Chat de Telegram**, pegue su identificador numérico y haga clic en **Guardar Cambios**.
7. A partir de este momento, cualquier solicitud de descarga de logs o alerta prioritaria asignada a su cuenta será notificada directamente a su dispositivo móvil.

---

## 4. Diccionario de Notificaciones

La interfaz de HoneyMetrics v2.0 utiliza un sistema estandarizado de notificaciones emergentes (componentes flotantes tipo *Toast* y banners de alerta contextual) para informar en tiempo real sobre el resultado de las transacciones, advertencias de seguridad y bloqueos operativos.

### 4.1 Semántica de Componentes Visuales
* **Verde (Éxito):** Confirma que una mutación o lectura en la base de datos o en el clúster Wazuh se ejecutó conforme a las reglas de negocio.
* **Azul (Informativo):** Indica que un proceso asíncrono o de consulta pesada está en ejecución activa en segundo plano.
* **Amarillo (Advertencia):** Alerta al usuario sobre condiciones que requieren atención, validaciones adicionales o acciones de confirmación humana (*Human-in-the-Loop*).
* **Rojo (Error Crítico):** Señala un fallo en la solicitud, violaciones de control de acceso RBAC, problemas de comunicación con servicios o datos sintácticamente inválidos.

### 4.2 Matriz Canónica de Notificaciones y Acciones Operativas

| Color / Tipo | Mensaje Ejemplo | Qué Significa | Qué Hacer |
| :--- | :--- | :--- | :--- |
| **Verde** / Éxito | `"Autenticación exitosa. Bienvenido al Centro de Operaciones."` | Las credenciales primarias y el código TOTP fueron validados satisfactoriamente por el backend. | Aguarde la redirección automática hacia el Dashboard principal del SOC. |
| **Verde** / Éxito | `"Indicador IOC registrado exitosamente en el Threat Center."` | La dirección IP hostil y sus atributos de amenaza fueron persistidos en la base de datos de amenazas. | El registro ya es visible en la tabla; proceda con el etiquetado táctico o mitigación. |
| **Verde** / Éxito | `"Extracción completada. Archivo de telemetría listo para descarga."` | El proceso de extracción asíncrona de eventos desde Wazuh ha compilado el archivo JSONL en el servidor. | Diríjase al historial del módulo de Logs y pulse el botón de descarga rotulado como JSONL. |
| **Verde** / Éxito | `"Bloqueo perimetral autorizado y sincronizado con Firewall."` | La solicitud de bloqueo fue aprobada mediante Telegram y la regla se aplicó en el firewall perimetral. | Verifique que el indicador figure con estado "Bloqueada" en el Threat Intelligence Center. |
| **Verde** / Éxito | `"Contraseña corporativa actualizada exitosamente."` | La nueva contraseña cumple las directivas de complejidad y fue almacenada con hash Bcrypt. | Inicie sesión nuevamente en la pantalla de bienvenida con su nueva clave definitiva. |
| **Azul** / Informativo | `"Consultando telemetría de Wazuh Indexer en tiempo real..."` | El backend está realizando una búsqueda agregada en los índices de OpenSearch sobre los honeypots. | Espere unos segundos mientras se recalculan los paneles de métricas y la distribución temporal. |
| **Azul** / Informativo | `"Generando reporte ejecutivo en memoria local (jsPDF)..."` | La biblioteca del cliente está compilando los vectores, tablas y formatos ejecutivos dentro del navegador. | Mantenga la pestaña abierta y espere a que el navegador active la ventana de descarga del PDF. |
| **Amarillo** / Advertencia | `"Solicitud masiva (>7 días): enviada a aprobación HITL vía Telegram."` | La extracción abarca más de 7 días o supera los 50.000 eventos, requiriendo autorización de un Administrador. | Notifique al Administrador del SOC para que revise y pulse el botón de aprobación en Telegram. |
| **Amarillo** / Advertencia | `"Código TOTP próximo a expirar en su dispositivo móvil."` | La ventana temporal de 30 segundos del código actual en su aplicación móvil está por concluir. | Espere a que la aplicación genere el nuevo código de 6 dígitos antes de hacer clic en Enviar. |
| **Amarillo** / Advertencia | `"La dirección IP ingresada ya se encuentra registrada en el sistema."` | El indicador de compromiso que intenta registrar ya existe en la base de datos de amenazas activas. | Utilice la barra de búsqueda de la tabla para localizar el registro y edite sus metadatos. |
| **Rojo** / Error Crítico | `"Credenciales inválidas o cuenta temporalmente suspendida."` | La combinación de correo y contraseña no coincide con ningún usuario activo del sistema. | Verifique que no tenga el bloqueo de mayúsculas activado; si persiste, contacte al Administrador. |
| **Rojo** / Error Crítico | `"Código MFA inválido o desfase horario detectado en el cliente."` | El código de 6 dígitos no fue reconocido por el servidor dentro de la ventana de tolerancia admitida. | Compruebe que la hora de su teléfono móvil esté en modo automático por red (NTP) y reintente. |
| **Rojo** / Error Crítico | `"Acceso denegado (HTTP 403): Su rol no cuenta con privilegios."` | El usuario intentó invocar una acción o ruta restringida que no pertenece a su rol RBAC asignado. | Opere exclusivamente dentro de los módulos autorizados para su función o solicite elevación formal. |
| **Rojo** / Error Crítico | `"Fallo de conexión con nodo Wazuh: activando modo de contingencia."` | El servicio central no logró comunicarse con el clúster OpenSearch debido a cortes de red o reinicios. | La plataforma desplegará registros en caché local; reporte la incidencia al Administrador. |

---

## 5. Guía por Rol

HoneyMetrics v2.0 implementa una estricta separación de responsabilidades a través de su arquitectura de Control de Acceso Basado en Roles (RBAC), formalizada mediante la enumeración canónica `RoleEnum`. A continuación se detalla la operatividad del sistema según el rol asignado a cada usuario.

### 5.1 Rol: Administrador
El **Administrador** posee el nivel máximo de autoridad dentro de la plataforma. Es el único rol facultado para gestionar identidades, autorizar operaciones críticas mediante el bot de Telegram y acceder a la Bóveda Forense de auditoría.

#### 5.1.1 Gestión Integral de Usuarios y Permisos
Desde el módulo **Administración de Usuarios** *(Referencia: `mockups/mockup_gestion_usuarios_1787432740779.jpg`)*:
* **Creación de nuevos operadores:** Pulse el botón **Añadir Usuario**, diligencie el nombre completo, el correo corporativo y seleccione uno de los cuatro roles canónicos del sistema (`Administrador`, `Analista de datos`, `Consultor de Ciberseguridad` o `Directivo de T.I.`). El sistema generará una contraseña temporal aleatoria de 12 caracteres y configurará la cuenta en estado de primer acceso obligatorio.
* **Modificación de privilegios:** Localice a un usuario en la tabla principal y presione el botón de edición para cambiar su rol asignado o actualizar su información de contacto.
* **Reinicio de credenciales y MFA:** Si un operador extravía su dispositivo móvil autenticador, el Administrador puede ingresar al perfil del usuario y seleccionar **Restablecer Doble Factor**. Esta acción elimina la semilla TOTP anterior y fuerza al usuario a enrolar un nuevo código QR en su próximo inicio de sesión.
* **Baja y suspensión de cuentas:** Permite desactivar de inmediato el acceso a un operador sin eliminar su historial de auditoría ni las solicitudes forenses que haya generado en el pasado.

#### 5.1.2 Flujo de Aprobación Human-in-the-Loop (HITL) vía Telegram
Para salvaguardar los recursos computacionales y prevenir bloqueos perimetrales indeseados, HoneyMetrics delega la aprobación de acciones masivas o de alta criticidad al Administrador:
1. Cuando un analista solicita una extracción masiva de eventos (rango superior a 7 días o volumen estimado superior a 50.000 logs), o cuando el sistema correlaciona un ataque persistente con Threat Score superior a 80, el bot de Telegram envía un mensaje directo al Administrador.
2. El mensaje contiene la identidad del solicitante, el rango de fechas, la cantidad estimada de eventos y la IP involucrada.
3. El Administrador visualiza dos botones interactivos: `✅ Aprobar` y `❌ Rechazar`.
4. Al presionar `✅ Aprobar`, Telegram despacha una petición webhook cifrada al backend de HoneyMetrics (`POST /api/v1/logs/webhook/telegram`), validada mediante una cabecera con token secreto HMAC en tiempo constante.
5. El sistema actualiza el estado de la solicitud a "Listo" y activa el worker de descarga o aplica la regla de bloqueo en el firewall perimetral.

#### 5.1.3 Acceso Exclusivo a la Bóveda Forense (`threat_ips_vault`)
A diferencia de los demás roles que interactúan con la tabla operativa de amenazas, el Administrador tiene acceso a la Bóveda Forense inmutable. Cada vez que una dirección IP es eliminada o modificada en el Threat Center, el sistema genera automáticamente una copia de respaldo en la bóveda con marca temporal precisa, usuario responsable y justificación técnica, garantizando el principio de no-repudio ante auditorías forenses externas.

---

### 5.2 Rol: Analista de datos
El **Analista de datos** está enfocado en la minería de telemetría de intrusión, el análisis cuantitativo de patrones de ataque y la exportación de registros para procesamiento en herramientas externas.

#### 5.2.1 Monitoreo Ejecutivo en el SOC Dashboard
Al ingresar al sistema, el analista accede al **Dashboard de Amenazas** *(Referencia: `mockups/mockup_dashboard_kpis_1787432688887.jpg`)*:
* **KPIs Consolidados:** Supervisión en tiempo real del Total de Alertas registradas, el Nivel Promedio de Severidad de las reglas Wazuh (`rule.level`) y el total de direcciones IP hostiles identificadas.
* **Filtros Temporales:** Permite segmentar el análisis en tres ventanas cronológicas predeterminadas: **Últimas 24 horas**, **Últimos 7 días** y **Últimos 30 días**. Al cambiar el filtro, los componentes gráficos recalculan sus distribuciones de inmediato.
* **Distribución de Grupos y Agentes:** Identificación de las categorías de ataque predominantes (fuerza bruta SSH, escaneo de puertos web, intentos de inyección) y los sensores honeypot más asediados.

#### 5.2.2 Análisis Temporal mediante el Mapa de Calor
El analista cuenta con la herramienta interactiva **Mapa de Calor Temporal** *(Referencia: `mockups/mockup_mapa_calor_1787432770813.jpg`)*:
* Visualiza la densidad de intrusiones cruzando las 24 horas del día con los 7 días de la semana.
* Permite corroborar de forma gráfica los intervalos de mayor actividad maliciosa recurrente (por ejemplo, los picos sistemáticos registrados entre las 11:00 y las 12:00 UTC por botnets automatizadas).
* Facilita la correlación de turnos de vigilancia con los períodos de mayor actividad adversaria.

#### 5.2.3 Extracción de Telemetría Forense en Formato JSONL
Desde el módulo **Logs de Seguridad** *(Referencia: `mockups/mockup_logs_historial_1787432807551.jpg`)*:
1. Haga clic en **Solicitar Extracción**.
2. Seleccione la fecha de inicio y la fecha de finalización del período de interés.
3. Si el rango es menor o igual a 7 días, el sistema encola la solicitud y la procesa de forma directa. Si supera dicho límite, se notificará al Administrador vía Telegram para su autorización HITL.
4. Una vez completado el procesamiento, localice el registro en la tabla histórica y presione el botón **JSONL**.
5. El navegador iniciará la descarga en streaming de un archivo con formato JSON Lines (`.jsonl`), donde cada línea contiene la estructura completa del evento de seguridad de Wazuh, listo para ser ingerido en scripts de Python, cuadernos de Jupyter, herramientas como `jq` o sistemas de almacenamiento analítico.

---

### 5.3 Consultor de Ciberseguridad
El **Consultor de Ciberseguridad** desempeña un rol táctico de respuesta ante incidentes, catalogación de amenazas perimetrales y administración activa de la lista de bloqueo (Blacklist).

#### 5.3.1 Operación del Threat Intelligence Center
En este módulo central *(Referencia: `mockups/mockup_threat_intelligence_1787432712377.jpg`)*, el consultor dispone de herramientas avanzadas para calificar a los atacantes:
* **Threat Score (0 a 100):** Indicador cuantitativo asignado a cada IP atacante en función de la severidad acumulada de las alertas disparadas, la frecuencia de intentos por hora y la recurrencia histórica de intrusiones.
* **Detección de Enjambres y Redes Botnet por CIDR:** El sistema agrupa automáticamente los orígenes de ataque por prefijos de red (`/24` y `/16`), permitiendo al consultor identificar cuándo múltiples direcciones aparentemente aisladas forman parte de una misma campaña distribuida.
* **Clasificación del Comportamiento Agresor:** Identifica si la actividad corresponde a escaneos indiscriminados de alta cadencia (*Bots automatizados* con más de 100 eventos por hora) o a ataques interactivos pausados que sugieren interacción humana dirigida.

#### 5.3.2 Administración del Ciclo de Vida de IOCs
* **Registro de nuevas amenazas:** Pulse **Agregar Indicador** e introduzca la dirección IP (IPv4 o IPv6), el país de origen inferido, el tipo de intrusión observada (ej. `Fuerza Bruta SSH`, `Exploitation Attempt`) y una descripción detallada en el campo *Origen / Justificación*.
* **Actualización y Mitigación:** Modifique el estado del indicador entre `En Observación`, `En Revisión`, `Bloqueada` o `Falso Positivo`.
* **Eliminación justificada:** Si una dirección IP fue catalogada erróneamente, el consultor puede darla de baja del listado activo, ingresando obligatoriamente el motivo de la exclusión para el registro de auditoría.

#### 5.3.3 Visualizador de Cadena de Ataque y Patch Intelligence
* **Kill Chain Visualizer:** Proporciona un mapeo interactivo de los eventos de intrusión contra las tácticas y técnicas del marco MITRE ATT&CK (como T1110.001 Password Guessing o T1046 Network Service Discovery). *(Referencia: `mockups/mockup_kill_chain_visualizer_1787432890592.jpg`)*.
* **Patch Intelligence Panel:** Cruza los intentos de explotación capturados por los honeypots con los identificadores de vulnerabilidades y exposiciones comunes (CVEs) activos en los sistemas de la organización, permitiendo priorizar planes de parchado de seguridad. *(Referencia: `mockups/mockup_patch_intelligence_1787432846482.jpg`)*.

---

### 5.4 Rol: Directivo de T.I.
El **Directivo de T.I.** es un rol estratégico diseñado para líderes de tecnología, oficiales de seguridad de la información (CISO) y auditores que requieren visibilidad global sin capacidad de mutación operativa.

#### 5.4.1 Supervisión de Indicadores Clave de Riesgo (KRIs / KPIs)
* Permite revisar la tasa de ataques perimetrales neutralizados durante el último mes.
* Evalúa la evolución cronológica del nivel de severidad de incidentes en la infraestructura.
* Monitorea la efectividad de las defensas y la distribución geográfica de los actores hostiles que apuntan a la organización.

#### 5.4.2 Auditoría en Modo Solo Lectura
* El directivo tiene acceso de lectura completo al **Threat Intelligence Center** y a la **Lista Negra de Amenazas**, pudiendo filtrar por país, tipo de ataque y nivel de riesgo.
* Por diseño del principio de menor privilegio, la interfaz oculta de forma automática los botones de creación, edición o eliminación de registros, así como el acceso al panel administrativo de usuarios.

#### 5.4.3 Generación de Informes Ejecutivos en Formato PDF
Para reuniones de comité directivo o auditorías de cumplimiento de normas internacionales como ISO/IEC 27001:
1. En cualquier pantalla analítica o en el historial de solicitudes, haga clic en el botón **Reporte Ejecutivo (PDF)**.
2. El sistema compilará en segundos un documento formal de diseño limpio que incluye:
   * Encabezado corporativo con marca de tiempo y firma digital de la plataforma.
   * Resumen ejecutivo del período analizado con métricas cuantitativas clave.
   * Gráficas vectoriales consolidadas de tendencias de ataque.
   * Tabla resumida de los 10 principales indicadores de compromiso y las acciones de mitigación adoptadas.
3. El archivo se descarga directamente al equipo del directivo sin requerir procesamiento adicional.

---

## 6. Casos Borde y Preguntas Frecuentes

### P1: ¿Qué debo hacer si extravío mi dispositivo móvil o el código TOTP de 6 dígitos es rechazado repetidamente?
Si el código TOTP es rechazado de forma sistemática a pesar de escribirlo correctamente, la causa principal suele ser una desincronización horaria en su teléfono móvil. Ingrese a los ajustes de fecha y hora de su dispositivo y asegúrese de que la opción **"Fecha y hora automáticas"** (sincronización vía red NTP) se encuentre habilitada.

En caso de extravío físico o daño irreparable de su teléfono móvil, comuníquese con el **Administrador del SOC**. El Administrador accederá al módulo de usuarios de HoneyMetrics y ejecutará la acción **Restablecer MFA** sobre su cuenta. En su siguiente inicio de sesión con correo y contraseña, el sistema desplegará un nuevo código QR para que vuelva a enrolar un dispositivo autenticador desde cero.

### P2: ¿Por qué mi solicitud de exportación de telemetría permanece en estado "Pendiente de Aprobación"?
Las solicitudes de extracción de registros que abarcan un intervalo cronológico superior a 7 días calendario o cuyo volumen preliminar supera los 50.000 eventos de seguridad se clasifican automáticamente como extracciones masivas. Para proteger la estabilidad de los nodos de indexación de Wazuh y garantizar la debida custodia de la información, el sistema suspende la ejecución hasta recibir una confirmación humana explícita (*Human-in-the-Loop*).

El Administrador del sistema habrá recibido una notificación interactiva en su bot de Telegram con los detalles de su requerimiento. Una vez que el Administrador presione el botón de autorización, el estado de la solicitud pasará a "Procesando" y, finalmente, a "Completado", habilitando el botón de descarga del archivo JSONL.

### P3: ¿Qué ocurre cuando intento registrar una dirección IP privada (RFC 1918) o un IOC ya existente en el Threat Center?
HoneyMetrics v2.0 incorpora filtros sintácticos estrictos en el formulario de adición de indicadores. Si un consultor intenta introducir una dirección IP perteneciente a rangos privados definidos por la norma RFC 1918 (tales como `10.0.0.0/8`, `172.16.0.0/12` o `192.168.0.0/16`), el sistema mostrará una advertencia contextual solicitando confirmación explícita, indicando que el registro corresponde a una red interna y no a un actor perimetral hostil.

Por otro lado, si la dirección IP ya existe en la base de datos de amenazas, el sistema abortará la inserción duplicada y emitirá una notificación amarilla informando: *"La dirección IP ya se encuentra registrada en el sistema"*. En este caso, el operador debe buscar el registro preexistente mediante la barra de filtrado y proceder a actualizar sus notas o incrementar su criticidad.

### P4: ¿Por qué el reporte ejecutivo en PDF se descarga de forma instantánea mientras que la telemetría en JSONL toma más tiempo?
La diferencia radica en el volumen de datos y en la arquitectura de procesamiento:
* **Reporte Ejecutivo (PDF):** Se compila directamente en la memoria del navegador utilizando la biblioteca `jsPDF`. Utiliza únicamente los datos agregados ya visibles en pantalla (máximo unos pocos cientos de registros sintetizados), tardando menos de dos segundos en completarse.
* **Telemetría Cruda (JSONL):** Implica realizar una consulta exhaustiva contra los índices profundos de Wazuh OpenSearch, recuperando potencialmente decenas de miles de eventos de seguridad con todas sus cabeceras técnicas, metadatos de reglas, hashes y marcas temporales crudas. El backend debe extraer, estructurar y transmitir estos datos en streaming asíncrono, lo cual demanda tiempo de procesamiento proporcional al rango temporal solicitado.

### P5: ¿Por qué un usuario con rol Directivo de T.I. no puede visualizar los botones de adición, edición o borrado de amenazas?
Este comportamiento responde al estricto diseño de Control de Acceso Basado en Roles (RBAC) de HoneyMetrics v2.0. El perfil de Directivo de T.I. ha sido concebido para tareas de supervisión gerencial, gobernanza de riesgos y consulta ejecutiva.

Para evitar errores operativos accidentales o modificaciones de indicadores sin la debida justificación táctica de seguridad, los componentes interactivos de mutación (botones de creación, modificación de severidad y eliminación de IOCs) se deshabilitan y ocultan en la interfaz React para este rol. Asimismo, cualquier intento directo de invocar los endpoints REST correspondientes desde herramientas externas retornará un código de respuesta HTTP `403 Forbidden`.

### P6: ¿Qué operaciones técnicas se ejecutan exactamente cuando el Administrador pulsa "Aprobar Bloqueo" en Telegram?
Al pulsar el botón `✅ Aprobar Bloqueo` en la interfaz del bot de Telegram:
1. Telegram despacha una petición webhook cifrada al backend de FastAPI (`POST /api/v1/logs/webhook/telegram`), acompañada de la cabecera `X-Telegram-Bot-Api-Secret-Token`.
2. El servidor valida la autenticidad del token secreto mediante funciones de comparación de tiempo constante (`hmac.compare_digest`) para prevenir ataques de suplantación o SSRF.
3. El servicio de amenazas actualiza el estado de la dirección IP en la base de datos PostgreSQL a "Bloqueada".
4. Se inserta un registro inmutable en la Bóveda Forense de Auditoría (`threat_ips_vault`) documentando la fecha, la IP, el identificador del administrador y el canal de aprobación utilizado.
5. El backend despacha la orden de bloqueo al API del firewall perimetral (o ejecuta la regla de filtrado en tablas de red locales) para descartar el tráfico proveniente de dicha dirección.
6. El mensaje original de Telegram se actualiza automáticamente mostrando el texto: *"IP bloqueada exitosamente en el perímetro"*.

### P7: ¿Cómo responde la plataforma si se interrumpe la conectividad con el clúster de Wazuh Indexer?
HoneyMetrics v2.0 incorpora un mecanismo de resiliencia y degradación elegante (*Graceful Fallback*). Si el nodo de indexación de Wazuh experimenta sobrecarga o una desconexión temporal de red, el backend de la plataforma detecta el fallo tras un tiempo de espera controlado y conmuta de inmediato a modo de contingencia:
* La interfaz desplegará un banner informativo indicando que el SIEM se encuentra temporalmente inaccesible.
* Los módulos del Dashboard continuarán presentando los últimos datos consolidados disponibles en el repositorio local.
* Las funcionalidades del Threat Intelligence Center, la gestión de usuarios y la administración de perfiles continuarán operando con normalidad, ya que su persistencia reside en la base de datos PostgreSQL independiente. Tan pronto como el clúster de Wazuh restablece su servicio, la sincronización en tiempo real se reanuda de forma transparente.

### P8: ¿Cuánto tiempo permanecen disponibles los archivos de logs exportados en el servidor antes de su purga automática?
Los archivos de extracción de telemetría en formato `.jsonl` generados en el servidor se conservan durante un período máximo de **7 días calendario** a partir del momento en que su estado pasa a "Completado".

Transcurrido este plazo, una tarea programada interna de mantenimiento en el servidor elimina físicamente los archivos del sistema de archivos para evitar el agotamiento del espacio en disco. En la interfaz del módulo de logs, el registro histórico permanecerá visible con fines de auditoría, pero su enlace de descarga figurará como expirado, requiriendo que el analista genere una nueva solicitud si precisa consultar la información nuevamente.

### P9: ¿Qué debo hacer si recibo el mensaje de error "HTTP 403 Forbidden - Acceso Restringido" tras hacer clic en un enlace de la interfaz?
El error HTTP 403 ocurre habitualmente bajo dos circunstancias:
1. **Expiración de la sesión activa:** Los tokens JWT de sesión poseen una vigencia de 30 minutos por políticas de seguridad. Si su sesión caducó mientras navegaba, cierre la ventana emergente, haga clic en el menú de usuario, seleccione **Cerrar Sesión** e inicie sesión nuevamente con sus credenciales y código TOTP.
2. **Privilegios insuficientes:** Intentó acceder a una función exclusiva de otro rol (por ejemplo, acceder a la gestión de usuarios siendo Consultor o solicitar descargas masivas siendo Directivo). Verifique que la acción corresponda a las funciones autorizadas para su perfil en la matriz RBAC de la Sección 5.

### P10: ¿Cuál es el procedimiento adecuado para cerrar sesión de forma segura en puestos compartidos del SOC?
En estaciones de trabajo compartidas donde múltiples analistas operan en diferentes turnos, no basta con simplemente cerrar la pestaña del navegador:
1. Haga clic sobre su nombre o avatar en la esquina superior derecha de la barra de navegación superior.
2. Seleccione la opción **Cerrar Sesión** en el menú desplegable.
3. El sistema emitirá una petición al backend para invalidar el token de acceso, limpiará los identificadores temporales almacenados en el estado de la aplicación React y purgará las cookies de autenticación con directiva `HttpOnly`.
4. La interfaz lo redirigirá a la pantalla pública de bienvenida.
5. Cierre completamente la ventana del navegador web para asegurar que la memoria caché de sesión quede totalmente liberada para el siguiente operador de turno.
