
""" modulo_sesion.py,  para inicio de sesión """

# importamos el modulo limpiar pantalla
from modulo_limpiar_pantalla import limpiar_pantalla
from modulo_conexion_mysql import ConexionMySQL

# Función iniciar sesión.
def iniciar_sesion(usuarios, contraseñas, roles, usuario, contraseña):
    # intentos de inicio de sesión.
    """ intentos_maximos = 3
        intentos = 0
        sesion_exitosa = False

    while intentos < intentos_maximos and not sesion_exitosa:
        print(f'Intento {intentos + 1} de {intentos_maximos}')

        # Entrada de datos por teclado:
        usuario = input('Ingrese Usuario: ')
        contraseña = input('Ingrese Contraseña: ') """
    
    """ Validacion de las listas locales """
    # Estructura condicional:
    try:
        idx = usuarios.index(usuario)
        if contraseña == contraseñas[idx]:
            return roles[idx]
            #limpiar_pantalla()
            #print(f'Inicio de sesión exitoso, bienevenido {usuario}')
            #return True
            #input('\nPresione "ENTER" para continuar...')
            #break
        else:
            #print('Contraseña incorrecta')
            return False
           
    except ValueError:
        print('Usuario no encontrado')
        #return False
        """intentos += 1

        if not sesion_exitosa and intentos > intentos_maximos:
            input('Credenciales no validas, presione "ENTER" para volver a intentar.')"""

        """ Validacion con base de datos MySQL """
        # 2. Si no está en las listas, validar en la base de datos MySQL
        db = ConexionMySQL()  # Usa la instancia singleton con las credenciales del .env
        
        query = "SELECT role FROM usuarios WHERE LOWER(usuario) = %s AND LOWER(contraseña) = %s"
        params = (usuario.lower(), contraseña.lower())
        resultado = db.obtener_datos(query, params)

        if resultado:
            rol_db = resultado[0]["role"]
            print(f"Inicio de sesión exitoso (MySQL): {usuario}")
            return rol_db
        else:
            print("Credenciales incorrectas en base de datos")
            return False