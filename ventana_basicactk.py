# Importacion de librerias
import customtkinter as ctk

# Bloque de configuracion de temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# función para el callback del boton
def button_callback():
    print("button clicked")

# Bloque de Configuracion de la ventana
app = ctk.CTk()
app.geometry("800x450+350+100") # Dimensiones y posicion de la ventana
app.title("Ventana de prueba") # Titulo de la ventana
app.configure(fg_color="dark gray") # Color de fondo de la ventana


# Bloque de Widgets
button = ctk.CTkButton(app, text="my button", command=button_callback)
button.pack(padx=20, pady=20)

# Inicializar la ventana
app.mainloop()





