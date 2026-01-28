# 1to1/src/logic.py

import json
from datetime import date
from typing import List, Dict, Any, Optional

import pandas as pd

try:
    # Opcional: solo se usará si activas el uso de la API
    from openai import OpenAI
except ImportError:
    OpenAI = None  # para no romper si no está instalada la librería


ESTADOS_ABIERTOS = ["pendiente", "reprogramado"]


def obtener_historial_participante(
    historial_df: pd.DataFrame,
    id_participante: str,
    n_ultimas: int = 3,
) -> pd.DataFrame:
    filtro = historial_df[historial_df["id_participante"] == id_participante].copy()
    if filtro.empty:
        return filtro
    filtro = filtro.sort_values("fecha_reunion", ascending=False)
    return filtro.head(n_ultimas)


def extraer_compromisos_abiertos(
    historial_df: pd.DataFrame,
    id_participante: str,
) -> List[Dict[str, Any]]:
    """
    Recorre todo el historial del participante y regresa
    una lista de compromisos con estado en ESTADOS_ABIERTOS.
    """
    abiertos: List[Dict[str, Any]] = []
    subset = historial_df[historial_df["id_participante"] == id_participante]

    for _, row in subset.iterrows():
        comp_str = row.get("compromisos")
        if not comp_str or pd.isna(comp_str):
            continue
        try:
            comp_list = json.loads(comp_str)
        except json.JSONDecodeError:
            continue
        for c in comp_list:
            if c.get("estado") in ESTADOS_ABIERTOS:
                abiertos.append(c)
    return abiertos


def generar_preparacion_basica(
    objetivos_anuales: str,
    fortalezas: Optional[str],
    oportunidades: Optional[str],
    resumen_historial: str,
    compromisos_abiertos: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Genera preguntas e insight de coaching sin usar la API de ChatGPT.
    Sirve como fallback o modo offline.
    """
    preguntas: List[str] = []

    preguntas.append("¿Cómo sientes tu avance frente a tus objetivos anuales en este último mes?")
    if objetivos_anuales:
        preguntas.append("De tus objetivos anuales, ¿cuál consideras prioritario para este mes y por qué?")

    if fortalezas:
        preguntas.append("¿Qué fortaleza crees que has aprovechado mejor recientemente?")
    if oportunidades:
        preguntas.append("¿En qué área te gustaría enfocarte para mejorar durante el próximo mes?")

    if compromisos_abiertos:
        preguntas.append("Revisemos los compromisos pendientes: ¿qué bloqueos han surgido y cómo podemos resolverlos?")

    preguntas.append("¿Hay algo que no estemos viendo o hablando que sea importante para ti en este momento?")

    insight = (
        "Reflexión: El seguimiento constante a tus objetivos y compromisos es lo que "
        "transforma buenas intenciones en progreso real. Esta reunión es un espacio para "
        "alinear expectativas, reducir fricciones y reforzar tu crecimiento profesional."
    )

    return {
        "preguntas": preguntas,
        "insight": insight,
    }


def generar_preparacion_con_chatgpt(
    objetivos_anuales: str,
    fortalezas: Optional[str],
    oportunidades: Optional[str],
    resumen_historial: str,
    compromisos_abiertos: List[Dict[str, Any]],
    modelo: str = "gpt-4.1-mini",
) -> Dict[str, Any]:
    """
    EJEMPLO opcional con API de ChatGPT (OpenAI).
    Solo se usará si OpenAI está disponible y el usuario lo activa explícitamente.
    """
    if OpenAI is None:
        return generar_preparacion_basica(
            objetivos_anuales, fortalezas, oportunidades, resumen_historial, compromisos_abiertos
        )

    client = OpenAI()  # requiere OPENAI_API_KEY en el entorno

    prompt = f"""
Eres un coach ejecutivo. Te doy contexto de un colaborador:

Objetivos anuales:
{objetivos_anuales or 'No especificados'}

Fortalezas:
{fortalezas or 'No especificadas'}

Oportunidades de mejora:
{oportunidades or 'No especificadas'}

Resumen de reuniones previas:
{resumen_historial or 'Sin historial previo'}

Compromisos abiertos:
{json.dumps(compromisos_abiertos, ensure_ascii=False, indent=2) if compromisos_abiertos else 'Sin compromisos abiertos'}

1) Genera entre 5 y 8 preguntas poderosas para una reunión 1:1 este mes.
2) Escribe una reflexión/insight breve (máx. 2 párrafos) en tono coaching y constructivo.

Devuélvelo en JSON con claves:
- "preguntas": lista de strings
- "insight": string
"""

    resp = client.responses.create(
        model=modelo,
        input=prompt,
        response_format={"type": "json_object"},
    )

    # Dependiendo de la versión del cliente, ajusta esta lectura.
    # Aquí asumimos que el contenido viene como texto plano JSON.
    raw_text = resp.output[0].content[0].text  # puede requerir ajuste según versión
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        return generar_preparacion_basica(
            objetivos_anuales, fortalezas, oportunidades, resumen_historial, compromisos_abiertos
        )

    preguntas = data.get("preguntas") or []
    insight = data.get("insight") or ""

    if not preguntas:
        return generar_preparacion_basica(
            objetivos_anuales, fortalezas, oportunidades, resumen_historial, compromisos_abiertos
        )

    return {
        "preguntas": preguntas,
        "insight": insight,
    }


def generar_preparacion(
    objetivos_anuales: str,
    fortalezas: Optional[str],
    oportunidades: Optional[str],
    historial_participante: pd.DataFrame,
    compromisos_abiertos: List[Dict[str, Any]],
    usar_chatgpt: bool = False,
) -> Dict[str, Any]:
    """
    Orquestador: decide si llama a la versión básica o a ChatGPT.
    """
    resumen_historial = ""
    if not historial_participante.empty:
        partes = []
        for _, row in historial_participante.iterrows():
            f = row.get("fecha_reunion", "")
            nota = row.get("notas_reunion", "")
            if isinstance(nota, str):
                nota_res = nota[:150] + ("..." if len(nota) > 150 else "")
            else:
                nota_res = ""
            partes.append(f"- {f}: {nota_res}")
        resumen_historial = "\n".join(partes)

    if usar_chatgpt:
        return generar_preparacion_con_chatgpt(
            objetivos_anuales, fortalezas, oportunidades, resumen_historial, compromisos_abiertos
        )
    else:
        return generar_preparacion_basica(
            objetivos_anuales, fortalezas, oportunidades, resumen_historial, compromisos_abiertos
        )


def hoy_str() -> str:
    return date.today().strftime("%Y-%m-%d")
