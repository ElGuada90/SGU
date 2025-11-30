###################################
""" Ventana de Inicio de Sesion"""
###################################

""" Bloque de configuraciones """

# importar librerias
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

# importar modulos
from modulo_resource_path import resource_path
from modulo_sesion import iniciar_sesion
from ventana_menuctk import ventana_principal
from modulo_conexion_mysql import ConexionMySQL


# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# enlace o ruta de imagenes
logo = resource_path("static\\images\\Logo Python.png")
icon = resource_path("static\\images\\Logo Python ico.ico")

#####################
# Crear ventana login
#####################
class VentanaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestion Unico")
        self.iconbitmap(icon)
        self.geometry("1280x720+150+8")
        self.resizable(True, True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # cargar imagen de logo
        self.logo_image = ctk.CTkImage(light_image=Image.open(logo), size=(50, 50))

        # Creamos las variables Globales para los intentos de inicio de sesión
        self.intentos = 0
        self.max_intentos = 3

        """ Bloque de widgets """

        # crear marco de ventana
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.grid(row=0, column=0, padx=10, pady=(10), sticky="nsew")
        self.frame_login.grid_columnconfigure(0, weight=1)
        self.frame_login.grid_rowconfigure(0, weight=1)

        # crear marco de fondo de ventana
        self.frame_back = ctk.CTkFrame(self.frame_login)
        self.frame_back.grid(row=0, column=0, padx=10, pady=10, sticky="")
        self.frame_back.grid_columnconfigure(0, weight=1)
        self.frame_back.grid_rowconfigure(0, weight=1)

        # crear marco de color de fondo de ventana interna
        self.frame_color = ctk.CTkFrame(self.frame_back, fg_color="#02243F")
        self.frame_color.grid(row=0, column=0, padx=10, pady=10, sticky="")
        self.frame_color.grid_columnconfigure(0, weight=1)
        self.frame_color.grid_rowconfigure(0, weight=1)

        # crear widgets de entrada
        self.label_logo = ctk.CTkLabel(self.frame_color, 
                                image=self.logo_image, 
                                text="", 
                                font=ctk.CTkFont(family="verdana", size=20, weight="bold"), 
                                width=250, 
                                height=40)
        self.label_logo.grid(row=0, column=0, padx=10, pady=(10))

        self.label_titulo = ctk.CTkLabel(self.frame_color, text="SESION", font=ctk.CTkFont(family="verdana", size=20, weight="bold"))
        self.label_titulo.grid(row=1, column=0, padx=10, pady=10)

        self.entrada_usuario = ctk.CTkEntry(self.frame_color, placeholder_text="Ingrese Usuario...", width=200, height=40)
        self.entrada_usuario.grid(row=2, column=0, padx=5, pady=5)

        self.entrada_contraseña = ctk.CTkEntry(self.frame_color, placeholder_text="Ingrese Contraseña...", show="*", width=200, height=40)
        self.entrada_contraseña.grid(row=3, column=0, padx=5, pady=5)

        self.checkbox_var = ctk.StringVar(value="off")
        self.checkbox_recordar = ctk.CTkCheckBox(self.frame_color, 
                                            text="Mostrar Contraseña", 
                                            font=ctk.CTkFont(family="verdana", size=12, weight="bold"), 
                                            command=self.mostrar_password,  
                                            variable=self.checkbox_var, 
                                            onvalue="on", 
                                            offvalue="off")
        self.checkbox_recordar.grid(row=4, column=0, padx=10, pady=10)

        self.boton_login = ctk.CTkButton(self.frame_color, text="Iniciar Sesión", command=self.validar_credenciales)
        self.boton_login.grid(row=5, column=0, padx=10, pady=10)

        self.label_footer = ctk.CTkLabel(self, 
                                    text=f"Copyright © 2025\nPython Hack: by ElGuada90", 
                                    font=ctk.CTkFont(family="verdana", 
                                    size=10, 
                                    weight="bold"))
        self.label_footer.grid(row=1, column=0, padx=10, pady=10)
        # Vinculamos la tecla "Enter" o "Return" a la función que valida las credenciales.
        # Usamos un "wrapper" para manejar el objeto de evento que Tkinter pasa automáticamente.
        self.bind("<Return>", self.validar_credenciales_con_evento)

    ###########################
    """ Bloque de funciones """
    ###########################

    # Funcion para activar el checkbox
    def mostrar_password(self):
        if self.checkbox_var.get() == "on":
            self.entrada_contraseña.configure(show="")
        else:
            self.entrada_contraseña.configure(show="*")

    # Funcion para definir las listas de usuarios, contraseñas y roles
    def bd_container(self):
        """ Contenedors para almacenar datos tipo lista """
        self.usuarios = ['sgu01', 'sgu02', 'sgu03']
        self.contraseñas = ['su12345_', 'ad12345*', 'u12345#']
        self.roles = ['SuperUser', 'admin', 'user']
        self.nombres = []
        self.apellidos = []
        self.emails = []
        self.telefonos = []
        self.fecha_registro = []
        return self.usuarios, self.contraseñas, self.roles

    # Esta función actuará como un "wrapper" o envoltorio para el evento de teclado
    def validar_credenciales_con_evento(self, event=None):
        self.validar_credenciales()

    # Función para validar las credenciales
    def validar_credenciales(self):
       

        usuarios, contraseñas, roles = self.bd_container()

        usuario = self.entrada_usuario.get().lower()
        contraseña = self.entrada_contraseña.get().lower()

        sesion_exitosa = iniciar_sesion(usuarios, contraseñas, roles, usuario, contraseña)

        if sesion_exitosa:
            #try:
                #rol = roles[usuarios.index(usuario)]
            rol = sesion_exitosa if isinstance(sesion_exitosa, str) else "Rol no definido"
            messagebox.showinfo("Inicio de Sesión", f"Bienvenido Usuario: {usuario}\nRol: {rol}")
                # Limpia los campos de entrada al tener éxito
            self.entrada_usuario.delete(0, 'end')
            self.entrada_contraseña.delete(0, 'end')
            #except ValueError:
                #messagebox.showinfo("Inicio de Sesión", f"Bienvenido {usuario}, Rol no definido.")
            """ Ingreso a la ventana principal """
            self.destroy()  # Cerrar la ventana de login
            #ventana_usuarios(usuario, rol) # Abrir la ventana principal
            ventana_principal(usuario, rol)
        else:
            self.intentos += 1
            if self.intentos >= self.max_intentos:
                messagebox.showerror("Inicio de Sesión", "Máximo de intentos alcanzado")
                self.destroy()  # Cerrar la ventana de login

            else:
                messagebox.showerror("Inicio de Sesión", "Usuario o contraseña incorrectos")
                # Limpia los campos de entrada al fallar
                self.entrada_usuario.delete(0, 'end')
                self.entrada_contraseña.delete(0, 'end')

#######################################################
""" Bloque de inicializacion de la ventana de login """
#######################################################

if __name__ == "__main__":
    sgu = VentanaLogin()
    sgu.mainloop()


