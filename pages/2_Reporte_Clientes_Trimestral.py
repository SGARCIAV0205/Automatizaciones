# pages/2_Reporte_Clientes_Trimestral.py

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
    from modules.reporte_clientes_trimestral import run_reporte_clientes_trimestral
    from modules.openai_client import render_openai_config_sidebar
    from modules.auth import authenticate_app, render_session_footer
    from modules.db_adapters import apply_database_patches
except ImportError as e:
    # Fallback: cargar auth directamente desde archivo
    auth_file = root_dir / "modules" / "auth.py"
    if auth_file.exists():
        with open(auth_file, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())
    
    # Intentar importar otros módulos
    try:
        from modules.ui_theme import apply_theme, sidebar_brand
        from modules.reporte_clientes_trimestral import run_reporte_clientes_trimestral
        from modules.openai_client import render_openai_config_sidebar
        from modules.db_adapters import apply_database_patches
    except ImportError as e2:
        st.error(f"Error importando módulos: {e2}")
        st.stop()

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

run_reporte_clientes_trimestral()

# ---------------------------------------------------------------------
# Footer de sesión
# ---------------------------------------------------------------------
render_session_footer()
