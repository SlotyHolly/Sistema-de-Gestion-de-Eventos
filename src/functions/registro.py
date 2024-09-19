import json
import hashlib
from pathlib import Path

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "data/users.json"
DEFAULT_ROLE = 'user'

def hash_password(password):
    """Devuelve el hash SHA-256 de la contraseña proporcionada."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Carga los usuarios desde el archivo JSON, o devuelve una lista vacía si el archivo no existe o está corrupto."""
    try:
        with open(USUARIOS_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"El archivo {USUARIOS_PATH} no existe. Creando un archivo nuevo...")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {USUARIOS_PATH} no contiene un JSON válido. Se reiniciará el archivo.")
        return []

def save_users(usuarios):
    """Guarda la lista de usuarios en el archivo JSON."""
    try:
        with open(USUARIOS_PATH, 'w') as file:
            json.dump(usuarios, file, indent=4)
        return True
    except IOError:
        print("Error al guardar los cambios en el archivo.")
        return False

def user_exists(username, usuarios):
    """Verifica si un usuario ya existe en la lista de usuarios."""
    return any(usuario['username'] == username for usuario in usuarios)

def register_user(username, password):
    """Registra un nuevo usuario con el nombre de usuario y contraseña proporcionados."""
    if not username or not password:
        return {'success': False, 'message': 'El nombre de usuario y la contraseña no pueden estar vacíos.'}

    usuarios = load_users()

    if user_exists(username, usuarios):
        return {'success': False, 'message': 'El nombre de usuario ya existe.'}

    password_hash = hash_password(password)
    new_user = {
        'username': username,
        'password': password_hash,
        'role': DEFAULT_ROLE
    }
    usuarios.append(new_user)

    if save_users(usuarios):
        return {'success': True, 'message': 'Usuario registrado correctamente.'}
    else:
        return {'success': False, 'message': 'Error al guardar el usuario.'}