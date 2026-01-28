from io import BytesIO
import pandas as pd
import streamlit as st
import importlib.util
import sys
from pathlib import Path

def read_csvfile(uploaded_file):
    try:
        return pd.read_csv(uploaded_file)
    except Exception:
        return None

def read_table(uploaded_file):
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            return pd.read_csv(uploaded_file)
        return pd.read_excel(uploaded_file)
    except Exception:
        return None

def dynamic_action_items():
    st.caption("Añade acuerdos/tareas con responsable y fecha de vencimiento.")
    items = []
    with st.container(border=True):
        n = st.number_input("Número de acuerdos/tareas", min_value=0, max_value=50, value=3, step=1)
        for i in range(int(n)):
            with st.expander(f"Item #{i+1}", expanded=(i==0)):
                desc = st.text_area(f"Descripción #{i+1}", key=f"desc_{i}")
                resp = st.text_input(f"Responsable #{i+1}", key=f"resp_{i}")
                due = st.date_input(f"Fecha compromiso #{i+1}", key=f"due_{i}")
                items.append({"descripcion": desc, "responsable": resp, "fecha": str(due)})
    return items

def parse_competitors(text_block, uploaded_file):
    names = []
    if text_block:
        names += [x.strip() for x in text_block.split("\n") if x.strip()]
    if uploaded_file:
        df = read_table(uploaded_file)
        if df is not None:
            col = None
            for c in df.columns:
                if c.strip().lower() in {"competidor", "competitors", "competitor", "empresa", "name"}:
                    col = c
                    break
            if col:
                names += df[col].dropna().astype(str).str.strip().tolist()
    names = [n for n in dict.fromkeys(names)]
    return names

def load_callable_from_file(file_path: str, func_name: str):
    """
    Carga dinámicamente una función desde un archivo .py.
    Retorna el callable o None si falla.
    """
    try:
        p = Path(file_path)
        if not p.exists():
            return None
        spec = importlib.util.spec_from_file_location(p.stem, str(p))
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        sys.modules[p.stem] = module
        spec.loader.exec_module(module)  # type: ignore[attr-defined]
        fn = getattr(module, func_name, None)
        return fn
    except Exception:
        return None
