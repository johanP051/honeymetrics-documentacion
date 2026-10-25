# Diagramas UML HoneyMetrics v2.0 (Especificación Canónica)

> **Ver también:**  
> - [Manual Técnico & Arquitectura](../manual-tecnico.md) — Lógica de negocio, service layer y contratos REST.  
> - [Diccionario de Datos](../diccionario-datos.md) — Modelo relacional físico de PostgreSQL 16 y tablas del sistema.  
> - [Especificación IEEE 830 de Casos de Uso](./MD_Definiciones/Diagramas_Casos_de_Uso.md) — Fichas detalladas con precondiciones y flujos básicos/alternos.  

---

## Índice General

1. [Diagramas de Secuencia (15 Flujos Canónicos)](#1-diagramas-de-secuencia-15-flujos-canonicos)
   - [RF01 Autenticación MFA v2](#rf01-autenticacion-mfa-v2)
   - [RF02 Consultar Telemetría y Métricas SOC (Dashboard)](#rf02-consultar-telemetria-y-metricas-soc-dashboard)
   - [RF03 Consultar Lista Negra IP (Threat Center)](#rf03-consultar-lista-negra-ip-threat-center)
   - [RF03 Registrar IP en Lista Negra](#rf03-registrar-ip-en-lista-negra)
   - [RF04 Actualizar IP en Lista Negra](#rf04-actualizar-ip-en-lista-negra)
   - [RF05 Eliminar IP de Lista Negra](#rf05-eliminar-ip-de-lista-negra)
   - [RF06 Consultar Usuarios](#rf06-consultar-usuarios)
   - [RF06 Crear Usuario](#rf06-crear-usuario)
   - [RF06 Actualizar Usuario](#rf06-actualizar-usuario)
   - [RF06 Eliminar Usuario](#rf06-eliminar-usuario)
   - [RF08 Exportación Telegram](#rf08-exportacion-telegram)
   - [RF10 Descarga de Logs](#rf10-descarga-de-logs)
   - [RF Generar Reporte PDF (Navegador)](#rf-generar-reporte-pdf-navegador)
   - [RF11 Bloqueo IP y Publicación MISP](#rf11-bloqueo-ip-y-publicacion-misp)
   - [RF12 Inferencia HMM y CTI](#rf12-inferencia-hmm-y-cti)
2. [Diagramas de Casos de Uso (8 Subsistemas + Tablas Gualivá)](#2-diagramas-de-casos-de-uso-8-subsistemas-tablas-gualiva)
   - [CU00 Jerarquía de actores](#cu00-jerarquia-de-actores)
   - [CU01 Acceso e identidad](#cu01-acceso-e-identidad)
   - [CU02 Dashboard y métricas](#cu02-dashboard-y-metricas)
   - [CU03 Lista negra](#cu03-lista-negra)
   - [CU04 Exportación de logs](#cu04-exportacion-de-logs)
   - [CU05 Administración](#cu05-administracion)
   - [CU06 Machine Learning](#cu06-machine-learning)
   - [CU07 Ingesta de eventos](#cu07-ingesta-de-eventos)
3. [Diagramas de Actividades (14 Flujos Operativos)](#3-diagramas-de-actividades-14-flujos-operativos)
   - [AD01 Iniciar Sesión](#ad01-iniciar-sesion)
   - [AD02 Eliminar IP Lista Negra](#ad02-eliminar-ip-lista-negra)
   - [AD03 Entrenar Modelo ML](#ad03-entrenar-modelo-ml)
   - [AD04 Ingestar Logs Telemetría](#ad04-ingestar-logs-telemetria)
   - [AD05 Consultar Telemetría SOC](#ad05-consultar-telemetria-soc)
   - [AD06 Crear IP Lista Negra](#ad06-crear-ip-lista-negra)
   - [AD07 Consultar IP Lista Negra](#ad07-consultar-ip-lista-negra)
   - [AD08 Actualizar IP Lista Negra](#ad08-actualizar-ip-lista-negra)
   - [AD09 Crear Usuario](#ad09-crear-usuario)
   - [AD10 Consultar Usuario](#ad10-consultar-usuario)
   - [AD11 Actualizar Usuario](#ad11-actualizar-usuario)
   - [AD12 Eliminar Usuario](#ad12-eliminar-usuario)
   - [AD Descargar Reporte PDF (Navegador)](#ad-descargar-reporte-pdf-navegador)
   - [AD Autorización Dual de Exportación en Telegram](#ad-autorizacion-dual-de-exportacion-en-telegram)
4. [Diagrama de Clases (Arquitectura Limpia & Desglose Modular)](#4-diagrama-de-clases-arquitectura-limpia-desglose-modular)
   - [4.1 Modelo de dominio](#41-modelo-de-dominio)
   - [4.2 API: identidad y acceso](#42-api-identidad-y-acceso)
   - [4.3 API: amenazas, logs e ingesta](#43-api-amenazas-logs-e-ingesta)
   - [4.4 Servicios: identidad y notificaciones](#44-servicios-identidad-y-notificaciones)
   - [4.5 Servicios: amenazas, logs y dashboard](#45-servicios-amenazas-logs-y-dashboard)
   - [4.6 Core y seguridad](#46-core-y-seguridad)
5. [Diagrama de Modelo Entidad-Relación (MER)](#5-diagrama-de-modelo-entidad-relacion-mer)
   - [5.1 Trazabilidad MER ↔ Modelos SQLAlchemy ↔ Diagrama de Clases](#51-trazabilidad-mer-modelos-sqlalchemy-diagrama-de-clases)

---

## 1. Diagramas de Secuencia (15 Flujos Canónicos)

> **Estándar Arquitectónico:** Líneas de vida normalizadas en 5 capas desacopladas:  
> `Usuario / Administrador` $\longrightarrow$ `Vista` $\longrightarrow$ `Controlador` $\longrightarrow$ `Modelo` $\longrightarrow$ `Base de datos`.  
> Todos los diagramas con precondición incorporan su marco `ref` con etiqueta canónica visible.

### RF01 Autenticación MFA v2
![RF01 Autenticación MFA v2](../assets/uml/RF01_Autenticacion_MFA_v2.png)

### RF02 Consultar Telemetría y Métricas SOC (Dashboard)
![RF02 Consultar Telemetría y Métricas SOC (Dashboard)](../assets/uml/RF02_Consultar_Telemetria_y_Metricas_SOC_Dashboard.png)

### RF03 Consultar Lista Negra IP (Threat Center)
![RF03 Consultar Lista Negra IP (Threat Center)](../assets/uml/RF03_Consultar_Lista_Negra_IP_Threat_Center.png)

### RF03 Registrar IP en Lista Negra
![RF03 Registrar IP en Lista Negra](../assets/uml/RF03_Registrar_IP_en_Lista_Negra.png)

### RF04 Actualizar IP en Lista Negra
![RF04 Actualizar IP en Lista Negra](../assets/uml/RF04_Actualizar_IP_en_Lista_Negra.png)

### RF05 Eliminar IP de Lista Negra
![RF05 Eliminar IP de Lista Negra](../assets/uml/RF05_Eliminar_IP_de_Lista_Negra.png)

### RF06 Consultar Usuarios
![RF06 Consultar Usuarios](../assets/uml/RF06_Consultar_Usuarios.png)

### RF06 Crear Usuario
![RF06 Crear Usuario](../assets/uml/RF06_Crear_Usuario.png)

### RF06 Actualizar Usuario
![RF06 Actualizar Usuario](../assets/uml/RF06_Actualizar_Usuario.png)

### RF06 Eliminar Usuario
![RF06 Eliminar Usuario](../assets/uml/RF06_Eliminar_Usuario.png)

### RF08 Exportación Telegram
![RF08 Exportación Telegram](../assets/uml/RF08_Exportacion_Telegram.png)

### RF10 Descarga de Logs
![RF10 Descarga de Logs](../assets/uml/RF10_Descarga_de_Logs.png)

### RF Generar Reporte PDF (Navegador)
Diagrama de interacción que describe la generación del reporte técnico en PDF directamente en el cliente (SPA React), consultando las definiciones de telemetría y estadísticas agregadas al API backend, y ensamblando el archivo descargable de forma local en el navegador del usuario:

![RF Generar Reporte PDF](../assets/uml/RF_Generar_Reporte_PDF.png)

### RF11 Bloqueo IP y Publicación MISP
![RF11 Bloqueo IP y Publicación MISP](../assets/uml/RF11_Bloqueo_IP_y_Publicacion_MISP.png)

### RF12 Inferencia HMM y CTI
![RF12 Inferencia HMM y CTI](../assets/uml/RF12_Inferencia_HMM_y_CTI.png)

---

## 2. Diagramas de Casos de Uso (8 Subsistemas + Tablas Gualivá)

### CU00 Jerarquía de actores
![CU00 Jerarquía de actores](../assets/uml/CU00_Jerarquia_de_actores.png)

| Actor | Descripción |
| :--- | :--- |
| **Usuario autenticado** | Actor abstracto. Agrupa el conjunto de capacidades operativas permitidas a cualquier cuenta con sesión válida en el sistema. |
| **Directivo de T.I.** | Hereda de Usuario autenticado. Consulta resúmenes estratégicos y visualizaciones agregadas para la toma de decisiones gerenciales; no muta datos operativos. |
| **Analista de datos** | Hereda de Usuario autenticado. Examina datos forenses de intrusión: solicita exportaciones masivas, analiza secuencias de atacantes y audita modelos ML. |
| **Consultor de Ciberseguridad** | Hereda de Usuario autenticado. Mitiga eventos de riesgo operativo: administra el catálogo de bloqueo de IP (lista negra) y examina anomalías detectadas por el SOC. |
| **Superusuario** | Hereda de Usuario autenticado. Administra integralmente la plataforma: gestión de usuarios, creación y asignación de roles RBAC, y resolución de autorizaciones duales de exportación. |

---

### CU01 Acceso e identidad
![CU01 Acceso e identidad](../assets/uml/CU01_Acceso_e_identidad.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Iniciar sesión | Visitante | Caso de uso base, donde el visitante suministra sus credenciales de acceso para ingresar a la plataforma HoneyMetrics. |
| Validar credenciales | — | Es un incluido de Iniciar sesión; el sistema verifica que el identificador exista y que el hash de la contraseña coincida con el registro de base de datos. |
| Validar segundo factor | — | Es un incluido de Iniciar sesión; el sistema solicita y comprueba el código temporal de seis dígitos generado por la aplicación autenticadora (TOTP). |
| Vincular autenticador | — | Extiende a Validar segundo factor; ocurre exclusivamente durante el primer ingreso, cuando la cuenta no tiene semilla TOTP registrada y el sistema despliega el código QR. |
| Cambiar contraseña inicial | — | Extiende a Iniciar sesión; ocurre cuando la cuenta fue creada provisionalmente por el Superusuario y se exige al usuario renovar su clave obligatoriamente. |
| Recuperar contraseña | — | Extiende a Iniciar sesión; ocurre cuando el usuario solicita el restablecimiento de su clave mediante el envío de un enlace con token firmado a su correo registrado. |
| Validar fortaleza de contraseña | — | Es un incluido de Recuperar contraseña y de Cambiar contraseña; el sistema comprueba los requisitos de longitud, mayúsculas, números y símbolos. |
| Gestionar perfil | Usuario autenticado | Caso de uso base, donde el usuario consulta o actualiza sus preferencias de interfaz, zona horaria, tema visual e identificador de Telegram. |
| Cambiar contraseña | Usuario autenticado | Caso de uso base, donde el usuario autenticado reemplaza voluntariamente su contraseña actual suministrando la clave anterior. |
| Cerrar sesión | Usuario autenticado | Caso de uso base, donde el usuario finaliza su sesión activa, provocando la revocación inmediata y persistida del token JWT. |

---

### CU02 Dashboard y métricas
![CU02 Dashboard y métricas](../assets/uml/CU02_Dashboard_y_metricas.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Consultar dashboard de eventos anómalos de seguridad | Superusuario, Directivo de T.I., Analista de datos, Consultor de Ciberseguridad | Caso de uso base, donde los usuarios autorizados visualizan en tiempo real los indicadores consolidados, distribución geográfica y volumen de intrusiones capturadas. |
| Consultar métricas | Superusuario, Directivo de T.I., Analista de datos, Consultor de Ciberseguridad | Caso de uso base, donde el analista consulta las estadísticas agregadas de tráfico, puertos atacados y tiempos de persistencia de las conexiones sospechosas. |
| Filtrar por intervalo de tiempo específico | Superusuario, Directivo de T.I., Analista de datos, Consultor de Ciberseguridad | Extiende a Consultar dashboard de eventos anómalos de seguridad; ocurre cuando el operador delimita la ventana de observación temporal de los eventos graficados. |

---

### CU03 Lista negra
![CU03 Lista negra](../assets/uml/CU03_Lista_negra.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Consultar lista negra | Superusuario, Directivo de T.I., Consultor de Ciberseguridad | Caso de uso base, donde el operador visualiza el catálogo de direcciones IP bloqueadas o bajo sospecha en el centro de amenazas (el Directivo en modo solo lectura). |
| Registrar IP | Superusuario, Directivo de T.I., Consultor de Ciberseguridad | Caso de uso base, donde el operador ingresa manualmente una nueva dirección IP al catálogo de bloqueo preventivo asignando severidad y justificación. |
| Validar IP protegida | — | Es un incluido de Registrar IP; el sistema valida estrictamente que la IP ingresada no pertenezca a rangos locales (RFC 1918), gateways, DNS públicos ni infraestructura propia. |
| Determinar estado de bloqueo | — | Es un incluido de Registrar IP y de Editar IP; el sistema evalúa la severidad y el score de amenaza para marcar formalmente la IP como bloqueada en la regla perimetral. |
| Editar IP | Superusuario, Directivo de T.I., Consultor de Ciberseguridad | Extiende a Consultar lista negra; ocurre cuando el operador selecciona un registro previamente listado y modifica su justificación, estado o nivel de severidad. |
| Eliminar IP | Superusuario, Directivo de T.I., Consultor de Ciberseguridad | Extiende a Consultar lista negra; ocurre cuando el operador retira una dirección IP del catálogo activo, archivando el registro con trazabilidad forense en la bóveda histórica. |

---

### CU04 Exportación de logs
![CU04 Exportación de logs](../assets/uml/CU04_Exportacion_de_logs.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Solicitar exportación | Superusuario, Analista de datos | Caso de uso base, donde el usuario formula una petición de extracción masiva de registros de telemetría y eventos forenses delimitando rangos de fechas y filtros. |
| Verificar volumen de la solicitud | — | Es un incluido de Solicitar exportación; el sistema calcula el número estimado de eventos y determina si supera el umbral crítico (más de 50.000 registros o 7 días) que exige aprobación dual. |
| Aprobar exportación masiva | Superusuario | Extiende a Solicitar exportación; ocurre exclusivamente cuando la solicitud supera el umbral crítico, despachando una notificación interactiva fuera de banda vía Telegram para su autorización. |
| Notificar resolución | — | Extiende a Aprobar exportación masiva; ocurre cuando el Superusuario emite su voto de aprobación o rechazo en Telegram, comunicando el veredicto al solicitante. |
| Consultar historial de exportaciones | Superusuario, Analista de datos | Caso de uso base, donde el solicitante examina la bitácora de extracciones previas, sus identificadores, estados de procesamiento y firmas criptográficas SHA-256. |
| Descargar archivo | Superusuario, Analista de datos | Extiende a Consultar historial de exportaciones; ocurre cuando el lote autorizado finaliza su empaquetado y el usuario descarga el archivo comprimido. |
| Validar titularidad y vigencia | — | Es un incluido de Descargar archivo; el sistema comprueba que el token de descarga pertenezca al usuario solicitante y que el enlace temporal no haya expirado. |
| Generar reporte de esquema | Superusuario, Analista de datos | Caso de uso base, donde el usuario descarga la especificación de tipos de datos, columnas y metadatos de los logs forenses para pipelines de análisis. |

---

### CU05 Administración
![CU05 Administración](../assets/uml/CU05_Administracion.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Consultar usuarios | Superusuario | Caso de uso base, donde el Superusuario examina la nómina completa de cuentas dadas de alta en la plataforma, auditando sus roles, estados y fechas de acceso. |
| Modificar usuario | — | Extiende a Consultar usuarios; ocurre cuando el Superusuario selecciona una cuenta del listado para modificar sus datos personales, correo o rol RBAC asignado. |
| Desactivar usuario | — | Extiende a Consultar usuarios; ocurre cuando el Superusuario suspende preventivamente el acceso a una cuenta seleccionada sin purgar su historial. |
| Validar autoprotección | — | Es un incluido de Modificar usuario y de Desactivar usuario; el sistema valida que la cuenta destino no corresponda al propio Superusuario activo para evitar bloqueos accidentales. |
| Registrar usuario | Superusuario | Caso de uso base, donde el Superusuario da de alta una nueva cuenta en la plataforma suministrando datos de identidad y asignando un perfil operativo. |
| Enviar credenciales de bienvenida | — | Extiende a Registrar usuario; ocurre cuando el sistema despacha automáticamente por correo seguro las credenciales iniciales de acceso y el enlace de primer inicio. |
| Consultar roles | Superusuario | Caso de uso base, donde el Superusuario inspecciona el catálogo de perfiles de acceso y permisos RBAC configurados en la plataforma. |
| Modificar rol | — | Extiende a Consultar roles; ocurre cuando el Superusuario selecciona un rol existente y actualiza su nombre descriptivo o conjunto de permisos vinculados. |
| Eliminar rol | — | Extiende a Consultar roles; ocurre cuando el Superusuario selecciona un rol para suprimirlo definitivamente de la plataforma. |
| Verificar rol sin usuarios | — | Es un incluido de Eliminar rol; el sistema valida estrictamente que ninguna cuenta activa o inactiva permanezca asociada al rol que se desea eliminar. |
| Crear rol | Superusuario | Caso de uso base, donde el Superusuario formula un nuevo perfil de privilegios asignando identificador y alcances de seguridad. |

---

### CU06 Machine Learning
![CU06 Machine Learning](../assets/uml/CU06_Machine_Learning.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Analizar sesión de atacante | Superusuario, Analista de datos | Caso de uso base, donde el usuario examina la secuencia cronológica de comandos y técnicas ejecutadas por un atacante durante su interacción con los honeypots. |
| Descartar atributos de identidad | — | Es un incluido de Analizar sesión de atacante; el pipeline de datos elimina direcciones IP y marcas volátiles para garantizar que el modelo aprenda comportamientos puros sin fuga (*anti-leakage*). |
| Curar arquetipo de sesión | — | Extiende a Analizar sesión de atacante; ocurre cuando el analista de datos calibra manualmente la etiqueta del arquetipo de ataque asignada por el modelo predictivo. |
| Consultar clasificación y score | Superusuario, Consultor de Ciberseguridad, Analista de datos | Caso de uso base, donde los operadores consultan la técnica MITRE ATT&CK identificada y la puntuación de riesgo estimada para un evento sospechoso. |
| Consultar estado de modelos | Superusuario, Analista de datos | Caso de uso base, donde se audita la versión activa en producción, huella criptográfica SHA-256, fecha de entrenamiento y latencia de inferencia de cada archivo `.joblib`. |
| Forzar reentrenamiento | Superusuario, Analista de datos | Caso de uso base, donde el analista de datos dispara un ciclo de reentrenamiento supervisado a partir de nuevos lotes de telemetría empírica validada. |
| Verificar degradación del modelo | — | Es un incluido de Forzar reentrenamiento; el sistema evalúa Out-Of-Fold (OOF) el nuevo modelo y comprueba que su F1-Score supere al baseline y su latencia no exceda el SLA (< 5 ms). |
| Revertir versión del modelo | — | Extiende a Verificar degradación del modelo; ocurre si el modelo candidato no supera los umbrales de rendimiento, restaurando inmediatamente la versión previa inmutable. |

---

### CU07 Ingesta de eventos
![CU07 Ingesta de eventos](../assets/uml/CU07_Ingesta_de_eventos.png)

| Caso de Uso | Actor(es) | Descripción |
| :--- | :--- | :--- |
| Ingestar eventos | Sistema Wazuh | Caso de uso base, donde el agente colector o sensor perimetral despacha lotes de eventos de seguridad crudos hacia el endpoint de ingestión del API. |
| Clasificar técnica MITRE | — | Es un incluido de Ingestar eventos; el motor de Machine Learning asigna a cada evento la técnica táctica de intrusión correspondiente según el framework MITRE ATT&CK. |
| Calcular score de riesgo | — | Es un incluido de Ingestar eventos; el sistema computa una puntuación de riesgo estandarizada de 0 a 100 basada en severidad, frecuencia de puertos y persistencia temporal. |
| Actualizar estado de bloqueo | — | Extiende a Calcular score de riesgo; ocurre de manera automatizada si la puntuación de amenaza supera el umbral crítico (> 70), matriculando la dirección IP en la lista de bloqueo preventivo. |

---

## 3. Diagramas de Actividades (14 Flujos Operativos)

### AD01 Iniciar Sesión
![AD01 Iniciar Sesión](../assets/uml/AD01_Iniciar_Sesion.png)

### AD02 Eliminar IP Lista Negra
![AD02 Eliminar IP Lista Negra](../assets/uml/AD02_Eliminar_IP_ListaNegra.png)

### AD03 Entrenar Modelo ML
![AD03 Entrenar Modelo ML](../assets/uml/AD03_Entrenar_Modelo_ML.png)

### AD04 Ingestar Logs Telemetría
![AD04 Ingestar Logs Telemetría](../assets/uml/AD04_Ingestar_Logs_Telemetria.png)

### AD05 Consultar Telemetría SOC
![AD05 Consultar Telemetría SOC](../assets/uml/AD05_Consultar_Telemetria_SOC.png)

### AD06 Crear IP Lista Negra
![AD06 Crear IP Lista Negra](../assets/uml/AD06_Crear_IP_ListaNegra.png)

### AD07 Consultar IP Lista Negra
![AD07 Consultar IP Lista Negra](../assets/uml/AD07_Consultar_IP_ListaNegra.png)

### AD08 Actualizar IP Lista Negra
![AD08 Actualizar IP Lista Negra](../assets/uml/AD08_Actualizar_IP_ListaNegra.png)

### AD09 Crear Usuario
![AD09 Crear Usuario](../assets/uml/AD09_Crear_Usuario.png)

### AD10 Consultar Usuario
![AD10 Consultar Usuario](../assets/uml/AD10_Consultar_Usuario.png)

### AD11 Actualizar Usuario
![AD11 Actualizar Usuario](../assets/uml/AD11_Actualizar_Usuario.png)

### AD12 Eliminar Usuario
![AD12 Eliminar Usuario](../assets/uml/AD12_Eliminar_Usuario.png)

### AD Descargar Reporte PDF (Navegador)
![AD Descargar Reporte PDF](../assets/uml/AD_Descargar_Reporte_PDF.png)

### AD Autorización Dual de Exportación en Telegram
![AD Autorización Dual de Exportación en Telegram](../assets/uml/AD_Autorizar_Exportacion_Telegram.png)

---

## 4. Diagrama de Clases (Arquitectura Limpia & Desglose Modular)

El diagrama estructural se divide por capas para garantizar legibilidad completa. Cada clase de dominio declara el estereotipo `«table: nombre_tabla»`, de modo que el vínculo entre el diagrama de clases y el MER sea verificable uno a uno:

| Diagrama | Capa Arquitectónica | Origen en el Código Fuente |
| :--- | :--- | :--- |
| **CD01** | Modelo de dominio (persistencia) | `app/models/` |
| **CD02** | API REST: identidad y acceso | `app/api/v1/endpoints/` (`auth`, `users`, `roles`, `health`) |
| **CD03** | API REST: amenazas, logs e ingesta | `app/api/v1/endpoints/` (`threats`, `logs`, `dashboard`, `ingest`) |
| **CD04** | Servicios: identidad y notificaciones | `app/services/` (`auth`, `user`, `role`, `email`, `telegram`) |
| **CD05** | Servicios: amenazas, logs y dashboard | `app/services/` (`threat`, `threat_crud`, `logs`, `dashboard`) |
| **CD06** | Core y seguridad | `app/core/` (`config`, `security`, `permissions`, `rate_limit`) y `app/api/deps.py` |

### 4.1 Modelo de dominio
![CD01 Modelo de Dominio](../assets/uml/CD01_Domain_Models.png)

### 4.2 API: identidad y acceso
![CD02 API Identidad](../assets/uml/CD02_API_Identity.png)

### 4.3 API: amenazas, logs e ingesta
![CD03 API Amenazas Logs Ingesta](../assets/uml/CD03_API_Threats_Logs_Ingest.png)

### 4.4 Servicios: identidad y notificaciones
![CD04 Servicios Identidad](../assets/uml/CD04_Services_Identity.png)

### 4.5 Servicios: amenazas, logs y dashboard
![CD05 Servicios Amenazas Logs](../assets/uml/CD05_Services_Threats_Logs.png)

### 4.6 Core y seguridad
![CD06 Core Seguridad](../assets/uml/CD06_Core_Security.png)

### Vista General: Diagrama de Clases Completo HoneyMetrics
![Diagrama de Clases Completo HoneyMetrics](../assets/uml/Diagrama_de_Clases_HoneyMetrics.png)

---

## 5. Diagrama de Modelo Entidad-Relación (MER)

**Leyenda:** Borde continuo = implementado en producción; Borde punteado y etiqueta `«pendiente»` = extensión arquitectónica por desarrollar.

![Modelo Entidad-Relación HoneyMetrics: Esquema Actual y Extensiones Pendientes](../assets/uml/MER_HoneyMetrics_Actual_Pendiente.png)

El MER reúne el esquema implementado y las extensiones previstas sin alterar lo existente: no se renombran, mueven ni eliminan columnas actuales. Las relaciones continuas corresponden a claves foráneas declaradas; las punteadas, a referencias lógicas o a estructuras aún no implementadas.

- **Esquema implementado (8 Tablas en PostgreSQL 16 Alpine):** `roles`, `users`, `permissions`, `role_permissions`, `threat_ips`, `threat_ips_vault`, `log_exports` y `revoked_tokens`.
- **Extensiones pendientes:** tablas `user_profiles`, `blacklist_records`, `user_saved_filters` y `security_alerts`; además de columnas nuevas en `roles`, `users` y `log_exports`.

![Modelo Entidad-Relación Físico Real (8 Tablas Implementadas)](../assets/uml/MER_HoneyMetrics_Real.png)

### 5.1 Trazabilidad MER ↔ Modelos SQLAlchemy ↔ Diagrama de Clases

| Tabla | Clase del Modelo (`app/models/`) | Clase UML | Estado Físico |
| :--- | :--- | :--- | :--- |
| `roles` | `Role` (`role.py`) | `Role` | Implementada |
| `users` | `User` (`user.py`) | `User` | Implementada |
| `permissions` | `Permission` (`permission.py`) | `Permission` | Implementada |
| `role_permissions` | `RolePermission` (`role_permission.py`) | `RolePermission` | Implementada |
| `threat_ips` | `ThreatIP` (`threat.py`) | `ThreatIP` | Implementada |
| `threat_ips_vault` | `ThreatIPVault` (`threat.py`) | `ThreatIPVault` | Implementada |
| `log_exports` | `LogExport` (`log_export.py`) | `LogExport` | Implementada |
| `revoked_tokens` | `RevokedToken` (`revoked_token.py`) | `RevokedToken` | Implementada |
| `user_profiles` | — | — | Propuesta Pendiente |
| `blacklist_records` | — | — | Propuesta Pendiente |
| `user_saved_filters` | — | — | Propuesta Pendiente |
| `security_alerts` | — | — | Propuesta Pendiente |
