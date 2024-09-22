from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/register")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Variables globales para almacenar los datos de registro
username = None
password = None

def init_register_user():
    global username, password

    def on_register():
        global username, password
        # Obtener los valores de los campos de entrada
        username = entry_2.get()
        password = entry_1.get()
        window.destroy()  # Cerrar la ventana de registro

    # Configuración de la ventana principal
    window = Tk()
    window.geometry("491x430")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=430,
        width=491,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Botón de registro
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=on_register,  # Asignar la función para registrar
        relief="flat"
    )
    button_1.place(x=148.0, y=339.0, width=196.0, height=54.0)

    # Campo de entrada para contraseña
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    canvas.create_image(265.5, 273.5, image=entry_image_1)
    entry_1 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(x=89.0, y=246.0, width=353.0, height=53.0)

    # Texto de "Contraseña"
    canvas.create_text(
        39.0, 196.0, anchor="nw", text="Contraseña\n",
        fill="#000000", font=("AndadaPro Bold", 32 * -1)
    )

    # Campo de entrada para nombre de usuario
    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    canvas.create_image(265.5, 159.5, image=entry_image_2)
    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(x=89.0, y=132.0, width=353.0, height=53.0)

    # Texto de "Usuario"
    canvas.create_text(
        39.0, 82.0, anchor="nw", text="Usuario\n",
        fill="#000000", font=("AndadaPro Bold", 32 * -1)
    )

    # Texto de "Registro"
    canvas.create_text(
        166.0, 24.0, anchor="nw", text="Registro",
        fill="#000000", font=("AndadaPro ExtraBold", 32 * -1)
    )

    window.resizable(False, False)
    window.mainloop()

    return username, password  # Devolver el nombre de usuario y la contraseña
