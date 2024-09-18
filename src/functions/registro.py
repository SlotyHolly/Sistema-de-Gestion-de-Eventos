import json
import hashlib
from pathlib import Path

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "data/users.json"

def hash_password(password):
    """Devuelve el hash SHA-256 de la contraseña proporcionada."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    # Cargar o crear el archivo de usuarios
    try:
        with open(USUARIOS_PATH, 'r') as file:
            usuarios = json.load(file)
    except FileNotFoundError:
        print(f"El archivo {USUARIOS_PATH} no existe. Creando un archivo nuevo...")
        usuarios = []
    except json.JSONDecodeError:
        print(f"Error: El archivo {USUARIOS_PATH} no contiene un JSON válido. Se reiniciará el archivo.")
        usuarios = []

    # Verificar si el usuario ya existe
    for usuario in usuarios:
        if usuario['username'] == username:
            print("El nombre de usuario ya existe.")
            return {'success': False, 'message': 'El nombre de usuario ya existe.'}

    # Crear un hash de la contraseña
    password_hash = hash_password(password)

    # Si no existe, agregar el nuevo usuario
    new_user = {
        'username': username,
        'password': password_hash,  # Guardar el hash de la contraseña
        'role': 'user'  # Asignar rol de usuario por defecto
    }
    usuarios.append(new_user)

    # Guardar los cambios en el archivo JSON
    try:
        with open(USUARIOS_PATH, 'w') as file:
            json.dump(usuarios, file, indent=4)
        print(f"Usuario {username} registrado exitosamente.")
        return {'success': True, 'message': 'Usuario registrado correctamente.'}
    except IOError:
        print("Error al guardar los cambios en el archivo.")
        return {'success': False, 'message': 'Error al guardar el usuario.'}
