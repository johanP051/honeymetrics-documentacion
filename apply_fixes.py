with open("docs/scrum/sprint_1_auth.md", "r", encoding="utf-8") as f:
    content = f.read()

# Fix 1: PB-HM-02.1
old_tasks_02 = """**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React
- [ ] Configurar validación de entradas (Email/Password)
- [ ] Integrar consumo del endpoint de autenticación"""

new_tasks_02 = """**Tareas de Desarrollo:**
- [ ] Diseñar y maquetar formulario de interfaz en React con validación de entradas (Email/Password).
- [ ] Integrar consumo del endpoint de autenticación (`POST /api/v1/auth/login`) y almacenar JWT en `httpOnly cookie` o `localStorage` con manejo de error 401.
- [ ] [Fix ZTNA - Punto Ciego 1] Configurar Cloudflare Zero Trust Access para el dominio `api.johan-d3v.site`: crear una Application de tipo "Self-hosted", definir una Policy de acceso restringiendo a correos del equipo. Esto actúa como un firewall de identidad antes de FastAPI."""

if old_tasks_02 in content:
    content = content.replace(old_tasks_02, new_tasks_02, 1)

# Fix 2: PB-HM-03.1
hu_03_marker = "### 🧩 HU: PB-HM-03.1"
hu_04_marker = "### 🧩 HU: PB-HM-04.1"

if hu_03_marker in content and hu_04_marker in content:
    start = content.index(hu_03_marker)
    end = content.index(hu_04_marker)
    segment_03 = content[start:end]

    old_tasks_03 = """**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI necesario
- [ ] Establecer lógica de estado (React hooks) y validaciones
- [ ] Conectar la interfaz con la API Backend correspondiente"""

    new_tasks_03 = """**Tareas de Desarrollo:**
- [ ] Diseñar e implementar el componente UI de error de login (mensaje genérico anti-enumeración, sin revelar si falló email o password).
- [ ] Establecer lógica de estado (React hooks): contador de intentos fallidos en frontend, deshabilitar botón "Ingresar" por 30 segundos tras 5 fallos consecutivos.
- [ ] [Fix ZTNA - Punto Ciego 2] Implementar Rate Limiting en FastAPI con la librería `slowapi`: decorar el endpoint `POST /api/v1/auth/login` con `@limiter.limit("5/minute")` por IP. Configurar respuesta HTTP 429 con header `Retry-After`. Documentar la dependencia en `requirements.txt`."""

    if old_tasks_03 in segment_03:
        new_segment_03 = segment_03.replace(old_tasks_03, new_tasks_03, 1)
        content = content[:start] + new_segment_03 + content[end:]

# Fix 3: PB-HM-06.1
hu_06_marker = "### 🧩 HU: PB-HM-06.1"
hu_07_marker = "### 🧩 HU: PB-HM-07.1"

if hu_06_marker in content and hu_07_marker in content:
    start = content.index(hu_06_marker)
    end = content.index(hu_07_marker)
    segment_06 = content[start:end]

    anchor_line = "- [ ] Integrar SDK de correo en FastAPI y conectar UI (React) para solicitar y procesar el token de recuperación de contraseña."
    new_task_line = "- [ ] [Fix ZTNA - Punto Ciego 3] Documentar en el `README.md` del repositorio frontend que la variable `VITE_API_URL` queda expuesta en el bundle de producción (característica de Vite). Confirmar que las capas de Cloudflare Access (Fix 1) y Rate Limiting (Fix 2) son la defensa en profundidad para mitigar abuso."

    if anchor_line in segment_06 and "[Fix ZTNA - Punto Ciego 3]" not in segment_06:
        new_segment_06 = segment_06.replace(anchor_line, anchor_line + "\n" + new_task_line, 1)
        content = content[:start] + new_segment_06 + content[end:]

with open("docs/scrum/sprint_1_auth.md", "w", encoding="utf-8") as f:
    f.write(content)
