# pages/1_Generar_Minutas.py

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
    page_title="Generación de Minutas",
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
# Localizar módulo Generación de Minutas
# --------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]   # .../Automatizaciones (raíz del repo)
minutas_root = AUTOM_ROOT / "Generación de Minutas"
app_file = minutas_root / "app.py"

st.write(f"DEBUG - Buscando en: {minutas_root}")
st.write(f"DEBUG - Archivo existe: {app_file.exists()}")

if not app_file.exists():
    st.error(f"No se encontró 'app.py' en: {minutas_root}")
    st.write(f"DEBUG - Contenido de {AUTOM_ROOT}:")
    try:
        for item in AUTOM_ROOT.iterdir():
            st.write(f"  - {item.name}")
    except Exception as e:
        st.write(f"Error listando directorio: {e}")
    st.stop()

# --------------------------------------------------
# Cargar módulo de forma aislada
# --------------------------------------------------
original_sys_path = list(sys.path)

try:
    # Permite imports como: import llm, render, utils, etc.
    sys.path.insert(0, str(minutas_root))

    loader = SourceFileLoader("generacion_minutas_ui", str(app_file))
    minutas_module = loader.load_module()

finally:
    sys.path = original_sys_path

# --------------------------------------------------
# Ejecutar UI
# --------------------------------------------------
# Caso 1: existe main()
if hasattr(minutas_module, "main") and callable(minutas_module.main):
    minutas_module.main()

# Caso 2: app.py ya ejecuta Streamlit al importarse
else:
    st.info(
        "Generación de Minutas cargada. "
        "Si no ves la interfaz, encapsula el código en una función main()."
    )
