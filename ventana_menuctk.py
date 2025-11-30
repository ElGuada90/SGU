""" Ventana de menu principal """

""" Bloque de Configuración """
# importamos librerias
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Frame, Menu
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from modulo_conexion_mysql import ConexionMySQL


# Importamos modulos
from modulo_resource_path import resource_path
from modulo_conexion_mysql import ConexionMySQL
from ventana_usuariosctk import ventana_usuarios



# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
# enlace o ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")

# funcion para crear la ventana principal
def ventana_principal(usuario, rol):
    ventana_principal = ctk.CTk()
    ventana_principal.title("Sistema de Gestion Unico")
    ventana_principal.iconbitmap(icon)
    ventana_principal.geometry("1280x720+150+8")
    ventana_principal.resizable(True, True)
    ventana_principal.grid_columnconfigure(0, weight=1)
    ventana_principal.grid_rowconfigure(1, weight=1)

    # --- Parametros Globales
    usuario = usuario
    rol = rol

    """ Función para abrir la ventana de usuarios """
    def abrir_usuarios():
        # cerramos la ventana principal
        ventana_principal.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_usuarios(usuario, rol)

    """ Función para abrir la ventana de productos """
    def abrir_productos():
        from ventana_productosctk import ventana_productos
        # cerramos la ventana principal
        ventana_principal.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_productos(usuario, rol)

    """ Función para abrir la ventana de ventas """
    def abrir_ventas():
        from ventana_ventasctk import ventana_ventas
        # cerramos la ventana principal
        ventana_principal.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_ventas(usuario, rol)

    """ Bloque de Funciones para Graficos """
    def grafico_ventas_por_vendedor(frame_grafico1):
        conexion = ConexionMySQL()
        query = """
            SELECT 
                v.valor,
                CONCAT(u.nombre, ' ', u.apellido) AS nombre
            FROM ventas v
            LEFT JOIN usuarios u ON v.id_usuario = u.id
            ORDER BY v.valor DESC;
        """
        datos = conexion.obtener_datos(query)

        if not datos:
            messagebox.showwarning("Aviso", "No hay datos de ventas para mostrar.")
            return

        # Extraer datos para el gráfico
        nombres = [fila["nombre"] for fila in datos]
        valores = [float(fila["valor"]) for fila in datos]

        # Crear la figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        # Crear gráfico de barras
        ax.bar(nombres, valores)
        ax.set_title("Ventas por Vendedor")
        ax.set_xlabel("Vendedor", fontsize=8)
        ax.set_ylabel("Monto Vendido")
        ax.tick_params(axis='x', rotation=25)

        # Insertar en el frame
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico1)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

    ##### Ventas por categoria      

    def grafico_ventas_por_categoria(frame_grafico2):
        import math
        conexion = ConexionMySQL()
        query = """
            SELECT
                SUM(v.valor) AS ventas,
                p.categoria
            FROM ventas v
            LEFT JOIN productos p
                ON v.id_producto = p.id
            GROUP BY p.categoria;
        """
        datos = conexion.obtener_datos(query)

        if not datos:
            messagebox.showwarning("Aviso", "No hay datos de ventas para mostrar.")
            return

        # Extraer datos para el gráfico
        nombres = [fila["categoria"] for fila in datos]
        valores = [float(fila["ventas"]) for fila in datos]

         # Crear figura
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111, aspect='equal')

        # Gráfico donut
        wedges, texts = ax.pie(
            valores,
            wedgeprops=dict(width=0.5),
            startangle=90
        )

        # Estilo de etiquetas externas con flechas
        bbox_props = dict(boxstyle="square,pad=0.3", fc="white", ec="black", lw=0.7)
        kw = dict(
            arrowprops=dict(arrowstyle="-"),
            bbox=bbox_props,
            zorder=10,
            va="center"
        )

        total = sum(valores)

        # ---- ANOTACIONES SIN NUMPY ----
        for i, wedge in enumerate(wedges):
            ang = (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1
            ang_rad = math.radians(ang)

            # Posiciones para la anotación
            x = math.cos(ang_rad)
            y = math.sin(ang_rad)

            alineacion = "left" if x > 0 else "right"

            porcentaje = f"{(valores[i] / total) * 100:.1f}%"
            texto = f"{nombres[i]} — {porcentaje}"

            # Estilo y posición de anotación
            ax.annotate(
                texto,
                xy=(x * 0.7, y * 0.7),
                xytext=(1.2 * x, 1.2 * y),
                horizontalalignment=alineacion,
                **kw
            )

        ax.set_title("Ventas por Categoría", fontsize=11)

        # Limpiar frame antes de dibujar
        for widget in frame_grafico2.winfo_children():
            widget.destroy()

        # Mostrar gráfico en customtkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def grafico_promedio_ventas(frame_grafico3):
        conexion = ConexionMySQL()
        query = """
            SELECT FLOOR(AVG(valor)) AS Promedio FROM ventas
        """
        datos = conexion.obtener_datos(query)
        
        promedio = datos[0]["Promedio"] 

        # Crear figura
        fig = Figure(figsize=(4, 3), dpi=100)
        ax = fig.add_subplot(111)

        # Datos reales
        ax.bar(["Promedio Ventas"], [promedio])
        ax.set_title("Promedio de Ventas")
        ax.set_ylabel("Valor Promedio")

        # Crear lienzo dentro del frame
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico3)
        canvas.draw()

        # Colocar el gráfico dentro del frame
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)

    # Funcion para el OptionMMenu
    def ejecutar_menu(opcion):
        if opcion == "Usuarios":
            abrir_usuarios()
        elif opcion == "Productos":
            abrir_productos()
        elif opcion == "Ventas":
            abrir_ventas()
        elif opcion == "Exit":
            ventana_principal.destroy()    

    frame_menu = ctk.CTkFrame(ventana_principal)
    frame_menu.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # ----- PRIMER OPTIONMENU (FILE) -----
    opciones_file = ["Usuarios", "Productos", "Ventas", "Exit"]

    menu_opciones = ctk.CTkOptionMenu(frame_menu,
                                values=opciones_file,
                                command=ejecutar_menu,
                                width=200)
    menu_opciones.set("Menu Principal")  # Texto inicial
    menu_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    
    """ Bloque de Frames """
    frame_principal = ctk.CTkFrame(ventana_principal)
    frame_principal.grid(row=1, column=0, padx=10, pady=2, sticky="nsew")
    frame_principal.grid_columnconfigure((0,1), weight=1)
    frame_principal.grid_rowconfigure((0,1), weight=1)

    frame_grafico1 = ctk.CTkFrame(frame_principal, fg_color="#02243F")
    frame_grafico1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame_grafico1.grid_columnconfigure(0, weight=1)
    frame_grafico1.grid_rowconfigure(0, weight=1)

    frame_grafico2 = ctk.CTkFrame(frame_principal, fg_color="#02243F")
    frame_grafico2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    frame_grafico2.grid_columnconfigure(0, weight=1)
    frame_grafico2.grid_rowconfigure(0, weight=1)

    frame_grafico3 = ctk.CTkFrame(frame_principal, fg_color="#02243F")
    frame_grafico3.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    frame_grafico3.grid_columnconfigure(0, weight=1)
    frame_grafico3.grid_rowconfigure(0, weight=1)

    grafico_ventas_por_vendedor(frame_grafico1)
    grafico_ventas_por_categoria(frame_grafico2)
    grafico_promedio_ventas(frame_grafico3)

    ventana_principal.mainloop()