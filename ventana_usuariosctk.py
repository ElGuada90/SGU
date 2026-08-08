""" Ventana para la gestión de usuarios """

""" Bloque de Configuración """
# importamos librerias
import customtkinter as ctk
from PIL import Image
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importamos modulos
from modulo_resource_path import resource_path
from modulo_conexion_mysql import ConexionMySQL

# temas y apariencia
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
# enlace o ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")


# funcion para crear la ventana principal
def ventana_usuarios(usuario, rol):

    lupa = resource_path("static\\images\\Lupa Blanca.png")
    lupa_icon = ctk.CTkImage(light_image=Image.open(lupa), size=(25, 25))
    add = resource_path("static\\images\\add.png")
    add_icon = ctk.CTkImage(light_image=Image.open(add), size=(25, 25))
    edit = resource_path("static\\images\\edit.png")
    edit_icon = ctk.CTkImage(light_image=Image.open(edit), size=(25, 25))
    delete = resource_path("static\\images\\delete.png")
    delete_icon = ctk.CTkImage(light_image=Image.open(delete), size=(25, 25))
    
    ventana_usuarios = ctk.CTk()
    ventana_usuarios.title("Sistema de Gestion Unico")
    ventana_usuarios.iconbitmap(icon)
    ventana_usuarios.geometry("1280x720+0+0")
    ventana_usuarios.resizable(True, True)
    ventana_usuarios.grid_columnconfigure(1, weight=1)
    ventana_usuarios.grid_rowconfigure(2, weight=1)

    """ Bloque de Funciones """
    # Crear instancia de conexión
    db = ConexionMySQL()

    # --- FUNCIONES CRUD ---
    def registrar_usuario():
        usuario = entry_usuario.get()
        contraseña = entry_contraseña.get()
        role = entry_role.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        email = entry_email.get()
        telefono = entry_telefono.get()

        if not usuario or not contraseña:
            messagebox.showwarning("Campos vacíos", "El campo Usuario y Contraseña son obligatorios.")
            return

        query = """
        INSERT INTO usuarios (usuario, contraseña, role, nombre, apellido, email, telefono, moddate, moduser)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """
        params = (usuario, contraseña, role, nombre, apellido, email, telefono, usuario)

        if db.ejecutar_consulta(query, params):
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            cargar_usuarios()

    def cargar_usuarios():
        limpiar_campos()
        for fila in treeview.get_children():
            treeview.delete(fila)

        query = "SELECT usuario, contraseña, role, nombre, apellido, email, telefono FROM usuarios"
        resultados = db.obtener_datos(query)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["usuario"], fila["contraseña"], fila["role"],
                fila["nombre"], fila["apellido"], fila["email"], fila["telefono"]
            ))

    def consulta_dinamica(event):
        consulta = entry_consulta.get().strip()

        # Limpiar el Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Si el entry está vacío, mostrar todos los registros
        if not consulta:
            cargar_usuarios()
            return

        # Consulta SQL dinámica (usa LIKE con %)
        query = """
        SELECT usuario, contraseña, role, nombre, apellido, email, telefono
        FROM usuarios
        WHERE usuario LIKE %s OR role LIKE %s OR nombre LIKE %s OR apellido LIKE %s
        """
        params = (f"%{consulta}%", f"%{consulta}%", f"%{consulta}%", f"%{consulta}%")

        resultados = db.obtener_datos(query, params)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["usuario"], fila["contraseña"], fila["role"],
                fila["nombre"], fila["apellido"], fila["email"], fila["telefono"]
            ))

    # Lista de Funciones    
    def role_acceso():
        """Verificar si el usuario tiene rol de 'Full Stack' o 'Admin'"""
        return role in ['Full Stack', 'admin']
     
    def limpiar_campos():
        """Limpia los campos de entrada."""
        for entry in [entry_usuario, entry_contraseña, entry_role, entry_nombre,
                      entry_apellido, entry_email, entry_telefono]:
            entry.delete(0, tk.END)

    def seleccionar_usuario(event):
        """Carga los datos del usuario seleccionado en los campos."""
        limpiar_campos()
        selected_item = treeview.focus()
        valores = treeview.item(selected_item, "values")

        if valores:
            entry_usuario.insert(0, valores[0])
            entry_contraseña.insert(0, valores[1])
            entry_role.insert(0, valores[2])
            entry_nombre.insert(0, valores[3])
            entry_apellido.insert(0, valores[4])
            entry_email.insert(0, valores[5])
            entry_telefono.insert(0, valores[6])

    def modificar_usuario():
        """Modificar los datos del usuario seleccionado en la base de datos"""
        selected_item = treeview.focus()  # Obtener el elemento seleccionado
        if not selected_item:
            messagebox.showerror("Error", "No se ha seleccionado ningún usuario")
            return

        # Obtener el ID del usuario seleccionado
        valores = treeview.item(selected_item, "values")
        usuario_actual = valores[0]

        # Obtener los nuevos valores de las entradas
        nuevo_usuario = entry_usuario.get()
        nueva_contraseña = entry_contraseña.get()
        nuevo_role = entry_role.get()
        nuevo_nombre = entry_nombre.get()
        nuevo_apellido = entry_apellido.get()
        nuevo_email = entry_email.get()
        nuevo_telefono = entry_telefono.get()

        if nuevo_usuario and nueva_contraseña:
            query = """
            UPDATE usuarios
            SET usuario=%s, contraseña=%s, role=%s, nombre=%s, apellido=%s, email=%s, telefono=%s
            WHERE usuario=%s
            """
            params = (nuevo_usuario, nueva_contraseña, nuevo_role, nuevo_nombre,
                      nuevo_apellido, nuevo_email, nuevo_telefono, usuario_actual)

            if db.ejecutar_consulta(query, params):
                messagebox.showinfo("Modificación", "Usuario modificado con éxito.")
                cargar_usuarios()
                limpiar_campos()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")


    
    """ Función para volver al menú principal """
    def volver_menu_principal():
        # Importación tardía para evitar la importación circular
        from ventana_menuctk import ventana_principal
        ventana_usuarios.destroy()  # Cerrar ventana actual
        ventana_principal(usuario, rol)  # Abrir menú principal

    def volver_productos():
        # Importación tardía para evitar la importación circular
        from ventana_productosctk import ventana_productos
        ventana_usuarios.destroy()  # Cerrar ventana actual
        ventana_productos(usuario, rol)  # Abrir menú principal

    def volver_ventas():
        # Importación tardía para evitar la importación circular
        from ventana_ventasctk import ventana_ventas
        ventana_usuarios.destroy()  # Cerrar ventana actual
        ventana_ventas(usuario, rol)  # Abrir menú principal
    
    # ============================================== #
    """ Función para manejar las opciones del menú """
    # ============================================== #
   
    # Funcion para el OptionMMenu
    def ejecutar_menu(opcion):
        if opcion == "Menu Principal":
            volver_menu_principal()
        elif opcion == "Productos":
            volver_productos()
        elif opcion == "Ventas":
            volver_ventas()
        elif opcion == "Exit":
            ventana_usuarios.destroy()  

    # =========================== #
    """ Bloque de Barra de Menu """
    # =========================== #  

    # --- Bloque de Frame para barra de navegación ---
    nav_frame = ctk.CTkFrame(ventana_usuarios, corner_radius=8) 
    nav_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_rowconfigure(0, weight=1)

    # ----- PRIMER OPTIONMENU (FILE) -----
    opciones_file = ["Menu Principal", "Productos", "Ventas", "Exit"]

    menu_opciones = ctk.CTkOptionMenu(nav_frame,
                                values=opciones_file,
                                command=ejecutar_menu,
                                width=200)
    menu_opciones.set("Usuarios")  # Texto inicial
    menu_opciones.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    # Label para contener icono de busqueda (Lupa)
    label_lupa_icon = ctk.CTkLabel(nav_frame,
                    text="",
                    image=lupa_icon,
                    font=ctk.CTkFont(size=18, weight="bold"),
                    height=31)
    label_lupa_icon.grid(row=0, column=0, padx=220, pady=(8), sticky="e")

    # Widget para busqueda dinamica de datos
    entry_consulta = ctk.CTkEntry(nav_frame,
                                    placeholder_text="Buscar...",
                                    width=210,
                                    height=30)
    entry_consulta.grid(row=0, column=0, padx=5, pady=(8), sticky="ne")
    entry_consulta.bind("<KeyRelease>", consulta_dinamica)

    """ Variables de sesión """
    usuario = usuario
    role = rol

    """ Bloque de Widgets """
    # Label de titulo
    label_titulo = ctk.CTkLabel(ventana_usuarios, 
                        text="Formulario de Registro de Usuarios",
                        font=ctk.CTkFont(family="candara", size=18, weight="normal"),
                        fg_color="transparent",
                        #bg_color="darkblue",
                        corner_radius=5,
                        #height=40 
                        )
    label_titulo.grid(row=1, column=0, padx=15, pady=5, sticky="nw")
        
    
    # Contenedor Form Frame
    form_frame = ctk.CTkFrame(ventana_usuarios, corner_radius=5)
    form_frame.grid(row=2, column=0, padx=(15,2), pady=2, sticky="nsew")
    form_frame.grid_columnconfigure((0,1,2), weight=1)

    label_usuario = ctk.CTkLabel(form_frame, text="Usuario", font=ctk.CTkFont(size=12, weight="bold"))
    label_usuario.grid(row=0, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_usuario = ctk.CTkEntry(form_frame, placeholder_text='Ingrese Usuario...', height=35)
    entry_usuario.grid(row=1, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_contraseña = ctk.CTkLabel(form_frame, text="Contraseña", font=ctk.CTkFont(size=12, weight="bold"))
    label_contraseña.grid(row=2, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_contraseña = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Contraseña...", height=35)
    entry_contraseña.grid(row=3, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_role = ctk.CTkLabel(form_frame, text="Role", font=ctk.CTkFont(size=12, weight="bold"))
    label_role.grid(row=4, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_role = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Role...", height=35)
    entry_role.grid(row=5, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_nombre = ctk.CTkLabel(form_frame, text="Nombre", font=ctk.CTkFont(size=12, weight="bold"))
    label_nombre.grid(row=6, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Nombre...", height=35)
    entry_nombre.grid(row=7, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_apellido = ctk.CTkLabel(form_frame, text="Apellido", font=ctk.CTkFont(size=12, weight="bold"))
    label_apellido.grid(row=8, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_apellido = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Apellido...", height=35)
    entry_apellido.grid(row=9, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_email = ctk.CTkLabel(form_frame, text="Email", font=ctk.CTkFont(size=12, weight="bold"))
    label_email.grid(row=10, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_email = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Email...", height=35)
    entry_email.grid(row=11, column=0, columnspan=3, padx=10, pady=1, sticky="ew")

    label_telefono = ctk.CTkLabel(form_frame, text="Teléfono", font=ctk.CTkFont(size=12, weight="bold"))
    label_telefono.grid(row=12, column=0, columnspan=3, padx=10, pady=(2,2), sticky="w")
    entry_telefono = ctk.CTkEntry(form_frame, placeholder_text="Ingrese Teléfono...", height=35)
    entry_telefono.grid(row=13, column=0, columnspan=3, padx=10, pady=1, sticky="ew")
    
    # Boton para registros nuevos
    boton_registrar = ctk.CTkButton(form_frame,
                                    text="",
                                    image=add_icon,
                                    corner_radius=5,
                                    width=100,
                                    command=registrar_usuario,
                                    height=35
                                    )
    boton_registrar.grid(row=14, column=0, padx=(10, 5), pady=15, sticky="we")

    # Boton para editar usuarios
    boton_editar = ctk.CTkButton(form_frame,
                                text="",   
                                image=edit_icon,        
                                corner_radius=5,
                                width=100,
                                command=modificar_usuario,
                                height=35
                                )
    boton_editar.grid(row=14, column=1, padx=(5, 5), pady=15, sticky="we")

    # Boton delete para eliminar usuarios
    boton_delete = ctk.CTkButton(form_frame,
                                    text="",  
                                    image=delete_icon,         
                                    corner_radius=5,
                                    width=100,
                                    command=cargar_usuarios,
                                    height=35
                                    )
    boton_delete.grid(row=14, column=2, padx=(5, 10), pady=15, sticky="ew")

    # === BLOQUE TABLA DE USUARIOS ===

    # Crear un marco con esquinas redondeadas para la tabla
    tabla_frame = ctk.CTkFrame(
        ventana_usuarios,
        corner_radius=15,          # Bordes redondeados
        fg_color="#2b2b2b",        # Color de fondo del frame
    )
    tabla_frame.grid(row=2, column=1, padx=(5,15), pady=2, sticky="nsew")
    #ventana_usuarios.grid_rowconfigure(0, weight=1)
    #ventana_usuarios.grid_columnconfigure(0, weight=1)

    # Crear los scrollbars
    scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    # scrollbar_x = ttk.Scrollbar(tabla_frame, orient="horizontal")
    # scrollbar_x.pack(side="bottom", fill="x")

    # Crear el Treeview
    treeview = ttk.Treeview(
        tabla_frame,
        columns=("Usuario", "Contraseña", "Role", "Nombre", "Apellido", "Email", "Teléfono"),
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
        font=("Candara", 14)
    )

    # Encabezados con color personalizado
    style.configure(
        "Treeview.Heading",
        background="#3b3b3b",
        foreground="#00bfff",
        font=("Candara", 14, "bold")
    )

    # Selección con color personalizado
    style.map(
        "Treeview",
        background=[("selected", "#0078d7")],
        foreground=[("selected", "#ffffff")]
    )
    
    # Definir encabezados de la tabla
    treeview.heading("Usuario", text="Usuario", anchor="w")
    treeview.heading("Contraseña", text="Contraseña", anchor="w")
    treeview.heading("Role", text="Role", anchor="w")
    treeview.heading("Nombre", text="Nombre", anchor="w")
    treeview.heading("Apellido", text="Apellido", anchor="w")
    treeview.heading("Email", text="Email", anchor="w")
    treeview.heading("Teléfono", text="Teléfono", anchor="w")

    # Ajustar el tamaño de las columnas
    treeview.column("Usuario", width=50)
    treeview.column("Contraseña", width=50)
    treeview.column("Role", width=50)
    treeview.column("Nombre", width=50)
    treeview.column("Apellido", width=50)
    treeview.column("Email", width=200)
    treeview.column("Teléfono", width=100)

    # Vincular evento de selección de fila
    treeview.bind("<ButtonRelease-1>", seleccionar_usuario)

        
    footer_label = ctk.CTkLabel(ventana_usuarios, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright © 2025 * Python Hack ElGuada90",
                                corner_radius=5)
    footer_label.grid(row=3, column= 0, columnspan=2, padx=5, pady=5, sticky="s" )

    # Cargar usuarios al iniciar la ventana
    cargar_usuarios()

    """ Ejecutar ventana """
    ventana_usuarios.mainloop()