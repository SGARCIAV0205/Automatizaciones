from typing import Dict, List
from datetime import date


def generate_demo_placeholder_map(placeholders: List[str], user_prompt: str = "") -> Dict[str, str]:
    today = date.today().strftime("%d/%m/%Y")

    base = {
        "TITULO": "Reporte Ejecutivo – Modo Demo",
        "SUBTITULO": "Documento generado sin conexión a OpenAI",
        "CLIENTE": "Cliente Demo",
        "FECHA": today,
        "AUTOR": "Template Writer",
        "RESUMEN_EJECUTIVO": (
            "Documento generado en modo demostración para validar el flujo: "
            "plantilla local → detección de placeholders → reemplazo → descarga."
        ),
    }

    out: Dict[str, str] = {}
    for k in placeholders:
        out[k] = base.get(k, f"Contenido demo para {k}.")

    if user_prompt.strip() and "CONTEXTO" in out:
        out["CONTEXTO"] = f"Prompt recibido (demo): {user_prompt.strip()[:240]}"

    return out
