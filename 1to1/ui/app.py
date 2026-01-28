# 1to1/ui/app.py

import json
from datetime import date
from pathlib import Path
import sys

import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# Ajuste de ruta para poder importar data_io y logic desde src/
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]  # carpeta 1to1
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from data_io import load_participantes, load_historial, save_historial
from logic import (
    obtener_historial_participante,
    extraer_compromisos_abiertos,
    generar_preparacion,
    hoy_str,
)


def main() -> None:
    # ---------------------------------------------------
    # Configuración básica de la página
    # ---------------------------------------------------
    st.set_page_config(
        page_title="Seguimiento 1:1 Mensuales",
        layout="wide",
    )

    st.title("Seguimiento de 1:1 mensuales")

    st.markdown(
        """
Módulo para gestionar las reuniones 1:1 mensuales con tu equipo:
- Selecciona un participante desde la base de datos.
- Consulta sus objetivos e historial.
- Genera preguntas sugeridas e insight tipo coaching.
- Registra health-check, compromisos y próxima reunión.
"""
    )

    # ---------------------------------------------------
    # Carga de datos
    # ---------------------------------------------------
    try:
        participantes_df = load_participantes()
    except Exception as e:
        st.error(
            f"Error cargando participantes: {e}. "
            "Verifica que '1to1/data/participantes.csv' exista y tenga el formato correcto."
        )
        st.stop()

    historial_df = load_historial()

    # ---------------------------------------------------
    # Selección de participante
    # ---------------------------------------------------
    nombres = participantes_df["nombre"].tolist()
    nombre_sel = st.selectbox("Selecciona el participante", ["-- Selecciona --"] + nombres)

    if nombre_sel == "-- Selecciona --":
        st.stop()

    part_row = participantes_df[participantes_df["nombre"] == nombre_sel].iloc[0]
    id_participante = part_row["id_participante"]
    objetivos_anuales = part_row.get("objetivos_anuales", "")
    fortalezas = part_row.get("fortalezas", "")
    oportunidades = part_row.get("oportunidades", "")

    hist_part = obtener_historial_participante(historial_df, id_participante, n_ultimas=3)
    compromisos_abiertos = extraer_compromisos_abiertos(historial_df, id_participante)

    col_ficha, col_hist = st.columns([2, 3])

    # ---------------------------------------------------
    # Ficha del participante
    # ---------------------------------------------------
    with col_ficha:
        st.subheader("Ficha del participante")
        st.markdown(f"**Nombre:** {nombre_sel}")
        st.markdown(f"**Puesto:** {part_row.get('puesto', '')}")
        st.markdown(f"**Área:** {part_row.get('area', '')}")

        st.markdown("**Objetivos anuales:**")
        st.write(objetivos_anuales)

        if fortalezas:
            st.markdown("**Fortalezas:**")
            st.write(fortalezas)

        if oportunidades:
            st.markdown("**Oportunidades:**")
            st.write(oportunidades)

    # ---------------------------------------------------
    # Historial reciente
    # ---------------------------------------------------
    with col_hist:
        st.subheader("Historial reciente de 1:1")
        if hist_part.empty:
            st.info("No hay reuniones previas registradas para este participante.")
        else:
            for _, row in hist_part.iterrows():
                st.markdown(f"**Fecha:** {row.get('fecha_reunion', '')}")
                st.markdown(f"- Health energía: {row.get('health_energia', '')}")
                st.markdown(f"- Health carga de trabajo: {row.get('health_carga_trabajo', '')}")
                st.markdown(f"- Health alineación: {row.get('health_alineacion_objetivos', '')}")
                notas = row.get("notas_reunion", "")
                if isinstance(notas, str) and notas.strip():
                    resumen = notas[:200] + ("..." if len(notas) > 200 else "")
                    st.markdown(f"- Notas: {resumen}")
                st.markdown("---")

    # ---------------------------------------------------
    # Formulario de la reunión actual
    # ---------------------------------------------------
    st.markdown("---")
    st.header("Preparación y registro de la reunión actual")

    with st.form(key="form_1to1"):

        # ----------------- Preparación automática -----------------
        st.subheader("Preparación automática")

        usar_chatgpt = st.checkbox(
            "Usar API de ChatGPT para generar preguntas e insight (opcional)",
            value=False,
            help="Si no está activo, se usarán reglas internas para generar preguntas.",
        )

        prep = generar_preparacion(
            objetivos_anuales=objetivos_anuales,
            fortalezas=fortalezas,
            oportunidades=oportunidades,
            historial_participante=hist_part,
            compromisos_abiertos=compromisos_abiertos,
            usar_chatgpt=usar_chatgpt,
        )

        preguntas_text_default = "\n".join(f"- {p}" for p in prep["preguntas"])
        insight_default = prep["insight"]

        preguntas_text = st.text_area(
            "Preguntas sugeridas para esta 1:1 (puedes editarlas)",
            value=preguntas_text_default,
            height=200,
        )

        insight_text = st.text_area(
            "Insight / reflexión tipo coaching (puedes editarlo)",
            value=insight_default,
            height=150,
        )

        # ----------------- Health-check -----------------
        st.subheader("Health-check del mes")

        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            health_energia = st.slider("Energía / motivación", min_value=1, max_value=5, value=4)
        with col_h2:
            health_carga = st.slider("Carga de trabajo percibida", min_value=1, max_value=5, value=3)
        with col_h3:
            health_alineacion = st.slider("Alineación con objetivos", min_value=1, max_value=5, value=4)

        health_notas = st.text_area(
            "Comentarios breves sobre el mes (opcional)",
            value="",
            height=80,
        )

        # ----------------- Compromisos anteriores -----------------
        st.subheader("Compromisos de reuniones anteriores")

        compromisos_actualizados = []

        if compromisos_abiertos:
            st.markdown("Compromisos abiertos (pendientes / reprogramados):")
            for idx, c in enumerate(compromisos_abiertos):
                st.markdown(f"**Compromiso {idx+1}:** {c.get('descripcion', '')}")
                col_c1, col_c2 = st.columns([2, 1])
                with col_c1:
                    nuevo_estado = st.selectbox(
                        "Estado",
                        options=["pendiente", "cumplido", "no_cumplido", "reprogramado"],
                        index=["pendiente", "cumplido", "no_cumplido", "reprogramado"].index(
                            c.get("estado", "pendiente")
                        ),
                        key=f"estado_comp_{idx}",
                    )
                with col_c2:
                    due_str = c.get("due_date")
                    try:
                        y, m, d = [int(x) for x in str(due_str).split("-")]
                        due_default = date(y, m, d)
                    except Exception:
                        due_default = date.today()

                    nuevo_due = st.date_input(
                        "Due date",
                        value=due_default,
                        key=f"due_comp_{idx}",
                    )

                actualizado = {
                    **c,
                    "estado": nuevo_estado,
                    "due_date": nuevo_due.strftime("%Y-%m-%d"),
                }
                compromisos_actualizados.append(actualizado)
                st.markdown("---")
        else:
            st.info("No hay compromisos abiertos para este participante.")

        # ----------------- Nuevos compromisos -----------------
        st.subheader("Nuevos compromisos de esta reunión")

        nuevos_compromisos: list[dict] = []

        num_nuevos = st.number_input(
            "Número de nuevos compromisos a capturar",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
        )

        for i in range(num_nuevos):
            st.markdown(f"**Nuevo compromiso {i+1}**")
            desc = st.text_input(
                "Descripción",
                key=f"desc_nuevo_{i}",
            )
            responsable = st.selectbox(
                "Responsable",
                options=["colaborador", "manager", "ambos"],
                key=f"resp_nuevo_{i}",
            )
            due_nuevo = st.date_input(
                "Due date",
                value=date.today(),
                key=f"due_nuevo_{i}",
            )
            if desc.strip():
                nuevos_compromisos.append(
                    {
                        "descripcion": desc.strip(),
                        "responsable": responsable,
                        "due_date": due_nuevo.strftime("%Y-%m-%d"),
                        "estado": "pendiente",
                        "origen_fecha_reunion": hoy_str(),
                    }
                )
            st.markdown("---")

        # ----------------- Notas y próxima reunión -----------------
        st.subheader("Notas de la reunión y próxima fecha")

        notas_reunion = st.text_area(
            "Notas de la reunión",
            value="",
            height=150,
        )

        fecha_prox = st.date_input(
            "Fecha estimada de la próxima reunión",
            value=date.today(),
        )

        submitted = st.form_submit_button("Guardar reunión")

    # ---------------------------------------------------
    # Guardado de la reunión
    # ---------------------------------------------------
    if submitted:
        todas_comp = compromisos_actualizados + nuevos_compromisos

        nueva_fila = {
            "id_participante": id_participante,
            "fecha_reunion": hoy_str(),
            "health_energia": str(health_energia),
            "health_carga_trabajo": str(health_carga),
            "health_alineacion_objetivos": str(health_alineacion),
            "health_notas": health_notas,
            "preguntas_generadas": preguntas_text,
            "insight_coaching": insight_text,
            "notas_reunion": notas_reunion,
            "compromisos": json.dumps(todas_comp, ensure_ascii=False),
            "fecha_proxima_reunion": fecha_prox.strftime("%Y-%m-%d"),
        }

        # FIX pandas 2.0+: usar concat en vez de append
        historial_df = pd.concat(
            [historial_df, pd.DataFrame([nueva_fila])],
            ignore_index=True,
        )

        save_historial(historial_df)

        st.success("Reunión guardada correctamente.")


if __name__ == "__main__":
    main()
