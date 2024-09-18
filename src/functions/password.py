import json
from pathlib import Path
import hashlib

# Ruta al archivo JSON de usuarios
USUARIOS_PATH = Path(__file__).parent.parent / "./data/users.json"

def hash_password(password):
    """Devuelve el hash SHA-256 de la contraseña proporcionada."""
    return hashlib.sha256(password.encode()).hexdigest()

def recovery_password(username, code, new_password):
    try:
        # Leer el archivo JSON de usuarios
        with open(USUARIOS_PATH, 'r') as file:
            usuarios = json.load(file)

        # Buscar el usuario en la lista
        for usuario in usuarios:
            if usuario['username'] == username:
                # Verificar el código de recuperación
                if code == "1234":
                    # Cambiar la contraseña
                    usuario['password'] = hash_password(new_password)
                    
                    # Guardar los cambios en el archivo JSON
                    with open(USUARIOS_PATH, 'w') as file:
                        json.dump(usuarios, file, indent=4)

                    return {'success': True, 'message': 'Contraseña cambiada exitosamente.'}
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
