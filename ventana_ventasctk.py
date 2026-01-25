""" VENTANA DE ventas"""

""" Bloque de Configuración """
# importamos librerias
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import Frame, Menu
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox

# Importamos modulos
from modulo_resource_path import resource_path
from modulo_conexion_mysql import ConexionMySQL



# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
# enlace o ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")

# funcion para crear la ventana ventas
def ventana_ventas(usuario, rol):

    lupa = resource_path("static\\images\\Lupa Blanca.png")
    lupa_icon = ctk.CTkImage(light_image=Image.open(lupa), size=(25, 25))
    
    ventana_ventas = ctk.CTk()
    ventana_ventas.title("Sistema de Gestion Unico")
    ventana_ventas.iconbitmap(icon)
    ventana_ventas.geometry("1280x720+150+8")
    ventana_ventas.resizable(True, True)
    ventana_ventas.grid_columnconfigure(0, weight=1)
    ventana_ventas.grid_rowconfigure(3, weight=1)

    """ Bloque de Funciones """
    # Crear instancia de conexión
    db = ConexionMySQL()


    """ Bloque de Menu """

    # ========== F U N C I O N E S ==========

    # ==========================
    # OBTENER PRODUCTOS
    # ==========================
    def obtener_productos():
        query = "SELECT id, producto FROM productos"
        resultados = db.obtener_datos(query)
        return [(fila["id"], fila["producto"]) for fila in resultados]

    # ==========================
    # OBTENER USUARIOS
    # ==========================
    def obtener_usuarios():
        query = "SELECT id, usuario FROM usuarios"
        resultados = db.obtener_datos(query)
        return [(fila["id"], fila["usuario"]) for fila in resultados]
    
    # Cargar datos
    productos_list = obtener_productos()
    usuarios_list = obtener_usuarios()

    # Diccionarios para mapear texto → id
    map_productos = {p[1]: p[0] for p in productos_list}
    map_usuarios = {u[1]: u[0] for u in usuarios_list}


    """ Función para obtener el usuario y rol """
    def cargar_ventas():
        #limpiar_campos()
        for fila in treeview.get_children():
            treeview.delete(fila)

        query = """
          SELECT * FROM ventas_por_vendedor
        """
        resultados = db.obtener_datos(query)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["valor"], fila["producto"], fila["usuario"], fila["nombre"], fila["fecha"]
            ))

    """ Función para abrir la ventana de usuarios """
    def abrir_usuarios():
        from ventana_usuariosctk import ventana_usuarios
        # cerramos la ventana principal
        ventana_ventas.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_usuarios(usuario, rol)

    """ Función para abrir la ventana de usuarios """
    def abrir_productos():
        from ventana_productosctk import ventana_productos
        # cerramos la ventana ventas
        ventana_ventas.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_productos(usuario, rol)


    """ Función para volver al menú principal """
    def volver_menu_principal():
        # Importación tardía para evitar la importación circular
        from ventana_menuctk import ventana_principal
        ventana_ventas.destroy()  # Cerrar ventana actual
        ventana_principal(usuario, rol)  # Abrir menú principal

     # ========== F R A M E  N A V B A R  ==========
    frame_btn = ctk.CTkFrame(ventana_ventas)
    frame_btn.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
    frame_btn.grid_columnconfigure(0, weight=1)
    frame_btn.grid_rowconfigure(0, weight=1)

     # Funcion para el OptionMMenu
    def ejecutar_menu(opcion):
        if opcion == "Menu Principal":
            volver_menu_principal()
        if opcion == "Usuarios":
            abrir_usuarios()
        elif opcion == "Productos":
            abrir_productos()
        elif opcion == "Exit":
            ventana_ventas.destroy()    


    # ----- PRIMER OPTIONMENU (MENU) -----
    opciones_file = ["Menu Principal", "Usuarios", "Productos", "Exit"]

    menu_opciones = ctk.CTkOptionMenu(frame_btn,
                                values=opciones_file,
                                command=ejecutar_menu,
                                width=200)
    menu_opciones.set("Ventas")  # Texto inicial
    menu_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    
    # ===== PRODUCTO (OPTIONMENU) =====
    optionmenu_producto = ctk.CTkOptionMenu(frame_btn, values=[p[1] for p in productos_list])
    optionmenu_producto.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    optionmenu_producto.set("Seleccione producto")

    # ===== USUARIO (COMBOBOX) =====
    combobox_usuario = ctk.CTkComboBox(frame_btn, values=[u[1] for u in usuarios_list], state="readonly")
    combobox_usuario.grid(row=0, column=1, padx=5, pady=5, sticky="e")
    combobox_usuario.set("Vendedor")

    # --------------------------------------------------
    # ENTRY PARA VALOR
    # --------------------------------------------------
    entry_valor = ctk.CTkEntry(frame_btn, placeholder_text="Valor $")
    entry_valor.grid(row=0, column=2, pady=5, padx=5, sticky="e")

     # ==========================
    # REGISTRAR VENTA
    # ==========================
    def registrar_venta():
        producto = optionmenu_producto.get().lower()
        usuario = combobox_usuario.get().lower()
        valor = entry_valor.get()

        if producto == "Seleccione producto" or usuario == "Vendedor" or valor.strip() == "":
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        try:
            id_producto = map_productos[producto]
            id_usuario = map_usuarios[usuario]

            conn = db.conectar()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO ventas (valor, id_producto, id_usuario, moddate)
                VALUES (%s, %s, %s, %s)
            """, (valor, id_producto, id_usuario, datetime.now()))

            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Venta registrada correctamente.")
            entry_valor.delete(0, "end")
            cargar_ventas()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    btn_registrar = ctk.CTkButton(frame_btn, text="Registrar Venta", command=registrar_venta)
    btn_registrar.grid(row=0, column=3, padx=5, pady=5, sticky="e")

    # ==========================
    #   TABLA DE VENTAS
    # ==========================
    tabla_frame = ctk.CTkFrame(ventana_ventas, corner_radius=15, fg_color="#2b2b2b")
    tabla_frame.grid(row=3, column=0, padx=15, pady=15, sticky="nsew")

    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    treeview = ttk.Treeview(
        tabla_frame,
        columns=("valor", "producto", "usuario", "nombre", "fecha"),
        show="headings",
        yscrollcommand=scrollbar_y.set,
    )
    treeview.pack(fill="both", expand=True, padx=10, pady=10)
    scrollbar_y.config(command=treeview.yview)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#2e2e2e", foreground="#ffffff", rowheight=28,
                    fieldbackground="#2e2e2e", font=("Candara", 11))
    style.configure("Treeview.Heading", background="#3b3b3b", foreground="#00bfff",
                    font=("Candara", 11, "bold"))
    style.map("Treeview", background=[("selected", "#0078d7")])

    treeview.heading("valor", text="Valor")
    treeview.heading("producto", text="Producto")
    treeview.heading("usuario", text="Usuario")
    treeview.heading("nombre", text="Nombre")
    treeview.heading("fecha", text="Fecha")

    treeview.column("valor", width=10)
    treeview.column("producto", width=50)
    treeview.column("usuario", width=50)
    treeview.column("nombre", width=50)
    treeview.column("fecha", width=50)


    # === BLOQUE TABLA DE ventas ===

    # Crear un marco con esquinas redondeadas para la tabla
    tabla_frame = ctk.CTkFrame(
        ventana_ventas,
        corner_radius=15,          # Bordes redondeados
        fg_color="#2b2b2b",        # Color de fondo del frame
    )
    tabla_frame.grid(row=3, column=0, padx=15, pady=15, sticky="nsew")
    #ventana_ventas.grid_rowconfigure(0, weight=1)
    #ventana_ventas.grid_columnconfigure(0, weight=1)

    # Crear los scrollbars
    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal")
    # scrollbar_x.pack(side="bottom", fill="x")

    # Crear el Treeview
    treeview = ttk.Treeview(
        tabla_frame,
        columns=("valor", "producto", "usuario", "nombre", "fecha"),
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
    treeview.heading("valor", text="Valor", anchor="w")
    treeview.heading("producto", text="Producto", anchor="w")
    treeview.heading("usuario", text="Usuario", anchor="w")
    treeview.heading("nombre", text="Nombre", anchor="w")
    treeview.heading("fecha", text="Fecha", anchor="w")
   

    # Ajustar el tamaño de las columnas
    treeview.column("valor", width=10)
    treeview.column("producto", width=50)
    treeview.column("usuario", width=50)
    treeview.column("nombre", width=50)
    treeview.column("fecha", width=50)
   

    # Vincular evento de selección de fila
    treeview.bind("<ButtonRelease-1>", )

        
    footer_label = ctk.CTkLabel(ventana_ventas, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright © 2025\nPython Hack ElGuada90",
                                corner_radius=5)
    footer_label.grid(row=4, column= 0, padx=5, pady=5, sticky="s" )

    # Cargar usuarios al iniciar la ventana
    cargar_ventas()

    """ Ejecutar ventana """
    ventana_ventas.mainloop()