from llm import chat

MAP_MODEL = "gpt-4o-mini"
REDUCE_MODEL = "gpt-4o"
CHECK_MODEL = "gpt-4o"

MAP_PROMPT = """Eres un asistente que resume transcripciones de reuniones.
Devuelve JSON con claves EXACTAS: puntos_clave[], decisiones[], acuerdos[], tareas[], riesgos[].
Cada tarea debe tener: descripcion, responsable(opcional), fecha(opcional), metrica(opcional).
Texto:
---
{texto}
---"""

REDUCE_PROMPT = """Integra listas de varios bloques (JSONs), deduplica y estandariza.
Exige tareas SMART; si falta responsable/fecha/metrica, marca “Pendiente”/“Proponer”.
Devuelve JSON con claves: resumen, decisiones[], acuerdos[], tareas[], riesgos[], proximos_pasos[].
Entrada (lista de JSON parciales):
{jsons}
"""

CHECK_PROMPT = """Revisa contradicciones, fechas imposibles y tareas sin verbo de acción.
Corrige mínimamente y devuelve el MISMO JSON con estructura final para minuta:
{json_entrada}"""

def map_blocks(blocks: list[str], model: str = MAP_MODEL) -> list[str]:
    outs = []
    for b in blocks:
        msg = [{"role": "user", "content": MAP_PROMPT.format(texto=b)}]
        outs.append(chat(model, msg, temperature=0.2))
    return outs

def reduce_summaries(mapped_jsons: list[str], model: str = REDUCE_MODEL) -> str:
    msg = [{"role":"user","content": REDUCE_PROMPT.format(jsons=mapped_jsons)}]
    return chat(model, msg, temperature=0.2)

def consistency_check(json_text: str, model: str = CHECK_MODEL) -> str:
    msg = [{"role":"user","content": CHECK_PROMPT.format(json_entrada=json_text)}]
    return chat(model, msg, temperature=0.1)
