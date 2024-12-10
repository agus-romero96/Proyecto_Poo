import sqlite3
from sqlite3 import Error

def crear_conexion():
    """Crear una conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect('clientes.db')
        return conn
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def crear_tabla():
    """Crear la tabla de clientes si no existe"""
    sql = '''CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT NOT NULL,
                telefono TEXT NOT NULL
            );'''
    
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Error as e:
            print(f"Error al crear la tabla: {e}")
        finally:
            conn.close()

def crear_registro(datos):
    """Crear un nuevo registro de cliente"""
    sql = '''INSERT INTO clientes(nombre, apellido, email, telefono)
             VALUES(?, ?, ?, ?)'''
    
    conn = crear_conexion()
    if conn is None:
        print("Error: No se pudo establecer conexión con la base de datos")
        return False
        
    try:
        cursor = conn.cursor()
        valores = (
            datos['nombre'],
            datos['apellido'],
            datos['email'],
            datos['telefono']
        )
        print(f"Intentando insertar valores: {valores}")  # Debug
        cursor.execute(sql, valores)
        conn.commit()
        print("Registro insertado exitosamente")  # Debug
        return True
    except Error as e:
        print(f"Error detallado al crear el registro: {e}")
        return False
    finally:
        conn.close()
def obtener_registros():
    """Obtener todos los registros de clientes"""
    sql = '''SELECT * FROM clientes'''
    
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            registros = cursor.fetchall()
            return registros
        except Error as e:
            print(f"Error al obtener registros: {e}")
            return []
        finally:
            conn.close()
    return []

def actualizar_registro(id, datos):
    """Actualizar un registro existente"""
    sql = '''UPDATE clientes
             SET nombre = ?, apellido = ?, email = ?, telefono = ?
             WHERE id = ?'''
    
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (
                datos['nombre'],
                datos['apellido'],
                datos['email'],
                datos['telefono'],
                id
            ))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al actualizar el registro: {e}")
            return False
        finally:
            conn.close()
    return False

def eliminar_registro(id):
    """Eliminar un registro"""
    sql = '''DELETE FROM clientes WHERE id = ?'''
    
    conn = crear_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, (id,))
            conn.commit()
            return True
        except Error as e:
            print(f"Error al eliminar el registro: {e}")
            return False
        finally:
            conn.close()
    return False