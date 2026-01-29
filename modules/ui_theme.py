# modules/ui_theme.py
import streamlit as st
from pathlib import Path
import base64

ASSETS = Path(__file__).resolve().parents[1] / "assets"

def apply_theme():
    st.markdown("""
    <style>
    /* ===== Tipografía global (Space Grotesk -> Arial -> sans) ===== */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

    :root{
      --ub-navy:#0B1220;
      --ub-navy-2:#121A2B;
      --ub-mint:#2EE6A6;
      --ub-gray:#9CA3AF;
      --ub-white:#FFFFFF;
    }

    html, body, [class*="css"], .stMarkdown, .stText, .stButton>button, .stSelectbox, .stDateInput,
    .stNumberInput, .stTextInput, .stRadio, .stCheckbox, .stDataFrame, .stAlert,
    .stDownloadButton>button, .stSlider, .stTabs, .stTextArea textarea {
      font-family: 'Space Grotesk', Arial, sans-serif !important;
      letter-spacing: .1px;
    }

    /* ===== Layout general ===== */
    .block-container {
    max-width: 100% !important;
    padding-top: 2.4rem;
    padding-bottom: 2.4rem;
    padding-left: 4rem;
    padding-right: 4rem;
    }


    /* Fondo decorativo superior (“fondito verde”) */
    .ub-bg{
      position: fixed; inset: 0 0 auto 0; height: 260px; z-index: -1;
      background: radial-gradient(1100px 260px at 50% -60px,
                                   rgba(46,230,166,0.20),
                                   rgba(11,18,32,0.0));
    }

    /* ===== Botones (incluye st.link_button) ===== */
   .stButton>button, .st-link-button{
      background: var(--ub-mint) !important;
      color: #0B1220 !important;
      font-weight: 800 !important;

      border-radius: 8px !important;   /* ← BOTÓN MÁS RECTANGULAR */
      padding: .65rem 1.4rem !important;
      border: 1px solid rgba(255,255,255,0.08) !important;
      box-shadow: 0 6px 16px rgba(46,230,166,.18);
    }
    .stButton>button:hover, .st-link-button:hover{ filter: brightness(1.05); }

    /* ===== Sliders: línea, thumb y valor ===== */
    input[type=range]::-webkit-slider-thumb {
      background: var(--ub-mint) !important;
      border: 2px solid var(--ub-navy-2) !important;
    }
    input[type=range]::-webkit-slider-runnable-track {
      background: linear-gradient(90deg, var(--ub-mint) 0%,
                                       rgba(46,230,166,0.35) 100%) !important;
      height: 5px !important; border-radius: 10px !important;
    }
    input[type=range]::-moz-range-thumb {
      background: var(--ub-mint) !important;
      border: 2px solid var(--ub-navy-2) !important;
    }
    input[type=range]::-moz-range-track {
      background: linear-gradient(90deg, var(--ub-mint) 0%,
                                       rgba(46,230,166,0.35) 100%) !important;
      height: 5px !important; border-radius: 10px !important;
    }
    /* Valor numérico encima del slider */
    .stSlider > div[data-testid="stThumbValue"] {
      color: var(--ub-mint) !important; font-weight: 700 !important;
    }
    /* Línea base detrás del control */
    div[data-baseweb="slider"] > div:first-child {
      background: linear-gradient(90deg, rgba(46,230,166,0.25) 0%,
                                       rgba(255,255,255,0.05) 100%) !important;
    }

    /* ===== Inputs redondeados ===== */
    .stSelectbox [data-baseweb="select"]>div,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput input,
    .stTextArea textarea{
      border-radius: 12px !important;
    }

    /* ===== Tarjetas reutilizables para módulos ===== */
    .ub-card{
      background: var(--ub-navy-2);
      border:1px solid rgba(255,255,255,0.06);
      border-radius:20px; padding:24px;
      transition: all .15s ease; height:100%;
      box-shadow: 0 6px 18px rgba(0,0,0,.28);
    }
    .ub-card:hover{ transform: translateY(-3px);
                    border-color: rgba(46,230,166,0.50); }
    .ub-chip{
      display:inline-block; background:rgba(46,230,166,.16);
      color:var(--ub-mint);
      border:1px solid rgba(46,230,166,.45);
      padding:4px 10px; border-radius:999px;
      font-size:12px; font-weight:800; margin-bottom:10px;
    }
    .ub-card h3{ margin:.25rem 0 .5rem 0; font-size:26px; font-weight:800; color: var(--ub-white); }
    .ub-card p{ color: var(--ub-gray); font-size:16px; line-height:1.5; }

    /* ===== Títulos centrados del hero ===== */
    .ub-title-center{ text-align:center; margin:.6rem 0 0 0; font-weight:900; font-size:54px; }
    .ub-sub-center { text-align:center; color: var(--ub-gray); margin:.35rem 0 2.0rem 0; font-size:18px; }
    .ub-badge{
      display:inline-block; font-size:13px; color:#0B1220; background:var(--ub-mint);
      padding:7px 14px; border-radius:999px; font-weight:900;
    }

    /* ===== Logo en sidebar ===== */
    .ub-side-logo { display:flex; justify-content:center; margin:10px 0 14px 0; }
    .ub-side-sep  { height:1px; width:100%; background:rgba(255,255,255,.10);
                    margin:6px 0 14px 0; }

    /* ===== Espaciadores reutilizables ===== */
    .ub-space-lg{ height: 36px; }
    .ub-space-xl{ height: 56px; }

    /* Limpieza de subrayados */
    a{ text-decoration: none; }


    /* ============================================================
       NUEVO: TITULOS UNIFICADOS PARA TODAS LAS PÁGINAS 
       Se agregan sin modificar nada más del archivo.
       ============================================================ */
    h1, h2 {
        font-family: 'Space Grotesk', Arial, sans-serif !important;
        font-weight: 700 !important;
        color: var(--ub-white) !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.8rem !important;
    }

    h1 {
        font-size: 2.35rem !important;   /* Tamaño uniforme global */
    }

    h2 {
        font-size: 1.75rem !important;
    }
    /* ============================================================ */

    </style>
    <div class="ub-bg"></div>
    """, unsafe_allow_html=True)



def centered_logo_and_titles(title_top: str, subtitle: str, logo_path: str | None = None):
    html_logo = ""
    if logo_path:
        p = Path(logo_path)
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()
            html_logo = f'<img src="data:image/{p.suffix[1:]};base64,{b64}" style="height:86px; margin-bottom:18px;" />'
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:center; flex-direction:column; margin-top:.2rem;">
            {html_logo}
            <div class="ub-badge">ASISTENTE VIRTUAL AI</div>
            <h1 class="ub-title-center">{title_top}</h1>
            <div class="ub-sub-center">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def sidebar_brand(logo_path: str | None = None):
    """Coloca el logo arriba del menú lateral (antes de la navegación)."""
    b64 = ""
    if logo_path:
        p = Path(logo_path)
        if p.exists():
            b64 = base64.b64encode(p.read_bytes()).decode()

    css = f"""
    <style>
    /* Inserta el logo por encima del nav del sidebar */
    [data-testid="stSidebarNav"]::before {{
      content: "";
      display:block;
      height: 48px;
      margin: 8px 12px 14px 12px;
      background: url('data:image/png;base64,{b64}') no-repeat center / contain;
    }}
    /* Línea separadora bajo el logo */
    [data-testid="stSidebarNav"]::after {{
      content:"";
      display:block;
      height:1px; margin: 6px 8px 10px 8px;
      background: rgba(255,255,255,.10);
    }}
    </style>
    """
    st.sidebar.markdown(css, unsafe_allow_html=True)
