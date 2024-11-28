import json
import os
from datetime import datetime, timedelta

def generate_sample_events(file_path, num_events=5):
    events = []
    base_date = datetime.now()

    for i in range(1, num_events + 1):
        event = {
            "name": f"Evento de Prueba {i}",
            "location": f"Lugar {i}",
            "date": (base_date + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S'),
            "tickets": 100 - i * 5,  # Cantidad decreciente de entradas
            "flyer": "/static/flyer_default.png"
        }
        events.append(event)

    with open(file_path, 'w') as f:
        json.dump(events, f, indent=4)

# Usar la función para generar eventos
file_path = os.path.join('src', 'data', 'events.json')
generate_sample_events(file_path)
