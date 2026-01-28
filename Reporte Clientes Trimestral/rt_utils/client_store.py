# utils/client_store.py

import json
from pathlib import Path
from config import DATA_DIR

CLIENTS_FILE = DATA_DIR / "clientes.json"


def load_clients():
    """
    Carga clientes existentes desde el JSON.
    """
    if not CLIENTS_FILE.exists():
        return []

    with open(CLIENTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_client(client_data: dict, persist: bool = True):
    """
    Agrega un nuevo cliente al catálogo.
    """
    clients = load_clients()

    existing_names = {c["name"] for c in clients}
    if client_data["name"] in existing_names:
        return clients

    clients.append(client_data)

    if persist:
        with open(CLIENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(clients, f, indent=2, ensure_ascii=False)

    return clients
