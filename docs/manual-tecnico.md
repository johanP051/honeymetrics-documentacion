# Manual Técnico y Arquitectura ("El Por Qué Técnico")

Este documento compila las justificaciones de ingeniería (Architectural Decision Records) detrás de HoneyMetrics v2.0.

> [!NOTE]
> Todo componente relacionado a Machine Learning (Clustering, HMM) está fuera del alcance de la Fase 1 (Sustentación Universitaria) y se abordará como "Trabajo Futuro" o "Fase Enterprise".

## 1. ¿Por qué Offloading de PDFs al Frontend?
Para generar reportes ejecutivos en PDF, HoneyMetrics delega el trabajo de renderizado a la librería `jsPDF` en el cliente (React) en lugar de generarlos en el backend con Python (ReportLab).
**El Por Qué Técnico:** Ahorro de memoria RAM. Generar PDFs binarios en el servidor de FastAPI saturaría la memoria del Nodo Central. Al pasarlo al cliente, distribuimos la carga de CPU a la máquina que está abriendo el navegador.

## 2. ¿Por qué usar RoleEnum en lugar de Strings para RBAC?
**El Por Qué Técnico:** Prevenir el fallo de "Magic Strings". Si se escribe `RoleChecker(["Analista de Datos"])` en lugar de `Analista de datos` (minúscula), el sistema deniega el acceso. Al utilizar una enumeración estricta de Python (`RoleEnum.ANALISTA`), los errores se detectan en tiempo de compilación y no se compromete la seguridad lógica del backend.

## 3. ¿Por qué forzar un Token Secreto de Webhook en Telegram?
**El Por Qué Técnico:** Prevención de Vulnerabilidades SSRF. Cualquiera en internet podría enviar un POST a `/api/v1/telegram-webhook` fingiendo ser Telegram y engañar al sistema para que apruebe falsamente un bloqueo. Forzando el envío del header `X-Telegram-Bot-Api-Secret-Token`, garantizamos criptográficamente el origen.
