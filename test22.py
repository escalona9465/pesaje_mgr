import sqlite3
import sys

# Ruta de la base de datos
dbPath = "components/database/pesaje.db"
sys.setrecursionlimit(100000000)

# Conectar a la base de datos
try:
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()

    # Consulta SQL
    query = "SELECT op FROM bobinas"

    # Ejecutar la consulta
    cursor.execute(query)
    
    # Obtener todos los resultados
    table = cursor.fetchall()
    
    # Imprimir los resultados
    print("Query success:", query)
    print(table)

    # Indicar que la consulta fue exitosa
    result = True

except sqlite3.Error as e:
    # Manejar cualquier error que ocurra
    print("Error executing query:", e)
    result = False

finally:
    # Cerrar la conexión a la base de datos
    if connection:
        connection.close()
        print("Database connection closed.")