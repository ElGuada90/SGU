# Modulo inicio de sesion
from modulo_limpiar_pantalla import limpiar_pantalla
from modulo_registros_datos_cli import registros_datos

titulo = (
        '+' + '-' * 29 + '+' + '\n' + 
        '|  Modulo | Inicio de Sesion  |' + '\n' + 
        '+' + '-' * 29 + '+'
    ) 

def inicio_sesion():
    print(titulo)
    # intentos de inicio de sesión.
    intentos_maximos = 3
    intentos = 0
    sesion_exitosa = False

    while intentos < intentos_maximos and not sesion_exitosa:
        print(f'Intento {intentos + 1} de {intentos_maximos}')

        # Entrada de datos por teclado:
        usuario = input('Ingrese Usuario: ')
        contraseña = input('Ingrese Contraseña: ')

        # Estructura condicional:
        if usuario in registros_datos:
            if contraseña == registros_datos[usuario]["contraseña"]:
                limpiar_pantalla()
                print(f'Inicio de sesión exitoso, bienvenido {usuario}')
                input('\nPresione "ENTER" para continuar...')
                return True
            else:
                print('Contraseña incorrecta')
                intentos += 1
        else:
            print('Usuario no encontrado')
            intentos += 1

        if intentos >= intentos_maximos:
            print('Se alcanzó el número máximo de intentos. Su cuenta ha sido bloqueada temporalmente.')
            input('Presione "ENTER" para volver al menú...')
            return False