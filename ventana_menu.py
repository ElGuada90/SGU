# importar libreria que activa la ventana

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch
from matplotlib import patheffects as pe
import matplotlib.pyplot as plt
from modulo_conexion_mysql import ConexionMySQL

# importar modulos 
from modulo_resource_path import resource_path

# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# enlace de ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")

class VentanaMenuPrincipal(ctk.CTk):
    def __init__(self, usuario=None, rol=None):
        super().__init__()
        self.usuario = usuario
        self.rol = rol
        self.title("Sistema de Gestion Unico")
        self.iconbitmap(icon)
        self.geometry("1280x720+0+0")
        self.resizable(True, True)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2), weight=1)  

        """ Bloque de Header """
        # Funcion para el OptionMMenu
        def ejecutar_menu(opcion):
            if opcion == "Usuarios":
                pass #abrir_usuarios()
            elif opcion == "Productos":
                pass #abrir_productos()
            elif opcion == "Ventas":
                pass #abrir_ventas()
            elif opcion == "Exit":
                self.destroy() 

        # Barra de navegacion
        self.navbar = ctk.CTkFrame(self, corner_radius=8)
        self.navbar.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="new")
        self.navbar.grid_columnconfigure(0, weight=1)
        self.navbar.grid_rowconfigure(0, weight=1)

        # ----- PRIMER OPTIONMENU (FILE) -----
        self.opciones_file = ["Usuarios", "Productos", "Ventas", "Exit"]

        self.menu_opciones = ctk.CTkOptionMenu(self.navbar,
                                    values=self.opciones_file,
                                    command=ejecutar_menu,
                                    width=200)
        self.menu_opciones.set("Menu Principal")  # Texto inicial
        self.menu_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Label de bienvenida  
        self.label_bienvenida = ctk.CTkLabel(self.navbar,
                        text=f'Bienvenido! {self.usuario.upper()}, Rol: {self.rol}',
                        font=ctk.CTkFont(family="candara", size=16, weight="bold"),
                        fg_color="#0078d7",
                        #bg_color="darkblue",
                        corner_radius=5)
                        #height=40               
        self.label_bienvenida.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    
        """ Bloque de Dashboard """
        self.frame_grafico1 = ctk.CTkFrame(self, fg_color="#02243F", corner_radius=20, border_width=1)
        self.frame_grafico1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_grafico2 = ctk.CTkFrame(self, fg_color="#02243F", corner_radius=20, border_width=1)
        self.frame_grafico2.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")  

        self.frame_grafico3 = ctk.CTkFrame(self, fg_color="#02243F", corner_radius=20, border_width=1)
        self.frame_grafico3.grid(row=1, rowspan=2, column=1, padx=10, pady=10, sticky="nsew")      

        self.footer_label = ctk.CTkLabel(self, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright 2025 © Python Hack ElGuada90",
                                corner_radius=5)
        self.footer_label.grid(row=3, column= 0, columnspan=2, padx=10, pady=10, sticky="s" )

#######################################################
""" Bloque de inicializacion de la ventana de login """
#######################################################

if __name__ == "__main__":
    sgu = VentanaMenuPrincipal()
    sgu.mainloop()