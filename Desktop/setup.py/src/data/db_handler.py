import sqlite3
import os

DB_NAME = "banco_sol.db"

def inicializar_db():
    """Crea la tabla de usuarios con todos los campos necesarios"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # IMPORTANTE: Aquí se define la estructura de la tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            documento TEXT UNIQUE NOT NULL,
            tipo_doc TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            clave TEXT  
        )
    ''')
    conn.commit()
    conn.close()

def registrar_usuario(nombre, documento, tipo, telefono, email, clave):
    """Guarda un nuevo usuario con TODOS sus datos de contacto"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        
        cursor.execute(
            "INSERT INTO usuarios (nombre, documento, tipo_doc, telefono, email, clave) VALUES (?, ?, ?, ?, ?, ?)", 
            (nombre, documento, tipo, telefono, email, clave)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def buscar_usuario(documento):
    """Busca un usuario y devuelve sus datos"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT nombre, documento, telefono, email FROM usuarios WHERE documento = ?", (documento,))
    usuario = cursor.fetchone()
    
    conn.close()
    return usuario 

def obtener_clave(documento):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT clave FROM usuarios WHERE documento = ?", (documento,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return resultado [0] #Devuelve solo el texto de la clave
    return None

def actualizar_contacto(documento, nuevo_telefono=None, nuevo_email=None):
    """Permite editar contacto"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    if nuevo_telefono:
        cursor.execute("UPDATE usuarios SET telefono = ? WHERE documento = ?", (nuevo_telefono, documento))
    
    if nuevo_email:
        cursor.execute("UPDATE usuarios SET email = ? WHERE documento = ?", (nuevo_email, documento))
        
    conn.commit()
    conn.close()
    return True

def actualizar_clave(documento, nueva_clave):
    #Actualiza la clave del usuario
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET clave = ? WHERE documento = ?", (nueva_clave, documento))
    conn.commit()
    conn.close()
    return True