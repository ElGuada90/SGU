########################
""" Modulo de fechas """
########################

# importamos librerias de python
from datetime import date, datetime, timedelta

# Seccion de Formatos

# ejemplos utilizando datetime.strftime() para formatear la fecha y hora

fecha = datetime.now()
# formato de fecha generica
#%Y-%m-%d %H:%M:%S.%f
#print(fecha)

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

# Formato de string para fecha

mes = datetime.now().strftime("%B")
# print(f'El mes actual es: {mes}')


# Libreria timedelta
# timedelta se utiliza para realizar operaciones aritméticas con fechas y horas, como sumar o restar 
# Ejemplo de sumar dias.
un_dia = timedelta(days=1)
ahora = datetime.now()
mañana_fecha = ahora + un_dia
mañana = mañana_fecha.strftime("%Y-%b-%d %H:%M:%p")
# print(f'La fecha de mañana es: {mañana}')

# Restar horas
una_hora = timedelta(hours=1)
hace_una_hora = ahora - una_hora
# print(f"Hace una hora: {hace_una_hora}")

# Sumar múltiples unidades
futuro = ahora + timedelta(days=7, hours=3, minutes=30)
# print(f"En una semana y un poco más: {futuro}")

# Calcular la diferencia entre dos fechas
fecha_pasada = datetime(2025, 6, 15, 10, 0, 0)
diferencia = ahora - fecha_pasada
# print(f"Diferencia: {diferencia}")
# print(f"Días de diferencia: {diferencia.days}")
# print(f"Segundos totales de diferencia: {diferencia.total_seconds()}")

# Calcular la edad de alguien:
fecha_nacimiento_str = "1990-05-15"
fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d')
hoy = datetime.now()

edad_delta = hoy - fecha_nacimiento
edad_en_años = edad_delta.days / 365.25 # Considera años bisiestos
# print(f"Edad aproximada: {int(edad_en_años)} años")

# Programar un evento para el próximo lunes:
hoy = date.today()
dias_para_lunes = (0 - hoy.weekday() + 7) % 7 # 0 es Lunes
proximo_lunes = hoy + timedelta(days=dias_para_lunes)
# print(f"El próximo lunes será: {proximo_lunes.strftime('%d de %B del %Y')}")

