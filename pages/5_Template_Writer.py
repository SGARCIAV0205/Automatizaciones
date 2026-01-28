# pages/5_Template_Writer.py

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
st.set_page_config(page_title="Template Writer", layout="wide")
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

ASSETS = Path(__file__).parents[1] / "assets"
logo_sidebar = ASSETS / "logo_ubimia_sidebar.png"
sidebar_brand(str(logo_sidebar) if logo_sidebar.exists() else str(ASSETS / "logo_ubimia.png"))

# --------------------------------------------------
# Localizar Template Writer
# --------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]  # Cambiar a parents[1] porque ahora estamos en la raíz
tw_root = AUTOM_ROOT / "Template Writer"
core_dir = tw_root / "core"
ui_file = core_dir / "ui_app.py"

if not ui_file.exists():
    st.error(f"No se encontró 'ui_app.py' en: {core_dir}")
    st.info("💡 Este módulo requiere la carpeta 'Template Writer' del proyecto original.")
    st.stop()

# --------------------------------------------------
# Cargar módulo externo de forma aislada
# --------------------------------------------------
original_sys_path = list(sys.path)

try:
    sys.path.insert(0, str(core_dir))
    sys.path.insert(0, str(tw_root))

    loader = SourceFileLoader("template_writer_ui", str(ui_file))
    tw_module = loader.load_module()

finally:
    sys.path = original_sys_path

# --------------------------------------------------
# Ejecutar UI
# --------------------------------------------------

fn = None
for name in ("main", "app", "run", "ui"):
    if hasattr(tw_module, name) and callable(getattr(tw_module, name)):
        fn = getattr(tw_module, name)
        break

if fn is not None:
    fn()
else:
    # Si el script ya renderiza Streamlit al importarse, no hay nada que llamar
    st.info("Template Writer cargado. Si la interfaz no aparece, envuélvela en una función main() o app().")
