# pages/4_Reuniones_1to1.py

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
    page_title="Reuniones 1:1",
    layout="wide",
)

apply_theme()

# Autenticación requerida
authenticate_app()

# Contenido principal
sidebar_brand()
render_openai_config_sidebar()

# Título principal
st.title("Reuniones Mensuales 1:1")
st.markdown("Gestiona reuniones mensuales: historial, health-check, compromisos y preparación automática.")

# Buscar el módulo 1to1
AUTOM_ROOT = Path(__file__).resolve().parents[2]
reuniones_root = AUTOM_ROOT / "1to1"

if not reuniones_root.exists():
    st.warning("Módulo '1to1' no encontrado en la estructura del proyecto.")
    st.info("Ubicación esperada: " + str(reuniones_root))
    
    # Interfaz básica mientras tanto
    st.subheader("Funcionalidad en Desarrollo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Preparación de Reunión")
        empleado = st.text_input("Nombre del empleado")
        notas_previas = st.text_area("Notas de reuniones anteriores", height=100)
        
        if st.button("Generar Preparación con AI"):
            if empleado:
                from modules.openai_client import openai_client, is_openai_available
                
                if is_openai_available():
                    with st.spinner("Generando preparación..."):
                        preparacion, error = openai_client.improve_1to1_preparation(
                            f"Empleado: {empleado}", notas_previas
                        )
                        
                        if error:
                            st.error(f"Error: {error}")
                        else:
                            st.success("Preparación generada")
                            st.markdown("### Preparación Sugerida")
                            st.markdown(preparacion)
                else:
                    st.warning("Configura tu API key de OpenAI para usar esta función")
            else:
                st.warning("Por favor ingresa el nombre del empleado")
    
    with col2:
        st.markdown("### Health Check")
        satisfaccion = st.slider("Satisfacción laboral", 1, 10, 7)
        carga_trabajo = st.slider("Carga de trabajo", 1, 10, 6)
        desarrollo = st.slider("Oportunidades de desarrollo", 1, 10, 5)
        
        if st.button("Guardar Health Check"):
            st.success("Health check guardado")
            
        st.markdown("### Métricas")
        st.metric("Satisfacción Promedio", "7.2", "0.3")
        st.metric("Reuniones Este Mes", "3", "1")
        st.metric("Compromisos Pendientes", "2", "-1")

else:
    st.info("Cargando módulo completo de Reuniones 1:1...")
    # Aquí iría la carga del módulo real cuando esté disponible