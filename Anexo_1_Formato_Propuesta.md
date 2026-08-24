# Anexo 1. Formato de Propuesta

> **CICLO:** Profesional / Formación Disciplinar (VI Semestre)

# DATOS GENERALES

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="2"><strong>PROGRAMA</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td colspan="2">Ingeniería de Sistemas y Computación</td>
</tr>
<tr class="even">
<td colspan="2"><strong>SEDE</strong></td>
</tr>
<tr class="odd">
<td colspan="2">Universidad de Cundinamarca - Extensión Facatativá</td>
</tr>
<tr class="even">
<td colspan="2"><strong>TIPO DE PROYECTO</strong></td>
</tr>
<tr class="odd">
<td colspan="2">Proyecto de Desarrollo Tecnológico e Innovación (Plataforma CTI y Ciberseguridad)</td>
</tr>
<tr class="even">
<td colspan="2"><strong>CICLO</strong></td>
</tr>
<tr class="odd">
<td colspan="2">Profesional / VI Semestre — Ingeniería de Software II</td>
</tr>
<tr class="even">
<td colspan="2"><p><strong>INTEGRANTES DEL PROYECTO</strong> (Nombres y apellidos de los constructores del conocimiento que conforman el Proyecto de Gestión del Conocimiento, agregue o elimine filas según corresponda)</p></td>
</tr>
<tr class="odd">
<td><p><strong>NOMBRES Y APELLIDOS</strong></p></td>
<td><p><strong>CORREO ELECTRÓNICO INSTITUCIONAL</strong></p></td>
</tr>
<tr class="even">
<td>Johan Sebastián Posada Beltrán</td>
<td>jposadabeltran@ucundinamarca.edu.co</td>
</tr>
<tr class="odd">
<td>Juan Pablo Fonseca Celis</td>
<td>jpfonsecac@ucundinamarca.edu.co</td>
</tr>
<tr class="even">
<td>Manuel Alejandro Aldana Rincón</td>
<td>maaldanar@ucundinamarca.edu.co</td>
</tr>
</tbody>
</table>

> **ESTRUCTURA DEL PROYECTO**

| **TÍTULO DEL PROYECTO:** |
| :--- |
| Sistema de inteligencia de amenazas cibernéticas (CTI) basado en ecosistemas honeypot y analítica de datos para el monitoreo de ataques en entornos de red controlados (Honeylabs) en la Sabana de Occidente. |
| **PLANTEAMIENTO DEL PROBLEMA Y JUSTIFICACIÓN:** |
| **Planteamiento del Problema:**<br>En la industria de la ciberseguridad actual, los Centros de Operaciones de Seguridad (SOC) enfrentan un volumen masivo y automatizado de ciberataques. Sin embargo, el principal problema no radica únicamente en la detección técnica, sino en el factor humano frente al exceso de alertas (fatiga de alertas). En la práctica profesional, los analistas de seguridad —especialmente aquellos con perfil Junior— se ven abrumados por los registros de los SIEM tradicionales, lo que genera dificultades para distinguir incidentes críticos de "falsos positivos". Esto provoca que verdaderas amenazas sean ignoradas o subestimadas, comprometiendo la infraestructura tecnológica de las organizaciones.<br><br>**Justificación:**<br>El presente proyecto se justifica al abordar directamente esta falencia operativa mediante el despliegue de HoneyMetrics, un sistema que utiliza un *Honeypot* (servidor trampa desplegado en un entorno controlado) para atraer atacantes reales, capturando su comportamiento mediante el motor Wazuh. A través de analítica de datos y representación visual interactiva, la plataforma procesa los registros crudos y los transforma en inteligencia accionable, filtrando el ruido y minimizando el margen de error del analista.<br><br>Institucionalmente, este proyecto se articula con el **Modelo Educativo Digital Transmoderno (MEDIT)** de la Universidad de Cundinamarca, impactando desde su dimensión Translocal: resolver un problema de alcance global (cibercrimen) generando tecnología y conocimiento desde el entorno local. Asimismo, el proyecto contribuye de forma directa a la Agenda 2030 de la ONU, impactando en el **ODS 4** (Educación de Calidad) al dotar a los estudiantes de un entorno de aprendizaje empírico sobre amenazas reales; el **ODS 9** (Industria, Innovación e Infraestructura) aportando innovación para infraestructuras digitales resilientes; y el **ODS 16** (Paz, Justicia e Instituciones Sólidas) al crear herramientas que mitigan el cibercrimen y protegen la soberanía de los datos. |
| **OBJETIVOS DEL PROYECTO** |
| **OBJETIVO GENERAL:**<br>Diseñar un sistema de inteligencia de amenazas cibernéticas (CTI) basado en ecosistemas honeypot y analítica de datos para el monitoreo de ataques en entornos de red controlados (Honeylabs) en la Sabana de Occidente. |
| **OBJETIVOS ESPECÍFICOS:**<br>1. **Analizar** los requerimientos funcionales y no funcionales del sistema mediante la identificación de tácticas de ciberataques comunes capturadas por el honeypot, para establecer el alcance y las métricas de la plataforma de inteligencia.<br>2. **Diseñar** la arquitectura de software (Backend y Frontend) y la interfaz de usuario mediante el uso de esquemas de modelado, garantizando un entorno visual ergonómico que minimice la fatiga de alertas para el usuario.<br>3. **Desarrollar** el sistema de información y los módulos de analítica de datos integrando el ecosistema de recolección de los agentes de seguridad (Wazuh), conforme a los parámetros arquitectónicos establecidos.<br>4. **Comprobar** y validar la fiabilidad de la plataforma mediante la ejecución de pruebas de integración y evaluación de la representación gráfica frente a eventos de ataque reales.<br>5. **Desplegar** el sistema en un entorno de servidor local asegurado para la visualización y auditoría continua de las amenazas recolectadas en el laboratorio (Honeylab). |
| **MARCO REFERENCIAL (Opcional):** |
| El proyecto se sustenta teóricamente en tres pilares:<br>1. **Honeypots y Cyber Threat Intelligence (CTI):** Redes trampa diseñadas para ser vulneradas con el fin de recolectar información sobre tácticas, técnicas y procedimientos (TTPs) de los ciberdelincuentes.<br>2. **Analítica de Datos Visual:** Empleo de metodologías para transformar *Big Data* de logs de seguridad en mapas de calor y gráficas interactivas, mitigando el error humano en el análisis de alertas.<br>3. **Modelos Arquitectónicos Desacoplados:** Uso de arquitecturas API-First que separan el procesamiento pesado del servidor (Backend asíncrono) del renderizado del cliente (SPA - Single Page Application). |
| **METODOLOGÍA A UTILIZAR Y CRONOGRAMA DE DESARROLLO:** |
| El proyecto se desarrollará bajo la **Metodología Ágil Scrum**, alineando sus fases con el Ciclo de Vida del Software (SDLC). El cronograma se distribuye en Sprints:<br>• **Sprint 1:** Análisis de requerimientos y diseño de la arquitectura. Implementación del Core de Autenticación y modelos de bases de datos.<br>• **Sprint 2:** Desarrollo de los módulos del *Threat Intelligence Center*, construcción del motor de filtros y desarrollo de las interfaces gráficas iniciales.<br>• **Sprint 3:** Integración de la analítica de datos (gráficas de dispersión, mapas de calor predictivo) y extracción de logs. Comprobación de integridad y despliegue del entorno funcional. |
| **REFERENCIAS BIBLIOGRÁFICAS (opcional):** |
| • Center for Internet Security (CIS). (2026). *CIS Benchmarks: Secure Configuration Guidelines*.<br>• MITRE Corporation. (2026). *MITRE ATT&CK: Design and Philosophy*.<br>• Wazuh, Inc. (2026). *Wazuh - The Open Source Security Platform Documentation*.<br>• Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson. |

<br>

| **PRODUCTOS ESPERADOS (marque con una X):** | |
| :--- | :---: |
| Documento síntesis de PGC | **X** |
| Software | **X** |
| Sistema de información | **X** |
| Prototipo | **X** |
| Artículo científico | |
| Póster- Ponencia | |
| Comunidad de práctica y redes de conocimiento | |
| Evento científico o académico | |
| Ediciones de revista o libro de divulgación | |
| Producción de contenidos digitales | |
| Publicaciones editoriales no especializadas | |
| Desarrollo Web | **X** |
| Creación de cursos | |
| Emprendimiento e innovación | |
| Otro ¿Cuál? | |
