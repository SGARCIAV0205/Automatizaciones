# pages/1_Generar_Minutas.py

import sys
from pathlib import Path
import streamlit as st
from datetime import date
import pandas as pd

# Agregar módulos al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.ui_theme import apply_theme, sidebar_brand
from modules.openai_client import render_openai_config_sidebar, openai_client, is_openai_available
from modules.auth import authenticate_app
from modules.minutas import generate_minutes, render_ai_enhancement_section
from modules.utils import dynamic_action_items

# --------------------------------------------------
# Configuración base
# --------------------------------------------------
st.set_page_config(
    page_title="Generación de Minutas",
    layout="wide",
)

apply_theme()

# --------------------------------------------------
# Autenticación requerida
# --------------------------------------------------
authenticate_app()

# --------------------------------------------------
# Contenido principal
# --------------------------------------------------
sidebar_brand()
render_openai_config_sidebar()

# Título principal
st.title("Generar Minutas")
st.markdown("Sube una transcripción, obtén acuerdos y próximos pasos y exporta a Markdown, PDF o DOCX.")

# --------------------------------------------------
# Buscar módulo externo primero
# --------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[2]
minutas_root = AUTOM_ROOT / "Generación de Minutas"
app_file = minutas_root / "app.py"

if app_file.exists():
    st.info("Cargando módulo completo de Generación de Minutas...")
    
    # Cargar módulo externo
    original_sys_path = list(sys.path)
    try:
        sys.path.insert(0, str(minutas_root))
        from importlib.machinery import SourceFileLoader
        loader = SourceFileLoader("generacion_minutas_ui", str(app_file))
        minutas_module = loader.load_module()
        
        if hasattr(minutas_module, "main") and callable(minutas_module.main):
            minutas_module.main()
        else:
            st.info("Módulo cargado. Si no ves la interfaz, encapsula el código en una función main().")
    finally:
        sys.path = original_sys_path

else:
    # Interfaz integrada
    st.warning("Módulo externo 'Generación de Minutas' no encontrado. Usando interfaz integrada.")
    
    # Sección de mejora con AI
    if is_openai_available():
        enhanced_content, transcription = render_ai_enhancement_section()
        
        if enhanced_content:
            st.markdown("### Contenido Generado por AI")
            st.markdown(enhanced_content)
            st.markdown("---")
    
    # Formulario principal
    st.subheader("Información de la Reunión")
    
    col1, col2 = st.columns(2)
    
    with col1:
        titulo = st.text_input("Título de la reunión", value="Reunión de Equipo")
        fecha_reunion = st.date_input("Fecha de la reunión", value=date.today())
        objetivos = st.text_area("Objetivos de la reunión", height=100)
    
    with col2:
        # Participantes
        st.markdown("### Participantes")
        participantes_text = st.text_area(
            "Lista de participantes (uno por línea)",
            height=100,
            placeholder="Juan Pérez\nMaría García\nCarlos López"
        )
        
        # Convertir a DataFrame si hay participantes
        attendees = None
        if participantes_text.strip():
            nombres = [nombre.strip() for nombre in participantes_text.split('\n') if nombre.strip()]
            if nombres:
                attendees = pd.DataFrame({"Nombre": nombres})
    
    # Resumen
    st.subheader("Resumen de la Reunión")
    resumen = st.text_area("Resumen de los puntos discutidos", height=150)
    
    # Acuerdos y tareas
    st.subheader("Acuerdos y Tareas")
    action_items = dynamic_action_items()
    
    # Configuración de salida
    col1, col2 = st.columns(2)
    
    with col1:
        formato = st.selectbox("Formato de salida", ["docx", "md"])
    
    with col2:
        nombre_archivo = st.text_input("Nombre del archivo", value="minuta_reunion")
    
    # Generar minuta
    if st.button("Generar Minuta", type="primary"):
        if titulo and resumen:
            try:
                # Crear directorio de salida
                output_dir = Path("outputs")
                output_dir.mkdir(exist_ok=True)
                
                # Generar archivo
                output_path = output_dir / f"{nombre_archivo}.{formato}"
                
                success = generate_minutes(
                    title=titulo,
                    date=fecha_reunion,
                    objectives=objetivos,
                    summary=resumen,
                    attendees=attendees,
                    action_items=action_items,
                    output_path=output_path,
                    output_format=formato
                )
                
                if success:
                    st.success("Minuta generada exitosamente")
                    
                    # Mostrar contenido si es markdown
                    if formato == "md" and output_path.exists():
                        st.markdown("### Vista previa:")
                        content = output_path.read_text(encoding="utf-8")
                        st.markdown(content)
                        
                        # Botón de descarga
                        st.download_button(
                            label="Descargar Minuta",
                            data=content,
                            file_name=f"{nombre_archivo}.md",
                            mime="text/markdown"
                        )
                    else:
                        st.info(f"Archivo generado: {output_path}")
                else:
                    st.error("Error al generar la minuta")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Por favor completa al menos el título y resumen")

# Información adicional
st.markdown("---")
st.markdown("### Características")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Formatos Soportados**
    - Microsoft Word (DOCX)
    - Markdown (MD)
    """)

with col2:
    st.markdown("""
    **Funciones AI**
    - Extracción automática de objetivos
    - Generación de resumen
    - Identificación de tareas
    """)

with col3:
    st.markdown("""
    **Características**
    - Lista de participantes
    - Acuerdos y compromisos
    - Exportación múltiple
    """)
