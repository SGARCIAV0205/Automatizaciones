# 1to1/src/data_io.py

from pathlib import Path
import pandas as pd

HISTORIAL_COLUMNS = [
    "id_participante",
    "fecha_reunion",
    "health_energia",
    "health_carga_trabajo",
    "health_alineacion_objetivos",
    "health_notas",
    "preguntas_generadas",
    "insight_coaching",
    "notas_reunion",
    "compromisos",
    "fecha_proxima_reunion",
]


def get_base_dir() -> Path:
    """
    Devuelve la ruta base del módulo 1to1.
    Asume que este archivo está en 1to1/src/.
    """
    return Path(__file__).resolve().parents[1]  # sube de src/ a 1to1/


def get_data_dir() -> Path:
    base_dir = get_base_dir()
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def load_participantes() -> pd.DataFrame:
    data_dir = get_data_dir()
    participantes_path = data_dir / "participantes.csv"
    if not participantes_path.exists():
        raise FileNotFoundError(
            f"No se encontró {participantes_path}. "
            "Asegúrate de crearlo con el formato definido."
        )
    df = pd.read_csv(participantes_path)
    if "id_participante" not in df.columns:
        raise ValueError("El archivo participantes.csv debe contener la columna 'id_participante'.")
    return df


def load_historial() -> pd.DataFrame:
    data_dir = get_data_dir()
    historial_path = data_dir / "historial_1to1.csv"

    if not historial_path.exists():
        # Crear DataFrame vacío con columnas definidas
        df = pd.DataFrame(columns=HISTORIAL_COLUMNS)
        df.to_csv(historial_path, index=False)
        return df

    df = pd.read_csv(historial_path, dtype=str)
    # Asegurar que todas las columnas existan
    for col in HISTORIAL_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df[HISTORIAL_COLUMNS]


def save_historial(historial_df: pd.DataFrame) -> None:
    data_dir = get_data_dir()
    historial_path = data_dir / "historial_1to1.csv"
    historial_df = historial_df[HISTORIAL_COLUMNS]
    historial_df.to_csv(historial_path, index=False)
