# modulo_conexion_mysql.py
import os
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class ConexionMySQL:
    """Clase para manejar la conexión a una base de datos MySQL de forma reutilizable."""
    
    # Variable de clase para mantener una única instancia (patrón Singleton)
    _instancia = None
    
    def __new__(cls, *args, **kwargs):
        """Implementación del patrón Singleton para asegurar una única conexión."""
        if not cls._instancia:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        """Inicializa la conexión usando variables de entorno."""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'administracion')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.connection = None

    def conectar(self):
        """Establece conexión con la base de datos MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos:\n{e}")
            return None

    def ejecutar_consulta(self, query, params=None):
        """Ejecuta una consulta INSERT, UPDATE o DELETE."""
        if not self.connection or not self.connection.is_connected():
            self.conectar()
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            messagebox.showerror("Error SQL", f"Error al ejecutar la consulta:\n{e}")
            return False

    def obtener_datos(self, query, params=None):
        """Ejecuta una consulta SELECT y devuelve los resultados."""
        if not self.connection or not self.connection.is_connected():
            self.conectar()
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except Error as e:
            messagebox.showerror("Error SQL", f"Error al obtener datos:\n{e}")
            return []    

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
