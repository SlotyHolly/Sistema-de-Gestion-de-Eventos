# src/functions.py
import json
import os
from functools import wraps
from flask import redirect, request, url_for, session, flash, abort
import uuid
from pathlib import Path
import qrcode # type: ignore
from functools import reduce

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
QR_DIR = os.path.join(os.path.dirname(__file__), 'data', 'qr_codes')
SESSIONS_PATH = Path(__file__).parent / "data/Sessions.json"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Diccionario de roles y permisos
ROLES_PERMISSIONS = {
    'admin': ['add_event', 'view_events', 'manage_users'],
    'user': ['view_events', 'buy_event']
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def redirect_to_dashboard(role):
    """Redirige al dashboard correspondiente según el rol."""
    if role == 'admin':
        return redirect(url_for('main.admin'))
    elif role == 'user':
        return redirect(url_for('main.index'))
    else:
        flash("Rol desconocido.", "error")
        return redirect(url_for('main.login'))

def has_permission(role, action):
    """Verifica si un rol tiene permiso para realizar una acción."""
    permissions = ROLES_PERMISSIONS.get(role, [])
    return action in permissions

def get_role_from_cookie():
    user_role = request.cookies.get('user_role')
    valid_roles = ['admin', 'user']
    if user_role in valid_roles:
        return user_role
    return None

def create_seating_matrix(rows, cols):
    """Crea una matriz de asientos disponibles para un evento."""
    return [[1 for _ in range(cols)] for _ in range(rows)]  # 1 indica asiento disponibl

def update_seat(event_id, row, col):
    events = load_events()
    for event in events:
        if event['id'] == event_id:
            if event['seating'][row][col] == 1:  # Verifica si el asiento está disponible
                event['seating'][row][col] = 0  # Marca el asiento como ocupado
                save_events(events)
                return True
    return False

def login_required(role=None):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            session_id = request.cookies.get('session_id')
            session_record = validate_session(session_id)

            if not session_record:
                flash("Por favor, inicia sesión.", "error")
                return redirect(url_for('main.login'))

            if role and session_record['role'] != role:
                abort(403)  # Acceso denegado

            session['username'] = session_record['username']
            session['role'] = session_record['role']
            return view_function(*args, **kwargs)
        return wrapped_view
    return decorator

def add_event_to_user(username, event_id):
    """Añade un evento al usuario especificado."""
    users = load_users()
    for user in users:
        if user['username'] == username:
            if 'purchased_events' not in user:
                user['purchased_events'] = []
            if event_id not in user['purchased_events']:
                user['purchased_events'].append(event_id)
                save_users(users)
                return True
    return False

# Funcion para generar codigos QR
def generate_qr_code(data, filename):
    """Genera un código QR con la información especificada."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def load_users():
    users_file = os.path.join(DATA_DIR, 'users.json')
    if not os.path.exists(users_file):
        return []
    with open(users_file, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(os.path.join(DATA_DIR, 'users.json'), 'w') as f:
        json.dump(users, f, indent=4)

def load_events():
    events_file = os.path.join(DATA_DIR, 'events.json')
    if not os.path.exists(events_file):
        return []
    with open(events_file, 'r') as f:
        return json.load(f)

def save_events(events):
    with open(os.path.join(DATA_DIR, 'events.json'), 'w') as f:
        json.dump(events, f, indent=4)

def load_sessions():
    """Cargar las sesiones activas desde el archivo JSON."""
    try:
        with open(SESSIONS_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_sessions(sessions):
    """Guardar las sesiones activas en el archivo JSON."""
    with open(SESSIONS_PATH, 'w') as file:
        json.dump(sessions, file, indent=4)

def create_session(username, role):
    """Crear una nueva sesión."""
    sessions = load_sessions()
    session_id = str(uuid.uuid4())
    sessions.append({
        "session_id": session_id,
        "username": username,
        "role": role
    })
    save_sessions(sessions)
    return session_id

def validate_session(session_id):
    """Validar si el session_id es válido."""
    sessions = load_sessions()
    return next((s for s in sessions if s['session_id'] == session_id), None)

def delete_session(session_id):
    """Eliminar una sesión activa."""
    sessions = load_sessions()
    sessions = [s for s in sessions if s['session_id'] != session_id]
    save_sessions(sessions)

def add_event(events, event_data):
    """Agrega un nuevo evento a la lista."""
    events.append(event_data)  # Agrega el evento a la lista
    save_events(events)  # Guarda la lista actualizada
    return True

def remove_event(events, event_id):
    """Elimina un evento por ID."""
    event_to_remove = next((e for e in events if str(e['id']) == str(event_id)), None)
    if event_to_remove:
        events.remove(event_to_remove)  # Elimina el evento
        save_events(events)
        return True
    return False

def get_available_events(events):
    """Obtiene eventos con entradas disponibles."""
    return list(filter(lambda e: e['tickets'] > 0, events))

def total_tickets_available(events):
    """Calcula el total de entradas disponibles."""
    return reduce(lambda acc, e: acc + e['tickets'], events, 0)
