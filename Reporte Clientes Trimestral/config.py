# config.py

from pathlib import Path

# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Crear carpeta de salida si no existe
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# Plantilla PPT
# ============================================================

PPT_TEMPLATE_NAME = "Plantilla_Reporte_Clientes_Estrategicos_UBIMIA.pptx"
PPT_TEMPLATE_PATH = TEMPLATES_DIR / PPT_TEMPLATE_NAME


# ============================================================
# Configuración general del reporte
# ============================================================

REPORT_TITLE_DEFAULT = "Reporte Trimestral de Clientes Estratégicos"
COMPANY_NAME = "UBIMIA"


# ============================================================
# Flags de ejecución
# ============================================================

# Permite ejecutar el módulo sin API de LLM
ENABLE_AI_GENERATION = True

# Máximo de noticias por cliente
MAX_NEWS_PER_CLIENT = 5


# ============================================================
# Configuración AI (si se habilita)
# ============================================================

AI_MODEL_NAME = "gpt-4o-mini"
AI_TEMPERATURE = 0.2
AI_MAX_TOKENS = 700


# ============================================================
# Periodos soportados (solo UI)
# ============================================================

SUPPORTED_PERIODS = [
    "Q1 2026",
    "Q2 2026",
    "Q3 2026",
    "Q4 2026"
]
