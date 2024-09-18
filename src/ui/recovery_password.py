from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from functions.password import recovery_password  # Importamos la función para la recuperación de contraseña

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\recovery_password")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def init_recovery_password():
    window = Tk()
    window.geometry("470x571")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=571,
        width=470,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Crear los campos de entrada
    entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(221.99999999999994, 145.5, image=entry_image_1)
    entry_user = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_user.place(x=78.99999999999994, y=121.0, width=286.0, height=47.0)

    entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(221.99999999999994, 262.5, image=entry_image_2)
    entry_code = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_code.place(x=78.99999999999994, y=238.0, width=286.0, height=47.0)

    entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
    entry_bg_3 = canvas.create_image(221.99999999999994, 373.5, image=entry_image_3)
    entry_new_password = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
    entry_new_password.place(x=78.99999999999994, y=349.0, width=286.0, height=47.0)

    # Función para manejar el cambio de contraseña
    def handle_recovery():
        username = entry_user.get()
        code = entry_code.get()
        new_password = entry_new_password.get()

        if not username or not new_password:
            messagebox.showerror("Error", "Por favor, ingresa un nombre de usuario y una nueva contraseña.")
            return

        if code == "1234" and not entry_code.get():
            # Mostrar mensaje con el código por defecto
            messagebox.showinfo("Código de Recuperación", "El código de recuperación es: 1234")
        
        # Llamar a la función de recuperación de contraseña
        result = recovery_password(username, code, new_password)
        if result['success']:
            messagebox.showinfo("Éxito", "La contraseña ha sido cambiada exitosamente.")
            window.destroy()  # Cerrar la ventana después de la recuperación exitosa
        else:
            messagebox.showerror("Error", result['message'])

    # Botones
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=handle_recovery,  # Llama a handle_recovery cuando se hace clic
        relief="flat"
    )
    button_1.place(x=136.99999999999994, y=420.0, width=196.0, height=54.0)

    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=window.destroy,  # Cierra la ventana cuando se hace clic
        relief="flat"
    )
    button_2.place(x=136.99999999999994, y=487.0, width=196.0, height=57.0)

    # Etiquetas y títulos
    canvas.create_text(24.999999999999943, 290.0, anchor="nw", text="Nueva Contraseña", fill="#000000", font=("AndadaPro Bold", 32 * -1))
    canvas.create_text(24.999999999999943, 180.0, anchor="nw", text="Código", fill="#000000", font=("AndadaPro Bold", 32 * -1))
    canvas.create_text(24.999999999999943, 68.0, anchor="nw", text="Usuario\n", fill="#000000", font=("AndadaPro Bold", 32 * -1))
    canvas.create_text(59.99999999999994, 15.0, anchor="nw", text="Recuperar Contraseña", fill="#000000", font=("AndadaPro ExtraBold", 32 * -1))

    window.resizable(False, False)
    window.mainloop()
