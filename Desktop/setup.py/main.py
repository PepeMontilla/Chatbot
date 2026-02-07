import sys 
from src.data import db_handler
from src.core import auth

# --- FUNCION: LIMPIAR PANTALLA ---

def menu_claves(usuario_actual):
    # Sub menu para la gestion de clave telefonica e internet
    while True:
    

        print("\n" + "=" * 30)
        print("   GESTION DE CLAVES")
        print("=" * 30)
        print("1. Clave Telefonica")
        print("2. Clave Internet")
        print("3. Volver al menu principal")

        opcion = input("\nSelecciona una opcion (1-3): ")

        if opcion == "3":
            break 

        nombre_clave = ""
        if opcion == "1":
            nombre_clave = "Clave Telefonica"
        elif opcion == "2":
            nombre_clave = "Clave Internet"
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")
            continue
            
        # Sub menu (Olvide / Cambiar)
       

        print("-" * 30)
        print(f"   OPCIONES: {nombre_clave.upper()}")
        print("-" * 30)
        print("1. Olvide clave")
        print("2. Cambiar clave")
        print("3. Cancelar")

        sub_opcion = input("\n> Selecciona: ")

        if sub_opcion == "1":
            print(f"\n[Sol]: Olvidaste tu {nombre_clave}? Tranquilo, no te preocupes.")
            print("Solo necesitas tu usuario del banco.")

            inicio = input("\nEmpezamos? (Si/No): ").lower().strip()

            if inicio in ["si", "s", "sí", "y"]:
                verificacion = input("Ingresa tu usuario del banco: ")

                if verificacion.strip().lower() == usuario_actual.lower():
                    print(f"\n✅ EXITO: Usuario verificado correctamente ({usuario_actual}).")
                    print(f"Hemos enviado el codigo de recuperacion a tu correo.")  
                else:
                    print(f"\nERROR: El usuario '{verificacion}' no coincide con nuestros registros.")
                    input("Presiona Enter para continuar...")

        elif sub_opcion == "2":
            print(f"\n[Sol]: Funcion para cambiar {nombre_clave} (Pendiente).")
            input("(Presiona Enter para volver...)")

        elif sub_opcion == "3":
            pass # No hace nada, vuelve al menu anterior
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")


def mostrar_menu():

    print("\n" + "="*30)
    print("   MENU DE FUNCIONALIDADES")
    print("="*30)
    print("1. Gestion de Claves")
    print("2. Gestion de Usuario")
    print("3. Salir")
    return input("\nSeleccione una opcion (1-3): ")

def main():

    db_handler.inicializar_db()
    
    print("Hola, soy Sol!")
    print("Por favor indicame tus datos de identidad para comenzar.")
    print("(Ejemplos: V-12345678, E-765432189, J-1234567890)")

    usuario_actual = ""

    # Bucle de Login
    while True:
        entrada = input("\n> Ingresa tu identificador: ")

        valido, tipo, numero, msg = auth.validar_identificador(entrada)

        if not valido:
            print(msg)
            continue

        documento_final = f"{tipo}-{numero}"
        datos = db_handler.buscar_usuario(documento_final)

        if datos:
            usuario_actual = datos[0]
            print(f"\nBienvenido de nuevo, {usuario_actual}!")
            input("(Presiona Enter para entrar al sistema...)")
            break
        else:
            print("\nParece que eres nuevo.")
            nombre = input("Como te llamas?: ")
            if db_handler.registrar_usuario(nombre, documento_final, tipo):
                print("Felicidades te has registrado exitosamente!")
                usuario_actual = nombre
                input("(Presiona Enter para continuar...)")
                break
            else:
                print("Error al registrar!")

    print(f"\nHola {usuario_actual}! Soy Sol.")

    # Menu principal
    while True:
        opcion = mostrar_menu()
        
        if opcion == '1':
            menu_claves(usuario_actual)
            
        elif opcion == '2':
            print(f"\n[Sol]: Usuario activo: {usuario_actual} ({documento_final})")
            input("(Presiona Enter para volver...)")
            
        elif opcion == '3':
            print(f"\nHasta pronto {usuario_actual}! Esperare tu regreso")
            break
        else:
            print("Opcion no valida.")
            input("(Presiona Enter para intentar de nuevo...)")

if __name__ == '__main__':
    main()