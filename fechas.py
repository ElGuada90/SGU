########################
""" Modulo de fechas """
########################

# importamos librerias de python
from datetime import datetime

# definir función datetime
def fecha_24():
    # Formato de fecha y hora de 24 horas.
    fecha_24h = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return fecha_24h

def fecha_12():
    # Formato de fecha y hora de 12 horas am y pm
    fecha_12h = datetime.now().strftime("%Y-%m-%d %I:%M:%p")
    return fecha_12h

def fecha_año():
    # Formato de año
    año = datetime.now().strftime("%Y")
    return año

def fecha_mes():
    # Formato de mes
    mes = datetime.now().strftime("%m")
    return mes



