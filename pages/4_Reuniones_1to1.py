# pages/4_Reuniones_1to1.py

import os
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
import streamlit as st

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Cargar módulos de forma robusta
try:
    from modules.ui_theme import apply_theme, sidebar_brand
    from modules.openai_client import render_openai_config_sidebar
    from modules.auth import authenticate_app, render_session_footer
    from modules.db_adapters import apply_database_patches
except ImportError as e:
    # Fallback: cargar módulos directamente desde archivos
    modules_to_load = {
        'auth.py': ['authenticate_app', 'render_session_footer'],
        'ui_theme.py': ['apply_theme', 'sidebar_brand'],
        'openai_client.py': ['render_openai_config_sidebar'],
        'db_adapters.py': ['apply_database_patches']
    }
    
    for module_file, functions in modules_to_load.items():
        module_path = root_dir / "modules" / module_file
        if module_path.exists():
            try:
                with open(module_path, 'r', encoding='utf-8') as f:
                    module_code = f.read()
                    # Crear un namespace temporal para el módulo
                    module_namespace = {}
                    exec(module_code, module_namespace)
                    # Importar las funciones necesarias al namespace global
                    for func_name in functions:
                        if func_name in module_namespace:
                            globals()[func_name] = module_namespace[func_name]
            except Exception as e2:
                st.error(f"Error cargando {module_file}: {e2}")
    
    # Definir apply_database_patches si no existe
    if 'apply_database_patches' not in globals():
        def apply_database_patches():
            pass  # Función vacía como fallback

# --------------------------------------------------
# Configuración base
# --------------------------------------------------
st.set_page_config(
    page_title="Reuniones Mensuales 1to1",
    layout="wide",
)

apply_theme()

# --------------------------------------------------
# Autenticación requerida
# --------------------------------------------------
authenticate_app()

# --------------------------------------------------
# Contenido principal (solo se muestra si está autenticado)
# --------------------------------------------------
sidebar_brand()

# --------------------------------------------------
# Configuración de OpenAI en sidebar
# --------------------------------------------------
render_openai_config_sidebar()

# --------------------------------------------------
# Aplicar parches de base de datos
# --------------------------------------------------
apply_database_patches()

# --------------------------------------------------
# Localizar módulo 1to1
# --------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]   # .../Automatizaciones (raíz del repo)
one_to_one_root = AUTOM_ROOT / "1to1"

if not one_to_one_root.exists():
    st.error(f"No se encontró la carpeta '1to1' en: {AUTOM_ROOT}")
    st.stop()

ui_dir = one_to_one_root / "ui"
module_path = ui_dir / "app.py"

if not module_path.exists():
    st.error(f"No se encontró 'app.py' en: {ui_dir}")
    st.stop()

# --------------------------------------------------
# Cargar módulo de forma aislada
# --------------------------------------------------
original_sys_path = list(sys.path)

try:
    # Asegurar que Python encuentra todos los módulos del proyecto 1to1
    sys.path.insert(0, str(one_to_one_root))
    sys.path.insert(0, str(ui_dir))

    loader = SourceFileLoader("one_to_one_external", str(module_path))
    one_to_one_module = loader.load_module()

    # Evitar segunda llamada a set_page_config dentro del módulo externo
    try:
        one_to_one_module.st.set_page_config = lambda *args, **kwargs: None
    except Exception:
        pass

    # Ejecutar interfaz original
    if hasattr(one_to_one_module, "main"):
        one_to_one_module.main()
    else:
        st.error("El módulo 'app.py' de 1to1 no define la función 'main()'.")

finally:
    sys.path = original_sys_path

# --------------------------------------------------
# Footer de sesión
# --------------------------------------------------
render_session_footer()