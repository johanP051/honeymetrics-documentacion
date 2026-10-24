#!/usr/bin/env python3
"""
scripts/capture_docs_media.py
Protocolo 'Director de Cine' con Playwright para HoneyMetrics v2.0.
Genera 10 capturas de alta resolución (.png) y 5 videos independientes en 1080p Full HD (.mp4)
utilizando cadencia pedagógica humana, cursor dorado inyectado (#hm-cursor) y transcodificación con ffmpeg.
"""

import os
import sys
import time
import uuid
import base64
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
import jwt
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("HM_FRONTEND_URL", "http://localhost:5173")
SCREENSHOTS_DIR = "/media/sebas/Exdrive/Workspace/honeymetrics-backend/docs/assets/screenshots"
VIDEOS_DIR = "/media/sebas/Exdrive/Workspace/honeymetrics-backend/docs/assets/videos"
TEMP_VIDEOS_DIR = "/tmp/hm_playwright_videos"
SECRET_KEY = os.environ.get("SECRET_KEY", "dev_supersecretkey_honeymetrics_local_2026_udec")
ALGORITHM = "HS256"

# Inyección del cursor visual de alta fidelidad (#hm-cursor)
INJECT_CURSOR_SCRIPT = """
(() => {
  if (document.getElementById('hm-cursor')) return;
  const cursor = document.createElement('div');
  cursor.id = 'hm-cursor';
  cursor.style.position = 'fixed';
  cursor.style.width = '24px';
  cursor.style.height = '24px';
  cursor.style.borderRadius = '50%';
  cursor.style.backgroundColor = 'rgba(212, 175, 55, 0.85)';
  cursor.style.border = '3px solid #ffffff';
  cursor.style.boxShadow = '0 0 14px rgba(212, 175, 55, 0.95)';
  cursor.style.pointerEvents = 'none';
  cursor.style.zIndex = '2147483647';
  cursor.style.transition = 'transform 0.08s ease-out';
  cursor.style.transform = 'translate(-50%, -50%)';
  cursor.style.top = '540px';
  cursor.style.left = '960px';
  cursor.style.display = 'block';
  document.documentElement.appendChild(cursor);

  window.addEventListener('mousemove', (e) => {
    cursor.style.display = 'block';
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  }, true);

  window.addEventListener('mousedown', (e) => {
    cursor.style.transform = 'translate(-50%, -50%) scale(0.7)';
    cursor.style.backgroundColor = 'rgba(255, 215, 0, 1)';
    const ripple = document.createElement('div');
    ripple.id = 'hm-click-ripple';
    ripple.style.position = 'fixed';
    ripple.style.left = e.clientX + 'px';
    ripple.style.top = e.clientY + 'px';
    ripple.style.width = '20px';
    ripple.style.height = '20px';
    ripple.style.borderRadius = '50%';
    ripple.style.border = '3px solid #D4AF37';
    ripple.style.pointerEvents = 'none';
    ripple.style.zIndex = '2147483646';
    ripple.style.transform = 'translate(-50%, -50%) scale(1)';
    ripple.style.opacity = '1';
    ripple.style.transition = 'all 0.25s ease-out';
    document.documentElement.appendChild(ripple);
    requestAnimationFrame(() => {
      ripple.style.transform = 'translate(-50%, -50%) scale(3.0)';
      ripple.style.opacity = '0';
    });
    setTimeout(() => ripple.remove(), 280);
  }, true);

  window.addEventListener('mouseup', () => {
    cursor.style.transform = 'translate(-50%, -50%) scale(1)';
    cursor.style.backgroundColor = 'rgba(212, 175, 55, 0.85)';
  }, true);
})();
"""

def generate_jwt(email: str, role: str, role_id: int, scopes: list[str]) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email,
        "role": role,
        "role_id": role_id,
        "auth_version": 0,
        "scopes": scopes,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=24)).timestamp()),
        "jti": str(uuid.uuid4()).replace("-", "")
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def seed_session(page, email: str, role: str, role_id: int, scopes: list[str]):
    token = generate_jwt(email, role, role_id, scopes)
    user_obj = {
        "id": role_id,
        "email": email,
        "role_name": role,
        "role": role,
        "scopes": scopes,
        "is_active": True,
        "is_mfa_enabled": False
    }
    page.goto(f"{BASE_URL}/login")
    page.evaluate("""([tok, usr, rle, scps]) => {
        localStorage.setItem('hm_access_token', tok);
        localStorage.setItem('hm_user', usr);
        localStorage.setItem('hm_role', rle);
        localStorage.setItem('hm_scopes', scps);
        sessionStorage.setItem('hm_access_token', tok);
        sessionStorage.setItem('hm_user', usr);
        sessionStorage.setItem('hm_role', rle);
        sessionStorage.setItem('hm_scopes', scps);
    }""", [token, json_dumps(user_obj), role, json_dumps(scopes)])

def json_dumps(obj):
    import json
    return json.dumps(obj)

def ensure_cursor(page):
    try:
        page.evaluate(INJECT_CURSOR_SCRIPT)
    except Exception:
        pass

def smooth_hover(page, locator, steps=28):
    try:
        ensure_cursor(page)
        box = locator.bounding_box()
        if box:
            cx = box["x"] + box["width"] / 2
            cy = box["y"] + box["height"] / 2
            page.mouse.move(cx, cy, steps=steps)
            page.evaluate("([x, y]) => { const c = document.getElementById('hm-cursor'); if (c) { c.style.left = x + 'px'; c.style.top = y + 'px'; } }", [cx, cy])
            page.wait_for_timeout(250)
            return cx, cy
    except Exception:
        pass
    return None

def human_click(page, locator, steps=28):
    try:
        ensure_cursor(page)
        box = locator.bounding_box()
        if box:
            cx = box["x"] + box["width"] / 2
            cy = box["y"] + box["height"] / 2
            page.mouse.move(cx, cy, steps=steps)
            page.evaluate("([x, y]) => { const c = document.getElementById('hm-cursor'); if (c) { c.style.left = x + 'px'; c.style.top = y + 'px'; } }", [cx, cy])
            page.wait_for_timeout(180)
            page.mouse.down()
            page.wait_for_timeout(90)
            page.mouse.up()
            page.wait_for_timeout(350)
            return
    except Exception:
        pass
    locator.click()

def transcode_video(webm_path: str, mp4_path: str):
    print(f"Transcodificando con ffmpeg a 1080p nativo: {webm_path} -> {mp4_path}")
    cmd = [
        "ffmpeg", "-y",
        "-i", webm_path,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        mp4_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(mp4_path):
        size_kb = os.path.getsize(mp4_path) / 1024
        print(f"Video final 1080p listo: {mp4_path} ({size_kb:.1f} KB)")

def record_video_flow(p, filename: str, duration_desc: str, flow_func):
    print(f"\n--- GRABANDO VIDEO FULL HD 1080p: {filename} ({duration_desc}) ---")
    os.makedirs(TEMP_VIDEOS_DIR, exist_ok=True)
    temp_dir = os.path.join(TEMP_VIDEOS_DIR, f"rec_{uuid.uuid4().hex[:8]}")
    os.makedirs(temp_dir, exist_ok=True)

    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=temp_dir,
        record_video_size={"width": 1920, "height": 1080},
        device_scale_factor=1
    )
    context.add_init_script(INJECT_CURSOR_SCRIPT)
    page = context.new_page()

    try:
        flow_func(page)
    finally:
        page.wait_for_timeout(1000)
        page.close()
        context.close()
        browser.close()

    # Localizar archivo webm generado
    webm_files = [f for f in os.listdir(temp_dir) if f.endswith(".webm")]
    if not webm_files:
        print(f"Error: No se generó webm en {temp_dir}")
        return
    raw_webm = os.path.join(temp_dir, webm_files[0])
    target_mp4 = os.path.join(VIDEOS_DIR, filename)
    transcode_video(raw_webm, target_mp4)
    shutil.rmtree(temp_dir, ignore_errors=True)

# -----------------------------------------------------------------------------
# FLUJO 1: 01_login_y_navegacion.mp4
# -----------------------------------------------------------------------------
def flow_01_login_y_navegacion(page):
    # 1. Landing Page
    page.goto(f"{BASE_URL}/")
    ensure_cursor(page)
    page.wait_for_timeout(1400)

    # 2. Clic en "Ingresar a Plataforma"
    enter_btn = page.locator("button:has-text('Ingresar a Plataforma')").first
    smooth_hover(page, enter_btn, steps=25)
    human_click(page, enter_btn)
    page.wait_for_timeout(1600)
    ensure_cursor(page)

    # 3. Formulario de Login: Tipeo de credenciales
    email_in = page.locator("#login-email")
    smooth_hover(page, email_in, steps=20)
    email_in.click()
    email_in.press_sequentially("analista.soc@ucundinamarca.edu.co", delay=55)
    page.wait_for_timeout(400)

    pass_in = page.locator("#login-password")
    smooth_hover(page, pass_in, steps=20)
    pass_in.click()
    pass_in.press_sequentially("Admin123!", delay=55)
    page.wait_for_timeout(500)

    # 4. Alternar icono del ojo para revelar contraseña
    eye_btn = page.locator("button[aria-label*='contraseña']").first
    if eye_btn.count() > 0:
        smooth_hover(page, eye_btn, steps=18)
        human_click(page, eye_btn)
        page.wait_for_timeout(900)
        # Ocultar de nuevo
        human_click(page, eye_btn)
        page.wait_for_timeout(600)

    # 5. Clic en "Ingresar"
    login_btn = page.locator("button[type='submit']")
    smooth_hover(page, login_btn, steps=22)
    human_click(page, login_btn)
    page.wait_for_timeout(2600)
    ensure_cursor(page)

    # 6. Recorrido lateral
    for nav_text in ["Threat Center", "Logs & Reportes", "Dashboard"]:
        nav_item = page.locator(f"aside nav[aria-label='Navegación Principal'] a:has-text('{nav_text}')").first
        if nav_item.count() > 0:
            smooth_hover(page, nav_item, steps=20)
            human_click(page, nav_item)
            page.wait_for_timeout(1600)
            ensure_cursor(page)

# -----------------------------------------------------------------------------
# FLUJO 2: 02_dashboard_cti_filtros.mp4
# -----------------------------------------------------------------------------
def flow_02_dashboard_cti_filtros(page):
    seed_session(page, "admin@ucundinamarca.edu.co", "Administrador", 1, [
        "admin:all", "dashboard:read", "threats:read", "logs:read"
    ])
    page.goto(f"{BASE_URL}/dashboard")
    ensure_cursor(page)
    page.wait_for_timeout(2400)

    # 1. Filtros temporales
    for range_label in ["Últimas 24h", "Últimos 7 días", "Últimos 30 días"]:
        btn = page.locator(f"button:has-text('{range_label}')").first
        if btn.count() > 0:
            smooth_hover(page, btn, steps=20)
            human_click(page, btn)
            page.wait_for_timeout(1400)

    # 2. Hover en gráficos de Plotly
    plotly_charts = page.locator(".js-plotly-plot")
    if plotly_charts.count() > 0:
        smooth_hover(page, plotly_charts.first, steps=25)
        page.wait_for_timeout(1100)
        if plotly_charts.count() > 1:
            smooth_hover(page, plotly_charts.nth(1), steps=25)
            page.wait_for_timeout(1100)

    # 3. Scroll suave hacia abajo (Heatmap y Honeypot Advisor)
    page.evaluate("window.scrollBy({ top: 480, behavior: 'smooth' })")
    page.wait_for_timeout(1400)
    ensure_cursor(page)

    # 4. Exploración de celdas o elementos de abajo
    advisor = page.locator("text=Honeypot Advisor").first
    if advisor.count() > 0:
        smooth_hover(page, advisor, steps=22)
        page.wait_for_timeout(1000)

    page.wait_for_timeout(1500)

# -----------------------------------------------------------------------------
# FLUJO 3: 03_threat_center_y_boveda.mp4
# -----------------------------------------------------------------------------
def flow_03_threat_center_y_boveda(page):
    # Diálogo de confirmación para borrado
    page.on("dialog", lambda dialog: dialog.accept())

    seed_session(page, "admin@ucundinamarca.edu.co", "Administrador", 1, [
        "admin:all", "threats:read", "threats:write", "threats:delete"
    ])
    page.goto(f"{BASE_URL}/threat-center")
    ensure_cursor(page)
    page.wait_for_timeout(2000)

    # 1. Abrir Modal Añadir Amenaza
    add_btn = page.locator("button:has-text('Añadir Amenaza')")
    smooth_hover(page, add_btn, steps=22)
    human_click(page, add_btn)
    page.wait_for_timeout(1200)

    # PASO A: Rechazo de IP privada (127.0.0.1)
    ip_in = page.locator("#threat-ip")
    smooth_hover(page, ip_in, steps=18)
    ip_in.click()
    ip_in.press_sequentially("127.0.0.1", delay=45)
    page.wait_for_timeout(300)

    country_in = page.locator("#threat-country")
    country_in.fill("Local")

    # Score slider
    score_slider = page.locator("#threat-score")
    score_slider.fill("80")

    # Guardar para detonar 422
    save_btn = page.locator("div[role='dialog'] button:has-text('Guardar')")
    smooth_hover(page, save_btn, steps=20)
    human_click(page, save_btn)
    # Espera pedagógica de 1.8s mostrando la alerta roja
    page.wait_for_timeout(1800)

    # PASO B: Corregir datos con IP pública válida
    ip_in.click()
    ip_in.fill("")
    ip_in.press_sequentially("45.148.10.215", delay=45)

    country_in.click()
    country_in.fill("")
    country_in.press_sequentially("Alemania", delay=45)

    cat_select = page.locator("#threat-category")
    cat_select.select_option("Botnet")

    score_slider.fill("92")

    notes_in = page.locator("#threat-notes")
    if notes_in.count() > 0:
        notes_in.click()
        notes_in.press_sequentially("Ráfaga SSH detectada en sensor Cowrie", delay=35)

    page.wait_for_timeout(500)
    smooth_hover(page, save_btn, steps=20)
    human_click(page, save_btn)
    page.wait_for_timeout(2200)
    ensure_cursor(page)

    # Hover sobre la fila recién creada
    new_row = page.locator("tr:has-text('45.148.10.215')").first
    if new_row.count() > 0:
        smooth_hover(page, new_row, steps=24)
        page.wait_for_timeout(1500)

        # PASO C: Eliminar y pasar a Bóveda Forense
        trash_btn = new_row.locator("button[aria-label*='Eliminar']").first
        smooth_hover(page, trash_btn, steps=18)
        human_click(page, trash_btn)
        page.wait_for_timeout(1600)

    # Cambiar a pestaña Bóveda Forense
    vault_tab = page.locator("button:has-text('Bóveda Forense')").first
    if vault_tab.count() > 0:
        smooth_hover(page, vault_tab, steps=22)
        human_click(page, vault_tab)
        page.wait_for_timeout(2500)
        ensure_cursor(page)

        # Hover sobre el registro archivado en la bóveda
        vault_row = page.locator("tr:has-text('45.148.10.215')").first
        if vault_row.count() > 0:
            smooth_hover(page, vault_row, steps=24)
            page.wait_for_timeout(1600)

# -----------------------------------------------------------------------------
# FLUJO 4: 04_logs_export_y_pdf.mp4
# -----------------------------------------------------------------------------
def flow_04_logs_export_y_pdf(page):
    seed_session(page, "admin@ucundinamarca.edu.co", "Administrador", 1, [
        "admin:all", "logs:read", "logs:export"
    ])
    page.goto(f"{BASE_URL}/logs")
    ensure_cursor(page)
    page.wait_for_timeout(2000)

    # 1. Abrir Modal Nuevo Export
    exp_btn = page.locator("button:has-text('Nuevo Export')").first
    smooth_hover(page, exp_btn, steps=22)
    human_click(page, exp_btn)
    page.wait_for_timeout(1200)

    # 2. Rango de fechas reales (4 días)
    start_in = page.locator("#export-start-date")
    start_in.fill("2026-10-18")
    page.wait_for_timeout(300)

    end_in = page.locator("#export-end-date")
    end_in.fill("2026-10-22")
    page.wait_for_timeout(500)

    # 3. Enviar solicitud de exportación
    submit_exp = page.locator("div[role='dialog'] button[type='submit']")
    smooth_hover(page, submit_exp, steps=20)
    human_click(page, submit_exp)
    page.wait_for_timeout(2000)
    ensure_cursor(page)

    # 4. Descargar PDF sobre fila con estado Listo
    ready_row = page.locator("tr:has-text('Listo')").first
    if ready_row.count() > 0:
        smooth_hover(page, ready_row, steps=22)
        page.wait_for_timeout(800)

        pdf_btn = ready_row.locator("button[aria-label*='Esquema Canónico en PDF']").first
        if pdf_btn.count() > 0:
            smooth_hover(page, pdf_btn, steps=20)
            pdf_path = "/tmp/honeymetrics_report.pdf"
            with page.expect_download() as download_info:
                human_click(page, pdf_btn)
            download = download_info.value
            download.save_as(pdf_path)
            page.wait_for_timeout(800)

            # Convertir página 1 a PNG con pdftoppm
            png_base = "/tmp/hm_pdf_preview"
            png_file = f"{png_base}-1.png"
            if os.path.exists(png_file):
                os.remove(png_file)
            subprocess.run(["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1", pdf_path, png_base], check=True)

            if os.path.exists(png_file):
                with open(png_file, "rb") as f:
                    b64_img = base64.b64encode(f.read()).decode("utf-8")

                # Inyectar overlay de visualización en pantalla completa
                page.evaluate("""(b64) => {
                    const overlay = document.createElement('div');
                    overlay.id = 'pdf-preview-overlay';
                    overlay.style = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:2147483646;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px;backdrop-filter:blur(6px);';
                    overlay.innerHTML = `
                      <div style="background:#111;border:2px solid #D4AF37;border-radius:12px;padding:16px;box-shadow:0 0 40px rgba(212,175,55,0.4);max-width:920px;max-height:92vh;display:flex;flex-direction:column;align-items:center;">
                        <div style="width:100%;display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;border-bottom:1px solid #333;padding-bottom:8px;">
                          <span style="color:#D4AF37;font-weight:bold;font-size:16px;font-family:sans-serif;">📄 HoneyMetrics CTI — Reporte Ejecutivo Oficial (Esquema Canónico PDF)</span>
                          <span style="background:rgba(16,185,129,0.2);color:#10b981;border:1px solid rgba(16,185,129,0.4);padding:2px 8px;border-radius:6px;font-size:12px;font-family:monospace;">DESCARGADO & VERIFICADO</span>
                        </div>
                        <img src="data:image/png;base64,${b64}" style="max-height:76vh;border-radius:6px;box-shadow:0 4px 20px rgba(0,0,0,0.8);object-fit:contain;" />
                      </div>
                    `;
                    document.body.appendChild(overlay);
                }""", b64_img)

                # Pausa pedagógica de 3.5 segundos para apreciar el reporte oficial
                page.wait_for_timeout(3500)

                # Cerrar overlay
                page.evaluate("() => { const ov = document.getElementById('pdf-preview-overlay'); if (ov) ov.remove(); }")
                page.wait_for_timeout(1000)

# -----------------------------------------------------------------------------
# FLUJO 5: 05_admin_usuarios_y_roles.mp4
# -----------------------------------------------------------------------------
def flow_05_admin_usuarios_y_roles(page):
    seed_session(page, "admin@ucundinamarca.edu.co", "Administrador", 1, ["admin:all"])
    page.goto(f"{BASE_URL}/settings")
    ensure_cursor(page)
    page.wait_for_timeout(2000)

    # 1. Pestaña Gestión de Usuarios & Roles
    users_tab = page.locator("button[role='tab']:has-text('Gestión de Usuarios & Roles')").first
    if users_tab.count() > 0:
        smooth_hover(page, users_tab, steps=22)
        human_click(page, users_tab)
        page.wait_for_timeout(1800)
        ensure_cursor(page)

    # 2. Clic en "Nuevo Usuario"
    new_user_btn = page.locator("button:has-text('Nuevo Usuario')").first
    smooth_hover(page, new_user_btn, steps=22)
    human_click(page, new_user_btn)
    page.wait_for_timeout(1200)

    # 3. Llenar email
    email_in = page.locator("#user-form-email")
    smooth_hover(page, email_in, steps=18)
    email_in.click()
    email_in.press_sequentially("consultor.soc@ucundinamarca.edu.co", delay=45)
    page.wait_for_timeout(300)

    # 4. Seleccionar rol
    role_select = page.locator("#user-form-role")
    role_select.select_option(value="3")  # Consultor
    page.wait_for_timeout(400)

    # 5. Clic dos veces en "Generar Segura" (CSPRNG)
    gen_btn = page.locator("button:has-text('Generar Segura')").first
    if gen_btn.count() > 0:
        smooth_hover(page, gen_btn, steps=18)
        human_click(page, gen_btn)
        page.wait_for_timeout(700)
        human_click(page, gen_btn)
        page.wait_for_timeout(700)

    # 6. Guardar Usuario
    submit_user = page.locator("div[role='dialog'] button[type='submit']")
    smooth_hover(page, submit_user, steps=20)
    human_click(page, submit_user)
    page.wait_for_timeout(2200)
    ensure_cursor(page)

    # 7. Hover sobre nuevo usuario en la tabla
    created_user_row = page.locator("tr:has-text('consultor.soc@ucundinamarca.edu.co')").first
    if created_user_row.count() > 0:
        smooth_hover(page, created_user_row, steps=24)
        page.wait_for_timeout(1200)

    # 8. Filtrar por rol
    filter_role = page.locator("select[aria-label='Filtrar por rol']").first
    if filter_role.count() > 0:
        smooth_hover(page, filter_role, steps=20)
        filter_role.select_option(value="3")  # Consultor
        page.wait_for_timeout(1200)
        filter_role.select_option(value="ALL")
        page.wait_for_timeout(800)

    # 9. Pestaña "Mi Perfil & Seguridad"
    profile_tab = page.locator("button[role='tab']:has-text('Mi Perfil & Seguridad')").first
    smooth_hover(page, profile_tab, steps=22)
    human_click(page, profile_tab)
    page.wait_for_timeout(1800)
    ensure_cursor(page)

    # 10. Scroll hacia formulario de cambio de clave
    new_pass_in = page.locator("#profile-new-password")
    if new_pass_in.count() > 0:
        new_pass_in.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        smooth_hover(page, new_pass_in, steps=20)
        new_pass_in.click()

        # Tipeo progresivo mostrando la barra Rojo -> Amarillo -> Verde
        new_pass_in.press_sequentially("Sec", delay=65)
        page.wait_for_timeout(800)
        new_pass_in.press_sequentially("ure2026", delay=65)
        page.wait_for_timeout(900)
        new_pass_in.press_sequentially("!Udec", delay=65)
        page.wait_for_timeout(2000)

# -----------------------------------------------------------------------------
# LIMPIEZA FINAL DE BD (Empirical Rigor & Hygiene)
# -----------------------------------------------------------------------------
def cleanup_test_data():
    print("\n--- LIMPIANDO REGISTROS DE PRUEBA DE LA BASE DE DATOS LOCAL ---")
    sql = """
    DELETE FROM threat_ips WHERE ip = '45.148.10.215';
    DELETE FROM threat_ips_vault WHERE ip = '45.148.10.215';
    DELETE FROM users WHERE email = 'consultor.soc@ucundinamarca.edu.co';
    """
    try:
        cmd = ["docker", "exec", "hm_db", "psql", "-U", "postgres", "-d", "honeymetrics", "-c", sql]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Registros transitorios eliminados exitosamente de PostgreSQL.")
    except Exception as e:
        print(f"Advertencia al limpiar base de datos: {e}")

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------
def main():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    print("=======================================================")
    print("🎬 HONEYMETRICS V2.0: PROTOCOLO 'DIRECTOR DE CINE' 1080p")
    print(f"Resolución nativa: 1920x1080 Full HD (CRF 18 Slow)")
    print(f"Destino Videos:    {VIDEOS_DIR}")
    print("=======================================================")

    with sync_playwright() as p:
        flows = [
            ("01_login_y_navegacion.mp4", "22s", flow_01_login_y_navegacion),
            ("02_dashboard_cti_filtros.mp4", "18s", flow_02_dashboard_cti_filtros),
            ("03_threat_center_y_boveda.mp4", "24s", flow_03_threat_center_y_boveda),
            ("04_logs_export_y_pdf.mp4", "20s", flow_04_logs_export_y_pdf),
            ("05_admin_usuarios_y_roles.mp4", "22s", flow_05_admin_usuarios_y_roles),
        ]
        for fname, dur, func in flows:
            target = os.path.join(VIDEOS_DIR, fname)
            if not os.path.exists(target) or fname == "05_admin_usuarios_y_roles.mp4":
                record_video_flow(p, fname, dur, func)

    # Limpieza final de la base de datos
    cleanup_test_data()

    print("\n=======================================================")
    print("✅ GRABACIÓN MULTIMEDIA 1080p FINALIZADA")
    print("=======================================================")

if __name__ == "__main__":
    main()
