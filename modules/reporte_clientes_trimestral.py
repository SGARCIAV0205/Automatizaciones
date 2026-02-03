# modules/reporte_clientes_trimestral.py

import sys
from pathlib import Path
import streamlit as st


def find_automatizaciones_root(start: Path) -> Path | None:
    """
    Sube en el árbol de directorios hasta encontrar la carpeta 'Automatizaciones'.
    """
    current = start.resolve()
    for _ in range(10):  # límite de seguridad
        if current.name.lower() == "automatizaciones":
            return current
        if current.parent == current:
            break
        current = current.parent
    return None


def run_reporte_clientes_trimestral():
    """
    Adaptador para ejecutar el módulo standalone
    'REPORTE CLIENTES TRIMESTRAL' desde el Asistente Virtual.
    """

    # --------------------------------------------------
    # 1) Encontrar raíz real 'Automatizaciones'
    # --------------------------------------------------
    automatizaciones_root = find_automatizaciones_root(Path(__file__))

    if automatizaciones_root is None:
        st.error(
            "No se pudo localizar la carpeta raíz 'Automatizaciones'. "
            "Revisa la estructura del proyecto."
        )
        st.stop()

    modulo_root = automatizaciones_root / "Reporte Clientes Trimestral"

    if not modulo_root.exists():
        st.error(
            f"No se encontró el módulo 'Reporte Clientes Trimestral' en:\n"
            f"{automatizaciones_root}"
        )
        st.stop()

    # Verificar que existe el archivo app.py
    app_path = modulo_root / "app.py"
    if not app_path.exists():
        st.error(
            f"No se encontró 'app.py' en:\n"
            f"{modulo_root}"
        )
        st.stop()

    # --------------------------------------------------
    # 2) Ejecutar módulo real usando importlib para evitar conflictos de caché
    # --------------------------------------------------
    original_sys_path = list(sys.path)
    
    try:
        # Agregar las rutas necesarias para el módulo
        sys.path.insert(0, str(modulo_root))

        # Usar importlib con nombre único para evitar conflictos de caché
        import importlib.util
        spec = importlib.util.spec_from_file_location("reporte_clientes_app", app_path)
        reporte_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reporte_app)

        if not hasattr(reporte_app, "main"):
            st.error(
                "El archivo app.py del módulo 'Reporte Clientes Trimestral' "
                "no define una función main()."
            )
            st.stop()

        # Ejecutar la interfaz del reporte con skip_page_config=True
        reporte_app.main(skip_page_config=True)

    except ImportError as e:
        st.error(f"Error importando el módulo Reporte Clientes Trimestral: {e}")
        st.info("Verificando estructura de archivos...")
        
        # Debug info
        if st.checkbox("Mostrar información de debug - Reporte Clientes"):
            st.write(f"**Módulo root:** {modulo_root}")
            st.write(f"**App.py existe:** {app_path.exists()}")
            st.write(f"**Sys.path actual:** {sys.path[:3]}")
        
        st.stop()
        
    except Exception as e:
        st.error(f"Error ejecutando el módulo Reporte Clientes Trimestral: {e}")
        st.stop()
        
    finally:
        sys.path = original_sys_path


def render_ai_insights_section():
    """Renderizar sección de insights con AI para reportes de clientes"""
    try:
        from .openai_client import openai_client, is_openai_available
        
        if not is_openai_available():
            return None
        
        st.subheader("🤖 Insights con AI")
        st.info("Genera análisis automático de datos de clientes usando ChatGPT.")
        
        # Input de datos del cliente
        client_data = st.text_area(
            "Datos del cliente para análisis",
            height=150,
            placeholder="Ej: Ventas Q1: $50K, Q2: $75K, Q3: $60K. Productos: A, B, C. Feedback: Positivo en producto A...",
            help="Proporciona datos relevantes del cliente para generar insights"
        )
        
        # Tipo de análisis
        analysis_type = st.selectbox(
            "Tipo de análisis",
            ["Tendencias de crecimiento", "Análisis de riesgo", "Oportunidades de upselling", "Satisfacción del cliente"],
            help="Selecciona el enfoque del análisis"
        )
        
        if st.button("✨ Generar Insights", type="primary"):
            if not client_data.strip():
                st.warning("Por favor ingresa datos del cliente")
                return None
            
            with st.spinner("Generando insights con AI..."):
                insights, error = openai_client.generate_client_insights(client_data, analysis_type)
                
                if error:
                    st.error(f"Error al generar insights: {error}")
                    return None
                else:
                    st.success("✅ Insights generados con AI")
                    st.markdown("### 📊 Análisis Generado")
                    st.markdown(insights)
                    return insights
        
        return None
        
    except ImportError:
        return None
