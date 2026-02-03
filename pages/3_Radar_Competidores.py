# pages/3_Radar_Competidores.py

import os
import sys
from pathlib import Path
import streamlit as st

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Cargar módulos de forma robusta
try:
    from modules.ui_theme import apply_theme, sidebar_brand
    from modules.radar_competidores import run_radar_competidores
    from modules.openai_client import render_openai_config_sidebar
    from modules.auth import authenticate_app, render_session_footer
    from modules.db_adapters import apply_database_patches
except ImportError as e:
    # Fallback: cargar módulos directamente desde archivos
    modules_to_load = {
        'auth.py': ['authenticate_app', 'render_session_footer'],
        'ui_theme.py': ['apply_theme', 'sidebar_brand'],
        'radar_competidores.py': ['run_radar_competidores'],
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

# ---------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Radar de Competidores",
    layout="wide"
)

apply_theme()

# ---------------------------------------------------------------------
# Autenticación requerida
# ---------------------------------------------------------------------
authenticate_app()

# ---------------------------------------------------------------------
# Contenido principal (solo se muestra si está autenticado)
# ---------------------------------------------------------------------
sidebar_brand()

# ---------------------------------------------------------------------
# Configuración de OpenAI en sidebar
# ---------------------------------------------------------------------
render_openai_config_sidebar()

# ---------------------------------------------------------------------
# Aplicar parches de base de datos
# ---------------------------------------------------------------------
apply_database_patches()

# ---------------------------------------------------------------------
# Ejecutar módulo
# ---------------------------------------------------------------------

# Demo mode por defecto (si aplica)
os.environ.setdefault("UBIMIA_DEMO_MODE", "1")

run_radar_competidores()

# ---------------------------------------------------------------------
# Footer de sesión
# ---------------------------------------------------------------------
render_session_footer()
