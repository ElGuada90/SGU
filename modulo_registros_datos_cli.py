
# Creamos un diccionario para almacenar los registros de datos de los usuarios
registros_datos = {}

def registrar_datos():
    titulo = (
        '+' + '-' * 30 + '+' + '\n' + 
        '|  Modulo | Registro de Datos  |' + '\n' + 
        '+' + '-' * 30 + '+'
    )
    print(titulo)
    # input para ingreso de datos por teclado
    usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")
    nombre = input("Ingrese su nombre: ")
    appellido = input("Ingrese su apellido: ")
    correo = input("Ingrese su correo electrónico: ")
    telefono = input("Ingrese su número de teléfono: ")

    # Guardamos los datos ingresados, en el diccionario
    registros_datos[usuario] = {
        "contraseña": contraseña,
        "nombre": nombre,
        "apellido": appellido,
        "correo": correo,
        "telefono": telefono
    }

    print("Datos registrados exitosamente.")
    input("Presione Enter para continuar...")
    return registros_datos

def mostrar_registros():
    titulo = (
        '+' + '-' * 30 + '+' + '\n' + 
        '|  Modulo | Mostrar Registros  |' + '\n' + 
        '+' + '-' * 30 + '+'
    )
    print(titulo)
    if not registros_datos:
        print("No hay registros de datos disponibles.")
    else:
        for usuario, datos in registros_datos.items():
            print(f"Usuario: {usuario}")
            print(f"Nombre: {datos['nombre']} {datos['apellido']}")
            print(f"Correo: {datos['correo']}")
            print(f"Teléfono: {datos['telefono']}")
            print("-" * 30)

    input("Presione Enter para continuar...")