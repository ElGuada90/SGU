# Importar librerías
import os, sys

# Función para obtener la ruta correcta del archivo en el ejecutable o en desarrollo
def resource_path(relative_path):
    try:
        # PyInstaller guarda archivos temporales en una carpeta diferente (sys._MEIPASS)
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")  # En desarrollo, usar la carpeta actual
    return os.path.join(base_path, relative_path)
