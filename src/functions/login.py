import json
from pathlib import Path

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "data/users.json"

def validate_credentials(username, password):
    try:
        # Leer el archivo JSON
        with open(USUARIOS_PATH, 'r') as file:
            usuarios = json.load(file)

        # Buscar el usuario en la lista de usuarios
        for usuario in usuarios:
            if usuario['username'] == username and usuario['password'] == password:
                # Devolver el rol si las credenciales coinciden
                return {'success': True, 'role': usuario['role']}
        
        # Si no se encuentra el usuario, devolver éxito como False
        return {'success': False, 'role': None}

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {USUARIOS_PATH}.")
        return {'success': False, 'role': None}
    except json.JSONDecodeError:
        print(f"Error: El archivo {USUARIOS_PATH} no contiene un JSON válido.")
        return {'success': False, 'role': None}