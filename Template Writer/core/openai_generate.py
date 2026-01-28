import json
import os
from typing import Dict, List

from openai import OpenAI


def generate_placeholder_map(
    user_prompt: str,
    placeholders: List[str],
    model: str = "gpt-4o",
    temperature: float = 0.2,
    max_output_tokens: int = 1200,
) -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("Falta OPENAI_API_KEY en variables de entorno.")

    client = OpenAI(api_key=api_key)

    schema_hint = {k: "string" for k in placeholders}

    instructions = (
        "Eres un asistente que genera contenido para rellenar plantillas.\n"
        "Devuelve SOLO JSON válido (sin markdown), con exactamente estas llaves:\n"
        f"{placeholders}\n"
        "No inventes llaves nuevas. Si un campo no aplica, devuelve cadena vacía.\n"
        "Escribe en tono profesional y directo."
    )

    resp = client.responses.create(
        model=model,
        instructions=instructions,
        input=(
            "Completa los campos de una plantilla.\n\n"
            f"JSON shape esperado: {json.dumps(schema_hint, ensure_ascii=False)}\n\n"
            f"Solicitud del usuario:\n{user_prompt}"
        ),
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )

    raw = (resp.output_text or "").strip()
    if not raw:
        raise ValueError("La API no devolvió contenido.")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("La API no devolvió JSON válido.") from e

    missing = [k for k in placeholders if k not in data]
    extra = [k for k in data.keys() if k not in placeholders]
    if missing or extra:
        raise ValueError(f"JSON inválido. Missing={missing}, Extra={extra}")

    return {k: ("" if data[k] is None else str(data[k])) for k in placeholders}
