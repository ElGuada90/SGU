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
        f"Créditos © {año_actual}\nDesarrollado por:{python_hack}\nTodos los derechos reservados."
        )