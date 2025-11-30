""" VENTANA DE PRODUCTOS"""

""" Bloque de Configuración """
# importamos librerias
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Frame, Menu
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importamos modulos
from modulo_resource_path import resource_path
from modulo_conexion_mysql import ConexionMySQL

from ventana_usuariosctk import ventana_usuarios
from ventana_ventasctk import ventana_ventas

# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
# enlace o ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")

# funcion para crear la ventana productos
def ventana_productos(usuario, rol):

    lupa = resource_path("static\\images\\Lupa Blanca.png")
    lupa_icon = ctk.CTkImage(light_image=Image.open(lupa), size=(25, 25))
    delete = resource_path("static\\images\\delete.png")
    delete_icon = ctk.CTkImage(light_image=Image.open(delete), size=(25, 25))
    
    ventana_productos = ctk.CTk()
    ventana_productos.title("Sistema de Gestion Unico")
    ventana_productos.iconbitmap(icon)
    ventana_productos.geometry("1280x720+150+8")
    ventana_productos.resizable(True, True)
    ventana_productos.grid_columnconfigure(1, weight=1)
    ventana_productos.grid_rowconfigure(1, weight=1)

    """ Bloque de Funciones """
    # Crear instancia de conexión
    db = ConexionMySQL()


    """ Función para obtener todos los datos de productos """
    def cargar_productos():
        #limpiar_campos()
        for fila in treeview.get_children():
            treeview.delete(fila)

        query = "SELECT id, producto, categoria FROM productos"
        resultados = db.obtener_datos(query)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["id"], fila["producto"], fila["categoria"]
            ))


    """ Función para volver al menú producto """
    def volver_menu_ventanas():
        # Importación tardía para evitar la importación circular
        from ventana_menuctk import ventana_principal
        ventana_productos.destroy()  # Cerrar ventana actual
        ventana_principal(usuario, rol)  # Abrir menú

    """ Función para abrir la ventana de usuarios """
    def abrir_usuarios():
        # cerramos la ventana producto
        ventana_productos.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_usuarios(usuario, rol)

    """ Función para abrir la ventana de ventas """
    def abrir_ventas():
        # cerramos la ventana producto
        ventana_productos.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_ventas(usuario, rol)

    """ Función para manejar las opciones del menú """
    # Funcion para el OptionMMenu
    def ejecutar_menu(opcion):
        if opcion == "Menu Principal":
            volver_menu_ventanas()
        elif opcion == "Usuarios":
            abrir_usuarios()
        elif opcion == "Ventas":
            abrir_ventas()
        elif opcion == "Exit":
            ventana_productos.destroy()    

    """ Bloque de Menu """
    # --- Bloque de Frame para barra de navegación ---
    
    nav_frame = ctk.CTkFrame(ventana_productos, corner_radius=8) 
    nav_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_rowconfigure(0, weight=1)

    # widget de meunu de ventanas
    # ----- PRIMER OPTIONMENU (FILE) -----
    opciones_file = ["Menu Principal", "Usuarios", "Ventas", "Exit"]

    menu = ctk.CTkOptionMenu(nav_frame, values=opciones_file, command=ejecutar_menu, width=200)
    menu.set("Productos")
    menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    form_frame = ctk.CTkFrame(ventana_productos, corner_radius=8) 
    form_frame.grid(row=1, column=0, padx=(15,2), pady=1, sticky="nsew")

    label_producto = ctk.CTkLabel(form_frame, text='Producto')
    label_producto.grid(row=4, column=0, padx=10, pady=2, sticky="nw")

    producto_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Producto...',
                                  height=40)
    producto_entry.grid(row=5, column=0, padx=(10,2), pady=2, sticky='new')

    label_descripcion = ctk.CTkLabel(form_frame, text='Descripcion')
    label_descripcion.grid(row=4, column=1, columnspan=2, padx=10, pady=2, sticky="nw")

    descripcion_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Descripcion...',
                                  height=40)
    descripcion_entry.grid(row=5, column=1, columnspan=2, padx=(2,10), pady=2, sticky='new')

    label_marca = ctk.CTkLabel(form_frame, text='Marca')
    label_marca.grid(row=6, column=0, padx=10, pady=(12,2), sticky="nw")

    marca_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Marca...',
                                  height=40)
    marca_entry.grid(row=7, column=0, padx=(10,2), pady=2, sticky='new')

    label_categoria = ctk.CTkLabel(form_frame, text='Categoria')
    label_categoria.grid(row=6, column=1, padx=(10,2), pady=(10,2), sticky="nw")

    categoria_combobox = ctk.CTkComboBox(form_frame, height=40, state="readonly")
    categoria_combobox.grid(row=7, column=1, padx=(2,2), pady=2, sticky='new')
    categoria_combobox.set("Seleccione..")

    label_subcategoria = ctk.CTkLabel(form_frame, text='Sub-Categoria')
    label_subcategoria.grid(row=6, column=2, padx=(2,10), pady=(10,2), sticky="nw")

    subcategoria_combobox = ctk.CTkComboBox(form_frame, height=40, state="readonly")
    subcategoria_combobox.grid(row=7, column=2, padx=(2,10), pady=2, sticky='new')
    subcategoria_combobox.set("Seleccione..")

    label_codigo = ctk.CTkLabel(form_frame, text='Codigo')
    label_codigo.grid(row=8, column=0, padx=10, pady=2, sticky="nw")

    codigo_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Codigo...',
                                  height=40)
    codigo_entry.grid(row=9, column=0, padx=(10,2), pady=(2,10), sticky='new')

    label_inventario = ctk.CTkLabel(form_frame, text='Cantidad')
    label_inventario.grid(row=8, column=1, padx=(2,2), pady=2, sticky="nw")

    inventario_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Inventario...',
                                  height=40)
    inventario_entry.grid(row=9, column=1, padx=(2,2), pady=(2,10), sticky='new')

    label_costo = ctk.CTkLabel(form_frame, text='Precio de Costo')
    label_costo.grid(row=8, column=2, padx=(2,10), pady=2, sticky="nw")

    costo_entry = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Costo...',
                                  height=40)
    costo_entry.grid(row=9, column=2, padx=(2,10), pady=(2,10), sticky='new')


    """ Bloque de Botones CRUD """

    registrar_button = ctk.CTkButton(form_frame, text="Registrar", height=40,)
    registrar_button.grid(row=14, column=0, padx=(10,2), pady=15, sticky="ew")

    editar_button = ctk.CTkButton(form_frame, text="Editar", height=40,)
    editar_button.grid(row=14, column=1, padx=(2,2), pady=15, sticky="ew")

    eliminar_button = ctk.CTkButton(form_frame, text="Eliminar", height=40, image=delete_icon)
    eliminar_button.grid(row=14, column=2, padx=(2,10), pady=15, sticky="ew")

    # === BLOQUE TABLA DE productos ===

    # Crear un marco con esquinas redondeadas para la tabla
    tabla_frame = ctk.CTkFrame(
        ventana_productos,
        corner_radius=15,          # Bordes redondeados
        fg_color="#2b2b2b",        # Color de fondo del frame
    )
    tabla_frame.grid(row=1, column=1, padx=5, pady=1, sticky="nsew")
    #ventana_productos.grid_rowconfigure(0, weight=1)
    #ventana_productos.grid_columnconfigure(0, weight=1)

    # Crear los scrollbars
    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal")
    # scrollbar_x.pack(side="bottom", fill="x")

    # Crear el Treeview
    treeview = ttk.Treeview(
        tabla_frame,
        columns=("Id", "Producto", "Categoria"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        #xscrollcommand=scrollbar_x.set,
    )

    treeview.pack(fill="both", expand=True, padx=10, pady=10)

    # Configurar los scrollbars
    scrollbar_y.config(command=treeview.yview)
    #scrollbar_x.config(command=treeview.xview)

    # --- Estilos de la tabla ---
    style = ttk.Style()
    style.theme_use("clam")  # Estilo neutro y compatible

    # Fondo oscuro y texto claro
    style.configure(
        "Treeview",
        background="#2e2e2e",
        foreground="#ffffff",
        rowheight=28,
        fieldbackground="#2e2e2e",
        bordercolor="#2b2b2b",
        borderwidth=0,
        font=("Candara", 11)
    )

    # Encabezados con color personalizado
    style.configure(
        "Treeview.Heading",
        background="#3b3b3b",
        foreground="#00bfff",
        font=("Candara", 11, "bold")
    )

    # Selección con color personalizado
    style.map(
        "Treeview",
        background=[("selected", "#0078d7")],
        foreground=[("selected", "#ffffff")]
    )
    
    # Definir encabezados de la tabla
    treeview.heading("Id", text="Id", anchor="w")
    treeview.heading("Producto", text="Producto", anchor="w")
    treeview.heading("Categoria", text="Categoria", anchor="w")
   

    # Ajustar el tamaño de las columnas
    treeview.column("Id", width=10)
    treeview.column("Producto", width=50)
    treeview.column("Categoria", width=50)
   

    # Vincular evento de selección de fila
    treeview.bind("<ButtonRelease-1>", )

        
    footer_label = ctk.CTkLabel(ventana_productos, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright © 2025\nPython Hack By ElGuada90",
                                corner_radius=5)
    footer_label.grid(row=4, column= 0, columnspan=2, padx=5, pady=5, sticky="s" )

    # Cargar usuarios al iniciar la ventana
    cargar_productos()

    """ Ejecutar ventana """
    ventana_productos.mainloop()