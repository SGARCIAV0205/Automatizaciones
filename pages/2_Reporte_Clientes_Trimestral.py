# pages/2_Reporte_Clientes_Trimestral.py

import os
import streamlit as st

from modules.ui_theme import apply_theme, sidebar_brand
from modules.reporte_clientes_trimestral import run_reporte_clientes_trimestral
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app

# ---------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Reporte Clientes Trimestral",
    layout="wide"
)

apply_theme()

# ---------------------------------------------------------------------
# Autenticación requerida
# ---------------------------------------------------------------------
authenticate_app(show_session_info=False)

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

run_reporte_clientes_trimestral()
