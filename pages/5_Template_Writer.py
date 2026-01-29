# pages/5_Template_Writer.py

import os
import sys
from pathlib import Path
import streamlit as st

# Agregar el directorio raíz al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.ui_theme import apply_theme, sidebar_brand
from modules.template_writer import run_template_writer
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app, render_session_footer

# ---------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Template Writer",
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
# Ejecutar módulo
# ---------------------------------------------------------------------

# Demo mode por defecto (si aplica)
os.environ.setdefault("UBIMIA_DEMO_MODE", "1")

run_template_writer()

# ---------------------------------------------------------------------
# Footer de sesión
# ---------------------------------------------------------------------
render_session_footer()