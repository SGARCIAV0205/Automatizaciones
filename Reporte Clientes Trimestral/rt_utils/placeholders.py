# utils/placeholders.py

"""
Contrato de placeholders entre la plantilla PPTX y el sistema.
NO modificar nombres aquí sin modificar la plantilla.
"""

# ============================================================
# Placeholders globales (aplican a todo el reporte)
# ============================================================

GLOBAL_PLACEHOLDERS = {
    "PERIODO": "{PERIODO}",
    "LISTA_CLIENTES": "{LISTA_CLIENTES}",
    "REPORT_TITLE": "{{REPORT_TITLE}}"
}


# ============================================================
# Placeholders por cliente
# ============================================================

CLIENT_PLACEHOLDERS = {
    "CLIENTE": "{CLIENTE}",

    # Visión general
    "DESCRIPCION_CLIENTE": "{DESCRIPCION_CLIENTE}",

    # Hallazgos
    "HALLAZGO_1": "{HALLAZGO_1}",
    "HALLAZGO_2": "{HALLAZGO_2}",
    "HALLAZGO_3": "{HALLAZGO_3}",

    # KPIs
    "KPI_1": "{KPI_1}",
    "KPI_2": "{KPI_2}",
    "KPI_3": "{KPI_3}",

    # Noticias
    "FECHA_1": "{FECHA_1}",
    "TITULAR_1": "{TITULAR_1}",
    "FUENTE_1": "{FUENTE_1}",

    "FECHA_2": "{FECHA_2}",
    "TITULAR_2": "{TITULAR_2}",
    "FUENTE_2": "{FUENTE_2}",

    # Oportunidades
    "OPORTUNIDAD_1": "{OPORTUNIDAD_1}",
    "OPORTUNIDAD_2": "{OPORTUNIDAD_2}",
    "OPORTUNIDAD_3": "{OPORTUNIDAD_3}"
}


# ============================================================
# Helpers
# ============================================================

def all_placeholders():
    """
    Devuelve una lista plana de todos los placeholders válidos
    """
    return list(GLOBAL_PLACEHOLDERS.values()) + list(CLIENT_PLACEHOLDERS.values())


def empty_payload_for_client(cliente: str):
    """
    Genera un payload vacío inicial para un cliente.
    Útil para modo manual o demo sin API.
    """
    payload = {k: "" for k in CLIENT_PLACEHOLDERS.keys()}
    payload["CLIENTE"] = cliente
    return payload
