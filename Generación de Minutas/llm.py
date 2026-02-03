# llm.py
import os
import streamlit as st
import tiktoken

# Detectar si estamos en modo demo
def is_demo_mode():
    # Verificar si hay API key disponible
    api_key = None
    
    # Intentar obtener desde Streamlit secrets primero
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except (AttributeError, FileNotFoundError):
        # Fallback a variables de entorno
        api_key = os.getenv("OPENAI_API_KEY")
    
    # Si no hay API key, usar modo demo
    return not bool(api_key)

DEMO_MODE = is_demo_mode()

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
    Función de chat que usa la API key configurada en Streamlit secrets o variables de entorno.
    Si no hay API key disponible, usa modo demo.
    """
    # Obtener API key
    api_key = None
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except (AttributeError, FileNotFoundError):
        api_key = os.getenv("OPENAI_API_KEY")
    
    # Si no hay clave, usar modo demo
    if not api_key:
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

    # Modo real: usar API key disponible
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model, 
            messages=messages, 
            temperature=temperature
        )
        return resp.choices[0].message.content
    except Exception as e:
        st.error(f"Error con OpenAI API: {e}")
        # Fallback a modo demo si hay error
        return '{"resumen":"Error al conectar con OpenAI. Usando modo demo.","decisiones":[],"acuerdos":[],"tareas":[],"riesgos":[],"proximos_pasos":[]}'
