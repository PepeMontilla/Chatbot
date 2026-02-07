import sys
from src.data import db_handler
from src.core import auth

def mostrar_menu():
    print("\n" + "═"*30)
    print("   MENÚ DE FUNCIONALIDADES")
    print("═"*30)
    print("1. Gestion de Claves")
    print("2. Gestion de Usuario")
    print("3. Salir")
    return input("Seleccione una opcion (1-3): ")

def main():
    #Inicializamos la bd

    db_handler.inicializar_db()
    print("Hola, soy Sol!")
    print("Por favor indicame tus datos de identidad para comenzar.")
    print("(Ejemplos: V-12345678, E-765432189, J-1234567890)")

    usuario_actual = ""

    while True:
        entrada = input("Ingresa tu identificador: ")

        valido, tipo, numero, msg = auth.validar_identificador(entrada)

        if not valido:
            print(msg)
            continue

        documento_final = f"{tipo}-{numero}"
        datos = db_handler.buscar_usuario(documento_final)

        if datos:
            usuario_actual = datos [0]
            print(f"Bienvenido de nuevo!, {usuario_actual}")
            break
        else:
            print("Parece que eres nuevo.")
            nombre = input("Como te llamas?: ")
            if db_handler.registrar_usuario(nombre, documento_final, tipo):
                print("Felicidades te as registrado exitosamente!")
                usuario_actual = nombre
                break
            else:
                print("Error al registrar!")
    #Menu principal
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            print("[Sol]: Gestion de Claves (Proximamente...)")
        elif opcion == '2':
            print(f"[Sol]: Usuario activo: {usuario_actual} ({documento_final})")
        elif opcion == '3':
            print (f"Hasta pronto {usuario_actual}! Esperare tu regreso")
            break
        else:
            print("Opcion no valida:(")



# Punto de entrada del Chatbot
if __name__ == '__main__':
    main()