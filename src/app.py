from flask import Flask, render_template, request, redirect, url_for
from functions.login import validar_credenciales, obtener_rol_usuario
from functions.dashboard import cargar_eventos

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        print(f"Intentando iniciar sesión con usuario: {username}")

        # Validar las credenciales de usuario
        if validar_credenciales(username, password):
            print(f"Credenciales válidas para usuario: {username}")
            # Obtener el rol desde el archivo JSON de usuarios
            role = obtener_rol_usuario(username)
            print(f"Rol obtenido: {role}")
            return redirect(url_for('dashboard', username=username, role=role))
        else:
            print(f"Credenciales incorrectas para usuario: {username}")
            return render_template('login.html', error="Credenciales incorrectas")
    
    return render_template('login.html')

# Ruta para el dashboard del admin o usuario
@app.route('/dashboard/<username>')
def dashboard(username):
    role = request.args.get('role')  # Recibir el rol desde los parámetros de la URL
    print(f"Mostrando dashboard para {username} con rol {role}")
    # Cargar eventos desde el archivo JSON
    eventos = cargar_eventos()
    return render_template('dashboard.html', username=username, role=role, eventos=eventos)

if __name__ == '__main__':
    app.run(debug=True)
