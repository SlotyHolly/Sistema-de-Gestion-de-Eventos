import json
import hashlib
from pathlib import Path

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "data/users.json"

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

def validate_credentials(username, password):
    """Valida las credenciales del usuario y devuelve su rol si son correctas."""
    try:
        usuarios = load_users()

        # Buscar el usuario en la lista de usuarios
        for usuario in usuarios:
            # Comparar el nombre de usuario y la contraseña hasheada
            if usuario['username'] == username and usuario['password'] == hash_password(password):
                # Devolver el rol si las credenciales coinciden
                return {'success': True, 'role': usuario['role']}
        
        # Si no se encuentra el usuario o la contraseña no coincide
        return {'success': False, 'role': None}

    except FileNotFoundError:
        print(f"El archivo {USUARIOS_PATH} no existe. Creando un archivo vacío...")
        # Crear un archivo vacío con una lista vacía de usuarios
        save_users([])
        return {'success': False, 'role': None}
    
    except json.JSONDecodeError:
        print(f"Error: El archivo {USUARIOS_PATH} no contiene un JSON válido.")
        return {'success': False, 'role': None}