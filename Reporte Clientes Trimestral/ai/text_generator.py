# ai/text_generator.py

import os
from typing import Dict, List

from config import (
    ENABLE_AI_GENERATION,
    AI_MODEL_NAME,
    AI_TEMPERATURE,
    AI_MAX_TOKENS
)
from rt_utils.placeholders import empty_payload_for_client

try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False


# ============================================================
# Prompt builder
# ============================================================

def build_prompt(cliente: dict, noticias: List[Dict], periodo: str) -> str:
    """
    Construye un prompt controlado y estructurado.
    """

    noticias_txt = ""
    for n in noticias:
        noticias_txt += f"- {n.get('titular')} ({n.get('fuente')})\n"

    prompt = f"""
Eres un analista senior de consultoría estratégica.

Cliente: {cliente.get('name')}
Sector: {cliente.get('sector')}
Periodo: {periodo}

Descripción base:
{cliente.get('description_hint', '')}

Noticias recientes:
{noticias_txt if noticias_txt else "No hay noticias relevantes."}

Genera:
1. Una descripción breve del cliente.
2. Tres hallazgos estratégicos del trimestre.
3. Tres KPIs estratégicos relevantes.
4. Tres oportunidades de colaboración para UBIMIA.

Responde en español, de forma ejecutiva y concisa.
"""
    return prompt.strip()


# ============================================================
# AI generation
# ============================================================

def generate_client_text(
    cliente: dict,
    noticias: List[Dict],
    periodo: str
) -> Dict:
    """
    Devuelve un payload listo para los placeholders.
    """

    # Base segura (modo manual / demo)
    payload = empty_payload_for_client(cliente.get("name"))

    # Si AI no está habilitado o no hay SDK
    if not ENABLE_AI_GENERATION or not _OPENAI_AVAILABLE:
        return payload

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return payload

    try:
        client = OpenAI(api_key=api_key)

        prompt = build_prompt(cliente, noticias, periodo)

        response = client.chat.completions.create(
            model=AI_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=AI_TEMPERATURE,
            max_tokens=AI_MAX_TOKENS
        )

        text = response.choices[0].message.content.strip()

        # Parsing simple (deliberadamente conservador)
        lines = [l.strip("- ").strip() for l in text.split("\n") if l.strip()]

        payload["DESCRIPCION_CLIENTE"] = lines[0] if len(lines) > 0 else ""
        payload["HALLAZGO_1"] = lines[1] if len(lines) > 1 else ""
        payload["HALLAZGO_2"] = lines[2] if len(lines) > 2 else ""
        payload["HALLAZGO_3"] = lines[3] if len(lines) > 3 else ""

        payload["KPI_1"] = lines[4] if len(lines) > 4 else ""
        payload["KPI_2"] = lines[5] if len(lines) > 5 else ""
        payload["KPI_3"] = lines[6] if len(lines) > 6 else ""

        payload["OPORTUNIDAD_1"] = lines[7] if len(lines) > 7 else ""
        payload["OPORTUNIDAD_2"] = lines[8] if len(lines) > 8 else ""
        payload["OPORTUNIDAD_3"] = lines[9] if len(lines) > 9 else ""

        return payload

    except Exception:
        # Fail-safe absoluto
        return payload
