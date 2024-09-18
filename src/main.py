from ui.login import init_login  # Importa la función para iniciar la ventana de login
from ui.user_dashboard import init_user_dashboard
from ui.admin_dashboard import init_admin_dashboard  # Cambié el nombre para reflejar la función actual
from ui.register import init_register_user
from functions.registro import register_user
from functions.login import validate_credentials

class Aplicacion:
    def __init__(self):
        # Inicializa variables de estado, como el usuario actual
        self.username = None
        self.rol = None

    def iniciar_aplicacion(self):
        """Inicia la aplicación con la ventana de login y controla el flujo."""
        while True:
            # Muestra la ventana de login y obtiene la acción seleccionada
            accion, username, password = init_login()

            # Controla el flujo basado en la acción devuelta
            if accion == 'login':
                self.login(username, password)
            elif accion == 'register':
                self.register_user()
            elif accion == 'change_password':
                self.change_password()
            elif accion is None:
                print("Cerrando la aplicación...")
                break  # Sale del bucle y cierra la aplicación

    def login(self, username, password):
        """Maneja el proceso de inicio de sesión."""
        resultado = validate_credentials(username, password)
        
        if resultado['success']:
            print(f"Usuario {username} ha iniciado sesión.")
            self.username = username  # Asigna el nombre de usuario al atributo de la clase
            self.rol = resultado['role']
            self.show_dashboard()  # Llama a show_dashboard sin pasar argumentos
        else:
            print("Credenciales inválidas. Inténtalo de nuevo.")

    def register_user(self):
        """Muestra la ventana de registro de usuario."""
        username, password = init_register_user()
        if username and password:
            # Llamar a la función de registro
            resultado = register_user(username, password)
            if resultado['success']:
                # Llamar nuevamente a la ventana de login
                accion, username, password = init_login()
            else:
                print(f"Error al registrar: {resultado['message']}")
        else:
            print("Registro cancelado.")

    def change_password(self):
        """Muestra la ventana para cambiar la contraseña."""
        print("Mostrar ventana de cambio de contraseña...")  # Llamada a la función de cambio de contraseña (a implementar)

    def show_dashboard(self):
        """Muestra el dashboard según el rol del usuario."""
        if self.rol == "usuario":
            init_user_dashboard(self.username)  # Abre el dashboard de usuario
        elif self.rol == "admin":
            init_admin_dashboard(self.username)  # Abre la consola de administrador

if __name__ == "__main__":
    app = Aplicacion()
    app.iniciar_aplicacion()
