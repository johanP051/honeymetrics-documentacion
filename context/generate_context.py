import os

def generate_tree_string(dir_path, prefix="", is_root=True):
    tree_str = ""
    if is_root:
        tree_str += f"{os.path.basename(dir_path)}/\n"
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return ""

    ignored_dirs = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv', 
        'site', '_backup', 'context', '.idea', '.vscode'
    }

    valid_entries = []
    for e in entries:
        full_path = os.path.join(dir_path, e)
        if e in ignored_dirs:
            continue
        if e.endswith(('.pyc', '.xlsx', '.docx', '.png', '.jpg', '.jpeg', '.lock')):
            continue
        valid_entries.append(e)

    for i, entry in enumerate(valid_entries):
        is_last = (i == len(valid_entries) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{entry}\n"
        
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            extension_prefix = "    " if is_last else "│   "
            tree_str += generate_tree_string(full_path, prefix + extension_prefix, is_root=False)
            
    return tree_str

def generar_contexto():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    output_file = 'contexto_documentacion.txt'
    output_path = os.path.join(script_dir, output_file)

    # Solo documentación y configuración relevante
    directorios_ignorados = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv', 
        'site', '_backup', 'context', '.idea', '.vscode', 'mockups'
    }

    # Orden prioritario de archivos para lectura de IA
    archivos_prioritarios = [
        'mkdocs.yml',
        'Pitch_HoneyMetrics.md',
        'Anexo_1_Formato_Propuesta.md',
        'docs/index.md',
        'docs/architecture/system_design.md',
        'docs/architecture/ui_ux_design_system.md',
        'docs/scrum/product_backlog.md',
        'docs/scrum/sprint_1_auth.md',
        'docs/scrum/sprint_2_dashboards.md',
        'docs/scrum/sprint_3_forensics.md',
        'docs/scrum/hus_adicionales_enterprise.md',
        '.agents/rules/arquitectura_desacoplada.md',
        '.agents/rules/reglas_scrum_director.md',
        '.agents/rules/topologia_hardware.md',
        '.agents/skills/scrum-agile-docs/SKILL.md'
    ]

    print(f"Generando contexto consolidado en: {output_path}")

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write("="*80 + "\n")
        f_out.write("# DOCUMENTACIÓN CONSOLIDADA — PROYECTO HONEYMETRICS v2.0\n")
        f_out.write("# Este archivo contiene el contexto íntegro de especificaciones, arquitectura,\n")
        f_out.write("# Product Backlog (70 HUs) y diseño de software para consumo de modelos de IA.\n")
        f_out.write("="*80 + "\n\n")

        # 1. Árbol de Documentación
        f_out.write("="*80 + "\n")
        f_out.write("## 1. ÁRBOL DE DIRECTORIOS DE LA DOCUMENTACIÓN\n")
        f_out.write("="*80 + "\n\n")
        arbol = generate_tree_string(base_dir)
        f_out.write(arbol)
        f_out.write("\n\n")

        # 2. Archivos Prioritarios
        f_out.write("="*80 + "\n")
        f_out.write("## 2. CONTENIDO DETALLADO DE ARCHIVOS DE DOCUMENTACIÓN\n")
        f_out.write("="*80 + "\n\n")

        archivos_procesados = set()

        # Primero los prioritarios
        for rel_path in archivos_prioritarios:
            full_path = os.path.join(base_dir, rel_path)
            if os.path.exists(full_path) and os.path.isfile(full_path):
                if os.path.getsize(full_path) == 0:
                    continue
                try:
                    with open(full_path, 'r', encoding='utf-8') as f_in:
                        contenido = f_in.read()
                    f_out.write(f"{'-'*70}\n")
                    f_out.write(f"--- ARCHIVO: {rel_path} ---\n")
                    f_out.write(f"{'-'*70}\n\n")
                    f_out.write(contenido.strip())
                    f_out.write("\n\n")
                    archivos_procesados.add(rel_path)
                    print(f"  [+] Añadido prioritario: {rel_path}")
                except Exception as e:
                    print(f"  [Error] {rel_path}: {e}")

        # Luego cualquier otro archivo .md no ignorado
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in directorios_ignorados]
            for file in sorted(files):
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, base_dir)
                    if rel_path not in archivos_procesados:
                        if os.path.getsize(full_path) == 0:
                            continue
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f_in:
                                contenido = f_in.read()
                            f_out.write(f"{'-'*70}\n")
                            f_out.write(f"--- ARCHIVO: {rel_path} ---\n")
                            f_out.write(f"{'-'*70}\n\n")
                            f_out.write(contenido.strip())
                            f_out.write("\n\n")
                            archivos_procesados.add(rel_path)
                            print(f"  [+] Añadido adicional: {rel_path}")
                        except Exception as e:
                            print(f"  [Error] {rel_path}: {e}")

    size_kb = os.path.getsize(output_path) / 1024
    print(f"\n¡Contexto generado exitosamente! Tamaño final: {size_kb:.1f} KB")

if __name__ == '__main__':
    generar_contexto()
