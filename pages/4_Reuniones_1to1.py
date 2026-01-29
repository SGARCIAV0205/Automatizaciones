# pages/4_Reuniones_1to1.py

import os
import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
import streamlit as st

from modules.ui_theme import apply_theme, sidebar_brand
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app

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