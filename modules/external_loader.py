# modules/external_loader.py
from pathlib import Path
import importlib.util
import runpy
import sys
from types import ModuleType
from typing import Iterable, Optional

import streamlit as st
from streamlit.errors import StreamlitAPIException

CANDIDATE_FUNCS: tuple[str, ...] = (
    "render_minutas",
    "render",
    "main",
    "run",
    "app",
)

def _import_module_from_file(py_path: Path) -> Optional[ModuleType]:
    spec = importlib.util.spec_from_file_location(py_path.stem, str(py_path))
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules[py_path.stem] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module

def _call_first_available_fn(module: ModuleType, candidates: Iterable[str]) -> bool:
    for name in candidates:
        fn = getattr(module, name, None)
        if callable(fn):
            try:
                fn()
                return True
            except StreamlitAPIException as e:
                # Si el script intenta volver a setear page_config, lo ignoramos y reintentamos
                if "set_page_config" in str(e):
                    continue
                raise
    return False

def render_external_streamlit_ui(file_path: str,
                                 candidate_functions: Iterable[str] = CANDIDATE_FUNCS) -> bool:
    """
    Intenta renderizar una UI de Streamlit desde un archivo externo .py.
    1) Importa como módulo y busca una función conocida (render_minutas/render/main/run/app).
    2) Si no existe, ejecuta el script con runpy.run_path en un namespace
       donde st.set_page_config es un no-op para evitar conflictos.
    Retorna True si logró renderizar algo, False si no pudo.
    """
    py = Path(file_path)
    if not py.exists() or py.suffix.lower() != ".py":
        st.error("Ruta inválida: debe ser un archivo .py existente.")
        return False

    try:
        # Opción A: import como módulo y llamar función
        module = _import_module_from_file(py)
        if module and _call_first_available_fn(module, candidate_functions):
            return True
    except Exception as e:
        st.warning(f"No se pudo ejecutar como módulo: {e}. Intentaré ejecutar el script completo…")

    # Opción B: ejecutar script completo (aislado) neutralizando set_page_config
    try:
        # Monkey-patch: desactiva set_page_config dentro de este run
        original_set_pc = st.set_page_config
        st.set_page_config = lambda *args, **kwargs: None  # type: ignore[assignment]
        try:
            runpy.run_path(str(py), run_name="__main__")
        finally:
            st.set_page_config = original_set_pc
        return True
    except Exception as e:
        st.error(f"No fue posible renderizar la interfaz externa: {e}")
        return False
