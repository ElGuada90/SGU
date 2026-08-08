
# ======================= #
""" VENTANA DE PRODUCTOS"""
# ======================= #

# =========================== #
""" Bloque de Configuración """
# =========================== #

# ================== #
# importamos librerias
# ================== #
import customtkinter as ctk
from PIL import Image, ImageTk
import os, shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ================== #
# Importamos modulos
# ================== #
from modulo_resource_path import resource_path
from modulo_conexion_mysql import ConexionMySQL

from ventana_usuariosctk import ventana_usuarios
from ventana_ventasctk import ventana_ventas

# ================= #
# temas y apariencia
# ================= #
ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"
# enlace o ruta de imagenes
icon = resource_path("static\\images\\Logo Python ico.ico")

# ====================================== #
# funcion para crear la ventana productos
# ====================================== #
def ventana_productos(usuario, rol):

    lupa = resource_path("static\\images\\Lupa Blanca.png")
    lupa_icon = ctk.CTkImage(light_image=Image.open(lupa), size=(25, 25))
    delete = resource_path("static\\images\\delete.png")
    delete_icon = ctk.CTkImage(light_image=Image.open(delete), size=(25, 25))
    edit = resource_path("static\\images\\edit.png")
    edit_icon = ctk.CTkImage(light_image=Image.open(edit), size=(25, 25))
    add = resource_path("static\\images\\add.png")
    add_icon = ctk.CTkImage(light_image=Image.open(add), size=(25, 25))
    
    ventana_productos = ctk.CTk()
    ventana_productos.title("Sistema de Gestion Unico")
    ventana_productos.iconbitmap(icon)
    ventana_productos.geometry("1280x720+0+0")
    ventana_productos.resizable(True, True)
    ventana_productos.grid_columnconfigure(1, weight=1)
    ventana_productos.grid_rowconfigure(1, weight=1)

    # ========================== #
    # Crear instancia de conexión
    # ========================== #
    db = ConexionMySQL()

    # =============================== #
    """ === Bloque de Funciones === """
    # =============================== #
    
    # ===================================================== #
    """ Función para obtener todos los datos de productos """
    # ===================================================== #
    def cargar_productos():
        #limpiar_campos()
        for fila in treeview.get_children():
            treeview.delete(fila)

        query = "SELECT * FROM productos"
        resultados = db.obtener_datos(query)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["codigo"], fila["producto"], fila["descripcion"], fila["marca"], fila["inventario"], fila["pcosto"], fila["categoria"], fila["subcategoria"]
            ))

    # ================================================================== #
    """Modificar los datos del usuario seleccionado en la base de datos"""
    # ================================================================== #
    def modificar_registro():
        selected_item = treeview.focus()  # Obtener el elemento seleccionado
        if not selected_item:
            messagebox.showerror("Error", "No se ha seleccionado ningún usuario")
            return

        # Obtener el ID del usuario seleccionado
        valores = treeview.item(selected_item, "values")
        usuario_actual = valores[0]

        # Obtener los nuevos valores de las entradas
        nuevo_codigo = entry_codigo.get()
        nuevo_producto = entry_producto.get()
        nueva_descripcion = entry_descripcion.get()
        nueva_marca = entry_marca.get()
        nuevo_cantidad = entry_cantidad.get()
        nuevo_pcosto = entry_pcosto.get()
        nueva_categoria = categoria_combobox.get()
        nueva_subcategoria = subcategoria_combobox.get()
        

        if nuevo_codigo and nuevo_producto:
            query = """
            UPDATE productos
            SET codigo=%s, producto=%s, descripcion=%s, marca=%s, inventario=%s, pcosto=%s, categoria=%s, subcategoria=%s, enlace=%s
            WHERE usuario=%s
            """
            params = (nuevo_codigo, nuevo_producto, nueva_descripcion, nueva_marca,
                      nuevo_cantidad, nuevo_pcosto, nueva_categoria, nueva_subcategoria, usuario_actual)

            if db.ejecutar_consulta(query, params):
                messagebox.showinfo("Modificación", "Usuario modificado con éxito.")
                cargar_productos()
                limpiar_campos()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos")

    # ==================================================================== #
    """Cargar los datos de la fila seleccionada en los campos de entrada"""
    # ==================================================================== #
    def seleccionar_producto(event):
        selected_item = treeview.focus()
        if not selected_item:
            return  # No hay fila seleccionada
    
        valores = treeview.item(selected_item, "values")
    
        # Asumimos que los valores están en el mismo orden que los entries
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, valores[0])
        entry_producto.delete(0, tk.END)
        entry_producto.insert(0, valores[1])
        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, valores[2])
        entry_marca.delete(0, tk.END)
        entry_marca.insert(0, valores[3])
        categoria_combobox.set(valores[6])
        subcategoria_combobox.set(valores[7])
        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, valores[4])
        entry_pcosto.delete(0, tk.END)
        entry_pcosto.insert(0, valores[5])

       

    # ======================================== #
    """ Función para volver al menú producto """
    # ======================================== #
    def volver_menu_ventanas():
        # Importación tardía para evitar la importación circular
        from ventana_menuctk import ventana_principal
        ventana_productos.destroy()  # Cerrar ventana actual
        ventana_principal(usuario, rol)  # Abrir menú

    # ============================================= #
    """ Función para abrir la ventana de usuarios """
    # ============================================= #
    def abrir_usuarios():
        # cerramos la ventana producto
        ventana_productos.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_usuarios(usuario, rol)

    # ============================================= #
    """ Función para abrir la ventana de ventas """
    # ============================================= #
    def abrir_ventas():
        # cerramos la ventana producto
        ventana_productos.destroy()
        # abrir la ventana de usuarios (la función debe crear su propia ventana)
        ventana_ventas(usuario, rol)

    # ================================== #
    """ Función para busqueda Dinámica """
    # ================================== #
    def consulta_dinamica(event):
        consulta = entry_consulta.get().strip()

        # Limpiar el Treeview
        for item in treeview.get_children():
            treeview.delete(item)

        # Si el entry está vacío, mostrar todos los registros
        if not consulta:
            cargar_productos()
            return

        # Consulta SQL dinámica (usa LIKE con %)
        query = """
        SELECT producto, categoria, subcategoria
        FROM productos
        WHERE producto LIKE %s OR categoria LIKE %s OR subcategoria LIKE %s
        """
        params = (f"%{consulta}%", f"%{consulta}%", f"%{consulta}%")

        resultados = db.obtener_datos(query, params)

        for fila in resultados:
            treeview.insert("", "end", values=(
                fila["producto"], fila["categoria"], fila["subcategoria"],
                #fila["nombre"], fila["apellido"], fila["email"], fila["telefono"]
            ))

    # ================================================ #
    """ Función para habilitar acceso a los usuarios """   
    # ================================================ #
    def role_acceso():
        """Verificar si el usuario tiene rol de 'Full Stack' o 'Admin'"""
        return rol in ['Full Stack', 'admin']
    
    # ==================================================== #
    """Función para cargar una imagen y almacenar la ruta"""
    # ==================================================== #
    def cargar_imagen(self):
        self.enlace = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.gif")])
        if self.enlace:
            # Obtiene el nombre del archivo de la imagen seleccionada
            nombre_imagen = os.path.basename(self.enlace)
            # Define la ruta de destino dentro de la carpeta 'static/image'
            destino = os.path.join("static", "image", nombre_imagen)
            try:
                # Crea la carpeta 'static/image' si no existe
                if not os.path.exists(os.path.dirname(destino)):
                    os.makedirs(os.path.dirname(destino))

                # Copia la imagen seleccionada a la carpeta destino
                shutil.copy(self.enlace, destino)

                # Guarda la ruta relativa de la imagen en la base de datos
                self.enlace = os.path.join("static", "image", nombre_imagen)
                #self.guardar_imagen_en_db(self.enlace)
                
                # Muestra un mensaje de éxito
                messagebox.showinfo("Imagen cargada", f"Imagen guardada en: {self.enlace}")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen: {str(e)}")  


    # === Funciones para limpiar Campos == #         
    def limpiar_campos(self):
        """Limpiar los campos de entrada"""
        entry_codigo.delete(0, tk.END)
        entry_producto.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)
        entry_marca.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_pcosto.delete(0, tk.END)
        categoria_combobox.set("")
        subcategoria_combobox.set("")
       

    # ============================================== #
    """ Función para manejar las opciones del menú """
    # ============================================== #
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

    # =========================== #
    """ Bloque de Barra de Menu """
    # =========================== #

    # --- Bloque de Frame para barra de navegación ---
    
    nav_frame = ctk.CTkFrame(ventana_productos, corner_radius=8) 
    nav_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="ew")
    nav_frame.grid_columnconfigure(0, weight=1)
    nav_frame.grid_rowconfigure(0, weight=1)

   
    # ----- PRIMER OPTIONMENU (FILE) -----
    opciones_file = ["Menu Principal", "Usuarios", "Ventas", "Exit"]

    menu = ctk.CTkOptionMenu(nav_frame, values=opciones_file, command=ejecutar_menu, width=200)
    menu.set("Productos")
    menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")

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

    form_frame = ctk.CTkFrame(ventana_productos, corner_radius=8) 
    form_frame.grid(row=1, column=0, padx=(15,2), pady=1, sticky="nsew")

    image_frame = ctk.CTkFrame(form_frame, corner_radius=8)
    image_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    image_btn = ctk.CTkButton(form_frame, text="Cargar Imagen...")
    image_btn.grid(row=3, column=0, columnspan=3, padx=10, pady=2, sticky="ew")

    label_producto = ctk.CTkLabel(form_frame, text='Producto')
    label_producto.grid(row=4, column=0, padx=10, pady=(10,2), sticky="w")

    entry_producto = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Producto...',
                                  height=40)
    entry_producto.grid(row=5, column=0, padx=(10,2), pady=2, sticky='ew')

    label_descripcion = ctk.CTkLabel(form_frame, text='Descripcion')
    label_descripcion.grid(row=4, column=1, columnspan=2, padx=10, pady=(10,2), sticky="w")

    entry_descripcion = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Descripcion...',
                                  height=40)
    entry_descripcion.grid(row=5, column=1, columnspan=2, padx=(2,10), pady=2, sticky='ew')

    label_marca = ctk.CTkLabel(form_frame, text='Marca')
    label_marca.grid(row=6, column=0, padx=10, pady=(10,2), sticky="w")

    entry_marca = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Marca...',
                                  height=40)
    entry_marca.grid(row=7, column=0, padx=(10,2), pady=2, sticky='ew')

    label_categoria = ctk.CTkLabel(form_frame, text='Categoria')
    label_categoria.grid(row=6, column=1, padx=(10,2), pady=(10,2), sticky="w")

    categoria_combobox = ctk.CTkComboBox(form_frame, height=40, state="readonly")
    categoria_combobox.grid(row=7, column=1, padx=(2,2), pady=2, sticky='ew')
    categoria_combobox.set("Seleccione..")

    label_subcategoria = ctk.CTkLabel(form_frame, text='Sub-Categoria')
    label_subcategoria.grid(row=6, column=2, padx=(2,10), pady=(10,2), sticky="w")

    subcategoria_combobox = ctk.CTkComboBox(form_frame, height=40, state="readonly")
    subcategoria_combobox.grid(row=7, column=2, padx=(2,10), pady=2, sticky='ew')
    subcategoria_combobox.set("Seleccione..")

    label_codigo = ctk.CTkLabel(form_frame, text='Codigo')
    label_codigo.grid(row=8, column=0, padx=10, pady=(10,2), sticky="w")

    entry_codigo = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Codigo...',
                                  height=40)
    entry_codigo.grid(row=9, column=0, padx=(10,2), pady=(2,10), sticky='ew')

    label_cantidad = ctk.CTkLabel(form_frame, text='Cantidad')
    label_cantidad.grid(row=8, column=1, padx=(2,2), pady=(10,2), sticky="w")

    entry_cantidad = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Inventario...',
                                  height=40)
    entry_cantidad.grid(row=9, column=1, padx=(2,2), pady=(2,10), sticky='ew')

    label_costo = ctk.CTkLabel(form_frame, text='Precio de Costo')
    label_costo.grid(row=8, column=2, padx=(2,10), pady=(10,2), sticky="w")

    entry_pcosto = ctk.CTkEntry(form_frame, 
                                  placeholder_text='Ingrese Costo...',
                                  height=40)
    entry_pcosto.grid(row=9, column=2, padx=(2,10), pady=(2,10), sticky='ew')


    """ Bloque de Botones CRUD """

    registrar_button = ctk.CTkButton(form_frame, text="", height=40, image=add_icon)
    registrar_button.grid(row=14, column=0, padx=(10,2), pady=15, sticky="ew")

    editar_button = ctk.CTkButton(form_frame, text="", height=40, image=edit_icon)
    editar_button.grid(row=14, column=1, padx=(2,2), pady=15, sticky="ew")

    eliminar_button = ctk.CTkButton(form_frame, text="", height=40, image=delete_icon)
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
        columns=("Codigo", "Producto", "Descripcion", "Marca", "Inventario", "PrecioCosto", "Categoria", "Subcategoria"),
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
        font=("Candara", 12)
    )

    # Encabezados con color personalizado
    style.configure(
        "Treeview.Heading",
        background="#3b3b3b",
        foreground="#00bfff",
        font=("Candara", 12, "bold")
    )

    # Selección con color personalizado
    style.map(
        "Treeview",
        background=[("selected", "#0078d7")],
        foreground=[("selected", "#ffffff")]
    )
    
    # Definir encabezados de la tabla
    treeview.heading("Codigo", text="Código", anchor="w")
    treeview.heading("Producto", text="Producto", anchor="w")
    treeview.heading("Descripcion", text="Descripción", anchor="w")
    treeview.heading("Marca", text="Marca", anchor="w")
    treeview.heading("Inventario", text="Inventario", anchor="w")
    treeview.heading("PrecioCosto", text="Precio de Costo", anchor="w")
    treeview.heading("Categoria", text="Categoría", anchor="w")
    treeview.heading("Subcategoria", text="Subcategoría", anchor="w")
   

    # Ajustar el tamaño de las columnas
    treeview.column("Codigo", width=50)
    treeview.column("Producto", width=50)
    treeview.column("Descripcion", width=50)
    treeview.column("Marca", width=50)
    treeview.column("Inventario", width=50)
    treeview.column("PrecioCosto", width=50)
    treeview.column("Categoria", width=50)
    treeview.column("Subcategoria", width=50)
   
   
    # Vincular evento de selección de fila
    treeview.bind("<ButtonRelease-1>", seleccionar_producto)

        
    footer_label = ctk.CTkLabel(ventana_productos, 
                                font=ctk.CTkFont(size=10, weight="bold"),
                                fg_color="transparent",
                                text="Copyright © 2025 * Python Hack By ElGuada90",
                                corner_radius=5)
    footer_label.grid(row=4, column= 0, columnspan=2, padx=5, pady=5, sticky="s" )

    # Cargar usuarios al iniciar la ventana
    cargar_productos()

    """ Ejecutar ventana """
    ventana_productos.mainloop()