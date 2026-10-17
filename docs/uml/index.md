# Diagramas UML HoneyMetrics v2.0 (Especificación Canónica)

## Índice
1. [Diagramas de Secuencia](#1-diagramas-de-secuencia)
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
   - [RF11 Bloqueo IP y Publicación MISP](#rf11-bloqueo-ip-y-publicacion-misp)
   - [RF12 Inferencia HMM y CTI](#rf12-inferencia-hmm-y-cti)
2. [Diagramas de Casos de Uso](#2-diagramas-de-casos-de-uso)
   - [CU00 Jerarquía de actores](#cu00-jerarquia-de-actores)
   - [CU01 Acceso e identidad](#cu01-acceso-e-identidad)
   - [CU02 Dashboard y métricas](#cu02-dashboard-y-metricas)
   - [CU03 Lista negra](#cu03-lista-negra)
   - [CU04 Exportación de logs](#cu04-exportacion-de-logs)
   - [CU05 Administración](#cu05-administracion)
   - [CU06 Machine Learning](#cu06-machine-learning)
   - [CU07 Ingesta de eventos](#cu07-ingesta-de-eventos)
3. [Descripciones de Casos de Uso](#3-descripciones-de-casos-de-uso)
4. [Diagramas de Actividades](#4-diagramas-de-actividades)
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
   - [AD Generar Reporte Telegram](#ad-generar-reporte-telegram)
5. [Diagrama de Clases](#5-diagrama-de-clases)
6. [Diagrama de Modelo Entidad-Relación (MER)](#6-diagrama-de-modelo-entidad-relacion-mer)

---

## 1. Diagramas de Secuencia

> **Estándar Arquitectónico:** Líneas de vida normalizadas en 5 capas desacopladas:  
> `Usuario / Administrador` $\longrightarrow$ `Vista` $\longrightarrow$ `Controlador` $\longrightarrow$ `Modelo` $\longrightarrow$ `Base de datos`.  
> Todos los diagramas con precondición incorporan su marco `ref` con etiqueta canónica visible.

### RF01 Autenticación MFA v2
![RF01 Autenticación MFA v2](./FinalSVGs_v2/RF01%20Autenticaci%C3%B3n%20MFA%20v2.svg)

### RF02 Consultar Telemetría y Métricas SOC (Dashboard)
![RF02 Consultar Telemetría y Métricas SOC (Dashboard)](./FinalSVGs_v2/RF02%20Consultar%20Telemetr%C3%ADa%20y%20M%C3%A9tricas%20SOC%20%28Dashboard%29.svg)

### RF03 Consultar Lista Negra IP (Threat Center)
![RF03 Consultar Lista Negra IP (Threat Center)](./FinalSVGs_v2/RF03%20Consultar%20Lista%20Negra%20IP%20%28Threat%20Center%29.svg)

### RF03 Registrar IP en Lista Negra
![RF03 Registrar IP en Lista Negra](./FinalSVGs_v2/RF03%20Registrar%20IP%20en%20Lista%20Negra.svg)

### RF04 Actualizar IP en Lista Negra
![RF04 Actualizar IP en Lista Negra](./FinalSVGs_v2/RF04%20Actualizar%20IP%20en%20Lista%20Negra.svg)

### RF05 Eliminar IP de Lista Negra
![RF05 Eliminar IP de Lista Negra](./FinalSVGs_v2/RF05%20Eliminar%20IP%20de%20Lista%20Negra.svg)

### RF06 Consultar Usuarios
![RF06 Consultar Usuarios](./FinalSVGs_v2/RF06%20Consultar%20Usuarios.svg)

### RF06 Crear Usuario
![RF06 Crear Usuario](./FinalSVGs_v2/RF06%20Crear%20Usuario.svg)

### RF06 Actualizar Usuario
![RF06 Actualizar Usuario](./FinalSVGs_v2/RF06%20Actualizar%20Usuario.svg)

### RF06 Eliminar Usuario
![RF06 Eliminar Usuario](./FinalSVGs_v2/RF06%20Eliminar%20Usuario.svg)

### RF08 Exportación Telegram
![RF08 Exportación Telegram](./FinalSVGs_v2/RF08%20Exportacion%20Telegram.svg)

### RF10 Descarga de Logs
![RF10 Descarga de Logs](./FinalSVGs_v2/RF10%20Descarga%20de%20Logs.svg)

### RF11 Bloqueo IP y Publicación MISP
![RF11 Bloqueo IP y Publicación MISP](./FinalSVGs_v2/RF11%20Bloqueo%20IP%20y%20Publicacion%20MISP.svg)

### RF12 Inferencia HMM y CTI
![RF12 Inferencia HMM y CTI](./FinalSVGs_v2/RF12%20Inferencia%20HMM%20y%20CTI.svg)

---

## 2. Diagramas de Casos de Uso

### CU00 Jerarquía de actores
![CU00 Jerarquía de actores](./FinalSVGs_v2/CU00%20Jerarqu%C3%ADa%20de%20actores.svg)

### CU01 Acceso e identidad
![CU01 Acceso e identidad](./FinalSVGs_v2/CU01%20Acceso%20e%20identidad.svg)

### CU02 Dashboard y métricas
![CU02 Dashboard y métricas](./FinalSVGs_v2/CU02%20Dashboard%20y%20botnets.svg)

### CU03 Lista negra
![CU03 Lista negra](./FinalSVGs_v2/CU03%20Lista%20negra.svg)

### CU04 Exportación de logs
![CU04 Exportación de logs](./FinalSVGs_v2/CU04%20Exportaci%C3%B3n%20de%20logs.svg)

### CU05 Administración
![CU05 Administración](./FinalSVGs_v2/CU05%20Administraci%C3%B3n.svg)

### CU06 Machine Learning
![CU06 Machine Learning](./FinalSVGs_v2/CU06%20Machine%20Learning.svg)

### CU07 Ingesta de eventos
![CU07 Ingesta de eventos](./FinalSVGs_v2/CU07%20Ingesta%20de%20eventos.svg)

---

## 3. Descripciones de Casos de Uso

Se asume la estructura del estándar IEEE 830 para las descripciones de casos de uso del sistema HoneyMetrics (actores, precondiciones, flujo normal, flujos alternativos y excepciones).

Para consultar la matriz completa de casos de uso y especificación formal paso a paso, remitirse a:
- [Diagramas_Casos_de_Uso.md](./MD_Definiciones/Diagramas_Casos_de_Uso.md)

---

## 4. Diagramas de Actividades

### AD01 Iniciar Sesión
![AD01 Iniciar Sesión](./FinalSVGs_v2/AD01_Iniciar_Sesion.svg)

### AD02 Eliminar IP Lista Negra
![AD02 Eliminar IP Lista Negra](./FinalSVGs_v2/AD02_Eliminar_IP_ListaNegra.svg)

### AD03 Entrenar Modelo ML
![AD03 Entrenar Modelo ML](./FinalSVGs_v2/AD03_Entrenar_Modelo_ML.svg)

### AD04 Ingestar Logs Telemetría
![AD04 Ingestar Logs Telemetría](./FinalSVGs_v2/AD04_Ingestar_Logs_Telemetria.svg)

### AD05 Consultar Telemetría SOC
![AD05 Consultar Telemetría SOC](./FinalSVGs_v2/AD05_Consultar_Telemetria_SOC.svg)

### AD06 Crear IP Lista Negra
![AD06 Crear IP Lista Negra](./FinalSVGs_v2/AD06_Crear_IP_ListaNegra.svg)

### AD07 Consultar IP Lista Negra
![AD07 Consultar IP Lista Negra](./FinalSVGs_v2/AD07_Consultar_IP_ListaNegra.svg)

### AD08 Actualizar IP Lista Negra
![AD08 Actualizar IP Lista Negra](./FinalSVGs_v2/AD08_Actualizar_IP_ListaNegra.svg)

### AD09 Crear Usuario
![AD09 Crear Usuario](./FinalSVGs_v2/AD09_Crear_Usuario.svg)

### AD10 Consultar Usuario
![AD10 Consultar Usuario](./FinalSVGs_v2/AD10_Consultar_Usuario.svg)

### AD11 Actualizar Usuario
![AD11 Actualizar Usuario](./FinalSVGs_v2/AD11_Actualizar_Usuario.svg)

### AD12 Eliminar Usuario
![AD12 Eliminar Usuario](./FinalSVGs_v2/AD12_Eliminar_Usuario.svg)

### AD Generar Reporte Telegram
![AD Generar Reporte Telegram](./FinalSVGs_v2/AD_Generar_Reporte_Telegram.svg)

---

## 5. Diagrama de Clases

Diagrama estructural de clases de la arquitectura limpia de HoneyMetrics (Backend FastAPI, Modelos SQLAlchemy, Capa de Servicios y Core de Seguridad):

![Diagrama de Clases HoneyMetrics](./FinalSVGs_v2/Main_ClassDiagram.svg)

---

## 6. Diagrama de Modelo Entidad-Relación (MER)

Diagrama de entidad-relación correspondiente a la persistencia relacional en PostgreSQL / SQLAlchemy (Módulo RBAC, Gestión de Usuarios, Telemetría de Amenazas, Lista Negra, Bóveda Forense y Auditoría de Exportaciones):

![Modelo Entidad-Relación HoneyMetrics](./FinalSVGs_v2/MER_HoneyMetrics.svg)
