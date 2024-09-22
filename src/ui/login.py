from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/login")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Variables globales para almacenar la acción y las credenciales
action = None
username = None
password = None

def init_login():
    global action, username, password

    # Acciones al hacer clic en los botones
    def on_login():
        global action, username, password
        action = 'login'
        username = entry_1.get()  # Obtiene el valor del campo de usuario
        password = entry_2.get()  # Obtiene el valor del campo de contraseña
        window.destroy()  # Cierra la ventana de login

    def on_register():
        global action
        action = 'register'
        window.destroy()

    def on_password_change():
        global action
        action = 'recovery_password'
        window.destroy()

    # Configuración de la ventana principal
    window = Tk()
    window.geometry("463x499")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=499,
        width=463,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Botones
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=on_login,  # Cambiado a on_login para manejar la acción
        relief="flat"
    )
    button_1.place(x=126.0, y=300.0, width=196.0, height=54.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=on_register,  # Cambiado a on_register para manejar la acción
        relief="flat"
    )
    button_2.place(x=127.0, y=374.0, width=196.0, height=54.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=on_password_change,  # Cambiado a on_password_change para manejar la acción
        relief="flat"
    )
    button_3.place(x=25.0, y=448.0, width=181.0, height=37.0)

    # Entradas de texto
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(215.5, 151.0, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_1.place(x=35.0, y=129.0, width=361.0, height=42.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(215.5, 257.0, image=entry_image_2)
    entry_2 = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_2.place(x=35.0, y=234.0, width=361.0, height=44.0)

    # Etiquetas de texto
    canvas.create_text(25.0, 186.0, anchor="nw", text="Contraseña\n", fill="#000000", font=("AndadaPro Bold", 32 * -1))
    canvas.create_text(25.0, 79.0, anchor="nw", text="Usuario:", fill="#000000", font=("AndadaPro Bold", 32 * -1))
    canvas.create_text(105.0, 21.0, anchor="nw", text="Inicio de Sesion\n", fill="#000000", font=("AndadaPro ExtraBold", 32 * -1))

    window.resizable(False, False)

    action = None  # Reiniciar la acción seleccionada
    window.mainloop()
    
    return action, username, password  # Devolver la acción seleccionada y las credenciales
