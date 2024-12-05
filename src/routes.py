# src/routes.py
from flask import Blueprint, flash, render_template, request, redirect, url_for, session, make_response
from flask_socketio import emit # type: ignore
from .functions import load_users, save_users, load_events, save_events, login_required, add_event_to_user, has_permission, create_seating_matrix, get_role_from_cookie, create_session, load_sessions, save_sessions, validate_session, delete_session, redirect_to_dashboard, get_available_events, total_tickets_available, validate_session, allowed_file
from .app import socketio
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import logging
logging.basicConfig(level=logging.DEBUG)

main = Blueprint('main', __name__)

@main.before_request
def validate_cookie():
    if request.endpoint in ['main.login', 'main.register', 'static', 'favicon']:
        return  # Permitir el acceso sin validación

    session_id = request.cookies.get('session_id')
    session_record = validate_session(session_id)

    if not session_record:
        response = make_response(redirect(url_for('main.login')))
        response.delete_cookie('session_id')
        return response

    # Actualizar sesión
    session['username'] = session_record['username']
    session['role'] = session_record['role']

@main.route('/')
def home():
    if 'username' in session:
        if session['role'] == 'admin':
            return redirect(url_for('main.admin'))
        else:
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.login'))

@main.route('/index')
@login_required(role='user')
def index():
    if 'username' in session:
        events = load_events()
        return render_template('index.html', events=events)
    else:
        return redirect(url_for('main.login'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Verificar si existe una cookie `session_id` válida
    session_id = request.cookies.get('session_id')
    if session_id:
        session_record = validate_session(session_id)
        if session_record:
            # Redirigir al dashboard según el rol
            if session_record:
                return redirect_to_dashboard(session_record['role'])

    # Si no hay cookie o no es válida, mostrar el formulario de login
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                # Crear una nueva sesión
                session_id = create_session(username, user['role'])

                # Configurar la cookie con el session_id
                if user['role'] == 'admin':
                    response = make_response(redirect(url_for('main.admin')))
                else:
                    response = make_response(redirect(url_for('main.index')))
                response.set_cookie('session_id', session_id, httponly=True, samesite='Strict')
                return response

        flash("Credenciales inválidas.", "error")
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('main.index'))  # Redirigir si ya está logueado

    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        # Verifica si el usuario ya existe
        for user in users:
            if user['username'] == username:
                return "El usuario ya existe"
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        users.append({'username': username, 'password': hashed_password, 'role': 'user'})
        save_users(users)
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/events/<category>')
@login_required(role='user')
def events_by_category(category):
    events = load_events()
    filtered_events = [event for event in events if event['category'].lower() == category.lower()]
    return render_template('index.html', events=filtered_events)

@main.route('/admin')
@login_required(role='admin')
def admin():
    eventos = load_events()
    # Degubeamos la variable eventos
    print(eventos)
    return render_template('admin.html', events=eventos)

@main.route('/add_event', methods=['GET', 'POST'])
@login_required(role='admin')
def add_event():
    """Permite al administrador agregar nuevos eventos."""
    if request.method == 'POST':
        try:
            # Cargar eventos existentes
            eventos = load_events()

            # Obtener datos del formulario
            name = request.form['name']
            location = request.form['location']
            date = request.form['date']
            flyer = request.form['flyer']
            rows = int(request.form.get('rows', 0))  # Filas de asientos
            cols = int(request.form.get('cols', 0))  # Columnas de asientos

            if not name or not location or not date or rows <= 0 or cols <= 0:
                flash("Todos los campos son obligatorios y deben ser válidos.", "error")
                return render_template('add_event.html')

            # Manejo de la imagen subida
            image = request.files.get('image')
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                flyer = f"/{image_path}"  # Usa la imagen subida como flyer

            # Crear nuevo evento
            new_event = {
                'id': f"event{len(eventos) + 1}",
                'name': name,
                'location': location,
                'date': date,
                'flyer': flyer,
                'tickets': rows * cols,
                'disponibilidad': rows * cols,
                'seating': create_seating_matrix(rows, cols)
            }

            # Agregar evento y guardar
            eventos.append(new_event)
            save_events(eventos)

            flash("Evento agregado exitosamente.", "success")
            return redirect(url_for('main.admin'))

        except Exception as e:
            print(f"Error al agregar evento: {e}")
            flash("Error al agregar el evento. Por favor, revisa los datos ingresados.", "error")
            return render_template('add_event.html')

    return render_template('add_event.html')

@main.route('/profile')
@login_required()
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'], role=session['role'])
    else:
        return redirect(url_for('main.login'))
    
@main.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')
    if session_id:
        delete_session(session_id)

    session.clear()
    response = make_response(redirect(url_for('main.login')))
    response.delete_cookie('session_id')
    flash("Sesión cerrada correctamente.", "success")
    return response

@main.route('/change_password', methods=['GET', 'POST'])
@login_required()
def change_password():
    if 'username' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        users = load_users()
        username = session['username']
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        for user in users:
            if user['username'] == username and check_password_hash(user['password'], old_password):
                user['password'] = generate_password_hash(new_password, method='pbkdf2:sha256')
                save_users(users)
                return redirect(url_for('main.index'))

        return "Contraseña incorrecta."

    return render_template('change_password.html')

@main.route('/my_events')
def my_events():
    if 'username' in session:
        username = session['username']
        users = load_users()
        events = load_events()

        # Obtener eventos comprados por el usuario
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('main.index'))

        purchased_events = []
        for record in user.get('purchased_events', []):
            event_id, tickets_bought = record.split(":")
            event = next((e for e in events if str(e['id']) == event_id), None)
            if event:
                purchased_events.append({
                    "name": event["name"],
                    "location": event["location"],
                    "date": event["date"],
                    "tickets_bought": tickets_bought
                })

        return render_template('my_events.html', purchased_events=purchased_events)

    return redirect(url_for('main.login'))

@main.route('/edit_event/<event_id>', methods=['GET', 'POST'])
@login_required(role='admin')
def edit_event(event_id):
    eventos = load_events()
    evento = next((e for e in eventos if str(e['id']) == str(event_id)), None)

    if not evento:
        flash("Evento no encontrado.", "error")
        return redirect(url_for('main.admin'))

    if request.method == 'POST':
        try:
            # Elimina espacios extra de los nombres de los campos
            form_data = {key.strip(): value for key, value in request.form.items()}

            evento['name'] = form_data['name']
            evento['location'] = form_data['location']
            evento['date'] = form_data['date']
            evento['flyer'] = form_data['flyer']
            evento['tickets'] = int(form_data['tickets'])

            # Manejo de la imagen subida
            image = request.files.get('image')
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                event['flyer'] = f"/{image_path}"

            save_events(eventos)
            flash("Evento actualizado exitosamente.", "success")
            return redirect(url_for('main.admin'))
        except Exception as e:
            print(f"Error al actualizar evento: {e}")
            print("Datos recibidos:", request.form)
            flash("Ocurrió un error al actualizar el evento.", "error")

    return render_template('edit_event.html', event=evento)

@main.route('/buy_event/<event_id>', methods=['GET', 'POST'])
def buy_event(event_id):
    if 'username' not in session:
        print("[DEBUG] Usuario no autenticado. Redirigiendo a login.")
        return redirect(url_for('main.login'))

    # Cargar datos
    print("[DEBUG] Cargando datos del evento y usuario.")
    events = load_events()
    users = load_users()
    username = session['username']

    # Encontrar el evento por ID
    event = next((e for e in events if str(e['id']) == str(event_id)), None)
    if not event:
        print(f"[DEBUG] Evento con ID {event_id} no encontrado.")
        flash("El evento no existe.", "error")
        return redirect(url_for('main.index'))

    print(f"[DEBUG] Evento encontrado: {event['name']} ({event_id})")

    if request.method == 'POST':
        print("[DEBUG] Procesando compra POST.")
        # Validar cantidad de tickets seleccionada
        try:
            tickets_to_buy = int(request.form['tickets'])
            print(f"[DEBUG] Tickets solicitados: {tickets_to_buy}")
        except ValueError:
            print("[DEBUG] Error: Cantidad de tickets no válida.")
            flash("Cantidad de tickets inválida.", "error")
            return redirect(url_for('main.buy_event', event_id=event_id))

        if tickets_to_buy <= 0 or tickets_to_buy > event['tickets']:
            print("[DEBUG] Error: Cantidad de tickets excede el límite.")
            flash("La cantidad de tickets no es válida.", "error")
            return redirect(url_for('main.buy_event', event_id=event_id))

        # Registrar la compra en el usuario
        user = next((u for u in users if u['username'] == username), None)
        if not user:
            print("[DEBUG] Usuario no encontrado.")
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('main.index'))

        if 'purchased_events' not in user:
            user['purchased_events'] = []

        # Formato "1:3" (ID del evento:Cantidad comprada)
        updated = False

        for i, purchase in enumerate(user['purchased_events']):
            if purchase.split(":")[0] == event_id:
                # Actualizamos la cantidad de tickets comprados
                current_tickets = int(purchase.split(":")[1])
                user['purchased_events'][i] = f"{event_id}:{current_tickets + tickets_to_buy}"
                updated = True
                break

        # Si el evento no está en purchased_events, lo añadimos
        if not updated:
            user['purchased_events'].append(f"{event_id}:{tickets_to_buy}")

        # Descontar tickets del evento
        print(f"[DEBUG] Tickets disponibles antes: {event['tickets']}")
        event['tickets'] -= tickets_to_buy
        print(f"[DEBUG] Tickets disponibles después: {event['tickets']}")

        # Guardar cambios
        save_events(events)
        save_users(users)
        print("[DEBUG] Cambios guardados en events.json y users.json.")

        flash(f"Compra realizada con éxito. Tickets comprados: {tickets_to_buy}.", "success")
        return redirect(url_for('main.my_events'))

    print("[DEBUG] Mostrando formulario de compra.")
    # Renderizar la página de selección de tickets (GET)
    return render_template('buy_event.html', event=event)


@main.route('/confirm_purchase/<event_id>', methods=['POST'])
@login_required(role='user')
def confirm_purchase(event_id):
    """Confirma la compra de tickets para el evento."""
    try:
        tickets = int(request.form['tickets'])
        eventos = load_events()
        users = load_users()

        evento = next((e for e in eventos if e['id'] == event_id), None)
        if not evento:
            flash("Evento no encontrado.", "error")
            return redirect(url_for('main.index'))

        if tickets <= 0 or tickets > evento['disponibilidad']:
            flash("Cantidad de tickets inválida.", "error")
            return redirect(url_for('main.buy_event_dashboard', event_id=event_id))

        # Reducir disponibilidad y guardar
        evento['disponibilidad'] -= tickets

        username = session.get('username')
        user = next((u for u in users if u['username'] == username), None)

        if not user:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for('main.login'))

        user.setdefault('purchased_events', {}).setdefault(event_id, 0)
        user['purchased_events'][event_id] += tickets

        save_events(eventos)
        save_users(users)

        flash(f"Compra exitosa. Has comprado {tickets} tickets para {evento['name']}.", "success")
        return redirect(url_for('main.my_events'))

    except Exception as e:
        print(f"Error al procesar la compra: {e}")
        flash("Ocurrió un error al procesar tu compra.", "error")
        return redirect(url_for('main.buy_event_dashboard', event_id=event_id))

@main.route('/manage_users')
@login_required(role='admin')
def manage_users():
    users = load_users()
    return render_template('manage_users.html', users=users)

@main.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required(role='admin')
def edit_user(username):
    users = load_users()
    user = next((u for u in users if u['username'] == username), None)

    if not user:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for('main.manage_users'))

    if request.method == 'POST':
        try:
            user['username'] = request.form['username']
            user['role'] = request.form['role']
            if request.form['password']:
                user['password'] = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

            save_users(users)
            flash("Usuario actualizado exitosamente.", "success")
            return redirect(url_for('main.manage_users'))
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            flash("Ocurrió un error al actualizar el usuario.", "error")

    return render_template('edit_user.html', user=user)

@main.route('/delete_user/<username>', methods=['POST'])
@login_required(role='admin')
def delete_user(username):
    try:
        users = load_users()
        users = [u for u in users if u['username'] != username]
        save_users(users)
        flash("Usuario eliminado exitosamente.", "success")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        flash("Ocurrió un error al eliminar el usuario.", "error")

    return redirect(url_for('main.manage_users'))


@main.route('/available_events')
def available_events():
    events = load_events()
    available = get_available_events(events)
    return render_template('index.html', events=available)

@main.route('/total_tickets')
def total_tickets():
    events = load_events()
    total = total_tickets_available(events)
    return f"El total de entradas disponibles es: {total}"

@socketio.on('update_event')
def handle_update_event(data):
    required_fields = ['event_id', 'action']
    if all(field in data for field in required_fields):
        emit('refresh_events', data, broadcast=True)
    else:
        print(f"Datos inválidos: {data}")