from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/change_password")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("576x554")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 554,
    width = 576,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=190.0,
    y=460.0,
    width=196.0,
    height=54.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    304.0,
    293.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=112.0,
    y=269.0,
    width=384.0,
    height=47.0
)

canvas.create_text(
    70.0,
    215.0,
    anchor="nw",
    text="Contraseña anterior:",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    304.0,
    176.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=112.0,
    y=152.0,
    width=384.0,
    height=47.0
)

canvas.create_text(
    70.0,
    98.0,
    anchor="nw",
    text="Contraseña anterior:",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    304.0,
    403.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=112.0,
    y=379.0,
    width=384.0,
    height=47.0
)

canvas.create_text(
    70.0,
    325.0,
    anchor="nw",
    text="Nueva Contraseña:",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

canvas.create_text(
    81.0,
    21.0,
    anchor="nw",
    text="Cambiar Contraseña",
    fill="#000000",
    font=("AndadaPro ExtraBold", 40 * -1)
)
window.resizable(False, False)
window.mainloop()
