# modules/template_writer.py

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


def run_template_writer():
    """
    Adaptador para ejecutar el módulo standalone
    'Template Writer' desde el Asistente Virtual.
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

    modulo_root = automatizaciones_root / "Template Writer"

    if not modulo_root.exists():
        st.error(
            f"No se encontró el módulo 'Template Writer' en:\n"
            f"{automatizaciones_root}"
        )
        st.stop()

    # --------------------------------------------------
    # 2) Ejecutar módulo real
    # --------------------------------------------------
    original_sys_path = list(sys.path)
    sys.path.insert(0, str(modulo_root))
    sys.path.insert(0, str(modulo_root / "core"))

    try:
        import ui_app as template_app

        if not hasattr(template_app, "app"):
            st.error(
                "El archivo ui_app.py del módulo 'Template Writer' "
                "no define una función app()."
            )
            st.stop()

        template_app.app(skip_page_config=True)

    finally:
        sys.path = original_sys_path