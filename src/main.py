from ui.login import init_login
from ui.user_dashboard import init_user_dashboard
from ui.admin_dashboard import init_admin_dashboard
from ui.recovery_password import init_recovery_password
from ui.register import init_register_user
from functions.registro import register_user
from functions.login import validate_credentials

class App:
    def __init__(self):
        self.username = None
        self.rol = None

    def run(self):
        while True:
            accion, username, password = init_login()
            if accion == 'login':
                self.login(username, password)
            elif accion == 'register':
                self.register_user()
            elif accion == 'recovery_password':
                self.init_recovery_password()
            elif accion is None:
                print("Cerrando la aplicación...")
                break  # Sale del bucle y cierra la aplicación

    def login(self, username, password):
        """Maneja el proceso de inicio de sesión."""
        result = validate_credentials(username, password)
        
        if result['success']:
            print(f"Usuario {username} ha iniciado sesión.")
            self.username = username  # Asigna el nombre de usuario al atributo de la clase
            self.rol = result['role']
            self.show_dashboard()  # Llama a show_dashboard sin pasar argumentos
        else:
            print("Credenciales inválidas. Inténtalo de nuevo.")

    def register_user(self):
        """Muestra la ventana de registro de usuario."""
        username, password = init_register_user()
        if username and password:
            # Llamar a la función de registro
            result = register_user(username, password)
            if result['success']:
                # Llamar nuevamente a la ventana de login
                accion, username, password = init_login()
            else:
                print(f"Error al registrar: {result['message']}")
        else:
            print("El nombre de usuario y la contraseña no pueden estar vacíos.")

    def init_recovery_password(self):
        """Muestra la ventana de recuperación de contraseña."""
        init_recovery_password()

    def show_dashboard(self):
        """Muestra el dashboard según el rol del usuario."""
        if self.rol == "usuario":
            init_user_dashboard(self.username)  # Abre el dashboard de usuario
        elif self.rol == "admin":
            init_admin_dashboard(self.username)  # Abre la consola de administrador

if __name__ == "__main__":
    app = App()
    app.run()
