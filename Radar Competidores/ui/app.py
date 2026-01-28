# ui/app.py

import os
from pathlib import Path
import subprocess
import yaml
import streamlit as st

# Ruta base del proyecto (carpeta "Radar Competidores")
BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config.yaml"
REPORTS_OUT = BASE_DIR / "reports" / "out"


# ----------------- helpers -----------------
def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)


def run_pipeline():
    """
    Ejecuta `python -m src.run_pipeline` desde la raíz del proyecto.
    """
    result = subprocess.run(
        ["python", "-m", "src.run_pipeline"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )
    return result


def find_latest_report():
    if not REPORTS_OUT.exists():
        return None
    pptx_files = sorted(REPORTS_OUT.glob("reporte_radar_UBIMIA_auto_v3_*.pptx"))
    return pptx_files[-1] if pptx_files else None


# ----------------- UI -----------------
def main(skip_page_config=False):
    if not skip_page_config:
        st.set_page_config(
            page_title="Radar de Competidores",
            layout="wide",
        )

    cfg = load_config()

    # ============= SIDEBAR =============
    st.sidebar.header("Parámetros Radar Competidores")

    periodo = st.sidebar.text_input(
        "Periodo del reporte",
        value=cfg.get("periodo", "2025-11"),
        help="Formato recomendado: YYYY-MM",
    )

    # Modo DEMO: desactiva el uso de API LLM
    modo_demo = st.sidebar.checkbox(
        "Modo DEMO (sin API)",
        value=not cfg.get("use_llm", False),
    )
    use_llm = not modo_demo

    notas_globales = st.sidebar.text_area(
        "Notas globales para el reporte (opcional)",
        value=cfg.get("notas_globales", ""),
        height=120,
    )

    with st.sidebar.expander("Opcional: integración con ChatGPT", expanded=False):
        api_key = st.text_input(
            "OpenAI API Key (no se guarda en disco)",
            type="password",
            value="",
        )
        modelo_llm = st.text_input(
            "Modelo LLM",
            value=cfg.get("openai_model", "gpt-4.1-mini"),
        )

    # La API key solo vive en esta sesión
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    st.sidebar.markdown("---")
    guardar_cfg = st.sidebar.button("Guardar configuración")

    if guardar_cfg:
        # Actualizamos configuración
        cfg["periodo"] = periodo
        cfg["use_llm"] = bool(use_llm)
        cfg["openai_model"] = modelo_llm
        cfg["notas_globales"] = notas_globales
        save_config(cfg)
        st.sidebar.success("Configuración guardada.")

    # ============= CUERPO PRINCIPAL =============
    st.title("Radar de Competidores")

    st.markdown(
        """
Este módulo genera un **reporte ejecutivo en PPTX** con un radar competitivo, 
puntajes ponderados por eje y narrativa automática del desempeño frente a los principales jugadores del mercado.

- El reporte utiliza un **período de corte** (por ejemplo, un mes) definido en los parámetros del radar.
- Los **puntajes por eje** se construyen a partir de señales de noticias, integraciones y actividad competitiva.
- Puedes **editar la lista de competidores** y registrar notas cualitativas por empresa que, en versiones futuras,
  se podrán incorporar al reporte.
        """
    )

    st.markdown("---")
    st.subheader("Configuración de competidores")

    competitors_list = cfg.get("competitors", [])
    competitors_str = "\n".join(competitors_list) if competitors_list else ""

    st.markdown("**Listado de competidores incluidos en el radar** (uno por línea)")
    competitors_str_new = st.text_area(
        label="",
        value=competitors_str,
        height=120,
        help="Cada línea se interpreta como un competidor distinto.",
    )

    # Notas por competidor (opcional)
    st.markdown("**Notas por competidor (opcional)**")
    notes_by_comp = cfg.get("competitor_notes", {}) or {}

    # Actualizar lista provisional de competidores
    current_competitors = [
        c.strip() for c in competitors_str_new.splitlines() if c.strip()
    ]

    updated_notes = {}
    for comp in current_competitors:
        with st.expander(f"Competidor: {comp}", expanded=False):
            txt = st.text_area(
                f"Notas para {comp}",
                value=notes_by_comp.get(comp, ""),
                height=100,
            )
            updated_notes[comp] = txt

    st.markdown("---")

    # Botón grande de generación de reporte
    col_empty, col_btn = st.columns([3, 1])
    with col_btn:
        ejecutar = st.button("Generar reporte PPTX", use_container_width=True)

    log_text = ""

    if ejecutar:
        # Antes de ejecutar, actualizamos config con todos los parámetros actuales
        cfg["periodo"] = periodo
        cfg["use_llm"] = bool(use_llm)
        cfg["openai_model"] = modelo_llm
        cfg["notas_globales"] = notas_globales
        cfg["competitors"] = current_competitors
        cfg["competitor_notes"] = updated_notes
        save_config(cfg)

        st.info(f"Ejecutando pipeline para el periodo `{periodo}`...")
        result = run_pipeline()

        if result.returncode == 0:
            st.success("Pipeline ejecutado correctamente. El reporte PPTX ha sido generado.")
        else:
            st.error("Error al ejecutar el pipeline. Revisa el log para más detalles.")

        log_text = result.stdout + "\n\n" + result.stderr

    # Sección de descarga del último reporte
    st.markdown("### Último reporte generado")

    latest_report = find_latest_report()
    if latest_report and latest_report.exists():
        st.write(f"`{latest_report.name}`")
        with open(latest_report, "rb") as f:
            st.download_button(
                label="Descargar reporte PPTX",
                data=f.read(),
                file_name=latest_report.name,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
    else:
        st.warning("Aún no se ha generado ningún reporte en `reports/out/`.")

    # Log de ejecución
    if log_text:
        st.markdown("### Log de ejecución")
        st.code(log_text, language="bash")

    st.markdown("---")
    st.caption(
        "La configuración del radar (periodo, competidores, notas y parámetros LLM) "
        "se guarda en `config.yaml`. El uso de la API de ChatGPT es opcional; "
        "si el modo DEMO está activado, el pipeline ignora cualquier llamada a la API."
    )


if __name__ == "__main__":
    main()
