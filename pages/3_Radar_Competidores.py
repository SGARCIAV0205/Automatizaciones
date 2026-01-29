# pages/3_Radar_Competidores.py

import os
import streamlit as st

from modules.ui_theme import apply_theme, sidebar_brand
from modules.radar_competidores import run_radar_competidores
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app, render_session_footer
from modules.db_adapters import apply_database_patches

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
