
from modulo_limpiar_pantalla import limpiar_pantalla
from modulo_creditos import mostrar_creditos
from modulo_registros_datos_cli import registrar_datos, mostrar_registros
from modulo_generador_contraseñas import generar_contraseña
from modulo_inicio_sesion_cli import inicio_sesion

def menu_principal():
    while True:
        limpiar_pantalla()
        # Menu de opciones para el sistema de gestión único
        titulo = (
            '+' + '-' * 30 + '+' + '\n' + 
            '|   Sistema de Gestión Único   |' + '\n' + 
            '+' + '-' * 30 + '+'
        )
        print(titulo)
        print(
            '\n' +
            '         Menu Principal         ' + '\n' +
            '+' + '-' * 30 + '+'
        )
        print("1. Generador de Contraseñas")
        print("2. Modulo | Registro de Datos")
        print("3. Modulo | Consultar Registros")
        print("4. Modulo | Inicio de Sesión")
        print("5. Salir del Sistema")
        print('-' + '-' * 30 + '-')

        opcion = input("Seleccione una opción (1-5): ")

        # Condicionales para cada opción del menú
        if opcion == "1":
            limpiar_pantalla()
            generar_contraseña()
            print("Has seleccionado: Generador de Contraseñas")
            # Aquí puedes agregar la lógica para el generador de contraseñas
        elif opcion == "2":
            limpiar_pantalla()
            registrar_datos()
            print("Has seleccionado: Registro de Datos")
            # Aquí puedes agregar la lógica para el generador de contraseñas
        elif opcion == "3":
            limpiar_pantalla()
            mostrar_registros()
            print("Has seleccionado: Consultar Datos Registrados")
            # Aquí puedes agregar la lógica para el inicio de sesión
            
        elif opcion == "4":
            limpiar_pantalla()
            inicio_sesion()
        elif opcion == "5":
            limpiar_pantalla()
            print("Sesion cerrada. ¡Hasta luego!")
            # Aquí puedes agregar la lógica para salir del sistema
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

            input("Presione Enter para continuar...")

    # derechos de autor
    mostrar_creditos()  

if __name__ == "__main__":
    menu_principal()