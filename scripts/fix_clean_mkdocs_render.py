#!/usr/bin/env python3
"""
fix_clean_mkdocs_render.py
Aplica las 4 reglas de renderizado limpio en MkDocs Material sobre todos los archivos docs/**/*.md:
1. Convierte bloques GitHub Alerts (> [!NOTE]) a Admonitions de MkDocs Material (!!! note "...").
2. Garantiza un salto de línea en blanco antes de listas ordenadas/desordenadas tras líneas con dos puntos (:).
3. Añade el atributo poster a las etiquetas <video> según el archivo de video enlazado.
4. Actualiza los dominios obsoletos honey.johan-d3v.site hacia los dominios oficiales de Cloudflare.
"""

import os
import re
import glob

DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs"))

VIDEO_POSTER_MAP = {
    "01_login_y_navegacion.mp4": "assets/screenshots/fig01_login.png",
    "02_dashboard_cti_filtros.mp4": "assets/screenshots/fig04_dashboard_cti.png",
    "03_threat_center_y_boveda.mp4": "assets/screenshots/fig05_threat_center_ioc.png",
    "04_logs_export_y_pdf.mp4": "assets/screenshots/fig06_exportacion_logs_modal.png",
    "05_admin_usuarios_y_roles.mp4": "assets/screenshots/fig07_admin_usuarios_roles.png",
}

ALERT_TYPE_MAP = {
    "NOTE": ("note", "⚡ Nota"),
    "IMPORTANT": ("warning", "⚡ Importante"),
    "WARNING": ("warning", "⚡ Advertencia"),
    "CAUTION": ("danger", "⚡ Precaución"),
    "TIP": ("tip", "⚡ Consejo")
}

def fix_alerts(lines):
    new_lines = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # Match alert header like: > [!NOTE] or > [!IMPORTANT]
        m = re.match(r"^(\s*)>\s*\[!(NOTE|IMPORTANT|WARNING|CAUTION|TIP)\]", line)
        if m:
            indent = m.group(1)
            alert_type_raw = m.group(2)
            adm_type, default_title = ALERT_TYPE_MAP.get(alert_type_raw, ("note", "⚡ Nota"))
            
            # Read subsequent blockquote lines
            i += 1
            body_lines = []
            while i < n and (lines[i].strip().startswith(">") or (lines[i].strip() == "" and i+1 < n and lines[i+1].strip().startswith(">"))):
                curr = lines[i].rstrip()
                if curr.strip().startswith(">"):
                    # Strip leading '>' and one space
                    stripped = re.sub(r"^\s*>\s?", "", curr)
                    body_lines.append(stripped)
                elif curr.strip() == "":
                    body_lines.append("")
                i += 1
            
            # Extract custom title if first line is like **Title:** or **Title — Sub:**
            title = default_title
            if body_lines:
                first_line = body_lines[0].strip()
                title_m = re.match(r"^\*\*(.*?)\*\*:?\s*(.*)$", first_line)
                if title_m:
                    extracted_title = title_m.group(1).rstrip(":").strip()
                    if not extracted_title.startswith("⚡"):
                        extracted_title = f"⚡ {extracted_title}"
                    title = extracted_title
                    rest = title_m.group(2).strip()
                    if rest:
                        body_lines[0] = rest
                    else:
                        body_lines.pop(0)

            # Build admonition
            new_lines.append(f'{indent}!!! {adm_type} "{title}"\n')
            for b in body_lines:
                if b.strip():
                    new_lines.append(f"{indent}    {b}\n")
                else:
                    new_lines.append("\n")
            continue
        else:
            new_lines.append(line)
            i += 1
    return new_lines

def fix_collapsed_lists(lines):
    new_lines = []
    n = len(lines)
    for i in range(n):
        line = lines[i]
        new_lines.append(line)
        if i + 1 < n:
            stripped = line.rstrip()
            next_stripped = lines[i+1].lstrip()
            # If line ends with ':' and next line starts with list marker without blank line in between
            if stripped.endswith(":") and re.match(r"^(1\.|-|\*)\s", next_stripped):
                # Don't add blank line if within YAML frontmatter or inside table or code block
                if not stripped.startswith("---") and not stripped.startswith("|") and not stripped.startswith("```"):
                    new_lines.append("\n")
    return new_lines

def fix_video_tags(content):
    # For every video in VIDEO_POSTER_MAP, check if <video> lacks poster
    for video_name, poster_path in VIDEO_POSTER_MAP.items():
        # Match <video ...> that precedes a source with video_name
        pattern = re.compile(
            r'(<video\s+)(?![^>]*\bposter=)([^>]*?>\s*<source\s+src=[\"\'][^\"\']*?' + re.escape(video_name) + r'[\"\'])',
            re.IGNORECASE | re.DOTALL
        )
        def repl(m):
            return f'{m.group(1)}poster="{poster_path}" {m.group(2)}'
        content = pattern.sub(repl, content)
    return content

def fix_domains(content, file_path):
    # In manual usuario: user visits the frontend URL
    content = content.replace("https://honey.johan-d3v.site/", "https://honeymetrics-frontend.johan-sebastianposada.workers.dev/")
    content = content.replace("https://honey.johan-d3v.site", "https://honeymetrics-frontend.johan-sebastianposada.workers.dev")
    # In deployment / backend context:
    if "guia-despliegue" in file_path:
        content = content.replace(
            "honey.johan-d3v.site",
            "api-honey-master-homeserver.johan-d3v.site"
        )
        content = content.replace(
            "https://honeymetrics-frontend.johan-sebastianposada.workers.dev",
            "https://api-honey-master-homeserver.johan-d3v.site"
        )
    return content

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)
    lines = fix_alerts(lines)
    lines = fix_collapsed_lists(lines)
    content = "".join(lines)
    content = fix_video_tags(content)
    content = fix_domains(content, file_path)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Procesado: {os.path.relpath(file_path, DOCS_DIR)}")

def main():
    md_files = glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
    print(f"Encontrados {len(md_files)} archivos Markdown en {DOCS_DIR}")
    for md in md_files:
        process_file(md)
    print("Corrección completada exitosamente.")

if __name__ == "__main__":
    main()
