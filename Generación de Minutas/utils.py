# utils.py
import pandas as pd
from datetime import date

def load_participants_csv(file) -> list:
    """
    Carga un CSV con columnas: nombre, email, rol
    Devuelve una lista de diccionarios [{nombre, email, rol}, ...]
    """
    try:
        df = pd.read_csv(file)
        columnas = [c.lower().strip() for c in df.columns]
        if "nombre" not in columnas or "email" not in columnas:
            raise ValueError("El CSV debe contener las columnas: nombre y email (rol es opcional).")

        participantes = []
        for _, row in df.iterrows():
            participante = {
                "nombre": str(row.get("nombre", "")).strip(),
                "email": str(row.get("email", "")).strip(),
                "rol": str(row.get("rol", "")).strip() if "rol" in columnas else ""
            }
            participantes.append(participante)
        return participantes

    except Exception as e:
        print(f"Error al leer participantes: {e}")
        return []


def base_payload(proyecto: str, fecha: str, participantes: list) -> dict:
    """
    Estructura base del JSON de minuta.
    """
    return {
        "meta": {
            "proyecto": proyecto,
            "fecha": fecha or date.today().isoformat(),
        },
        "participantes": participantes or [],
        "resumen": "",
        "decisiones": [],
        "acuerdos": [],
        "tareas": [],
        "riesgos": [],
        "proximos_pasos": []
    }
