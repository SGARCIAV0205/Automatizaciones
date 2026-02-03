# modules/radar_competidores.py

import sys
from pathlib import Path
import streamlit as st


def find_automatizaciones_root(start: Path) -> Path | None:
    """
    Sube en el árbol de directorios hasta encontrar la carpeta 'Automatizaciones'.
    """
    current = start.resolve()
    for _ in range(10):  # límite de seguridad
        if current.name.lower() == "automatizaciones":
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def run_radar_competidores():
    """
    Adaptador para ejecutar el módulo standalone
    'Radar Competidores' desde el Asistente Virtual.
    """

    # --------------------------------------------------
    # 1) Encontrar raíz real 'Automatizaciones'
    # --------------------------------------------------
    automatizaciones_root = find_automatizaciones_root(Path(__file__))

    if automatizaciones_root is None:
        st.error(
            "No se pudo localizar la carpeta raíz 'Automatizaciones'. "
            "Revisa la estructura del proyecto."
        )
        st.stop()

    modulo_root = automatizaciones_root / "Radar Competidores"

    if not modulo_root.exists():
        st.error(
            f"No se encontró el módulo 'Radar Competidores' en:\n"
            f"{automatizaciones_root}"
        )
        st.stop()

    # Verificar que existe el archivo app.py en ui/
    ui_app_path = modulo_root / "ui" / "app.py"
    if not ui_app_path.exists():
        st.error(
            f"No se encontró 'app.py' en:\n"
            f"{modulo_root / 'ui'}"
        )
        st.stop()

    # --------------------------------------------------
    # 2) Ejecutar módulo real usando importlib para evitar conflictos de caché
    # --------------------------------------------------
    original_sys_path = list(sys.path)
    
    try:
        # Agregar las rutas necesarias para el módulo
        sys.path.insert(0, str(modulo_root))
        sys.path.insert(0, str(modulo_root / "ui"))
        sys.path.insert(0, str(modulo_root / "src"))

        # Usar importlib con nombre único para evitar conflictos de caché
        import importlib.util
        spec = importlib.util.spec_from_file_location("radar_competidores_app", ui_app_path)
        radar_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(radar_app)

        if not hasattr(radar_app, "main"):
            st.error(
                "El archivo app.py del módulo 'Radar Competidores' "
                "no define una función main()."
            )
            st.stop()

        # Ejecutar la interfaz del radar con skip_page_config=True
        radar_app.main(skip_page_config=True)

    except ImportError as e:
        st.error(f"Error importando el módulo Radar Competidores: {e}")
        st.info("Verificando estructura de archivos...")
        
        # Debug info
        if st.checkbox("Mostrar información de debug - Radar"):
            st.write(f"**Módulo root:** {modulo_root}")
            st.write(f"**UI path:** {modulo_root / 'ui'}")
            st.write(f"**App.py existe:** {ui_app_path.exists()}")
            st.write(f"**Sys.path actual:** {sys.path[:3]}")
        
        st.stop()
        
    except Exception as e:
        st.error(f"Error ejecutando el módulo Radar Competidores: {e}")
        st.stop()
        
    finally:
        sys.path = original_sys_path