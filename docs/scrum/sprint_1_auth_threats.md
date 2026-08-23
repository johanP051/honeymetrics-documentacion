# 🔐 Sprint 1 — Autenticación Premium & Threat Intelligence Center

> **Período:** Semanas 2–3
> **Foco:** Login con experiencia 3D Globe + OTP, y CRUD completo del Threat Intelligence Center
> **Total Story Points del Sprint:** 38 SP

---
### 🧩 HU: PB-HM-02.1 — Login con Experiencia 3D Globe y JWT

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-02 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_login_3d.jpg` |

**Narrativa:**
> Como **Usuario** quiero **iniciar sesión ingresando mis credenciales sobre un fondo interactivo 3D** para **acceder de forma segura y visualmente premium a la plataforma CTI.**

**Tareas de Desarrollo:**
- [ ] Implementar componente de fondo Globe 3D con Three.js
- [ ] Construir formulario `.glass-card` con inputs de email y contraseña
- [ ] Integrar validación con AuthContext

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el usuario se encuentra en la pantalla de Login 3D
Cuando el usuario ingresa credenciales válidas y presiona "Ingresar"
Entonces el sistema valida la identidad, almacena el token de sesión y redirige al dashboard correspondiente según su rol.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el usuario intenta ingresar al sistema
Cuando el usuario proporciona una contraseña incorrecta
Entonces el sistema muestra un mensaje de error genérico "Credenciales inválidas" sin revelar si el fallo fue en el email o la contraseña.
```

---
### 🧩 HU: PB-HM-07.1 — Verificar Código OTP (Segundo Factor)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-07 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_login_otp.jpg` |

**Narrativa:**
> Como **Usuario** quiero **verificar mi código OTP como segundo paso de autenticación** para **garantizar la seguridad de mi cuenta ante posibles filtraciones de contraseñas.**

**Tareas de Desarrollo:**
- [ ] Crear vista OTP con input de 6 dígitos
- [ ] Implementar lógica de reintento de validación OTP
- [ ] Manejar expiración de token temporal (refresh)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el usuario superó correctamente el primer paso de login (contraseña)
Cuando el usuario introduce un código OTP de 6 dígitos válido antes de que expire
Entonces el sistema le otorga acceso completo a la plataforma.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el usuario está en el paso de validación OTP
Cuando introduce un código expirado o incorrecto
Entonces el sistema muestra un mensaje de error claro, limpia el campo de texto y actualiza el contador de intentos restantes (máximo 3).
```

---
### 🧩 HU: PB-HM-08.1 — Vincular Google Authenticator en Primer Login

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-08 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_qr_setup.jpg` |

**Narrativa:**
> Como **Usuario nuevo** quiero **poder vincular mi cuenta con Google Authenticator mediante un código QR** para **habilitar el doble factor de autenticación requerido.**

**Tareas de Desarrollo:**
- [ ] Renderizar código QR desde el secret proporcionado por el backend
- [ ] Vista de configuración obligatoria en el primer inicio de sesión

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que es el primer inicio de sesión del usuario en la plataforma
Cuando el usuario escanea el código QR proporcionado e ingresa el primer token generado
Entonces el sistema vincula exitosamente el dispositivo y activa el requerimiento 2FA de forma permanente.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el usuario intenta vincular su dispositivo autenticador
Cuando el usuario ingresa un token que no corresponde al código QR escaneado
Entonces el sistema rechaza la vinculación y solicita que reinicie el proceso de configuración del QR.
```

---
### 🧩 HU: PB-HM-71.1 — [LISTAR] Ver Tabla del Threat Intelligence Center

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-71 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_threat_list.jpg` |

**Narrativa:**
> Como **Analista** quiero **visualizar una tabla con todas las amenazas registradas incluyendo su Threat Score** para **evaluar rápidamente el estado de riesgo general.**

**Tareas de Desarrollo:**
- [ ] Crear tabla de datos con paginación
- [ ] Implementar calculador/renderer visual de Threat Score (barra 0-100)
- [ ] Mostrar badges categorizados (APT, Botnet, Scanner)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista accede a la vista de Threat Intelligence Center
Cuando los datos se cargan correctamente desde el servidor
Entonces visualiza una tabla con IPs atacantes, un Score visual (0-100) y badges categóricos como APT o Scanner.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista accede al Threat Intelligence Center
Cuando el sistema determina que no hay registros almacenados actualmente
Entonces muestra un mensaje vacío amigable indicando que no hay amenazas activas.
```

---
### 🧩 HU: PB-HM-72.1 — [CREAR] Registrar Nueva Amenaza Manualmente

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-72 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_threat_create.jpg` |

**Narrativa:**
> Como **Analista** quiero **poder registrar una nueva amenaza manualmente a través de un formulario** para **mantener actualizada la base de datos de inteligencia con hallazgos externos.**

**Tareas de Desarrollo:**
- [ ] Crear modal de registro con validación de IP (Regex)
- [ ] Campos para descripción, severidad manual y tipo de actor

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista abre el modal de registro de amenazas
Cuando ingresa una IP válida, completa los campos requeridos y guarda el formulario
Entonces el sistema registra la amenaza, calcula su score automático inicial y actualiza la tabla de datos.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista intenta registrar una nueva amenaza
Cuando introduce un formato de IP inválido en el campo correspondiente
Entonces el formulario muestra un error de validación inline (rojo) sin cerrar el modal ni enviar la petición HTTP.
```

---
### 🧩 HU: PB-HM-73.1 — [EDITAR] Actualizar Clasificación de Amenaza

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-73 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_threat_edit.jpg` |

**Narrativa:**
> Como **Analista** quiero **actualizar la clasificación y notas asociadas a una amenaza** para **enriquecer el contexto de inteligencia conforme evoluciona un ataque.**

**Tareas de Desarrollo:**
- [ ] Modal de edición con datos precargados
- [ ] Lógica para solo enviar campos modificados (PATCH)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista edita los detalles de una amenaza existente
Cuando guarda satisfactoriamente los cambios realizados en el formulario
Entonces la tabla principal se actualiza reflejando la nueva clasificación sin requerir que la página se recargue por completo.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista abre el modal de edición de una amenaza
Cuando hace clic en "Guardar" sin haber modificado ningún campo
Entonces el sistema cierra el modal sin generar ninguna petición de red innecesaria hacia el servidor.
```

---
### 🧩 HU: PB-HM-74.1 — [ELIMINAR] Retirar Amenaza con Confirmación

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-74 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_threat_delete.jpg` |

**Narrativa:**
> Como **Analista** quiero **eliminar una amenaza registrada del centro de inteligencia mediante una acción confirmada** para **corregir falsos positivos o descartar IPs ya mitigadas.**

**Tareas de Desarrollo:**
- [ ] Crear componente modal de alerta (rojo) para confirmación destructiva
- [ ] Actualización optimista de UI tras confirmación

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el analista selecciona la acción de eliminar sobre una amenaza
Cuando confirma la acción destructiva en el diálogo de advertencia
Entonces la IP es eliminada permanentemente del sistema y la tabla se actualiza removiendo la fila.
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el analista ve el diálogo de advertencia para eliminar una amenaza
Cuando decide hacer clic en "Cancelar" o pulsa la tecla ESC
Entonces el diálogo se cierra y ningún cambio ocurre en los datos del sistema.
```

---
### 🧩 HU: PB-HM-62.1 — Detectar Botnet Coordinada (CIDR /24)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-62 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_botnet_alert.jpg` |

**Narrativa:**
> Como **Analista** quiero **que el sistema agrupe IPs atacantes por su subred /24** para **detectar y mitigar rápidamente redes de botnets coordinadas.**

**Tareas de Desarrollo:**
- [ ] Algoritmo de agrupación de subredes en la vista
- [ ] Renderizado condicional del botón de "Bloqueo por CIDR"

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que el sistema evalúa la actividad reciente de amenazas
Cuando detecta 3 o más IPs activas pertenecientes a la misma subred /24
Entonces muestra una alerta de "Posible Botnet Coordinada" y habilita un botón para "Bloquear CIDR completo".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que el sistema analiza las IPs entrantes
Cuando solo detecta 2 IPs activas dentro de la misma subred
Entonces no activa la alerta de botnet, ya que no se ha alcanzado el umbral mínimo de coordinación.
```

---
### 🧩 HU: PB-HM-63.1 — Clasificador Bot vs Humano (Velocidad)

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-63 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `mockups/mockup_bot_classifier.jpg` |

**Narrativa:**
> Como **Analista** quiero **ver si una IP es clasificada como Bot o Humano según su velocidad de ataque** para **priorizar la contención de intrusiones dirigidas manuales.**

**Tareas de Desarrollo:**
- [ ] Lógica visual de etiquetado (Bot vs Humano)
- [ ] Ordenamiento en tabla basado en etiqueta Humano (mayor riesgo de APT)

**Criterios de Aceptación (BDD):**

**Escenario 1 — Happy Path:**
```gherkin
Dado que una IP atacante tiene un registro de actividad excesiva
Cuando supera una tasa de 100 eventos por hora (ej. 6.315 eventos/hora)
Entonces la interfaz le asigna y renderiza una etiqueta visual de "🤖 Bot".
```

**Escenario 2 — Error / Edge Case:**
```gherkin
Dado que una IP realiza intentos de ataque pausados y calculados
Cuando el sistema registra una tasa baja (ej. 8 eventos por hora) sobre servicios específicos
Entonces etiqueta visualmente a la IP como "🧑 Humano" y eleva su prioridad visual en el dashboard de alertas tempranas.
```
