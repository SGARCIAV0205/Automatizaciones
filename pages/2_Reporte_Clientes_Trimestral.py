# pages/2_Reporte_Clientes_Trimestral.py

import os
import sys
from pathlib import Path
import streamlit as st

from modules.ui_theme import apply_theme, sidebar_brand
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
# Localizar módulo Reporte Clientes Trimestral
# ---------------------------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]   # .../Automatizaciones (raíz del repo)
reporte_root = AUTOM_ROOT / "Reporte Clientes Trimestral"
app_file = reporte_root / "app.py"

if not app_file.exists():
    st.error(f"No se encontró 'app.py' en: {reporte_root}")
    st.write(f"DEBUG - Contenido de {AUTOM_ROOT}:")
    try:
        for item in AUTOM_ROOT.iterdir():
            if item.is_dir():
                st.write(f"  - {item.name}/")
    except Exception as e:
        st.write(f"Error listando directorio: {e}")
    st.stop()

# ---------------------------------------------------------------------
# Cargar módulo de forma aislada
# ---------------------------------------------------------------------
original_sys_path = list(sys.path)

try:
    # Demo mode por defecto (si aplica)
    os.environ.setdefault("UBIMIA_DEMO_MODE", "1")
    
    # Permite imports como: import config, rt_ingest, etc.
    sys.path.insert(0, str(reporte_root))

    # Usar importlib para cargar el módulo de forma más segura
    from importlib.machinery import SourceFileLoader
    
    # Leer el contenido del archivo para verificar si tiene st.set_page_config
    with open(app_file, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Si tiene st.set_page_config, crear una versión temporal sin él
    if 'st.set_page_config(' in app_content:
        # Crear archivo temporal modificado
        temp_file = reporte_root / "app_temp.py"
        modified_content = app_content.replace(
            'st.set_page_config(',
            '# st.set_page_config('
        )
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        # Cargar el archivo temporal
        loader = SourceFileLoader("reporte_clientes_ui", str(temp_file))
        reporte_module = loader.load_module()
        
        # Limpiar archivo temporal
        temp_file.unlink()
    else:
        # Cargar directamente si no tiene conflictos
        loader = SourceFileLoader("reporte_clientes_ui", str(app_file))
        reporte_module = loader.load_module()

finally:
    sys.path = original_sys_path

# ---------------------------------------------------------------------
# Ejecutar UI si tiene función main
# ---------------------------------------------------------------------
if hasattr(reporte_module, "main") and callable(reporte_module.main):
    reporte_module.main()
else:
    st.info("Módulo Reporte Clientes Trimestral cargado correctamente.")
