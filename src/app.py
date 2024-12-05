# src/app.py
from flask import Flask
from .extensions import socketio
from .routes import main
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'

    # Configuración para subida de imágenes
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    # Crea la carpeta de subidas si no existe
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.register_blueprint(main)

    socketio.init_app(app)

    return app
