# pages/1_Generar_Minutas.py

import sys
from pathlib import Path
from importlib.machinery import SourceFileLoader
import streamlit as st

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Cargar módulos de forma robusta
try:
    from modules.ui_theme import apply_theme, sidebar_brand
    from modules.openai_client import render_openai_config_sidebar
    from modules.auth import authenticate_app, render_session_footer
except ImportError as e:
    # Fallback: cargar auth directamente desde archivo
    auth_file = root_dir / "modules" / "auth.py"
    if auth_file.exists():
        # Ejecutar el archivo auth.py en el namespace global
        with open(auth_file, 'r', encoding='utf-8') as f:
            exec(f.read(), globals())
    else:
        st.error(f"No se pudo cargar el módulo de autenticación: {e}")
        st.stop()
    
    # Intentar importar otros módulos
    try:
        from modules.ui_theme import apply_theme, sidebar_brand
        from modules.openai_client import render_openai_config_sidebar
    except ImportError as e2:
        st.error(f"Error importando otros módulos: {e2}")
        st.stop()

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

if not app_file.exists():
    st.error(f"No se encontró 'app.py' en: {minutas_root}")
    st.stop()

# --------------------------------------------------
# Cargar módulo de forma aislada
# --------------------------------------------------
original_sys_path = list(sys.path)

try:
    # Permite imports como: import llm, render, utils, etc.
    sys.path.insert(0, str(minutas_root))

    # Leer el contenido del archivo y modificarlo para evitar st.set_page_config
    with open(app_file, 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Comentar la línea de st.set_page_config
    modified_content = app_content.replace(
        'st.set_page_config(',
        '# st.set_page_config('
    )
    
    # Ejecutar el código modificado
    exec(modified_content, globals())

finally:
    sys.path = original_sys_path

# --------------------------------------------------
# Footer de sesión
# --------------------------------------------------
render_session_footer()
