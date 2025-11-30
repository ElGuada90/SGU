""" Modulo de registros de usuario """
# Importar librerias

""" importar modulos. """
from modulo_limpiar_pantalla import limpiar_pantalla
from fechas import fecha_24, fecha_12

""" Función registro de datos. """
def registrar_datos(usuarios, 
                    contraseñas, 
                    roles, 
                    nombres, 
                    apellidos, 
                    emails, 
                    telefonos, 
                    fecha_registro, 
                    usuario, 
                    contraseña, 
                    nombre, 
                    apellido, 
                    email, 
                    telefono):
    
    """ while True:
        limpiar_pantalla()
        # Formulario de registro:
        usuario = input('Ingrese Usuario: ')
        contraseña = input('Ingrese Contraseña: ')
        nombre = input('Ingrese Nombre: ')
        apellido = input('Ingrese Apellido: ')
        email = input('Ingrese e-mail: ') """
    
    """ Definimos el formato de fecha y Rol"""
    fecha = fecha_24
    rol = "user"

    """ Metodo append() para agregar los datos a los contenedores. """
    usuarios.append(usuario)
    contraseñas.append(contraseña)
    nombres.append(nombre)
    apellidos.append(apellido)
    emails.append(email)
    telefonos.append(telefono)
    fecha_registro.append(fecha)
    roles.append(rol)
    return True

""" Mensaje de registro exitoso.
    print('Su registro se a guardado exitosamente...')
    break

    input('Presione "ENTER" para continuar...')

if __name__ == '__main__':
    registrar_datos()  """