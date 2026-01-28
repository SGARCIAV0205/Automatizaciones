# pages/4_Reuniones_1to1.py

import os
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader

import streamlit as st
from modules.ui_theme import apply_theme, sidebar_brand
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app

# ---------------------------------------------------------
# Configuración inicial de la página principal
# ---------------------------------------------------------
st.set_page_config(page_title="Reuniones Mensuales 1to1", layout="wide")
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
# 1. Localizar proyecto externo "1to1"
# ---------------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]      # Cambiar a parents[1] porque ahora estamos en la raíz
one_to_one_root = AUTOM_ROOT / "1to1"

if not one_to_one_root.exists():
    st.error(f"No se encontró la carpeta '1to1' en: {AUTOM_ROOT}")
    st.info("💡 Este módulo requiere la carpeta '1to1' del proyecto original.")
    st.stop()

ui_dir = one_to_one_root / "ui"
module_path = ui_dir / "app.py"

if not module_path.exists():
    st.error(f"No se encontró 'app.py' en: {ui_dir}")
    st.stop()

# ---------------------------------------------------------
# 2. Carga dinámica del módulo externo
# ---------------------------------------------------------
try:
    original_sys_path = list(sys.path)

    # Asegurar que Python encuentra todos los módulos del proyecto 1to1
    sys.path.insert(0, str(one_to_one_root))
    sys.path.insert(0, str(ui_dir))

    loader = SourceFileLoader("one_to_one_external", str(module_path))
    one_to_one_module = loader.load_module()

finally:
    # Restaurar sys.path
    sys.path = original_sys_path

# ---------------------------------------------------------
# 3. Ejecutar interfaz externa (main)
# ---------------------------------------------------------
if not hasattr(one_to_one_module, "main"):
    st.error("El módulo 'app.py' de 1to1 no define la función 'main()'.")
    st.stop()

# Evitar segunda llamada a set_page_config dentro del módulo externo
try:
    one_to_one_module.st.set_page_config = lambda *args, **kwargs: None
except Exception:
    pass

# Ejecutar interfaz original
one_to_one_module.main()
