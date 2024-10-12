from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path

app = Flask(__name__)

# Ruta a los archivos de datos
USERS_PATH = Path(__file__).parent / "data/users.json"
EVENTS_PATH = Path(__file__).parent / "data/events.json"

# Ruta principal - Página de inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validar las credenciales de usuario
        if validar_credenciales(username, password):
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
    return render_template('login.html')

# Ruta para el dashboard del admin
@app.route('/dashboard/<username>')
def dashboard(username):
    # Cargar eventos desde el archivo JSON
    eventos = cargar_eventos()
    role = "admin"  # Simulación para el rol (en este caso, admin)
    return render_template('dashboard.html', username=username, role=role, eventos=eventos)

# Ruta para cargar los eventos
def cargar_eventos():
    try:
        with open(EVENTS_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Validar credenciales (se puede mejorar para usar hashed passwords)
def validar_credenciales(username, password):
    try:
        with open(USERS_PATH, 'r') as file:
            usuarios = json.load(file)
            for usuario in usuarios:
                if usuario['username'] == username and usuario['password'] == password:
                    return True
        return False
    except (FileNotFoundError, json.JSONDecodeError):
        return False

if __name__ == '__main__':
    app.run(debug=True)

