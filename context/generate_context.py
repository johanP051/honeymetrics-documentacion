import os

def is_venv(path):
    """Detecta si una carpeta es un entorno virtual"""
    name = os.path.basename(path).lower()
    
    # 1. Nombres obvios o que contienen 'venv' (ej. HoneyVenv, .venv, venv)
    if 'venv' in name or name == 'env':
        return True
        
    # 2. Indicadores estándar de venv
    if os.path.exists(os.path.join(path, 'pyvenv.cfg')) or \
       os.path.exists(os.path.join(path, 'bin', 'activate')):
        return True
        
    # 3. Estructura típica de venv (lib/pythonX.X/site-packages)
    lib_path = os.path.join(path, 'lib')
    if os.path.exists(lib_path) and os.path.isdir(lib_path):
        try:
            for py_dir in os.listdir(lib_path):
                if os.path.exists(os.path.join(lib_path, py_dir, 'site-packages')):
                    return True
        except Exception:
            pass
            
    return False

def generate_tree_string(dir_path, prefix="", is_root=True):
    """
    Genera un string con el árbol de directorios estilo comando 'tree'.
    Incluye archivos ocultos (.env, .gitignore) pero evita entrar en .git/
    """
    tree_str = ""
    if is_root:
        tree_str += f"{os.path.basename(dir_path)}/\n"
    
    try:
        entries = sorted(os.listdir(dir_path))
    except PermissionError:
        return ""

    # Nombres a ignorar en el árbol visual
    ignored_for_tree = {'__pycache__', 'downloads', '.idea', '.vscode', 'node_modules', 'HoneyVenv', 'venv', '.venv'}
    
    # Filtrar entradas
    valid_entries = []
    for e in entries:
        full_path = os.path.join(dir_path, e)
        # Ocultar extensiones basura y carpetas ignoradas
        if e in ignored_for_tree or e.endswith('.pyc') or e.endswith('.jsonl'):
            continue
        # Ocultar entornos virtuales en el árbol
        if os.path.isdir(full_path) and is_venv(full_path):
            continue
        valid_entries.append(e)

    for i, entry in enumerate(valid_entries):
        is_last = (i == len(valid_entries) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{entry}\n"
        
        full_path = os.path.join(dir_path, entry)
        
        if os.path.isdir(full_path):
            # Si es .git, mostramos la carpeta pero NO entramos (para no generar ruido)
            if entry == '.git':
                continue
                
            extension_prefix = "    " if is_last else "│   "
            tree_str += generate_tree_string(full_path, prefix + extension_prefix, is_root=False)
            
    return tree_str

def generar_contexto():
    script_dir = os.path.abspath(os.path.dirname(__file__))
    base_dir = os.path.abspath(os.path.join(script_dir, '..'))
    
    output_file = 'contexto_proyecto.txt'
    output_path = os.path.join(script_dir, output_file)

    extensiones_permitidas = {'.py', '.html', '.css', '.js', '.yml', '.yaml', '.sql', '.md'}
    archivos_especificos = {'Dockerfile', 'requirements.txt', '.env.example', '.gitignore'}

    # ---> AQUÍ AGREGAMOS 'vendor' A LA LISTA DE IGNORADOS <---
    directorios_ignorados = {
        '.git', '__pycache__', 'migrations', 'media', 'UML', 'data', 
        '.vscode', '.idea', 'node_modules', 'logs',
        'vendor', 'HoneyVenv', 'venv', '.venv'
    }

    print(f"Iniciando escaneo en: {base_dir}")

    with open(output_path, 'w', encoding='utf-8') as f_out:
        # 1. ESCRIBIR EL ÁRBOL DE DIRECTORIOS PRIMERO
        f_out.write("="*80 + "\n")
        f_out.write("# ÁRBOL DE DIRECTORIOS DEL PROYECTO\n")
        f_out.write("="*80 + "\n\n")
        
        arbol = generate_tree_string(base_dir)
        f_out.write(arbol)
        f_out.write("\n\n")

        # 2. ESCRIBIR EL CONTENIDO DE LOS ARCHIVOS
        f_out.write("="*80 + "\n")
        f_out.write("# CONTENIDO DE LOS ARCHIVOS\n")
        f_out.write("="*80 + "\n\n")

        for root, dirs, files in os.walk(base_dir):
            
            # Filtrar carpetas
            dirs_to_keep = []
            for d in dirs:
                dir_path = os.path.join(root, d)
                if d in directorios_ignorados or is_venv(dir_path):
                    continue
                dirs_to_keep.append(d)
            dirs[:] = dirs_to_keep

            for file in files:
                if file.endswith('.jsonl') or file.endswith('.pyc') or file == output_file:
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

    print(f"\n¡Éxito! Archivo de contexto generado en: {output_path}")

if __name__ == '__main__':
    generar_contexto()