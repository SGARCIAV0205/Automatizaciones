# app.py

import streamlit as st
import os
from pathlib import Path

from config import (
    SUPPORTED_PERIODS,
    PPT_TEMPLATE_PATH,
    OUTPUT_DIR,
    REPORT_TITLE_DEFAULT,
    ENABLE_AI_GENERATION
)

from rt_utils.client_store import load_clients, add_client
from rt_utils.placeholders import empty_payload_for_client
from rt_utils.validators import validate_full_payload
from rt_ingest.news_fetcher import fetch_news
from ai.text_generator import generate_client_text
from rt_render.ppt_writer import generate_ppt


# ============================================================
# Helpers AI (estimación de costo)
# ============================================================

def estimate_ai_cost(num_clients: int, avg_news_per_client: int = 3):
    """
    Estimación conservadora de costo de uso de ChatGPT.
    Suposiciones:
    - ~600 tokens input + ~400 output por cliente
    - GPT-4o-mini (aprox USD 0.00015 / 1K tokens)
    """
    tokens_por_cliente = 1000
    total_tokens = num_clients * tokens_por_cliente

    costo_por_1k = 0.00015
    costo_estimado = (total_tokens / 1000) * costo_por_1k

    return total_tokens, round(costo_estimado, 4)


# ============================================================
# Main
# ============================================================

def main():

    # --------------------------------------------------------
    # Configuración básica
    # --------------------------------------------------------
    st.set_page_config(
        page_title="Reporte Trimestral de Clientes",
        layout="wide"
    )
    
    st.title("Reporte Trimestral de Clientes Estratégicos")
    st.markdown(
        """
        Este módulo permite generar reportes trimestrales en PowerPoint
        a partir de una plantilla corporativa, con generación manual
        o asistida por ChatGPT.
        """
    )

    # --------------------------------------------------------
    # Carga de clientes base
    # --------------------------------------------------------
    clientes_catalogo = load_clients()
    clientes_nombres = [c["name"] for c in clientes_catalogo]

    # --------------------------------------------------------
    # Parámetros globales
    # --------------------------------------------------------
    st.subheader("Parámetros del Reporte")

    col1, col2 = st.columns(2)

    with col1:
        periodo = st.selectbox(
            "Periodo del reporte",
            SUPPORTED_PERIODS,
            key="periodo_reporte"
        )

    with col2:
        report_title = st.text_input(
            "Título del reporte",
            value=REPORT_TITLE_DEFAULT,
            key="titulo_reporte"
        )

    # --------------------------------------------------------
    # Selección de clientes
    # --------------------------------------------------------
    st.subheader("Clientes incluidos en el reporte")

    clientes_seleccionados = st.multiselect(
        "Selecciona los clientes",
        options=clientes_nombres,
        key="clientes_seleccionados"
    )

    # --------------------------------------------------------
    # Agregar nuevo cliente
    # --------------------------------------------------------
    with st.expander("Agregar nuevo cliente"):
        new_name = st.text_input("Nombre del cliente", key="nuevo_cliente_nombre")
        new_sector = st.text_input("Sector (opcional)", key="nuevo_cliente_sector")
        new_keywords = st.text_input(
            "Keywords para noticias (separadas por coma)",
            key="nuevo_cliente_keywords"
        )

        if st.button("Agregar cliente", key="btn_agregar_cliente"):
            if new_name:
                client_data = {
                    "name": new_name,
                    "sector": new_sector,
                    "keywords": [k.strip() for k in new_keywords.split(",") if k.strip()]
                }
                clientes_catalogo = add_client(client_data)
                st.success("Cliente agregado correctamente.")
            else:
                st.warning("El nombre del cliente es obligatorio.")

    # --------------------------------------------------------
    # Modo de generación
    # --------------------------------------------------------
    st.subheader("Modo de generación de contenido")

    ai_disponible = ENABLE_AI_GENERATION and bool(os.getenv("OPENAI_API_KEY"))

    modo = st.radio(
        "Selecciona el modo",
        options=["Manual", "AI"] if ai_disponible else ["Manual"],
        horizontal=True,
        key="modo_generacion"
    )

    if ENABLE_AI_GENERATION and not ai_disponible:
        st.info(
            "El modo ChatGPT está habilitado en configuración, "
            "pero no se detectó una API key de OpenAI. "
            "Se utilizará el modo Manual."
        )

    # --------------------------------------------------------
    # Estimación de costo AI
    # --------------------------------------------------------
    if modo == "AI" and clientes_seleccionados:
        total_tokens, costo_estimado = estimate_ai_cost(len(clientes_seleccionados))

        st.markdown("### Estimación de uso de ChatGPT")
        st.write(f"- Clientes: {len(clientes_seleccionados)}")
        st.write(f"- Tokens estimados: {total_tokens:,}")
        st.write(f"- Costo aproximado: **USD {costo_estimado}**")

    # --------------------------------------------------------
    # Contenido por cliente
    # --------------------------------------------------------
    clients_payload = []

    st.subheader("Contenido por cliente")

    for cliente_nombre in clientes_seleccionados:

        cliente_data = next(
            c for c in clientes_catalogo if c["name"] == cliente_nombre
        )

        with st.expander(f"Cliente: {cliente_nombre}", expanded=False):

            noticias = fetch_news(cliente_data, periodo)

            if modo == "AI":
                payload = generate_client_text(
                    cliente=cliente_data,
                    noticias=noticias,
                    periodo=periodo
                )
            else:
                payload = empty_payload_for_client(cliente_nombre)

            payload["CLIENTE"] = cliente_nombre

            payload["DESCRIPCION_CLIENTE"] = st.text_area(
                "Descripción del cliente",
                value=payload.get("DESCRIPCION_CLIENTE", ""),
                height=80,
                key=f"{cliente_nombre}_DESCRIPCION_CLIENTE"
            )

            st.markdown("**Hallazgos del trimestre**")
            payload["HALLAZGO_1"] = st.text_input(
                "Hallazgo 1",
                value=payload.get("HALLAZGO_1", ""),
                key=f"{cliente_nombre}_HALLAZGO_1"
            )
            payload["HALLAZGO_2"] = st.text_input(
                "Hallazgo 2",
                value=payload.get("HALLAZGO_2", ""),
                key=f"{cliente_nombre}_HALLAZGO_2"
            )
            payload["HALLAZGO_3"] = st.text_input(
                "Hallazgo 3",
                value=payload.get("HALLAZGO_3", ""),
                key=f"{cliente_nombre}_HALLAZGO_3"
            )

            st.markdown("**KPIs clave**")
            payload["KPI_1"] = st.text_input(
                "KPI 1",
                value=payload.get("KPI_1", ""),
                key=f"{cliente_nombre}_KPI_1"
            )
            payload["KPI_2"] = st.text_input(
                "KPI 2",
                value=payload.get("KPI_2", ""),
                key=f"{cliente_nombre}_KPI_2"
            )
            payload["KPI_3"] = st.text_input(
                "KPI 3",
                value=payload.get("KPI_3", ""),
                key=f"{cliente_nombre}_KPI_3"
            )

            st.markdown("**Oportunidades para UBIMIA**")
            payload["OPORTUNIDAD_1"] = st.text_input(
                "Oportunidad 1",
                value=payload.get("OPORTUNIDAD_1", ""),
                key=f"{cliente_nombre}_OPORTUNIDAD_1"
            )
            payload["OPORTUNIDAD_2"] = st.text_input(
                "Oportunidad 2",
                value=payload.get("OPORTUNIDAD_2", ""),
                key=f"{cliente_nombre}_OPORTUNIDAD_2"
            )
            payload["OPORTUNIDAD_3"] = st.text_input(
                "Oportunidad 3",
                value=payload.get("OPORTUNIDAD_3", ""),
                key=f"{cliente_nombre}_OPORTUNIDAD_3"
            )

            if noticias:
                st.markdown("**Noticias detectadas**")
                for i, n in enumerate(noticias[:2], start=1):
                    payload[f"FECHA_{i}"] = str(n.get("fecha", ""))
                    payload[f"TITULAR_{i}"] = n.get("titular", "")
                    payload[f"FUENTE_{i}"] = n.get("fuente", "")

                    st.markdown(f"- {n.get('titular')} ({n.get('fuente')})")

            clients_payload.append(payload)

    # --------------------------------------------------------
    # Generación del reporte
    # --------------------------------------------------------
    st.subheader("Generar reporte")

    if st.button("Generar PowerPoint", key="btn_generar_ppt"):

        global_payload = {
            "PERIODO": periodo,
            "LISTA_CLIENTES": ", ".join(clientes_seleccionados),
            "REPORT_TITLE": report_title
        }

        errors = validate_full_payload(global_payload, clients_payload)

        if errors:
            st.error("Existen errores en el reporte:")
            for e in errors:
                st.write(f"- {e}")
        else:
            output_name = f"Reporte_Clientes_UBIMIA_{periodo.replace(' ', '_')}.pptx"
            output_path = OUTPUT_DIR / output_name

            generate_ppt(
                global_payload=global_payload,
                clients_payload=clients_payload,
                template_path=PPT_TEMPLATE_PATH,
                output_path=output_path
            )

            st.success("Reporte generado correctamente.")
            st.download_button(
                label="Descargar PowerPoint",
                data=open(output_path, "rb"),
                file_name=output_name,
                key="download_ppt"
            )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()
