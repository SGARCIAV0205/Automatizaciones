# pages/5_Template_Writer.py

import streamlit as st
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.ui_theme import apply_theme, sidebar_brand
from modules.auth import authenticate_app
from modules.openai_client import render_openai_config_sidebar

# Configuración de página
st.set_page_config(
    page_title="Template Writer",
    layout="wide",
)

apply_theme()

# Autenticación requerida
authenticate_app()

# Contenido principal
sidebar_brand()
render_openai_config_sidebar()

# Título principal
st.title("📄 Template Writer")
st.markdown("Genera documentos o presentaciones a partir de una configuración y plantillas estándar.")

# Buscar el módulo Template Writer
AUTOM_ROOT = Path(__file__).resolve().parents[2]
template_root = AUTOM_ROOT / "Template Writer"

if not template_root.exists():
    st.warning("⚠️ Módulo 'Template Writer' no encontrado en la estructura del proyecto.")
    st.info("📁 Ubicación esperada: " + str(template_root))
    
    # Interfaz básica mientras tanto
    st.subheader("🚧 Funcionalidad en Desarrollo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Configuración del Documento")
        
        tipo_doc = st.selectbox(
            "Tipo de documento",
            ["Reporte Ejecutivo", "Presentación", "Propuesta", "Informe Técnico"]
        )
        
        titulo = st.text_input("Título del documento")
        
        contenido = st.text_area(
            "Contenido principal",
            height=200,
            placeholder="Describe el contenido que quieres generar..."
        )
        
        formato = st.selectbox(
            "Formato de salida",
            ["DOCX", "PPTX", "PDF", "Markdown"]
        )
    
    with col2:
        st.markdown("### ⚙️ Configuración Avanzada")
        
        plantilla = st.selectbox(
            "Plantilla base",
            ["Corporativa", "Minimalista", "Técnica", "Creativa"]
        )
        
        idioma = st.selectbox("Idioma", ["Español", "Inglés"])
        
        incluir_graficos = st.checkbox("Incluir gráficos", value=True)
        incluir_tablas = st.checkbox("Incluir tablas", value=False)
        
        st.markdown("### 🎨 Personalización")
        color_primario = st.color_picker("Color primario", "#1f77b4")
        
    if st.button("🚀 Generar Documento", type="primary"):
        if titulo and contenido:
            with st.spinner("Generando documento..."):
                # Simulación de generación
                import time
                time.sleep(2)
                
                st.success("✅ Documento generado exitosamente")
                
                # Mostrar resumen
                st.markdown("### 📋 Resumen del Documento")
                st.info(f"""
                **Tipo:** {tipo_doc}
                **Título:** {titulo}
                **Formato:** {formato}
                **Plantilla:** {plantilla}
                **Idioma:** {idioma}
                """)
                
                # Botón de descarga simulado
                st.download_button(
                    label=f"📥 Descargar {formato}",
                    data="Contenido del documento generado...",
                    file_name=f"{titulo.replace(' ', '_')}.{formato.lower()}",
                    mime="application/octet-stream"
                )
        else:
            st.warning("⚠️ Por favor completa el título y contenido")

else:
    st.info("🔄 Cargando módulo completo de Template Writer...")
    # Aquí iría la carga del módulo real cuando esté disponible

# Información adicional
st.markdown("---")
st.markdown("### 💡 Características del Template Writer")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **📄 Formatos Soportados**
    - Microsoft Word (DOCX)
    - PowerPoint (PPTX)
    - PDF
    - Markdown
    """)

with col2:
    st.markdown("""
    **🎨 Plantillas**
    - Corporativa
    - Minimalista
    - Técnica
    - Creativa
    """)

with col3:
    st.markdown("""
    **⚡ Funciones**
    - Generación automática
    - Personalización de colores
    - Múltiples idiomas
    - Integración con AI
    """)