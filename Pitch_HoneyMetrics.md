# 🍯 HoneyMetrics: Plataforma Avanzada de Cyber Threat Intelligence (CTI)

## 1. El Origen: ¿De dónde nace la idea?
La idea de HoneyMetrics nació de una conversación muy reveladora. Mi hermano trabaja como consultor de ciberseguridad en **INDRA** y, charlando sobre su día a día, me compartió una problemática crítica en la industria: **el factor humano en el análisis de alertas**.

Él desplegó un *honeypot* (un servidor trampa) en nuestra red doméstica y comenzó a capturar datos en Wazuh. Sin embargo, la interfaz por defecto no ofrecía una lectura visual rápida y útil. Pero el problema real iba más allá del software: en las empresas, los analistas de seguridad Junior a menudo carecen de la experiencia necesaria para distinguir un ataque real de un "falso positivo". Peor aún, el exceso de alertas (fatiga de alertas) genera que, por pereza o agotamiento, los analistas ignoren reportes asumiendo que "no es nada grave". 

Ese sesgo humano es la puerta de entrada para los ataques más destructivos. Ahí vimos la oportunidad: **¿Y si creamos una plataforma que mastique esos datos, los grafique de forma intuitiva y filtre el ruido, ayudando a los analistas a no equivocarse?**

---

## 2. ¿Qué es HoneyMetrics?
**HoneyMetrics** es una plataforma de Inteligencia de Amenazas (CTI) diseñada para capturar, procesar y visualizar métricas de ciberataques en tiempo real. 

El concepto es simple pero poderoso:
- **Honey (La Trampa):** Usamos hardware de bajo costo (Orange Pi 5) para desplegar señuelos en la red. Los atacantes creen que están vulnerando un servidor real, pero en realidad están siendo estudiados.
- **Metrics (La Inteligencia):** Todo lo que hace el atacante se registra, se procesa y se envía a un Dashboard centralizado donde el ruido se convierte en gráficas claras, precisas y accionables.

---

## 3. El Problema que Resolvemos
1. **Fatiga de Alertas:** Los SIEMs tradicionales generan miles de logs incomprensibles.
2. **Falta de Experiencia (El error Junior):** Minimizar el margen de error humano de analistas que descartan falsos positivos o ignoran alertas reales por cansancio.
3. **Carencia de Visibilidad:** Dificultad para entender "quién nos ataca, cuándo y cómo".

---

## 4. Nuestra Arquitectura (El Motor del Proyecto)
Hemos diseñado HoneyMetrics bajo una arquitectura moderna, profesional y altamente escalable (API-First):

- **El Cerebro (Backend):** Desarrollado en **FastAPI** (Python). Es ultrarrápido, asíncrono y se encarga de procesar los datos masivos provenientes de la API de Wazuh (OpenSearch).
- **El Rostro (Frontend):** Construido con **React 18** y TailwindCSS. Un diseño "Dark Mode" (estilo *Glassmorphism*) enfocado en la experiencia de usuario (UX) para Centros de Operaciones de Seguridad (SOC). Todo el trabajo pesado de renderizar reportes PDF se hace del lado del cliente para no saturar el servidor.
- **El Ecosistema (Sensores):** Agentes Wazuh corriendo en placas Orange Pi 5, demostrando que se puede hacer ciberseguridad de alto nivel con eficiencia de recursos.

---

## 5. Enfoque Actual: Análisis de Datos (Entrega a 2 meses)
Para la entrega proyectada en dos meses, el proyecto tiene un enfoque estricto en el **Análisis y Visualización de Datos**. 

Sabemos que la Inteligencia Artificial es un campo complejo que requiere bases de datos sólidas y un entendimiento matemático profundo que aún estamos asimilando. Por lo tanto, en esta fase **no integraremos modelos predictivos de IA**, sino que nos enfocaremos en:
- **Dashboards Interactivos:** Gráficas de torta, líneas y barras generadas con *Plotly*.
- **Mapas de Calor (Heatmaps):** Visualización de las horas y días pico donde ocurren los ataques.
- **Top de Amenazas:** Ranking de las reglas de seguridad más violadas y las direcciones IP más hostiles.
- **Descarga de Evidencia:** Generación de reportes dinámicos para auditoría.

*En resumen: Estamos construyendo los cimientos perfectos (recolectando más de 165.000 eventos) para que, en un futuro, un modelo de Machine Learning tenga datos limpios y estructurados de dónde aprender.*

---

## 6. Articulación Institucional

Este proyecto no solo es un desafío técnico, sino que se alinea profundamente con la visión de la Universidad y las necesidades globales:

### Modelo MEDIT (Universidad de Cundinamarca)
HoneyMetrics se articula con la **Dimensión Translocal** del Modelo Educativo Digital Transmoderno (MEDIT). 
Actuamos como un "agente de transformación social que resuelve problemas desde lo local para la globalidad". La ciberseguridad es una amenaza mundial, pero estamos creando tecnología, talento y soluciones directamente desde nuestro territorio (Facatativá) para proteger infraestructuras digitales sin depender exclusivamente de licencias extranjeras costosas.

### Objetivos de Desarrollo Sostenible (ODS)
- **ODS 9 (Industria, Innovación e Infraestructura):** Aportamos innovación tecnológica para construir infraestructuras digitales resilientes, protegiendo los datos de las organizaciones frente a ciberataques.
- **ODS 16 (Paz, Justicia e Instituciones Sólidas):** Fomentamos la seguridad y la reducción del cibercrimen, dotando a las instituciones (públicas y privadas) de herramientas para defender su soberanía digital.

---
> *"HoneyMetrics no solo detecta el ataque; transforma el caos de los logs en inteligencia visual para que ningún analista vuelva a ignorar una amenaza crítica."*
