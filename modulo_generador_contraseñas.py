# Modulo Generador de Contraseña

# Bloque de librerias y dependecias de python
from datetime import datetime
import random, string, os

# Importar Modulos
from modulo_limpiar_pantalla import limpiar_pantalla

# titulo del programa
titulo = (
    '+' + '-' * 30 + '+' + '\n' + 
    '|   Generador de Contraseñas   |' + '\n' + 
    '+' + '-' * 30 + '+'
)

# Función para generar contraseña
def generar_contraseña():
    ''' Generar una contraseña personalizada, según las preferencias
    del usuario '''
    # Bloque 1: Solicitar la cantidad de caracteres.
    while True:
        try:
            print(titulo)
            digitos = int(input('\nIngrese la cantidad de digitos para su contraseña (mínimo 4): '))
            if digitos >= 4:
                break
            else:
                print('\nError: La cantidad de digitos debe ser al menos 4.')
        except ValueError:
            print('\nError: Por favor, ingrese un número entero válido.')

    # Bloque 2: Solicitar el tipo de caracteres a incluir.
    while True:
        print('\nSeleccione el tipo de caracteres a incluir en su contraseña:')
        print('1. Solo letras (mayúsculas y minúsculas)')
        print('2. Solo números')
        print('3. caracteres especiales')
        print('4. Letras y números')
        print('5. Letras y caracteres especiales')
        print('6. Letras, números y caracteres especiales')
        opcion = input('Ingrese el número de su opción (1-6): ')

        if opcion == '1':
            caracteres = string.ascii_letters
            break
        elif opcion == '2':
            caracteres = string.digits
            break
        elif opcion == '3':
            caracteres = string.punctuation
            break
        elif opcion == '4':
            caracteres = string.ascii_letters + string.digits
            break
        elif opcion == '5':
            caracteres = string.ascii_letters + string.punctuation
            break
        elif opcion == '6':
            caracteres = string.ascii_letters + string.digits + string.punctuation
            break
        else:
            print('\nError: Opción no válida. Por favor, seleccione una opción válida.')  

    # Bloque 3: Generar la contraseña utilizando random.choice()
    contraseña = []
    for _ in range(digitos):
        caracter_aleatorio = random.choice(caracteres)
        contraseña.append(caracter_aleatorio)

    # 4 Unir los caracteres para formar la contraseña final
    contraseña_final = ''.join(contraseña)
    print(f'\nSu contraseña generada es: {contraseña_final}')
    input('\nPresione ENTER para continuar...')

# Bucle principal para generar multiples contraseñas
if __name__ == '__main__':
    while True:
        limpiar_pantalla()
        generar_contraseña()

        # Preguntar al usuario si desea generar otra contraseña
        respuesta = input('Desea generar otra contraseña? (s/n): ')
        if respuesta.lower() != 's':
            limpiar_pantalla()
            print('¡Gracias por usar el Generador de Contraseñas! ¡Hasta luego!')
            break