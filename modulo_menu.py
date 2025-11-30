""" Modulo Menu """

# importar modulos
from modulo_registros import registrar_datos
from modulo_sesion import iniciar_sesion
from modulo_limpiar_pantalla import limpiar_pantalla


#listas para almacenamiento Global
usuarios = []
contraseñas = []
roles = []
nombres = []
apellidos = []
emails = []
telefonos = []
fecha_registro = []


# Función de manú principal
def main():
    while True:
        limpiar_pantalla()
        print('--* Menu Principal *--')
        print('1.Registro de datos.')
        print('2.Iniciar Sesión.')
        print('3.Salir del sistema.')
        print('--------------------')

        opcion = input('\nSelecione opción del menú: ')

        if opcion == '1':
            # 1. Pide los datos de un solo usuario
            # Esto es lo que falta en tu código actual
            usuario = input("Ingrese el nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")
            nombre = input("Ingrese su nombre: ")
            apellido = input("Ingrese su apellido: ")
            email = input("Ingrese su correo electrónico: ")
            telefono = input("Ingrese su número de teléfono: ")
            
            # 2. Ahora, llama a la función con las listas Y los nuevos datos
            resultado = registrar_datos(usuarios, contraseñas, roles, nombres, apellidos, emails, telefonos, fecha_registro, usuario, contraseña, nombre, apellido, email, telefono)
            # Verifica el resultado retornado
            if resultado: # Si 'resultado' tiene un valor (el rol del usuario)
                print(f"Registro de usuario exitoso. ¡Bienvenido, {nombre} {apellido}!")
            else: # Si el resultado es False
                print("Todos los campos son requeridos.")
            
            input('\nPresione "ENTER" para continuar...')
        elif opcion == '2':
            # Pide las credenciales AQUÍ para iniciar sesión
            usuario = input("Ingrese el nombre de usuario: ")
            contraseña = input("Ingrese la contraseña: ")

            resultado = iniciar_sesion(usuarios, contraseñas, roles, usuario, contraseña)

            # Verifica el resultado retornado
            if resultado: # Si 'resultado' tiene un valor (el rol del usuario)
                print(f"Inicio de sesión exitoso. ¡Bienvenido, {usuario}! Tu rol es: {resultado}")
            else: # Si el resultado es False
                print("Usuario o contraseña incorrectos.")
            
            input('\nPresione "ENTER" para continuar...')

        elif opcion == '3':
            limpiar_pantalla()
            print('Salir del sistema, Hasta luego!.')
            break
        else:
            print('Seleccione una opcion valida del 1 - 3')

# Inicializar función
if __name__ == '__main__':
    main()












