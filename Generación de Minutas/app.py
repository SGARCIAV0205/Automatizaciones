# app.py
import os
import json
from pathlib import Path
from datetime import date

import streamlit as st
from dotenv import load_dotenv

# Módulos locales del proyecto
try:
    from ingest import load_transcript
    from split import chunk_text
    from summarize import map_blocks, reduce_summaries, consistency_check
    from render import render_markdown, save_outputs
    from utils import load_participants_csv, base_payload
    from llm import count_tokens, estimate_cost
except ImportError as e:
    st.error(f"Error importando módulos locales: {e}")
    st.info("Verifica que todos los archivos del módulo estén presentes.")
    st.stop()

# ---------------------------------------------------------------------
# Configuración inicial
# ---------------------------------------------------------------------
load_dotenv()

# Verificar disponibilidad de API key
api_key_available = False
try:
    api_key_available = bool(st.secrets.get("OPENAI_API_KEY"))
except (AttributeError, FileNotFoundError):
    api_key_available = bool(os.getenv("OPENAI_API_KEY"))

DEMO_MODE = not api_key_available

st.set_page_config(page_title="Minutas AI", layout="wide")

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

# Mostrar estado de la API
if api_key_available:
    st.success("OpenAI API conectada - Generación inteligente habilitada")
else:
    st.warning("OpenAI API no disponible - Usando modo demostración")
    st.info("Para habilitar la generación inteligente, configura tu API key de OpenAI en los secrets de Streamlit Cloud")

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

    # Detectar si estamos en Streamlit Cloud o local
    is_cloud = os.getenv("STREAMLIT_SHARING_MODE") or "streamlit.app" in os.getenv("HOSTNAME", "")
    
    if is_cloud:
        # En Streamlit Cloud, usar directorio temporal
        import tempfile
        if "output_dir" not in st.session_state:
            st.session_state["output_dir"] = tempfile.gettempdir()
        
        st.info("En Streamlit Cloud los archivos se guardan temporalmente y se pueden descargar directamente.")
        st.text_input(
            label="",
            value="Directorio temporal (descarga automática)",
            disabled=True,
            key="output_dir_display"
        )
    else:
        # En local, permitir selección de directorio
        if "output_dir" not in st.session_state:
            st.session_state["output_dir"] = str(Path.home() / "Downloads")

        dir_col, btn_col = st.columns([5, 2])

        with dir_col:
            # Permitir edición manual del directorio
            new_dir = st.text_input(
                label="",
                value=st.session_state["output_dir"],
                key="output_dir_input",
                help="Puedes editar la ruta manualmente"
            )
            
            # Actualizar si cambió
            if new_dir != st.session_state["output_dir"]:
                st.session_state["output_dir"] = new_dir

        with btn_col:
            if st.button("Examinar"):
                st.session_state["show_folder_picker"] = True

        # File uploader para selección de carpeta (solo local)
        if st.session_state.get("show_folder_picker", False):
            st.info("Selecciona cualquier archivo dentro de la carpeta donde quieres guardar las minutas")
            folder_anchor = st.file_uploader(
                "Archivo de referencia para la carpeta",
                type=None,
                key="hidden_folder_picker",
                help="El archivo no se usará, solo para seleccionar la carpeta"
            )

            if folder_anchor:
                st.session_state["output_dir"] = str(Path(folder_anchor.name).parent)
                st.session_state["show_folder_picker"] = False
                st.success(f"Directorio seleccionado: {st.session_state['output_dir']}")
                st.rerun()

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
        try:
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
                
                try:
                    payload = json.loads(final)
                except json.JSONDecodeError as e:
                    st.error(f"Error procesando respuesta de AI: {e}")
                    st.text_area("Respuesta cruda de AI:", final, height=200)
                    st.stop()
                
                payload["participantes"] = participantes
                minuta_md = render_markdown(payload)

            base_path = Path(output_dir) / f"minuta_{proyecto.replace(' ', '_')}_{fecha}"
            
            # Detectar si estamos en Streamlit Cloud
            is_cloud = os.getenv("STREAMLIT_SHARING_MODE") or "streamlit.app" in os.getenv("HOSTNAME", "") or output_dir == "/tmp"
            
            if not is_cloud:
                # Solo guardar archivos si NO estamos en la nube
                try:
                    save_outputs(minuta_md, payload, base_path)
                    st.success(f"Minuta generada y guardada en: {base_path.parent}")
                except Exception as e:
                    st.warning(f"No se pudo guardar en {output_dir}: {e}")
                    is_cloud = True  # Forzar modo descarga si falla el guardado
            
            if is_cloud:
                st.success("Minuta generada correctamente.")
                # En Streamlit Cloud, ofrecer descarga directa
                st.markdown("### Descargar archivos")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Descargar Markdown
                    st.download_button(
                        label="Descargar MD",
                        data=minuta_md,
                        file_name=f"minuta_{proyecto.replace(' ', '_')}_{fecha}.md",
                        mime="text/markdown"
                    )
                
                with col2:
                    # Descargar JSON
                    json_data = json.dumps(payload, ensure_ascii=False, indent=2)
                    st.download_button(
                        label="Descargar JSON", 
                        data=json_data,
                        file_name=f"minuta_{proyecto.replace(' ', '_')}_{fecha}.json",
                        mime="application/json"
                    )
                
                with col3:
                    # Intentar generar PDF si pypandoc está disponible
                    try:
                        import pypandoc
                        pdf_data = pypandoc.convert_text(minuta_md, "pdf", format="md")
                        st.download_button(
                            label="Descargar PDF",
                            data=pdf_data,
                            file_name=f"minuta_{proyecto.replace(' ', '_')}_{fecha}.pdf",
                            mime="application/pdf"
                        )
                    except Exception:
                        st.info("PDF no disponible (requiere pandoc)")
            
            st.text_area("Vista previa de la minuta", minuta_md, height=420)
            
        except Exception as e:
            st.error(f"Error generando minuta: {e}")
            st.info("Intenta nuevamente o verifica la transcripción.")
