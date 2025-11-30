""" Modulo Limpiar pantalla """
# importar librerias
from datetime import datetime
import os

# Función limpiar_pantalla
def limpiar_pantalla():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')