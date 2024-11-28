# src/app.py
from flask import Flask
from .extensions import socketio
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu_clave_secreta'

    app.register_blueprint(main)

    socketio.init_app(app)

    return app
