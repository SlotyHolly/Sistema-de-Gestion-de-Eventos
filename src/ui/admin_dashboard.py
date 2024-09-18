from pathlib import Path
from tkinter import Tk, Canvas, Frame, Scrollbar, Button, PhotoImage, Label, VERTICAL, RIGHT, Y
import json

# Ruta al archivo JSON de eventos
EVENTS_PATH = Path(__file__).parent.parent / "data/events.json"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\dashboard_admin")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Función para cargar eventos desde el archivo JSON
def cargar_eventos():
    try:
        with open(EVENTS_PATH, 'r') as file:
            eventos = json.load(file)
        return eventos
    except FileNotFoundError:
        print(f"El archivo {EVENTS_PATH} no existe. Creando un archivo vacío...")
        with open(EVENTS_PATH, 'w') as file:
            json.dump([], file)
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {EVENTS_PATH} no contiene un JSON válido.")
        return []

# Configuración de la ventana principal
window = Tk()
window.geometry("1067x581")
window.configure(bg="#FFFFFF")

# Crear un Canvas para permitir el scroll
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=581,
    width=1067,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Crear un Frame dentro del Canvas para contener los eventos
event_frame = Frame(canvas, bg="#FFFFFF")

# Añadir un Scrollbar al Canvas
scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Cargar y mostrar eventos
eventos = cargar_eventos()
for idx, evento in enumerate(eventos):
    if idx < 6:  # Mostrar solo 6 eventos a la vez
        # Crear un Label para el flyer del evento
        flyer_image = PhotoImage(file=relative_to_assets(evento.get('flyer', 'default_flyer.png')))
        flyer_label = Label(event_frame, image=flyer_image, bg="#FFFFFF")
        flyer_label.image = flyer_image  # Necesario para evitar que la imagen sea recolectada por el garbage collector
        flyer_label.grid(row=idx, column=0, padx=10, pady=10)

        # Crear un Label para la información del evento
        info_label = Label(event_frame, text=evento['nombre'], bg="#FFFFFF", font=("Inter", 16))
        info_label.grid(row=idx, column=1, padx=10, pady=10)

# Configurar el Frame en el Canvas y permitir el scroll
canvas.create_window((0, 0), window=event_frame, anchor='nw')
event_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Otros elementos de la UI
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(x=51.0, y=192.0, width=206.0, height=80.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=51.0, y=424.0, width=206.0, height=80.0)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(x=51.0, y=308.0, width=206.0, height=80.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(x=51.0, y=76.0, width=206.0, height=80.0)

canvas.create_rectangle(942.0, 16.0, 1042.0, 116.0, fill="#000000", outline="")
canvas.create_rectangle(947.0, 21.0, 1037.0, 111.0, fill="#000000", outline="")

canvas.create_text(803.0, 34.0, anchor="nw", text="USER", fill="#000000", font=("Inter", 20 * -1))
canvas.create_text(803.0, 66.0, anchor="nw", text="ADMIN", fill="#000000", font=("Inter", 20 * -1))

window.resizable(False, False)
window.mainloop()
