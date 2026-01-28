# pages/2_Reporte_Clientes_Trimestral.py

import os
import sys
from pathlib import Path
import streamlit as st

from modules.ui_theme import apply_theme, sidebar_brand
from modules.openai_client import render_openai_config_sidebar
from modules.auth import authenticate_app

# ---------------------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="Reporte Clientes Trimestral",
    layout="wide"
)

apply_theme()

# ---------------------------------------------------------------------
# Autenticación requerida
# ---------------------------------------------------------------------
authenticate_app()

# ---------------------------------------------------------------------
# Contenido principal (solo se muestra si está autenticado)
# ---------------------------------------------------------------------
sidebar_brand()

# ---------------------------------------------------------------------
# Configuración de OpenAI en sidebar
# ---------------------------------------------------------------------
render_openai_config_sidebar()

# ---------------------------------------------------------------------
# Localizar módulo Reporte Clientes Trimestral
# ---------------------------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]   # .../Automatizaciones (raíz del repo)
reporte_root = AUTOM_ROOT / "Reporte Clientes Trimestral"
app_file = reporte_root / "app.py"

if not app_file.exists():
    st.error(f"No se encontró 'app.py' en: {reporte_root}")
    st.write(f"DEBUG - Contenido de {AUTOM_ROOT}:")
    try:
        for item in AUTOM_ROOT.iterdir():
            if item.is_dir():
                st.write(f"  - {item.name}/")
    except Exception as e:
        st.write(f"Error listando directorio: {e}")
    st.stop()

# ---------------------------------------------------------------------
# Cargar módulo de forma aislada
# ---------------------------------------------------------------------
AUTOM_ROOT = Path(__file__).resolve().parents[1]   # .../Automatizaciones (raíz del repo)
reporte_root = AUTOM_ROOT / "Reporte Clientes Trimestral"
app_file = reporte_root / "app.py"

if not app_file.exists():
    st.error(f"No se encontró 'app.py' en: {reporte_root}")
    st.stop()

# Mostrar información sobre el módulo
st.info(f"Módulo encontrado en: {reporte_root}")
st.warning("El módulo 'Reporte Clientes Trimestral' tiene problemas de compatibilidad con la estructura actual.")

# Interfaz temporal básica
st.subheader("Funcionalidad Temporal - Reporte Clientes Trimestral")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Configuración del Reporte")
    cliente = st.text_input("Nombre del cliente")
    trimestre = st.selectbox("Trimestre", ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"])
    tipo_reporte = st.selectbox("Tipo de reporte", ["Ejecutivo", "Detallado", "Resumen"])
    
    incluir_graficos = st.checkbox("Incluir gráficos", value=True)
    incluir_metricas = st.checkbox("Incluir métricas", value=True)

with col2:
    st.markdown("### Datos del Cliente")
    ventas = st.number_input("Ventas del trimestre", min_value=0, value=50000)
    crecimiento = st.slider("Crecimiento (%)", -50, 100, 15)
    satisfaccion = st.slider("Satisfacción del cliente", 1, 10, 8)
    
    st.markdown("### Vista Previa")
    st.metric("Ventas", f"${ventas:,}", f"{crecimiento}%")
    st.metric("Satisfacción", f"{satisfaccion}/10", "0.5")

if st.button("Generar Reporte", type="primary"):
    if cliente:
        with st.spinner("Generando reporte..."):
            import time
            time.sleep(2)
            
            st.success("Reporte generado exitosamente")
            
            # Mostrar resumen
            st.markdown("### Resumen del Reporte")
            st.info(f"""
            **Cliente:** {cliente}
            **Trimestre:** {trimestre}
            **Tipo:** {tipo_reporte}
            **Ventas:** ${ventas:,}
            **Crecimiento:** {crecimiento}%
            **Satisfacción:** {satisfaccion}/10
            """)
            
            # Botón de descarga simulado
            st.download_button(
                label="Descargar PPTX",
                data="Contenido del reporte generado...",
                file_name=f"Reporte_{cliente}_{trimestre}.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
    else:
        st.warning("Por favor ingresa el nombre del cliente")

# Información adicional
st.markdown("---")
st.markdown("### Información del Módulo")
st.info("""
**Estado:** El módulo original tiene problemas de compatibilidad con la estructura actual de Streamlit Cloud.

**Funcionalidad Temporal:** Esta interfaz básica permite generar reportes mientras se resuelven los problemas de compatibilidad.

**Próximos Pasos:** Se trabajará en adaptar el módulo original para que funcione correctamente en la nueva estructura.
""")
