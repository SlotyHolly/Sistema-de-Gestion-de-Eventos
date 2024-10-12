import json
from pathlib import Path

EVENTS_PATH = Path(__file__).parent.parent / "data/events.json"

# Ruta para cargar los eventos
def cargar_eventos():
    try:
        with open(EVENTS_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []