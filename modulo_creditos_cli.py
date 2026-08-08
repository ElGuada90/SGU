##########################
""" Modulo de creditos """
##########################

# importamos modulos
from fechas import fecha_año

# Definir función de créditos
def mostrar_creditos():
    año_actual = fecha_año()
    python_hack = "ElGuada90"

    print(
        '+' + '-' * 42 + '+' + '\n' +
        f'| Copyright © {año_actual} * Hack brand: {python_hack} |' + '\n' +
        '+' + '-' * 42 + '+' + '\n' +
        'Todos los derechos reservados.'
    )

