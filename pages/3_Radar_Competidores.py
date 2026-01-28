# pages/3_Radar_Competidores.py

import os
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader

import streamlit as st
from modules.ui_theme import apply_theme, sidebar_brand
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app


# ---------------------------------------------------------
# Configuración base de la página principal
# ---------------------------------------------------------
st.set_page_config(page_title="Radar de Competidores", layout="wide")
apply_theme()

# ---------------------------------------------------------
# Autenticación requerida
# ---------------------------------------------------------
authenticate_app()

# ---------------------------------------------------------
# Contenido principal (solo se muestra si está autenticado)
# ---------------------------------------------------------
ASSETS = Path(__file__).parents[1] / "assets"
logo_sidebar = ASSETS / "logo_ubimia_sidebar.png"
sidebar_brand(str(logo_sidebar) if logo_sidebar.exists() else str(ASSETS / "logo_ubimia.png"))

# ---------------------------------------------------------
# Configuración de OpenAI en sidebar
# ---------------------------------------------------------
render_openai_config_sidebar()

# ---------------------------------------------------------
# 1. Localizar proyecto externo "Radar Competidores"
# ---------------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]        # .../Automatizaciones (raíz del repo)
radar_root = AUTOM_ROOT / "Radar Competidores"

if not radar_root.exists():
    st.error(f"No se encontró la carpeta 'Radar Competidores' en: {AUTOM_ROOT}")
    st.stop()

ui_dir = radar_root / "ui"
module_path = ui_dir / "app.py"

if not module_path.exists():
    st.error(f"No se encontró 'app.py' en: {ui_dir}")
    st.stop()

# ---------------------------------------------------------
# 2. Cargar módulo de forma aislada (mismo método que Generar Minutas)
# ---------------------------------------------------------
original_sys_path = list(sys.path)

try:
    # Añadimos las rutas del proyecto de competidores
    sys.path.insert(0, str(radar_root))
    sys.path.insert(0, str(ui_dir))

    # Leer el contenido del archivo y modificarlo para evitar st.set_page_config
    with open(module_path, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Comentar la línea de st.set_page_config si existe
    modified_content = app_content.replace(
        'st.set_page_config(',
        '# st.set_page_config('
    )
    
    # Ejecutar el código modificado
    exec(modified_content, globals())

finally:
    # Restaurar sys.path tal como estaba
    sys.path = original_sys_path
