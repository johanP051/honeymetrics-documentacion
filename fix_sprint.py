with open("docs/scrum/sprint_1_auth.md", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "PB-HM-06.1" in line:
        start_idx = i
        break

# find Tareas de Desarrollo:
for i in range(start_idx, len(lines)):
    if "**Tareas de Desarrollo:**" in lines[i]:
        tareas_idx = i
        break

lines[tareas_idx+1] = "- [ ] Configurar proveedor de correos transaccionales (Resend) y verificar dominio `johan-d3v.site` en Cloudflare (registros SPF, DKIM, DMARC).\n"
lines[tareas_idx+2] = "- [ ] Plan de Contingencia (Opción B): Si fallan los filtros universitarios, documentar e implementar envío de correos vía Microsoft Graph API usando un entorno M365 Developer.\n"
lines[tareas_idx+3] = "- [ ] Integrar SDK de correo en FastAPI y conectar UI (React) para solicitar y procesar el token de recuperación de contraseña.\n"

with open("docs/scrum/sprint_1_auth.md", "w") as f:
    f.writelines(lines)
