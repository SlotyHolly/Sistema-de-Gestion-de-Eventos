from pathlib import Path
from tkinter import Tk, Canvas, Frame, Scrollbar, Button, PhotoImage, Label, VERTICAL, RIGHT, Y
import json
from PIL import Image, ImageTk

# Ruta al archivo JSON de eventos y la carpeta de imágenes
EVENTS_PATH = Path(__file__).parent.parent / "data/events.json"
FLYERS_PATH = Path(__file__).parent.parent / "data/events_data"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/dashboard_admin")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_flyers(path: str) -> Path:
    return FLYERS_PATH / Path(path)

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

# Función para redimensionar imágenes
def cargar_imagen_redimensionada(path, size=(100, 100)):
    try:
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")
        return None

# Nueva función para abrir el dashboard admin
def init_admin_dashboard(username):
    # Configuración de la ventana principal
    window = Tk()
    window.geometry("1067x581")
    window.configure(bg="#FFFFFF")

    # Crear un Frame superior para el texto de "USER" y "ADMIN"
    top_frame = Frame(window, bg="#FFFFFF", height=80)
    top_frame.pack(fill='x')

    # Crear texto de "USER" y "ADMIN" en el Frame superior con el nombre del usuario
    user_label = Label(top_frame, text=username, font=("Inter", 20), bg="#FFFFFF")
    user_label.place(x=803.0, y=10.0)

    admin_label = Label(top_frame, text="ADMIN", font=("Inter", 20), bg="#FFFFFF")
    admin_label.place(x=803.0, y=40.0)

    # Crear un Canvas para el área desplazable, ahora ajustado debajo del Frame superior
    scroll_canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=501,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    scroll_canvas.place(x=267, y=80)

    # Añadir un Scrollbar al Canvas
    scrollbar = Scrollbar(window, orient=VERTICAL, command=scroll_canvas.yview)
    scrollbar.place(x=1050, y=80, height=501)

    # Configurar el Canvas para el scroll
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un Frame dentro del Canvas para contener los eventos
    event_frame = Frame(scroll_canvas, bg="#FFFFFF")
    scroll_canvas.create_window((0, 0), window=event_frame, anchor='nw')

    # Cargar y mostrar eventos
    eventos = cargar_eventos()  # Cargar los eventos reales desde el JSON
    if not eventos:
        eventos = [{"nombre": "Este es un evento de prueba con una descripción larga", "flyer": "default_flyer.png"}] * 10  # Eventos de prueba

    # Definir el tamaño de la cuadrícula
    rows, columns = 3, 2  # 3 rows, 2 columns por pantalla (6 eventos por pantalla)
    matriz_eventos = [eventos[i:i+columns] for i in range(0, len(eventos), columns)]

    # Mostrar los eventos en la cuadrícula
    for i, fila_eventos in enumerate(matriz_eventos):
        for j, evento in enumerate(fila_eventos):
            try:
                flyer_path = relative_to_flyers(evento.get('flyer', 'default_flyer.png'))
                flyer_image = cargar_imagen_redimensionada(flyer_path, size=(100, 100))
                if flyer_image:
                    # Mostrar el flyer
                    flyer_label = Label(event_frame, image=flyer_image, bg="#FFFFFF")
                    flyer_label.image = flyer_image
                    flyer_label.grid(row=i, column=j*2, padx=(10, 25), pady=10)

                    # Mostrar la información del evento
                    info_label = Label(event_frame, text=evento['nombre'], bg="#FFFFFF", font=("Inter", 10), wraplength=200, justify="left")
                    info_label.grid(row=i, column=j*2+1, padx=10, pady=10)
            except Exception as e:
                print(f"Error al cargar el evento: {e}")

    # Configurar el área desplazable
    event_frame.update_idletasks()
    scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))

    # Añadir los botones estáticos
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        window,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1 clicked"),
        relief="flat"
    )
    button_1.place(x=51.0, y=192.0, width=206.0, height=80.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        window,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2 clicked"),
        relief="flat"
    )
    button_2.place(x=51.0, y=424.0, width=206.0, height=80.0)

    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        window,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    button_3.place(x=51.0, y=308.0, width=206.0, height=80.0)

    button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
    button_4 = Button(
        window,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4 clicked"),
        relief="flat"
    )
    button_4.place(x=51.0, y=76.0, width=206.0, height=80.0)

    window.resizable(False, False)
    window.mainloop()
