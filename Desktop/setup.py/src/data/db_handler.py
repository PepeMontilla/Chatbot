import sqlite3 

#Nombre de la base de datos 
DB_NAME = "chatbot_sol.db"

def inicializar_db():
    """Aqui si la tabla de usuarios no existe se va a crear"""

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor() 

    #Aqui se va a crear la tabla con las siguiente columnas (ID, Nombre, Documento (Cedula/RIF) y tipo (V/E/J))
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            documento TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            tipo_documento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def registrar_usuario(nombre, documento, tipo):
    "Uso try aqui para guardar un usuario nuevo. Me retornara True si salio bien."
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, documento, tipo_documento) VALUES (?, ?, ?)", 
                       (nombre, documento, tipo))
        conn.commit()
        return True
    
    except sqlite3.IntegrityError:
        #Esto va a ocurrir si el documento ya fue registrado para evitar que se repitan la cedula.
        return False
    finally:
        conn.close()

def buscar_usuario(documento):
    #Esta funcion lo que va a ser es buscar si el usuario existe por su documento
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT nombre FROM usuarios WHERE documento = ?", (documento,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado