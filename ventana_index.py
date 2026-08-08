###################################
""" Ventana de Index """
###################################

""" Bloque de configuraciones """

# importar librerias
import customtkinter as ctk
from PIL import Image

# importar modulos
from modulo_resource_path import resource_path
from ventana_loginctk import VentanaLogin

# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# enlace o ruta de imagenes
logo = resource_path("static\\images\\logo-python_convert.png")
icon = resource_path("static\\images\\Logo Python ico.ico")

#####################
# Crear ventana index
#####################
class VentanaIndex(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestion Unico")
        self.iconbitmap(icon)
        self.geometry("1280x720+0+0")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # cargar imagen de logo
        self.logo_image = ctk.CTkImage(light_image=Image.open(logo), size=(550, 350))

         # crear marco de ventana
        self.frame_index = ctk.CTkFrame(self)
        self.frame_index.grid(row=0, column=0, padx=10, pady=(10), sticky="nsew")
        self.frame_index.grid_columnconfigure(0, weight=1)
        self.frame_index.grid_rowconfigure(0, weight=1)

        # crear widgets de entrada
        self.label_logo = ctk.CTkLabel(self.frame_index, 
                                image=self.logo_image, 
                                text="", 
                                font=ctk.CTkFont(family="verdana", size=20, weight="bold"), 
                                width=250, 
                                height=40)
        self.label_logo.grid(row=0, column=0, padx=10, pady=(125, 1))

        self.boton_login = ctk.CTkButton(
            self.frame_index,
            text="Iniciar Sesión",
            command=self.abrir_ventana_login,
            font=ctk.CTkFont(family="verdana", size=20, weight="bold")
        )
        self.boton_login.grid(row=1, column=0, padx=10, pady=(1,100))

        # Vinculamos la tecla "Enter" o "Return" a la función que abre la ventana de login.
        self.bind("<Return>", self.abrir_ventana_login)

        self.label_footer = ctk.CTkLabel(
            self,
            text=f"Copyright © 2025 * Python Hack: by ElGuada90",
            font=ctk.CTkFont(family="verdana", size=10, weight="bold")
        )
        self.label_footer.grid(row=1, column=0, padx=10, pady=10)
        

    def abrir_ventana_login(self, event=None):
        self.destroy()
        ventana_login = VentanaLogin()
        ventana_login.mainloop()

#######################################################
""" Bloque de inicializacion de la ventana de index """
#######################################################

if __name__ == "__main__":
    sgu = VentanaIndex()
    sgu.mainloop()