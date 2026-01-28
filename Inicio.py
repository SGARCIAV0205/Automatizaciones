# Inicio.py

from pathlib import Path
import streamlit as st
import sys

# Agregar la carpeta del asistente al path
sys.path.insert(0, str(Path(__file__).parent / "Asistente Virtual AI Ubimia"))

from modules.ui_theme import apply_theme, centered_logo_and_titles, sidebar_brand
from modules.auth import authenticate_app

# ---------------------------------------------------
# Configuración de página
# ---------------------------------------------------
st.set_page_config(
    page_title="Asistente Virtual AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# ---------------------------------------------------
# Autenticación requerida
# ---------------------------------------------------
authenticate_app()

# ---------------------------------------------------
# Contenido principal (solo se muestra si está autenticado)
# ---------------------------------------------------
ASSETS = Path(__file__).parent / "Asistente Virtual AI Ubimia" / "assets"
sidebar_brand()

# ---------------------------------------------------
# Hero
# ---------------------------------------------------
centered_logo_and_titles(
    title_top="¿En qué te puedo asistir hoy?",
    subtitle=(
        "Centraliza tus automatizaciones: genera minutas, crea el reporte trimestral de clientes, "
        "monitorea competidores y gestiona reuniones 1:1, sin código."
    ),
    logo_path=str(ASSETS / "logo_ubimia.png")
    if (ASSETS / "logo_ubimia.png").exists()
    else None,
)

st.markdown("<div class='ub-space-xl'></div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Tarjetas (mismo look & feel)
# ---------------------------------------------------
c1, c2, c3 = st.columns(3, gap="large")
c4, c5, c6 = st.columns(3, gap="large")

def card_open(tag: str, title: str, desc: str):
    st.markdown('<div class="ub-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="ub-chip">{tag}</div>', unsafe_allow_html=True)
    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Tarjeta 1 – Minutas
# ---------------------------------------------------
with c1:
    card_open(
        "RESUMEN",
        "Generar Minutas",
        "Sube una transcripción, obtén acuerdos y próximos pasos y exporta a Markdown, PDF o DOCX.",
    )
    st.page_link("pages/1_Generar_Minutas.py", label="Ir al módulo →")
    card_close()

# ---------------------------------------------------
# Tarjeta 2 – Reporte Clientes Trimestral (NUEVO)
# ---------------------------------------------------
with c2:
    card_open(
        "ANÁLISIS",
        "Reporte Clientes Trimestral",
        "Genera presentaciones ejecutivas por cliente y trimestre en PPTX, con o sin IA.",
    )
    st.page_link("pages/2_Reporte_Clientes_Trimestral.py", label="Ir al módulo →")
    card_close()

# ---------------------------------------------------
# Tarjeta 3 – Radar Competidores
# ---------------------------------------------------
with c3:
    card_open(
        "ANÁLISIS",
        "Radar de Competidores",
        "Monitorea noticias y señales clave por competidor, con exportación directa a PPTX.",
    )
    st.page_link("pages/3_Radar_Competidores.py", label="Ir al módulo →")
    card_close()

# ---------------------------------------------------
# Tarjeta 4 – Reuniones 1:1
# ---------------------------------------------------
with c4:
    card_open(
        "SEGUIMIENTO",
        "Reuniones Mensuales 1:1",
        "Gestiona reuniones mensuales: historial, health-check, compromisos y preparación automática.",
    )
    st.page_link("pages/4_Reuniones_1to1.py", label="Ir al módulo →")
    card_close()

# ---------------------------------------------------
# Tarjeta 5 – Template Writer
# ---------------------------------------------------
with c5:
    card_open(
        "REPORTES",
        "Template Writer",
        "Genera documentos o presentaciones a partir de una configuración y plantillas estándar.",
    )
    st.page_link("pages/5_Template_Writer.py", label="Ir al módulo →")
    card_close()

# ---------------------------------------------------
# Tarjeta 6 – Próximamente
# ---------------------------------------------------
with c6:
    card_open(
        "AI POWERED",
        "Funciones AI Integradas",
        "Todas las herramientas ahora incluyen funcionalidades de ChatGPT para mejorar tu productividad.",
    )
    st.markdown("**🤖 AI disponible en:**")
    st.markdown("• Generación de minutas")
    st.markdown("• Análisis de competidores") 
    st.markdown("• Insights de clientes")
    st.markdown("• Preparación de 1:1s")
    card_close()

st.markdown("<div class='ub-space-lg'></div>", unsafe_allow_html=True)
