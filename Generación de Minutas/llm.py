# llm.py
import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()

DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# Precios solo para estimación en UI (no se usan en demo)
PRICES = {
    "gpt-4o-mini": {"in": 0.15, "out": 0.60},
    "gpt-4o": {"in": 2.50, "out": 10.00},
}

def count_tokens(text: str, model_encoding: str = "o200k_base") -> int:
    try:
        enc = tiktoken.get_encoding(model_encoding)
    except Exception:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text or ""))

def estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    p = PRICES.get(model, {"in": 0.0, "out": 0.0})
    return (input_tokens/1e6)*p["in"] + (output_tokens/1e6)*p["out"]

def chat(model: str, messages: list, temperature: float = 0.2) -> str:
    """
    En DEMO_MODE (o sin API key) NO llama a OpenAI.
    Devuelve JSON de ejemplo suficiente para que la UI funcione.
    """
    # Si no hay clave o estamos en demo, retornamos mocks
    if DEMO_MODE or not os.getenv("OPENAI_API_KEY"):
        content = (messages[0].get("content") or "").lower()

        # Reduce/Check piden estructura final
        if "claves: resumen" in content or "estructura final" in content:
            return (
                '{'
                '"resumen":"(DEMO) Reunión de seguimiento. Se revisaron avances, riesgos y próximos pasos.",'
                '"decisiones":[{"texto":"Aprobar piloto","responsable":"Líder de proyecto","impacto":"Alto"}],'
                '"acuerdos":[{"texto":"Entregar reporte semanal","responsable":"Analista","fecha":"2025-11-01"}],'
                '"tareas":[{"descripcion":"Configurar tablero","responsable":"BI","fecha_objetivo":"2025-11-03","metrica":"Dashboard operativo visible"}],'
                '"riesgos":[{"texto":"Retraso de datos","prob":"Media","impacto":"Alto","mitigacion":"Plan B de fuente","dueno":"Datos"}],'
                '"proximos_pasos":[{"texto":"Convocar a comité","dueno":"PMO","fecha":"2025-11-04"}]'
                '}'
            )
        # Map por bloque
        return (
            '{'
            '"puntos_clave":["(DEMO) Revisión general","(DEMO) Definición de tareas"],'
            '"decisiones":[{"texto":"Continuar con sprint 2"}],'
            '"acuerdos":[{"texto":"Compartir minutas","responsable":"PM"}],'
            '"tareas":[{"descripcion":"Preparar dataset inicial"}],'
            '"riesgos":[{"texto":"Disponibilidad de APIs"}]'
            '}'
        )

    # Modo real: solo si hay API key
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
    return resp.choices[0].message.content
