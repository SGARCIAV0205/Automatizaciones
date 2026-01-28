import os
import yaml
from datetime import date

def load_cfg(cfg_path="config.yaml"):
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dirs():
    for d in ["data/raw", "data/processed", "reports/out"]:
        os.makedirs(d, exist_ok=True)

def today_iso():
    return date.today().isoformat()
