# utils/validators.py

from rt_utils.placeholders import GLOBAL_PLACEHOLDERS, CLIENT_PLACEHOLDERS


# ============================================================
# Validaciones globales
# ============================================================

def validate_global_payload(payload: dict):
    """
    Valida información global del reporte
    """
    errors = []

    if not payload.get("PERIODO"):
        errors.append("El PERIODO del reporte es obligatorio.")

    if not payload.get("LISTA_CLIENTES"):
        errors.append("La LISTA_CLIENTES no puede estar vacía.")

    if not payload.get("REPORT_TITLE"):
        errors.append("El REPORT_TITLE es obligatorio.")

    return errors


# ============================================================
# Validaciones por cliente
# ============================================================

def validate_client_payload(client_payload: dict):
    """
    Valida la información mínima requerida por cliente
    """
    errors = []

    if not client_payload.get("CLIENTE"):
        errors.append("El nombre del CLIENTE es obligatorio.")

    # Campos críticos mínimos
    required_fields = [
        "DESCRIPCION_CLIENTE",
        "HALLAZGO_1",
        "KPI_1",
        "OPORTUNIDAD_1"
    ]

    for field in required_fields:
        if not client_payload.get(field):
            errors.append(
                f"El campo '{field}' es obligatorio para el cliente {client_payload.get('CLIENTE')}"
            )

    return errors


# ============================================================
# Validación completa del reporte
# ============================================================

def validate_full_payload(global_payload: dict, clients_payload: list):
    """
    Valida todo el contenido antes de generar el PPT
    """
    errors = []

    errors.extend(validate_global_payload(global_payload))

    if not clients_payload:
        errors.append("Debe existir al menos un cliente en el reporte.")
        return errors

    for client in clients_payload:
        errors.extend(validate_client_payload(client))

    return errors
