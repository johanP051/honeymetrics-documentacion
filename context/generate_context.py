import os

def is_ignored_dir(name):
    ignored = {'.git', '.vscode', '.idea', 'mockups'}
    return name in ignored

def generate_tree_string(dir_path, prefix="", is_root=True):
    tree_str = ""
    if is_root:
        tree_str += f"{os.path.basename(dir_path)}/\n"
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return ""

    ignored_for_tree = {'.git', '.idea', '.vscode'}
    valid_entries = [e for e in entries if e not in ignored_for_tree]

    for i, entry in enumerate(valid_entries):
        is_last = (i == len(valid_entries) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{entry}\n"
        
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            if entry == '.git':
                continue
            extension_prefix = "    " if is_last else "│   "
            tree_str += generate_tree_string(full_path, prefix + extension_prefix, is_root=False)
            
    return tree_str

def generar_contexto():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    output_file = 'contexto_documentacion.txt'
    output_path = os.path.join(script_dir, output_file)

    extensiones_permitidas = {'.md', '.txt', '.json', '.yml', '.yaml'}
    archivos_especificos = {'README_backlog.md', 'product_backlog_honeymetrics.md', '.gitignore'}

    print(f"Iniciando escaneo Documentación en: {base_dir}")

    with open(output_path, 'w', encoding='utf-8') as f_out:
        f_out.write("="*80 + "\n")
        f_out.write("# ÁRBOL DE LA SUITE DE DOCUMENTACIÓN Y PRODUCT BACKLOG (IS2)\n")
        f_out.write("="*80 + "\n\n")
        
        arbol = generate_tree_string(base_dir)
        f_out.write(arbol)
        f_out.write("\n\n")

        f_out.write("="*80 + "\n")
        f_out.write("# CONTENIDO DE LOS DOCUMENTOS Y ESPECIFICACIONES\n")
        f_out.write("="*80 + "\n\n")

        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if not is_ignored_dir(d)]

            for file in files:
                if file in {output_file} or file.endswith('.jpg') or file.endswith('.png'):
                    continue

                _, ext = os.path.splitext(file)
                if ext.lower() in extensiones_permitidas or file in archivos_especificos:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, base_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f_in:
                            contenido = f_in.read()
                            
                        f_out.write(f"{'-'*60}\n")
                        f_out.write(f"--- ARCHIVO: {relative_path} ---\n")
                        f_out.write(f"{'-'*60}\n\n")
                        f_out.write(contenido)
                        f_out.write("\n\n")
                    except Exception as e:
                        print(f"  [Error] No se pudo leer {relative_path}: {e}")

    print(f"¡Éxito! Archivo de contexto documentación generado en: {output_path}")

if __name__ == '__main__':
    generar_contexto()
