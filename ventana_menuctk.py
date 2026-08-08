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
from matplotlib.patches import FancyBboxPatch
from matplotlib import patheffects as pe
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

def aplicar_bordes_redondeados(fig, ax, color_fondo="#14213d", color_borde="#5dade2"):
    fig.patch.set_facecolor(color_fondo)

    rounded_box = FancyBboxPatch(
        (-0.02, -0.02), 1.04, 1.04,
        boxstyle="round,pad=0.0,rounding_size=0.06",
        transform=fig.transFigure,
        linewidth=1.9,
        edgecolor=color_borde,
        facecolor=color_fondo,
        zorder=-1,
    )
    rounded_box.set_path_effects([
        pe.withStroke(linewidth=3, foreground="black", alpha=0.22)
    ])
    fig.add_artist(rounded_box)

    ax.set_facecolor(color_fondo)
    ax.set_position([0.07, 0.12, 0.86, 0.74])
    ax.set_zorder(1)

# funcion para crear la ventana principal
def ventana_principal(usuario, rol):
    ventana_principal = ctk.CTk()
    ventana_principal.title("Sistema de Gestion Unico")
    ventana_principal.iconbitmap(icon)
    ventana_principal.geometry("1280x720+0+0")
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
        fig = Figure(figsize=(6.2, 3.4), dpi=100)
        ax = fig.add_subplot(111)
        aplicar_bordes_redondeados(fig, ax)
        fig.subplots_adjust(left=0.08, right=0.98, top=0.90, bottom=0.24)

        # Crear gráfico de barras
        ax.bar(nombres, valores)
        ax.set_title("Ventas por Vendedor", color="white")
        ax.set_ylabel("Monto Vendido", color="white")
        ax.tick_params(axis='x', rotation=35, labelsize=7, colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color("white")
        fig.subplots_adjust(bottom=0.25)  # Aumenta margen inferior

        # Insertar en el frame
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico1)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=8, pady=8)

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
        fig = Figure(figsize=(6.2, 3.4), dpi=100)
        ax = fig.add_subplot(111, aspect='equal')
        aplicar_bordes_redondeados(fig, ax)
        fig.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.10)

        # Gráfico donut
        wedges, texts = ax.pie(
            valores,
            wedgeprops=dict(width=0.5),
            startangle=50
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
            if valores[i] / total < 0.02:   # menos de 2%
                ang += 8
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
                xytext=(1.35 * x, 1.35 * y),
                horizontalalignment=alineacion,
                **kw
            )

        ax.set_title("Ventas por Categoría", fontsize=11, color="white")
        ax.set_ylabel("", color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color("white")

        # Limpiar frame antes de dibujar
        for widget in frame_grafico2.winfo_children():
            widget.destroy()

        # Mostrar gráfico en customtkinter
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico2)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=8, pady=8)


    def grafico_promedio_ventas(frame_grafico3):
        conexion = ConexionMySQL()
        query = """
            SELECT FLOOR(AVG(valor)) AS Promedio FROM ventas
        """
        datos = conexion.obtener_datos(query)
        
        promedio = datos[0]["Promedio"] 

        # Crear figura
        fig = Figure(figsize=(5.2, 3.8), dpi=100)
        ax = fig.add_subplot(111)
        aplicar_bordes_redondeados(fig, ax)

        # Datos reales
        barras = ax.bar(["Valor Promedio"], [promedio])
        ax.set_title("Promedio de Ventas", color="white")
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color("white")
        #ax.set_ylabel("Valor Promedio")

        # Obtener referencia de la única barra
        barra = barras[0]

        # Coordenadas del centro de la barra
        x = barra.get_x() + barra.get_width() / 2
        y = promedio / 2

        ax.text(
            x, y,
            str(promedio),
            ha="center",
            va="center",
            fontsize=50,
            color="white",      # si fondo es azul se verá mejor
            fontweight="bold"
        )

        # Crear lienzo dentro del frame
        canvas = FigureCanvasTkAgg(fig, master=frame_grafico3)
        canvas.draw()

        # Colocar el gráfico dentro del frame
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True, padx=8, pady=8)

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

    # --- Bloque de Frame para barra de navegación ---
    nav_frame = ctk.CTkFrame(ventana_principal, corner_radius=8) 
    nav_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_rowconfigure(0, weight=1)

    # ----- PRIMER OPTIONMENU (FILE) -----
    opciones_file = ["Usuarios", "Productos", "Ventas", "Exit"]

    menu_opciones = ctk.CTkOptionMenu(nav_frame,
                                values=opciones_file,
                                command=ejecutar_menu,
                                width=200)
    menu_opciones.set("Menu Principal")  # Texto inicial
    menu_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Label de bienvenida
    label = ctk.CTkLabel(nav_frame,
                        text=f'Bienvenido! {usuario}, Rol: {rol}',
                        font=ctk.CTkFont(family="candara", size=16, weight="bold"),
                        fg_color="#0078d7",
                        #bg_color="darkblue",
                        corner_radius=5,
                        #height=40 
                        )
    label.grid(row=0, column=0, padx=5, pady=8, sticky="e")
    
    """ Bloque de Frames """
    frame_principal = ctk.CTkFrame(ventana_principal)
    frame_principal.grid(row=1, column=0, padx=15, pady=2, sticky="nsew")
    frame_principal.grid_columnconfigure((0,1), weight=1)
    frame_principal.grid_rowconfigure((0,1), weight=1)

    frame_grafico1 = ctk.CTkFrame(frame_principal, fg_color="#02243F", corner_radius=20, border_width=1)
    frame_grafico1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    frame_grafico1.grid_columnconfigure(0, weight=1)
    frame_grafico1.grid_rowconfigure(0, weight=1)

    frame_grafico2 = ctk.CTkFrame(frame_principal, fg_color="#02243F", corner_radius=20, border_width=1)
    frame_grafico2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    frame_grafico2.grid_columnconfigure(0, weight=1)
    frame_grafico2.grid_rowconfigure(0, weight=1)

    frame_grafico3 = ctk.CTkFrame(frame_principal, fg_color="#02243F", corner_radius=20, border_width=1)
    frame_grafico3.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
    frame_grafico3.grid_columnconfigure(0, weight=1)
    frame_grafico3.grid_rowconfigure(0, weight=1)

    grafico_ventas_por_vendedor(frame_grafico1)
    grafico_ventas_por_categoria(frame_grafico2)
    grafico_promedio_ventas(frame_grafico3)

    footer_label = ctk.CTkLabel(ventana_principal, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright © 2025 * Python Hack ElGuada90",
                                corner_radius=5)
    footer_label.grid(row=2, column= 0, columnspan=2, padx=5, pady=5, sticky="s" )

    ventana_principal.mainloop()