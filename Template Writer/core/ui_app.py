import os
import tempfile
from pathlib import Path

import streamlit as st
import yaml

from placeholders_extract import extract_placeholders_docx, extract_placeholders_pptx
from openai_generate import generate_placeholder_map
from docx_fill import fill_docx_template
from pptx_fill import fill_pptx_template


# -----------------------------
# Utils
# -----------------------------
def load_cfg() -> dict:
    here = Path(__file__).parent
    for p in [here / "config.yaml", here.parent / "config.yaml"]:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
    return {}


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def resolve_template_path(rel_path: str) -> Path:
    return project_root() / rel_path


def prettify(ph: str) -> str:
    return ph.replace("_", " ").title()


# Orden lógico según plantilla
PLACEHOLDER_ORDER = [
    "TITULO",
    "SUBTITULO",
    "CLIENTE",
    "FECHA",
    "AUTOR",
    "RESUMEN_EJECUTIVO",
    "CONTEXTO",
    "OBJETIVO",
    "ALCANCE",
    "HALLAZGO_1",
    "HALLAZGO_2",
    "HALLAZGO_3",
    "RECOMENDACION_1",
    "RECOMENDACION_2",
    "RECOMENDACION_3",
    "SIGUIENTES_PASOS",
    "RIESGO_1",
    "MITIGANTE_1",
    "RIESGO_2",
    "MITIGANTE_2",
    "ANEXOS",
]


def order_placeholders(detected: list[str]) -> list[str]:
    ordered = [p for p in PLACEHOLDER_ORDER if p in detected]
    remaining = [p for p in detected if p not in ordered]
    return ordered + remaining


def is_long_field(ph: str) -> bool:
    return any(
        k in ph.upper()
        for k in [
            "RESUMEN",
            "CONTEXTO",
            "OBJETIVO",
            "ALCANCE",
            "HALLAZGO",
            "RECOMENDACION",
            "SIGUIENTES",
            "RIESGO",
            "MITIGANTE",
            "ANEXO",
        ]
    )


# -----------------------------
# App
# -----------------------------
def app() -> None:
    cfg = load_cfg()

    st.set_page_config(
        page_title=cfg.get("module_name", "Template Writer"),
        layout="wide",
    )

    # -----------------------------
    # Header / Descripción
    # -----------------------------
    st.title(cfg.get("module_name", "Template Writer"))

    st.markdown(
        """
Este módulo permite generar **documentos Word (DOCX)** o **presentaciones PowerPoint (PPTX)** 
a partir de **plantillas predefinidas**, de dos formas:

**1. Generación automática con IA**
- Describe el reporte que necesitas.
- El sistema genera todo el contenido y lo inserta en la plantilla.

**2. Llenado manual guiado**
- Completa un formulario estructurado.
- Cada campo corresponde a una sección del documento.
- No necesitas escribir placeholders ni usar IA.

Las plantillas están preconfiguradas y no requieren ser cargadas por el usuario.
"""
    )

    st.divider()

    # -----------------------------
    # Configuración
    # -----------------------------
    templates_cfg = cfg.get("templates", {})
    docx_path = resolve_template_path(templates_cfg.get("docx"))
    pptx_path = resolve_template_path(templates_cfg.get("pptx"))

    openai_cfg = cfg.get("openai", {})
    ai_enabled = openai_cfg.get("enabled", True)
    model = openai_cfg.get("model", "gpt-4o")
    temperature = float(openai_cfg.get("temperature", 0.2))
    max_output_tokens = int(openai_cfg.get("max_output_tokens", 1200))

    # -----------------------------
    # Selección de salida
    # -----------------------------
    out_type = st.selectbox("Tipo de reporte a generar", ["Documento (DOCX)", "Presentación (PPTX)"])
    is_docx = out_type.startswith("Documento")
    suffix = ".docx" if is_docx else ".pptx"
    template_path = docx_path if is_docx else pptx_path

    if not template_path.exists():
        st.error(f"No existe la plantilla esperada:\n{template_path}")
        st.stop()

    # -----------------------------
    # Detectar placeholders
    # -----------------------------
    detected = (
        extract_placeholders_docx(str(template_path))
        if is_docx
        else extract_placeholders_pptx(str(template_path))
    )

    if not detected:
        st.error("La plantilla no contiene placeholders válidos.")
        st.stop()

    placeholders = order_placeholders(detected)

    # -----------------------------
    # Selección de modo
    # -----------------------------
    mode = st.radio(
        "Modo de generación",
        ["Generar automáticamente con IA", "Llenar manualmente el reporte"],
        horizontal=True,
    )

    st.divider()

    # =============================
    # MODO IA
    # =============================
    if mode.startswith("Generar automáticamente"):
        st.subheader("Generación automática con IA")

        if not ai_enabled:
            st.warning("La generación con IA está deshabilitada en configuración.")
            st.stop()

        if not os.environ.get("OPENAI_API_KEY"):
            st.error("No se encontró OPENAI_API_KEY. Este modo requiere API Key.")
            st.stop()

        prompt = st.text_area(
            "Describe el reporte que deseas generar",
            height=220,
            placeholder="Ej: Genera un reporte ejecutivo sobre el avance del proyecto X...",
        )

        if st.button("Generar reporte con IA", type="primary", disabled=not prompt.strip()):
            with st.spinner("Generando contenido y construyendo archivo..."):
                mapping = generate_placeholder_map(
                    user_prompt=prompt,
                    placeholders=placeholders,
                    model=model,
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                )

                with tempfile.TemporaryDirectory() as td:
                    td = Path(td)
                    tmp = td / f"template{suffix}"
                    out = td / f"output{suffix}"
                    tmp.write_bytes(template_path.read_bytes())

                    if is_docx:
                        fill_docx_template(str(tmp), str(out), mapping)
                    else:
                        fill_pptx_template(str(tmp), str(out), mapping)

                    st.success("Reporte generado.")
                    st.download_button(
                        "Descargar",
                        data=out.read_bytes(),
                        file_name=f"reporte_generado{suffix}",
                        mime="application/octet-stream",
                    )

    # =============================
    # MODO MANUAL
    # =============================
    else:
        st.subheader("Llenado manual del reporte")
        st.caption("Completa cada sección. El documento se generará automáticamente.")

        with st.form("manual_form"):
            mapping = {}
            for ph in placeholders:
                label = prettify(ph)
                if is_long_field(ph):
                    mapping[ph] = st.text_area(label, height=90)
                else:
                    mapping[ph] = st.text_input(label)

            submitted = st.form_submit_button("Generar reporte", type="primary")

        if submitted:
            with st.spinner("Construyendo archivo..."):
                with tempfile.TemporaryDirectory() as td:
                    td = Path(td)
                    tmp = td / f"template{suffix}"
                    out = td / f"output{suffix}"
                    tmp.write_bytes(template_path.read_bytes())

                    if is_docx:
                        fill_docx_template(str(tmp), str(out), mapping)
                    else:
                        fill_pptx_template(str(tmp), str(out), mapping)

                    st.success("Reporte generado.")
                    st.download_button(
                        "Descargar",
                        data=out.read_bytes(),
                        file_name=f"reporte_manual{suffix}",
                        mime="application/octet-stream",
                    )


if __name__ == "__main__":
    app()
