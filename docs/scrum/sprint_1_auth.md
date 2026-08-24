# 🚀 Sprint 1 — Historias de Usuario Premium

> **Foco:** Desarrollo de HUs originales de Sprint 1.

---
### 🧩 HU: PB-HM-01.1 — Visualizar la página de inicio pública

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-01 |
| **Actor** | Visitante / Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Visitante quiero visualizar la página de inicio pública para conocer el propósito de HoneyMetrics y acceder al sistema.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que ingreso a la raíz del sitio, Cuando carga la página, Entonces veo un navbar, sección hero, muestra de código y el mapa de calor ilustrativo.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que estoy en la Landing Page, Cuando hago clic en el punto de acceso, Entonces soy redirigido al formulario de Login.
```

---
### 🧩 HU: PB-HM-02.1 — Iniciar sesión con credenciales institucionales

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-02 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero iniciar sesión con credenciales institucionales para acceder al dashboard que me corresponde.

**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React con validación de entradas (Email/Password).
- [ ] Integrar consumo del endpoint de autenticación (`POST /api/v1/auth/login`) y almacenar JWT en `httpOnly cookie` o `localStorage` con manejo de error 401.
- [ ] [Fix ZTNA - Punto Ciego 1] Configurar Cloudflare Zero Trust Access para el dominio `api.johan-d3v.site`: crear una Application de tipo "Self-hosted", definir una Policy de acceso restringiendo a correos del equipo. Esto actúa como un firewall de identidad antes de FastAPI.

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que tengo credenciales válidas, Cuando ingreso mi correo @ucundinamarca.edu.co y contraseña, Entonces el sistema identifica mi rol y me redirige al dashboard.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que inicio sesión exitosamente, Cuando el sistema procesa mi petición, Entonces se me asigna un token JWT de sesión válido.
```

---
### 🧩 HU: PB-HM-03.1 — Que se bloquee el acceso por credenciales inválidas

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-03 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero que se bloquee el acceso por credenciales inválidas para mantener la seguridad de mi cuenta.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI de error de login (mensaje genérico anti-enumeración, sin revelar si falló email o password).
- [ ] Establecer lógica de estado (React hooks): contador de intentos fallidos en frontend, deshabilitar botón "Ingresar" por 30 segundos tras 5 fallos consecutivos.
- [ ] [Fix ZTNA - Punto Ciego 2] Implementar Rate Limiting en FastAPI con la librería `slowapi`: decorar el endpoint `POST /api/v1/auth/login` con `@limiter.limit("5/minute")` por IP. Configurar respuesta HTTP 429 con header `Retry-After`. Documentar la dependencia en `requirements.txt`.

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy en el formulario de Login, Cuando ingreso una contraseña incorrecta, Entonces el sistema rechaza el ingreso mostrando un mensaje genérico.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que el sistema rechaza el acceso, Cuando muestra el mensaje de error, Entonces no revela si el fallo fue en el correo o en la contraseña (anti-enumeración).
```

---
### 🧩 HU: PB-HM-04.1 — Forzar el cambio de contraseña en mi primer inicio de sesión

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-04 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero forzar el cambio de contraseña en mi primer inicio de sesión para asegurar que no quede con la clave temporal.

**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React
- [ ] Configurar validación de entradas (Email/Password)
- [ ] Integrar consumo del endpoint de autenticación

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que es mi primer inicio de sesión, Cuando ingreso con mi contraseña temporal, Entonces soy redirigido obligatoriamente a la vista de cambio de clave antes del dashboard.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que estoy en la vista forzada de cambio de clave, Cuando intento navegar a otra ruta, Entonces el sistema me bloquea hasta actualizar la contraseña.
```

---
### 🧩 HU: PB-HM-05.1 — Cambiar mi contraseña voluntariamente

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-05 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario autenticado quiero cambiar mi contraseña voluntariamente para mantener la seguridad de mi cuenta actualizada.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy en mi perfil, Cuando solicito cambiar mi contraseña ingresando una que cumple los criterios de seguridad (min. 8, no común, alfanumérica), Entonces la contraseña se actualiza exitosamente verificando la clave actual.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que ingreso una nueva contraseña, Cuando esta no cumple la longitud de 8 caracteres o no es alfanumérica, Entonces el sistema rechaza el cambio y me muestra un error.
```

---
### 🧩 HU: PB-HM-06.1 — Restablecer mi contraseña olvidada vía correo electrónico

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-06 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero restablecer mi contraseña olvidada vía correo electrónico para recuperar el acceso a mi cuenta.

**Tareas de Desarrollo:**
- [ ] Configurar proveedor de correos transaccionales (Resend) y verificar dominio `johan-d3v.site` en Cloudflare (registros SPF, DKIM, DMARC).
- [ ] Plan de Contingencia (Opción B): Si fallan los filtros universitarios, documentar e implementar envío de correos vía Microsoft Graph API usando un entorno M365 Developer.
- [ ] Integrar SDK de correo en FastAPI y conectar UI (React) para solicitar y procesar el token de recuperación de contraseña.
- [ ] [Fix ZTNA - Punto Ciego 3] Documentar en el `README.md` del repositorio frontend que la variable `VITE_API_URL` queda expuesta en el bundle de producción (característica de Vite). Confirmar que las capas de Cloudflare Access (Fix 1) y Rate Limiting (Fix 2) son la defensa en profundidad para mitigar abuso.

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que olvidé mi contraseña, Cuando solicito restablecerla, Entonces recibo un enlace de uso único en mi correo institucional.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que recibí el enlace, Cuando intento usarlo después de 1 hora, Entonces el sistema me indica que el token expiró y debo solicitar otro.
```

---
### 🧩 HU: PB-HM-07.1 — Autenticar con un segundo factor (2fa-otp) condicional

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-07 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero autenticar con un segundo factor (2FA-OTP) condicional para agregar una capa extra de seguridad.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que ya configuré el 2FA en el pasado, Cuando ingreso usuario y contraseña correctamente, Entonces el sistema solo me pide el input de 6 dígitos OTP de forma condicional.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que ingreso el código OTP correcto, Cuando el sistema lo valida con Google Authenticator, Entonces se completa el acceso al dashboard.
```

---
### 🧩 HU: PB-HM-08.1 — Vincular google authenticator en mi primer inicio

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-08 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero vincular Google Authenticator en mi primer inicio para habilitar el 2FA.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que no he configurado 2FA previamente (OTP condicional), Cuando ingreso mis credenciales válidas, Entonces el sistema muestra un código QR para que configure el autenticador.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que escaneo el código QR, Cuando ingreso el primer token OTP generado, Entonces el sistema verifica la sincronización y me concede el acceso.
```

---
### 🧩 HU: PB-HM-09.1 — Cerrar sesión de forma segura

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-09 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero cerrar sesión de forma segura para evitar accesos no autorizados a mi cuenta.

**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React
- [ ] Configurar validación de entradas (Email/Password)
- [ ] Integrar consumo del endpoint de autenticación

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy en el dashboard, Cuando hago clic en cerrar sesión, Entonces el sistema invalida el token JWT en el servidor y limpia el almacenamiento local.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que cerré mi sesión, Cuando intento usar el botón "Atrás" del navegador, Entonces el sistema me bloquea y me exige iniciar sesión nuevamente.
```

---
### 🧩 HU: PB-HM-10.1 — Que el sistema me redireccione al login al acceder a rutas protegidas sin sesión

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-10 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero que el sistema me redireccione al login al acceder a rutas protegidas sin sesión para mantener el control de acceso.

**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React
- [ ] Configurar validación de entradas (Email/Password)
- [ ] Integrar consumo del endpoint de autenticación

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que no tengo un token de sesión válido, Cuando intento acceder a una ruta protegida del dashboard, Entonces soy redirigido automáticamente al Login.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que mi sesión expiró, Cuando intento recargar una vista del dashboard, Entonces el sistema detecta la falta de sesión y me envía al Login.
```

---
### 🧩 HU: PB-HM-11.1 — Ver un banner informativo

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-11 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario sin rol asignado quiero ver un banner informativo para saber que debo solicitar permisos al Administrador.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que me autentico correctamente pero no tengo rol asignado, Cuando ingreso al sistema, Entonces veo una interfaz con acceso mínimo.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que tengo acceso mínimo, Cuando reviso la pantalla, Entonces veo un banner informativo indicando que debo solicitar permisos al Administrador.
```

---
### 🧩 HU: PB-HM-12.1 — Acceder al panel de administración profunda desde el frontend

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-12 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero acceder al panel de administración profunda desde el frontend para gestionar el sistema sin escribir URLs manualmente.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que tengo el rol de Administrador, Cuando hago clic en el botón "Gestión", Entonces accedo directamente al panel de administración.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que un usuario sin rol de Administrador intenta ver el botón "Gestión", Cuando carga el navbar, Entonces el botón no es visible.
```

---
### 🧩 HU: PB-HM-13.1 — Crear un nuevo rol/grupo de permisos

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-13 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero crear un nuevo Rol/Grupo de permisos para estructurar mejor el control de accesos.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy en el panel de Gestión, Cuando creo un nuevo rol con nombre único y le asigno permisos, Entonces se registra exitosamente en el sistema.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que intento crear un rol, Cuando uso un nombre que ya existe (ej. Consultor de Ciberseguridad repetido), Entonces el sistema muestra un error impidiendo la duplicidad.
```

---
### 🧩 HU: PB-HM-14.1 — Consultar la lista de roles/grupos existentes

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-14 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 1 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero consultar la lista de Roles/Grupos existentes para ver cómo están distribuidos los usuarios.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que accedo a la sección de Roles, Cuando carga la vista, Entonces veo todos los grupos registrados y la cantidad de usuarios asociados.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que la lista se muestra en pantalla, Cuando reviso los registros, Entonces puedo identificar claramente el nombre de cada grupo existente.
```

---
### 🧩 HU: PB-HM-15.1 — Modificar un rol/grupo de permisos existente

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-15 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero modificar un Rol/Grupo de permisos existente para ajustar sus capacidades en el sistema.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que selecciono un rol existente, Cuando edito su nombre o permisos asignados, Entonces los cambios se guardan correctamente.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que edité un rol, Cuando un usuario con ese rol realiza una acción, Entonces los nuevos permisos se aplican inmediatamente.
```

---
### 🧩 HU: PB-HM-16.1 — Eliminar un rol/grupo de permisos

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-16 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero eliminar un Rol/Grupo de permisos para limpiar el sistema de grupos obsoletos.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que intento borrar un grupo, Cuando solicito la eliminación, Entonces el sistema me avisa cuántos usuarios quedarán sin rol.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que veo la advertencia, Cuando confirmo explícitamente, Entonces el grupo se borra permanentemente del sistema.
```

---
### 🧩 HU: PB-HM-17.1 — Crear la cuenta de un nuevo usuario

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-17 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero crear la cuenta de un nuevo usuario para integrar nuevos miembros al equipo.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy en la gestión de usuarios, Cuando ingreso nombre, correo institucional, clave temporal y asigno un único rol (Directivo, Consultor o Analista), Entonces se registra el nuevo usuario.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que intento crear un usuario, Cuando intento asignar más de un rol simultáneamente, Entonces el sistema me bloquea.
```

---
### 🧩 HU: PB-HM-18.1 — Consultar la lista de usuarios registrados

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-18 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 2 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero consultar la lista de usuarios registrados para administrar las cuentas activas e inactivas.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que accedo a la sección de Usuarios, Cuando visualizo la tabla, Entonces veo columnas de nombre, correo, rol y estado.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que la tabla tiene registros, Cuando uso la barra de búsqueda o filtros, Entonces puedo encontrar un usuario específico rápidamente.
```

---
### 🧩 HU: PB-HM-19.1 — Modificar los datos de un usuario existente

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-19 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero modificar los datos de un usuario existente para mantener su perfil actualizado sin recrear su cuenta.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que selecciono un usuario, Cuando edito su nombre, correo o rol asignado, Entonces la información se actualiza correctamente.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que modifico el rol de un usuario, Cuando este intenta acceder, Entonces se le aplican sus nuevos permisos inmediatamente sin eliminar su cuenta.
```

---
### 🧩 HU: PB-HM-20.1 — Eliminar un usuario del sistema de forma segura

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-20 |
| **Actor** | Administrador |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Administrador quiero eliminar un usuario del sistema de forma segura para remover el acceso de miembros que ya no pertenecen al equipo.

**Tareas de Desarrollo:**
- [ ] Desarrollar formulario/modal para la acción
- [ ] Validar permisos del rol en el frontend
- [ ] Conectar endpoint CRUD y mostrar notificación de resultado

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que solicito borrar un usuario, Cuando inicio el proceso, Entonces el sistema muestra un aviso detallado de los datos en cascada que serán eliminados.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que reviso la advertencia, Cuando realizo la confirmación explícita, Entonces el usuario se elimina definitivamente y permanentemente.
```

---
### 🧩 HU: PB-HM-21.1 — Visualizar y editar mi perfil propio

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-21 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero visualizar y editar mi perfil propio para personalizar mi experiencia y gestionar mi información.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que accedo a mi perfil, Cuando visualizo mis datos, Entonces puedo ver mi rol y cambiar mi zona horaria.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que edito mis preferencias, Cuando subo una foto (JPG/PNG máx. 2MB) o cambio entre tema claro/oscuro, Entonces los cambios se guardan con éxito.
```

---
### 🧩 HU: PB-HM-22.1 — Consultar la lista negra de ips

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-22 |
| **Actor** | Todos |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero consultar la Lista Negra de IPs para identificar las amenazas registradas de manera interactiva.

**Tareas de Desarrollo:**
- [ ] Crear componente de tabla interactiva (paginación/filtros)
- [ ] Implementar petición GET para listar registros
- [ ] Validar renderizado condicional de acciones según rol

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que accedo a la Lista Negra, Cuando se carga la tabla mediante Fetch DataTables (paginación del servidor a 10 por página), Entonces veo las columnas de IP, tipo, país, ataque y reportador.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que visualizo los registros, Cuando reviso las IPs, Entonces veo insignias visuales de IP Pública/Privada, y si soy "Directivo de T.I.", veo candados visuales indicando solo lectura.
```

---
### 🧩 HU: PB-HM-23.1 — Agregar una ip a la lista negra

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-23 |
| **Actor** | Adm. / Consultor / Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario Operativo quiero agregar una IP a la Lista Negra para reportar nuevas amenazas en el sistema con un modal.

**Tareas de Desarrollo:**
- [ ] Crear componente de tabla interactiva (paginación/filtros)
- [ ] Implementar petición GET para listar registros
- [ ] Validar renderizado condicional de acciones según rol

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que uso el formulario modal, Cuando ingreso una IP, Entonces el sistema valida su formato (IPv4/IPv6) y calcula la insignia de IP Pública/Privada.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que completo el formulario correctamente, Cuando lo guardo, Entonces el sistema asigna automáticamente al usuario en sesión como creador del reporte.
```

---
### 🧩 HU: PB-HM-24.1 — Eliminar una ip de la lista negra

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-24 |
| **Actor** | Adm. / Consultor / Analista |
| **Puntos (Fibonacci)** | 3 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario Operativo quiero eliminar una IP de la Lista Negra para corregir falsos positivos o remover IPs limpias.

**Tareas de Desarrollo:**
- [ ] Crear componente de tabla interactiva (paginación/filtros)
- [ ] Implementar petición GET para listar registros
- [ ] Validar renderizado condicional de acciones según rol

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que estoy viendo la tabla de Lista Negra, Cuando selecciono la opción de remover en una fila, Entonces el sistema pide confirmación explícita para evitar borrados accidentales.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que confirmo la eliminación, Cuando se procesa, Entonces el registro desaparece permanentemente de la lista de amenazas.
```

---
### 🧩 HU: PB-HM-25.1 — Exportar la lista negra de ips

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-25 |
| **Actor** | Dir. T.I / Consultor / Analista |
| **Puntos (Fibonacci)** | 5 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Usuario quiero exportar la Lista Negra de IPs para analizar los datos en herramientas externas.

**Tareas de Desarrollo:**
- [ ] Crear componente de tabla interactiva (paginación/filtros)
- [ ] Implementar petición GET para listar registros
- [ ] Validar renderizado condicional de acciones según rol

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que la tabla contiene datos y tiene filtros activos, Cuando hago clic en exportar a CSV/Excel, Entonces el sistema descarga el archivo respetando dichos filtros.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que la tabla no contiene ningún dato, Cuando intento exportar, Entonces el botón de exportación se encuentra deshabilitado visualmente.
```

---
### 🧩 HU: PB-HM-61.1 — Visualizar un threat score dinámico

| Campo | Valor |
|---|---|
| **Código PB Padre** | PB-HM-61 |
| **Actor** | Analista |
| **Puntos (Fibonacci)** | 8 |
| **Estado** | Sin empezar |
| **Mockup de referencia** | `N/A` |

**Narrativa:**
> Como Analista quiero visualizar un Threat Score Dinámico para cada IP con el fin de evaluar su nivel de peligrosidad.

**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente

**Criterios de Aceptación (BDD):**

**Escenario 1:**:
```gherkin
- **Escenario 1:** Dado que observo una IP en el Threat Intelligence Center, Cuando el sistema procesa sus métricas, Entonces veo un Threat Score dinámico de 0 a 100 calculado por volumen, persistencia, tácticas y severidad.
```

**Escenario 2:**:
```gherkin
- **Escenario 2:** Dado que la IP recibe su puntaje dinámico, Cuando rebasa los umbrales configurados, Entonces se le asigna una categoría adecuada (Ej. APT, Botnet, Scanner) visible en pantalla.
```

---
