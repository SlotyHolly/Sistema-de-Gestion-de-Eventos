
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\recovery_password")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("567x450")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 450,
    width = 567,
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
    x=184.99999999999994,
    y=381.0,
    width=196.0,
    height=54.0
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    282.99999999999994,
    319.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=134.99999999999994,
    y=285.0,
    width=296.0,
    height=67.0
)

canvas.create_text(
    134.99999999999994,
    301.0,
    anchor="nw",
    text="Nueva Contraseña",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    282.99999999999994,
    224.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=134.99999999999994,
    y=190.0,
    width=296.0,
    height=67.0
)

canvas.create_text(
    136.99999999999994,
    207.0,
    anchor="nw",
    text="Codigo",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    283.99999999999994,
    132.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=135.99999999999994,
    y=98.0,
    width=296.0,
    height=67.0
)

canvas.create_text(
    136.99999999999994,
    114.0,
    anchor="nw",
    text="Usuario\n",
    fill="#000000",
    font=("AndadaPro Bold", 32 * -1)
)

canvas.create_text(
    108.99999999999994,
    23.0,
    anchor="nw",
    text="Recuperar Contraseña",
    fill="#000000",
    font=("AndadaPro ExtraBold", 32 * -1)
)
window.resizable(False, False)
window.mainloop()
