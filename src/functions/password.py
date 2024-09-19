import json
import hashlib
from pathlib import Path

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "data/users.json"
RECOVERY_CODE = "1234"

def hash_password(password):
    """Devuelve hash SHA-256 de la contraseña proporcionada."""
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

def recovery_password(username, code, new_password):
    """Cambia la contraseña de un usuario si el código de recuperación es correcto."""
    try:
        usuarios = load_users()

        # Buscar el usuario en la lista
        for usuario in usuarios:
            if usuario['username'] == username:
                # Verificar el código de recuperación
                if code == RECOVERY_CODE:
                    # Cambiar la contraseña
                    usuario['password'] = hash_password(new_password)
                    
                    # Guardar los cambios en el archivo JSON
                    if save_users(usuarios):
                        return {'success': True, 'message': 'Contraseña cambiada exitosamente.'}
                    else:
                        return {'success': False, 'message': 'Error al guardar el usuario.'}
                else:
                    # Código incorrecto
                    return {'success': False, 'message': 'Código de recuperación incorrecto.'}

        # Usuario no encontrado
        return {'success': False, 'message': 'Usuario no encontrado.'}

    except FileNotFoundError:
        return {'success': False, 'message': 'Archivo de usuarios no encontrado.'}
    except json.JSONDecodeError:
        return {'success': False, 'message': 'Error al leer el archivo de usuarios.'}
    except Exception as e:
        return {'success': False, 'message': f'Error inesperado: {e}'}