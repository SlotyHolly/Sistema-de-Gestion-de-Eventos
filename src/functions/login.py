import json
from pathlib import Path

USERS_PATH = Path(__file__).parent.parent / "data/users.json"

# Validar credenciales (se puede mejorar para usar hashed passwords)
def validar_credenciales(username, password):
    print(f"Validando credenciales para usuario: {username}")
    print(f"Password: {password}")
    try:
        with open(USERS_PATH, 'r') as file:
            usuarios = json.load(file)
            for usuario in usuarios:
                if usuario['username'] == username and usuario['password'] == password:
                    return True
        return False
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error al leer el archivo de usuarios")
        return False
    
def obtener_rol_usuario(username):
    try:
        with open(USERS_PATH, 'r') as file:
            usuarios = json.load(file)
            for usuario in usuarios:
                if usuario['username'] == username:
                    return usuario['role']
    except (FileNotFoundError, json.JSONDecodeError):
        return None
