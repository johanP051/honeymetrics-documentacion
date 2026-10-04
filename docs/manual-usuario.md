# Manual de Usuario: Plataforma CTI

Este manual describe el uso interactivo de la interfaz de HoneyMetrics v2.0 (Desarrollada en React SPA Dark CTI).

## 1. El "Momento Show" (Uso del Sistema en Stand)

### ¿Cómo lanzar una alerta de prueba?
Si usted es un evaluador en el stand físico, busque nuestro código QR gigante impreso en el banner. 
1. Escanee el código desde su smartphone.
2. Será redirigido a una terminal de prueba ofensiva segura.
3. Seleccione "Ejecutar Escaneo Nmap" contra la IP trampa.

### Respuesta del Sistema
Como administrador, usted observará en la pantalla del Centro de Comando de HoneyMetrics:
- La IP del teléfono aparecerá inmediatamente en la tabla **Threat Center** con estado *En Observación*.
- **Aprobación de Telegram (HITL):** En el celular del administrador principal de T.I. llegará un mensaje con dos botones interactivos: `Bloquear en Firewall` o `Falso Positivo`.

## 2. Funciones del Analista de Datos
El rol de Analista tiene permisos orientados a la investigación forense:
- **Mapa de Calor:** Visualización de picos de ataque (usualmente altos entre las 11:00 y 12:00 UTC).
- **Descarga de Logs:** Permite extraer en formato JSONL los eventos masivos directos desde Wazuh para investigaciones que requieran la Cadena de Custodia.
