# app.py
import os
import json
from pathlib import Path
from datetime import date

import streamlit as st
from dotenv import load_dotenv

# Módulos locales del proyecto
from ingest import load_transcript
from split import chunk_text
from summarize import map_blocks, reduce_summaries, consistency_check
from render import render_markdown, save_outputs
from utils import load_participants_csv, base_payload
from llm import count_tokens, estimate_cost

# ---------------------------------------------------------------------
# Configuración inicial
# ---------------------------------------------------------------------
load_dotenv()
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

st.set_page_config(page_title="Minutas AI", page_icon="🗒️", layout="wide")

# ---------------------------------------------------------------------
# CSS de alineación fina
# ---------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Ajuste vertical del input de ruta */
    div[data-testid="stTextInput"] {
        margin-top: -6px;
    }

    /* Botón Examinar */
    button {
        height: 3rem;
        white-space: nowrap;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Header
# =========================
st.title("Automatización de Minutas")

st.markdown(
    """
    Genera minutas estructuradas a partir de transcripciones de reuniones.
    Carga la transcripción, ajusta parámetros y obtén un documento listo para distribuir.
    """
)

with st.expander("Guía rápida de configuración"):
    st.markdown(
        """
        Tokens por bloque:
        - Reuniones cortas (≤30 min): 800–1200
        - Reuniones medias (30–60 min): 1500–2200
        - Reuniones largas (>60 min): 2500–3500  

        Modelo (Map):
        - gpt-4o-mini: recomendado para extracción inicial.
        - gpt-4o: solo si el contenido es muy técnico.

        Modelo (Reduce / Check):
        - gpt-4o: recomendado para coherencia y estructura final.
        """
    )

st.divider()

# =========================
# Paso 1: Parámetros
# =========================
st.subheader("1. Parámetros de la minuta")

c1, c2, c3 = st.columns([3, 3, 4])

with c1:
    proyecto = st.text_input("Proyecto", value="Reunión General")

with c2:
    fecha = st.date_input("Fecha")

with c3:
    st.markdown("**Directorio de salida**")

    if "output_dir" not in st.session_state:
        st.session_state["output_dir"] = r"C:\Users\sara.garcia\OneDrive"

    dir_col, btn_col = st.columns([5, 2])

    with dir_col:
        st.text_input(
            label="",
            value=st.session_state["output_dir"],
            disabled=True,
            key="output_dir_display"
        )

    with btn_col:
        if st.button("Examinar"):
            st.session_state["show_folder_picker"] = True

# File uploader oculto
if st.session_state.get("show_folder_picker", False):
    folder_anchor = st.file_uploader(
        "Selecciona cualquier archivo dentro de la carpeta deseada",
        type=None,
        key="hidden_folder_picker"
    )

    if folder_anchor:
        st.session_state["output_dir"] = str(Path(folder_anchor.name).parent)
        st.session_state["show_folder_picker"] = False
        st.success(f"Directorio seleccionado: {st.session_state['output_dir']}")

output_dir = st.session_state["output_dir"]

c4, c5 = st.columns(2)

with c4:
    tokens_por_bloque = st.slider(
        "Tokens por bloque",
        min_value=500,
        max_value=4000,
        step=100,
        value=1800,
    )

with c5:
    modelo_map = st.selectbox(
        "Modelo (Map)",
        ["gpt-4o-mini", "gpt-4o"],
        index=0,
    )

modelo_reduce = st.selectbox(
    "Modelo (Reduce / Check)",
    ["gpt-4o", "gpt-4.1"],
    index=0,
)

st.divider()

# =========================
# Paso 2: Transcripción
# =========================
st.subheader("2. Carga de la transcripción")

col_t1, col_t2 = st.columns(2)

with col_t1:
    uploaded_file = st.file_uploader(
        "Sube la transcripción (.txt, .docx, .srt, .vtt)",
        type=["txt", "docx", "srt", "vtt"]
    )

with col_t2:
    texto_manual = st.text_area(
        "O pega aquí la transcripción",
        height=260,
        placeholder="Pega aquí el texto completo de la reunión..."
    )

if "texto_transcripcion" not in st.session_state:
    st.session_state.texto_transcripcion = ""

if texto_manual.strip():
    st.session_state.texto_transcripcion = texto_manual.strip()
    st.success("Transcripción cargada desde texto.")
elif uploaded_file:
    try:
        tmp_path = Path(f"_tmp_{uploaded_file.name}")
        tmp_path.write_bytes(uploaded_file.getbuffer())
        st.session_state.texto_transcripcion = load_transcript(str(tmp_path))
        tmp_path.unlink(missing_ok=True)
        st.success("Transcripción cargada desde archivo.")
    except Exception as e:
        st.error(f"Error al leer la transcripción: {e}")
else:
    st.info("Carga un archivo o pega el texto para continuar.")

st.divider()

# =========================
# Paso 3: Participantes
# =========================
st.subheader("3. Participantes (opcional)")

participants_file = st.file_uploader(
    "Sube un CSV con columnas: nombre, email, rol",
    type=["csv"]
)

if participants_file:
    participantes = load_participants_csv(participants_file)
    st.success(f"{len(participantes)} participantes cargados.")
else:
    participantes = []
    st.info("Si no se carga CSV, la minuta se generará sin participantes.")

st.divider()

# =========================
# Paso 4: Generación
# =========================
st.subheader("4. Generar minuta")

disabled = not bool(st.session_state.texto_transcripcion.strip())

if st.button("Generar Minuta", disabled=disabled):
    with st.spinner("Generando minuta..."):
        if DEMO_MODE:
            payload = base_payload(
                proyecto=proyecto,
                fecha=str(fecha),
                participantes=participantes,
            )
            payload["resumen"] = "Minuta generada en modo demostración."
            minuta_md = render_markdown(payload)
        else:
            bloques = chunk_text(
                st.session_state.texto_transcripcion,
                target_tokens=tokens_por_bloque
            )
            parciales = map_blocks(bloques, model=modelo_map)
            reducido = reduce_summaries(parciales, model=modelo_reduce)
            final = consistency_check(reducido, model=modelo_reduce)
            payload = json.loads(final)
            payload["participantes"] = participantes
            minuta_md = render_markdown(payload)

        base_path = Path(output_dir) / f"minuta_{proyecto.replace(' ', '_')}_{fecha}"
        save_outputs(minuta_md, payload, base_path)

        st.success("Minuta generada correctamente.")
        st.text_area("Vista previa de la minuta", minuta_md, height=420)
